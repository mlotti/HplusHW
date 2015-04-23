#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CombineTools as CombineTools
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as commonLimitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tanbetaTools as tbtools

import os
import sys
from optparse import OptionParser

def findTaskDirs(currentDir):
    myCollection = []
    myList = os.listdir(currentDir)
    for item in myList:
        if item.startswith(CombineTools.taskDirprefix):
            myCollection.append(item)
        elif os.path.isdir(item):
            myCollection.extend(findTaskDirs(os.path.join(currentDir,item)))
    return myCollection

def analyseTaskDir(taskDir, scenarioData, scenario, massWhiteList, massPoints):
    myScenario = None
    myTanbeta = None
    mySplit = taskDir.split("_")
    myScenario = mySplit[2]
    if myScenario != scenario:
        # Scenario not requested, do not consider it
        return
    myTanbeta = mySplit[4].replace("tanbetascan","")
    myList = os.listdir(taskDir)
    for item in myList:
        if item.startswith("higgsCombineobs_") and item.endswith(".root"):
            mySplit = item.split(".")
            myMass = mySplit[len(mySplit)-2].replace("mH","")
            if len(massWhiteList) > 0:
                if not myMass in massWhiteList:
                    continue
            if not myMass in massPoints:
                massPoints.append(myMass)
            # Read result
            myResult = commonLimitTools.Result(myMass)
            myStatus = CombineTools.parseResultFromCombineOutput(taskDir, myResult, myMass)
            if myStatus != 6: # 1 obs + 5 exp values
                # Combine failed
                myResult.failed = True
            # Store result
            myKey = tbtools.constructResultKey(myMass, myTanbeta)
            if myKey in scenarioData.keys():
                raise Exception("Duplicate results for scenario=%s mass=%s tanbeta=%s! Remove wrong ones and then rerun!"%(myScenario, myMass, myTanbeta))
            scenarioData[myKey] = {}
            scenarioData[myKey]["combineResult"] = myResult
            print "Result found for scenario=%s mass=%s tanbeta=%s"%(myScenario, myMass, myTanbeta)

def produceOutputFromTaskDirs(massWhiteList, scenario):
    myScenarioData = {}
    myResultKeys = tbtools._resultKeys[:]
    # Get list of task directories
    myTaskDirs = findTaskDirs(".")
    # Loop over task directories
    myMassPoints = []
    for d in myTaskDirs:
        analyseTaskDir(d, myScenarioData, scenario, massWhiteList, myMassPoints)
    myMassPoints.sort()
    if len(myScenarioData.keys()) == 0:
        return
    # Construct objects
    brContainer = tbtools.BrContainer(decayModeMatrix=None, mssmModel=scenario)
    brContainer._results = myScenarioData
    # Obtain theoretical xsection values form database
    for myKey in myScenarioData.keys():
        myKeyComponents = tbtools.disentangleResultKey(myKey)
        brContainer._readFromDatabase(myKeyComponents["m"], myKeyComponents["tb"])
    # Write
    myPlotContainer = tbtools.TanBetaResultContainer(scenario, myMassPoints)
    tbtools.saveTanbetaResults(brContainer, myPlotContainer, scenario, myMassPoints, myResultKeys)
    # Do a plot
    myPlotContainer.doPlot()
    
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--scen", dest="scenarios", action="append", default=[], help="MSSM scenarios")
    parser.add_option("-m", "--mass", dest="massPoints", action="append", default=[], help="mass values (will scan only these)")
    (opts, args) = parser.parse_args()
    # Parse selected models
    myModelNames = tbtools.findModelNames(".")
    mySelectedModels = opts.scenarios
    if len(opts.scenarios) == 0:
        mySelectedModels = myModelNames[:]
    # Loop over scenario models
    resultKeys = ["observed",  "expected", "expectedPlus1Sigma", "expectedPlus2Sigma", "expectedMinus1Sigma", "expectedMinus2Sigma"]
    for m in myModelNames:
        print "Considering model: %s"%m
        # result structure: dictionary(key=m_tb, value=Result))
        if os.path.exists(tbtools._resultsPattern%m):
            # Results text file exists, read them
            print "..."
        else:
            # Convert root files from crab jobs to text files for inspection
            produceOutputFromTaskDirs(opts.massPoints, m)
