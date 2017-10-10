## \package multicrabConsistencyCheck

import os
import sys

histogramName = "SplittedBinInfo"

def getNumberOfJobsFromMultiCrabCfg(multicrabDir):
    myFile = open(multicrabDir+"/multicrab.cfg")
    myLines = myFile.readlines()
    myFile.close()
    myDict = {}
    myDsetName = None
    for line in myLines:
        if not line.startswith("#"):
            if "[" in line and "]" in line:
                myDsetName = line.replace("[","").replace("]","").replace("#","").replace("\n","")
            if "CMSSW.number_of_jobs" in line:
                myNumber = line.replace("CMSSW.number_of_jobs","").replace(" ","").replace("=","").replace("#","").replace("\n","")
                myDict[myDsetName] = int(myNumber)
    return myDict

def getNumberOfJobsFromMergedHistogramsFromDsetMgr(dsetMgr,myMergedDict):
    for dset in dsetMgr.getAllDatasets():
        (h,hname) = dset.getRootHisto(histogramName)
        if h == None:
            raise Exception("Error: cannot find histogram %s in file %s"%(histogramName, dset.getName()))
        if h.GetXaxis().GetBinLabel(1) != "Control":
            raise Exception()
        n = int(h.GetBinContent(1))
        if dset.getName() in myMergedDict.keys():
            if n != myMergedDict[dset.getName()]:
                raise Exception("dset %s: number of jobs alternates inside the merged root file!"%dset.getName())
        else:
            myMergedDict[dset.getName()] = n

def checkConsistency(myDict, myMergedDict, name=None, printStatus=False):
    myGoodStatus = True
    myTable = []
    myKeys = myMergedDict.keys()
    myKeys.sort()

    # For-loop: All datasets
    for m in myKeys:
        myStatus = False
        
        if 0:
            print m
            print myDict.keys()
            print
            
        # For-loop: All keys
        for k in myDict.keys():
            print "myDict[%s] = %s" % (k, myDict[k])
            if m == k:
                myStatus = True
                if myMergedDict[m] == myDict[k]:
                    myTable.append([k, "OK"])
                elif myMergedDict[m] <= myDict[k]:
                    myTable.append([k, "merged root file contains %d jobs instead of requested %d jobs -> this is recoved automatically for MC (although stat. resolution is poorer)"%(myMergedDict[m],myDict[k])])
                else:
                    myTable.append([k, "merged root file contains %d jobs instead of requested %d jobs -> ERROR: you need to rerun the multicrab or hplusMultiCrabMerge.py for this dataset!"%(myMergedDict[m],myDict[k])])
                    myGoodStatus = False
    if printStatus or not myGoodStatus:
        if name == None:
            print "\nMulticrab consistency check:"
        else:
            print "\nMulticrab consistency check (%s):" % name
        col_width = [max(len(x) for x in col) for col in zip(*myTable)]
        for line in myTable:
            print "| %s | %s |"%(line[0].ljust(col_width[0]), line[1].ljust(col_width[1]))
        print
    if not myGoodStatus:
        raise Exception("Error: did not pass consistency check, see table above!")
    return

def checkConsistencyStandalone(multicrabDir, dsetMgr, name=None, printStatus=False):
    if printStatus:
        print "=== multicrabConsistencyCheck.py: Unsure if obsolete or not! The code needs to checked"
    myDict = getNumberOfJobsFromMultiCrabCfg(multicrabDir)
    myMergedDict = {}
    getNumberOfJobsFromMergedHistogramsFromDsetMgr(dsetMgr, myMergedDict)
    checkConsistency(myDict, myMergedDict, name, printStatus)
    return
