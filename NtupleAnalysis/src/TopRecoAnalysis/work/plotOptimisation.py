#!/usr/bin/env python
'''
Description:

Usage:
./plotProbability.py -m <pseudo_mcrab> [opts]

Examples:
./plotMC_HPlusMass.py -m <peudo_mcrab> -o "" --url --normaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --folder topologySelection_ --url --normaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalMass 500
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalMass 500

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
from optparse import OptionParser

import ROOT
import array

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
# ==============================================================================================


kwargs = {
    "verbose"          : False,
    "dataEra"          : None,
    "searchMode"       : None,
    "analysis"         : "MyHplusKInematics",
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf"],
    "xlabel"           : None,
    "ylabel"           : "Probability",#"Probability",
    "rebinX"           : 1,
    "rebinY"           : 1,
    "xlabelsize"       : None,
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : True,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Simulation",
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": +0.0, "dh": +0.1},
    "cutValue"         : None,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
    "zlabel"           : "test",
    "drawStyle"      : "CPE",  #CPE                                                                                                                                                                                    
    "legStyle"       : "LP",

    }


htb = "ChargedHiggs_HplusTB_HplusToTB_"
styleDict = {
     "Data"             : styles.dataStyle,
     htb + "M_800"      : styles.signal800Style,
     htb + "M_2000"     : styles.signal2000Style,
     htb + "M_1000"     : styles.signal1000Style,
     htb + "M_500"      : styles.signal500Style,
     htb + "M_400"      : styles.signal400Style,
     htb + "M_350"      : styles.signal350Style,
     htb + "M_300"      : styles.signal300Style,
     htb + "M_250"      : styles.signal250Style,
     htb + "M_220"      : styles.signal220Style,
     htb + "M_200"      : styles.signal200Style,
     htb + "M_180"      : styles.signal180Style,
     "QCD-b"            : styles.qcdBEnrichedStyle,
     "QCD"              : styles.qcdStyle, #qcdFillStyle,                                                                                                                                                               
     "QCD_Pt_15to30"    : styles.qcdFillStyle,
     "QCD_Pt_30to50"    : styles.qcdFillStyle,
     "QCD_Pt_50to80"    : styles.qcdFillStyle,
     "QCD_Pt_80to120"   : styles.qcdFillStyle,
     "QCD_Pt_120to170"  : styles.qcdFillStyle,
     "QCD_Pt_170to300"  : styles.qcdFillStyle,
     "QCD_Pt_300to470"  : styles.qcdFillStyle,
     "QCD_Pt_470to600"  : styles.qcdFillStyle,
     "QCD_Pt_600to800"  : styles.qcdFillStyle,
     "QCD_Pt_800to1000" : styles.qcdFillStyle,
     "QCD_Pt_1000to1400": styles.qcdFillStyle,
     "QCD_Pt_1400to1800": styles.qcdFillStyle,
     "QCD_Pt_1800to2400": styles.qcdFillStyle,
     "QCD_Pt_2400to3200": styles.qcdFillStyle,
     "QCD_Pt_3200toInf" : styles.qcdFillStyle,

     "QCD_bEnriched_HT300to500"  : styles.qcdFillStyle,
     "QCD_bEnriched_HT500to700"  : styles.qcdFillStyle,
     "QCD_bEnriched_HT700to1000" : styles.qcdFillStyle,
     "QCD_bEnriched_HT1000to1500": styles.qcdFillStyle,
     "QCD_bEnriched_HT1500to2000": styles.qcdFillStyle,
     "QCD_bEnriched_HT2000toInf" : styles.qcdFillStyle,

     "TTBB"                   : styles.ttbbStyle,
     "TT"                   : styles.signal350Style,#styles.ttStyle, #here                                                                                                                                              
     "TTJets"               : styles.ttjetsStyle,
     "SingleTop"            : styles.singleTopStyle,
     "TTTT"                 : styles.ttttStyle,
     "TTWJetsToQQ"          : styles.ttwStyle,
     "TTZToQQ"              : styles.ttzStyle,
     "WJetsToQQ_HT_600ToInf": styles.wjetsStyle,
     "WWTo4Q"               : styles.wStyle,
     "ZJetsToQQ_HT600toInf" : styles.zjetsStyle,
     "ZZTo4Q"               : styles.zzStyle ,
     "Diboson"              : styles.dibStyle,
     "ttbb"                 : styles.ttbbStyle,
     "QCD"                  : styles.ttbbStyle,
     "EWK"                  : styles.ttStyle,
     "Top"                  : styles.qcdBEnrichedStyle,
     "QCD+Top"              : styles.zjetsStyle,
     }

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

#"QCD_HT1000to1500|QCD_HT1500to2000|QCD_HT200\
#0toInf|QCD_HT300to500|QCD_HT500to700|QCD_HT700to1000"
def GetListOfQCDatasets():
    Verbose("Getting list of QCD datasets")
    return ["QCD_HT1000to1500", "QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000"]

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
    

# =========================================================================================================================================
#                                                          MAIN
# =========================================================================================================================================
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
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Determine integrated Lumi before removing data
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 35800

        # Remove datasets
        if 1:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTZToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTTT" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "FakeBMeasurementTrijetMass" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "M_" in name and "M_" + str(opts.signalMass) not in name, datasetsMgr.getAllDatasetNames()))

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

#        datasetsMgr.merge("QCD", GetListOfQCDatasets())
#        plots._plotStyles["QCD"] = styles.getAltEWKStyle()
#        Background1_Dataset = datasetsMgr.getDataset("QCD")
        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            if "M_" in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())
            
        for m in signalMass:
            datasetOrder.insert(0, m)
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
        
        numerators   = ["TopQuarkPt_InTopDirBDT",
                        "AllTopQuarkPt_InTopDirBDT",
                        "AllTopQuarkPt_MatchedBDT",
                        "TrijetNotInTopDirPt_BDT",
                        "TrijetFakePt_BDT",
                        "AllTopQuarkPt_InTopDir",
                        "AllTopQuarkPt_Matched",
                        "EventTrijetPt2T_MatchedBDT",
                        "EventTrijetPt2T_MatchedBDT",
                        "EventTrijetPt2T_MatchedBDT",
                        "AllTopQuarkPt_NotInTopDir",
                        "EventTrijetPt_InTopDirBDT",
                        "AllTopQuarkPt_MatchedBDT",
                        "TrijetPtMaxMVASameFakeObj_BjetPassCSV",
                        "SelectedTrijetsPt_BjetPassCSVdisc_afterCuts",
                        "TrijetPt_PassBDT_BJetPassCSV",
                        "TopFromHiggsPt_isLdgMVATrijet_afterCuts",
                        "TopFromHiggsPt_isSubldgMVATrijet_afterCuts",
                        "TopFromHiggsPt_isMVATrijet_afterCuts",
                        "LdgBjetPt_isLdgFreeBjet",
                        "ChHiggsBjetPt_TetrajetBjetPt_Matched_afterCuts",
                        "TopFromHiggsPt_notMVATrijet_afterCuts",
                        "HiggsBjetPt_isTrijetSubjet_afterCuts",
                        ]
        denominators = ["TrijetPt_BDT",
                        "AllTopQuarkPt_InTopDir",
                        "AllTopQuarkPt_Matched",
                        "TrijetNotInTopDirPt",
                        "TrijetFakePt",
                        "TopQuarkPt",
                        "TopQuarkPt",
                        "EventTrijetPt2T_BDT",
                        "EventTrijetPt2T_Matched",
                        "EventTrijetPt2T",
                        "TopQuarkPt",
                        "EventTrijetPt_BDT",
                        "TopQuarkPt",
                        "TrijetPtMaxMVASameFakeObj",
                        "SelectedTrijetsPt_afterCuts",
                        "TrijetPt_PassBDT",
                        "TopFromHiggsPt_afterCuts",
                        "TopFromHiggsPt_afterCuts",
                        "TopFromHiggsPt_afterCuts",
                        "LdgBjetPt",
                        "ChHiggsBjetPt_foundTetrajetBjet_afterCuts",
                        "TopFromHiggsPt_afterCuts",
                        "HiggsBjetPt_afterCuts",
                        ]
        

#        for i in range(len(numerators)):
#            PlotProb(datasetsMgr.getAllDatasets(), folder+"/"+numerators[i], folder+"/"+denominators[i])
        datasets = datasetsMgr.getAllDatasets()
        signals = []
        for dataset in datasets:
            if "M_300" in dataset.getName():
                signal300_dataset = dataset
                signals.append(signal300_dataset)
            if "M_200" in dataset.getName():
                signal200_dataset = dataset
                signals.append(signal200_dataset)
            if "M_500" in dataset.getName():
                signal500_dataset = dataset
                signals.append(signal500_dataset)
            if "M_1000" in dataset.getName():
                signal1000_dataset = dataset
                signals.append(signal1000_dataset)
            if "TT" in dataset.getName():
                backgroundTT_dataset = dataset
                datasetName = dataset.getName()
                #print "Dataset = ", datasetName
            
        for hName in [folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet"]:
#            for signal_dataset in signals:
#                maxSignX, maxSignY, hSignif = GetRectangularSignificance(signal_dataset, backgroundTT_dataset, hName)

            maxSignX, maxSignY, hSignif = GetCircularSignificance(signals, backgroundTT_dataset, hName, intLumi)
            GetCircularEfficiency(signals, backgroundTT_dataset, hName, intLumi)
            maxSignX_opp, maxSignY_opp, hSignif_opp = GetCircularSignificance_opp(signals, backgroundTT_dataset, hName, intLumi)
            GetCircularEfficiency_opp(signals, backgroundTT_dataset, hName, intLumi)

        hName_real  = "TopAnalysisTH2True/DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth"
        hName_total = folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet"
        maxSignXreal, maxSignYreal, hSignif_real = GetCircularSignificance_RealTetrajet(signals, backgroundTT_dataset, hName_real, hName_total, intLumi)
        GetCircularEfficiency_RealTetrajet(signals, backgroundTT_dataset, hName_real, hName_total, intLumi)

        maxSignXreal_opp, maxSignYreal_opp, hSignif_real_opp = GetCircularSignificance_RealTetrajet_opp(signals, backgroundTT_dataset, hName_real, hName_total, intLumi)
        GetCircularEfficiency_RealTetrajet_opp(signals, backgroundTT_dataset, hName_real, hName_total, intLumi)


        hName_tetrajetMass = "AnalysisTriplets/TetrajetMass"
        for hName in  ["AnalysisTriplets/TetrajetMass_closeJetToTetrajetBjet", 
                       "AnalysisTripletsTrue/TetrajetMass_closeJetToTetrajetBjet", 
                       "AnalysisTripletsFalse/TetrajetMass_closeJetToTetrajetBjet"]:        
            bkg_total = backgroundTT_dataset.getDatasetRootHisto(hName_tetrajetMass)
            bkg = backgroundTT_dataset.getDatasetRootHisto(hName)
            bkg.normalizeToLuminosity(intLumi)
            bkg_total.normalizeToLuminosity(intLumi)
            hBkg = bkg.getHistogram()
            hBkg_total = bkg_total.getHistogram()
            #CheckNegatives(hBkg, hBkg_total, True)

            Ibackground = hBkg.Integral(0, hBkg.GetXaxis().GetNbins()+1)
            Ibackground_total = hBkg_total.Integral(0, hBkg_total.GetXaxis().GetNbins()+1)
            
            print backgroundTT_dataset.getName(), hName+": ", Ibackground/Ibackground_total
            for signal_dataset in signals:
                sig_total = signal_dataset.getDatasetRootHisto(hName_tetrajetMass)
                sig = signal_dataset.getDatasetRootHisto(hName)

                sig.normalizeToLuminosity(intLumi)
                sig_total.normalizeToLuminosity(intLumi)
                
                hSig = sig.getHistogram()
                hSig_total = sig_total.getHistogram()
                
                #CheckNegatives(hSig, hSig_total, True)

                Isignal = hSig.Integral(0, hSig.GetXaxis().GetNbins()+1)
                Isignal_total = hSig_total.Integral(0, hSig_total.GetXaxis().GetNbins()+1)

                print signal_dataset.getName(), hName+": ", Isignal/Isignal_total
                #PlotTH2(datasetsMgr, signal_dataset, hSignif, "Signif")
#        for hName in [folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet", 
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p1",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p2",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p3",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p4",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p5",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1", 
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1p5", 
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2",
#                      folder+"/"+"DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2p5"
#                      ]:
#            for signal_dataset in signals:
#                sig = signal_dataset.getDatasetRootHisto(hName)
#                sig.normalizeToLuminosity(intLumi)
#                h_Signal = sig.getHistogram()
#                bkg = backgroundTT_dataset.getDatasetRootHisto(hName)
#                bkg.normalizeToLuminosity(intLumi)
#                h_Background = bkg.getHistogram()
#                h_Signal = signal_dataset.getDatasetRootHisto(hName).getHistogram()
#                h_Background = backgroundTT_dataset.getDatasetRootHisto(hName).getHistogram()
                
#                signal_total = h_Signal.Integral(0, h_Signal.GetXaxis().GetNbins()+1, 0, h_Signal.GetYaxis().GetNbins()+1)
#                background_total = h_Background.Integral(0, h_Background.GetXaxis().GetNbins()+1, 0, h_Background.GetYaxis().GetNbins()+1)
                

#                print "CHECK ", hName, signal_total/math.sqrt(background_total+signal_total)
#                print "pass plots", signal_total, background_total

        folder     = "ForDataDrivenCtrlPlots"
        histoList  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folder)
        hList0     = [x for x in histoList if "TrijetMass" in x]
        hList1     = [x for x in histoList if "TetrajetMass" in x]
        hList2     = [x for x in histoList if "TetrajetBjetPt" in x]
        histoPaths2 = [os.path.join(folder, h) for h in hList0+hList1+hList2]
        

    return


def GetHistoKwargs(h, opts):

    # Defaults                                                                                                                                                                                                          
    xMin  =   0
    if opts.logX:
        yMin    =  1e0
    xMax  = 800
    yMin  =   0
    yMax  = 800
    if opts.logY:
        yMin    =  1
    yMaxF       = 10
    zMin        =  0
    zMax        = None
    zLabel      = "z-axis"
    if opts.normalizeToLumi:
        zLabel  = "Events"
        #zMin    = 1e-1                                                                                                                                                                                                 
    elif opts.normalizeByCrossSection:
        zLabel  = "#sigma (pb)"
        #zMin    = 0 #1e-3                                                                                                                                                                                              
    elif opts.normalizeToOne:
        zLabel  = "Arbitrary Units"
    else:
        zLabel = "Unknown"
    cutBox      = {"cutValue": -1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #box = True works                                                                                               
    cutBoxY     = {"cutValue": -1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,

                   "mainCanvas": True, "ratioCanvas": False} # box = True not working                                                                                                                                   
    kwargs = {
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": opts.normalizeToLumi,
        "addCmsText"       : True,
        "cmsExtraText"     : "  Preliminary",
        "xmin"             : xMin,
        "xmax"             : xMax,
        "ymin"             : yMin,
        "zmin"             : zMin,
        "zmax"             : zMax,
        "cutBox"           : cutBox,
        "cutBoxY"          : cutBoxY,
        "moveLegend"       : {"dx": -2.0, "dy": 0.0, "dh": -100.0}, #hack to remove legend (tmp)                                                                                                                        
        "zlabel"           : zLabel
        }

    return kwargs

def PlotTH2(datasetsMgr, signal_dataset, histo, histoName):
    #p = plots.PlotBase([histo], kwargs.get("saveFormats"))
        
        #p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
    Verbose("Plotting Data-MC Histograms")

    # Get Histogram name and its kwargs                                                                                                                                                                                 
    saveName = histoName.rsplit("/")[-1]
    kwargs   = GetHistoKwargs(saveName, opts)

    # Create the 2d plot                                                                                                                                                                                                
#    if opts.dataset == "Data":
#        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])
#    else:
    if(0):
        if opts.normalizeToLumi:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
        elif opts.normalizeByCrossSection:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeByCrossSection=True, **{})
        elif opts.normalizeToOne:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToOne=True, **{})
        else:
            raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")

    p = plots.PlotBase(datasetRootHistos=[histo], saveFormats=kwargs.get("saveFormats"))
    #p.setDrawOptions(**kwargs)






    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
    p.createFrame(saveName, opts=options)

     # Set Titles                                                                                                                                                                                                
#    p.getFrame().GetXaxis().SetTitle(xTitle)
#    p.getFrame().GetYaxis().SetTitle(yTitle)
    
    # Set range
#    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
#    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                                                                                                                                                
#    histograms.addStandardTexts()

    p.draw()

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, "HplusMasses", numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut

    SavePlot(p, saveName, save_path)







    # Customise z-axis                                                                  
    #p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle(kwargs["zlabel"]))        
        
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(1.3))
    if kwargs.get("zmin") != None:
        zMin = float(kwargs.get("zmin"))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(zMin))
    if kwargs.get("zmax") != None:
        zMax = float(kwargs.get("zmax"))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(zMax))

    # Drawing style                                                                                                                                                                                                    
    p.histoMgr.setHistoDrawStyleAll("COLZ")

    # Add dataset name on canvas                                                                                                                                                                                       
    p.appendPlotObject(histograms.PlotText(0.18, 0.88, plots._legendLabels[opts.dataset], bold=True, size=22))

    # Draw the plot                                                                                                                                                                                                    
    #plots.drawPlot(p, saveName, **kwargs) #the "**" unpacks the kwargs_ dictionary                                                                                                                                   

    p.draw()

    # Save the plots in custom list of saveFormats                                                                                                                                                                     
    SavePlot(p, saveName, os.path.join(opts.saveDir, dataset, opts.optMode) )
#    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode, opts.folder), [".pdf"])#, ".pdf"] )                                                                                                                  
    return



       # Customise z-axis                                                                           
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle(kwargs["zlabel"]))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(1.3))
#        if kwargs.get("zmin") != None:
#            zMin = float(kwargs.get("zmin"))
#            p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(zMin))
#        if kwargs.get("zmax") != None:
#            zMax = float(kwargs.get("zmax"))
#            p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(zMax))

        # Create a frame                                                                                                                                                                                    
#        opts      = {"ymin": 1E-4, "ymaxfactor": 1.2}
#        saveName = "testPlot"
#        p.createFrame(saveName, opts=opts)
        
        # Customise Legend                                                                                                                                                                                  
#        moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
#        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        # Drawing style                                                                                                                                                                         
#        p.histoMgr.setHistoDrawStyleAll("COLZ")
        # Add dataset name on canvas                                                                                                                                                         
        #p.appendPlotObject(histograms.PlotText(0.18, 0.88, plots._legendLabels[opts.dataset], bold=True, size=22))
        # Draw the plot                                                                                                                                                                                 
        ##plots.drawPlot(p, saveName, **kwargs) #the "**" unpacks the kwargs_ dictionary                                                          
#        p.draw()
        # Save the plots in custom list of saveFormats 
#        sotiSave = "/publicweb/s/skonstan/MyHPlusAnalysis"
#        sotiOptMode = ""
#        sotiFolder = folder
#        SavePlot(p, saveName, os.path.join(sotiSave, sotiOptMode, sotiFolder), [".pdf"])#, ".pdf"] )  


def CheckNegatives(n, d, verbose=False):
    '''
    '''
    table    = []
    txtAlign = "{:<5} {:>20} {:>20}"
    hLine    = "="*50
    table.append(hLine)
    table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
    table.append(hLine)

    # For-loop: All bins in x-axis
    for i in range(1, n.GetNbinsX()+1):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)
#        print i, nbin, dbin
        table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))

        # Numerator > Denominator
        if nbin > dbin:
            n.SetBinContent(i,dbin)

        # Numerator < 0 
        if nbin < 0:
            n.SetBinContent(i,0)
            
        # Denominator < 0
        if dbin < 0:
            n.SetBinContent(i,0)
            d.SetBinContent(i,0)
            
    #if verbose:
    #    for r in table:
    #        print r
    return

# ----------------------------
#  Remove Negatives
# ----------------------------
def RemoveNegatives(histo):
    '''
    '''
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return

# ------------------------------------------------
#    Plot Probabilities
# ------------------------------------------------
def PlotProb(datasets, numPath, denPath):


    EfficiencyList = []

    for dataset in datasets:
        
        datasetName = dataset.getName()
        print "Dataset = ", datasetName
        

        statOption = ROOT.TEfficiency.kFNormal        
        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        n.normalizeToOne()
        d = dataset.getDatasetRootHisto(denPath).getHistogram()
        

#        if "TT" in datasetName and ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#            continue
#        elif "M_"  in datasetName and not ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#            continue

#        n.Rebin(6)
#        d.Rebin(6)
        
        if d.GetEntries() == 0 or n.GetEntries() == 0:
            continue

        if n.GetEntries() > d.GetEntries():
            continue
        # Check Negatives
        CheckNegatives(n, d, True)
        
        # Remove Negatives 
        RemoveNegatives(n)
                
        nBins = d.GetNbinsX()
        xMin  = d.GetXaxis().GetXmin()
        xMax  = d.GetXaxis().GetXmax()
        
        binwidth = int(n.GetBinWidth(0))
                
        # ----------------------------------------------------------------------------------------- #
        #      Ugly hack to ignore EMPTY (in the wanted range) histograms with overflows/underflows
        # ----------------------------------------------------------------------------------------- #
        if (0):
            print "\n"
            print "=========== getEfficiency:"
            print "Dataset             = ", dataset.getName()
            print "Numerator:   entries=", n.GetEntries(), " Bins=", n.GetNbinsX(), " Low edge=", n.GetBinLowEdge(1)
            print "Denominator: entries=", d.GetEntries(), " Bins=", d.GetNbinsX(), " Low edge=", d.GetBinLowEdge(1)
            print "\n"
            
            print ">>>>>>  Sanity Check:  <<<<<<"
            print "Numerator Mean       = ", n.GetMean()
            print "Numerator RMS        = ", n.GetRMS()                                                                                                                
            print "Numerator Integral   = ", n.Integral(1, nBins)
            print "Denominator Mean     = ", d.GetMean()
            print "Denominator RMS      = ", d.GetRMS()
            print "Denominator Integral = ", d.Integral(1, nBins)
            
        if (n.GetMean() == 0 or d.GetMean() == 0): continue
        if (n.GetRMS()  == 0 or d.GetRMS()  == 0): continue
        if (n.Integral(1,nBins) == 0 or d.Integral(1,nBins) == 0): continue
        
#        if not (ROOT.TEfficiency.CheckConsistency(n,d)): continue;
        effic = ROOT.TEfficiency(n,d)
        effic.SetStatisticOption(statOption)
        
        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
            effic.SetWeight(weight)
            
        eff = convert2TGraph(effic)
    

        # Apply Styles
        if "TT" in datasetName:
            styles.signalStyleHToTB500.apply(eff)
#            styles.ttStyle.apply(eff)
            eff.SetLineStyle(1)
            eff.SetLineWidth(3)
            eff.SetLineColor(619)
            legend = "TT"
        elif "M_500" in datasetName:
            styles.signalStyleHToTB500.apply(eff)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in datasetName:
            styles.signalStyleHToTB300.apply(eff)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in datasetName:
            styles.signalStyleHToTB1000.apply(eff)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in datasetName:
            styles.signalStyleHToTB800.apply(eff)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in datasetName:
            styles.signalStyleHToTB200.apply(eff)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        else:
            styles.ttStyle.apply(eff)
            legend = "other"


        EfficiencyList.append(histograms.HistoGraph(eff, legend, "lp", "P"))
            
    saveName = "Eff_"+numPath.split("/")[-1]+"Over"+denPath.split("/")[-1]
    if "Pt" in numPath:
        xMin = 0.0
#        rebinX = 2
        xMax = 705.0
        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Efficiency / "   + str(binwidth) + units
        yMin = 0.0
        yMax = 1.1

    elif "_Eta" in numPath:
        xMin = -3.0
        xMax = +3.0
        xTitle = "#eta"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 1.1

    elif "_Mass" in numPath:
        xMin = 50.0
        xMax = 300
        xTitle = "M (GeV/c^{2})"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 1.1

    elif "_Phi" in numPath:
        xMin = -3
        xMax = +3
        xTitle = "#phi"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 1.1

    else:
        xMin = 0.0
        xMax = 250.0
        xTitle = "xTitle"
        yTitle = "yTitle"
        yMin = 0.0
        yMax = 1.1

    if "Fake" in numPath:
        xMin = 90.0
        xMax = 705.0
        xTitle = "p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Misid rate / "  + str(binwidth) + units
        yMin = 0.0
        yMax = 0.11

    if "Event" in numPath:
        xMin = 95.0
        xMax = 705.0
        xTitle = "candidate p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Efficiency  / "  + str(binwidth) + " "+ units
        yMin = 0.0
        yMax = 1.1
        
    if "NonMatched" in numPath:
        xMin = 90.0
        xMax = 700.0
        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} (GeV)"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 0.15

    if "AllTopQuarkPt_MatchedBDT" in numPath and "TopQuarkPt" in denPath:
        xMin = 5.0
        xMax = 705.0
        xMax = 555.0 # For topPt < 500GeV
        units = "GeV/c"
        xTitle = "generated top p_{T} (GeV/c)"
        yTitle = "Efficiency / "  + str(binwidth) + units
        yMin = 0.0
        yMax = 1.1

    if "SameFake" in numPath:
        xMin = 95.0
        xMax = 705.0
        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} [GeV]"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 1.1


    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}

#    if "TT" in datasetName and ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#        return
#    if "M_"  in datasetName and not ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#        return

    p = plots.PlotBase(datasetRootHistos=EfficiencyList, saveFormats=kwargs.get("saveFormats"))

    #p = plots.ComparisonManyPlot(refEff, EfficiencyList, saveFormats=[])
    
    p.createFrame(saveName, opts=options)

#    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))

     # Set Titles                                                                                                                                                                                                
#    p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))  #"ylabel"
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)
    
    # Set range
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
    
    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                                                                                                                                                
    histograms.addStandardTexts()

    p.draw()

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, "HplusMasses", numPath.split("/")[0], opts.optMode)
    save_path = savePath + opts.MVAcut

#    SavePlot(p, saveName, savePath)
    SavePlot(p, saveName, save_path)
    return


# ---------------------------------------
#   Convert to TGraph
# ---------------------------------------

def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()
    for i in range(1,n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        # ugly hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
    return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                  array.array("d",y),
                                  array.array("d",xerrl),
                                  array.array("d",xerrh),
                                  array.array("d",yerrl),
                                  array.array("d",yerrh))

# ------------------------------------------------
#    Plot Histograms
# ------------------------------------------------
def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}

    if "Pt" in histo:
        _rebinX = 1
    elif "ChiSqr" in histo:
        _rebinX = 1
        logY    = True
        _units  = ""
        _format = "%0.1f " + _units
        _xlabel = "#chi^{2}"
        _cutBox = {"cutValue": 10.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 100
    
    if "_Mass" in histo:
        _opts["xmin"] = 140
        _opts["xmax"] = 220
    elif "trijetmass" in histo.lower():
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 805 #1005
    elif "ht" in histo.lower():
        logY    = False
        _units  = "GeV"
        _format = "%0.0f " + _units
        _xlabel = "H_{T} (%s)" % _units
        _cutBox = {"cutValue": 500, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        #_opts["xmin"] = 500
        _opts["xmax"] = 2000
    elif "tetrajetmass" in histo.lower():
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500 #3500.0
        #_rebinX = 10
        #_opts["xmax"] = 3500
    elif "tetrajetbjetpt" in histo.lower():
        logY    = False
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T}  (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 600
    elif "foxwolframmoment" in histo.lower():
        _format = "%0.1f"
        _cutBox = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    else:
        pass

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
        p.histoMgr.setHistoDrawStyle("TT", "AP")
        p.histoMgr.setHistoLegendStyle("TT", "LP")

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))

    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
    SavePlot(p_eff, saveName, savePath) 
    return



def Get2DRectangularSignificance(signal_dataset, background_dataset, histoName):
    SignalName = signal_dataset.getName()
    BackgroundName = background_dataset.getName()
    print "Signal = ", SignalName
    print "Background = ", BackgroundName

    #statOption = ROOT.TEfficiency.kFNormal
    sig = signal_dataset.getDatasetRootHisto(histoName)
    sig.normalizeToLuminosity(intLumi)
#    sig.normalizeByCrossSection() #fixme
    h_Signal = sig.getHistogram()
    
    bkg = background_dataset.getDatasetRootHisto(histoName)
    bkg.normalizeToLuminosity(intLumi)
#    bkg.normalizeByCrossSection() #fixme
    h_Background = bkg.getHistogram()
    
    significancePlots =[]
    maxSignXvalues = []
    windowOpeningValues = []
    x=[]
    y=[]
    z=[]
    
    maxSignY = 0
    maxSignX = 0
    maxSignZ = 0

#    cutvalue = 3.25
    my_range = []
#    for i in range(1,145):
#        my_range.append(cutvalue)
#        cutvalue = cutvalue - 0.25


    x_bins = h_Signal.GetXaxis().GetNbins()
    y_bins = h_Signal.GetYaxis().GetNbins()

    i = 1
    while i < x_bins+1:
        my_range.append(i)
        i = i + 1
        
    xmin = h_Signal.GetXaxis().GetBinLowEdge(1)+0.5*h_Signal.GetXaxis().GetBinWidth(1)
    xmax = h_Signal.GetXaxis().GetBinLowEdge(x_bins)+0.5*h_Signal.GetXaxis().GetBinWidth(x_bins)
    ymin = h_Signal.GetXaxis().GetBinLowEdge(1)+0.5*h_Signal.GetXaxis().GetBinWidth(1)
    ymax = h_Signal.GetXaxis().GetBinLowEdge(y_bins)+0.5*h_Signal.GetXaxis().GetBinWidth(y_bins)


    for xcut in my_range:
        for ycut in my_range:
   
            signal_total = h_Signal.Integral(1, x_bins, 1, y_bins)
            background_total = h_Background.Integral(1, x_bins, 1, y_bins)

            signal_fail = h_Signal.Integral(xcut, x_bins, 0, ycut)
            background_fail = h_Background.Integral(xcut, x_bins, 0, ycut)

            signal_pass = signal_total - signal_fail
            background_pass = background_total - background_fail

            significance = float(signal_pass)/math.sqrt(float(background_pass+signal_pass))
            #print significance
                                                         
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
            
                #print "pass", signal_pass, background_pass, significance
                #print "fail", signal_fail, background_fail, xcut, ycut
                #print "cuts", h_Signal.GetXaxis().GetBinLowEdge(xcut)+0.5*h_Signal.GetXaxis().GetBinWidth(xcut), h_Signal.GetXaxis().GetBinLowEdge(ycut)+0.5*h_Signal.GetXaxis().GetBinWidth(ycut), significance
            x.append(xcut)
            y.append(ycut)
            z.append(significance)
            
            #print significance

            if (significance > maxSignZ):
                maxSignY = h_Signal.GetXaxis().GetBinLowEdge(ycut)+0.5*h_Signal.GetXaxis().GetBinWidth(ycut)
                maxSignX = h_Signal.GetXaxis().GetBinLowEdge(xcut)+0.5*h_Signal.GetXaxis().GetBinWidth(xcut)
                maxSignZ = significance
                
                 # Create the Significance Plot                                                                                                            \
                                                                                                                                                
    #tGraph = ROOT.TGraph(len(x_values), array.array("d", x_values), array.array("d", y_values))

     # Customize the Significance Plot                                                                                                         \
                                                                                                                                                
     #ytitle = "S/ #sqrt{B} "
     #styleDict[signal_dataset.getName()].apply(tGraph)
     #tGraph.SetName(signal_dataset.getName())
     #tGraph.GetYaxis().SetTitle( ytitle + " /10" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                        
     #tGraph.GetXaxis().SetTitle("Cut window opening")#h_signal.GetXaxis().GetTitle())                                                           
     #                                                                                                                                         \
                                                                                                                                                
     #significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)



     #return significanceGraph, maxSignX

    hSignif = ROOT.TH2D("Signif", "Signif", x_bins, xmin, xmax, y_bins, ymin, ymax)
        
    for i in x:
        hSignif.Fill(x[i], y[i], z[i])

    return maxSignY, maxSignX, maxSignZ, hSignif



def HasKeys(keyList, **kwargs):                                                                                                                                                                                        
    for key in keyList:                                                                                                                                                                                                
        if key not in kwargs:                                                                                                                                                                                         
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return





def GetRectangularSignificance(signal_dataset, background_dataset, histoName):
    HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
    drawStyle    = kwargs.get("drawStyle")
    legStyle     = kwargs.get("legStyle")
    legName      = plots._legendLabels[signal_dataset.getName()]
    
    SignalName = signal_dataset.getName()
    BackgroundName = background_dataset.getName()
    print "Signal = ", SignalName
    print "Background = ", BackgroundName

    #statOption = ROOT.TEfficiency.kFNormal
    sig = signal_dataset.getDatasetRootHisto(histoName)
    sig.normalizeToLuminosity(intLumi)
#    sig.normalizeByCrossSection() #fixme
    h_Signal = sig.getHistogram()
    
    bkg = background_dataset.getDatasetRootHisto(histoName)
    bkg.normalizeToLuminosity(intLumi)
#    bkg.normalizeByCrossSection() #fixme
    h_Background = bkg.getHistogram()
    
    significancePlots =[]
    maxSignXvalues = []
    windowOpeningValues = []
    x=[]
    y=[]
    
    maxSignY = 0
    maxSignX = 0

#    cutvalue = 3.25
    my_range = []
#    for i in range(1,145):
#        my_range.append(cutvalue)
#        cutvalue = cutvalue - 0.25


    x_bins = h_Signal.GetXaxis().GetNbins()
    y_bins = h_Signal.GetYaxis().GetNbins()

    i = 1
    while i < x_bins+1:
        my_range.append(i)
        i = i + 1
        
    xmin = h_Signal.GetXaxis().GetBinLowEdge(1)+0.5*h_Signal.GetXaxis().GetBinWidth(1)
    xmax = h_Signal.GetXaxis().GetBinLowEdge(x_bins)+0.5*h_Signal.GetXaxis().GetBinWidth(x_bins)
    ymin = h_Signal.GetYaxis().GetBinLowEdge(1)+0.5*h_Signal.GetYaxis().GetBinWidth(1)
    ymax = h_Signal.GetYaxis().GetBinLowEdge(y_bins)+0.5*h_Signal.GetYaxis().GetBinWidth(y_bins)

    print "min, max ", xmin, xmax, ymin, ymax
    for xcut in my_range:
        
        signal_total = h_Signal.Integral(1, x_bins, 1, x_bins)
        background_total = h_Background.Integral(1, x_bins, 1, y_bins)
        
        signal_fail = h_Signal.Integral(xcut, x_bins, 1, xcut)
        background_fail = h_Background.Integral(xcut, x_bins, 1, xcut)
        
        signal_pass = signal_total - signal_fail
        background_pass = background_total - background_fail
        
        #significance = float(signal_pass)/math.sqrt(float(background_pass+signal_pass))
            #print significance
        
        if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
            significance = 0
        else:
            significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
            
                #print "pass", signal_pass, background_pass, significance
                #print "fail", signal_fail, background_fail, xcut, ycut
                #print "cuts", h_Signal.GetXaxis().GetBinLowEdge(xcut)+0.5*h_Signal.GetXaxis().GetBinWidth(xcut), h_Signal.GetXaxis().GetBinLowEdge(ycut)+0.5*h_Signal.GetXaxis().GetBinWidth(ycut), significance

        x.append(h_Signal.GetXaxis().GetBinLowEdge(xcut)+0.5*h_Signal.GetXaxis().GetBinWidth(xcut))
        y.append(significance)
        print "SIGN FULL",  float(signal_total)/math.sqrt(float(background_total + signal_total))
        
        if (significance > maxSignY):
            maxSignY = significance
            maxSignX = h_Signal.GetXaxis().GetBinLowEdge(xcut)+0.5*h_Signal.GetXaxis().GetBinWidth(xcut)

                
                 # Create the Significance Plot                                                                                                          
                 # Create the Significance Plot                                                                                                                                                                            
    tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))

          # Customize the Significance Plot                                                                                                                                                                             
    ytitle = "S/ #sqrt{B+S}"
    styleDict[signal_dataset.getName()].apply(tGraph)
    tGraph.SetName(signal_dataset.getName())
    tGraph.GetYaxis().SetTitle( ytitle + " /20" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                                                                           
    tGraph.GetXaxis().SetTitle(h_Signal.GetXaxis().GetTitle())#h_signal.GetXaxis().GetTitle())                                                                                                                    
          #                                                                                                                                                                                                          
    significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
    significancePlots.append(significanceGraph)
    
    if (1):
        xMin =xmin
#        rebinX = 2                                                                                                                                                                                                    
        xMax = xmax
        xTitle = "#Delta#phi(Top, b^{ldg}_{free})"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
#        print "binw", binwidth
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax = maxSignY + 0.5

    
    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
    p = plots.PlotBase(datasetRootHistos=significancePlots, saveFormats=kwargs.get("saveFormats"))
    saveName = "Signif_"+histoName.split("/")[-1]
    p.createFrame(saveName, opts=options)
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)

    # Set range                                                                                                                                                                                                       
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
    
    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add Standard Texts to plot                                                                                                                                                                                        
    histograms.addStandardTexts()
    
    p.draw()

    # Save plot in all formats                                                                                                                                                                                          
    savePath = os.path.join(opts.saveDir, "HplusMasses", histoName.split("/")[0], opts.optMode)
#    save_path = savePath + opts.MVAcut
    
#    SavePlot(p, saveName, savePath)                                                                                                                                                                                    
    SavePlot(p, saveName, savePath)


#    significancePlots.append(significanceGraph)
#    maxSignXvalues.append(maxSignX)

    return maxSignX, maxSignY, significanceGraph
                                             


def set_range(start, end, step):
     while start <= end:
          yield start
          start += step


#=======
def GetCircularSignificance(signals, background_dataset, histoName, intLumi):
    significancePlots = []
    efficiencyPlots   = []
#    signals.append(background_dataset)
    sig_eff =[]
    bkg_eff =[]
    r_ = []
    name_ = []
    signif_ = []
    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()

        print "==========================="
        print "Signal = ", SignalName
        print "Background = ", BackgroundName
        print "==========================="

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()


        sig = signal_dataset.getDatasetRootHisto(histoName)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoName)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        x=[]
        y=[]
#        xeff=[]
#        yeff=[]
        
        maxSignY = 0
        maxSignX = 0
        maxSelected_signal = 0
        maxSelected_background = 0
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass     +=  sigContent
                        background_pass +=  bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
                

            if (R < 0.9):
                sig_eff.append(float(signal_pass)/float(signal_total))
                bkg_eff.append(float(background_pass)/float(background_total))
                r_.append(R)
                signif_.append(significance)
                SignalName1 = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
                name_.append(SignalName1)
#                print "Signal Efficiency at",     round(R,2), ": ", round(float(signal_pass)/float(signal_total), 3)
#                print "Background Efficiency at", round(R,2), ": ", round(float(background_pass)/float(background_total), 3)
#                print "Significance at",            round(R,2), ": ", round(significance, 3)

            if "M_" in SignalName:
                x.append(R)
                y.append(significance)
            else:
                x.append(-1)
                y.append(-1)

#            xeff.append(R)
#            yeff.append(float(signal_pass)/float(signal_total))
            #print float(signal_pass)/float(signal_total)
            #print significance

            if (significance > maxSignY):
                maxSignY = significance
                maxSignX = R        
                maxSelected_signal = signal_pass
                maxSelected_background = background_pass

    # Create the Significance Plot                                                                   
        tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
#        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))

    # Customize the Significance Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        else:
            styles.ttStyle.apply(tGraph)
            legend = "other"


    # Customize the Efficiency Plot                                                                                                   
#        if "M_500" in SignalName:
#            styles.signalStyleHToTB500.apply(tGraph_eff)
#            legend = "H^{+} m_{H^{+}} = 500 GeV"
#        elif "M_300" in SignalName:
#            styles.signalStyleHToTB300.apply(tGraph_eff)
#            legend = "H^{+} m_{H^{+}} = 300 GeV"
#        elif "M_1000" in SignalName:
#            styles.signalStyleHToTB1000.apply(tGraph_eff)
#            legend = "H^{+} m_{H^{+}} = 1000 GeV"
#        elif "M_800" in SignalName:
#            styles.signalStyleHToTB800.apply(tGraph_eff)
#            legend = "H^{+} m_{H^{+}} = 800 GeV"
#        elif "M_200" in SignalName:
#            styles.signalStyleHToTB200.apply(tGraph_eff)
#            legend = "H^{+} m_{H^{+}} = 200 GeV"
#        else:
#            styles.ttStyle.apply(tGraph_eff)
#            legend = "other"



        tGraph.SetLineWidth(1)
        tGraph.SetMarkerSize(1)
#        tGraph_eff.SetLineWidth(1)
#        tGraph_eff.SetMarkerSize(1)

        significanceGraph = histograms.HistoGraph(tGraph, legName, "lp", drawStyle)
#        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)
#        significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
        if "M_" in SignalName:
            significancePlots.append(significanceGraph)
#        efficiencyPlots.append(efficiencyGraph)
#        significancePlots.append(histograms.HistoGraph(tGraph, legName, "lp", "P"))
        print "maximum Significance at ",        round(maxSignX,2),  ": ",round(maxSignY, 3)
        print "Maximum Signal Efficiency: ",     round(float(maxSelected_signal)/float(signal_total), 3)
        print "Maximum Background Efficiency: ", round(float(maxSelected_background)/float(background_total), 3)
    
    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
#        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax = maxSignY + 0.5
 #       yMax_eff = 1.0
        
    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
#    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    p = plots.PlotBase(datasetRootHistos=significancePlots, saveFormats=kwargs.get("saveFormats"))
#    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))
    saveName = "Signif_"+histoName.split("/")[-1]
#    saveName_eff = "Eff_"+histoName.split("/")[-1]

    p.createFrame(saveName, opts=options)
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)

#    p_eff.createFrame(saveName_eff, opts=options_eff)
#    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
#    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
#    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)

#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
#    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p.draw()
#    p_eff.draw()
    k=0
    txtAlign = "{:>20} {:>20} {:2} {:>20} {:5}"
    
    j=0
    while j < 9:
        print "\hspace{0.5cm} $R_{\Delta\phi}$ = ", round(r_[j],1), " - Background Efficiency: ", round(bkg_eff[j], 3)
        print txtAlign.format("$m_{H^{\pm}} (GeV/c^{2})$", "significance", "&", "signal efficiency", "\\")
        i = j
        while i < len(sig_eff): 
#        for i in set_range(j, len(sig_eff), 9):
            print txtAlign.format(name_[i], "%0.3f" % (signif_[i]), "&", "%0.3f" % (sig_eff[i]), "\\" )
            i+=9
        j+=1

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoName.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath)
#    SavePlot(p_eff, saveName_eff, savePath)
    
    return maxSignX, maxSignY, significancePlots #significanceGraph
#======





def GetCircularEfficiency(signals, background_dataset, histoName, intLumi):
    efficiencyPlots   = []
    signals.append(background_dataset)

    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()


        sig = signal_dataset.getDatasetRootHisto(histoName)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoName)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        xeff=[]
        yeff=[]
        
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))


        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
            
            efficiency = signal_pass/signal_total

            xeff.append(R)
            yeff.append(efficiency)

    # Create the Significance Plot                                                                   
        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))


    # Customize the Efficiency Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        elif "TT" in SignalName:
            styles.ttStyle.apply(tGraph_eff)            
            legend = "TT"
        else:
            styles.ttStyle.apply(tGraph_eff)
            legend = "other"

        if "M_" in SignalName:
            tGraph_eff.SetLineWidth(1)
            tGraph_eff.SetMarkerSize(1)
        else:
            tGraph_eff.SetLineWidth(2)
            tGraph_eff.SetMarkerSize(1)
            

        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)

        efficiencyPlots.append(efficiencyGraph)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax_eff = 1.0 + 0.1
        
    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))

    saveName_eff = "Eff_"+histoName.split("/")[-1]

    p_eff.createFrame(saveName_eff, opts=options_eff)
    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p_eff.draw()

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoName.split("/")[0], opts.optMode)
    SavePlot(p_eff, saveName_eff, savePath)
    signals.remove(background_dataset)
    return
#======




def GetCircularSignificance_opp(signals, background_dataset, histoName, intLumi):
    significancePlots = []
    efficiencyPlots   = []
#    signals.append(background_dataset)
    sig_eff =[]
    bkg_eff =[]
    r_ = []
    name_ = []
    signif_ = []
    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()

        print "==========================="
        print "Signal = ", SignalName
        print "Background = ", BackgroundName
        print "==========================="

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()


        sig = signal_dataset.getDatasetRootHisto(histoName)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoName)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        x=[]
        y=[]
#        xeff=[]
#        yeff=[]
        
        maxSignY = 0
        maxSignX = 0
        maxSelected_signal = 0
        maxSelected_background = 0
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if (xvalue*xvalue + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass     +=  sigContent
                        background_pass +=  bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
                

            if (R < 0.9):
                sig_eff.append(float(signal_pass)/float(signal_total))
                bkg_eff.append(float(background_pass)/float(background_total))
                r_.append(R)
                signif_.append(significance)
                SignalName1 = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
                name_.append(SignalName1)
#                print "Signal Efficiency at",     round(R,2), ": ", round(float(signal_pass)/float(signal_total), 3)
#                print "Background Efficiency at", round(R,2), ": ", round(float(background_pass)/float(background_total), 3)
#                print "Significance at",            round(R,2), ": ", round(significance, 3)

            if "M_" in SignalName:
                x.append(R)
                y.append(significance)
            else:
                x.append(-1)
                y.append(-1)

#            xeff.append(R)
#            yeff.append(float(signal_pass)/float(signal_total))
            #print float(signal_pass)/float(signal_total)
            #print significance

            if (significance > maxSignY):
                maxSignY = significance
                maxSignX = R        
                maxSelected_signal = signal_pass
                maxSelected_background = background_pass

    # Create the Significance Plot                                                                   
        tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
#        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))

    # Customize the Significance Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        else:
            styles.ttStyle.apply(tGraph)
            legend = "other"


        tGraph.SetLineWidth(1)
        tGraph.SetMarkerSize(1)
#        tGraph_eff.SetLineWidth(1)
#        tGraph_eff.SetMarkerSize(1)

        significanceGraph = histograms.HistoGraph(tGraph, legName, "lp", drawStyle)
#        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)
#        significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
        if "M_" in SignalName:
            significancePlots.append(significanceGraph)
#        efficiencyPlots.append(efficiencyGraph)
#        significancePlots.append(histograms.HistoGraph(tGraph, legName, "lp", "P"))
        print "maximum Significance at ",        round(maxSignX,2),  ": ",round(maxSignY, 3)
        print "Maximum Signal Efficiency: ",     round(float(maxSelected_signal)/float(signal_total), 3)
        print "Maximum Background Efficiency: ", round(float(maxSelected_background)/float(background_total), 3)
    
    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
#        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax = maxSignY + 0.5
 #       yMax_eff = 1.0
        
    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
#    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    p = plots.PlotBase(datasetRootHistos=significancePlots, saveFormats=kwargs.get("saveFormats"))
#    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))
    saveName = "Signif_center0_"+histoName.split("/")[-1]
#    saveName_eff = "Eff_"+histoName.split("/")[-1]

    p.createFrame(saveName, opts=options)
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)

#    p_eff.createFrame(saveName_eff, opts=options_eff)
#    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
#    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
#    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)

#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
#    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p.draw()
#    p_eff.draw()
    k=0
    txtAlign = "{:>20} {:>20} {:2} {:>20} {:5}"
    
    j=0
    while j < 9:
        print "\hspace{0.5cm} $R_{\Delta\phi}$ = ", round(r_[j],1), " - Background Efficiency: ", round(bkg_eff[j], 3)
        print txtAlign.format("$m_{H^{\pm}} (GeV/c^{2})$", "significance", "&", "signal efficiency", "\\")
        i = j
        while i < len(sig_eff): 
#        for i in set_range(j, len(sig_eff), 9):
            print txtAlign.format(name_[i], "%0.3f" % (signif_[i]), "&", "%0.3f" % (sig_eff[i]), "\\" )
            i+=9
        j+=1

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoName.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath)
#    SavePlot(p_eff, saveName_eff, savePath)
    
    return maxSignX, maxSignY, significancePlots #significanceGraph
#======





def GetCircularEfficiency_opp(signals, background_dataset, histoName, intLumi):
    efficiencyPlots   = []
    signals.append(background_dataset)

    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()


        sig = signal_dataset.getDatasetRootHisto(histoName)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoName)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        xeff=[]
        yeff=[]
        
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))


        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if (xvalue*xvalue + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
            
            efficiency = signal_pass/signal_total

            xeff.append(R)
            yeff.append(efficiency)

    # Create the Significance Plot                                                                   
        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))


    # Customize the Efficiency Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        elif "TT" in SignalName:
            styles.ttStyle.apply(tGraph_eff)            
            legend = "TT"
        else:
            styles.ttStyle.apply(tGraph_eff)
            legend = "other"

        if "M_" in SignalName:
            tGraph_eff.SetLineWidth(1)
            tGraph_eff.SetMarkerSize(1)
        else:
            tGraph_eff.SetLineWidth(2)
            tGraph_eff.SetMarkerSize(1)
            

        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)

        efficiencyPlots.append(efficiencyGraph)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax_eff = 1.0 + 0.1
        
    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))

    saveName_eff = "Eff_center0_"+histoName.split("/")[-1]

    p_eff.createFrame(saveName_eff, opts=options_eff)
    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p_eff.draw()

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoName.split("/")[0], opts.optMode)
    SavePlot(p_eff, saveName_eff, savePath)
    signals.remove(background_dataset)
    return
#======



def GetCircularEfficiency_RealTetrajet(signals, background_dataset, histoNameSignal, histoNameBackground, intLumi):
    efficiencyPlots   = []
    signals.append(background_dataset)

    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()
        if "M_200" in SignalName:
            continue

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()

        if "M_" in SignalName:
            sig = signal_dataset.getDatasetRootHisto(histoNameSignal)
        else:
            sig = signal_dataset.getDatasetRootHisto(histoNameBackground)

        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoNameBackground)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        xeff=[]
        yeff=[]
        
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))

            efficiency = signal_pass/signal_total

            xeff.append(R)
            yeff.append(efficiency)

    # Create the Significance Plot                                                                   
        
        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))


    # Customize the Efficiency Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        elif "TT" in SignalName:
            styles.ttStyle.apply(tGraph_eff)            
            legend = "TT"
        else:
            styles.ttStyle.apply(tGraph_eff)
            legend = "other"

        if "M_" in SignalName:
            tGraph_eff.SetLineWidth(1)
            tGraph_eff.SetMarkerSize(1)
        else:
            tGraph_eff.SetLineWidth(2)
            tGraph_eff.SetMarkerSize(1)
            

        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)

        efficiencyPlots.append(efficiencyGraph)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0
        yMax_eff = 1.0 + 0.1
        
    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))

    saveName_eff = "Eff_"+histoNameSignal.split("/")[-1]

    p_eff.createFrame(saveName_eff, opts=options_eff)
    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p_eff.draw()

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoNameSignal.split("/")[0], opts.optMode)
    SavePlot(p_eff, saveName_eff, savePath)
    signals.remove(background_dataset)
    return





def GetCircularEfficiency_RealTetrajet_opp(signals, background_dataset, histoNameSignal, histoNameBackground, intLumi):
    efficiencyPlots   = []
    signals.append(background_dataset)

    for signal_dataset in signals:
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName = signal_dataset.getName()
        BackgroundName = background_dataset.getName()
        if "M_200" in SignalName:
            continue

#        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        d = dataset.getDatasetRootHisto(denPath).getHistogram()

        if "M_" in SignalName:
            sig = signal_dataset.getDatasetRootHisto(histoNameSignal)
        else:
            sig = signal_dataset.getDatasetRootHisto(histoNameBackground)

        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(histoNameBackground)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        #h_Signal = signal_dataset.getDatasetRootHisto(histoName).getHistogram()
        #h_Background = background_dataset.getDatasetRootHisto(histoName).getHistogram()
        
        windowOpeningValues = []
        
        xeff=[]
        yeff=[]
        
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinLowEdge(1)
        xmax = h_Signal.GetXaxis().GetBinUpEdge(x_bins)
        ymin = h_Signal.GetYaxis().GetBinLowEdge(1)
        ymax = h_Signal.GetYaxis().GetBinUpEdge(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if (xvalue*xvalue + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))

            efficiency = signal_pass/signal_total

            xeff.append(R)
            yeff.append(efficiency)

    # Create the Significance Plot                                                                   
        
        tGraph_eff = ROOT.TGraph(len(xeff), array.array("d", xeff), array.array("d", yeff))


    # Customize the Efficiency Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph_eff)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        elif "TT" in SignalName:
            styles.ttStyle.apply(tGraph_eff)            
            legend = "TT"
        else:
            styles.ttStyle.apply(tGraph_eff)
            legend = "other"

        if "M_" in SignalName:
            tGraph_eff.SetLineWidth(1)
            tGraph_eff.SetMarkerSize(1)
        else:
            tGraph_eff.SetLineWidth(2)
            tGraph_eff.SetMarkerSize(1)
            

        efficiencyGraph = histograms.HistoGraph(tGraph_eff, legName, "lp", drawStyle)

        efficiencyPlots.append(efficiencyGraph)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yTitle_eff = "Efficiency / "   + str(round(binwidth, 2)) + units
        yMin = 0
        yMax_eff = 1.0 + 0.1
        
    options_eff = {"ymin": yMin  , "ymax": yMax_eff, "xmin":xMin, "xMax":xMax}

    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p_eff = plots.PlotBase(datasetRootHistos=efficiencyPlots, saveFormats=kwargs.get("saveFormats"))

    saveName_eff = "Eff_center0_"+histoNameSignal.split("/")[-1]

    p_eff.createFrame(saveName_eff, opts=options_eff)
    p_eff.getFrame().GetXaxis().SetTitle(xTitle)
    p_eff.getFrame().GetYaxis().SetTitle(yTitle_eff)
    
    # Set range                                                                                                                                                                                                       
    p_eff.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p_eff.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p_eff.draw()

    savePath = os.path.join(opts.saveDir, "HplusMasses", histoNameSignal.split("/")[0], opts.optMode)
    SavePlot(p_eff, saveName_eff, savePath)
    signals.remove(background_dataset)
    return








def GetCircularSignificance_RealTetrajet(signals, background_dataset, hName_real, hName_total, intLumi):
    significancePlots =[]
    sig_eff =[]
    bkg_eff = []
    r_ = []
    signif_ = []
    name_ = []

    for signal_dataset in signals:        
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName     = signal_dataset.getName()
        BackgroundName = background_dataset.getName()
        if "M_200" in SignalName:
            continue
        if "TT" in SignalName:
            continue

        print "Signal = ",     SignalName
        print "Background = ", BackgroundName
        
        sig = signal_dataset.getDatasetRootHisto(hName_real)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(hName_total)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        windowOpeningValues = []
        
        x=[]
        y=[]
        
        maxSignY = 0
        maxSignX = 0
        maxSelected_signal = 0
        maxSelected_background = 0
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinCenter(1)
        xmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        ymin = h_Signal.GetYaxis().GetBinCenter(1)
        ymax = h_Signal.GetYaxis().GetBinCenter(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
                

            if (R < 0.9):
                sig_eff.append(float(signal_pass)/float(signal_total))
                bkg_eff.append(float(background_pass)/float(background_total))
                r_.append(R)
                signif_.append(significance)
                SignalName1 = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
                name_.append(SignalName1)

            x.append(R)
            y.append(significance)
            
            #print significance

            if (significance > maxSignY):
                maxSignY = significance
                maxSignX = R        
                maxSelected_signal = signal_pass
                maxSelected_background = background_pass

    # Create the Significance Plot                                                                   
        tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))

    # Customize the Significance Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        else:
            styles.ttStyle.apply(tGraph)
            legend = "other"

        tGraph.SetLineWidth(1)
        tGraph.SetMarkerSize(1)
        significanceGraph = histograms.HistoGraph(tGraph, legName, "lp", drawStyle)
#        significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
        significancePlots.append(significanceGraph)
#        significancePlots.append(histograms.HistoGraph(tGraph, legName, "lp", "P"))
        print "==========="
        print "Real Hplus:"
        print "==========="
        print "maximum Significance at ",        round(maxSignX,2),  ": ",round(maxSignY, 3)
        print "Maximum Signal Efficiency: "    , round(float(maxSelected_signal)/float(signal_total), 3)
        print "Maximum Background Efficiency: ", round(float(maxSelected_background)/float(background_total), 3)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax = maxSignY + 0.1
        logY = True
        
    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p = plots.PlotBase(datasetRootHistos=significancePlots, saveFormats=kwargs.get("saveFormats"))
    saveName = "Signif_"+hName_real.split("/")[-1]
    p.createFrame(saveName, opts=options)
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)
    
    # Set range                                                                                                                                                                                                       
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p.draw()

    k=0
    txtAlign = "{:>20} {:>20} {:2} {:>20} {:5}"
    
    j=0
    while j < 9:
        print "\hspace{0.5cm} $R_{\Delta\phi}$ = ", round(r_[j],1), " - Background Efficiency: ", round(bkg_eff[j], 3)
        print txtAlign.format("$m_{H^{\pm}} (GeV/c^{2})$", "significance", "&", "signal efficiency", "\\")
        i = j
        while i < len(sig_eff): 
#        for i in set_range(j, len(sig_eff), 9):
            print txtAlign.format(name_[i], "%0.3f" % (signif_[i]), "&", "%0.3f" % (sig_eff[i]), "\\" )
            i+=9
        j+=1

    savePath = os.path.join(opts.saveDir, "HplusMasses", hName_real.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath)
    return maxSignX, maxSignY, significancePlots #significanceGraph

#        maxSignXreal, maxSignYreal, hSignif_real = GetCircularSignificance_RealTetrajet(signals, backgroundTT_dataset, hName_real, hName_total)









def GetCircularSignificance_RealTetrajet_opp(signals, background_dataset, hName_real, hName_total, intLumi):
    significancePlots =[]
    sig_eff =[]
    bkg_eff = []
    r_ = []
    signif_ = []
    name_ = []

    for signal_dataset in signals:        
        HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
        drawStyle    = kwargs.get("drawStyle")
        legStyle     = kwargs.get("legStyle")
        legName      = plots._legendLabels[signal_dataset.getName()]

        SignalName     = signal_dataset.getName()
        BackgroundName = background_dataset.getName()
        if "M_200" in SignalName:
            continue
        if "TT" in SignalName:
            continue

        print "Signal = ",     SignalName
        print "Background = ", BackgroundName
        
        sig = signal_dataset.getDatasetRootHisto(hName_real)
        sig.normalizeToLuminosity(intLumi)
        h_Signal = sig.getHistogram()
        
        bkg = background_dataset.getDatasetRootHisto(hName_total)
        bkg.normalizeToLuminosity(intLumi)
        h_Background = bkg.getHistogram()
        
        windowOpeningValues = []
        
        x=[]
        y=[]
        
        maxSignY = 0
        maxSignX = 0
        maxSelected_signal = 0
        maxSelected_background = 0
        my_range = []
        
        x_bins = h_Signal.GetXaxis().GetNbins()
        y_bins = h_Signal.GetYaxis().GetNbins()
        
        i = 1
        while i < x_bins+1:
            my_range.append(i)
            i = i + 1
            
        xmin = h_Signal.GetXaxis().GetBinCenter(1)
        xmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        ymin = h_Signal.GetYaxis().GetBinCenter(1)
        ymax = h_Signal.GetYaxis().GetBinCenter(y_bins)
        
        Rmax = h_Signal.GetXaxis().GetBinCenter(x_bins)
        Rstep = (h_Signal.GetXaxis().GetBinCenter(2) - h_Signal.GetXaxis().GetBinCenter(1))

        for R in set_range(0, Rmax, Rstep):
            signal_pass = 0
            background_pass = 0
            for ycut in my_range:
                for xcut in my_range:
                    
                    xvalue = h_Signal.GetXaxis().GetBinCenter(xcut)
                    yvalue = h_Signal.GetYaxis().GetBinCenter(ycut)
                    
                    if (xvalue*xvalue + yvalue*yvalue >= R*R): 
                        sigContent = h_Signal.GetBinContent(xcut, ycut)
                        bkgContent = h_Background.GetBinContent(xcut, ycut)
                        if (sigContent < 0):
                            sigContent = 0
                        if (bkgContent < 0):
                            bkgContent = 0
                    #if ( (xvalue-xmax)*(xvalue-xmax) + yvalue*yvalue >= R*R): 
                        signal_pass  +=  sigContent
                        background_pass += bkgContent
            if (R==0):
                signal_total = signal_pass
                background_total = background_pass
           
            if ((float(background_pass) <= 1 ) or (float(signal_pass) <= 0)):
                significance = 0
            else:
                significance = float(signal_pass)/math.sqrt(float(background_pass + signal_pass))
                

            if (R < 0.9):
                sig_eff.append(float(signal_pass)/float(signal_total))
                bkg_eff.append(float(background_pass)/float(background_total))
                r_.append(R)
                signif_.append(significance)
                SignalName1 = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
                name_.append(SignalName1)

            x.append(R)
            y.append(significance)
            
            #print significance

            if (significance > maxSignY):
                maxSignY = significance
                maxSignX = R        
                maxSelected_signal = signal_pass
                maxSelected_background = background_pass

    # Create the Significance Plot                                                                   
        tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))

    # Customize the Significance Plot                                                                                                   
        if "M_500" in SignalName:
            styles.signalStyleHToTB500.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 500 GeV"
        elif "M_300" in SignalName:
            styles.signalStyleHToTB300.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 300 GeV"
        elif "M_1000" in SignalName:
            styles.signalStyleHToTB1000.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 1000 GeV"
        elif "M_800" in SignalName:
            styles.signalStyleHToTB800.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 800 GeV"
        elif "M_200" in SignalName:
            styles.signalStyleHToTB200.apply(tGraph)
            legend = "H^{+} m_{H^{+}} = 200 GeV"
        else:
            styles.ttStyle.apply(tGraph)
            legend = "other"

        tGraph.SetLineWidth(1)
        tGraph.SetMarkerSize(1)
        significanceGraph = histograms.HistoGraph(tGraph, legName, "lp", drawStyle)
#        significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
        significancePlots.append(significanceGraph)
#        significancePlots.append(histograms.HistoGraph(tGraph, legName, "lp", "P"))
        print "==========="
        print "Real Hplus:"
        print "==========="
        print "maximum Significance at ",        round(maxSignX,2),  ": ",round(maxSignY, 3)
        print "Maximum Signal Efficiency: "    , round(float(maxSelected_signal)/float(signal_total), 3)
        print "Maximum Background Efficiency: ", round(float(maxSelected_background)/float(background_total), 3)

    if (1):
        xMin = xmin - 0.1
        #rebinX = 2                                      
        xMax = xmax
        xTitle = "R_{#Delta#phi}"
        units = ""
        _format = "%0.1f" + units
        binwidth = h_Signal.GetXaxis().GetBinWidth(1)
        yTitle = "N_{S}/#sqrt{N_{S}+N_{B}} / "   + str(round(binwidth, 2)) + units
        yMin = 0.0
        yMax = maxSignY + 0.1
        logY = True
        
    options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
    SignalName = SignalName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "_")
    p = plots.PlotBase(datasetRootHistos=significancePlots, saveFormats=kwargs.get("saveFormats"))
    saveName = "Signif_center0_"+hName_real.split("/")[-1]
    p.createFrame(saveName, opts=options)
    p.getFrame().GetXaxis().SetTitle(xTitle)
    p.getFrame().GetYaxis().SetTitle(yTitle)
    
    # Set range                                                                                                                                                                                                       
    p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)
    
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    moveLegend = {"dx": -0.10, "dy": -0.01, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    
    # Add Standard Texts to plot                                     
    histograms.addStandardTexts()
    
    p.draw()

    k=0
    txtAlign = "{:>20} {:>20} {:2} {:>20} {:5}"
    
    j=0
    while j < 9:
        print "\hspace{0.5cm} $R_{\Delta\phi}$ = ", round(r_[j],1), " - Background Efficiency: ", round(bkg_eff[j], 3)
        print txtAlign.format("$m_{H^{\pm}} (GeV/c^{2})$", "significance", "&", "signal efficiency", "\\")
        i = j
        while i < len(sig_eff): 
#        for i in set_range(j, len(sig_eff), 9):
            print txtAlign.format(name_[i], "%0.3f" % (signif_[i]), "&", "%0.3f" % (sig_eff[i]), "\\" )
            i+=9
        j+=1

    savePath = os.path.join(opts.saveDir, "HplusMasses", hName_real.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath)
    return maxSignX, maxSignY, significancePlots #significanceGraph

#        maxSignXreal, maxSignYreal, hSignif_real = GetCircularSignificance_RealTetrajet(signals, backgroundTT_dataset, hName_real, hName_total)







def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/s/skonstan/", "http://home.fnal.gov/~skonstan/")
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
    ANALYSISNAME = "MyHplusAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [200, 500, 800, 2000]
#    SIGNALMASS   = [200, 300, 1000]
    SIGNALMASS   = [200, 300, 500, 1000]
#    SIGNALMASS   = [1000]
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/s/skonstan/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"
    MVACUT       = "MVA"
    LOGX         = False
    LOGY         = False
    LOGZ         = False
    INTLUMI      = -1.0
    NORM2ONE     = False
    NORM2XSEC    = False
    NORM2LUMI    = False
    DATASET      = "Data"

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


    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX,
                      help="Set x-axis to logarithm scale [default: %s]" % LOGX)
    
    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Set y-axis to logarithm scale [default: %s]" % LOGY)
    
    parser.add_option("--logZ", dest="logZ", action="store_true", default=LOGZ,
                      help="Set z-axis to logarithm scale [default: %s]" % LOGZ)

#    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
#                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--normalizeToOne", dest="normalizeToOne", action="store_true", default=NORM2ONE,
                      help="Normalise plot to one [default: %s]" % NORM2ONE)

    parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default=NORM2XSEC,
                      help="Normalise plot by cross-section [default: %s]" % NORM2XSEC)

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default=NORM2LUMI,
                      help="Normalise plot to luminosity [default: %s]" % NORM2LUMI)

    parser.add_option("--dataset", dest="dataset", default = DATASET,
                      help="Dataset to draw (only 1 allowed in 2D) [default: %s]" % (DATASET) )

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
