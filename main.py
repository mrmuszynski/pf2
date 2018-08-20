#! /usr/bin/env python3
###############################################################################
#
#	Title   : main.py
#	Author  : Matt Muszynski
#	Date    : 08/18/18
#	Synopsis: Wrapper script for pf2
#
###############################################################################

import sys
import pdb

sys.path.insert(0, 'lib')
from pfLib import simScenario, account, job

main = simScenario()
main.name = "Main Simulation"

checking = account()
checking.name = "Checking Account"

savings = account()
savings.name = "Savings Account"
savings.interestRate = .10
savings.balance = 100.

################################################################################
#
#	Define Credit Card Account
#
################################################################################
creditCard = account()
creditCard.name = "Credit Card"
creditCard.balance = 6417.63
creditCard.asset = 0
creditCard.interestRate = 0.1999

################################################################################
#
#	Define Jenny's Loan Accounts
#
################################################################################
jSM = account()
jNav1_01 = account()
jNav1_02 = account()
jNav1_03 = account()
jNav1_04 = account()

jSM.name = "Sallie Mae Private (JLK)"
jNav1_01.name = "1-01 Direct S (JLK)"
jNav1_02.name = "1-02 Direct U (JLK)"
jNav1_03.name = "1-03 Direct S (JLK)"
jNav1_04.name = "1-04 Direct U (JLK)"

jSM.balance = -45572.47 #as of 08/19/18
jNav1_01.balance = -3537.00 #as of 08/19/18
jNav1_02.balance = -7115.07 #as of 08/19/18
jNav1_03.balance = -8243.25 #as of 08/19/18
jNav1_04.balance = -4000.00 #as of 08/19/18

jSM.minimumPayment = 587
jNav1_01.minimumPayment = 36
jNav1_02.minimumPayment = 72
jNav1_03.minimumPayment = 86
jNav1_04.minimumPayment = 41

jSM.asset = 0
jNav1_01.asset = 0
jNav1_02.asset = 0
jNav1_03.asset = 0
jNav1_04.asset = 0

jSM.interestRate = 0.09375
jNav1_01.interestRate = 0.0386
jNav1_02.interestRate = 0.0386
jNav1_03.interestRate = 0.0466
jNav1_04.interestRate = 0.0429

################################################################################
#
#	Define Matt's Loan Accounts
#
################################################################################

mSM = account()
mNav1_01 = account()
mNav1_02 = account()
mNav1_03 = account()
mNav1_04 = account()

mSM.name = "Sallie Mae Private (MRM)"
mNav1_01.name = "1-04 Direct S (MRM)"
mNav1_02.name = "1-05 Direct U (MRM)"
mNav1_03.name = "1-06 Direct S (MRM)"
mNav1_04.name = "1-07 Direct U (MRM)"

mSM.balance = -37604.97 #as of 08/19/18
mNav1_01.balance = -3537.37 #as of 08/19/18
mNav1_02.balance = -7112.79 #as of 08/19/18
mNav1_03.balance = -5500.00 #as of 08/19/18
mNav1_04.balance = -3933.79 #as of 08/19/18

mSM.minimumPayment = 399 #figured on 5% interest for 10 years
mNav1_01.minimumPayment = 36
mNav1_02.minimumPayment = 72
mNav1_03.minimumPayment = 56
mNav1_04.minimumPayment = 41

mSM.asset = 0
mNav1_01.asset = 0
mNav1_02.asset = 0
mNav1_03.asset = 0
mNav1_04.asset = 0

mSM.interestRate = 0.04375 #as of 08/19/18
mNav1_01.interestRate = 0.0386
mNav1_02.interestRate = 0.0386
mNav1_03.interestRate = 0.0429
mNav1_04.interestRate = 0.0466

################################################################################
#
#	Define Putnam/MFS Funds
#
################################################################################


putnamMF = account()
putnamMF.name = "Putnam Mutual Funds"
putnamMF.balance = 83155.53 #as of 08/19/18
putnamMF.asset = 1
putnamMF.interestRate = -1 #follows "spring-force" market rate

putnamIRA = account()
putnamIRA.name = "Putnam IRA"
putnamIRA.balance = 18182.18 #as of 08/19/18
putnamIRA.asset = 1
putnamIRA.interestRate = -1 #follows "spring-force" market rate

MFSMF = account()
MFSMF.name = "MFS Mutual Funds"
MFSMF.balance = 52152.83 #as of 08/19/18
MFSMF.asset = 1
MFSMF.interestRate = -1 #follows "spring-force" market rate

MFSIRA = account()
MFSIRA.name = "MFS IRA"
MFSIRA.balance = 13578.89 #as of 08/19/18
MFSIRA.asset = 1
MFSIRA.interestRate = -1 #follows "spring-force" market rate

jJPL = job()
jJPL.name = "JPL (Jenny)"
jJPL.directDeposit = checking
jJPL.salary = 3860. - 104
jJPL.withholding = 1064.

mJPL = job()
mJPL.name = "JPL (Matt)"
mJPL.directDeposit = checking
mJPL.salary = 3760. - 104.
mJPL.withholding = 825.

main.addAccount([
	checking,
	savings,
	jSM,
	jNav1_01,
	jNav1_02,
	jNav1_03,
	jNav1_04,
	mSM,
	mNav1_01,
	mNav1_02,
	mNav1_03,
	mNav1_04
	])
main.addJob([jJPL,mJPL])

main.run()
main.plotNetWorth()
main.plotMfRate()
main.showPlots()

pdb.set_trace()