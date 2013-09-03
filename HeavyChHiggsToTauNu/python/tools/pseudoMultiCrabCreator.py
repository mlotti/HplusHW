## \package PseudoMultiCrabCreator
# Description: used for creating a root file and proper directory structure to fool the dataset.py to think
# it is a genuine multicrab directory
#
# Use cases: Converterting QCD measuerement results to readable format for the datacard generator
#
# Authors: Lauri A. Wendland

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
import shutil
from math import sqrt

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

class PseudoMultiCrabCreator:
    ## Constructor
    # title is a string that goes to the multicrab directory name
    def __init__(self, title, inputMulticrabDir):
        self._title = title
        self._modulesList = [] # List of PseudoMultiCrabModule objects
        self._inputMulticrabDir = inputMulticrabDir

    def addModule(self, module):
        self._modulesList.append(module)

    def writeToDisk(self):
        # Create directory structure
        myDir = "pseudoMulticrab_%s"%self._title
        if os.path.exists(myDir):
            shutil.rmtree(myDir)
        os.mkdir(myDir)
        os.mkdir("%s/data"%myDir)
        os.mkdir("%s/data/res"%myDir)
        # Open root file
        myRootFile = ROOT.TFile("%s/data/res/histograms-data.root"%myDir,"CREATE")
        # Write modules
        for m in self._modulesList:
            m.writeModuleToRootFile(myRootFile)
        # Create config info histogram
        myRootFile.cd("/")
        myRootFile.mkdir("configInfo")
        myRootFile.cd("configInfo")
        hConfigInfo = ROOT.TH1F("configinfo","configinfo",4,0,4)
        hConfigInfo.GetXaxis().SetBinLabel(1,"control")
        hConfigInfo.SetBinContent(1, 1)
        hConfigInfo.GetXaxis().SetBinLabel(2,"energy")
        hConfigInfo.SetBinContent(2, 0)
        hConfigInfo.GetXaxis().SetBinLabel(3,"crossSection")
        hConfigInfo.SetBinContent(3, 1)
        hConfigInfo.GetXaxis().SetBinLabel(4,"isData")
        hConfigInfo.SetBinContent(4, 1)
        # Note that data version and code version are stored to the modules
        # Write and close the root file
        myRootFile.Write()
        myRootFile.Close()
        # Copy lumi.json file from input multicrab directory
        os.system("cp %s/lumi.json %s"%(self._inputMulticrabDir, myDir))
        # Create multicrab.cfg
        f = open(os.path.join(myDir, "multicrab.cfg"), "w")
        f.write("# Ultimate pseudo-multicrab for fooling dataset.py, created by PseudoMultiCrabCreator\n")
        f.write("[data]\n")
        f.close()
        # Done
        print HighlightStyle()+"Created pseudo-multicrab directory %s%s"%(myDir,NormalStyle())

class PseudoMultiCrabModule:
    ## Constructor
    def __init__(self, dsetMgr, era, searchMode, optimizationMode, systematicsVariation=None):
        # Note that 'signalAnalysis' only matters for dataset.py to find the proper module
        self._moduleName = "signalAnalysis%s%s"%(searchMode, era)
        if optimizationMode != "" and optimizationMode != None:
            self._moduleName += "%s"%optimizationMode
        if systematicsVariation != None:
            self._moduleName += "SystVar%s"%systematicsVariation
        # Initialize containers
        self._shapes = [] # Shape histograms
        self._dataDrivenControlPlots = [] # Data driven control plot histograms
        self._counters = {} # Dictionary for counter values to be stored
        self._counterUncertainties = {} # Dictionary for counter values to be stored
        self._hCounters = None
        # Obtain luminosity information and store it as a counter
        myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
        self._counters["luminosity"] = myLuminosity
        self._counterUncertainties["luminosity"] = 0
        # Copy splittedBinInfo (for self-documenting)
        self._hSplittedBinInfo = dsetMgr.getDataset("Data").getDatasetRootHisto("SplittedBinInfo").getHistogram().Clone()
        for i in range(2,self._hSplittedBinInfo.GetNbinsX()+1):
            self._hSplittedBinInfo.SetBinContent(i, self._hSplittedBinInfo.GetBinContent(i)/self._hSplittedBinInfo.GetBinContent(1))
        self._hSplittedBinInfo.SetName("SplittedBinInfo")
        # Copy parameter set information
        (objs, realNames) = dsetMgr.getDataset("Data").datasets[0].getRootObjects("parameterSet")
        self._psetInfo = objs[0].Clone()
        # Copy data version
        (objs, realNames) = dsetMgr.getDataset("Data").datasets[0].getRootObjects("../configInfo/dataVersion")
        self._dataVersion = objs[0].Clone()
        # Copy code version
        (objs, realNames) = dsetMgr.getDataset("Data").datasets[0].getRootObjects("../configInfo/codeVersion")
        self._codeVersion = objs[0].Clone()

    def addShape(self, shapeHisto, plotName):
        self._shapes.append(shapeHisto.Clone(plotName))
        myValue = 0.0
        myUncert = 0.0
        for i in range(1, shapeHisto.GetNbinsX()+1):
            myValue += shapeHisto.GetBinContent(i)
            myUncert += shapeHisto.GetBinError(i)**2
        self._counters[plotName] = myValue
        self._counterUncertainties[plotName] = sqrt(myUncert)

    def addDataDrivenControlPlot(self, histo, name):
        self._dataDrivenControlPlots.append(histo.Clone("%s%s"%(name,h.GetTitle())))

    def addDataDrivenControlPlots(self, histoList, name):
        for h in histoList:
            self._dataDrivenControlPlots.append(h.Clone("%s%s"%(name,h.GetTitle())))

    def writeModuleToRootFile(self, rootfile):
        # Create module directory
        rootfile.cd("/")
        myModuleDir = rootfile.mkdir(self._moduleName)
        # Save shape information
        for h in self._shapes:
            h.SetDirectory(myModuleDir)
        # Save data-driven control plots
        myDDPlotsDirName = "ForDataDrivenCtrlPlots"
        myDDPlotsDir = myModuleDir.mkdir(myDDPlotsDirName)
        for h in self._dataDrivenControlPlots:
            h.SetDirectory(myDDPlotsDir)
        # Save counter histogram
        myCounterDir = myModuleDir.mkdir("counters")
        myWeightedCounterDir = myCounterDir.mkdir("weighted")
        self._hCounters = ROOT.TH1F("counter","counter",len(self._counters),0,len(self._counters))
        i = 1
        for key in self._counters.keys():
            self._hCounters.GetXaxis().SetBinLabel(i, key)
            i += 1
            self._hCounters.SetBinContent(i, self._counters[key])
            self._hCounters.SetBinError(i, self._counterUncertainties[key])
        self._hCounters.SetDirectory(myWeightedCounterDir)
        # Save splittedBinInfo
        self._hSplittedBinInfo.SetDirectory(myModuleDir)
        # Save parameter set, code version and data version
        myModuleDir.Add(self._psetInfo)
        myModuleDir.Add(self._dataVersion)
        myModuleDir.Add(self._codeVersion)
        #self._psetInfo.SetDirectory(rootfile)
        #.SetDirectory(rootfile)
        #self._codeVersion.SetDirectory(rootfile)

