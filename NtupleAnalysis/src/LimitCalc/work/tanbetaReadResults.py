#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.LimitCalc..CombineTools as CombineTools
import HiggsAnalysis.LimitCalc..CommonLimitTools as commonLimitTools
import HiggsAnalysis.LimitCalc..tanbetaTools as tbtools
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle

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

def produceOutputFromTaskDirs(massWhiteList, scenario, mAtanbetaStatus):
    print "Reading input from task directories"
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
        return False
    # Construct objects
    brContainer = tbtools.BrContainer(decayModeMatrix=None, mssmModel=scenario)
    brContainer._results = myScenarioData
    # Obtain theoretical xsection values form database
    for myKey in myScenarioData.keys():
        myKeyComponents = tbtools.disentangleResultKey(myKey)
        brContainer._readFromDatabase(myKeyComponents["m"], myKeyComponents["tb"])
    # Analyze and write
    myPlotContainer = tbtools.TanBetaResultContainer(scenario, myMassPoints)
    tbtools.analyzeTanbetaResults(brContainer, myPlotContainer, scenario, myMassPoints, myResultKeys, saveToDisk=True)
    # Create plot
    myPlotContainer.doPlot(mAtanbetaStatus)
    return True 

def parseTextResultsFromFile(brContainer, massWhiteList, scen, resultKeys):
    # Read 
    name = tbtools._resultsPattern%scen
    print "Opening file '%s' for input"%(name)
    f = open(name)
    if f == None:
        raise Exception("Error: Could not open result file '%s' for input!"%name)
    lines = f.readlines()
    f.close()
    # Obtain mass points
    myMassPoints = []
    if len(massWhiteList) > 0:
        myMassPoints = massWhiteList[:]
    else:
        myLine = 0
        while myLine < len(lines):
            if lines[myLine].startswith("Tan beta limit scan ("):
                s = lines[myLine].replace("Tan beta limit scan (","").replace(") for m=",",").replace(" and key: ",",").replace("\n","")
                mySplit = s.split(",")
                m = mySplit[1]
                if not m in myMassPoints:
                    myMassPoints.append(m)
            myLine += 1
    myMassPoints.sort()
    # Analyse lines
    for m in myMassPoints:
        for myKey in resultKeys:
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
                    if len(mySplit) > 1 and s[0] != "#" and not mySplit[2] in ["failed","n.a.",""] and mySplit[1] != "None":
                        myTanBeta = mySplit[0]
                        tanbetakey = tbtools.constructResultKey(m, myTanBeta)
                        if not brContainer.resultExists(m, myTanBeta):
                            brContainer._results[tanbetakey] = {}
                            if mySplit[1] == "None":
                                brContainer._results[tanbetakey]["sigmaTheory"] = None
                            else:
                                brContainer._results[tanbetakey]["sigmaTheory"] = float(mySplit[1])
                            result = commonLimitTools.Result(0)
                            setattr(result, myKey, float(mySplit[2]))
                            brContainer.setCombineResult(m, myTanBeta, result)
                        else:
                            # Add result key
                            setattr(brContainer._results[tanbetakey]["combineResult"], myKey, float(mySplit[2]))
    return myMassPoints

def readTextResults(massWhiteList, scen, mAtanbetaStatus):
    myResultKeys = tbtools._resultKeys[:]
    # Create BrContainer
    brContainer = tbtools.BrContainer(decayModeMatrix=None, mssmModel=scen)
    # Parse input text file
    myMassPoints = parseTextResultsFromFile(brContainer, massWhiteList, scen, myResultKeys)
    # Analyze
    myPlotContainer = tbtools.TanBetaResultContainer(scen, myMassPoints)
    tbtools.analyzeTanbetaResults(brContainer, myPlotContainer, scen, myMassPoints, myResultKeys, saveToDisk=False)
    # Create plot
    myPlotContainer.doPlot(mAtanbetaStatus)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--scen", dest="scenarios", action="append", default=[], help="MSSM scenarios")
    parser.add_option("-m", "--mass", dest="massPoints", action="append", default=[], help="mass values (will scan only these)")
    parser.add_option("--mAtanbeta", dest="mAtanbeta", action="store_true", default=False, help="do mA,tanbeta plot (default=mHp,tanbeta)")
    (opts, args) = parser.parse_args()
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    # Parse selected models
    myModelNames = tbtools.findModelNames(".")
    mySelectedModels = myModelNames[:]
    if len(opts.scenarios) > 0:
        mySelectedModels = opts.scenarios[:]
    # Loop over scenario models
    myPrintReminderStatus = False
    for m in mySelectedModels:
        print "Considering model: %s"%m
        # result structure: dictionary(key=m_tb, value=Result))
        print tbtools._resultsPattern%m
        if os.path.exists(tbtools._resultsPattern%m):
            # Results text file exists, read them
            readTextResults(opts.massPoints, m, opts.mAtanbeta)
        else:
            # Convert root files from crab jobs to text files for inspection
            myStatus = produceOutputFromTaskDirs(opts.massPoints, m, opts.mAtanbeta)
            myPrintReminderStatus = myPrintReminderStatus or myStatus
    if myPrintReminderStatus:
        print "\nImportant: please edit now the txt files to fix any bad converging of combine results (can happen for observed)"
        print "When done, execute the same command (tanbetaReadResults.py) to produce the plots with the txt files as input"
