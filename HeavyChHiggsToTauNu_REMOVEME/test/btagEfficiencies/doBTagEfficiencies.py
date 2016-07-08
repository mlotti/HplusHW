#!/usr/bin/env python

######################################################################
#
# This plot script is for producing the btag efficiency curves
#
# Authors: Shih-Yen Tseng, Lauri Wendland, (Stefan Richter)
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

from optparse import OptionParser
import time
import os
import shutil

# main function
def main(opts,signalDsetCreator,era,searchMode,optimizationMode):
    # Make directory for output
    mySuffix = "btagEfficiency_%s_%s_%s_%s"%(opts.dset,era,searchMode,optimizationMode)
    if os.path.exists(mySuffix):
        shutil.rmtree(mySuffix)
    os.mkdir(mySuffix)
    # Create dataset manager
    myDsetMgr = signalDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    # Set as luminosity 1 fb (since one looks only at MC)
    myLuminosity = 1000.0
    # Do merges
    style = tdrstyle.TDRStyle()
    myDsetMgr.updateNAllEventsToPUWeighted()
    plots.mergeRenameReorderForDataMC(myDsetMgr)
    # Set defaults for histograms
    histograms.createLegend.moveDefaults(dx=-0.05)
    histograms.createSignalText.set(xmin=0.4, ymax=0.93, mass=120)
    # Show info of available datasets
    myDsetMgr.printDatasetTree()

    # Create plots
    #distributionPtEta(opts, myDsetMgr, myLuminosity, mySuffix) # FIXME: don't think this is used anymore
    efficiencyplot(opts, myDsetMgr, myLuminosity, mySuffix) # Tested and works

    print HighlightStyle()+"\nResults saved to directory: %s%s"%(mySuffix,NormalStyle())

#def failsafeProjection(inputHistogram, outputHistogram, axis, rangeMin, rangeMax):
    ## Create temporary histogram
    #myAxis = None
    #if axis == "X":
        #myAxis = inputHistogram.GetXaxis()
    #elif axis == "Y":
        #myAxis = inputHistogram.GetYaxis()
    #h = ROOT.TH1F("htemp","htemp", myAxis.GetNbins(), myAxis.GetXmin(), myAxis.GetXmax())
    ## Loop over bins of input histogram
    #for i in range(1,inputHistogram.GetNbinsX()+1):
        #for j in range(1,inputHistogram.GetNbinsY()+1):
            #if axis == "X":
                ## Check if the current bin is in the selected range
                #if myAxis.GetBinLowEdge(i) >= rangeMin and myAxis.GetBinUpEdge(i) <= rangeMax:
                    ## Add values (use squared sum for uncertainties)
                    #h.SetBinContent(i, h.GetBinContent(i)+inputHistogram.GetBinContent(i,j))
                    #h.SetBinError(i, h.GetBinError(i)+(inputHistogram.GetBinError(i,j)**2))
            #elif axis == "X":
                ## Check if the current bin is in the selected range
                #if myAxis.GetBinLowEdge(j) >= rangeMin and myAxis.GetBinUpEdge(j) <= rangeMax:
                    ## Add values (use squared sum for uncertainties)
                    #h.SetBinContent(j, h.GetBinContent(j)+inputHistogram.GetBinContent(i,j))
                    #h.SetBinError(j, h.GetBinError(j)+(inputHistogram.GetBinError(i,j)**2))
    ## Temporary histogram has been filled, now take square root of its errors to get correct uncertainties
    #for i in range(1,h.GetNbinsX()+1):
        #h.SetBinError(i, sqrt(h.GetBinError(i)))
    ## Set output object
    #outputHistogram = h.Clone()

#def distributionPtEta(opts, dsetMgr, luminosity, myDir):
    #myAllJetsLabel = "BTaggingEfficiencyInMC/genuineBJetPtAndEta"
    #myBtaggedJetsLabel = "BTaggingEfficiencyInMC/genuineBJetWithBTagPtAndEta"
    #myRangeList = [-3,-2,-1,0,1,2,3]

    ## Specify output histogram binning
    #myHistoSpecs = {
      #"rangeMin": 0.0,
      #"rangeMax": 500.0,
      #"variableBinSizeLowEdges": [20,40,60,80,100,120,140,160,200,250,300,350,400], # if an empty list is given, then uniform bin width is used
      #"xtitle": "Jet p_{T} / GeV/c",
      #"ytitle": "Arb. units"
    #}

    ## Obtain histograms
    #myAllJetsDsetHisto = dsetMgr.getDataset(opts.dset).getDatasetRootHisto(myAllJetsLabel)
    #myAllJetsDsetHisto.normalizeToLuminosity(luminosity)
    #hAllJets = myAllJetsDsetHisto.getHistogram()
    #myBJetsDsetHisto = dsetMgr.getDataset(opts.dset).getDatasetRootHisto(myBJetsLabel)
    #myBJetsDsetHisto.normalizeToLuminosity(luminosity)
    #hBJets = myBJetsDsetHisto.getHistogram()
    ## Setup histogramming
    #myModifier = ShapeHistoModifier(myHistoSpecs)

    ## Loop over ranges
    #for i in range(0,len(myRangeList)-1):
        #myRangeMin = myRangeList[i]
        #myRangeMax = myRangeList[i+1]
        ## Obtain histogram for all jets
        #myName = "AllJetsPt_forEtaSlice_%d_%d"%(myRangeMin, myRangeMax)
        #myName.replace("-","n")
        #h = myModifier.createEmptyShapeHistogram(myName)
        #hResult = None
        #failsafeProjection(hAllJets, hResult, "Y", myRangeMin, myRangeMax)
        #myModifier.addShape(source=hResult, dest=h)
        #myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        ## Make plot
        #plot = plots.PlotBase([histograms.Histo(h,"shape",drawStyle="E")])
        #plot.createFrame("%s/%s"%(myDir,myName), opts={"addMCUncertainty": True})
        #plot.frame.GetXaxis().SetTitle(histoSpecs["xtitle"])
        #plot.frame.GetYaxis().SetTitle(histoSpecs["ytitle"])
        #styles.dataStyle(plot.histoMgr.getHisto("shape"))
        #drawPlot(plot,myDir)
        ## Obtain histogram for b jets
        #myName = "BJetsPt_forEtaSlice_%d_%d"%(myRangeMin, myRangeMax)
        #myName.replace("-","n")
        #h = myModifier.createEmptyShapeHistogram(myName)
        #hResult = None
        #failsafeProjection(hBJets, hResult, "Y", myRangeMin, myRangeMax)
        #myModifier.addShape(source=hResult, dest=h)
        #myModifier.finaliseShape(dest=h) # Convert errors from variances to std.devs.
        ## Make plot
        #plot = plots.PlotBase([histograms.Histo(h,"shape",drawStyle="E")])
        #plot.createFrame("%s/%s"%(myDir,myName), opts={"addMCUncertainty": True})
        #plot.frame.GetXaxis().SetTitle(histoSpecs["xtitle"])
        #plot.frame.GetYaxis().SetTitle(histoSpecs["ytitle"])
        #styles.dataStyle(plot.histoMgr.getHisto("shape"))
        #drawPlot(plot,myDir)

class BtagEfficiencyResult:
    def __init__(self):
        self._resultString = ""

    def addGeneralInfo(self, label):
        # Give some auto-documentation
        self._resultString += "// This code was auto-generated by plotBtagEfficiency.py at %s\n"%time.ctime()
        self._resultString += "// It contains tagging efficiencies measured in %s\n"%label
        self._resultString += "// Uncertainties displayed are absolute uncertainties\n"

    def addBinning(self, label, binList):
        # Give some auto-documentation
        s = "// %s bins are: "%label
        for i in range(0,len(binList)-1):
            s += "%.1f..%.1f, "%(binList[i],binList[i+1])
        s += ">%.1f\n"%binList[len(binList)-1]
        s += "// Note that last bin contains also overflow bin\n\n"
        # Now write the actual data
        s += "double %sBinLowEdges[] = {"%label
        s += ", ".join(map(str, binList))
        s += "};\n\n"
        # Store result string
        self._resultString += s

    def addEffObject(self, effObject, label, effLabel):
        s = "// %s\n"%(label)
        s += "double eff_%s[] = {"%(effLabel)
        sUncertUp = "double effUncertUp_%s[] = {"%(effLabel)
        sUncertDown = "double effUncertDown_%s[] = {"%(effLabel)
        for i in range(1,effObject.GetPassedHistogram().GetNbinsX()+1): # Note that bin 0 is the underflow bin
            s += "%f"%effObject.GetEfficiency(i)
            sUncertUp += "%f"%effObject.GetEfficiencyErrorUp(i)
            sUncertDown += "%f"%effObject.GetEfficiencyErrorUp(i)
            if i != effObject.GetPassedHistogram().GetNbinsX():
                s += ", "
                sUncertUp += ", "
                sUncertDown += ", "
        s += "};"
        sUncertUp += "};"
        sUncertDown += "};"
        # Store result string
        self._resultString += s+"\n"
        self._resultString += sUncertUp+"\n"
        self._resultString += sUncertDown+"\n"
        self._resultString += "\n"

    def writeResultToDisk(self, myDir):
        myFilename = os.path.join(myDir, "btagEfficiencies.txt")
        f = open(myFilename, "w")
        f.write(self._resultString)
        f.close()
        print "Result for efficiency calculation:"
        print self._resultString
        print HighlightStyle()+"\nWritten btag efficiency result to %s%s"%(myFilename,NormalStyle())

def efficiencyplot(opts, dsetMgr, luminosity, myDir):
    myDirInRootFile = "BTaggingEfficiencyInMC"
    myAllJetsTemplate = "genuine%sJet%s"
    myBJetsTemplate = "genuine%sJetWithBTag%s"

    myPartonList = ["B","C","G","UDS","L"]
    mySuffixList = ["Pt","Eta"]

    # Specify output histogram binning
    myHistoSpecsPt = {
      "rangeMin": 0.0,
      "rangeMax": 500.0,
      # if an empty list is given, then uniform bin width is used:
      #"variableBinSizeLowEdges": [20,30,40,50,60,70,80,90,100,120,140,160,200,250,300,350,400], # B and C
      "variableBinSizeLowEdges": [20,30,60,100,150,250], # G and UDS
      "xtitle": "Jet p_{T} / GeV/c",
      "ytitle": "dN_{jets}/dp_{T}, arb. normalization"
    }
    myHistoSpecsEta = {
      "rangeMin": -2.5,
      "rangeMax": 2.5,
      "variableBinSizeLowEdges": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0], # if an empty list is given, then uniform bin width is used
      "xtitle": "Jet #eta",
      "ytitle": "dN_{jets}/d#eta, arb. normalization"
    }
    myHistoSpecsList = {"Pt": myHistoSpecsPt,
                        "Eta": myHistoSpecsEta }
    drawPlot = plots.PlotDrawer(log=True, ratio=False, addLuminosityText=False, optsLog={"ymin": 1e-4, "ymax": 300}, cmsText="CMS preliminary")
    drawPlotEfficiency = plots.PlotDrawer(log=False, ratio=False, addLuminosityText=False, cmsText="CMS preliminary", opts={"ymin": 0, "ymax": 1}, ylabel="Efficiency")

    # Loop over variables
    myResult = BtagEfficiencyResult()
    for suffix in mySuffixList:
        # Store binning to result
        myResult.addGeneralInfo(myDir.replace("btagEfficiency_",""))
        myResult.addBinning(suffix, myHistoSpecsList[suffix]["variableBinSizeLowEdges"])
        # Initialize lists for histograms.Histo objects
        hAllJetsList = []
        hBJetsList = []
        hEfficiencyList = []
        # Loop over partons
        for parton in myPartonList:
            print HighlightStyle()+"Creating plots for parton %s, variable %s%s"%(parton,suffix,NormalStyle())
            # Obtain histograms
            myAllJetsDsetHisto = dsetMgr.getDataset(opts.dset).getDatasetRootHisto("%s/%s"%(myDirInRootFile,myAllJetsTemplate%(parton,suffix)))
            myAllJetsDsetHisto.normalizeToLuminosity(luminosity)
            hAllJets = myAllJetsDsetHisto.getHistogram().Clone()
            myBJetsDsetHisto = dsetMgr.getDataset(opts.dset).getDatasetRootHisto("%s/%s"%(myDirInRootFile,myBJetsTemplate%(parton,suffix)))
            myBJetsDsetHisto.normalizeToLuminosity(luminosity)
            hBJets = myBJetsDsetHisto.getHistogram().Clone()
            # Setup histogramming
            myModifier = ShapeHistoModifier(myHistoSpecsList[suffix])
            # Make plot for all jets
            myPlotName = "%sForAll%sJets"%(suffix,parton)
            myLabel = "All %s jets"%(parton.replace("L","udsg").lower())
            hBinnedAllJets = myModifier.createEmptyShapeHistogram(myPlotName)
            myModifier.addShape(source=hAllJets,dest=hBinnedAllJets)
            myModifier.finaliseShape(dest=hBinnedAllJets)
            rootHistoObjectAll = histograms.Histo(hBinnedAllJets.Clone(),myLabel,legendStyle="LV",drawStyle="E")
            hAllJetsList.append(rootHistoObjectAll)
            plot = plots.PlotBase([rootHistoObjectAll])
            styles.dataStyle(plot.histoMgr.getHisto(myLabel))
            drawPlot(plot,"%s/%s"%(myDir,myPlotName),divideByBinWidth=True,xlabel=myHistoSpecsList[suffix]["xtitle"],ylabel=myHistoSpecsList[suffix]["ytitle"])
            plot.save()
            # Make plot for b jets
            myPlotName = "%sForBtagged%sJets"%(suffix,parton)
            myLabel = "All btagged %s jets"%(parton.replace("L","udsg").lower())
            hBinnedBJets = myModifier.createEmptyShapeHistogram(myPlotName)
            myModifier.addShape(source=hBJets,dest=hBinnedBJets)
            myModifier.finaliseShape(dest=hBinnedBJets)
            rootHistoObjectB = histograms.Histo(hBinnedBJets.Clone(),myLabel,legendStyle="LV",drawStyle="E")
            hBJetsList.append(rootHistoObjectB)
            plot = plots.PlotBase([rootHistoObjectB])
            styles.dataStyle(plot.histoMgr.getHisto(myLabel))
            drawPlot(plot,"%s/%s"%(myDir,myPlotName),divideByBinWidth=True,xlabel=myHistoSpecsList[suffix]["xtitle"],ylabel=myHistoSpecsList[suffix]["ytitle"])
            plot.save()
            # Make efficiency plot and convert it to TH1
            myEff = ROOT.TEfficiency(hBinnedBJets,hBinnedAllJets)
            myResult.addEffObject(myEff, myDir.replace("btagEfficiency_",""), "%stoB_by%s"%(parton.replace("L","UDSG"),suffix))
            myPlotName = "Efficiency_%sForBtagged%sJets"%(suffix,parton)
            myLabel = "%s#rightarrowb"%(parton.replace("L","udsg").lower())
            rootHistoObjectEff = histograms.HistoEfficiency(myEff,myLabel,legendStyle="LV",drawStyle="")
            hEfficiencyList.append(rootHistoObjectEff)
            plot = plots.PlotBase([rootHistoObjectEff])
            styles.dataStyle(plot.histoMgr.getHisto(myLabel))
            drawPlotEfficiency(plot,"%s/%s"%(myDir,myPlotName),xlabel=myHistoSpecsList[suffix]["xtitle"]) # opts={"log":False}
            plot.save()
        # Set plotting styles
        for i in range(0,len(hAllJetsList)):
            styles.applyStyle(hAllJetsList[i].getRootHisto(),i)
            styles.applyStyle(hBJetsList[i].getRootHisto(),i)
            styles.applyStyle(hEfficiencyList[i].getRootHisto(),i)
        # Do plots with different parton flavors on same canvas
        plot = plots.PlotBase(hAllJetsList)
        drawPlot(plot,"%s/%s"%(myDir,"Combined_%sForAllJets"%suffix),xlabel=myHistoSpecsList[suffix]["xtitle"],ylabel=myHistoSpecsList[suffix]["ytitle"])
        plot.save()
        plot = plots.PlotBase(hBJetsList)
        drawPlot(plot,"%s/%s"%(myDir,"Combined_%sForBTaggedJets"%suffix),xlabel=myHistoSpecsList[suffix]["xtitle"],ylabel=myHistoSpecsList[suffix]["ytitle"])
        plot.save()
        plot = plots.PlotBase(hEfficiencyList)
        drawPlotEfficiency(plot,"%s/%s"%(myDir,"Combined_Efficiency_%s"%suffix),xlabel=myHistoSpecsList[suffix]["xtitle"])
        plot.save()
    # Save to disk the efficiency results
    myResult.writeResultToDisk(myDir)

if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--dataset", dest="dset", help="Name of merged dataset (TTJets, WJets, ...)")
    parser.add_option("--mdir", dest="mdir", help="Path to multicrab directory")
    (opts, args) = parser.parse_args()

    if opts.dset == None:
        raise Exception(ErrorLabel()+"You forgot to specify which dataset you want to use! Add --dataset parameter (for example --dataset TTJets)")

    # Get dataset manager creator and handle different era/searchMode/optimizationMode combinations
    myPath = "."
    if opts.mdir != None:
        myPath = opts.mdir
    if not os.path.exists("%s/multicrab.cfg"%myPath):
        raise Exception(ErrorLabel()+"You forgot to provide the path to the multicrab directory with --mdir")
    signalDsetCreator = dataset.readFromMulticrabCfg(directory=myPath)
    myModuleSelector.setPrimarySource("Signal analysis", signalDsetCreator)
    myModuleSelector.doSelect(opts)

    # Arguments are ok, proceed to run
    myChosenModuleCount = len(myModuleSelector.getSelectedEras())*len(myModuleSelector.getSelectedSearchModes())*len(myModuleSelector.getSelectedOptimizationModes())
    print "Will run over %d modules (%d eras x %d searchModes x %d optimizationModes)"%(myChosenModuleCount,len(myModuleSelector.getSelectedEras()),len(myModuleSelector.getSelectedSearchModes()),len(myModuleSelector.getSelectedOptimizationModes()))
    myCount = 1
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                print "%sProcessing module %d/%d: era=%s searchMode=%s optimizationMode=%s%s"%(HighlightStyle(), myCount, myChosenModuleCount, era, searchMode, optimizationMode, NormalStyle())
                main(opts,signalDsetCreator,era,searchMode,optimizationMode)
                myCount += 1
    print "\n%sPlotting done.%s"%(HighlightStyle(),NormalStyle())
