#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.LimitCalc..BRXSDatabaseInterface as BRXSDB

import os
import sys
import math

_linearSummingForTheoryUncertainties = True
_minTanBeta = 1.1
_minTanBeta = 10
_maxTanBeta = 60.0

myScenarios = ["mhmaxup", "mhmodm", "mhmodp", "lightstau", "lightstop", "tauphobic"]
myMassPoints = ["200","220","250","300","400","500","600"]

class MyMinMax:
    def __init__(self, label):
        self._plusmin = 9999.0
        self._plusmax = -1.0
        self._minusmin = 9999.0
        self._minusmax = -1.0
        self._label = label
    
    def update(self, plus, minus):
        self._plusmin = min(self._plusmin, plus)
        self._plusmax = max(self._plusmax, plus)
        self._minusmin = min(self._minusmin, minus)
        self._minusmax = max(self._minusmax, minus)
    
    def output(self):
        print "%s: plus range = %.3f-%.3f, minus range = %.3f-%.3f"%(self._label, self._plusmin, self._plusmax, self._minusmin, self._minusmax)

def main(scen):
    # Create data members
    xsec = MyMinMax("xsection")
    brtaunuonly = MyMinMax("Br(Hp->taunu) alone")
    brtaunu = MyMinMax("Br(Hp->taunu)")
    brtb = MyMinMax("Br(Hp->tb)")
    myData = [xsec, brtaunuonly, brtaunu, brtb]
  
    # Open scenario
    myDbInputName = "%s-LHCHXSWG.root"%scen
    if not os.path.exists(myDbInputName):
        raise Exception("Error: Cannot find file '%s'!"%myDbInputName)
    db = BRXSDB.BRXSDatabaseInterface(myDbInputName, silentStatus=True)
    # Loop over mass points    
    for m in myMassPoints:
        print "Scanning tan beta points for m=%s"%m
        # Loop over tan beta range
        tb = _minTanBeta
        while tb < _maxTanBeta:
            xsecminus = db.xsecUncertOrig("mHp", "tanb", "", int(m), tb, "-")
            xsecplus = db.xsecUncertOrig("mHp", "tanb", "", int(m), tb, "+")
            xsec.update(xsecplus, xsecminus)
            # taunu alone
            myDecayModeKeys = ["BR_Hp_taunu"]
            myBrUncert = db.brUncert("mHp", "tanb", myDecayModeKeys, m, tb, linearSummation=_linearSummingForTheoryUncertainties, silentStatus=True)
            taunuSum = 0.0
            for k in myBrUncert.keys():
                if myDecayModeKeys[0] in k:
                    if _linearSummingForTheoryUncertainties:
                        taunuSum += myBrUncert[k]
                    else:
                        taunuSum = math.sqrt(taunuSum**2 + myBrUncert[k]**2)
            brtaunuonly.update(taunuSum, taunuSum)
            # taunu and tb uncert
            myDecayModeKeys = ["BR_Hp_taunu", "BR_Hp_tb"]
            myBrUncert = db.brUncert("mHp", "tanb", myDecayModeKeys, m, tb, linearSummation=_linearSummingForTheoryUncertainties, silentStatus=True)
            taunuSum = 0.0
            tbSum = 0.0
            for k in myBrUncert.keys():
                if myDecayModeKeys[0] in k:
                    if _linearSummingForTheoryUncertainties:
                        taunuSum += myBrUncert[k]
                    else:
                        taunuSum = math.sqrt(taunuSum**2 + myBrUncert[k]**2)
                if myDecayModeKeys[1] in k:
                    if _linearSummingForTheoryUncertainties:
                        tbSum += myBrUncert[k]
                    else:
                        tbSum = math.sqrt(tbSum**2 + myBrUncert[k]**2)
            brtaunu.update(taunuSum, taunuSum)
            brtb.update(tbSum, tbSum)
            if tb < 10:
                tb += 0.1
            else:
                tb += 1
    # Print result
    print "\nTheoretical uncertainty ranges (%s):"%(scen)
    print "Linear summing of uncertainties:",_linearSummingForTheoryUncertainties
    print "Tan beta range=%.1f-%.1f"%(_minTanBeta, _maxTanBeta)
    for item in myData:
        item.output()
    print ""
    # Something in memory management leaks - the following helps dramatically to recude the leak
    ROOT.gROOT.CloseFiles()
    ROOT.gROOT.GetListOfCanvases().Delete()
    ROOT.gDirectory.GetList().Delete()

if __name__ == "__main__":
   for scen in myScenarios:
      main(scen)
