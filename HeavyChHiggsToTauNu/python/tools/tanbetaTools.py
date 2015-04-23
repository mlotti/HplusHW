## Code for doing tan beta limits
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRXSDatabaseInterface as BRXSDB
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit

import array
import re
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

_minTanBeta = 1.1
_maxTanBeta = 69.0
_minBrTanBeta = 8.0
_linearSummingForTheoryUncertainties = True # LHCHXSWG recommendation True
_separateTheoreticalXsectionAndBrUncertainties = False # LHCHXSWG recommendation False (because of correlations)
_modelPattern = "%s-LHCHXSWG.root"
_resultsPattern = "results-%s.txt"
_resultKeys = ["observed",  "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]

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
        myName = _modelPattern%self._mssmModel
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
	    myFinalStateLabel.append("  ^{}#tau_{h}+jets, #mu#tau_{h}, ll")
	    myFinalStateLabel.append("^{}H^{+}#rightarrowt#bar{b} final states:")
	    myFinalStateLabel.append("  ^{}l+jets, #mu#tau_{h}, ll")
        if float(self._massPoints[0]) < 179:
            limit.doTanBetaPlotGeneric("tanbeta_%s_light"%self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="light")
        else:
            limit.doTanBetaPlotGeneric("limitsTanbCombination_heavy_"+self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="combination")
                                                                           
class BrContainer:
    def __init__(self, decayModeMatrix, mssmModel, massPoints=None):
        self._decayModeMatrix = decayModeMatrix
        self._mssmModel = mssmModel
        self._separateTheoreticalXsectionAndBrUncertainties = _separateTheoreticalXsectionAndBrUncertainties
        self._results = {} # dictionary, where key is tan beta
        # Make dictionary of key labels
        self._brkeys = {}
        if decayModeMatrix != None:
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
        myRootFilename = _modelPattern%self._mssmModel
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
        tblabel = constructResultKey(mHp, tanbeta)
        if not tblabel in self._results.keys():
            self._results[tblabel] = {}
            self._results[tblabel]["combineResult"] = None
        if not myTanBetaValueFoundStatus or not myFoundMassStatus:
            for brkey in self._brkeys.keys():
                self._results[tblabel]["%sTheory"%brkey] = None
            self._results[tblabel]["sigmaTheory"] = None
        else:
            for brkey in self._brkeys.keys():
                self._results[tblabel]["%sTheory"%brkey] = self._brkeys[brkey][0]
            if float(mHp) > 179:
                self._results[tblabel]
                self._results[tblabel]["sigmaTheory"] = sigmaInTree[0]*2.0*0.001 # fb->pb; xsec is in database for only H+, factor 2 gives xsec for Hpm
            else:
                self._results[tblabel]["sigmaTheory"] = brTBHInTree[0] # Br(t->bH+) for light H+
        
        s = "  - m=%s, tanbeta=%.1f: "%(mHp, float(tanbeta))
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
        if self._results[constructResultKey(mHp, tanbeta)]["sigmaTheory"] == None:
            return
        
        #print "    Scaled '%s/%s' signal in datacards by branching %f (mHp=%s, tanbeta=%.1f)"%(mySignalScaleFactor, mHp, tanbeta)
        # Obtain theoretical uncertinties from MSSM model database
        myDbInputName = _modelPattern%self._mssmModel
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
        a = constructResultKey(mHp, tanbeta)
        if len(self._results) == 0:
            return False
        return a in self._results.keys()
    
    def setCombineResult(self, mHp, tanbeta, result):
        a = constructResultKey(mHp, tanbeta)
        if len(self._results) == 0:
            return None
        self._results[a]["combineResult"] = result
    
    def getResult(self, mHp, tanbeta):
        a = constructResultKey(mHp, tanbeta)
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

def constructResultKey(mHp, tanbeta):
    if isinstance(tanbeta, str):
        return "%s_%04.1f"%(mHp,float(tanbeta))
    else:
        return "%s_%04.1f"%(mHp,tanbeta)

def disentangleResultKey(key):
    s = key.split("_")
    result = {}
    result["m"] = s[0]
    result["tb"] = s[1]
    return result

def findModelNames(dirname = "."):
    myModelNames = []
    myPossiblePatterns = [_modelPattern]
    myList = os.listdir(dirname)
    for item in myList:
        for p in myPossiblePatterns:
            mySplit = p.split("%s")
            myExpression = re.compile("%s(?P<name>\S+)%s"%(mySplit[0],mySplit[1]))
            myMatch = myExpression.search(item)
            if myMatch:
                myModelNames.append(myMatch.group("name"))
    return myModelNames

def saveTanbetaResults(brContainer, plotContainer, scen, massPoints, resultKeys):
    myMassPoints = None
    if isinstance(massPoints, list):
        myMassPoints = massPoints[:]
    else:
        myMassPoints = [massPoints]
    
    outtxt = ""
    for m in myMassPoints:
        # produce text from results
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
                                            plotContainer.addLowResult(m, myResultKey, myTbvalue)
                                            lowFound = True
                                        else:
                                            myHighTanBetaLimit = myTbvalue
                                            plotContainer.addHighResult(m, myResultKey, myTbvalue)
                                            highFound = True
                            myPreviousStatus = myCurrentStatus
                            myPreviousValidTanBetaKey = i
            outtxt +=  "  key='%s' allowed range: %.2f - %.2f\n"%(myResultKey, myLowTanBetaLimit, myHighTanBetaLimit)
            if not lowFound:
                plotContainer.addLowResult(m, myResultKey, None)
            if not highFound:
                plotContainer.addHighResult(m, myResultKey, None)

    #print outtxt
    f = open(_resultsPattern%scen, "w")
    f.write(outtxt)
    f.close()
    print "Written results to",_resultsPattern%scen
