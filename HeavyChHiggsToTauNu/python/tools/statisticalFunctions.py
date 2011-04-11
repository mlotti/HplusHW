from HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRdataInterface import *
from math import sqrt,log
import crosssection
import BRdataInterface

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
    xSec_atRef = crosssection.whTauNuCrossSection(mHp, tanbRef, mu)
    xSec_atLimit = xSec_atRef*nSignalAtLimit/nSignal
#    print "check signalXsecAtNsigma xSec_atRef,xSec_atLimit,nSignalAtLimit,nSignal ",xSec_atRef,xSec_atLimit,nSignalAtLimit,nSignal
    return xSec_atLimit

def tanbForXsec(xSecAtLimit,mHp,tanbRef,mu):

    tanb = tanbRef

    xSec = crosssection.whTauNuCrossSection(mHp,tanb,mu)
    while(abs(xSecAtLimit - xSec)/xSecAtLimit > 0.001 and xSec > 0 and tanb < 219 ):
        tanb = tanb + 0.1*(xSecAtLimit - xSec)/xSecAtLimit*tanb
	xSec = crosssection.whTauNuCrossSection(mHp,tanb,mu)
#        print "       tanbForXsec loop, tanb, xsec ",tanb,xSec
#    print "check tanbForXsec ",tanb
    if tanb > 219 or xSec <= 0:
	return -1
    return tanb

def tanbForBR(brAtLimit, mHp, tanbRef, mu):
    return tanbForXsec(crosssection.ttCrossSection*brAtLimit, mHp, tanbRef, mu)

def tanbForTheoryLimit(mHp,mu):
    nTanbs = 0
    lastTanb = 0
    nValidTanbs = 0
    tanbs = hplusBranchingRatio[mHp].keys()
    for tanb in tanbs:
#        print "    check loop tanb ",tanb,getBR_top2bHp(mHp,tanb,mu),mHp,tanb,mu
	nTanbs = nTanbs+1
	if BRdataInterface.getBR_top2bHp(mHp,tanb,mu) > 0:
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
