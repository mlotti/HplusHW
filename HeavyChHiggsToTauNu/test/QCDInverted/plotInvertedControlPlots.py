#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen, Lauri Wendland
#
######################################################################

import ROOT
import sys,os,shutil
#from optparse import OptionParser
from time import sleep
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gStyle.SetPalette(1)
from array import array
from math import fabs
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.FindFirstBinAbove import * 
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.bayes import * 
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.myArrays import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdInverted.QCDInvertedPlotting import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

from InvertedTauID import *

# Configuration
optionBrTopToHplusb = 0.01 # Br(t->bH+), needed only for plotting signal for light H+

era              = "Run2012ABCD"
searchMode       = "Light"
optimizationMode = "OptQCDTailKillerLoosePlus"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False

lastPtBin150 = False
lastPtBin120 = True

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

landsInput = "histogramsForLands.root"

histoSpecsMt = { "bins": 11,
    "rangeMin": 0.0,
    "rangeMax": 500.0,
    #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
    #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
    "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250], # if an empty list is given, then uniform bin width is used
    "xtitle": "Transverse mass / GeV",
    "ytitle": "N_{Events}" }
histoSpecsInvMass = { "bins": 15,
    "rangeMin": 0.0,
    "rangeMax": 500.0,
    #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
    #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
    "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,220,250,300,400], # if an empty list is given, then uniform bin width is used
    "xtitle": "Invariant mass / GeV",
    "ytitle": "N_{Events}" }
histoSpecsMet = { "bins": 13,
    "rangeMin": 0.0,
    "rangeMax": 500.0,
    #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
    "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
    #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250], # if an empty list is given, then uniform bin width is used
    "xtitle": "E_{T}^{miss} / GeV",
    "ytitle": "N_{Events}" }


# write histograms to file
def writeTransverseMass(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity, myNormFactors):
    mt = plots.DataMCPlot(datasets_lands, "transverseMass")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    f = ROOT.TFile.Open(landsInput, "RECREATE")
    mt_data = mt.histoMgr.getHisto("Data").getRootHisto().Clone("mt_data")
    mt_data.SetDirectory(f)
    mt_hw = mt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("mt_hw")
    mt_hw.SetDirectory(f)
#    mt_hh = mt.histoMgr.getHisto("TTToHplusBHminusB_M120").getRootHisto().Clone("mt_hh")
#    mt_hh.SetDirectory(f)
    f.Write()
    f.Close()


def doPlots(opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
    #The following fragment is not used
    #def createPlot(name, **kwargs):
        #if mcOnly:
            #return plots.MCPlot(datasets, name, normalizeToLumi=mcOnlyLumi, **kwargs)
        #else:
            #return plots.DataMCPlot(datasets, name, **kwargs)

    controlPlots(opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors)

    # Systematics plots
    mySystematics = QCDInvertedSystematics("METShape", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematics.doSystematicsForMetShapeDifference("MT","AfterCollinearCuts","shapeTransverseMass")
    mySystematics.doSystematicsPlots()
    mySystematicsTest1 = QCDInvertedSystematics("METShapeAndB2BDeltaPhi", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematicsTest1.doSystematicsForMetShapeDifference("MT","AfterCollinearCutsPlusBackToBackCuts","shapeTransverseMass")
    mySystematicsTest1.doSystematicsPlots()
    mySystematicsTest2 = QCDInvertedSystematics("METShapeAndBtag", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematicsTest2.doSystematicsForMetShapeDifference("MT","AfterCollinearCutsPlusBtag","shapeTransverseMass")
    mySystematicsTest2.doSystematicsPlots()
    mySystematicsTest3 = QCDInvertedSystematics("METShapeAndBtagAndB2BDeltaPhi", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematicsTest3.doSystematicsForMetShapeDifference("MT","AfterCollinearCutsPlusBtagPlusBackToBackCuts","shapeTransverseMass")
    mySystematicsTest3.doSystematicsPlots()
    mySystematicsTest4 = QCDInvertedSystematics("METShapeAfterMet", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematicsTest4.doSystematicsForMetShapeDifference("MT","AfterMet","shapeTransverseMass")
    mySystematicsTest4.doSystematicsPlots()
    mySystematicsTest5 = QCDInvertedSystematics("METShapeAfterMetAndB2B", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMt)
    mySystematicsTest5.doSystematicsForMetShapeDifference("MT","AfterMetPlusBackToBackCuts","shapeTransverseMass")
    mySystematicsTest5.doSystematicsPlots()
    mySystematicsTest6 = QCDInvertedSystematics("METShapeAsFunctionOfMet", opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecsMet)
    mySystematicsTest6.doSystematicsForMetShapeDifference("MET","AfterCollinearCuts","Inverted/METInvertedTauIdAfterBackToBackCuts")
    mySystematicsTest6.doSystematicsPlots()
    
    # For reference, make also systematics plots as function of MET
    #FIXME


def doCounters(opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
    def printSubCounterTable(eventCounter, subCounterName, cellFormat):
        # Check existence
        if subCounterName in eventCounter.getSubCounterNames():
            # Subcounter exists, go ahead and print it
            return eventCounter.getSubCounterTable(subCounterName).format(cellFormat)
        else:
            return "Subcounter '%s' does not exist (please note that for optimization runs subcounters are not saved)"%subCounterName

    eventCounter = counter.EventCounter(dsetMgr)
    eventCounter.normalizeMCToLuminosity(myLuminosity)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    myOutput = ""
    myOutput += mainTable.format(cellFormat) + "\n\n"
    myOutput += printSubCounterTable(eventCounter, "b-tagging", cellFormat) + "\n\n"
    myOutput += printSubCounterTable(eventCounter, "Jet selection", cellFormat) + "\n\n"
    myOutput += printSubCounterTable(eventCounter, "Jet main", cellFormat) + "\n\n"
    # Write the output to file
    f = open(os.path.join(myDir, "counterOutput.txt"), "w")
    f.write(myOutput)
    f.close()
    # Write the output to screen
    print myOutput



def controlPlots(opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
    print "Making control plots"
    # Initialize plotting class
    myQCDPlotter = QCDInvertedPlot(opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors)

    #### Transverse mass final plot
    myQCDPlotter.makeFinalPlot("shapeTransverseMass", "mT_final", histoSpecsMt, plotOptions={"addMCUncertainty": True, "ymin": -2, "ymax": 40, "xmin": 0, "xmax": 500})

    #### Transverse mass final plot
    myQCDPlotter.makeFinalPlot("Inverted/MTInvertedTauIdAfterCollinearCuts", "mT_after_collDphi", histoSpecsMt, plotOptions={"addMCUncertainty": True, "ymin": -2, "ymax": 40, "xmin": 0, "xmax": 500})
    myQCDPlotter.makeFinalPlot("Inverted/MTInvertedTauIdAfterMet", "mT_after_MET", histoSpecsMt, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/MTInvertedTauIdAfterBtag", "mT_after_btag", histoSpecsMt, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/MTInvertedTauIdAfterCollinearCutsPlusBveto", "mT_after_collDphi_and_bveto", histoSpecsMt, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/MTInvertedTauIdAfterCollinearCutsPlusBtag", "mT_after_collDphi_and_btag", histoSpecsMt, plotOptions={"addMCUncertainty": True})

    #### MET after jets final plot
    histoSpecsMet = { "bins": 50,
        "rangeMin": 0.0,
        "rangeMax": 500.0,
        "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
        #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250,300,400], # if an empty list is given, then uniform bin width is used
        #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200,250], # if an empty list is given, then uniform bin width is used
        "xtitle": "E_{T}^{miss} / GeV",
        "ytitle": "N_{Events}" }
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterJets", "MET_after_jets", histoSpecsMet, plotOptions={"addMCUncertainty": True})

    #### MET after delta phi collinear final plot
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterCollinearCuts", "MET_after_collDphi", histoSpecsMet, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterMetSF", "MET_after_METSF", histoSpecsMet, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterBackToBackCuts", "MET_after_backDphi", histoSpecsMet, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterCollinearCutsPlusBveto", "MET_after_collDphi_and_bveto", histoSpecsMet, plotOptions={"addMCUncertainty": True})
    myQCDPlotter.makeFinalPlot("Inverted/METInvertedTauIdAfterCollinearCutsPlusBtag", "MET_after_collDphi_and_btag", histoSpecsMet, plotOptions={"addMCUncertainty": True})

    #### Invariant Higgs mass final plot
    myQCDPlotter.makeFinalPlot("shapeInvariantMass", "invMass_final", histoSpecsInvMass, plotOptions={"ymax": 40, "addMCUncertainty": True})

    #### Njets (after tau ID + e/mu veto) final plot
    histoSpecsNJets = { "bins": 10,
        "rangeMin": 0.0,
        "rangeMax": 10.0,
        "xtitle": "N_{jets}",
        "ytitle": "N_{Events}" }
    myQCDPlotter.makeFinalPlot("ForDataDrivenCtrlPlots/Njets", "Njets_after_lepton_veto", histoSpecsNJets, plotOptions={"addMCUncertainty": True})

    #### Njets (after tau ID + e/mu veto + jet selection + MET SF) final plot
    myQCDPlotter.makeFinalPlot("ForDataDrivenCtrlPlots/NjetsAfterJetSelectionAndMETSF", "Njets_after_METSF", histoSpecsNJets, plotOptions={"addMCUncertainty": True})

    #### Njets after MET: histograms not available

    #### Nbjets (after MET) final plot
    histoSpecsNBJets = { "bins": 10,
        "rangeMin": 0.0,
        "rangeMax": 10.0,
        "xtitle": "N_{b jets}",
        "ytitle": "N_{Events}" }
    myQCDPlotter.makeFinalPlot("ForDataDrivenCtrlPlots/NBjets", "NBjets_after_MET", histoSpecsNBJets, plotOptions={"addMCUncertainty": True})

    #### Delta phi (tail killers) final plots
    for i in range(1,4):
        histoSpecsDeltaPhi = { "bins": 13,
            "rangeMin": 0.0,
            "rangeMax": 260.0,
            "xtitle": "#sqrt{#Delta#phi(180^{o}-#tau,E_{T}^{miss.})^{2}+(#Delta#phi(jet_{%d},E_{T}^{miss.})^{2}}, ^{o}"%i,
            "ytitle": "N_{Events}" }
        myQCDPlotter.makeFinalPlot("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet%dCollinear"%i, "DeltaPhiCollinearJet%d"%i, histoSpecsDeltaPhi, plotOptions={"addMCUncertainty": True})
        histoSpecsDeltaPhi = { "bins": 13,
            "rangeMin": 0.0,
            "rangeMax": 260.0,
            "xtitle": "#sqrt{#Delta#phi(#tau,E_{T}^{miss.})^{2}+(180^{o}-#Delta#phi(jet_{%d},E_{T}^{miss.})^{2}}, ^{o}"%i,
            "ytitle": "N_{Events}" }
        myQCDPlotter.makeFinalPlot("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet%dBackToBack"%i, "DeltaPhiBackToBackJet%d"%i, histoSpecsDeltaPhi, plotOptions={"addMCUncertainty": True})


    # Add here more plots, if desired



#def scaleMC(histo, scale):
    #if histo.isMC():
        #th1 = histo.getRootHisto()
        #th1.Scale(scale)

#def scaleMCHistos(h, scale):
    #h.histoMgr.forEachHisto(lambda histo: scaleMC(histo, scale))

#def scaleMCfromWmunu(h):
    ## Data/MC scale factor from AN 2011/053
##    scaleMCHistos(h, 1.736)
    #scaleMCHistos(h, 1.0)

#def replaceQCDfromData(plot, datasetsQCD, path):
##    normalization = 0.00606 * 0.86
    #normalization = 0.025
    #drh = datasetsQCD.getDatasetRootHistos(path)
    #if len(drh) != 1:
        #raise Exception("There should only one DatasetRootHisto, got %d", len(drh))
    #histo = histograms.HistoWithDatasetFakeMC(drh[0].getDataset(), drh[0].getHistogram(), drh[0].getName())
    #histo.getRootHisto().Scale(normalization)
    #plot.histoMgr.replaceHisto("QCD", histo)
    #return plot

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
#def flipName(name):
    #tmp = name.split("_")
    #return tmp[-1] + "_" + tmp[-2]

# Common drawing function
#def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    #if cutLine != None and cutBox != None:
        #raise Exception("Both cutLine and cutBox were given, only either one can exist")

    #if rebin > 1:
        #h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    #ylab = ylabel
    #if "%" in ylabel:
        #ylab = ylabel % h.binWidth()


    #scaleMCfromWmunu(h)     
##    h.stackMCSignalHistograms()

    #h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
##    h.stackMCHistograms()
    
    #if addMCUncertainty:
        #h.addMCUncertainty()
        
    #_opts = {"ymin": 0.01, "ymaxfactor": 2}
    #if not log:
        #_opts["ymin"] = 0
        #_opts["ymaxfactor"] = 1.1
###    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    #_opts2 = {"ymin": 0.0, "ymax": 2.0}
    #_opts.update(opts)
    #_opts2.update(opts2)

    ##if log:
    ##    name = name + "_log"
    #h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    #if log:
        #h.getPad().SetLogy(log)
    #h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    ## Add cut line and/or box
    #if cutLine != None:
        #lst = cutLine
        #if not isinstance(lst, list):
            #lst = [lst]

        #for line in lst:
            #h.addCutBoxAndLine(line, box=False, line=True)
    #if cutBox != None:
        #lst = cutBox
        #if not isinstance(lst, list):
            #lst = [lst]

        #for box in lst:
            #h.addCutBoxAndLine(**box)

    #common(h, xlabel, ylab, textFunction=textFunction)

## Common formatting
#def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    #h.frame.GetXaxis().SetTitle(xlabel)
    #h.frame.GetYaxis().SetTitle(ylabel)
    #h.draw()
    #histograms.addCmsPreliminaryText()
    #histograms.addEnergyText()
    #if addLuminosityText:
        #h.addLuminosityText()
    #if textFunction != None:
        #textFunction()
    #h.save()

#class AddMassBRText:
    #def __init__(self):
        #self.mass = 120
        #self.br = 0.01
        #self.size = 20
        #self.separation = 0.04

    #def setMass(self, mass):
        #self.mass = mass

    #def setBR(self, br):
        #self.br = br

    #def __call__(self, x, y):
        #mass = "m_{H^{#pm}} = %d GeV/c^{2}" % self.mass
        #br = "BR(t #rightarrow bH^{#pm})=%.2f" % self.br

        #histograms.addText(x, y, mass, size=self.size)
        #histograms.addText(x, y-self.separation, br, size=self.size)

#addMassBRText = AddMassBRText()

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir>"
    print
    sys.exit()
                    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":


    if len(sys.argv) < 2:
        usage()
    myMulticrabDir = sys.argv[1]
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    myNormalizationFactorSource = "QCDInvertedNormalizationFactors"

    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes

#    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=True,conflict_handler="resolve")
#    myModuleSelector.addParserOptions(parser)
#    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")
#    # Add here parser options, if necessary, following line is an example
#    #parser.add_option("--showcard", dest="showDatacard", action="store_true", default=False, help="Print datacards also to screen")
#
#    # Parse options
#    (opts, args) = parser.parse_args()
#
#    # Obtain multicrab directory
#    myMulticrabDir = "."
#    if opts.multicrabDir != None:
#        myMulticrabDir = opts.multicrabDir
    if not os.path.exists(myMulticrabDir+"/multicrab.cfg"):
        print "\n"+ErrorLabel()+"Cannot find multicrab.cfg!"# Did you use the --mdir parameter?\n"
        usage()
#        parser.print_help()
#        sys.exit()

    # Obtain normalisation coefficients
    myNormFactors = None
    if os.path.exists(myNormalizationFactorSource+".py"):
        from QCDInvertedNormalizationFactors import *
        QCDInvertedNormalizationSafetyCheck(era)
        myNormFactors = QCDInvertedNormalization.copy()
    else:
        raise Exception(ErrorLabel()+"Normalisation factors ('%s.py') not found!\nRun script InvertedTauID_Normalization.py to generate the normalization factors."%myNormalizationFactorSource)
    

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myMulticrabDir)
#    myModuleSelector.setPrimarySource("analysis", dsetMgrCreator)
#    # Select modules
#    myModuleSelector.doSelect(opts)

    myDisplayStatus = True
    # Loop over era/searchMode/optimizationMode options
#    for era in myModuleSelector.getSelectedEras():
#        for searchMode in myModuleSelector.getSelectedSearchModes():
#            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                # Check if normalisation factors are compatible with the requested module
#                if era != myNormFactors["era"]:
#                    raise Exception(ErrorLabel()+"You requested to do analysis with era='%s', but the normalization factors have been calculated for the era '%s'!\nRecalculate norm. factors with InvertedTauID_Normalization.py or change requested era with -e!"%(era,myNormFactors["era"]))
#                if searchMode != myNormFactors["searchMode"]:
#                    raise Exception(ErrorLabel()+"You requested to do analysis with searchMode='%s', but the normalization factors have been calculated for the searchMode '%s'!\nRecalculate norm. factors with InvertedTauID_Normalization.py or change requested searchMode with -m!"%(searchMode,myNormFactors["searchMode"]))
#                if "Jet" in optimizationMode or "Jet" in myNormFactors["optimizationMode"]:
#                    print WarningLabel()+"You ask for the variation '%s', which varies the JetSelection properties."%optimizationMode
#                    print WarningLabel()+"The normalization factors were calculated for the variation '%s'."%myNormFactors["optimizationMode"]
#                    print WarningLabel()+"Please check if they are compatible with each other! (you may need to calculate new normalization factors for the results to make sense)"
                    # Add a small delay to give a chance for the user to see the warning message
#                    for i in range(0,5):
#                        sys.stdout.write("\rContinuing in %d seconds ..."%(5-i))
#                        sys.stdout.flush()
#                        sleep(1)
#                    print
    # Construct info string of module
    myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)
    print HighlightStyle()+"Module:",myModuleInfoString,NormalStyle()
    # Obtain dataset manager
    dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    # Do the usual normalisation
    dsetMgr.updateNAllEventsToPUWeighted()
    dsetMgr.loadLuminosities()
    plots.mergeRenameReorderForDataMC(dsetMgr)
    dsetMgr.merge("EWK", [
                  "TTJets",
                  "WJets",
                  "DYJetsToLL",
                  "SingleTop",
                  "Diboson"
                  ],keepSources=True) # Keep sources needed to keep open TTJets
    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(dsetMgr, br_tH=optionBrTopToHplusb, br_Htaunu=1)
    # Set the signal cross sections to a value from MSSM
    # xsect.setHplusCrossSectionsToMSSM(dsetMgr, tanbeta=20, mu=200)
    plots.mergeWHandHH(dsetMgr) # merging of WH and HH signals must be done after setting the cross section

    # Make a directory for output
    myDir = "invertedControlPlots_%s"%myModuleInfoString
    # Remove the directory with its contents if it exists
    if os.path.exists(myDir):
        shutil.rmtree(myDir)
    os.mkdir(myDir)
    # Obtain luminosity
    myLuminosity = dsetMgr.getDataset("Data").getLuminosity()
    # Print info so that user can check that merge went correct
    if myDisplayStatus:
        dsetMgr.printDatasetTree()
        print "Luminosity = %f 1/fb"%(myLuminosity / 1000.0)
        print
        myDisplayStatus = False
    # Call methods for module
    # Create plots
    opts={}
    doPlots(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity, myNormFactors)

    # Print counters
    #doCounters(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity, myNormFactors)

    # Write mt histograms to ROOT file
    #writeTransverseMass(opts, dsetMgr, myModuleInfoString, myDir, myLuminosity, myNormFactors)

