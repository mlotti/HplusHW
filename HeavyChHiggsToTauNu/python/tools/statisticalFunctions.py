from HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRdataInterface import *
from math import sqrt,log
import crosssection

def signif(nSignal,nBackgr,sysErrorBackgr):
    if (sysErrorBackgr > 1 or sysErrorBackgr < 0):
	return 0

    if nBackgr > 0 :
	return sqrt(2*((nSignal+nBackgr*(1+sysErrorBackgr))*log(1+nSignal/(nBackgr*(1+sysErrorBackgr)))-nSignal))
#	return nSignal/sqrt(nBackgr)

    return 0

def signalAtNsigma(nBackgr,sysError,Nsigma):
    nSignal = Nsigma*sqrt(nBackgr) # initial guess
    significance = signif(nSignal,nBackgr,sysError)
    while(abs(significance - Nsigma) > 0.001) :
	nSignal = nSignal - (significance - Nsigma)
	significance = signif(nSignal,nBackgr,sysError)
    return nSignal

def tanbAtNsigma(nSignal,tanbRef,nBackgr,sysError,mHp,mu,Nsigma):
    nSignalAtLimit = signalAtNsigma(nBackgr,sysError,Nsigma)
    xSecAtLimit = signalXsecAtNsigma(nSignal,tanbRef,nSignalAtLimit,mHp,mu)
#    print "check tanbAtNsigma ",nSignalAtLimit,xSecAtLimit
    return tanbForXsec(xSecAtLimit,mHp,tanbRef,mu)

def signalXsecAtNsigma(nSignal,tanbRef,nSignalAtLimit,mHp,mu):
    xSec_atRef = crosssection.whTauNuCrossSectionMSSM(mHp, tanbRef, mu)
    xSec_atLimit = xSec_atRef*nSignalAtLimit/nSignal
#    print "check signalXsecAtNsigma xSec_atRef,xSec_atLimit,nSignalAtLimit,nSignal ",xSec_atRef,xSec_atLimit,nSignalAtLimit,nSignal
    return xSec_atLimit

def tanbForXsec(xSecAtLimit,mHp,tanbRef,mu):

    tanb = tanbRef

    accuracy = 0.001    

    counter = 0
    xSec = crosssection.whTauNuCrossSectionMSSM(mHp,tanb,mu)
    while(abs(xSecAtLimit - xSec)/xSecAtLimit > accuracy and xSec > 0 and tanb < 99 ):
        tanb = tanb + 0.1*(xSecAtLimit - xSec)/xSecAtLimit*tanb
	xSec = crosssection.whTauNuCrossSectionMSSM(mHp,tanb,mu)
	counter = counter+1
	if counter > 10: # to prevent infinite loops
	    counter = 0
	    accuracy = accuracy*2
#        print "       tanbForXsec loop, tanb, xsec ",tanb,xSec
#    print "check tanbForXsec ",tanb
    if tanb > 99 or xSec <= 0:
	return -1
    return tanb

def tanbForXsecLow(xSecAtLimit,mHp,tanbRef,mu):

    tanb = tanbRef
        
    accuracy = 0.001
    
    counter = 0
    xSec = crosssection.whTauNuCrossSectionMSSM(mHp,tanb,mu)
    while(abs(xSecAtLimit - xSec)/xSecAtLimit > accuracy and xSec > 0 and tanb > 1.1 ):
        tanb = tanb - 0.1*(xSecAtLimit - xSec)/xSecAtLimit*tanb
        xSec = crosssection.whTauNuCrossSectionMSSM(mHp,tanb,mu)
        counter = counter+1
        if counter > 10: # to prevent infinite loops
            counter = 0
            accuracy = accuracy*2
    if tanb < 1.1 or xSec <= 0:
        return -1
    return tanb

def tanbForBR(brAtLimit, mHp, tanbRef, mu):
    tanb = tanbRef
    
    br = getBR_top2bHp(mHp, tanb, mu)
    maxIter = 100
    i = 0
    while abs(br - brAtLimit)/brAtLimit > 0.01 and br > 0 and tanb < 219 and i < maxIter:
        i += 1
        tanb_delta = 0.1*(brAtLimit - br)/brAtLimit * tanb
        tanb = tanb + tanb_delta
        br = getBR_top2bHp(mHp, tanb, mu)
#        print "       tanbForBR loop, tanb %f, tanb_delta %f, br %f" % (tanb, tanb_delta, br)
#    print "check tanbForBR ",tanb
    if i >= maxIter:
        print "Maximum number of iterations reached (%d), difference in (br-limit)/limit = %f" % (maxIter, (br-brAtLimit)/brAtLimit)

    if tanb > 219 or br <= 0:
        return -1
    return tanb
#    return tanbForXsec(crosssection.whTauNuCrossSection(brAtLimit, 1), mHp, tanbRef, mu)

def tanbForBRlow(brAtLimit, mHp, tanbRef, mu):
    tanb = tanbRef
    
    br = getBR_top2bHp(mHp, tanb, mu)
    maxIter = 100
    i = 0
    while abs(br - brAtLimit)/brAtLimit > 0.01 and br > 0 and tanb > 1.1 and i < maxIter:
        i += 1
        tanb_delta = 0.1*(brAtLimit - br)/brAtLimit * tanb
        tanb = tanb - tanb_delta
        br = getBR_top2bHp(mHp, tanb, mu)
#        print "       tanbForBR loop, tanb %f, tanb_delta %f, br %f" % (tanb, tanb_delta, br)
#    print "check tanbForBR ",tanb
    if i >= maxIter:
        print "Maximum number of iterations reached (%d), difference in (br-limit)/limit = %f" % (maxIter, (br-brAtLimit)/brAtLimit)

    if tanb < 1.1 or br <= 0:
        return -1
    return tanb
#    return tanbForXsec(crosssection.whTauNuCrossSection(brAtLimit, 1), mHp, tanbRef, mu)

def tanbForTheoryLimit(mHp,mu):
    nTanbs = 0
    lastTanb = 0
    nValidTanbs = 0
    tanbs = hplusBranchingRatio[mHp].keys()
    for tanb in tanbs:
#        print "    check loop tanb ",tanb,getBR_top2bHp(mHp,tanb,mu),mHp,tanb,mu
	nTanbs = nTanbs+1
	if getBR_top2bHp(mHp,tanb,mu) > 0:
	   nValidTanbs = nValidTanbs+1
	   lastTanb = tanb

    if nValidTanbs < nTanbs:
	return lastTanb
    return -1
#    print "check tanbForTheoryLimit ",lastTanb,nTanbs,nValidTanbs

class MassPoint:
    def __init__(self, nSignal, tanb, nBackgr):
        self.nSignal = nSignal
	self.tanbRef = tanb
        self.nBackgr = nBackgr


# Testing
if __name__ == "__main__":
    print "tanbForXsec(10, 120, 20, 200) = %f" % tanbForXsec(10, 120, 20, 200)
    print "tanbForBR(0.2, 120, 20, 200) = %f" % tanbForBR(0.2, 120, 20, 200)
