#! /usr/bin/env python

import os
import sys
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.limit as limit
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

class MLFitRootFileReader:
    def __init__(self, workdirpath):
        print "Reading directory",workdirpath
        self._workdirpath = workdirpath
        self._massPoints = []
        self._label = None
        self._mu_sb = {}
        self._mu_b = {}
        
        self._extractVariationName(workdirpath)
        self._findMassPoints()
        self._read()
        
    def _extractVariationName(self, myPath):
        mySubPath = myPath.split("/")
        for item in mySubPath:
            if "SHAPETEST" in item:
                mySplit = item.split("_")
                for i in range(0,len(mySplit)):
                    if mySplit[i] == "SHAPETEST":
                        myShapeSensitivityTestLabel = "_".join(map(str,mySplit[i+1:len(mySplit)]))
                        myShapeSensitivityTestLabel = myShapeSensitivityTestLabel.replace("UP","Up").replace("DOWN","Down")
                        self._label = myShapeSensitivityTestLabel
                        return
        raise Exception()
    
    def _findMassPoints(self):
        myList = os.listdir(self._workdirpath)
        for item in myList:
            if os.path.isdir(os.path.join(self._workdirpath,item)) and item.startswith("mlfit_m"):
                self._massPoints.append(item.replace("mlfit_m",""))
        if len(self._massPoints) == 0:
            raise Exception("Could not find mlfit result directories in '%s'! Did you run the ML fits?"%item)

    def _read(self):
        for m in self._massPoints:
            # Open root file
            myFileName = os.path.join(self._workdirpath, "mlfit_m%s"%m, "mlfit.root")
            myRootFile = ROOT.TFile.Open(myFileName)
            if myRootFile == None:
                raise Exception("Could not open %s!"%myFileName)
            # Get tree for sb
            myTree = myRootFile.Get("tree_fit_sb")
            myTree.GetEntry(0)
            self._mu_sb[m] = myTree.GetLeaf("mu").GetValue()
            myTree.Delete()
            # Get tree for b-only
            myTree = myRootFile.Get("tree_fit_b")
            myTree.GetEntry(0)
            self._mu_b[m] = myTree.GetLeaf("mu").GetValue()
            myTree.Delete()
            myRootFile.Close()

    def printSB(self):
        for key in self._mu_sb:
            print "%s: mu_b = %f, mu_sb = %f"%(key, self._mu_b[key], self._mu_sb[key])

    def getLabel(self):
        return self._label

    def getMassPoints(self):
        return self._massPoints
      
    def getMuSB(self, mass):
        return self._mu_sb[mass]

    def getMuBOnly(self, mass):
        return self._mu_b[mass]

    def getRelativeMuSB(self, mass, ctrl):
        return abs(self._mu_sb[mass]/ctrl)

    def getRelativeMuBOnly(self, mass, ctrl):
        return abs(self._mu_b[mass]/ctrl)


def getCombineWorkDirList(myPath):
    myOutList = []
    myList = os.listdir(myPath)
    for item in myList:
        if item.startswith("CombineMultiCrab_") and os.path.join(myPath,item):
            myOutList.append(os.path.join(myPath,item))
        elif os.path.isdir(item):
            myOutList.extend(getCombineWorkDirList(os.path.join(myPath,item)))
    return myOutList

if __name__ == "__main__":
    # Get list of combine work dirs
    myWorkDirs = getCombineWorkDirList(".")
    # Organize the directories
    myVariationDirs = []
    myCtrlDir = None
    for d in myWorkDirs:
        if "SHAPETEST" in d:
            if "CONTROL" in d:
                myCtrlDir = d
            else:
                myVariationDirs.append(d)
    # Check that control dir exists
    if myCtrlDir == None:
        raise Exception("Could not find control combine work directory!")
    if len(myVariationDirs) == 0:
        raise Exception("Could not find combine work directories for variations!")
    # Read input
    myCtrlReader = MLFitRootFileReader(myCtrlDir)
    myVariationReaders = []
    for item in myVariationDirs:
        myVariationReaders.append(MLFitRootFileReader(item))
    # Analyse
    for m in myCtrlReader.getMassPoints():
        myCtrlValue = myCtrlReader.getMuSB(m)
        print "\nm=%s, ctrl mu=%f"%(m, myCtrlValue)
        for r in sorted(myVariationReaders, key=lambda x: x.getRelativeMuSB(m, myCtrlValue), reverse=True):
            print "%40s, mu=%g, diff=%.6f"%(r.getLabel(), r.getMuSB(m), r.getRelativeMuSB(m, myCtrlValue))

