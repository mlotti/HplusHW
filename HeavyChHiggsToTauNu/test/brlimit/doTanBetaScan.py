#!/usr/bin/env python

# Produces jobs for calculating tan beta limits
# Strategy:
# 1) loop over m_Hp, tan beta, and MSSM models
# 2) scale signal to Br(H+ -> X) of the model
# 3) calculate limit on sigma_Hp for that point
# 4) if sigma is lower than MSSM sigma_Hp, then point is excluded

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CombineTools as combine
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as commonLimitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.BRXSDatabaseInterface as BRXSDB
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

import os
import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

_resultFilename = "results.txt"
_theoreticalUncertainty = 0.32

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
                self._resultsHigh[resultKey][m] = 75.0
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
        graphs["obs_th_plus"] = self._getResultGraphForOneKey("observedPlusTheorUncert")
        graphs["obs_th_minus"] = self._getResultGraphForOneKey("observedMinusTheorUncert")
        myName = "%s-LHCHXSWG.root"%self._mssmModel
        if not os.path.exists(myName):
            raise Exception("Error: Cannot find file '%s'!"%myName)
        db = BRXSDB.BRXSDatabaseInterface(myName)
        graphs["Allowed"] = db.mhLimit("mh","mHp","mHp > 0","125.0+-3.0")
        if self._mssmModel == "tauphobic":
            # Fix a buggy second upper limit (the order of points is left to right, then right to left; remove further passes to fix the bug)
            decreasingStatus = False
            i = 0
            while i < graphs["Allowed"].GetN():
                removeStatus = False
                y = graphs["Allowed"].GetY()[i]
                if i > 0:
                    if graphs["Allowed"].GetY()[i-1] - y < 0:
                        decreasingStatus = True
                    else:
                        if decreasingStatus:
                            graphs["Allowed"].RemovePoint(i)
                            removeStatus = True
                if not removeStatus:
                    i += 1
            #for i in range(0, graphs["Allowed"].GetN()):
                #print graphs["Allowed"].GetX()[i], graphs["Allowed"].GetY()[i]
        myFinalStateLabel = []
        myFinalStateLabel.append("^{}H^{+}#rightarrow#tau^{+}#nu_{#tau} final states:")
        myFinalStateLabel.append("  ^{}#tau_{h}+jets, #mu#tau_{h}, ee, e#mu, #mu#mu")
        myFinalStateLabel.append("^{}H^{+}#rightarrowt#bar{b} final states:")
        myFinalStateLabel.append("  ^{}#mu#tau_{h}, ee, e#mu, #mu#mu")
        limit.doTanBetaPlotGeneric("limitsTanbCombination_heavy_"+self._mssmModel, graphs, 19700, myFinalStateLabel, limit.mHplus(), self._mssmModel, regime="combination")
                                                                           
class BrContainer:
    def __init__(self, label, datacardPatterns, rootFilePatterns, branchingLabel, mssmModel):
        if len(datacardPatterns) != len(rootFilePatterns):
            raise Exception("This should not happen")
        self._label = label
        self._datacardPatterns = datacardPatterns
        self._rootFilePatterns = rootFilePatterns
        self._branchingLabel = branchingLabel
        self._mssmModel = mssmModel
        self._results = {} # dictionary, where key is tan beta
    
    def getDatacardPatterns(self):
        return self._datacardPatterns
      
    def getRootfilePatterns(self):
        return self._rootFilePatterns
    
    def setMassPoints(self, massPoints):
        self._massPoints = massPoints

    def _readFromDatabase(self, mHp, tanbeta):
        if not os.path.exists(self._datacardPatterns[0]%mHp):
            raise Exception("Error: no support for template morphing between mass points; use one of the mass points!")
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
        tanbInTree = array.array('d',[0])
        mHpInTree = array.array('d',[0])
        branchingRatioInTree = array.array('d',[0])
        sigmaInTree = array.array('d',[0])
        myTree.SetBranchAddress("mHp", mHpInTree)
        myTree.SetBranchAddress("tanb", tanbInTree)
        if myTree.GetBranch(self._branchingLabel) == None:
            raise Exception("Error: Could not find branch by name '%s' in root tree '%s' in root file '%s'!"%(self._branchingLabel, _treename, myRootFilename))
        myTree.SetBranchAddress(self._branchingLabel, branchingRatioInTree)
        myTree.SetBranchAddress("tHp_xsec", sigmaInTree)
        # Find branching
        myTanBetaValueFoundStatus = False
        myBranching = None
        i = 0
        nentries = myTree.GetEntries()
        while i < nentries and myBranching == None:
            myTree.GetEvent(i)
            if abs(tanbInTree[0] - float(tanbeta)) < 0.0001:
                myTanBetaValueFoundStatus = True
                if abs(mHpInTree[0] - float(mHp)) < 0.0001:
                    myBranching = branchingRatioInTree
            i += 1
        f.Close()
        if not myTanBetaValueFoundStatus:
            raise Exception("Error: Could not find tan beta value %f in '%s'!"%(tanbeta, myRootFilename))
        if myBranching == None:
            raise Exception("Error: Could not find branching ratio value in '%s'!"%(myRootFilename))
        # Found branching and sigma, store them
        tblabel = "%.1f"%tanbeta
        self._results[tblabel] = {}
        self._results[tblabel]["brTheory"] = branchingRatioInTree[0]
        self._results[tblabel]["sigmaTheory"] = sigmaInTree[0]*2.0*0.001 # fb->pb; xsec is in database for only H+, factor 2 gives xsec for Hpm
        self._results[tblabel]["combineResult"] = None

    def produceScaledCards(self, mHp, tanbeta):
        if len(self._datacardPatterns) == 0:
            return
        if self.resultExists(tanbeta):
            return
        # Obtain branching and sigma from MSSM model database
        self._readFromDatabase(mHp, tanbeta)
        # Scale datacards
        a = self.getResult(tanbeta)["brTheory"]
        for i in range(0, len(self._datacardPatterns)):
            myReader = DatacardReader.DataCardReader(".", mHp, self._datacardPatterns[i], self._rootFilePatterns[i], rootFileDirectory="", readOnly=False)
            myReader.scaleSignal(a)
            myReader.close(silent=True)
        print "    Scaled '%s' signal in datacards by branching %f (mHp=%s, tanbeta=%.1f)"%(self._label, a, mHp, tanbeta)
            
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


def getCombineResultPassedStatus(opts, taunuContainer, tbContainer, mHp, tanbeta, resultKey, scen):
    reuseStatus = False
    if not taunuContainer.resultExists(tanbeta):
        # Result does not exist, let's calculate it
        # Produce cards
        taunuContainer.produceScaledCards(mHp, tanbeta)
        tbContainer.produceScaledCards(mHp, tanbeta)
        # Run Combine
        resultContainer = combine.produceLHCAsymptotic(opts, ".", massPoints=[mHp],
            datacardPatterns = taunuContainer.getDatacardPatterns()+tbContainer.getDatacardPatterns(),
            rootfilePatterns = taunuContainer.getRootfilePatterns()+tbContainer.getRootfilePatterns(),
            clsType = combine.LHCTypeAsymptotic(opts),
            postfix = "lhcasy_%s_mHp%s_tanbetascan%.1f"%(scen,mHp,tanbeta),
            quietStatus = True)
        if len(resultContainer.results) > 0:
            result = resultContainer.results[0]
            # Add theoretical uncertainty
            result.observedPlusTheorUncert = result.observed * (1.0 + _theoreticalUncertainty)
            result.observedMinusTheorUncert = result.observed * (1.0 - _theoreticalUncertainty)
            # Store result
            taunuContainer.setCombineResult(tanbeta, result)
            tbContainer.setCombineResult(tanbeta, result)
    else:
        reuseStatus = True
    myContainer = None
    if taunuContainer.resultExists(tanbeta):
        myContainer = taunuContainer
    elif tbContainer.resultExists(tanbeta):
        myContainer = tbContainer
    else:
        raise Exception("No datacards present")
    
    # Print output
    s = "- mHp=%s, tanbeta=%.1f, sigmaTheory=%.3f"%(mHp, tanbeta, myContainer.getResult(tanbeta)["sigmaTheory"])
    if myContainer.getFailedStatus(tanbeta):
        s += " sigmaCombine (%s)=failed"%resultKey
    else:
        s += " sigmaCombine (%s)=%.3f, passed=%d"%(resultKey, myContainer.getCombineResultByKey(tanbeta, resultKey), myContainer.getPassedStatus(tanbeta, resultKey))
    if not reuseStatus:
        print s
    # return limit from combine
    if myContainer.getFailedStatus(tanbeta):
        return None
    return myContainer.getPassedStatus(tanbeta, resultKey)

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
def scan(opts, taunuContainer, tbContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scan):
    print "scanning %s / %.1f-%.1f"%(resultKey, tanbetaMin,tanbetaMax)
    tanbetaMid = findMiddlePoint(tanbetaMin, tanbetaMax)
    if tanbetaMid == None:
        return []
    # Calculate results
    minPassed = getCombineResultPassedStatus(opts, taunuContainer, tbContainer, mHp, tanbetaMin, resultKey, scen)
    midPassed = getCombineResultPassedStatus(opts, taunuContainer, tbContainer, mHp, tanbetaMid, resultKey, scen)
    maxPassed = getCombineResultPassedStatus(opts, taunuContainer, tbContainer, mHp, tanbetaMax, resultKey, scen)
    # Calculate new ranges
    ranges = []
    if minPassed != midPassed:
        ranges.append([tanbetaMin, tanbetaMid])
    if midPassed != maxPassed:
        ranges.append([tanbetaMid, tanbetaMax])
    return ranges

def scanRanges(opts, taunuContainer, tbContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scen):
    myRanges = scan(opts, taunuContainer, tbContainer, mHp, tanbetaMin, tanbetaMax, resultKey, scen)
    for l in myRanges:
        scanRanges(opts, taunuContainer, tbContainer, mHp, l[0], l[1], resultKey, scen)

def readResults(opts, taunuContainer, tbContainer, m, myKey, scen):
    myList = os.listdir(".")
    for name in myList:
        if name.startswith("results_") and name.endswith(".txt"):
            print "Opening file '%s' ..."%name
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
                if lines[myLine].startswith("Tan beta limit scan ("):
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
                    if len(mySplit) > 1:
                        tanbetakey = "%04.1f"%(float(mySplit[0]))
                        if not taunuContainer.resultExists(tanbetakey):
                            taunuContainer._results[tanbetakey] = {}
                            taunuContainer._results[tanbetakey]["sigmaTheory"] = float(mySplit[1])
                            result = commonLimitTools.Result(0)
                            setattr(result, myKey, float(mySplit[2]))
                            taunuContainer.setCombineResult(tanbetakey, result)
                        else:
                            # Add result key
                            setattr(taunuContainer._results[tanbetakey]["combineResult"], myKey, float(mySplit[2]))

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

def main(opts, taunuContainer, tbContainer, m, scen, plotContainers):
    resultKeys = ["observed", "observedPlusTheorUncert", "observedMinusTheorUncert", "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]
    #resultKeys = ["observed","expected"]
    for myKey in resultKeys:
        if opts.analyseOutput:
            readResults(opts, taunuContainer, tbContainer, m, myKey, scen)
        else:
            scanRanges(opts, taunuContainer, tbContainer, m, 1.1, 75, myKey, scen)
    
    outtxt = ""
    # Print results
    myTanBetaKeys = taunuContainer._results.keys()
    myTanBetaKeys.sort()
    for myResultKey in resultKeys:
        outtxt += "\nTan beta limit scan (%s) for m=%s and key: %s\n"%(scen, m,myResultKey)
        for k in myTanBetaKeys:
            theory = taunuContainer.getResult(k)["sigmaTheory"]
            combineResult = ""
            if taunuContainer.getFailedStatus(k):
                combineResult = "failed"
            else:
                combineResult = "%f pb"%getattr(taunuContainer.getResult(k)["combineResult"], myResultKey)
            outtxt += "  tan beta=%s, xsecTheor=%f pb, limit(%s)=%s, passed=%d\n"%(k, theory, myResultKey, combineResult, taunuContainer.getPassedStatus(k, myResultKey))
    
    # Find limits
    outtxt += "\nAllowed tan beta ranges (%s) for m=%s (linear interpolation used)\n"%(scen, m)
    for myResultKey in resultKeys:
        myLowTanBetaLimit = 1.0
        myHighTanBetaLimit = 75
        lowFound = False
        highFound = False
        myPreviousStatus = None
        for i in range(0, len(myTanBetaKeys)):
            if not taunuContainer.getFailedStatus(myTanBetaKeys[i]):
                myCurrentStatus = taunuContainer.getPassedStatus(myTanBetaKeys[i], myResultKey)
                if myPreviousStatus != None:
                    if myPreviousStatus != myCurrentStatus:
                        # Cross-over point, check direction
                        myTbvalue = linearCrossOverOfTanBeta(taunuContainer, myTanBetaKeys[i-1], myTanBetaKeys[i], myResultKey)
                        combineValue = getattr(taunuContainer.getResult(k)["combineResult"], myResultKey)
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
        outtxt +=  "  key='%s' allowed range: %.2f - %.2f\n"%(myResultKey, myLowTanBetaLimit, myHighTanBetaLimit)
        if not lowFound:
            plotContainers[scen].addLowResult(m, myResultKey, None)
        if not highFound:
            plotContainers[scen].addHighResult(m, myResultKey, None)
        
    print outtxt
    f = open(_resultFilename, "a")
    f.write(outtxt)
    f.close()

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
    opts = commonLimitTools.parseOptionParser(parser)
    if opts.rmin == None:
        opts.rmin = "0"
    if opts.rmax == None:
        opts.rmax = "1000" # To facilitate the search for different tan beta values
    
    # MSSM scenario settings
    myScenarios = ["mhmaxup", "mhmodm", "mhmodp", "lightstau", "lightstop", "tauphobic"]
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
        datacardPatternsTauNu = []
        rootFilePatternsTauNu = []
        # taunu, tau+jets final state
        settings = commonLimitTools.GeneralSettings(myDir, opts.masspoints)
        addToDatacards(myDir, myMassPoints, datacardPatternsTauNu, rootFilePatternsTauNu, settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS), settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS))
        # taunu, tau mu final state
        addToDatacards(myDir, myMassPoints, datacardPatternsTauNu, rootFilePatternsTauNu, "datacard_mutau_taunu_m%s_mutau.txt", "shapes_taunu_m%s_btagmultiplicity_j.root")
        # taunu, dilepton final states
        addToDatacards(myDir, myMassPoints, datacardPatternsTauNu, rootFilePatternsTauNu, "DataCard_ee_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_ee.root")
        addToDatacards(myDir, myMassPoints, datacardPatternsTauNu, rootFilePatternsTauNu, "DataCard_emu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_emu.root")
        addToDatacards(myDir, myMassPoints, datacardPatternsTauNu, rootFilePatternsTauNu, "DataCard_mumu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_mumu.root")
        # tb, tau mu final state
        datacardPatternsTB = []
        rootFilePatternsTB = []
        addToDatacards(myDir, myMassPoints, datacardPatternsTB, rootFilePatternsTB, "datacard_mutau_tb_m%s_mutau.txt", "shapes_tb_m%s_btagmultiplicity_j.root")
        # tb, dilepton final states
        addToDatacards(myDir, myMassPoints, datacardPatternsTB, rootFilePatternsTB, "DataCard_ee_tb_m%s.txt", "CrossSectionShapes_tb_m%s_ee.root")
        addToDatacards(myDir, myMassPoints, datacardPatternsTB, rootFilePatternsTB, "DataCard_emu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_emu.root")
        addToDatacards(myDir, myMassPoints, datacardPatternsTB, rootFilePatternsTB, "DataCard_mumu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_mumu.root")
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
                if not scen in myPlots.keys():
                    myPlots[scen] = TanBetaResultContainer(scen, myMassPoints)
                taunuContainer = BrContainer("Hp_taunu",datacardPatternsTauNu, rootFilePatternsTauNu, "BR_Hp_taunu", scen)
                tbContainer = BrContainer("Hp_tb",datacardPatternsTB, rootFilePatternsTB, "BR_Hp_tb", scen)
                main(opts, taunuContainer, tbContainer, m, scen, myPlots)
    print "\nTan beta scan is done, results have been saved to %s"%_resultFilename
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    for scen in myScenarios:
        myPlots[scen].doPlot()
