#! /usr/bin/env python3
###############################################################################
#
#	Title   : main.py
#	Author  : Matt Muszynski
#	Date    : 08/18/18
#	Synopsis: pf2 classes
#
###############################################################################

#Import time stuff
from datetime import date, timedelta
#Import array stuff
from numpy import array, hstack, zeros
#Import math stuff
from numpy import exp
#Import random stuff
from numpy.random import normal
#Import plotting stuff
from matplotlib import pyplot as plt
#Import debug and logging stuff
import pdb
import logging
import coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level='debug')


class simScenario:
	def __init__(self):
		self.name = ""
		self.startDate = date(2018, 12, 31)
		self.date = -1
		self.step = 1
		self.fullTime = 365
		self.accounts = []
		self.jobs = []
		self.time = []
		self.netWorth = -1
		self.totalAssets = -1
		self.totalLiabilities = -1
		self.mfRate = 0.09
		self.moneyOut = -1
		self.moneyIn = -1
		self.totalWithdrawls = 0

	def describe(self):
		print("#"*80)
		print('# simScenario: ' + self.name)
		print('#' + '-'*79)
		print('# Accounts:')			
		for account in self.accounts:
			account.describe()
		print('#' + '-'*79)
		print('# Jobs:')			
		for job in self.jobs:
			job.describe()
		print("#"*80)

	def addAccount(self, accounts):
		'''
		addAccount() adds either one account or a list of accounts to
		the simScenario account list.
		'''
		if type(accounts) != list:
			accounts = [accounts]

		for account in accounts:
			self.accounts.append(account)
			account.simScenario = self

	def addJob(self, jobs):
		'''
		addJob() adds either one account or a list of accounts to
		the simScenario account list.
		'''
		if type(jobs) != list:
			jobs = [jobs]

		for job in jobs:
			self.jobs.append(job)
			job.simScenario = self

	def springForce(self,x,k,sigma,mean,restPoint):
		u = normal(mean,sigma)
		return -k*(x - restPoint) + u

	def updateMfRate(self):
		currentRate = self.mfRate[-1]
		change = self.springForce(
			currentRate,
			0.002,  #spring constant
			0.002, #noise std
			0,		#noise mean
			0.09)	#spring zero-stretch point
		return currentRate + change

	#################################################################
	#
	#	Plotting Functions
	#
	#################################################################
	def plotNetWorth(self):
		plt.figure()
		plt.plot(self.totalAssets,color='green')	
		plt.plot(self.netWorth,color='black')
		plt.plot(self.totalLiabilities,color='red')

	def plotMfRate(self):
		plt.figure()
		plt.plot(self.mfRate)

	def showPlots(self):
		plt.show()

	#################################################################
	#
	#	Misc Functions
	#
	#################################################################

	def inputChecks(self):
		return

	#################################################################
	#
	#	Main scenario run function
	#
	#################################################################

	def run(self):
		'''
		Main method of simScenario. Adds a value to the time array
		and a value to each account's balance for each time step
		in the full time of simScenario.
		'''
		#record initial values
		self.mfRate = [self.mfRate]
		for account in self.accounts:
			account.balance = [account.balance]
		self.time = hstack([self.time,0])
		for t in range(1,self.fullTime,self.step):

			#update time variables
			self.date = self.startDate + timedelta(t)
			self.time = hstack([self.time,t])

			#update scenario-wide mutual fund rate
			self.mfRate = hstack([
				self.mfRate,
				self.updateMfRate()])

			#update accounts
			for account in self.accounts:
				try:
					account.balance = hstack(
						[account.balance,account.balance[-1]])
				except TypeError:
					account.balance = array([account.balance])
				account.accrue()

			#make payments
			#for rule in self.payment rules:
			if self.date.day == 1: #pay rent
				logging.debug("Month begin balance for " + \
					self.date.strftime("%B") + ": " + \
					str(self.accounts[0].balance[-1]))
				#this is not the right way to do it, just getting
				#it done quick and dirty so I can move on to other
				#things and get the thing running in the first place.
				logging.debug('Paid rent of $3500 on ' + str(self.date))
				self.accounts[0].withdraw(3500)
				logging.debug('Misc Expenses of $4000 on ' + str(self.date))
				self.accounts[0].withdraw(4000)
				self.accounts[0].transfer(1000, self.accounts[1])

				for account in self.accounts:
					if not(account.asset): account.payMinimum(self.accounts[0])
			#pay biweeky from jobs
			if t%14 == 13:
				for job in self.jobs: job.payday()

		#calculate totals at end of scenario
		self.totalAssets = zeros(len(self.time))
		self.totalLiabilities = zeros(len(self.time))
		for account in self.accounts:
			if account.asset:
				self.totalAssets += account.balance
			else:
				self.totalLiabilities += account.balance

		self.netWorth = self.totalAssets + self.totalLiabilities



class account:
	def __init__(self):
		self.name = ""
		self.balance = 0.0
		self.interestRate = 0.0
		self.simScenario = -1
		self.asset = 1

	def describe(self):
		print("#	" + "-"*30)
		print("#	Name: " + self.name)
		print("#	Balance: " + str(self.balance))
		print("#	Interest Rate: " + str(self.interestRate))

	def transfer(self, amt, toAcct):
		'''
		transfer() is a method for moving money between accounts. Money
		that is transferred stays within the scenario and should be 
		conserved.
		'''
		toAcct.balance[-1] += amt
		self.balance[-1] -= amt
		logging.debug("Transferred $" + str(amt) + " from " + \
			self.name + " to " + toAcct.name + " on " + \
			str(self.simScenario.date))

	def deposit(self,amt):
		'''
		deposit() is a method for adding money from external accounts.
		e.g. jobs or beauty pagaent winnings. Money from deposits come
		from outside the system, so should not expect to be conserved.
		'''
		self.balance[-1] += amt

	def withdraw(self,amt):
		self.balance[-1] -= amt
		self.simScenario.totalWithdrawls += amt

	def payMinimum(self, fromAcct):
		fromAcct.transfer(self.minimumPayment, self)


	def accrue(self):
		'''
		accrue() is a method by which accounts accrue interest. Interest
		is accrued by every account on every time step. If the account
		in question does not accrue interest (like a checking account),
		self.interestRate should be set to zero so accrue will do nothing.
		'''
		if self.interestRate == -1:
			ir = self.simScenario.mfRate[-1]
		else:
			ir = self.interestRate
		self.balance[-1] *= exp(ir*self.simScenario.step/365)

class job:
	def __init__(self):
		self.name = ""
		self.salary = 1000.0
		self.directDeposit = ""
		self.simScenario = -1
		self.withholdingAccount = account()
		self.withholdingAccount.balance = [0]

	def describe(self):
		print("#	" + "-"*30)		
		print("#	Name: " + self.name)
		print("#	Salary: " + str(self.salary))

	def payday(self):
		self.withholdingAccount.deposit(self.withholding)
		logging.debug(self.name + ' paid $' + str(self.withholding) + \
			" to tax withholding on " + str(self.simScenario.date) + ".")

		self.directDeposit.deposit(self.salary - self.withholding)
		logging.debug(self.name + ' paid $' + str(self.salary - self.withholding) + \
			" to " + self.directDeposit.name + "on " + \
			str(self.simScenario.date) + ".")
class expense:
	def __init__(self):
		self.name = ""
		self.mean = -1
		self.std = -1

