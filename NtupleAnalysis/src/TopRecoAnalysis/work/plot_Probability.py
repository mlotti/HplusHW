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
    "saveFormats"      : [".pdf", "png"],
    "xlabel"           : None,
    "ylabel"           : "Probability",#"Probability",
    "rebinX"           : 2,
    "rebinY"           : 2,
    "xlabelsize"       : None,
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : False,
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
    

def GetDatasetsFromDir_secondDir(opts):
    Verbose("Getting datasets")
    usemcrab = "MyHplusAnalysis_180201_TrainingDRQuarks08"
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([usemcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([usemcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([usemcrab],
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

        datasetsMgr1 = GetDatasetsFromDir_secondDir(opts)
        datasetsMgr1.updateNAllEventsToPUWeighted()
        datasetsMgr1.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        for d in datasetsMgr1.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr1.getDataset(d.getName()).setCrossSection(1.0)
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        plots.mergeRenameReorderForDataMC(datasetsMgr1) 
        
        # Determine integrated Lumi before removing data
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 0

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
            datasetsMgr1.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "TTZToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "TTTT" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "TT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr1.remove(filter(lambda name: "FakeBMeasurementTrijetMass" in name, datasetsMgr.getAllDatasetNames()))
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
        datasetsMgr1.selectAndReorder(datasetOrder)

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
        
        numerators   = [#"TopQuarkPt_InTopDirBDT",
                        #"AllTopQuarkPt_InTopDirBDT",
                        "AllTopQuarkPt_MatchedBDT",
                        #"TrijetNotInTopDirPt_BDT",
                        "TrijetFakePt_BDT",
                        #"AllTopQuarkPt_InTopDir",
                        "AllTopQuarkPt_Matched",
                        "EventTrijetPt2T_MatchedBDT",
                        "EventTrijetPt2T_MatchedBDT",
                        "EventTrijetPt2T_MatchedBDT",
                        #"AllTopQuarkPt_NotInTopDir",
                        #"EventTrijetPt_InTopDirBDT",
                        "AllTopQuarkPt_MatchedBDT",
                        #"TrijetPtMaxMVASameFakeObj_BjetPassCSV",
                        "SelectedTrijetsPt_BjetPassCSVdisc_afterCuts",
                        "TrijetPt_PassBDT_BJetPassCSV",
#                        "TopFromHiggsPt_isLdgMVATrijet_afterCuts",
#                        "TopFromHiggsPt_isSubldgMVATrijet_afterCuts",
#                        "TopFromHiggsPt_isMVATrijet_afterCuts",
#                        "LdgBjetPt_isLdgFreeBjet",
#                        "ChHiggsBjetPt_TetrajetBjetPt_Matched_afterCuts",
#                        "TopFromHiggsPt_notMVATrijet_afterCuts",
#                        "HiggsBjetPt_isTrijetSubjet_afterCuts",
                        ]
        denominators = [#"TrijetPt_BDT",
                        #"AllTopQuarkPt_InTopDir",
                        "AllTopQuarkPt_Matched",
                        #"TrijetNotInTopDirPt",
                        "TrijetFakePt",
                        #"TopQuarkPt",
                        "TopQuarkPt",
                        "EventTrijetPt2T_BDT",
                        "EventTrijetPt2T_Matched",
                        "EventTrijetPt2T",
                        #"TopQuarkPt",
                        #"EventTrijetPt_BDT",
                        "TopQuarkPt",
                        #"TrijetPtMaxMVASameFakeObj",
                        "SelectedTrijetsPt_afterCuts",
                        "TrijetPt_PassBDT",
#                        "TopFromHiggsPt_afterCuts",
#                        "TopFromHiggsPt_afterCuts",
#                        "TopFromHiggsPt_afterCuts",
#                        "LdgBjetPt",
#                        "ChHiggsBjetPt_foundTetrajetBjet_afterCuts",
#                        "TopFromHiggsPt_afterCuts",
#                        "HiggsBjetPt_afterCuts",
                        ]
        
        datasets  = datasetsMgr.getAllDatasets()
        datasets1 = datasetsMgr1.getAllDatasets()

        for dataset in datasets1:
            datasets.append(dataset)
        for i in range(len(numerators)):
            
#            PlotProb(datasetsMgr.getAllDatasets(), folder+"/"+numerators[i], folder+"/"+denominators[i])
            PlotProb(datasets, folder+"/"+numerators[i], folder+"/"+denominators[i])

        myHistoList = ["AllTopQuarkPt_MatchedBDT", "AllTopQuarkPt_Matched", "TrijetFakePt_BDT", "TrijetFakePt", "EventTrijetPt2T_MatchedBDT", "EventTrijetPt2T_BDT", "TopQuarkPt", "TrijetPt_BDT",
                       "LdgTrijetPt", "SubldgTrijetPt", "TopQuarkPt_BDT",]
        for i in range(len(myHistoList)):
            PlotMC(datasetsMgr, datasetsMgr1, folder+"/"+myHistoList[i], intLumi)


        folder     = "ForDataDrivenCtrlPlots"
        histoList  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folder)
        hList0     = [x for x in histoList if "TrijetMass" in x]
        hList1     = [x for x in histoList if "TetrajetMass" in x]
        hList2     = [x for x in histoList if "TetrajetBjetPt" in x]
        histoPaths2 = [os.path.join(folder, h) for h in hList0+hList1+hList2]

        '''
        histoPaths = histoPaths1 + histoPaths2
        for h in histoPaths:
            
            if "Vs" in h:                     # Skip TH2D
                continue
            PlotMC(datasetsMgr, h, intLumi)
            '''
    return


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
    index = 0
    for dataset in datasets:
        
        datasetName = dataset.getName()
        print "Dataset = ", datasetName
        
        
        statOption = ROOT.TEfficiency.kFNormal        
##        n = dataset.getDatasetRootHisto(numPath).getHistogram()
#        n.normalizeToOne()
##        d = dataset.getDatasetRootHisto(denPath).getHistogram()
        nn = dataset.getDatasetRootHisto(numPath)
        nn.normalizeToLuminosity(35.8*(10**3))
        n = nn.getHistogram()
        dd = dataset.getDatasetRootHisto(denPath)
#        dd.normalizeToOne()                                                                                                                                            
#        dd.normalizeToLuminosity(36.3*(10**3))
        dd.normalizeToLuminosity(35.8*(10**3))                                                                                                                                   
#        dd.normalizeByCrossSection()
        d = dd.getHistogram()


#        if "TT" in datasetName and ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#            continue
#        elif "M_"  in datasetName and not ("Higgs" in numPath or "LdgBjetPt_isLdgFreeBjet" in numPath):
#            continue
        
        if "Event" in numPath:
            n.Rebin(10)
            d.Rebin(10)
        else:
            n.Rebin(5)
            d.Rebin(5)
        
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
            if index == 0:
                styles.signalStyleHToTB500.apply(eff)
#            styles.ttStyle.apply(eff)
                eff.SetLineStyle(1)
                eff.SetLineWidth(3)
                eff.SetLineColor(619)
                legend = "Default: t#bar{t}"
                index = 1
            else:
                styles.signalStyleHToTB500.apply(eff)
                #            styles.ttStyle.apply(eff)
                eff.SetLineStyle(1)
                eff.SetLineWidth(3)
                eff.SetLineColor(417)
                legend = "#Delta R(q,q')>0.8: t#bar{t}"

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
        xMax = 805.0
#        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Efficiency / "   + str(binwidth) + " "+units
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
#        xMin = 95.0
#        rebinX = 4                                                                                                                                                  
        xMax = 805.0
        xTitle = "candidate p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Misid rate / "  + str(binwidth) + " " +units
        yMin = 0.0
        yMax = 0.11

    if "Event" in numPath:
        rebinX = 2
#        xMin = 95.0
        xMax = 805.0
        xTitle = "candidate p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.1f" + units
        yTitle = "Efficiency  / "  + str(binwidth) + " "+ units
        yMin = 0.0
        yMax = 1.1
        
    if "NonMatched" in numPath:
        xMin = 90.0
        rebinX = 4
        xMax = 700.0
        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} (GeV)"
        yTitle = "Efficiency"
        yMin = 0.0
        yMax = 0.15

    if "AllTopQuarkPt_MatchedBDT" in numPath and "TopQuarkPt" in denPath:
        xMin = 0.0
#        rebinX = 4
        xMax = 805.0 #705
        units = "GeV/c"
        xTitle = "generated top p_{T} (GeV/c)"
        yTitle = "Efficiency / "  + str(binwidth) + " " + units
        yMin = 0.0
        yMax = 1.1

    if "SameFake" in numPath:
        xMin = 95.0
        rebinX = 4
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
    
    
    moveLegend = {"dx": -0.55, "dy": -0.02, "dh": -0.2}
#    moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
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
def PlotMC(datasetsMgr, datasetsMgr1, histo, intLumi):

    kwargs = {}
    print "here1"
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[".pdf", "png"], **kwargs)
        p = plots.MCPlot(datasetsMgr1, histo, normalizeToOne=True, saveFormats=[".pdf", ".png"], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[".pdf", ".png"], **kwargs)
        p = plots.MCPlot(datasetsMgr1, histo, normalizeToOne=True, saveFormats=[".pdf", "png"], **kwargs)

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}
    print "here2"
    if "Pt" in histo:
        _rebinX = 2
        xMin = 0.0
#        rebinX = 2
        xMax = 805.0
#        xMax = 555.0 # For topPt < 500GeV
        xTitle = "p_{T} (GeV/c)"
        units = "GeV/c"
        _format = "%0.0f" + units
#        yTitle = "Efficiency / "   + str(binwidth) + " "+units
#        yMin = 0.0
#        yMax = 1.1


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

    print "here3"
    
    histoDef = datasetsMgr.getDataset("TT").getDatasetRootHisto(histo)
    histoDR = datasetsMgr1.getDataset("TT").getDatasetRootHisto(histo)

    histoDef.normalizeToOne()
    histoDR.normalizeToOne()

    hDef = histoDef.getHistogram()
    hDR = histoDR.getHistogram()

    p = plots.ComparisonPlot(histograms.Histo(hDR,"DeltaR08", "l", "L"),
                             histograms.Histo(hDef,"Default", "l", "L"))

    p.histoMgr.setHistoLegendLabelMany({"DeltaR08": "#DeltaR(q,q')>0.8",
                                        "Default": "Default"})

    p.histoMgr.forHisto("DeltaR08", styles.getQCDLineStyle() )
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
    p.histoMgr.setHistoDrawStyle("DeltaR08", "HIST") #HIST
    p.histoMgr.setHistoLegendStyle("DeltaR08", "L") #F

    p.histoMgr.setHistoDrawStyle("Default", "HIST") #HIST
    p.histoMgr.setHistoLegendStyle("Default", "L") #F

    p.histoMgr.forHisto("Default", styles.ttStyle)  

    print "here4"

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))
    print "here5"
    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.75, "x2": 0.92, "y2": 0.92},
#                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )
    print "here6"
    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath) 
    print "here7"
    return





#soti
def PlotMC_ForEffPlots(datasetsMgr, histoName, intLumi):

    index = 0
    for dataset in datasetsMgr.getAllDatasets():

        datasetName = dataset.getName()
        rootHisto = dataset.getDatasetRootHisto(histoName)
        rootHisto.normalizeToLuminosity(intLumi)
        histo = rootHisto.getHistogram()
        
        kwargs = {}

        
        if index == 0:
        # Apply Styles                                                                                                                                                                   
            if "TT" in datasetsMgr.getAllDatasets():
                p.histoMgr.setHistoDrawStyle("TT", "AP")
                p.histoMgr.setHistoLegendStyle("TT", "LP")
                index = 1
                
        else:
        # Apply Styles                                                                                                                                                                   
            if "TT" in datasetsMgr.getAllDatasets():
                p.histoMgr.setHistoDrawStyle("TTTT", "AP")
                p.histoMgr.setHistoLegendStyle("TTTT", "LP")
                
        _xlabel = "p_{T} (GeV/c)"
        logY = False
        _rebinX = 1
        units = "GeV/c"
        _format = "%0.1f" + units
        _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}
        _cutBox = False
#        _cutBox = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
 
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
    SavePlot(p, saveName, savePath)
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
    SIGNALMASS   = [300, 500, 1000]
    SIGNALMASS   = []
    INTLUMI      = -1.0
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
