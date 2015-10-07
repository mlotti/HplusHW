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

import HiggsAnalysis.LimitCalc..CombineTools as combine
import HiggsAnalysis.LimitCalc..CommonLimitTools as commonLimitTools
import HiggsAnalysis.LimitCalc..tanbetaTools as tbtools
import HiggsAnalysis.LimitCalc.DatacardReader as DatacardReader
import HiggsAnalysis.LimitCalc..BRXSDatabaseInterface as BRXSDB

import os
import sys
import array
import math

_resultFilename = "results.txt"

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
    if opts.creategridjobs:
        return None
    
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

def main(opts, brContainer, m, scen, plotContainers):
    resultKeys = tbtools._resultKeys[:]
    #resultKeys = ["observed","expected"]
    if opts.gridRunAllMassesInOneJob:
        resultKeys = ["observed"]
    for myKey in resultKeys:
        # Force calculation of few first points
        myTanBetaValues = []
        if len(opts.tanbeta) > 0:
            for tb in opts.tanbeta:
                if not float(tb) in myTanBetaValues:
                    myTanBetaValues.append(float(tb))
        if len(opts.tanbetarangemin) > 0 and len(opts.tanbetarangemax) > 0:
            tb = float(opts.tanbetarangemin[0])
            while tb < float(opts.tanbetarangemax[0]) and tb <= tbtools._maxTanBeta:
                myTanBetaValues.append(tb)
                if tb < 10:
                    tb += 0.1
                else:
                    tb += 1
        if len(myTanBetaValues) > 0:
            print "Considering tan beta values:", myTanBetaValues
            for tb in myTanBetaValues:
                getCombineResultPassedStatus(opts, brContainer, m, tb, myKey, scen)
        else:
            if float(m) > 179:
                getCombineResultPassedStatus(opts, brContainer, m, 1.1, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.2, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.3, myKey, scen)
                getCombineResultPassedStatus(opts, brContainer, m, 1.4, myKey, scen)
            scanRanges(opts, brContainer, m, tbtools_minTanBeta, 7.9, myKey, scen)
            scanRanges(opts, brContainer, m, 8.0, tbtools._maxTanBeta, myKey, scen)
    
    if opts.creategridjobs:
        return
      
    #tbtools.saveTanbetaResults(brContainer, plotContainers[scen], scen, m, resultKeys)

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
    parser.add_option("--scen", dest="scenarios", action="append", default=[], help="MSSM scenarios")
    parser.add_option("-t", "--tanbeta", dest="tanbeta", action="append", default=[], help="tanbeta values (will scan only these)")
    parser.add_option("--tanbetarangemin", dest="tanbetarangemin", action="append", default=[], help="tanbeta values minimum range")
    parser.add_option("--tanbetarangemax", dest="tanbetarangemax", action="append", default=[], help="tanbeta values maximum range")
    parser.add_option("--evalUuncert", dest="evaluateUncertainties", action="store_true", default=False, help="Make plots of theoretical uncertainties")
    parser.add_option("--creategridjobs", dest="creategridjobs", action="store_true", default=False, help="Create crab task dirs for running on grid")
    parser.add_option("--gridmassive", dest="gridRunAllMassesInOneJob", action="store_true", default=False, help="Crab jobs run all masses in one job (default=1 job / mass)")
    opts = commonLimitTools.parseOptionParser(parser)
    if opts.rmin == None:
        opts.rmin = "0"
    if opts.rmax == None:
        opts.rmax = "1" # To facilitate the search for different tan beta values
    
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
            myCategory = {"Hp_tb": ["HpToSingleLepton_datacard_"+l+"_%s.txt", "HpToSingleLepton_HT_M%s_"+l+".root"]}
            myDecayModeMatrix["ljets_%s"%l] = myCategory
        myLabels = ["Control_nB0_mu", "Control_nB1_mu", "Control_nB2p_mu", "Control_nB0_el", "Control_nB1_el", "Control_nB2p_el"]
        for l in myLabels:
            myCategory = {"Hp_tb": ["HpToSingleLepton_datacard_"+l+".txt", "HpToSingleLepton_HT_CR_"+l+".root"]}
            myDecayModeMatrix["ljets_%s"%l] = myCategory
        
        # Purge matrix
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
                if opts.gridRunAllMassesInOneJob:
                    if m == myMassPoints[0]:
                        print scen
                else:
                    print scen,m
                if not scen in myPlots.keys():
                    myPlots[scen] = tbtools.TanBetaResultContainer(scen, myMassPoints)
                brContainer = tbtools.BrContainer(myDecayModeMatrix, scen, myMassPoints)
                main(opts, brContainer, m, scen, myPlots)
    
    if opts.creategridjobs:
        # Print instructions
        print "*** Created crab task dirs for multicrab ***"
        print "*** To submit, retrieve and obtain results run tanbetaOmatic.py ***"
    else:
        # interactive running
        print "*** Tan beta scan is done ***"
        print "*** To do plots, run brlimit/tanbetaReadResults.py ***"
