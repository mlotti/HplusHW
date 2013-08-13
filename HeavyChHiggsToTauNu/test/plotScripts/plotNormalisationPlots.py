#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
# Adapted from original for signal analysis debugging and validation
# by Lauri Wendland
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

from optparse import OptionParser
import os
import shutil

# Configuration
removeQCD = False

optionBr = 0.01

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

# main function
def main(opts,signalDsetCreator,era,searchMode,optimizationMode):
    # Make directory for output
    mySuffix = "normalisationPlots_%s_%s_%s"%(era,searchMode,optimizationMode)
    if os.path.exists(mySuffix):
        if os.path.exists("%s_old"%mySuffix):
            shutil.rmtree("%s_old"%mySuffix)
        os.rename(mySuffix, "%s_old"%mySuffix)
    os.mkdir(mySuffix)
    # Create dataset manager
    myDsetMgr = signalDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    if mcOnly:
        myDsetMgr.remove(myDsetMgr.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        myDsetMgr.loadLuminosities()
    myDsetMgr.updateNAllEventsToPUWeighted()

    # Take QCD from data
    if opts.noMCQCD:
        myDsetMgr.remove(filter(lambda name: "QCD" in name, myDsetMgr.getAllDatasetNames()))
    # Remove signal
    if opts.noSignal:
        myDsetMgr.remove(filter(lambda name: "TTToHplus" in name, myDsetMgr.getAllDatasetNames()))
        myDsetMgr.remove(filter(lambda name: "Hplus_taunu" in name, myDsetMgr.getAllDatasetNames()))
        myDsetMgr.remove(filter(lambda name: "HplusTB" in name, myDsetMgr.getAllDatasetNames()))

    plots.mergeRenameReorderForDataMC(myDsetMgr)

    if mcOnly:
        print "Int.Lumi (manually set)",mcOnlyLumi
    else:
        print "Int.Lumi",myDsetMgr.getDataset("Data").getLuminosity()
    if not opts.noSignal:
        print "norm=",myDsetMgr.getDataset("TTToHplusBWB_M120").getNormFactor()

    myDsetMgr.remove(filter(lambda name: "QCD_Pt20_MuEnriched" in name, myDsetMgr.getAllDatasetNames()))
    # Remove signals other than M120
    myDsetMgr.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, myDsetMgr.getAllDatasetNames()))
    myDsetMgr.remove(filter(lambda name: "Hplus_taunu" in name, myDsetMgr.getAllDatasetNames()))
    myDsetMgr.remove(filter(lambda name: "HplusTB" in name, myDsetMgr.getAllDatasetNames()))
    
    histograms.createLegend.moveDefaults(dx=-0.05)
    histograms.createSignalText.set(xmin=0.4, ymax=0.93, mass=120)
    
    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(myDsetMgr, br_tH=optionBr, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(myDsetMgr, tanbeta=20, mu=200)

    plots.mergeWHandHH(myDsetMgr) # merging of WH and HH signals must be done after setting the cross section
    
    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    #plots.replaceLightHplusWithSignalPlusBackground(myDsetMgr)
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(myDsetMgr, opts, mySuffix)

    # Print counters
    #doCounters(myDsetMgr)
    print "Results saved in directory: %s"%mySuffix

def doPlots(myDsetMgr, opts, mySuffix):
    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    drawPlot = plots.PlotDrawer(ylabel="N_{events}", log=True, ratio=True, ratioYlabel="Data/MC", opts2={"ymin": 0, "ymax": 2}, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True)

    global plotIndex
    plotIndex = 1
    def createDrawPlot(name, moveSignalText={}, fullyBlinded=False, addBlindedText=True, moveBlindedText={}, **kwargs):
        # Create the plot object
        print "Creating plot:",name
        args = {}
        if mcOnly:
            args["normalizeToLumi"] = mcOnlyLumi
        p = plots.DataMCPlot(myDsetMgr, name, **args)

        # Remove data if fully blinded
        if not mcOnly and fullyBlinded and p.histoMgr.hasHisto("Data"):
            p.histoMgr.removeHisto("Data")
            if addBlindedText:
                tb = histograms.PlotTextBox(xmin=0.4, ymin=None, xmax=0.6, ymax=0.84, size=17)
                tb.addText("Data blinded")
                tb.move(**moveBlindedText)
                p.appendPlotObject(tb)

        # Add the signal information text box
        if not opts.noSignal:
            st = histograms.createSignalText()
            st.move(**moveSignalText)
            p.appendPlotObject(st)

        # Set the file name
        global plotIndex
        filename = "%s/%03d_%s"%(mySuffix, plotIndex, name.replace("/", "_"))
        plotIndex += 1

        # Draw the plot
        drawPlot(p, filename, **kwargs)

    # common arguments for plots which make sense only for MC
    mcArgs = {"fullyBlinded": True, "addBlindedText": False}

    # Common plots
    myCommonPlotDirs = ["VertexSelection","TauSelection","TauWeight","ElectronVeto","MuonVeto","JetSelection","MET","BTagging","Selected","FakeTaus_BTagging","FakeTaus_Selected"]
    def createDrawCommonPlot(path, **kwargs):
        for plotDir in myCommonPlotDirs:
            args = {}
            args.update(kwargs)
            if "transverseMass" in path:
                if "BTagging" in plotDir or "Selected" in plotDir:
                    args["customizeBeforeFrame"] = lambda p: plots.partiallyBlind(p, maxShownValue=60)
            elif "Selected" in plotDir:
                args["fullyBlinded"] = True
            if "FakeTaus" in plotDir:
                args.update(mcArgs)
            createDrawPlot(path%plotDir, **args)

    #phiBinWidth = 2*3.14159/72
    phiBinWidth = 2*3.14159/36

    myDirs = ["NormalisationAnalysis/DYEnrichedWithGenuineTaus",
              "NormalisationAnalysis/DYEnrichedWithFakeTaus",
              "NormalisationAnalysis/WJetsEnrichedWithGenuineTaus",
              "NormalisationAnalysis/WJetsEnrichedWithFakeTaus",
              "NormalisationAnalysis/TTJetsEnrichedWithGenuineTaus",
              "NormalisationAnalysis/TTJetsEnrichedWithFakeTaus"]
    for myDir in myDirs:
        createDrawPlot(myDir+"/tauPt", xlabel="#tau p_{T}, GeV/c")
        createDrawPlot(myDir+"/nJets", xlabel="N_{jets}")
        createDrawPlot(myDir+"/met", xlabel="E_{T}^{miss}, GeV")
        createDrawPlot(myDir+"/metPhi", xlabel="E_{T}^{miss} #phi, GeV")
        createDrawPlot(myDir+"/nBJets", xlabel="N_{b jets}")
        createDrawPlot(myDir+"/transverseMass", xlabel="m_T(#tau,E_{T}^{miss}), GeV/c^{2}")
        createDrawPlot(myDir+"/zMass", xlabel="m_Z(#ell#ell), GeV/c^{2}")
        createDrawPlot(myDir+"/fakeTauTauPt", xlabel="#tau p_{T}, GeV/c")
        createDrawPlot(myDir+"/fakeTauNJets", xlabel="N_{jets}")
        createDrawPlot(myDir+"/fakeTauMet", xlabel="E_{T}^{miss}, GeV")
        createDrawPlot(myDir+"/fakeTauMetPhi", xlabel="E_{T}^{miss} #phi, GeV")
        createDrawPlot(myDir+"/fakeTauNBJets", xlabel="N_{b jets}")
        createDrawPlot(myDir+"/fakeTauTransverseMass", xlabel="m_T(#tau,E_{T}^{miss}), GeV/c^{2}")
        createDrawPlot(myDir+"/fakeTauZMass", xlabel="m_Z(#ell#ell), GeV/c^{2}")


def doCounters(myDsetMgr, mySuffix):
    eventCounter = counter.EventCounter(myDsetMgr)

    # append row from the tree to the main counter
#    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    ewkDatasets = [
        "WJets", "W1Jets", "W2Jets", "W3Jets", "W4Jets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print mySuffix
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default
#    cellFormat = counter.TableFormatText()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=False))
    print mainTable.format(cellFormat)




#    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
    print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("TauIDPassedJets::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    
    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MuonSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat) 
    print eventCounter.getSubCounterTable("ElectronSelection").format(cellFormat)  
#    print eventCounter.getSubCounterTable("top").format(cellFormat) 

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("--noMCQCD", dest="noMCQCD", action="store_true", default=False, help="remove MC QCD")
    parser.add_option("--noSignal", dest="noSignal", action="store_true", default=False, help="remove MC QCD")
    parser.add_option("--mdir", dest="multicrabDir", help="path to multicrab directory")
    (opts, args) = parser.parse_args()

    # Get dataset manager creator and handle different era/searchMode/optimizationMode combinations
    myPath = "."
    if opts.multicrabDir != None:
        myPath = opts.multicrabDir
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
