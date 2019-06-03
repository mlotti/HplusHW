#!/usr/bin/env python
'''
Description:

Usage:
./plotMC_HPlusMass.py -m <pseudo_mcrab> [opts]

Examples:
./plotMC_HPlusMass.py -m <peudo_mcrab> -o "" --url --nomaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --folder topologySelection_ --url --normaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalMass 500
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalsMass 500

Last Used:
./plotMC_HPlusMass.py -m MyHplusAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --normaliseToOne --url --mergeEWK
./plotMC_HPlusMass.py -m MyHplusAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --normaliseToOne --folder ""
./plotMC_HPlusMass.py -m MyHplusAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --folder topSelection_ --url --normaliseToOne

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import getpass
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


def GetListOfQCDatasets():
    Verbose("Getting list of QCD datasets")
    return ["QCD_bEnriched_HT200to300",
            "QCD_bEnriched_HT300to500",
            "QCD_bEnriched_HT500to700",
            "QCD_bEnriched_HT700to1000",
            "QCD_HT1000to1500",
            "QCD_bEnriched_HT1000to1500",
            "QCD_bEnriched_HT1500to2000",
            "QCD_bEnriched_HT2000toInf",
            "QCD_HT1500to2000_ext1",
            "QCD_HT2000toInf",
            "QCD_HT2000toInf_ext1",
            "QCD_HT200to300",
            "QCD_HT200to300_ext1",
            "QCD_HT1000to1500_ext1",
            "QCD_HT100to200",
            "QCD_HT1500to2000",
            "QCD_HT500to700_ext1",
            "QCD_HT50to100",
            "QCD_HT700to1000",
            "QCD_HT700to1000_ext1",
            "QCD_HT300to500",
            "QCD_HT300to500_ext1",
            "QCD_HT500to700"
            ]


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

    optModes = ["OptChiSqrCutValue100"]                                                                                                                             

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
                       
        # Determine integrated Lumi before removing data
#        intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 35920
        datasetsMgr.PrintInfo()

    
        #datasetsMgr.merge("QCD", GetListOfQCDatasets())
        #plots._plotStyles["QCD"] = styles.getQCDLineStyle()

        
        #if opts.noQCD:
            #datasetsMgr.remove(filter(lambda name: "QCD_b" in name, datasetsMgr.getAllDatasetNames()))  
            #datasetsMgr.remove(filter(lambda name: "QCD_HT" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))


        # Remove datasets
        if 1:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "Diboson" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD_b" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "QCD_HT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "SingleTop" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "DYJetsToQQHT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTZToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "WJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "Diboson" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTTT" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "FakeBMeasurementTrijetMass" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "M_" in name and "M_" + str(opts.signalMass) not in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "ZJets" in name, datasetsMgr.getAllDatasetNames()))
            
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 

        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Determine integrated Lumi before removing data
        intLumi = 35920
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            if "M_" in d.getName():
#            if "M_" in d.getName() and "200" not in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())

            #newOrder = ["TT", "QCD"]
            #newOrder = ["TT", "QCD"]
        for m in signalMass:
            #newOrder.insert(0, m)
            datasetOrder.insert(0, m)
            #datasetsMgr.selectAndReorder(newOrder)
        datasetsMgr.selectAndReorder(datasetOrder)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
        style.setGridY(False)

        # Do the topSelection histos
        folder      = opts.folder 
        histoPaths1 = []

        if folder != "":
            histoList  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folder)
            histoPaths1 = [os.path.join(folder, h) for h in histoList]
        
        folder     = ""
        histoList  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folder)
        hList0     = [x for x in histoList if "TrijetMass" in x]
        hList1     = [x for x in histoList if "TetrajetMass" in x]
        hList2     = [x for x in histoList if "TetrajetBjetPt" in x]
        histoPaths2 = [os.path.join(folder, h) for h in hList0+hList1+hList2]

        histoPaths = histoPaths1 + histoPaths2

        for h in histoPaths:
            if "Vs" in h: # Skip TH2D
                continue
            if "VS" in h: # Skip TH2D
                continue

            PlotMC(datasetsMgr, h, intLumi)
        ROOT.gStyle.SetNdivisions(10, "X")

        
    return

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]



def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf", ".png"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s/" % (getpass.getuser()))
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(savePath + ext, i==0)
        plot.saveAs(savePath, formats=saveFormats)
    return





#PlotMC(datasetsMgr, h, intLumi)
def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)
#    p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)
    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.1f"
    _xlabel = None

    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}


    if "ChiSqr" in histo:
        _rebinX = 1
        #logY    = True
        _units  = ""
        _format = "%0.1f " + _units
        _xlabel = "#chi^{2}"
        _cutBox = {"cutValue": 10.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 100

    elif "trijetjets_deltarmin" in histo.lower():
        _xlabel = "#Delta R_{min}"
        _rebinX = 2
        _opts["xmax"] = 3
        _units = ""
        _format = "%0.1f "
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        
        
    elif "trijetjets_deltarmax" in histo.lower():
        _xlabel = "#Delta R_{max}"
        _rebinX = 2
        _opts["xmax"] = 3.5
        _units = ""
        _format = "%0.1f "
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    elif "trijetdijetdr" in histo.lower():
        _rebinX = 1
        units = ""
        _format = "%0.1f "
        _opts["xmax"] = 3.5
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    elif "trijetdijetpt" in histo.lower():
        _rebinX = 2
        _units = "GeV/c"
        _format = "%0.0f " + _units
        _opts["xmax"] = 800

    elif "trijetdijetmass" in histo.lower():
        _rebinX = 1
        _units = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _opts["xmax"] = 200
        _xlabel = "m_{w} (%s)" % _units
        _cutBox = {"cutValue": 80.39, "fillColor": 16, "box": False, "line": True, "greaterThan": True}


    if "cevts_ldgtrijetmatchedtofatjet_fatjetpt" in histo.lower():
        _rebin = 1
        _opts["xmax"] = 3

    elif "pt" in histo.lower():
        _rebinX = 2
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _opts["xmax"] = 800



    elif "trijetmass" in histo.lower():
        _rebinX = 1
#        logY    = False
        _units  = "GeV/c^{2}"
#        _format = "%0.0f " + _units
        _format = "%0.0f" + (_units)
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 305 #1005
        _opts["xmin"] = 55 #1005


    elif "topcandmass" in histo.lower():
        _rebinX = 1
#        logY    = False
        _units  = "GeV/c^{2}"
#        _format = "%0.0f " + _units
        _format = "%0.0f" + (_units)
        _xlabel = "m_{jjb}^{BDTG} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 505 #1005
        _opts["xmin"] = 0 #1005


#    elif "ht" in histo.lower():
#        _rebinX = 2
##        logY    = False
#        _units  = "GeV"
#        _format = "%0.0f " + _units
#        _xlabel = "H_{T} (%s)" % _units
#        _cutBox = {"cutValue": 500, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
#        _opts["xmax"] = 2000

    elif "tetrajetptd" in histo.lower():
        _rebinX = 2 #5 #10 #4
        _units  = "GeV/c^{2}"
#        _xlabel = "m_{jjbb} (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 2000 #3500.0
        _cutBox = {"cutValue": 400, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    elif "tetrajetmass" in histo.lower() or "tetrajetmass_" in histo.lower():
        #ROOT.gStyle.SetNdivisions(10, "X")
#        h = dataset.getDatasetRootHisto(histo).getHistogram()
#        h.SetTickLength(100, "X")
        _rebinX = 5 #5 #10 #4
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 1500 #3500.0
        _cutBox = {"cutValue": 500, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    elif "dijetmass" in histo.lower():
        _rebinX = 1 #5 #10 #4
#        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{W} (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 800 #3500.0
        _cutBox = {"cutValue": 80.4, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 205

    elif "trijetmultiplicitypassbdt" in histo.lower():
        _rebinX = 1
        _opts["xmax"] = 5
        _format = "%0.0f "

    elif "bdtg" or "bdtvalue" in histo.lower():
        _rebinX = 1 
        _format = "%0.2f "

    elif "trijetbdt_mass" in histo.lower():
        _rebinX = 2
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _opts["xmax"] = 800


#    if "eta" or "phi" or "delta" in histo.lower():
        #_rebinX = 1 #5 #10 #4
#        _units  = ""
#        _format = "%0.1f " 

#    if "eta" in histo.lower():
#        _xlabel = "#eta"
#    if "phi" in histo.lower():
#        _xlabel = "#phi"
#    if "pt" in histo.lower():
#        _opts["xmax"] = 800
    elif "boosted" in histo.lower():
        _xlabel = "Trijet Counter"
    elif "matched_dijetpt" in histo.lower():
        _units = "(GeV/c)"
        _xlabel = "p_{T}" +_units

    elif "deltar_bdttrijets_tetrajetbjet" in  histo.lower():
        _xlabel = "#Delta R(Trijet,b_{free})"



    elif "tetrajetbjetbdisc" in histo.lower():
        _rebinX = 2
        _opts["xmax"] = 1.05

#    if "matched_dijetmass" in histo.lower():
#        _rebinX = 2
#    if "higgstop_dijetmass" in histo.lower():
#        _rebinX = 2
        
    elif "trijet_deltaeta_trijet_tetrajetbjet" in histo.lower():
        _rebinX = 2
        _xlabel = "#Delta #eta (Trijet, b_{free})"

    elif "trijet_deltaphi_trijet_tetrajetbjet" in histo.lower():
        _xlabel = "#Delta #phi (Trijet, b_{free})"
    elif "cevts_closejettotetrajetbjet_isbtagged" in histo.lower():
        _units = ""
        _format = "%0.0f " + _units
#    if "higgstop_" in histo.lower():
#        _rebinX = 2
    if "eventtrijetpt2t" in histo.lower():
        _rebinX = 2

    if "ldgfatjetpt" in histo.lower():
        _opts["xmax"] = 1000

    if "deltar_w" in histo.lower():
        _rebinX = 2
        _xlabel = "#Delta R"
        _format = "%0.1f "
        _opts["xmax"] = 5
        logY = True

    if "ldgtrijet_deltar" in histo.lower():
        _rebinX = 2
        _xlabel = "#Delta R"
        _format = "%0.1f "
        _opts["xmax"] = 5
        logY = True

    if "higgstop_deltar" in histo.lower():
        _rebinX = 2
        _xlabel = "#Delta R"
        _format = "%0.1f "
        _opts["xmax"] = 5
        logY = True


    if "allfatjet" in histo.lower():
        _rebinX = 2
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _opts["xmax"] = 800


    else:
        pass


    if opts.normaliseToOne:
        logY    = True
        Ylabel  = "Arbitrary Units / %s" % (_format)
    else:
        logY    = True
        Ylabel  = "Events / %s" % (_format)

    if logY:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.2


    _opts["ymaxfactor"] = yMaxFactor
    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
        #_opts   = {"ymin": 1e-3, "ymaxfactor": yMaxFactor, "xmax": None}
    else:
        _opts["ymin"] = 1e0
        #_opts["ymaxfactor"] = yMaxFactor
        #_opts   = {"ymin": 1e0, "ymaxfactor": yMaxFactor, "xmax": None}

    # Customise styling
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    if "QCD" in datasetsMgr.getAllDatasets():        
        p.histoMgr.forHisto("QCD", styles.getQCDFillStyle() )
        p.histoMgr.setHistoDrawStyle("QCD", "HIST")
        p.histoMgr.setHistoLegendStyle("QCD", "F")

    if "TT" in datasetsMgr.getAllDatasets():
        p.histoMgr.setHistoDrawStyle("TT", "HIST")
        p.histoMgr.setHistoLegendStyle("TT", "LP")

#    if "M_200" in datasetsMgr.getAllDatasets() or "M_300" in datasetsMgr.getAllDatasets():        
#        p.histoMgr.forHisto("QCD", styles.getQCDFillStyle() )
#        p.histoMgr.setHistoDrawStyle("QCD", "P")
#        p.histoMgr.setHistoLegendStyle("QCD", "F")

#    elif d.getName() == "TT" or d.getName() == "QCD" or d.getName() == "Data":
#            otherHisto = histograms.Histo(histo, legName, "LP", "P")
#            otherHistos.append(otherHisto)


    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))
#soti
#        p.histoMgr.setHistoDrawStyle("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, "LP")
#        p.histoMgr.setHistoLegendStyle("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, "P")
        

    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = Ylabel,#"Arbitrary Units / %s" % (_format), #"Events / %s" % (_format), #"Arbitrary Units / %s" % (_format),
#                   ylabel       = "Arbitrary Units / %s" % (_format), #"Events / %s" % (_format), #"Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", #_rebinX
                   #createLegend = {"x1": 0.48, "y1": 0.45, "x2": 0.92, "y2": 0.92}, #All datasets
#                   createLegend = {"x1": 0.58, "y1": 0.7, "x2": 0.92, "y2": 0.92},
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.87},
                   #createLegend = {"x1": 0.73, "y1": 0.85, "x2": 0.97, "y2": 0.77},   #One dataset
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)

    if opts.normaliseToOne:
        save_path = savePath + opts.MVAcut
        if opts.noQCD:
            save_path = savePath + opts.MVAcut + "/noQCD/"
    else:
        save_path = savePath + opts.MVAcut + "/normToLumi/TT/"
        if opts.noQCD:
            save_path = savePath + opts.MVAcut + "/noQCD/"

#    SavePlot(p, saveName, savePath) 
    SavePlot(p, saveName, save_path) 

    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf", ".png"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s/" % (getpass.getuser()))
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
    ANALYSISNAME = "TopRecoAnalysis"
    MVACUT       = "TH1plots"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    SIGNALMASS   = [500, 400]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    NOQCD        = False
#    if (1): #opts.normaliseToOne:
#        DIR = MVACUT
#    else:
#        DIR = MVACUT+ "/normToLumi/"
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"

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

    parser.add_option("--MVAcut", dest="MVAcut", type="string", default = MVACUT,
                      help="Save plots to directory in respect of the MVA cut value [default: %s]" % (MVACUT) )

    parser.add_option("--noQCD", dest="noQCD", action="store_true", default = NOQCD,
                      help="Exclude QCD samples [default: %s]" % (NOQCD) )


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
        raw_input("=== plotMC_HPlusMass.py: Press any key to quit ROOT ...")
