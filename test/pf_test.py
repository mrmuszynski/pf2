#! /usr/bin/env python3
###############################################################################
#
#	Title   : pf_tests.py
#	Author  : Matt Muszynski
#	Date    : 01/13/18
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################

#Import pf library
import sys
sys.path.insert(0, 'lib')
from pfLib import simScenario, account, job
#Import math stuff
from numpy import exp

import pdb

###############################################################################
#
#	Create Scenario
#
###############################################################################

checking = account()
checking.name = "Checking Account"

savings = account()
savings.name = "Savings Account"
savings.interestRate = .10
savings.balance = 100.

job = job()
job.name = "My First Job"
job.directDeposit = checking

main = simScenario()
main.name = "Main Simulation"
main.addAccount([checking, savings])
main.addJob(job)
main.step = 1
main.fullTime = 366

main.run()
print(main.time)

def test_accrue_and_payday():
	assert( checking.balance[-1] == 26000)
	assert( abs(savings.balance[-1] - 100*exp(0.1)) < 1e-12)








