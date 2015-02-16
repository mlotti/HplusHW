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

import os
import sys
import array

_resultFilename = "results.txt"
_theoreticalUncertainty = 0.32 # OBSOLETE
_maxTanBeta = 69.0
_linearSummingForTheoryUncertainties = not True

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
            g.SetPoint(i, float(self._massPoints[i]), self._resultsLow[firstKey][self._massPoints[i]])
        # Low limit, top pass right to left
        for i in range(0, lenm):
            j = lenm - i - 1
            g.SetPoint(i+lenm, float(self._massPoints[j]), self._resultsLow[secondKey][self._massPoints[j]])
        # intermediate points
        g.SetPoint(lenm*2, -1.0, self._resultsLow[secondKey][self._massPoints[lenm-1]])
        g.SetPoint(lenm*2+1, -1.0, self._resultsHigh[firstKey][self._massPoints[0]])
        # Upper limit, bottom pass left to right
        for i in range(0, lenm):
            g.SetPoint(i+lenm*2+2, float(self._massPoints[i]), self._resultsHigh[firstKey][self._massPoints[i]])
        # Upper limit, top pass right to left
        for i in range(0, lenm):
            j = lenm - i - 1
            g.SetPoint(i+lenm*3+2, float(self._massPoints[j]), self._resultsHigh[secondKey][self._massPoints[j]])
        return g

    def _getResultGraphForOneKey(self, resultKey):
        if not resultKey in self._resultsLow.keys():
            return None
        lenm = len(self._massPoints)
        g = ROOT.TGraph(lenm*2+5)
        # Upper limit, top part left to right
        g.SetPoint(0, -1.0, 100.0)
        g.SetPoint(1, 1000.0, 100.0)
        # Upper limit, pass right to left
        for i in range(0, lenm):
            j = lenm - i - 1
            g.SetPoint(i+2, float(self._massPoints[j]), self._resultsHigh[resultKey][self._massPoints[j]])
        # intermediate points
        g.SetPoint(lenm+2, -1.0, self._resultsLow[resultKey][self._massPoints[lenm-1]])
        g.SetPoint(lenm+3, -1.0, self._resultsHigh[resultKey][self._massPoints[0]])
        # Low limit, pass left to right
        for i in range(0, lenm):
            g.SetPoint(i+lenm+3, float(self._massPoints[i]), self._resultsLow[resultKey][self._massPoints[i]])
        # Low limit, bottom part right to left
        g.SetPoint(lenm*2+4, 1000.0, 0.0)
        g.SetPoint(lenm*2+5, -1.0, 0.0)
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
        myFinalStateLabel.append("^{}H^{+}#rightarrow#tau^{+}#nu_{#tau} final states:")
        myFinalStateLabel.append("  ^{}#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu")
        myFinalStateLabel.append("^{}H^{+}#rightarrowt#bar{b} final states:")
        myFinalStateLabel.append("  ^{}#mu#tau_{h}, ee, e#mu, #mu#mu")
        limit.doTanBetaPlotGeneric("limitsTanbCombination_heavy_"+self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="combination")
                                                                           
class BrContainer:
    def __init__(self, decayModeMatrix, mssmModel, massPoints):
        self._decayModeMatrix = decayModeMatrix
        self._mssmModel = mssmModel
        self._massPoints = massPoints
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
        myTree.SetBranchAddress("mHp", mHpInTree)
        myTree.SetBranchAddress("tanb", tanbInTree)
        myTree.SetBranchAddress("tHp_xsec", sigmaInTree)
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
            raise Exception("Error: Could not find tan beta value %f in '%s'!"%(tanbeta, myRootFilename))
        if not myFoundMassStatus:
            raise Exception("Error: Could not find mass value %s in '%s'!"%(mHp, myRootFilename))
        # Found branching and sigma, store them
        tblabel = "%04.1f"%tanbeta
        self._results[tblabel] = {}
        for brkey in self._brkeys.keys():
            self._results[tblabel]["%sTheory"%brkey] = self._brkeys[brkey][0]
        self._results[tblabel]["sigmaTheory"] = sigmaInTree[0]*2.0*0.001 # fb->pb; xsec is in database for only H+, factor 2 gives xsec for Hpm
        self._results[tblabel]["combineResult"] = None
        
        s = "  - m=%s, tanbeta=%.1f: sigma_theor=%f pb"%(mHp, tanbeta, self._results[tblabel]["sigmaTheory"])
        for brkey in self._brkeys.keys():
            s += ", Br(%s)=%f"%(brkey, self._brkeys[brkey][0])
        print s

    def produceScaledCards(self, mHp, tanbeta):
        if self.resultExists(tanbeta):
            return
        # Obtain branching and sigma from MSSM model database
        self._readFromDatabase(mHp, tanbeta)
        #print "    Scaled '%s/%s' signal in datacards by branching %f (mHp=%s, tanbeta=%.1f)"%(mySignalScaleFactor, mHp, tanbeta)
        # Obtain theoretical uncertinties from MSSM model database
        myDbInputName = "%s-LHCHXSWG.root"%self._mssmModel
        if not os.path.exists(myDbInputName):
            raise Exception("Error: Cannot find file '%s'!"%myDbInputName)
        # Scale datacards
        myResult = self.getResult(tanbeta)
        for fskey in self._decayModeMatrix.keys():
            print "    . final state %10s:"%fskey
            myOriginalRates = []
            myPrimaryReader = None
            for dmkey in self._decayModeMatrix[fskey].keys():
                myDatacardPattern = self._decayModeMatrix[fskey][dmkey][0]
                myRootFilePattern = self._decayModeMatrix[fskey][dmkey][1]
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
            mySignalColumnName = myPrimaryReader.getDatasetNames()[0]
            myUpdatedRate = float(myPrimaryReader.getRateValue(myPrimaryReader.getDatasetNames()[0]))
            myTheorUncertPrefix = "theory_"
            # Add theoretical cross section uncertainties to datacard 
            db = BRXSDB.BRXSDatabaseInterface(myDbInputName, silentStatus=True)
            myXsecUncert = [db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "-"),
                            db.xsecUncertOrig("mHp", "tanb", "", mHp, tanbeta, "+")]
            myUncertValueString = "%.3f/%.3f"%(1.0-myXsecUncert[0], 1.0+myXsecUncert[1])
            myNuisanceName = "%sxsectionHp"%myTheorUncertPrefix
            myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueString)
            print "      . H+ xsec uncert: %s"%myUncertValueString
            # Add theoretical branching ratio uncertainties to datacard (depends on how many decay modes are combined)
            myDecayModeKeys = self._decayModeMatrix[fskey].keys()
            for i in range(len(myDecayModeKeys)):
                myDecayModeKeys[i] = "BR_%s"%myDecayModeKeys[i]
            myBrUncert = db.brUncert("mHp", "tanb", myDecayModeKeys, mHp, tanbeta, linearSummation=_linearSummingForTheoryUncertainties, silentStatus=True)
            for i in range(len(myDecayModeKeys)):
                for k in myBrUncert.keys():
                    if myDecayModeKeys[i] in k:
                        # Scale uncertainty according to amount of signal from that decay mode
                        myUncertValue = myBrUncert[k] * myOriginalRates[i] / myUpdatedRate
                        myNuisanceName = "%s%s"%(myTheorUncertPrefix,k)
                        myUncertValueString = "%.3f"%(1.0+myUncertValue)
                        myPrimaryReader.addNuisance(myNuisanceName, "lnN", mySignalColumnName, myUncertValueString)
                        print "      . H+ Br uncert(%s): %s"%(k, myUncertValueString)
            # Write changes to datacard
            myPrimaryReader.close()
            
    def resultExists(self, tanbeta):
        a = ""
        if isinstance(tanbeta, str):
            a = "%04.1f"%(float(tanbeta))
        else:
            a = "%04.1f"%tanbeta
        if len(self._results) == 0:
            return False
        return a in self._results.keys()
    
    def setCombineResult(self, tanbeta, result):
        a = ""
        if isinstance(tanbeta, str):
            a = "%04.1f"%(float(tanbeta))
        else:
            a = "%04.1f"%tanbeta
        if len(self._results) == 0:
            return None
        self._results[a]["combineResult"] = result
    
    def getResult(self, tanbeta):
        a = ""
        if isinstance(tanbeta, str):
            a = "%04.1f"%(float(tanbeta))
        else:
            a = "%04.1f"%tanbeta
        return self._results[a]

    def getCombineResultByKey(self, tanbeta, resultKey):
        result = self.getResult(tanbeta)
        return getattr(result["combineResult"], resultKey)
      
    def getPassedStatus(self, tanbeta, resultKey):
        if self.getFailedStatus(tanbeta):
            return True
        a = self.getResult(tanbeta)["sigmaTheory"]
        b = self.getCombineResultByKey(tanbeta, resultKey)
        return b > a
      
    ## Combine failed or not
    def getFailedStatus(self, tanbeta):
        result = self.getResult(tanbeta)
        return result["combineResult"] == None


def getCombineResultPassedStatus(opts, brContainer, mHp, tanbeta, resultKey, scen):
    reuseStatus = False
    if not brContainer.resultExists(tanbeta):
        # Produce cards
        myPostFix = "lhcasy_%s_mHp%s_tanbetascan%.1f"%(scen,mHp,tanbeta)
        myList = os.listdir(".")
        myList.sort()
        myResultDir = None
        myResultFound = False
        for item in myList:
            if myPostFix in item:
                myResultDir = item
        if myResultDir != None:
            myList = os.listdir("./%s"%myResultDir)
            for item in myList:
                if item.startswith("higgsCombineobs"):
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
                        brContainer.setCombineResult(tanbeta, myResult)
                    f.Close()
        if not myResultFound:
            # Result does not exist, let's calculate it
            brContainer.produceScaledCards(mHp, tanbeta)
            # Run Combine
            resultContainer = combine.produceLHCAsymptotic(opts, ".", massPoints=[mHp],
                datacardPatterns = brContainer.getDatacardPatterns(),
                rootfilePatterns = brContainer.getRootfilePatterns(),
                clsType = combine.LHCTypeAsymptotic(opts),
                postfix = myPostFix,
                quietStatus = True)
            if len(resultContainer.results) > 0:
                result = resultContainer.results[0]
                # Store result
                brContainer.setCombineResult(tanbeta, result)
    else:
        reuseStatus = True
    #if brContainer.resultExists(tanbeta):
        #myContainer = brContainer
    #else:
        #raise Exception("No datacards present")
    
    # Print output
    s = "- mHp=%s, tanbeta=%.1f, sigmaTheory=%.3f"%(mHp, tanbeta, brContainer.getResult(tanbeta)["sigmaTheory"])
    if brContainer.getFailedStatus(tanbeta):
        s += " sigmaCombine (%s)=failed"%resultKey
    else:
        s += " sigmaCombine (%s)=%.3f, passed=%d"%(resultKey, brContainer.getCombineResultByKey(tanbeta, resultKey), brContainer.getPassedStatus(tanbeta, resultKey))
    if not reuseStatus:
        print s
    # return limit from combine
    if brContainer.getFailedStatus(tanbeta):
        return None
    return brContainer.getPassedStatus(tanbeta, resultKey)

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
                    if len(mySplit) > 1 and s[0] != "#" and mySplit[2] != "failed":
                        tanbetakey = "%04.1f"%(float(mySplit[0]))
                        if not brContainer.resultExists(tanbetakey):
                            brContainer._results[tanbetakey] = {}
                            brContainer._results[tanbetakey]["sigmaTheory"] = float(mySplit[1])
                            result = commonLimitTools.Result(0)
                            setattr(result, myKey, float(mySplit[2]))
                            brContainer.setCombineResult(tanbetakey, result)
                        else:
                            # Add result key
                            setattr(brContainer._results[tanbetakey]["combineResult"], myKey, float(mySplit[2]))

def linearCrossOverOfTanBeta(container, tblow, tbhigh, resultKey):
    limitLow = getattr(container.getResult(tblow)["combineResult"], resultKey)
    limitHigh = getattr(container.getResult(tbhigh)["combineResult"], resultKey)
    theoryLow = container.getResult(tblow)["sigmaTheory"]
    theoryHigh = container.getResult(tbhigh)["sigmaTheory"]
    # subtract the theory from the limit (assume linear behavior)
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
    for myKey in resultKeys:
        if opts.analyseOutput:
            readResults(opts, brContainer, m, myKey, scen)
        else:
            # Force calculation of few first points
            if len(opts.tanbeta) > 0:
                for tb in opts.tanbeta:
                    getCombineResultPassedStatus(opts, brContainer, m, float(tb), myKey, scen)
            else:
                getCombineResultPassedStatus(opts, brContainer, m, 1.1, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.2, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.3, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.4, myKey, scen)
                scanRanges(opts, brContainer, m, 1.1, 8.0, myKey, scen)
                scanRanges(opts, brContainer, m, 8.0, _maxTanBeta, myKey, scen)
    
    outtxt = ""
    # Print results
    myTanBetaKeys = brContainer._results.keys()
    myTanBetaKeys.sort()
    for myResultKey in resultKeys:
        outtxt += "\nTan beta limit scan (%s) for m=%s and key: %s\n"%(scen, m,myResultKey)
        for k in myTanBetaKeys:
            theory = brContainer.getResult(k)["sigmaTheory"]
            combineResult = ""
            passedStatus = ""
            if brContainer.getFailedStatus(k):
                combineResult = "failed"
                passedStatus = "n.a."
            else:
                #print brContainer.getResult(k), myResultKey
                if hasattr(brContainer.getResult(k)["combineResult"], myResultKey):
                    myValue = getattr(brContainer.getResult(k)["combineResult"], myResultKey)
                    if myValue != None:
                        combineResult = "%f pb"%myValue
                        passedStatus = "%d"%brContainer.getPassedStatus(k, myResultKey)
                    else:
                        combineResult = "n.a."
                        passedStatus = "n.a."
            outtxt += "  tan beta=%s, xsecTheor=%f pb, limit(%s)=%s, passed=%s\n"%(k, theory, myResultKey, combineResult, passedStatus)
    
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
            if not brContainer.getFailedStatus(myTanBetaKeys[i]):
                if hasattr(brContainer.getResult(myTanBetaKeys[i])["combineResult"], myResultKey) and getattr(brContainer.getResult(myTanBetaKeys[i])["combineResult"], myResultKey) != None:
                    myCurrentStatus = brContainer.getPassedStatus(myTanBetaKeys[i], myResultKey)
                    if myPreviousStatus != None:
                        if myPreviousStatus != myCurrentStatus:
                            # Cross-over point, check direction
                            myTbvalue = linearCrossOverOfTanBeta(brContainer, myTanBetaKeys[myPreviousValidTanBetaKey], myTanBetaKeys[i], myResultKey)
                            combineValue = getattr(brContainer.getResult(myTanBetaKeys[i])["combineResult"], myResultKey)
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
                #print "Warning: removing decay mode %s / %s"%(myDecayModeMatrix.keys()[i], myDecayModeMatrix[i].keys()[j])
                del myDecayModeMatrix[fskey][dmkey]
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
        if len(myDecayModeMatrix[fskey].keys()) == 0:
            del myDecayModeMatrix[fskey]
    # Print combination details
    print "Input for combination:"
    for fskey in myDecayModeMatrix.keys():
        print "- final state:", fskey
        for dmkey in myDecayModeMatrix[fskey].keys():
            print "  - decay mode:", dmkey
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
    parser.add_option("--tanbeta", dest="tanbeta", action="append", default=[], help="tanbeta values (will scan only these)")
    parser.add_option("--evalUuncert", dest="evaluateUncertainties", action="store_true", default=False, help="Make plots of theoretical uncertainties")
    opts = commonLimitTools.parseOptionParser(parser)
    if opts.rmin == None:
        opts.rmin = "0"
    if opts.rmax == None:
        opts.rmax = "10" # To facilitate the search for different tan beta values
    
    # MSSM scenario settings
    myScenarios = ["mhmaxup", "mhmodm", "mhmodp", "lightstau", "lightstop", "tauphobic"]
    if len(opts.scenarios) > 0:
        myScenarios = opts.scenarios[:]
    
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
        
        # Purge matrix
        purgeDecayModeMatrix(myDecayModeMatrix, myMassPoints)

        # reject mass points between 160-200 GeV
        i = 0
        while i < len(myMassPoints):
            m = float(myMassPoints[i])
            if m > 160.1 and m < 199.9:
                myMassPoints.remove(myMassPoints[i])
            else:
                i += 1
        if len(myMassPoints) == 0:
            print "Automatic mass identification failed, trying default range (this could of course fail)"
            myMassPoints.extend(["200", "220", "250", "300", "400", "500", "600"])
        print "The following masses are considered:",", ".join(map(str, myMassPoints))
        for m in myMassPoints:
            for scen in myScenarios:
                print scen,m
                if not scen in myPlots.keys():
                    myPlots[scen] = TanBetaResultContainer(scen, myMassPoints)
                brContainer = BrContainer(myDecayModeMatrix, scen, myMassPoints)
                #tbContainer = BrContainer("Hp_tb",datacardPatternsTB, rootFilePatternsTB, "BR_Hp_tb", scen)
                main(opts, brContainer, m, scen, myPlots)
    print "\nTan beta scan is done, results have been saved to %s"%_resultFilename
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    for scen in myScenarios:
        myPlots[scen].doPlot()
