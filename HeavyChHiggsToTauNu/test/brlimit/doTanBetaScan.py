#!/usr/bin/env python

# Produces jobs for calculating tan beta limits
# Strategy:
# 1) loop over m_Hp, tan beta, and MSSM models
# 2) scale signal to Br(H+ -> X) of the model
# 3) calculate limit on sigma_Hp for that point
# 4) if sigma is lower than MSSM sigma_Hp, then point is excluded

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CombineTools as combine
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as commonLimitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRXSDatabaseInterface as BRXSDB
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

import os
import sys
import array
import math


_resultFilename = "results.txt"
_maxTanBeta = 69.0
_minBrTanBeta = 8.0
_linearSummingForTheoryUncertainties = True # LHCHXSWG recommendation True
_separateTheoreticalXsectionAndBrUncertainties = False # LHCHXSWG recommendation False (because of correlations)

class TanBetaResultContainer:
    def __init__(self, mssmModel, massPoints):
        self._mssmModel = mssmModel
        self._massPoints = massPoints[:]
        self._resultKeys = []
        self._resultsLow = {} # dictionary, where key is resultKey and values are dictionaries of tan beta limits for masses
        self._resultsHigh = {} # dictionary, where key is resultKey and values are dictionaries of tan beta limits for masses

    def addLowResult(self, mass, resultKey, tanbetalimit):
        if not resultKey in self._resultKeys:
            self._resultKeys.append(resultKey)
        if not resultKey in self._resultsLow.keys():
            self._resultsLow[resultKey] = {}
            for m in self._massPoints:
                self._resultsLow[resultKey][m] = -1.0
        if tanbetalimit != None:
            #if mass in self._resultsLow[resultKey].keys():
            #    print "Warning: overriding low limit for (%s) / m=%s / %s"%(self._mssmModel, mass, resultKey)
            if tanbetalimit < 10:
                self._resultsLow[resultKey][mass] = tanbetalimit
            #self._resultsLow[resultKey][mass] = -1.0

    def addHighResult(self, mass, resultKey, tanbetalimit):
        if not resultKey in self._resultKeys:
            self._resultKeys.append(resultKey)
        if not resultKey in self._resultsHigh.keys():
            self._resultsHigh[resultKey] = {}
            for m in self._massPoints:
                self._resultsHigh[resultKey][m] = _maxTanBeta
        if tanbetalimit != None:
            #if mass in self._resultsHigh[resultKey].keys():
            #    print "Warning: overriding low limit for (%s) / m=%s / %s"%(self._mssmModel, mass, resultKey)
            self._resultsHigh[resultKey][mass] = tanbetalimit
        
    def _getResultGraphForTwoKeys(self, firstKey, secondKey):
        if not firstKey in self._resultsLow.keys() or not secondKey in self._resultsLow.keys():
            return None
        lenm = len(self._massPoints)
        g = ROOT.TGraph(lenm*4+2)
        # Low limit, bottom pass left to right
        for i in range(0, lenm):
	    a = self._resultsLow[firstKey][self._massPoints[i]]
	    if a < 0:
		g.SetPoint(i, float(self._massPoints[i]), _minBrTanBeta)
	    else:
		g.SetPoint(i, float(self._massPoints[i]), a)
        # Low limit, top pass right to left
        for i in range(0, lenm):
            j = lenm - i - 1
            a = self._resultsLow[secondKey][self._massPoints[j]]
            if a < 0:
		g.SetPoint(i+lenm, float(self._massPoints[j]), _minBrTanBeta)
	    else:
		g.SetPoint(i+lenm, float(self._massPoints[j]), a)
        # intermediate points
        g.SetPoint(lenm*2, -1.0, self._resultsLow[secondKey][self._massPoints[lenm-1]])
        g.SetPoint(lenm*2+1, -1.0, self._resultsHigh[firstKey][self._massPoints[0]])
        # Upper limit, bottom pass left to right
        for i in range(0, lenm):
	    a = self._resultsHigh[firstKey][self._massPoints[i]]
	    if a == _maxTanBeta:
		g.SetPoint(i+lenm*2+2, float(self._massPoints[i]), _minBrTanBeta)
	    else:
		g.SetPoint(i+lenm*2+2, float(self._massPoints[i]), a)
        # Upper limit, top pass right to left
        for i in range(0, lenm):
            j = lenm - i - 1
            a = self._resultsHigh[secondKey][self._massPoints[j]]
            if a == _maxTanBeta:
		g.SetPoint(i+lenm*3+2, float(self._massPoints[j]), _minBrTanBeta)
	    else:
		g.SetPoint(i+lenm*3+2, float(self._massPoints[j]), a)
        return g

    def _getResultGraphForOneKey(self, resultKey):
        if not resultKey in self._resultsLow.keys():
            return None
        lenm = len(self._massPoints)
        g = ROOT.TGraph(lenm*2+4)
        # Upper limit, top part left to right
        g.SetPoint(0, -1.0, 90.0)
        g.SetPoint(1, 1000.0, 90.0)
        # Upper limit, pass right to left
        offset = 0
        previousPointExcludedStatus = False
        for i in range(0, lenm):
            j = lenm - i - 1
            a = self._resultsHigh[resultKey][self._massPoints[j]]
            if a == _maxTanBeta:
		if not previousPointExcludedStatus:
		    g.SetPoint(i+2+offset, float(self._massPoints[j]), _minBrTanBeta)
		    offset += 1
		else:
		    offset -= 1
		previousPointExcludedStatus = True
	    else:
		g.SetPoint(i+2+offset, float(self._massPoints[j]), a)
        # intermediate points
        if previousPointExcludedStatus:
	    #g.SetPoint(lenm+2+offset, -1.0, _minBrTanBeta)
	    #g.SetPoint(lenm+3+offset, -1.0, _minBrTanBeta)
	    offset -= 2
	else:
	    g.SetPoint(lenm+2+offset, -1.0, self._resultsLow[resultKey][self._massPoints[lenm-1]])
	    g.SetPoint(lenm+3+offset, -1.0, self._resultsHigh[resultKey][self._massPoints[0]])
        # Low limit, pass left to right
        previousPointExcludedStatus = False
        for i in range(0, lenm):
	    a = self._resultsLow[resultKey][self._massPoints[i]]
	    if a < 0:
		offset -= 1
		previousPointExcludedStatus = True
	    else:
		if previousPointExcludedStatus:
		    previousPointExcludedStatus = False
		    #g.SetPoint(i+lenm+3+offset, float(self._massPoints[j-1]), _minBrTanBeta)
		    #offset += 1
		g.SetPoint(i+lenm+3+offset, float(self._massPoints[i]), a)
        # Low limit, bottom part right to left
        g.SetPoint(lenm*2+3+offset, 1000.0, 0.0)
        g.SetPoint(lenm*2+4+offset, -1.0, 0.0)
        return g

    def doPlot(self):
        graphs = {}
        #["observed", "observedPlusTheorUncert", "observedMinusTheorUncert", "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]
        graphs["exp"] = self._getResultGraphForOneKey("expected")
        graphs["exp1"] = self._getResultGraphForTwoKeys("expectedPlus1Sigma", "expectedMinus1Sigma")
        graphs["exp2"] = self._getResultGraphForTwoKeys("expectedPlus2Sigma", "expectedMinus2Sigma")
        graphs["obs"] = self._getResultGraphForOneKey("observed")
        myName = "%s-LHCHXSWG.root"%self._mssmModel
        if not os.path.exists(myName):
            raise Exception("Error: Cannot find file '%s'!"%myName)
        db = BRXSDB.BRXSDatabaseInterface(myName)
        graphs["Allowed"] = db.mhLimit("mh","mHp","mHp > 0","125.0+-3.0")
        db.close()
        if self._mssmModel == "tauphobic":
            ## Fix a buggy second upper limit (the order of points is left to right, then right to left; remove further passes to fix the bug)
            #decreasingStatus = False
            #i = 0
            #while i < graphs["Allowed"].GetN():
                #removeStatus = False
                #y = graphs["Allowed"].GetY()[i]
                #if i > 0:
                    #if graphs["Allowed"].GetY()[i-1] - y < 0:
                        #decreasingStatus = True
                    #else:
                        #if decreasingStatus:
                            #graphs["Allowed"].RemovePoint(i)
                            #removeStatus = True
                #if not removeStatus:
                    #i += 1
            #for i in range(0, graphs["Allowed"].GetN()):
                #print graphs["Allowed"].GetX()[i], graphs["Allowed"].GetY()[i]
            ## Fix m=500 and m=600
            n = graphs["Allowed"].GetN()
            graphs["Allowed"].SetPoint(n-2, 500, 4.77)
            graphs["Allowed"].SetPoint(n-1, 600, 4.71)
        myFinalStateLabel = []
        if float(self._massPoints[0]) < 179:
	    myFinalStateLabel.append("^{}H^{+}#rightarrow#tau^{+}#nu_{#tau}, ^{}#tau_{h}+jets final state")
	else:
	    myFinalStateLabel.append("^{}H^{+}#rightarrow#tau^{+}#nu_{#tau} final states:")
	    myFinalStateLabel.append("  ^{}#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu")
	    myFinalStateLabel.append("^{}H^{+}#rightarrowt#bar{b} final states:")
	    myFinalStateLabel.append("  ^{}#mu#tau_{h}, ee, e#mu, #mu#mu")
        if float(self._massPoints[0]) < 179:
            limit.doTanBetaPlotGeneric("tanbeta_%s_light"%self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="light")
        else:
            limit.doTanBetaPlotGeneric("limitsTanbCombination_heavy_"+self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="combination")
                                                                           
class BrContainer:
    def __init__(self, decayModeMatrix, mssmModel, massPoints):
        self._decayModeMatrix = decayModeMatrix
        self._mssmModel = mssmModel
        self._massPoints = massPoints
        self._separateTheoreticalXsectionAndBrUncertainties = _separateTheoreticalXsectionAndBrUncertainties
        self._results = {} # dictionary, where key is tan beta
        # Make dictionary of key labels
        self._brkeys = {}
        for fskey in self._decayModeMatrix.keys():
            for dmkey in self._decayModeMatrix[fskey].keys():
                if dmkey not in self._brkeys:
                    self._brkeys[dmkey] = array.array('d',[0])

    def getDatacardPatterns(self):
        myList = []
        for fskey in self._decayModeMatrix.keys():
            # Get only the first decay mode key 
            myFirstDMKey = self._decayModeMatrix[fskey].keys()[0]
            myList.append(self._decayModeMatrix[fskey][myFirstDMKey][0])
        return myList
      
    def getRootfilePatterns(self):
        myList = []
        for fskey in self._decayModeMatrix.keys():
            # Get only the first decay mode key 
            myFirstDMKey = self._decayModeMatrix[fskey].keys()[0]
            myList.append(self._decayModeMatrix[fskey][myFirstDMKey][1])
        return myList

    def _readFromDatabase(self, mHp, tanbeta):
        #if not os.path.exists(self._datacardPatterns[0]%mHp):
        #    raise Exception("Error: no support for template morphing between mass points; use one of the mass points!")
        # Open model root file
        myRootFilename = "%s-LHCHXSWG.root"%self._mssmModel
        if not os.path.exists(myRootFilename):
            raise Exception("Error: The root file '%s' for the MSSM model does not exist in this directory!"%myRootFilename)
        # Open root file and obtain branch
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        f = ROOT.TFile.Open(myRootFilename)
        ROOT.gErrorIgnoreLevel = backup
        _treename = "FeynHiggs_results"
        myTree = f.Get(_treename)
        if myTree == None:
            f.Close()
            raise Exception("Error: Could not find tree '%s' in root file '%s'!"%(_treename, myRootFilename))
        # Set branch adresses for reading
        mHpInTree = array.array('d',[0])
        tanbInTree = array.array('d',[0])
        sigmaInTree = array.array('d',[0])
        brTBHInTree = array.array('d',[0])
        myTree.SetBranchAddress("mHp", mHpInTree)
        myTree.SetBranchAddress("tanb", tanbInTree)
        myTree.SetBranchAddress("tHp_xsec", sigmaInTree)
        myTree.SetBranchAddress("BR_tHpb", brTBHInTree)
        # Set branch adresses for branching keys
        for brkey in self._brkeys.keys():
            myBrLabel = "BR_%s"%brkey
            if myTree.GetBranch(myBrLabel) == None:
                raise Exception("Error: Could not find branch by name '%s' in root tree '%s' in root file '%s'!"%(myBrLabel, _treename, myRootFilename))
            myTree.SetBranchAddress(myBrLabel, self._brkeys[brkey])
        # Find values from root database
        myTanBetaValueFoundStatus = False
        myFoundMassStatus = False
        i = 0
        nentries = myTree.GetEntries()
        while i < nentries and not myFoundMassStatus:
            myTree.GetEvent(i)
            if abs(tanbInTree[0] - float(tanbeta)) < 0.0001:
                myTanBetaValueFoundStatus = True
                if abs(mHpInTree[0] - float(mHp)) < 0.0001:
                    myFoundMassStatus = True
            i += 1
        f.Close()
        if not myTanBetaValueFoundStatus:
            print "Warning: Could not find tan beta value %f in '%s'!"%(tanbeta, myRootFilename)
        if not myFoundMassStatus:
            print "Warning: Could not find mass value %s in '%s'!"%(mHp, myRootFilename)
        # Found branching and sigma, store them
        tblabel = "%s_%04.1f"%(mHp, tanbeta)
        self._results[tblabel] = {}
        if not myTanBetaValueFoundStatus or not myFoundMassStatus:
            for brkey in self._brkeys.keys():
                self._results[tblabel]["%sTheory"%brkey] = None
            self._results[tblabel]["sigmaTheory"] = None
        else:
            for brkey in self._brkeys.keys():
                self._results[tblabel]["%sTheory"%brkey] = self._brkeys[brkey][0]
            if float(mHp) > 179:
                self._results[tblabel]["sigmaTheory"] = sigmaInTree[0]*2.0*0.001 # fb->pb; xsec is in database for only H+, factor 2 gives xsec for Hpm
            else:
                self._results[tblabel]["sigmaTheory"] = brTBHInTree[0] # Br(t->bH+) for light H+
        self._results[tblabel]["combineResult"] = None
        
        s = "  - m=%s, tanbeta=%.1f: "%(mHp, tanbeta)
        if not myTanBetaValueFoundStatus or not myFoundMassStatus:
            s += "Failed to found theor. input!"
        else:
            s += "sigma_theor=%f pb"%(self._results[tblabel]["sigmaTheory"])
            for brkey in self._brkeys.keys():
                s += ", Br(%s)=%f"%(brkey, self._brkeys[brkey][0])
        print s

    def produceScaledCards(self, mHp, tanbeta):
        if self.resultExists(mHp, tanbeta):
            return
        # Obtain branching and sigma from MSSM model database
        self._readFromDatabase(mHp, tanbeta)
        if self._results["%s_%04.1f"%(mHp,float(tanbeta))]["sigmaTheory"] == None:
            return
        
        #print "    Scaled '%s/%s' signal in datacards by branching %f (mHp=%s, tanbeta=%.1f)"%(mySignalScaleFactor, mHp, tanbeta)
        # Obtain theoretical uncertinties from MSSM model database
        myDbInputName = "%s-LHCHXSWG.root"%self._mssmModel
        if not os.path.exists(myDbInputName):
            raise Exception("Error: Cannot find file '%s'!"%myDbInputName)
        # Scale datacards
        myResult = self.getResult(mHp, tanbeta)
        for fskey in self._decayModeMatrix.keys():
            print "    . final state %10s:"%fskey
            myOriginalRates = []
            myPrimaryReader = None
            for dmkey in self._decayModeMatrix[fskey].keys():
                myDatacardPattern = self._decayModeMatrix[fskey][dmkey][0]
                myRootFilePattern = self._decayModeMatrix[fskey][dmkey][1]
                if myRootFilePattern != None:
                    mySignalScaleFactor = myResult["%sTheory"%dmkey]
                    # Leave reader for first key open
                    if dmkey == self._decayModeMatrix[fskey].keys()[0]:
                        myPrimaryReader = DatacardReader.DataCardReader(".", mHp, myDatacardPattern, myRootFilePattern, rootFileDirectory="", readOnly=False)
                        myPrimaryReader.scaleSignal(mySignalScaleFactor)
                        myOriginalRates.append(float(myPrimaryReader.getRateValue(myPrimaryReader.getDatasetNames()[0])))
                        #print fskey,dmkey,myOriginalRates[len(myOriginalRates)-1]
                    else:
                        # Scale according to br and add signal to primary (i.e. only one datacard for the decay modes)
                        myReader = DatacardReader.DataCardReader(".", mHp, myDatacardPattern, myRootFilePattern, rootFileDirectory="", readOnly=False)
                        myReader.scaleSignal(mySignalScaleFactor)
                        myOriginalRates.append(float(myReader.getRateValue(myReader.getDatasetNames()[0])))
                        #print fskey,dmkey,myOriginalRates[len(myOriginalRates)-1]
                        myPrimaryReader.addSignal(myReader)
                        myReader.close()
                        # Remove datacard from current directory so that it is not used for limit calculation (a copy of them is at originalDatacards directory)
                        if os.path.exists(myDatacardPattern%mHp):
                            os.system("rm %s"%(myDatacardPattern%mHp))
                            os.system("rm %s"%(myRootFilePattern%mHp))
            if myPrimaryReader != None:
                mySignalColumnName = myPrimaryReader.getDatasetNames()[0]
                myUpdatedRate = float(myPrimaryReader.getRateValue(myPrimaryReader.getDatasetNames()[0]))
                myTheorUncertPrefix = "theory_"
                # Add theoretical cross section uncertainties to datacard 
                db = BRXSDB.BRXSDatabaseInterface(myDbInputName, silentStatus=True)
                myXsecUncert = [0.0, 0.0]
                if float(mHp) > 179:
                    myXsecUncert = [db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "-"),
                                    db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "+")]
                    if self._separateTheoreticalXsectionAndBrUncertainties:
                        myNuisanceName = "%sxsectionHp"%myTheorUncertPrefix
                        myUncertValueString = "%.3f/%.3f"%(1.0-myXsecUncert[0], 1.0+myXsecUncert[1])
                        myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueString)
                        print "      . H+ xsec uncert: %s"%myUncertValueString
                else:
                    self._separateTheoreticalXsectionAndBrUncertainties = True
                # Add theoretical branching ratio uncertainties to datacard (depends on how many decay modes are combined)
                myDecayModeKeys = self._decayModeMatrix[fskey].keys()
                for i in range(len(myDecayModeKeys)):
                    myDecayModeKeys[i] = "BR_%s"%myDecayModeKeys[i]
                myBrUncert = None
                if float(mHp) < 179:
                    myBrUncert = db.brUncertLight("mHp", "tanb", myDecayModeKeys, mHp, tanbeta, linearSummation=_linearSummingForTheoryUncertainties, silentStatus=True)               
                else:
                    myBrUncert = db.brUncertHeavy("mHp", "tanb", myDecayModeKeys, mHp, tanbeta, linearSummation=_linearSummingForTheoryUncertainties, silentStatus=True)
                for i in range(len(myDecayModeKeys)):
                    for k in myBrUncert.keys():
                        if myDecayModeKeys[i] in k:
                            # Scale uncertainty according to amount of signal from that decay mode
                            myUncertValue = myBrUncert[k] * myOriginalRates[i] / myUpdatedRate
                            if self._separateTheoreticalXsectionAndBrUncertainties:
                                myNuisanceName = "%s%s"%(myTheorUncertPrefix,k)
                                myUncertValueString = "%.3f"%(1.0+myUncertValue)
                                if float(mHp) < 179 and ("HH" in mySignalColumnName or "ttHpHp" in mySignalColumnName):
                                    # Add for HH
                                    myUncertValueStringHH = "%.3f"%(1.0+myUncertValue*2.0)
                                    myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueStringHH)
                                    # Add for HW
                                    myPrimaryReader.addNuisance(myNuisanceName, "lnN", myPrimaryReader.getDatasetNames()[1], myUncertValueString)
                                    print "      . H+ HH Br uncert(%s): %s"%(k, myUncertValueStringHH)
                                    print "      . H+ HW Br uncert(%s): %s"%(k, myUncertValueString)
                                else:
                                    myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueString)
                                    print "      . H+ Br uncert(%s): %s"%(k, myUncertValueString)
                            else:
                                if _linearSummingForTheoryUncertainties:
                                    myXsecUncert[0] += myUncertValue
                                    myXsecUncert[1] += myUncertValue
                                else:
                                    myXsecUncert[0] = math.sqrt(myXsecUncert[0]**2 + myUncertValue**2)
                                    myXsecUncert[1] = math.sqrt(myXsecUncert[1]**2 + myUncertValue**2)
                if not self._separateTheoreticalXsectionAndBrUncertainties:
                    myNuisanceName = "%sxsectionHp_and_Br"%myTheorUncertPrefix
                    myUncertValueString = "%.3f/%.3f"%(1.0-myXsecUncert[0], 1.0+myXsecUncert[1])
                    myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueString)
                    print "      . %s: %s"%(myNuisanceName, myUncertValueString)
                # Write changes to datacard
                myPrimaryReader.close()
                # Something in memory management leaks - the following helps dramatically to recude the leak
                ROOT.gROOT.CloseFiles()
                ROOT.gROOT.GetListOfCanvases().Delete()
                ROOT.gDirectory.GetList().Delete()
            else:
                print "      . no changes to datacard needed"

    def resultExists(self, mHp, tanbeta):
        a = ""
        if isinstance(tanbeta, str):
            a = "%s_%04.1f"%(mHp,float(tanbeta))
        else:
            a = "%s_%04.1f"%(mHp,tanbeta)
        if len(self._results) == 0:
            return False
        return a in self._results.keys()
    
    def setCombineResult(self, mHp, tanbeta, result):
        a = ""
        if isinstance(tanbeta, str):
            a = "%s_%04.1f"%(mHp,float(tanbeta))
        else:
            a = "%s_%04.1f"%(mHp,tanbeta)
        if len(self._results) == 0:
            return None
        self._results[a]["combineResult"] = result
    
    def getResult(self, mHp, tanbeta):
        a = ""
        if isinstance(tanbeta, str):
            a = "%s_%04.1f"%(mHp,float(tanbeta))
        else:
            a = "%s_%04.1f"%(mHp,tanbeta)
        return self._results[a]

    def getCombineResultByKey(self, mHp, tanbeta, resultKey):
        result = self.getResult(mHp, tanbeta)
        return getattr(result["combineResult"], resultKey)
      
    def getPassedStatus(self, mHp, tanbeta, resultKey):
        if self.getFailedStatus(mHp, tanbeta):
            return True
        a = self.getResult(mHp, tanbeta)["sigmaTheory"]
        b = self.getCombineResultByKey(mHp, tanbeta, resultKey)
        return b > a
      
    ## Combine failed or not
    def getFailedStatus(self, mHp, tanbeta):
        result = self.getResult(mHp, tanbeta)
        return result["combineResult"] == None


def getCombineResultPassedStatus(opts, brContainer, mHp, tanbeta, resultKey, scen):
    reuseStatus = False
    if not brContainer.resultExists(mHp, tanbeta):
        # Produce cards
        myPostFix = "lhcasy_%s_mHp%s_tanbetascan%.1f"%(scen,mHp,tanbeta)
        myPostFixAllMasses = "lhcasy_%s_mHpAll_tanbetascan%.1f"%(scen,tanbeta)
        myList = os.listdir(".")
        myList.sort()
        myResultDir = None
        myResultFound = False
        for item in myList:
            if myPostFix in item or myPostFixAllMasses in item:
                myResultDir = item
        if myResultDir != None:
            myList = os.listdir("./%s"%myResultDir)
            for item in myList:
                if item.startswith("higgsCombineobs_m%s"%mHp):
                    f = ROOT.TFile.Open(os.path.join(myResultDir, item))
                    myTree = f.Get("limit")
                    myValue = array.array('d',[0])
                    myTree.SetBranchAddress("limit", myValue)
                    myResult = commonLimitTools.Result(mHp)
                    if myTree.GetEntries() != 6:
                        myResult.failed = True
                    else:
                        myResult.failed = False
                        i = 0
                        while i < myTree.GetEntries():
                            myTree.GetEvent(i)
                            if i == 0:
                                myResult.expectedMinus2Sigma = myValue[0]
                            elif i == 1:
                                myResult.expectedMinus1Sigma = myValue[0]
                            elif i == 2:
                                myResult.expected = myValue[0]
                            elif i == 3:
                                myResult.expectedPlus1Sigma = myValue[0]
                            elif i == 4:
                                myResult.expectedPlus2Sigma = myValue[0]
                            elif i == 5:
                                myResult.observed = myValue[0]
                            i += 1
                        myResultFound = True
                        brContainer._readFromDatabase(mHp, tanbeta)
                        brContainer.setCombineResult(mHp, tanbeta, myResult)
                    f.Close()
        if not myResultFound:
            massInput = [mHp]
            postFixInput = myPostFix
            if opts.gridRunAllMassesInOneJob:
                if mHp != opts.masspoints[0]:
                    return None
                massInput = opts.masspoints[:]
                postFixInput = myPostFixAllMasses
            # Result does not exist, let's calculate it
            if opts.gridRunAllMassesInOneJob:
                for m in opts.masspoints:
                    brContainer.produceScaledCards(m, tanbeta)
            else:
                brContainer.produceScaledCards(mHp, tanbeta)
            # Run Combine
            if "CMSSW_BASE" in os.environ or opts.creategridjobs:
                resultContainer = combine.produceLHCAsymptotic(opts, ".", massPoints=massInput,
                    datacardPatterns = brContainer.getDatacardPatterns(),
                    rootfilePatterns = brContainer.getRootfilePatterns(),
                    clsType = combine.LHCTypeAsymptotic(opts),
                    postfix = postFixInput,
                    quietStatus = True)
                if resultContainer != None and len(resultContainer.results) > 0:
                    result = resultContainer.results[0]
                    # Store result
                    brContainer.setCombineResult(mHp, tanbeta, result)
            else:
                print "... Skipping combine (assuming debug is intended; to run combine, do first cmsenv) ..."
    else:
        reuseStatus = True
    #if brContainer.resultExists(mHp, tanbeta):
        #myContainer = brContainer
    #else:
        #raise Exception("No datacards present")
    
    # Print output
    s = "- mHp=%s, tanbeta=%.1f, sigmaTheory="%(mHp, tanbeta)
    if brContainer.getResult(mHp, tanbeta)["sigmaTheory"] == None:
        s += "None"
    else:
        s += "%.3f"%brContainer.getResult(mHp, tanbeta)["sigmaTheory"]
    if brContainer.getFailedStatus(mHp, tanbeta):
        s += " sigmaCombine (%s)=failed"%resultKey
    else:
        s += " sigmaCombine (%s)=%.3f, passed=%d"%(resultKey, brContainer.getCombineResultByKey(mHp, tanbeta, resultKey), brContainer.getPassedStatus(mHp, tanbeta, resultKey))
    if not reuseStatus:
        print s
    # return limit from combine
    if brContainer.getFailedStatus(mHp, tanbeta):
        return None
    return brContainer.getPassedStatus(mHp, tanbeta, resultKey)

def findMiddlePoint(tanbetaMin, tanbetaMax):
    a = (tanbetaMax + tanbetaMin) / 2.0
    if a < 10:
        # Check if finest available resolution has been achieved
        if (tanbetaMax - tanbetaMin - 0.1) < 0.00001:
            return None
        return round(a,1)
    else:
        # Check if finest available resolution has been achieved
        if (tanbetaMax - tanbetaMin - 1) < 0.00001:
            return None
        return round(a,0)

## Scans three values and returns a list of new range pairs
def scan(opts, brContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scen):
    print "scanning %s / %.1f-%.1f"%(resultKey, tanbetaMin,tanbetaMax)
    tanbetaMid = findMiddlePoint(tanbetaMin, tanbetaMax)
    if tanbetaMid == None:
        return []
    # Calculate results
    minPassed = getCombineResultPassedStatus(opts, brContainer, mHp, tanbetaMin, resultKey, scen)
    midPassed = getCombineResultPassedStatus(opts, brContainer, mHp, tanbetaMid, resultKey, scen)
    maxPassed = getCombineResultPassedStatus(opts, brContainer, mHp, tanbetaMax, resultKey, scen)
    # Calculate new ranges
    ranges = []
    if minPassed != midPassed:
        ranges.append([tanbetaMin, tanbetaMid])
    if midPassed != maxPassed:
        ranges.append([tanbetaMid, tanbetaMax])
    return ranges

def scanRanges(opts, brContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scen):
    myRanges = scan(opts, brContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scen)
    for l in myRanges:
        scanRanges(opts, brContainer, mHp, l[0], l[1], resultKey, scen)

def readResults(opts, brContainer, m, myKey, scen):
    myList = os.listdir(".")
    for name in myList:
        if name.startswith("results_") and name.endswith(".txt"):
            print "Opening file '%s', key %s"%(name, myKey)
            f = open(name)
            if f == None:
                raise Exception("Error: Could not open result file '%s' for input!"%name)
            lines = f.readlines()
            f.close()
            # Analyse lines
            myBlockStart = None
            myBlockEnd = None
            myLine = 0
            while myLine < len(lines) and myBlockEnd == None:
                if lines[myLine].startswith("Tan beta limit scan (") or lines[myLine].startswith("Allowed tan beta"):
                    if myBlockStart == None:
                        s = lines[myLine].replace("Tan beta limit scan (","").replace(") for m=",",").replace(" and key: ",",").replace("\n","")
                        mySplit = s.split(",")
                        if scen == mySplit[0] and m == mySplit[1] and myKey == mySplit[2]:
                            # Entry found, store beginning
                            myBlockStart = myLine
                    else:
                        myBlockEnd = myLine
                myLine += 1
            if myBlockStart == None or myLine - myBlockStart > 100:
                print "... could not find results"
            else:
                myBlockEnd = myLine
            if myBlockEnd != None:
                for i in range(myBlockStart+1, myBlockEnd-1):
                    s = lines[i].replace("  tan beta=","").replace(" xsecTheor=","").replace(" pb, limit(%s)="%myKey,",").replace(" pb, passed=",",")
                    mySplit = s.split(",")
                    if len(mySplit) > 1 and s[0] != "#" and mySplit[2] != "failed" and mySplit[1] != "None":
                        myTanBeta = mySplit[0]
                        tanbetakey = "%s_%04.1f"%(float(myTanBeta))
                        if not brContainer.resultExists(m, myTanBeta):
                            brContainer._results[tanbetakey] = {}
                            if mySplit[1] == "None":
				brContainer._results[tanbetakey]["sigmaTheory"] = None
			    else:
				brContainer._results[tanbetakey]["sigmaTheory"] = float(mySplit[1])
                            result = commonLimitTools.Result(0)
                            setattr(result, myKey, float(mySplit[2]))
                            brContainer.setCombineResult(mHp, myTanBeta, result)
                        else:
                            # Add result key
                            setattr(brContainer._results[tanbetakey]["combineResult"], myKey, float(mySplit[2]))

def linearCrossOverOfTanBeta(mHp, container, tblow, tbhigh, resultKey):
    limitLow = getattr(container.getResult(mHp, tblow)["combineResult"], resultKey)
    limitHigh = getattr(container.getResult(mHp, tbhigh)["combineResult"], resultKey)
    theoryLow = container.getResult(mHp, tblow)["sigmaTheory"]
    theoryHigh = container.getResult(mHp, tbhigh)["sigmaTheory"]
    # subtract the theory from the limit (assume linear behavior)
    if theoryLow == None or theoryHigh == None:
        return -1.0
    subLow = limitLow - theoryLow
    subHigh = limitHigh - theoryHigh
    tbLowValue = float(tblow)
    tbHighValue = float(tbhigh)
    dydx = (subHigh-subLow) / (tbHighValue-tbLowValue)
    b = subLow - tbLowValue*dydx
    tbinterpolation = -b / dydx
    if tbinterpolation < tbLowValue:
        tbinterpolation = tbLowValue
    if tbinterpolation > tbHighValue:
        tbinterpolation = tbHighValue
    return tbinterpolation

def main(opts, brContainer, m, scen, plotContainers):
    resultKeys = ["observed",  "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]
    #resultKeys = ["observed","expected"]
    if opts.gridRunAllMassesInOneJob:
        resultKeys = ["observed"]
    for myKey in resultKeys:
        if opts.analyseOutput:
            readResults(opts, brContainer, m, myKey, scen)
        else:
            # Force calculation of few first points
            if len(opts.tanbeta) > 0:
                for tb in opts.tanbeta:
                    getCombineResultPassedStatus(opts, brContainer, m, float(tb), myKey, scen)
            else:
                if float(m) > 179:
                    getCombineResultPassedStatus(opts, brContainer, m, 1.1, myKey, scen)
                    getCombineResultPassedStatus(opts, brContainer, m, 1.2, myKey, scen)
                    getCombineResultPassedStatus(opts, brContainer, m, 1.3, myKey, scen)
                    getCombineResultPassedStatus(opts, brContainer, m, 1.4, myKey, scen)
                scanRanges(opts, brContainer, m, 1.1, 7.9, myKey, scen)
                scanRanges(opts, brContainer, m, 8.0, _maxTanBeta, myKey, scen)
    
    outtxt = ""
    if opts.creategridjobs:
        return
    # Print results
    myTanBetaKeys = brContainer._results.keys()
    myTanBetaKeys.sort()
    for myResultKey in resultKeys:
        outtxt += "\nTan beta limit scan (%s) for m=%s and key: %s\n"%(scen, m,myResultKey)
        for k in myTanBetaKeys:
            mySplit = k.split("_")
            if m == mySplit[0]:
                myTanBeta = mySplit[1]
                theory = brContainer.getResult(m, myTanBeta)["sigmaTheory"]
                combineResult = ""
                passedStatus = ""
                if brContainer.getFailedStatus(m, myTanBeta):
                    combineResult = "failed"
                    passedStatus = "n.a."
                else:
                    #print brContainer.getResult(m, myTanBeta), myResultKey
                    if hasattr(brContainer.getResult(m, myTanBeta)["combineResult"], myResultKey):
                        myValue = getattr(brContainer.getResult(m, myTanBeta)["combineResult"], myResultKey)
                        if myValue != None:
                            combineResult = "%f pb"%myValue
                            passedStatus = "%d"%brContainer.getPassedStatus(m, myTanBeta, myResultKey)
                        else:
                            combineResult = "n.a."
                            passedStatus = "n.a."
                if theory == None:
                    outtxt += "  tan beta=%s, xsecTheor=None, limit(%s)=%s, passed=%s\n"%(myTanBeta, myResultKey, combineResult, passedStatus)
                else:
                    outtxt += "  tan beta=%s, xsecTheor=%f pb, limit(%s)=%s, passed=%s\n"%(myTanBeta, theory, myResultKey, combineResult, passedStatus)
    
    # Find limits
    outtxt += "\nAllowed tan beta ranges (%s) for m=%s (linear interpolation used)\n"%(scen, m)
    for myResultKey in resultKeys:
        myLowTanBetaLimit = 1.0
        myHighTanBetaLimit = 75
        lowFound = False
        highFound = False
        myPreviousStatus = None
        myPreviousValidTanBetaKey = None
        for i in range(0, len(myTanBetaKeys)):
            mySplit = myTanBetaKeys[i].split("_")
            if m == mySplit[0]:
                myTanBeta = mySplit[1]
                if not brContainer.getFailedStatus(m, myTanBeta):
                    if hasattr(brContainer.getResult(m, myTanBeta)["combineResult"], myResultKey) and getattr(brContainer.getResult(m, myTanBeta)["combineResult"], myResultKey) != None:
                        myCurrentStatus = brContainer.getPassedStatus(m, myTanBeta, myResultKey)
                        if myPreviousStatus != None:
                            if myPreviousStatus != myCurrentStatus:
                                # Cross-over point, check direction
                                myTbvalue = linearCrossOverOfTanBeta(m, brContainer, myTanBetaKeys[myPreviousValidTanBetaKey], myTanBeta, myResultKey)
                                combineValue = getattr(brContainer.getResult(m, myTanBeta)["combineResult"], myResultKey)
                                if combineValue < 2.0:
                                    if not myPreviousStatus:
                                        myLowTanBetaLimit = myTbvalue
                                        plotContainers[scen].addLowResult(m, myResultKey, myTbvalue)
                                        lowFound = True
                                    else:
                                        myHighTanBetaLimit = myTbvalue
                                        plotContainers[scen].addHighResult(m, myResultKey, myTbvalue)
                                        highFound = True
                        myPreviousStatus = myCurrentStatus
                        myPreviousValidTanBetaKey = i
        outtxt +=  "  key='%s' allowed range: %.2f - %.2f\n"%(myResultKey, myLowTanBetaLimit, myHighTanBetaLimit)
        if not lowFound:
            plotContainers[scen].addLowResult(m, myResultKey, None)
        if not highFound:
            plotContainers[scen].addHighResult(m, myResultKey, None)
        
    print outtxt
    f = open(_resultFilename, "a")
    f.write(outtxt)
    f.close()


def purgeDecayModeMatrix(myDecayModeMatrix, myMassPoints):
    myCommonMassPoints = []
    myDirList = os.listdir(".")
    for fskey in myDecayModeMatrix.keys():
        for dmkey in myDecayModeMatrix[fskey].keys():
            myDecayModeMassPoints = []
            myFoundStatus = False
            # Look for datacards
            s = myDecayModeMatrix[fskey][dmkey][0].split("%s")
            if len(s) > 1:
                for item in myDirList:
                    if item.startswith(s[0]) and item.endswith(s[1]):
                        myFoundStatus = True
                        mass = item.replace(s[0],"").replace(s[1],"")
                        myDecayModeMassPoints.append(mass)
                        # Check if root file exists
                        if len(myDecayModeMatrix[fskey][dmkey]) > 1:
                            if not os.path.exists(myDecayModeMatrix[fskey][dmkey][1]%mass):
                                raise Exception("Error: the datacard for mass %s exists, but the root file '%s' does not!"%(mass, myDecayModeMatrix[fskey][dmkey][1]%mass))
                if not myFoundStatus:
                    print "Warning: no datacards found for decay mode %s / %s, removing it ..."%(fskey,dmkey)
                    del myDecayModeMatrix[fskey][dmkey]
                else:
                    # Purge non-common mass points
                    if len(myCommonMassPoints) == 0:
                        myCommonMassPoints.extend(myDecayModeMassPoints)
                    else:
                        i = 0
                        while i < len(myCommonMassPoints):
                            if not myCommonMassPoints[i] in myDecayModeMassPoints:
                                del myCommonMassPoints[i]
                            else:
                                i += 1
            else:
                if not os.path.exists(myDecayModeMatrix[fskey][dmkey][0]):
                    print "Warning: no datacard found for decay mode %s / %s, removing it ..."%(fskey,dmkey)
                    del myDecayModeMatrix[fskey][dmkey]
        if len(myDecayModeMatrix[fskey].keys()) == 0:
            del myDecayModeMatrix[fskey]
    # Print combination details
    print "Input for combination:"
    myDecayModes = []
    for fskey in myDecayModeMatrix.keys():
        for dmkey in myDecayModeMatrix[fskey].keys():
            if dmkey not in myDecayModes:
                myDecayModes.append(dmkey)
    myDecayModes.sort()
    for dm in myDecayModes:
        print "  - decay mode:", dm
        myList = []
        for fskey in myDecayModeMatrix.keys():
            for dmkey in myDecayModeMatrix[fskey].keys():
                if dm == dmkey:
                    myList.append(fskey)
        myList.sort()
        for l in myList:
            print "    - final state or category:", l
    # Solve common mass points
    if len(myMassPoints) > 0:
        i = 0
        while i < len(myMassPoints):
            if not myMassPoints[i] in myCommonMassPoints:
                del myMassPoints[i]
            i += 1
    else:
        myMassPoints.extend(myCommonMassPoints)
    myMassPoints.sort()

def evaluateUncertainties(myScenarios):
    print "Evaluating theoretical syst. uncertainties"
    myMassPoints = ["200", "300", "400", "500", "600"]
    tanbMin = 10
    tanbMax = 60
    #hXsectUncert = ROOT.TH2F("xsectUncert","xsectUncert",len(myMassPoints),myMassPoints[0],myMassPoints[len(myMassPoints)-1], tanbMax-tanbMin, tanbMin, tanbMax)
    #hBrTaunuUncert = ROOT.TH2F("BrTaunuUncert","BrTaunuUncert",len(myMassPoints),myMassPoints[0],myMassPoints[len(myMassPoints)-1], tanbMax-tanbMin, tanbMin, tanbMax)
    #hBrTBUncert = ROOT.TH2F("BrTBUncert","BrTBUncert",len(myMassPoints),myMassPoints[0],myMassPoints[len(myMassPoints)-1], tanbMax-tanbMin, tanbMin, tanbMax)
    for scen in myScenarios:
        xsectUncertPlusMin = 9999
        xsectUncertPlusMax = 0
        xsectUncertMinusMin = 9999
        xsectUncertMinusMax = 0
        brTaunuUncertPlusMin = 9999
        brTaunuUncertPlusMax = 0
        brTaunuUncertMinusMin = 9999
        brTaunuUncertMinusMax = 0
        brTBUncertPlusMin = 9999
        brTBUncertPlusMax = 0
        brTBUncertMinusMin = 9999
        brTBUncertMinusMax = 0
        brCombUncertPlusMin = 9999
        brCombUncertPlusMax = 0
        brCombUncertMinusMin = 9999
        brCombUncertMinusMax = 0
        myDbInputName = "%s-LHCHXSWG.root"%scen
        if not os.path.exists(myDbInputName):
            raise Exception("Error: Cannot find file '%s'!"%myDbInputName)
        db = BRXSDB.BRXSDatabaseInterface(myDbInputName, silentStatus=True)
        for mHp in myMassPoints:
            print scen,mHp
            for tanbeta in range(tanbMin, tanbMax):
                myTheorUncertLabel = "theory_Hpxsection"
                value = db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "-")
                xsectUncertMinusMin = min(xsectUncertMinusMin, value)
                xsectUncertMinusMax = max(xsectUncertMinusMin, value)
                value = db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "+")
                xsectUncertPlusMin = min(xsectUncertPlusMin, value)
                xsectUncertPlusMax = max(xsectUncertPlusMin, value)
                value = db.brUncert("mHp", "tanb", "BR_Hp_taunu", mHp, tanbeta, "-")
                brTaunuUncertMinusMin = min(brTaunuUncertMinusMin, value)
                brTaunuUncertMinusMax = max(brTaunuUncertMinusMax, value)
                value = db.brUncert("mHp", "tanb", "BR_Hp_taunu", mHp, tanbeta, "+")
                brTaunuUncertPlusMin = min(brTaunuUncertPlusMin, value)
                brTaunuUncertPlusMax = max(brTaunuUncertPlusMax, value)
                value = db.brUncert("mHp", "tanb", "BR_Hp_tb", mHp, tanbeta, "-")
                brTBUncertMinusMin = min(brTBUncertMinusMin, value)
                brTBUncertMinusMax = max(brTBUncertMinusMax, value)
                value = db.brUncert("mHp", "tanb", "BR_Hp_tb", mHp, tanbeta, "+")
                brTBUncertPlusMin = min(brTBUncertPlusMin, value)
                brTBUncertPlusMax = max(brTBUncertPlusMax, value)
                db.brUncert2("mHp", "tanb", "BR_Hp_taunu", "BR_Hp_tb", mHp, tanbeta, "-")
                brCombUncertMinusMin = min(brCombUncertMinusMin, value)
                brCombUncertMinusMax = max(brCombUncertMinusMax, value)
                db.brUncert2("mHp", "tanb", "BR_Hp_taunu", "BR_Hp_tb", mHp, tanbeta, "+")
                brCombUncertPlusMin = min(brCombUncertPlusMin, value)
                brCombUncertPlusMax = max(brCombUncertPlusMax, value)
        db.close()
        print "Syst. uncertainties for %s, mHp=%s-%s, tanbeta=%s-%s"%(scen, myMassPoints[0],myMassPoints[len(myMassPoints)-1], tanbMin, tanbMax)
        print "xsect uncert: minus: %f-%f, plus %f-%f"%(xsectUncertMinusMin,xsectUncertMinusMax,xsectUncertPlusMin,xsectUncertPlusMax)
        print "br(taunu) uncert: minus: %f-%f, plus %f-%f"%(brTaunuUncertMinusMin,brTaunuUncertMinusMax,brTaunuUncertPlusMin,brTaunuUncertPlusMax)
        print "br(tb) uncert: minus: %f-%f, plus %f-%f"%(brTBUncertMinusMin,brTBUncertMinusMax,brTBUncertPlusMin,brTBUncertPlusMax)
        print "br(taunu+tb) uncert: minus: %f-%f, plus %f-%f"%(brCombUncertMinusMin,brCombUncertMinusMax,brCombUncertPlusMin,brCombUncertPlusMax)
  

if __name__ == "__main__":

    def addToDatacards(myDir, massPoints, dataCardList, rootFileList, dataCardPattern, rootFilePattern):
        m = DatacardReader.getMassPointsForDatacardPattern(myDir, dataCardPattern)
        if len(m) > 0:
            m = DatacardReader.getMassPointsForDatacardPattern(myDir, dataCardPattern, massPoints)
            del massPoints[:]
            massPoints.extend(m)
            dataCardList.append(dataCardPattern)
            rootFileList.append(rootFilePattern)

    parser = commonLimitTools.createOptionParser(False, False, True)
    parser.add_option("--analyseOutput", dest="analyseOutput", action="store_true", default=False, help="Read only output and print summary")
    parser.add_option("--scen", dest="scenarios", action="append", default=[], help="MSSM scenarios")
    parser.add_option("-t", "--tanbeta", dest="tanbeta", action="append", default=[], help="tanbeta values (will scan only these)")
    parser.add_option("--evalUuncert", dest="evaluateUncertainties", action="store_true", default=False, help="Make plots of theoretical uncertainties")
    parser.add_option("--creategridjobs", dest="creategridjobs", action="store_true", default=False, help="Create crab task dirs for running on grid")
    parser.add_option("--gridmassive", dest="gridRunAllMassesInOneJob", action="store_true", default=False, help="Crab jobs run all masses in one job (default=1 job / mass)")
    opts = commonLimitTools.parseOptionParser(parser)
    if opts.rmin == None:
        opts.rmin = "0"
    if opts.rmax == None:
        opts.rmax = "4" # To facilitate the search for different tan beta values
    
    if opts.creategridjobs:
        print "*** Start creating individual crab job directories for grid submission ... ***"

    # MSSM scenario settings
    myScenarios = ["mhmaxup", "mhmodm", "mhmodp", "lightstau", "lightstop", "tauphobic"]
    if len(opts.scenarios) > 0:
        myScenarios = opts.scenarios[:]
    else:
        opts.scenarios = myScenarios[:]
    
    if opts.evaluateUncertainties:
        evaluateUncertainties(myScenarios)
        sys.exit()
    
    myPlots = {}
    #myScenarios = ["mhmaxup"]
    
    # General settings
    myDirs = opts.dirs[:]
    if len(myDirs) == 0:
        myDirs.append(".")
    myCurrentDir = os.getcwd()

    for myDir in myDirs:
        os.chdir(myCurrentDir)
        if os.path.exists(_resultFilename):
            os.system("mv %s %s.old"%(_resultFilename, _resultFilename))
        myMassPoints = []
        if len(opts.masspoints) > 0:
            myMassPoints = opts.masspoints[:]
        print "Considering directory:",myDir
        os.chdir(myDir)

        # Work with the original cards
        if os.path.exists("originalDatacards"):
            os.system("cp originalDatacards/* .")
        # Matrix of decay mode inputs; use as key the branching key
        myDecayModeMatrix = {}
        settings = commonLimitTools.GeneralSettings(myDir, opts.masspoints)
        myTauJetsDecayMode = {"Hp_taunu": [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS), settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)]}
        myTauMuDecayMode = {"Hp_taunu": ["datacard_mutau_taunu_m%s_mutau.txt", "shapes_taunu_m%s_btagmultiplicity_j.root"],
                            "Hp_tb": ["datacard_mutau_tb_m%s_mutau.txt", "shapes_tb_m%s_btagmultiplicity_j.root"]}
        myEEDecayMode = {"Hp_taunu": ["DataCard_ee_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_ee.root"],
                         "Hp_tb": ["DataCard_ee_tb_m%s.txt", "CrossSectionShapes_tb_m%s_ee.root"]}
        myEMuDecayMode = {"Hp_taunu": ["DataCard_emu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_emu.root"],
                         "Hp_tb": ["DataCard_emu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_emu.root"]}
        myMuMuDecayMode = {"Hp_taunu": ["DataCard_mumu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_mumu.root"],
                         "Hp_tb": ["DataCard_mumu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_mumu.root"]}
        myDecayModeMatrix["taujets"] = myTauJetsDecayMode
        myDecayModeMatrix["mutau"] = myTauMuDecayMode
        myDecayModeMatrix["ee"] = myEEDecayMode
        myDecayModeMatrix["emu"] = myEMuDecayMode
        myDecayModeMatrix["mumu"] = myMuMuDecayMode
        # Single lepton
        myLabels = ["nB1_mu", "nB2p_mu", "nB1_el", "nB2p_el"]
        for l in myLabels:
            myCategory = {"Hp_tb": ["HpToSingleLepton_datacard_"+l+"_%s.txt", "HT_M%s_binnedStat_p10_"+l+".root"]}
            myDecayModeMatrix["ljets_%s"%l] = myCategory
        myLabels = ["Control_nB0_mu", "Control_nB1_mu", "Control_nB2p_mu", "Control_nB0_el", "Control_nB1_el", "Control_nB2p_el"]
        for l in myLabels:
            myCategory = {"Hp_tb": ["HpToSingleLepton_datacard_"+l+".txt", None]}
            myDecayModeMatrix["ljets_%s"%l] = myCategory
        
        # Purge matrix
        if not opts.analyseOutput:
	    purgeDecayModeMatrix(myDecayModeMatrix, myMassPoints)
        # reject mass points between 160-200 GeV
        i = 0
        while i < len(myMassPoints):
            m = float(myMassPoints[i])
            if (m > 160.1 and m < 199.9) or m < 89.9:
                myMassPoints.remove(myMassPoints[i])
            else:
                i += 1
        if len(myMassPoints) == 0:
            if len(opts.masspoints) > 0:
                raise Exception("Check that the mass point parameters are correct!")
            print "Automatic mass identification failed, trying default range (this could of course fail)"
            myMassPoints.extend(["200", "220", "250", "300", "400", "500", "600"])
        print "The following masses are considered:",", ".join(map(str, myMassPoints))
        opts.masspoints = myMassPoints[:]
        for m in myMassPoints:
            for scen in myScenarios:
                print scen,m
                if not scen in myPlots.keys():
                    myPlots[scen] = TanBetaResultContainer(scen, myMassPoints)
                brContainer = BrContainer(myDecayModeMatrix, scen, myMassPoints)
                #tbContainer = BrContainer("Hp_tb",datacardPatternsTB, rootFilePatternsTB, "BR_Hp_tb", scen)
                main(opts, brContainer, m, scen, myPlots)
    print "\nTan beta scan is done, results have been saved to %s"%_resultFilename
    
    if opts.creategridjobs:
        # Print instructions
        print "*** Created crab task dirs for multicrab ***"
        #print "*** To submit, do the following ***"
        #print "cd %s"%dirname
        #print "multicrab -create -submit all"
    else:
        # Apply TDR style
        style = tdrstyle.TDRStyle()

        for scen in myScenarios:
            myPlots[scen].doPlot()
