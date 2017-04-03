#!/usr/bin/env python
'''
Description:
Generic scipt that plots most TH1 histograms produced by the
FakeBMeasurement.cc class. 

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotFakeBAnalysis.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotFakeBAnalysis.py -m FakeBMeasurement_170315_FullStats/ -v
./plotFakeBAnalysis.py -m FakeBMeasurement_170315_FullStats/ -i "JetHT|TT" s
./plotFakeBAnalysis.py -m FakeBMeasurement_170401_LE0Bjets/ --noError --format %.3f --latex --mergeEWK
./plotFakeBAnalysis.py -m FakeBMeasurement_170316_FullStats/ --mcOnly --intLumi 100000
./plotFakeBAnalysis.py -m FakeBMeasurement_170401_LE0Bjets/ --noError --format %.3f --precision 3 --mergeEWK
./plotFakeBAnalysis.py -m FakeBMeasurement_170401_LE0Bjets/ --noError --format %.3f --precision 3 --mergeEWK --latex

Examples (tables):
./plotFakeBAnalysis.py -m FakeBMeasurement_170316_FullStats --noError --format %.3f --latex
'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck

from old_InvertedTauID import *

#================================================================================================ 
# Function Definition
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def GetLumi(datasetsMgr):
    Verbose("Determininig Integrated Luminosity")                                                                                                                                                                                                                                   
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi


def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def main(opts):
    Verbose("main function")

    comparisonList = ["AfterStdSelections"]

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities() # from lumi.json
    if opts.verbose:
        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()

    # Check multicrab consistency
    # consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="CorrelationAnalysis")

    # Custom Filtering of datasets 
    # datasetsMgr.remove(filter(lambda name: "HplusTB" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "ST" in name, datasetsMgr.getAllDatasetNames()))
               
    # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
    plots.mergeRenameReorderForDataMC(datasetsMgr)
   
    # Get Integrated Luminosity
    if opts.mcOnly:
        # Determine integrated lumi
        if opts.intLumi < 0.0:
            opts.intLumi = GetLumi(datasetsMgr)
        else:
            pass
        # Remove data datasets
        datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))

    # Print dataset information
    datasetsMgr.PrintInfo()

    # Re-order datasets (different for inverted than default=baseline)
    newOrder = ["Data", "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
    if opts.mcOnly:
        newOrder.remove("Data")
    datasetsMgr.selectAndReorder(newOrder)

    # Set/Overwrite cross-sections                                                                                                                                                                                             
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

    # Merge EWK samples
    if opts.mergeEWK:
        datasetsMgr.merge("EWK", ["TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)


    #===============================
    # Do the plots
    #===============================
    # PurityTripletPlots(datasetsMgr, analysisType="")
    # PurityTripletPlots(datasetsMgr, analysisType="EWKFakeB")
    # PurityTripletPlots(datasetsMgr, analysisType="EWKGenuineB")

    #OtherHistograms(datasetsMgr, analysisType="Baseline")
    #OtherHistograms(datasetsMgr, analysisType="Inverted")

    # MtComparison(datasets)
    # MetComparisonBaselineVsInverted(datasets)
    # MetComparison(datasets)
    # TauPtComparison(datasets)

    #===============================
    # Do the counters
    #===============================
    doCounters(datasetsMgr)

    return


try:
    from QCDNormalizationFactors_AfterStdSelections_Run2015_80to1000 import *
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print



def normalisationInclusive():

    norm_inc = QCDPlusEWKFakeTausNormalization["Inclusive"]
    # normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]

    print "inclusive norm", norm_inc
    return norm_inc


def doCounters(datasetsMgr):
    '''
    '''
    Verbose("Doing the counters")

    # Definitions
    eventCounter = counter.EventCounter(datasetsMgr)
    ewkDatasets = ["TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]

    if opts.mcOnly and opts.intLumi>-1.0:
        eventCounter.normalizeMCToLuminosity(opts.intLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
        # eventCounter.normalizeMCByCrossSection()

    # Print the counters
    hLine    = "="*10
    msg = " Main counter (MC normalized by collision data luminosity) "
    print "\n" + hLine + msg + hLine

    # Construct the table
    mainTable = eventCounter.getMainCounterTable()

    # Only keep selected rows?
    rows = [
        #"ttree: skimCounterAll",
        #"ttree: skimCounterPassed",
        #"Base::AllEvents", 
        #"Base::PUReweighting",
        #"Base::Prescale", 
        #"Base::Weighted events with top pT",
        #"Base::Weighted events for exclusive samples",
        "All events",
        "Passed trigger",
        "passed METFilter selection ()",
        "Passed PV",
        "passed e selection (Veto)",
        "passed mu selection (Veto)",
        "Passed tau selection (Veto)",
        #"Passed tau selection and genuine (Veto)",
        "passed jet selection ()",
        #"passed b-jet selection ()",
        #"passed light-jet selection ()",
        "Baseline: passed b-jet selection",
        "Baseline: b tag SF",
        #"passed MET selection (Baseline)",
        "passed topology selection (Baseline)",
        "passed top selection (Baseline)",
        "Baseline: selected events",
        "Inverted: passed b-jet veto",
        "Inverted: b tag SF",
        #"passed MET selection (Inverted)",
        "passed topology selection (Inverted)",
        "passed top selection (Inverted)",
        "Inverted: selected events"
        ]
    mainTable.keepOnlyRows(rows)

    # Get number of rows/columns
    nRows    = mainTable.getNrows()
    nColumns = mainTable.getNcolumns()

    # Merge EWK into a new column?
    if not opts.mergeEWK:
        mainTable.insertColumn(nColumns, counter.sumColumn("EWK", [mainTable.getColumn(name=name) for name in ewkDatasets]))

    # Additional column (through inter-column operations)
    mainTable.insertColumn(mainTable.getNcolumns(), counter.subtractColumn("Data-EWK", mainTable.getColumn(name="Data"), mainTable.getColumn(name="EWK") ) )
    mainTable.insertColumn(mainTable.getNcolumns(), counter.divideColumn("QCD Purity", mainTable.getColumn(name="Data-EWK"), mainTable.getColumn(name="Data") ) )

    # Optional: Produce table in Text or LaTeX format?
    if opts.latex:
        cellFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat=opts.format, withPrecision=opts.precision))
    else:
        cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=opts.valueOnly, valueFormat=opts.format))
    print mainTable.format(cellFormat)

    # print eventCounter.getSubCounterTable("TauSelection").format(cellFormat)
    # print eventCounter.getSubCounterTable("e selection").format(cellFormat)
    # print eventCounter.getSubCounterTable("mu selection").format(cellFormat)
    # print eventCounter.getSubCounterTable("jet selection").format(cellFormat)
    # print eventCounter.getSubCounterTable("angular cuts / Collinear").format(cellFormat)
    # print eventCounter.getSubCounterTable("bjet selection").format(cellFormat)
    # print eventCounter.getSubCounterTable("angular cuts / BackToBack").format(cellFormat)                                                                                                                                
    return


def PurityTripletPlots(datasetsMgr, analysisType=""):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting the Purity-Triplets for %s" % analysisType)

    analysisTypes = ["", "EWKFakeB", "EWKGenuineB"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        folder = "FakeBPurity" + analysisType

    # Definitions
    histoNames  = []    
    histoKwargs = {}
    saveFormats = [".png", ".pdf"]

    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": -0.15}
    else:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": 0.1}

    _kwargs = {"xlabel": "",
               "ylabel": "",
               "rebinX": 1,
               "rebinY": None,
               "ratioYlabel": "Data/MC",
               "ratio": False, 
               "stackMCHistograms": True,
               "ratioInvert": False, 
               "addMCUncertainty": False, 
               "addLuminosityText": True,
               "addCmsText": True,
               "cmsExtraText": "Preliminary",
               "opts": {"ymin": 2e-1, "ymaxfactor": 10},
               "opts2": {"ymin": 0.0, "ymax": 2.0},
               "log": True,
               "errorBarsX": True, 
               "moveLegend": _moveLegend,
               "cutBox": {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               }

    # Create/Draw the plots
    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet p_{T} (GeV/c)"
    kwargs["ylabel"] = "Events / %.0f GeV/c"
    kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet #eta"
    kwargs["ylabel"] = "Events / %.2f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet b-tag discriminator"
    kwargs["ylabel"] = "Events / %.2f"
    kwargs["cutBox"] = {"cutValue": 0.5426, "fillColor": 16, "box": True, "line": True, "greaterThan": False}
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet pdgId"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet parton flavour"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet hadron flavour"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "ancestor bit"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections" % folder] = kwargs


    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = os.path.join(opts.saveDir, histoName.replace("/", "_"))

        if opts.mcOnly:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
            kwargs_.pop("ratio", None)
            kwargs_.pop("ratioYlabel", None)
            kwargs_.pop("ratioInvert", None)
            kwargs_.pop("opts2", None)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        else:
            p = plots.DataMCPlot(datasetsMgr, histoName)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

        # For-loop: All save formats
        for i, ext in enumerate(saveFormats):
            Print("%s" % saveName + ext, i==0)
            p.saveAs(saveName, formats=saveFormats)

    return


def OtherHistograms(datasetsMgr, analysisType=""):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting all other histograms for %s" % analysisType)

    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass

    # Definitions
    histoNames  = []
    histoKwargs = {}
    saveFormats = [".png", ".pdf"]

    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": -0.15}
    else:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": 0.1}

    _kwargs = {"rebinX": 1,
               "rebinY": None,
               "ratioYlabel": "Data/MC",
               "ratio": False, 
               "stackMCHistograms": True,
               "ratioInvert": False, 
               "addMCUncertainty": False, 
               "addLuminosityText": True,
               "addCmsText": True,
               "cmsExtraText": "Preliminary",
               "opts": {"ymin": 2e-1, "ymaxfactor": 10}, #1.2
               "opts2": {"ymin": 0.0, "ymax": 2.0},
               "log": True,
               "errorBarsX": True, 
               "moveLegend": _moveLegend,
               "cutBox": {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               }

    # Create/Draw the plots
    histoName = "%s_TopMassReco_LdgTrijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgTrijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgTrijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgTrijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgDijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgDijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgDijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgDijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs


    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = os.path.join(opts.saveDir, histoName.replace("/", "_"))

        if opts.mcOnly:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
            kwargs_.pop("ratio", None)
            kwargs_.pop("ratioYlabel", None)
            kwargs_.pop("ratioInvert", None)
            kwargs_.pop("opts2", None)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        else:
            p = plots.DataMCPlot(datasetsMgr, histoName)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

        # For-loop: All save formats
        for i, ext in enumerate(saveFormats):
            Print("%s" % saveName + ext, i==0)
            p.saveAs(saveName, formats=saveFormats)
    return
    
'''     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/jetPtAll"), "jetPtAll",
                    xlabel="Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
  
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/jetEtaAll"), "jetEtaAll",
                    xlabel="Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsFirstJetPt"), "selectedJetsFirstJetPt",
                    xlabel="First Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsFirstJetEta"), "selectedJetsFirstJetEta",
                    xlabel="First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsSecondJetPt"), "selectedJetsSecondJetPt",
                    xlabel="Second Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsSecondJetEta"), "selectedJetsSecondJetEta",
                    xlabel="First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsThirdJetPt"), "selectedJetsThirdJetPt",
                    xlabel="Third Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsThirdJetEta"), "selectedJetsThirdJetEta",
                    xlabel="Third Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
    plots.drawPlot(plots.DataMCPlot(datasets, "eSelection_VetoInvertedTau/electronPtPassed"), "electronPtPassed",
                    xlabel="Passed electron p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "eSelection_VetoInvertedTau/electronEtaPassed"), "electronEtaPassed",
                    xlabel="Passed electron #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "muSelection_VetoInvertedTau/IsolPtBefore"), "IsolPtBefore",
                    xlabel="Muon p_{T} (GeV/c) before isolation", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "muSelection_VetoInvertedTau/IsolEtaBefore"), "IsolEtaBefore",
                    xlabel="Muon #eta before isolation", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
         
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsFirstJetPt"), "selectedBJetsFirstJetPt",
                    xlabel="selected B Jets First Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsSecondJetPt"), "selectedBJetsSecondJetPt",
                    xlabel="selected B Jets Second Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsFirstJetEta"), "selectedBJetsFirstJetEta",
                    xlabel="selected B Jets First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsSecondJetEta"), "selectedBJetsSecondJetEta",
                    xlabel="selected B Jets Second Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
'''

'''
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterTau_realTau"), "TauPt_inv_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
     inverted = plots.DataMCPlot(datasets,"TauPt_inv_afterTau")
     invertedData = inverted.histoMgr.getHisto("Data").getRootHisto().Clone("TauPt_inv_afterTau")
     invertedRealTau = plots.DataMCPlot(datasets,"TauPt_inv_afterTau_realTau")
     invertedEWKRealTau = invertedRealTau.histoMgr.getHisto("EWK").getRootHisto().Clone("TauPt_inv_afterTau_realTau")
     dataMinusRealTau = invertedData.Clone()
     dataMinusRealTau.SetName("dataMinusRealTau")
     dataMinusRealTau.Add(invertedEWKRealTau,-1)
'''
     
     
'''
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterTau"), "TauPt_inv_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=10, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau"), "Met_inv_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=10, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau_realTau"), "Met_inv_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
'''

'''
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterJets_realTau"), "TauPt_inv_afterJets_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
                    
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_baseline_afterTau_realTau"), "TauPt_baseline_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
                    
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau_realTau"), "Met_inv_afterTau_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
                    
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterJets_realTau"), "Met_inv_afterJets_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterBtag_realTau"), "Met_inv_afterBtag_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
'''

'''
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_baseline_afterTau"), "TauPt_baseline_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_baseline_afterTau_realTau"), "TauPt_baseline_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterJets"), "TauPt_inv_afterJets",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=10, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)


 
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterBtag"), "TauPt_inv_afterBtag",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=10, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)



    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau"), "Met_inv_afterTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterJets"), "Met_inv_afterJets",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)



    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterBtag"), "Met_inv_afterBtag",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
  ####################################################################################        
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/MET/METInclusive"), "METInclusive_ForDataDrivenCrlPlots",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
    
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/BackToBackAngularCutsMinimum_AfterAllSelections/BackToBackAngularCutsMinimum_AfterAllSelectionsInclusive"), "BackToBackAngularCutsMinimum_AfterAllSelectionsInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 200, "ymaxfactor": 10}, log=True)
    
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/BackToBackAngularCutsMinimum/BackToBackAngularCutsMinimumInclusive"), "BackToBackAngularCutsMinimumInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 200, "ymaxfactor": 10}, log=True)

                 
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/MET_AfterAllSelections/MET_AfterAllSelectionsInclusive"), "MET_AfterAllSelectionsInclusive_ForDataDrivenCrlPlots",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
    
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/NBjets/NBjetsInclusive"), "NBjetsInclusive",
                    xlabel="N_{B jets}", ylabel="Number of events",
                    rebin=1, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 10, "ymaxfactor": 10}, log=True)

             
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/shapeTransverseMass/shapeTransverseMassInclusive"), "shapeTransverseMassInclusive",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10.0}, log=True)
     
  
         
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "METInvertedTauAfterStdSelectionsInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)   
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "METInvertedTauAfterStdSelectionsInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=15, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive"), "METBaselineTauAfterStdSelectionsInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKFakeTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "MetInvertedTauAfterStdSelectionsInclusiveFakeTaus",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKFakeTaus/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelectionsInclusiveFakeTaus",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelections",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=10, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKGenuineTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "MetInvertedTauAfterStdSelectionsInclusiveGenuineTaus",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKGenuineTaus/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelectionsInclusiveGenuineTaus",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
'''


                         
def getHistos(datasets, name1, name2, name3):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto(name1)
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto(name2)
     drh3 = datasets.getDataset("TTJets").getDatasetRootHisto(name3)
     drh1.setName("transverseMass")
     drh2.setName("transverseMassTriangleCut")
     drh3.setName("transverseMass3JetCut")
     return [drh1, drh2, drh3]


def MtComparison(datasets):
    mt = plots.PlotBase(getHistos(datasets,"ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKFakeTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKGenuineTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[3]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("transverseMass", st1)
    mt.histoMgr.forHisto("transverseMassTriangleCut", st2)
    mt.histoMgr.forHisto("transverseMass3JetCut", st3)

    mt.histoMgr.setHistoLegendLabelMany({
            "transverseMass": "All inverted Taus",
            "transverseMassTriangleCut": "Inverted Fake Taus",
            "transverseMass3JetCut": "Inverted Genuine Taus"
            })

    mt.appendPlotObject(histograms.PlotText(50, 1, "3-prong Taus", size=20))
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=10, log=True,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
    return


def MetComparisonBaselineVsInverted(datasets):
    mt = plots.PlotBase(getHistos2(datasets,"ForQCDNormalization/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", "ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("ForQCDNormalization/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", st1)
    mt.histoMgr.forHisto("ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive", st2)
 
    mt.histoMgr.setHistoLegendLabelMany({
            "NormalizationMETBaselineTauAfterStdSelectionsInclusive": "Baseline",
            "NormalizationMETInvertedTauAfterStdSelectionsInclusive": "Inverted",
             })

    mt.appendPlotObject(histograms.PlotText(50, 1, "1-prong Taus", size=20))
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MetComparisonBaselineVsInverted", xlabel=xlabel, ylabel=ylabel, rebinX=1, log=True,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
    return


def MtComparisonBaseline(datasets):
    mt = plots.PlotBase(getHistos(datasets,"ForQCDNormalization/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKFakeTaus/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKGenuineTaus/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[3]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("transverseMass", st1)
    mt.histoMgr.forHisto("transverseMassTriangleCut", st2)
    mt.histoMgr.forHisto("transverseMass3JetCut", st3)

    mt.histoMgr.setHistoLegendLabelMany({
            "transverseMass": "All baseline Taus",
            "transverseMassTriangleCut": "Baseline Fake Taus",
            "transverseMass3JetCut": "Baseline Genuine Taus"
            })
#    mt.histoMgr.setHistoDrawStyleAll("P")

    mt.appendPlotObject(histograms.PlotText(50, 1, "3-prong Taus", size=20))
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparisonBaseline", xlabel=xlabel, ylabel=ylabel, rebinX=1, log=True,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
    return


def getHistos2(datasets,name1, name2):
     drh1 = datasets.getDataset("Data").getDatasetRootHisto(name1)
     drh2 = datasets.getDataset("Data").getDatasetRootHisto(name2)

     drh1.setName("Baseline")
     drh2.setName("Inverted")
     return [drh1, drh2]


def MetComparison(datasets):
    mt = plots.ComparisonPlot(*getHistos2(datasets,"Met","Met"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())                                                                                                                                                                                  
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("Met_madgraph", st1)
    mt.histoMgr.forHisto("Met_pythia8", st2)
    mt.histoMgr.setHistoLegendLabelMany({
            "Met_madgraph": "Met from Madgraph",
            "Met_pythia8": "Met from Pythia8"
            })
    mt.histoMgr.setHistoDrawStyleAll("PE")


    mt.appendPlotObject(histograms.PlotText(100, 0.01, "tt events", size=20))
    xlabel = "PF E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MetComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=True,
                   createLegend={"x1": 0.6, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 50}, opts={"xmax": 500})


def getHistos3(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")

     drh1.setName("Taupt_madgraph")
     drh2.setName("Taupt_pythia8")
     return [drh1, drh2]


def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()


#    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    if addMCUncertainty:
        h.addMCUncertainty()
        
    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
##    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts2 = {"ymin": 0.0, "ymax": 2.0}
    _opts.update(opts)
    _opts2.update(opts2)

    #if log:
    #    name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    if log:
        h.getPad().SetLogy(log)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    common(h, xlabel, ylab, textFunction=textFunction)
    return


def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    '''
    Common formatting
    '''
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    h.save()
    return


#================================================================================================ 
# Main
#================================================================================================ 
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''
    
    # Default Settings
    ANALYSISNAME = "FakeBMeasurement"
    BATCHMODE    = True
    DATAERA      = "Run2016"
    FORMAT       = "%.3f"
    PRECISION    = 3
    INTLUMI      = -1.0
    LATEX        = False
    MCONLY       = False
    MERGEEWK     = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    SEARCHMODE   = "80to1000"
    VERBOSE      = False

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--mcOnly", dest="mcOnly", action="store_true", default=MCONLY,
                      help="Plot only MC info [default: %s]" % MCONLY)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--latex", dest="latex", action="store_true", default=LATEX,
                      help="The table formatting is in LaTeX instead of plain text (ready for generation)  [default: %s]" % (LATEX) )
    
    parser.add_option("--format", dest="format", default=FORMAT,
                      help="The table value-format of strings [default: %s]" % (FORMAT) )

    parser.add_option("--precision", dest="precision", type=int, default=PRECISION,
                      help="The table value-precision [default: %s]" % (PRECISION) )

    parser.add_option("--noError", dest="valueOnly", action="store_true", default=NOERROR,
                      help="Don't print statistical errors in tables [default: %s]" % (NOERROR) )


    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
