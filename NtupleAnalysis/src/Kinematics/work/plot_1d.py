#!/usr/bin/env python
'''
Description:
Generate all TH1 generated from the Kinematics analyzer (GEN-level info).

Usage:
./plot_1d.py -m <pseudo_mcrab> [opts]

Examples:
./plot_1d.py -m <peudo_mcrab> -o "" --url --normaliseToOne
./plot_1d.py -m Kinematics_170828_082301/ -i 'TT' --url --normaliseToOne
./plot_1d.py -m Kinematics_170828_082301/ -e "QCD_b|M_180|M_200|M_220|M_250|M_300|M_350|M_400|M_500|M_1000|M_2000" --url --mergeEWK
./plot_1d.py -m Kinematics_170828_082301/ -e "QCD_b|M_180|M_200|M_220|M_250|M_350|M_400|M_1000|M_2000|M_3000" --mergeEWK --url
./plot_1d.py -m Kinematics_170828_082301/ -e "QCD_b|M_180|M_200|M_220|M_250|M_350|M_400|M_1000|M_2000|M_3000" --url --mergeEWK --normaliseToOne

Last Used:
./plot_1d.py -m Kinematics_FullStats_170831_085353 -e "QCD_b|M_180|M_200|M_220|M_250|M_350|M_400|M_1000|M_2000|M_3000" --url --mergeEWK --normaliseToOne  
./plot_1d.py -m Kinematics_170830_060219 -e "QCD_b|M_180|M_200|M_220|M_250|M_350|M_400|M_1000|M_2000|M_3000" --url --mergeEWK --normaliseToOne

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
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
    aux.Print(msg, printHeader)
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


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def main(opts, signalMass):

    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Determine integrated Lumi before removing data
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 5747.588 + 2573.399 + 4248.384 + 4008.663 + 2704.118 + 405.222 + 7539.457 + 8390.5 + 215.149

        # Remove datasets
        if 0:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "SingleTop" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "DYJetsToQQHT" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TTZToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "WJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "Diboson" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TTTT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "FakeBMeasurementTrijetMass" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "M_" in name and "M_" + str(opts.signalMass) not in name, datasetsMgr.getAllDatasetNames()))

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()


        # Re-order datasets (different for inverted than default=baseline)
        newOrder = []
        if opts.mergeEWK:
            newOrder = ["EWK", "QCD"]
        else:
            newOrder.extend(GetListOfEwkDatasets())
            newOrder.append("QCD")
        for d in datasetsMgr.getAllDatasetNames():
            if "ChargedHiggs" in d:
                newOrder.extend([d])        
        datasetsMgr.selectAndReorder( reversed(newOrder) )


        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
        style.setGridY(False)

        # Do the topSelection histos
        folder     = opts.folder
        histoPaths = []
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        hList      = [x for x in histoList if "_Vs_" not in x] # remove TH2
        histoPaths = [os.path.join(folder, h) for h in hList]
        skipMe     = ["counters", "Weighting", "config", "configInfo"]
        for h in histoPaths:
            if h in skipMe:
                continue
            PlotMC(datasetsMgr, h, intLumi)
    return


def GetHistoKwargs(histo, opts):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    if opts.normaliseToOne:
        yLabel = "Arbitrary Units"
    else:
        yLabel = "Events"
    logY       = False
    yMaxFactor = 1.2

    # Create with default values
    kwargs = {
        "xlabel"           : "x-label",
        "ylabel"           : yLabel,
        "rebinX"           : 1,
        "rebinY"           : 1,
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True, 
        "stackMCHistograms": True,
        "ratioInvert"      : False, 
        "addMCUncertainty" : False, 
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": yMaxFactor},
        "opts2"            : {"ymin": 0.0, "ymax": 2.0},
        "log"              : logY,
        "moveLegend"       : {"dx": -0.1, "dy": 0.0, "dh": -0.1},
        "cutBox"           : {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        }

    if "eta" in histo.lower(): 
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#eta"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}#, "ymin": 1e+0, "ymaxfactor": 10}

    if "deta" in histo.lower(): 
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}

    if "met_et" in histo.lower():
        units            = "GeV/c"
        format           = "%0.0f " + units
        kwargs["xlabel"] = "E_{T}^{miss} (%s)" % units
        kwargs["ylabel"] = yLabel + "/ %s " % format
        print kwargs["ylabel"]
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 300.0}
        kwargs["log"]    = True
        
    if "ht" in histo.lower():
        units            = "GeV"
        format           = "%0.0f " + units
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "H_{T} (%s)"  % units
        kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["rebinX"] = 1
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 2000, "ymin": 1e+0, "ymaxfactor": 10}
        ROOT.gStyle.SetNdivisions(5, "X")

    if "MHT" in histo:
        units            = "GeV"
        format           = "%0.0f " + units
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "MHT (%s)"  % units
        kwargs["rebinX"] = 1
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 300, "ymin": 1e+0, "ymaxfactor": 10}
        ROOT.gStyle.SetNdivisions(5, "X")

    if "jt" in histo.lower():
        units            = "GeV"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "J_{T} (%s)"  % units
        kwargs["rebinX"] = 1
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 1500, "ymin": 1e+0, "ymaxfactor": 10}
        ROOT.gStyle.SetNdivisions(5, "X")

    if "alphat" in histo.lower():
        units            = ""
        kwargs["xlabel"] = "#alpha_{T}"
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 1.0, "ymin": 1e-5, "ymaxfactor": 10}
        kwargs["log"]    = True

    if "y23" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "y_{23}"

    if "sphericity" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "Sphericity"

    if "planarity" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "Planarity"

    if "aplanarity" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "Aplanarity"

    if "centrality" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "Centrality"
        kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}

    if "circularity" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "Circularity"

    if "h2" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "H_{2}"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 1.01}
        kwargs["cutBox"] = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "cparameter" in histo.lower():
        kwargs["ylabel"]      = yLabel + " / %.2f"
        kwargs["xlabel"]     = "C"
        kwargs["opts"]       = {"xmin": 0.0, "xmax": 1.01}
        kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}

    if "dparameter" in histo.lower():
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["xlabel"] = "D"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 1.01}
        ROOT.gStyle.SetNdivisions(10, "X")

    if  histo == "Y":
        units            = ""
        kwargs["xlabel"] = "Y"
        kwargs["ylabel"] = yLabel + " / %.1f"

    if "_Pt" in histo:
        kwargs["rebinX"] = 1
        units            = "GeV/c"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "p_{T} (%s)"  % units
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "GenJet1" in histo:
            kwargs["xlabel"] = "jet_{1} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 1000, "ymin": 1e+0, "ymaxfactor": 10}
        if "GenJet2" in histo:
            kwargs["xlabel"] = "jet_{2} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 600, "ymin": 1e+0, "ymaxfactor": 10}
        if "GenJet3" in histo:
            kwargs["xlabel"] = "jet_{3} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 400, "ymin": 1e+0, "ymaxfactor": 10}
        if "GenJet4" in histo:
            kwargs["xlabel"] = "jet_{4} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 300, "ymin": 1e+0, "ymaxfactor": 10}
        if "GenJet5" in histo:
            kwargs["xlabel"] = "jet_{5} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 200, "ymin": 1e+0, "ymaxfactor": 10}
        if "GenJet6" in histo:
            kwargs["xlabel"] = "jet_{6} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 150, "ymin": 1e+0, "ymaxfactor": 10}
        if "BQuark1" in histo:
            kwargs["xlabel"] = "b_{1} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 600, "ymin": 1e+0, "ymaxfactor": 10}
        if "BQuark2" in histo:
            kwargs["xlabel"] = "b_{2} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 300, "ymin": 1e+0, "ymaxfactor": 10}
        if "BQuark3" in histo:
            kwargs["xlabel"] = "b_{3} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 200, "ymin": 1e+0, "ymaxfactor": 10}
        if "BQuark4" in histo:
            kwargs["xlabel"] = "b_{4} p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 100, "ymin": 1e+0, "ymaxfactor": 10}
        if "MaxPt" in histo:
            kwargs["log"]    = True
            kwargs["opts"]   = {"xmin": 0, "xmax": 1000}#, "ymin": 1e+0, "ymaxfactor": 10}
        if "MaxMass" in histo:
            kwargs["log"]    = True
            ROOT.gStyle.SetNdivisions(5, "X")
            kwargs["opts"]   = {"xmin": 0, "xmax": 1000}
        if "BQuarkPair_dRMin" in histo:
            kwargs["opts"]   = {"xmin": 0, "xmax": 500}#, "ymin": 1e+0, "ymaxfactor": 10}
        if "MaxDiJetMass" in histo:
            kwargs["rebinX"] = 2
            kwargs["opts"]   = {"xmin": 0, "xmax": 600}#, "ymin": 1e+0, "ymaxfactor": 10}
        if "MaxTriJetPt" in histo:
            units            = "GeV/c"
            kwargs["ylabel"] = yLabel + " / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0}
        if "dRMinDiJet_NoBJets" in histo:
            units            = "GeV/c"
            kwargs["ylabel"] = yLabel + " / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0, "xmax": 800, "ymin": 1e+0, "ymaxfactor": 10}
        if "BQuarkPair_dR" in histo:
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

#    if "eta" in histo.lower(): 
#        kwargs["ylabel"] = yLabel + " / %.1f"
#        kwargs["xlabel"] = "#eta"
#        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
#        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}#, "ymin": 1e+0, "ymaxfactor": 10}
#
#        if "dEta" in histo:
#            #kwargs["ylabel"] = yLabel + " / %.2f"
#            kwargs["xlabel"] = "#Delta#eta"
#            kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}
                
    if "MaxMass_Eta" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#eta"
        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}#, "ymin": 1e+0, "ymaxfactor": 10}

    if "MaxDiJetMass_Eta" in histo:
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}

    if "MaxDiJetMass_dEta" in histo:
        kwargs["rebinX"]     = 2
        kwargs["xlabel"]     = "#Delta#eta"
        kwargs["opts"]      = {"xmin": 0.0, "xmax": +5.0}
        kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}

    if "MaxTriJetPt_dEtaMin" == histo:
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.5}
        
    if "dRMinDiJet_NoBJets_Eta" in histo:
        kwargs["opts"]   = {"xmin": -3.0, "xmax": +3.0}
            
    if "phi" in histo.lower():
        units            = "rads"
        kwargs["xlabel"] = "#phi (%s)" % units
        kwargs["ylabel"] = yLabel + "/ %.1f " + units

        if "dPhi" in histo:
            kwargs["xlabel"] = "#Delta#phi (%s)" % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}
        
        if "BQuarkPair_dRMin" in histo:
            kwargs["opts"]   = {"xmin": -3.2, "xmax": +3.2}

        if "MET" in histo:
            kwargs["opts"]   = {"xmin": -3.2, "xmax": +3.2}

        if "MaxMass_Phi" in histo:
            kwargs["opts"]   = {"xmin": -3.2, "xmax": +3.2}

        if "MaxPt_Phi" in histo:
            kwargs["opts"]   = {"xmin": -3.2, "xmax": +3.2}

        if "MaxTriJetPt_dPhiAverage" == histo:
            kwargs["xlabel"] = "#bar{#Delta#phi} (%s)" % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}
            kwargs["log"]    = True
            
        if "MaxTriJetPt_dPhiMin" == histo:
            kwargs["xlabel"] = "#Delta#phi (%s)" % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}
            kwargs["log"]    = True

        if "dRMin_Phi" in histo:
            kwargs["xlabel"] = "#phi (%s)" % units
            kwargs["opts"]   = {"xmin": -3.2, "xmax": +3.2}

        if "dRMin_dPhi" in histo:
            kwargs["xlabel"] = "#Delta#phi (%s)" % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

        if "MaxDiJetMass_dPhi" in histo:
            kwargs["xlabel"] = "#Delta#phi (%s)" % units
            kwargs["opts"]       = {"xmin": 0.0, "xmax": +3.2}#, "ymin": 1e+0, "ymaxfactor": 10}
            kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}

        if "dRMinDiJet_NoBJets_dPhi" == histo:
            kwargs["xlabel"] = "#Delta#phi (%s)" % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}
            kwargs["log"]    = True

    if "dRMinDiJet_NoBJets_dEta" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 3.0}
        kwargs["log"]    = True

    if "MaxMass_M" in histo:
        kwargs["rebinX"] = 2
        units            = "GeV/c^{2}"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "M (%s)"  % units
        kwargs["log"]    = True
        kwargs["opts"]   = {"xmin": 0, "xmax": 1500}

    if "MaxPt_M" in histo:
        kwargs["rebinX"] = 4
        units            = "GeV/c^{2}"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "M (%s)"  % units
        kwargs["log"]    = True
        kwargs["opts"]   = {"xmin": 0, "xmax": 1200}

    if "MaxPt_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_dEta" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}

    if "BQuarkPair_dEtaAverage" in histo:
        kwargs["rebinX"] = 2
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#bar{#Delta#eta}"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}

    if "BQuarkPair_dPhiAverage" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#bar{#Delta#phi} (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if "BQuarkPair_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_dRAverage" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#bar{#DeltaR}"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_dRMin_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +4.0}

    if "BQuarkPair_dRMin_jet1_dPhi" == histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if "BQuarkPair_dRMin_jet1_dEta" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}
        kwargs["log"]   = True

    if "BQuarkPair_dRMin_jet2_dPhi" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if "BQuarkPair_dRMin_jet2_dEta" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}
        kwargs["log"]   = True

    if "BQuarkPair_MaxPt_jet1_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_MaxPt_jet2_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_dRMin_jet1_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_dRMin_jet2_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_MaxMass_jet1_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "BQuarkPair_MaxMass_jet2_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}

    if "MaxTriJetPt_dRMax" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}
        kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}

    if "MaxTriJetPt_dRMin" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 26.0}

    if "MaxTriJetPt_dRAverage" == histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#bar{#DeltaR}"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}

    if "dRMinDiJet_NoBJets_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}
        kwargs["log"]    = True
                
    if "BQuarkPair_MaxMass_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}
        
    if "Rap" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#omega"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -10.0, "xmax": +10.0}
        
        if "MaxTriJetPt_Rap" in histo:
            kwargs["opts"]   = {"xmin": -3.0, "xmax": +3.0}

        if "dRMinDiJet_NoBJets_Rap" in histo:
            kwargs["opts"]   = {"xmin": -3.0, "xmax": +3.0}
            
        if "MaxDiJetMass_Rap" in histo:
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -5.0, "xmax": +5.0}

        if "dRap" in histo:
            kwargs["xlabel"] = "#Delta#omega"
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}
            if "MaxDiJetMass_dRap" in histo:
                kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": -0.1}
            if "MaxDiJetMass_dRrap" in histo:
                kwargs["moveLegend"] = {"dx": -0.53, "dy": -0.0, "dh": -0.1}
            
    if "BQuarks_N" in histo:
        units            = ""
        kwargs["ylabel"] = yLabel + " / %.0f"
        kwargs["xlabel"] = "b-quark multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +14.0}
        kwargs["log"]    = True

    if "GenJet_N" in histo:
        units            = ""
        kwargs["ylabel"] = yLabel + " / %.0f"
        kwargs["xlabel"] = "genJets multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +15.0}

    if "_Mass" in histo:
        kwargs["rebinX"] = 2
        units            = "GeV/c^{2}"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "M (%s)"  % units
        kwargs["log"]    = True
        kwargs["opts"]   = {"xmin": 0, "xmax": 800}

        if "MaxTriJetPt_Mass" in histo:
            kwargs["rebinX"] = 4
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0}
            kwargs["log"]    = False
            #kwargs["opts"]   = {"xmin": 0.0, "xmax": +3000.0}
            #kwargs["log"]    = True

        if "dRMinDiJet_NoBJets_Mass" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +800.0}

        if "MaxDiJetMass_Mass" in histo:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +2000.0}
        
    if "MaxDiJetMass_dR" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#DeltaR"
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +6.0}
        kwargs["moveLegend"] = {"dx": -0.53, "dy": -0.0, "dh": -0.1}

    if "MaxTriJetPt_dRMin" in histo:
        kwargs["ylabel"] = yLabel + " / %.2f"
        kwargs["rebinX"] = 1
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.5}

    if "BQuarkPair_dRMin_Pt" in histo:
        kwargs["rebinX"] = 1
        units            = "GeV/c"
        kwargs["ylabel"] = yLabel + " / %.0f " + units
        kwargs["xlabel"] = "p_{T} (%s)"  % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +600.0}

    if "BQuarkPair_dRMin_dEta" in histo:
        kwargs["rebinX"] = 2
        kwargs["ylabel"] = yLabel + " / %.1f"
        kwargs["xlabel"] = "#Delta#eta"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0}

    if "BQuarkPair_dRMin_dPhi" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if "BQuarkPair_dRMin_jet1_dPhi" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if "BQuarkPair_dRMin_jet2_dPhi" in histo:
        kwargs["ylabel"] = yLabel + " / %.1f"
        units            = "rads"
        kwargs["xlabel"] = "#Delta#phi (%s)" % units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3.2}

    if opts.normaliseToOne:
        yMin = 1e-5
    else:
        yMin = 1e0

    if kwargs["log"] == True:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.2

    # Finalise and return
    kwargs["opts"]["ymaxfactor"] = yMaxFactor
    kwargs["opts"]["ymin"]       = yMin
    return kwargs
  

def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Get histogram<->kwargs dictionary 
    kwargs = GetHistoKwargs(histo, opts)

    # Customise styling
    if 0:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerSize(0))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerStyle(6))

    # Customise signal
        for d in datasetsMgr.getAllDatasetNames():
            if "Charged" not in d:
                continue
            else:
                #p.histoMgr.setHistoDrawStyle(d, "HIST")
                p.histoMgr.setHistoLegendStyle(d, "L")
                p.histoMgr.setHistoLegendStyle(d, "L")
        
    #  Customise QCD style
    p.histoMgr.setHistoDrawStyle("QCD", "P")
    p.histoMgr.setHistoLegendStyle("QCD", "P")
    p.histoMgr.setHistoLegendLabelMany({
            "QCD": "QCD (MC)",
            })

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        dName = "ChargedHiggs_HplusTB_HplusToTB_M_%s" %m
        if dName in datasetsMgr.getAllDatasetNames():
            p.histoMgr.forHisto(dName, styles.getSignalStyleHToTB_M(m))
            p.histoMgr.setHistoLegendStyle(dName, "LP")

    # Plot customised histogram
    plots.drawPlot(p, 
                   histo,  
                   xlabel       = kwargs.get("xlabel"),
                   ylabel       = kwargs.get("ylabel"),
                   log          = kwargs.get("log"),
                   rebinX       = kwargs.get("rebinX"), 
                   cmsExtraText = "Preliminary", 
                   #createLegend = {"x1": 0.62, "y1": 0.75, "x2": 0.92, "y2": 0.92},
                   moveLegend   = kwargs.get("moveLegend"),
                   opts         = kwargs.get("opts"),
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = kwargs.get("cutBox"),
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    if opts.folder == "":
        savePath = os.path.join(opts.saveDir, opts.optMode)
    else:
        savePath = os.path.join(opts.saveDir, histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath, [".png", ".pdf"]) 
    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(savePath + ext, i==0)
        plot.saveAs(savePath, formats=saveFormats)
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
    ANALYSISNAME = "Kinematics"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [200, 500, 800, 2000]
    SIGNALMASS   = [300, 500, 800, 1000]
    #SIGNALMASS   = [200, 500, 800, 1000, 2000, 3000]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "TH1" #"TH2"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    #parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
                      #help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Sanity check
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_1d.py: Press any key to quit ROOT ...")
