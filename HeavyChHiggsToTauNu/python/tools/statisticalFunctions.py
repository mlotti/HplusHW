from HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRdataInterface import *
from math import sqrt,log

def signif(nSignal,nBackgr,sysErrorBackgr):
    if (sysErrorBackgr > 1 or sysErrorBackgr < 0):
	return 0

    if nBackgr > 0 :
	return sqrt(2*((nSignal+nBackgr)*log(1+nSignal/(nBackgr*(1+sysErrorBackgr)))-nSignal))
#	return nSignal/sqrt(nBackgr)

    return 0

def signalAtNsigma(nBackgr,sysError,Nsigma):
    nSignal = Nsigma*sqrt(nBackgr) # initial guess
    significance = signif(nSignal,nBackgr,sysError)
    while(abs(significance - Nsigma) > 0.001) :
	nSignal = nSignal - (significance - Nsigma)
	significance = signif(nSignal,nBackgr,sysError)
    return nSignal


class MassPoint:
    def __init__(self, nSignal, tanb, nBackgr):
        self.nSignal = nSignal
	self.tanbRef = tanb
        self.nBackgr = nBackgr

