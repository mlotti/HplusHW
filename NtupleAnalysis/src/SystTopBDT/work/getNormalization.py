#!/usr/bin/env python
'''
   DESCRIPTION:
   
   This script calculates the QCD & TT normalization factors.
   
   The phase space is devided in four regions:
   

    0.2 |--------|--------|--------
        |        |        |
        |  CR2   |        |  VR
    0.1 |--------|        |--------
        |        |        |
        |  CR1   |        |  SR
    0.0 |--------|--------|-------->
                20        50          
                
     - The QCD normalization factor (F1) is taken from a phase space with low MET < 20 GeV and high muon mini-isolation > 0.1 (Background region (CR2))
       
       QCD in Data:    Data_{BR} - EWK_{BR} - ST_{BR} - TT_{BR}
       QCD in MC:      QCD_{BR}
   
       F1 = QCD in Data / QCD in MC
       
     - The TT normalization factor (F2) is taken from a phase space with high MET > 50 GeV and low muon mini-isolation < 0.1 (Signal region (SR))
     
       TT in Data:    Data_{SR} - EWK_{SR} - ST_{SR} - F1*QCD_{SR}
       TT in MC:      TT_{SR}
       
       F2 = TT in Data / TT in MC
   
   USAGE:
   ./getNormalization.py -m <pseudo-multicrab> --url
    
   LAST USED:
   
   (1) ./getNormalization.py -m SystTopBDT_180528_151309_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   (2) ./getNormalization.py -m SystTopBDT_180528_151533_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   (3) ./getNormalization.py -m SystTopBDT_180528_152141_MET50_MuIso0p1_InvMET20_InvMuIso0p2_noSF -e "TTW|TTZ"
   (4) ./getNormalization.py -m SystTopBDT_180528_152310_MET40_MuIso0p1_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   (5) ./getNormalization.py -m SystTopBDT_180528_152540_MET30_MuIso0p1_InvMET15_InvMuIso0p2_noSF -e "TTW|TTZ"
   (6) ./getNormalization.py -m SystTopBDT_180528_152944_MET30_MuIso0p2_InvMET20_InvMuIso0p4_noSF -e "TTW|TTZ"
   (7) ./getNormalization.py -m SystTopBDT_180529_093052_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
   (8) ./getNormalization.py -m SystTopBDT_180529_165537_MET30_MuIso0p1_InvMET30_InvMuIso0p1_noSF -e "TTW|TTZ"
   (9) ./getNormalization.py -m SystTopBDT_180529_170402_MET30_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"   
   (10)./getNormalization.py -m SystTopBDT_180529_094433_MET30_MuIso0p1_InvMET15_InvMuIso0p1_noSF -e "TTW|TTZ"
   (11)./getNormalization.py -m SystTopBDT_180529_094647_MET50_MuIso0p2_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   (12)./getNormalization.py -m SystTopBDT_180529_094856_MET30_MuIso0p1_InvMET20_InvMuIso0p3_noSF -e "TTW|TTZ"x

   ./getNormalization.py -m SystTopBDT_180524_074141_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
   
   USED for AN plots:
   ./getNormalization.py -m SystTopBDT_180513_101101_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"

   Other selections:
   Selection A) ./getNormalization.py -m SystTopBDT_180513_100633_MET50_MuIso0p2_InvMET20_InvMuIso0p2_noSF -e "TTW|TTZ"
   Selection C) ./getNormalization.py -m SystTopBDT_180513_101634_MET50_MuIso0p2_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   Selection D) ./getNormalization.py -m SystTopBDT_180513_102112_MET50_MuIso0p1_InvMET30_InvMuIso0p1_noSF -e "TTW|TTZ" 
   Selection E) ./getNormalization.py -m SystTopBDT_180514_110341_MET40_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
   Selection F) ./getNormalization.py -m SystTopBDT_180514_115524_MET40_MuIso0p1_InvMET30_InvMuIso0p1_noSF -e "TTW|TTZ"
   Selection G) ./getNormalization.py -m SystTopBDT_180514_115629_MET30_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
   Selection H) ./getNormalization.py -m SystTopBDT_180517_102420_MET40_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
   Selection I) ./getNormalization.py -m SystTopBDT_180517_102638_MET30_MuIso0p1_InvMET20_InvMuIso0p2_noSF -e "TTW|TTZ"
   Selection J) ./getNormalization.py -m SystTopBDT_180517_102808_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
   Selection K) ./getNormalization.py -m SystTopBDT_180517_174526_TopDir_noSF -e "TTW|TTZ"
'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
from optparse import OptionParser

import getpass

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
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
# Ignore Runtime warnings: Base category for warnings about dubious runtime features.
import warnings
warnings.filterwarnings("ignore")

ROOT.gErrorIgnoreLevel = ROOT.kError

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


def GetHistoKwargs(h, opts):
    _moveLegend =  {"dx": -0.13, "dy": -0.02, "dh": -0.12}
    logY    = True
    _yLabel = "Events / %.0f "
    yMin    = 1e0
    if logY:
        yMaxF = 10
    else:
        yMaxF = 1.2

    _kwargs = {
        "ylabel"           : _yLabel,
        "rebinX"           : 1,
        "rebinY"           : None,
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioCreateLegend": True,
        "ratioType"        : "errorScale",
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.05},
        "stackMCHistograms": False, #not opts.nostack,
        "ratioInvert"      : False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": yMin, "ymaxfactor": yMaxF},
        "opts2"            : {"ymin": 0.59, "ymax": 1.41},
        "log"              : logY,
        "moveLegend"       : _moveLegend,
        }
    
    kwargs = copy.deepcopy(_kwargs)
    
    if "pt" in h.lower():
        units            = "(GeV/c)"
        kwargs["ylabel"] = _yLabel + units
        kwargs["xlabel"] = "p_{T}" + units
        kwargs["rebinX"] = 2
        
    return kwargs


def main(opts):
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(False)
    style.setGridY(False)
    
     # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        else:
            pass
        optModes = optList
    else:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt
        
        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() 
        
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            
        # Print dataset information before removing anything?
        if 1:
            datasetsMgr.PrintInfo()
            
        # Remove datasets
        filterKeys = ["TTW"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
            
        # Re-order datasets
        datasetOrder = []
        haveQCD = False
        for d in datasetsMgr.getAllDatasets():
            if "QCD" in d.getName():
                haveQCD = True
            datasetOrder.append(d.getName())
        datasetsMgr.selectAndReorder(datasetOrder)
        
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Merge EWK datasets
        EWKlist = ["WJetsHT", "DYJetsToLL", "Diboson"]
        datasetsMgr.merge("EWK", EWKlist)
        
        # Print dataset information after merging
        datasetsMgr.PrintInfo()
        
        # Determine integrated Lumi before removing data
        intLumi = datasetsMgr.getDataset('Data').getLuminosity()
        
        # Define Numerator & Denominator Histograms
        numerator_name   = "AfterAllSelections_LeadingTrijet_Pt"
        denominator_name = "AfterStandardSelections_LeadingTrijet_Pt" 
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folderListIncl = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        folderList = [h for h in folderListIncl if "AfterAllSelections_LeadingTrijet_Pt" in h ]
        
        folderPath = os.path.join(opts.folder, "")
        folderPathGen = os.path.join(opts.folder+"Genuine", "")
        folderPathFake =os.path.join(opts.folder+"Fake", "")
        
        histoList = folderList
        num_pathList = [os.path.join(folderPath, h) for h in histoList]
        num_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        num_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])
        
        for h in num_pathList:
            if "lowMET" in h:
                num_pathList.remove(h)

        histoList = [h for h in folderListIncl if "AfterStandardSelections_LeadingTrijet_Pt" in h]
        den_pathList = [os.path.join(folderPath, h) for h in histoList]
        den_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        den_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])
        
        for h in den_pathList:
            if "lowMET" in h:
                den_pathList.remove(h)
                
        # Calculate Scale Factors
        GetScaleFactors(datasetsMgr, num_pathList, den_pathList, intLumi)
        
        
    return


def CheckNegatives(hNum, hDen, verbose=False):
    '''
    Checks two histograms (numerator and denominator) bin-by-bin for negative contents.
    If such a bin is is found the content is set to zero.
    Also, for a given bin, if numerator > denominator they are set as equal.
    '''
    table    = []
    txtAlign = "{:<5} {:>20} {:>20}"
    hLine    = "="*50
    table.append(hLine)
    table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
    table.append(hLine)
    
    # For-loop: All bins in x-axis
    for i in range(1, hNum.GetNbinsX()+1):
        nbin = hNum.GetBinContent(i)
        dbin = hDen.GetBinContent(i)
        table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))
        
        # Numerator > Denominator
        if nbin > dbin:
            hNum.SetBinContent(i, dbin)

        # Numerator < 0 
        if nbin < 0:
            hNum.SetBinContent(i,0)
            
         # Denominator < 0
        if dbin < 0:
            hNum.SetBinContent(i,0)
            hDen.SetBinContent(i,0)
        return

    
def GetHistoKwargs_Efficiency(histoName, opts):
     '''                                                                                                                                                                                                                                                            
     Dictionary with                                                                                                                                                                                                                                                
     key   = histogram name                                                                                                                                                                                                                                         
     value = kwargs                                                                                                                                                                                                                                                 
     '''
     h = histoName.lower()
     kwargs     = {
         "xlabel"           : "x-axis",
         "ylabel"           : "Misidentification rate", #/ %.1f ",
         #"rebinX"           : 1,
         "ratioYlabel"      : "Data/MC",
         "ratio"            : False,
         "ratioInvert"      : False,
         "stackMCHistograms": False,
         "addMCUncertainty" : False,
         "addLuminosityText": False,
         "addCmsText"       : True,
         "cmsExtraText"     : "Preliminary",
         "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2},
         "opts2"            : {"ymin": 0.5, "ymax": 1.5},
         "log"              : False,
         "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": -0.18},
         "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
         }

     myBins  = []
     if "pt" in h:
         units   = "GeV/c"
         xlabel  = "p_{T} (%s)" % (units)
         myBins  = [0, 100, 200, 300, 400, 500, 600, 800]
         kwargs["xmax"] = 800
         kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

     kwargs["xlabel"]  = xlabel
     if units != "":
         kwargs["ylabel"] += (" / "+units)


     if len(myBins) > 0:
         kwargs["binList"] = array.array('d', myBins)
     return kwargs


def PlotEfficiency(datasetsMgr, num, den, intLumi):
     if 1:
         xBins   = array.array('d', [0, 100, 200, 300, 400, 500, 600, 800])
         nx      = len(xBins)-1
         num     = num.Rebin(nx, "", xBins)
         den     = den.Rebin(nx, "", xBins)

     # Sanity checks
     if den.GetEntries() == 0 or num.GetEntries() == 0:
         return#continue
     if num.Integral(0, num.GetXaxis().GetNbins()) > den.Integral(0, den.GetXaxis().GetNbins()):
         return

     # Create Efficiency plots with Clopper-Pearson stats
     eff = ROOT.TEfficiency(num, den)
     eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP 

     eff = convert2TGraph(eff)
     return eff


def RemoveNegatives(histo):
     '''
     Removes negative bins from histograms
     '''
     for binX in range(histo.GetNbinsX()+1):
         if histo.GetBinContent(binX) < 0:
             histo.SetBinContent(binX, 0.0)
     return

def GetHisto(datasetsMgr, dataset, hName, intLumi):
     n = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hName)
     n.normalizeToLuminosity(intLumi)
     histo = n.getHistogram()
     #histo.Rebin(2)
     return histo

def GetHistoPathDict(histoList, printList=False):

     histoDict = {}

     # For-loop: All histograms (full paths)
     for h in histoList:
         if "_SR" in h:
             region = "SR"
         elif "_VR" in h:
             region = "VR"
         elif "_CR1" in h:
             region = "CR1"
         elif "_CR2" in h:
             region = "CR2"
         else:
             raise Exception("Could not determine Control Region for histogram %s" % (h) )

         lIncl = "%s-%s" % (region, "Inclusive")
         lGen  = "%s-%s" % (region, "Genuine")
         lFake = "%s-%s" % (region, "Fake")

         if "Genuine" in h:
             histoDict[lGen] = h
         elif "Fake" in h:
             histoDict[lFake] = h
         else:
             histoDict[lIncl] = h

     # Create table of key->histogram mapping
     rows   = []
     align  = "{:<40} {:<80}"
     header = align.format("Key", "Full Path")
     hLine  = "="*120
     rows.append(hLine)
     rows.append(header)
     rows.append(hLine)
     for k in histoDict:
         rows.append(align.format(k, histoDict[k]))
     rows.append(hLine)
     rows.append("")

     if 1:
         for i, row in enumerate(rows, 1):
             Print(row, i==1)
     return histoDict

def GetHistosForEfficiency(hNumerator, hDenominator):

     hNum = hNumerator.Clone("Numerator")
     hDen = hDenominator.Clone("Denominator")
     hNum.Reset()
     hDen.Reset()

      # Debug                                                                                                                                                                                                         
     for i in range(0, hDenominator.GetNbinsX()+1):
         num    = hNumerator.GetBinContent(i)
         numErr = hNumerator.GetBinError(i)
         den    = hDenominator.GetBinContent(i)
         denErr = hDenominator.GetBinError(i)

         if num < 0:
             num    = 0.00001
             numErr = 0.000001

         if den == 0:
             den    = 0.00001
             denErr = 0.000001

         if num > den:
             num = den

         # Fill histos                                                                                                                                                                                               
         if 0:
             print "num: %s +/- %s" % (num, numErr)
             print "den: %s +/- %s" % (den, denErr)
             print

         hNum.SetBinContent(i, num)
         hNum.SetBinError(i, numErr)
         hDen.SetBinContent(i, den)
         hDen.SetBinError(i, denErr)
     return hNum, hDen



def GetRootHistos(datasetsMgr, histo, regions):

    # Definitions
    hPathDict = GetHistoPathDict( histo, printList=True)
    rhDict    = {}
    
     # For-loop: All Control Regions (CR)
    for region in regions:
        
        # Define labels
        lIncl = "%s-%s" % (region, "Inclusive")
        lGen  = "%s-%s" % (region, "Genuine")
        lFake = "%s-%s" % (region, "Fake")
        
        # Get the desired histograms
        pIncl = plots.DataMCPlot(datasetsMgr, hPathDict[lIncl])
        pGen  = plots.DataMCPlot(datasetsMgr, hPathDict[lGen])
        pFake = plots.DataMCPlot(datasetsMgr, hPathDict[lFake])
        
        # Get the desired histograms
        p = plots.DataMCPlot(datasetsMgr, hPathDict[lIncl])
             
        # TT
        rhDict["TT-"  + lIncl] = pIncl.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lIncl)
        rhDict["TT-"  + lGen ] = pGen.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lGen)
        rhDict["TT-"  + lFake] = pFake.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lFake)
        
        # EWK
        rhDict["EWK-" + lIncl] = pIncl.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK-" + lIncl)
        # QCD
        rhDict["QCD-" + lIncl] = pIncl.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-" + lIncl)
        # Data
        rhDict["Data-"+ lIncl] = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("Data-" + lIncl)
        # Single Top
        rhDict["SingleTop-" + lIncl] = pIncl.histoMgr.getHisto("SingleTop").getRootHisto().Clone("SingleTop-" + lIncl)
        
    return rhDict


def GetScaleFactors(datasetsMgr, num_pathList, den_pathList, intLumi):  

    # Get kwargs
    _kwargs = GetHistoKwargs(num_pathList[0], opts)        
    _kwargs["stackMCHistograms"] = False
    _kwargs["opts2"] = {"ymin": 0.50, "ymax": 1.50}
    _kwargs["ratioType"] = "errorScale"
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    
    # Get Dictionaries 
    rhDict_num = GetRootHistos(datasetsMgr, num_pathList, regions)
    rhDict_den = GetRootHistos(datasetsMgr, den_pathList, regions)

    # ----------------------------------------------------------------------------
    # Get the QCD in Data (Data - EWK - TT - Single Top) and MC in all regions
    # ----------------------------------------------------------------------------
    for re in regions:
        rhDict_den["QCDinData-"+re+"-Inclusive"] = rhDict_den["Data-"+re+"-Inclusive"].Clone("QCDinData-"+re+"-Inclusive")
        rhDict_den["QCDinData-"+re+"-Inclusive"].Add(rhDict_den["EWK-"+re+"-Inclusive"]       , -1)
        rhDict_den["QCDinData-"+re+"-Inclusive"].Add(rhDict_den["TT-"+re+"-Inclusive"]        , -1)
        rhDict_den["QCDinData-"+re+"-Inclusive"].Add(rhDict_den["SingleTop-"+re+"-Inclusive"] , -1)
        
    # ----------------------------------------------------------------------------
    # (1) Plot QCD (Data Vs MC) before any normalization in all regions
    # ----------------------------------------------------------------------------
    for re in regions:
        
        hName = "QCD_"+re+"_Before_Normalization"
        
        h0 = rhDict_den["QCDinData-"+re+"-Inclusive"].Clone("QCD (Data)")
        h1 = rhDict_den["QCD-"+re+"-Inclusive"].Clone("QCD (MC)")

        # Get Histos
        h_QCDinData = histograms.Histo( h0, "QCD (Data)", "Data");  h_QCDinData.setIsDataMC(isData=True, isMC=False)
        h_QCDinMC   = histograms.Histo( h1, "QCD (MC)", "MC");      h_QCDinMC.setIsDataMC(isData=False, isMC=True)
        
        # Create plot
        pQCD = plots.ComparisonManyPlot(h_QCDinMC, [h_QCDinData], saveFormats=[])
        pQCD.setLuminosity(intLumi)
        pQCD.setDefaultStyles()
        plots.drawPlot(pQCD, hName, **_kwargs)
        SavePlot(pQCD, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
        
        # Reset histograms
        h0.Reset()
        h1.Reset()
        
    # ------------------------------------------------------------------------------
    # (2) Find the normalization factor using CR2
    # ------------------------------------------------------------------------------
    n_QCDinData = rhDict_den["QCDinData-CR2-Inclusive"].Integral()
    n_QCDinMC   = rhDict_den["QCD-CR2-Inclusive"].Integral()
    f1 = float(n_QCDinData)/float(n_QCDinMC)
    Print("QCD Normalization factor: = %s%0.6f%s in CR2" % (ShellStyles.NoteStyle(), f1, ShellStyles.NormalStyle()), True)
    
    # ------------------------------------------------------------------------------
    # (3) Normalize QCD (MC) in all regions
    # -------------------------------------------------------------------------------
    for re in regions:
        rhDict_den["NormQCD-"+re+"-Inclusive"] = rhDict_den["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_den["NormQCD-"+re+"-Inclusive"].Scale(f1)
        
        rhDict_num["NormQCD-"+re+"-Inclusive"] = rhDict_num["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num["NormQCD-"+re+"-Inclusive"].Scale(f1)
        
    # ------------------------------------------------------------------------------
    # (4) Plot all regions after applying the normalization factor    
    # ------------------------------------------------------------------------------
    regions2 = ["CR2"]
    for re in regions2:
        
        # Reset histograms
        h0.Reset()
        h1.Reset()
        
        h0 = rhDict_den["QCDinData-"+re+"-Inclusive"].Clone("QCD (Data)")
        h1 = rhDict_den["NormQCD-"+re+"-Inclusive"].Clone("F1*QCD (MC)")
        
        h_QCDinData = histograms.Histo( h0, "QCD (Data)", "Data")
        h_QCDinData.setIsDataMC(isData=True, isMC=False)
        
        h_QCDinMC_After = histograms.Histo( h1, "QCD (MC)", "QCD")
        h_QCDinMC_After.setIsDataMC(isData=False, isMC=True)
        
        p0 = plots.ComparisonManyPlot(h_QCDinMC_After, [h_QCDinData], saveFormats=[])
        p0.setLuminosity(intLumi)
        p0.setDefaultStyles()
    
        # Draw the plot and save it
        hName = "QCD_"+re+"_After_Normalization"
        plots.drawPlot(p0, hName, **_kwargs)
        SavePlot(p0, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
        
    #========================================================================================
    # Get TT in Data (Data - EWK - QCD*f1 - Single Top) in all regions
    #=========================================================================================
    for re in regions:
        rhDict_den["TTinData-"+re+"-Inclusive"] = rhDict_den["Data-"+re+"-Inclusive"].Clone("TTinData-"+re+"-Inclusive")
        rhDict_den["TTinData-"+re+"-Inclusive"].Add(rhDict_den["EWK-"+re+"-Inclusive"]       , -1)
        rhDict_den["TTinData-"+re+"-Inclusive"].Add(rhDict_den["NormQCD-"+re+"-Inclusive"]   , -1)
        rhDict_den["TTinData-"+re+"-Inclusive"].Add(rhDict_den["SingleTop-"+re+"-Inclusive"] , -1)
    
    # ----------------------------------------------------------------------------
    # (1) Plot inclusive TT (Data Vs MC) before any normalization in all regions
    # ----------------------------------------------------------------------------
    for re in regions:
        
        hName = "TT_"+re+"_Before_Normalization"
        
        h0.Reset()
        h1.Reset()
        
        h0 = rhDict_den["TTinData-"+re+"-Inclusive"].Clone("t#bar{t} (Data)")
        h1 = rhDict_den["TT-SR-Inclusive"].Clone("t#bar{t} (MC)")
        
        h_TTinData = histograms.Histo( h0, "t#bar{t} (Data)", "TT");    h_TTinData.setIsDataMC(isData=True, isMC=False)
        h_TTinMC   = histograms.Histo( h1, "t#bar{t} (MC)", "TT");      h_TTinMC.setIsDataMC(isData=False, isMC=True)
        
        pTT = plots.ComparisonManyPlot(h_TTinMC, [h_TTinData], saveFormats=[])
        pTT.setLuminosity(intLumi)
        pTT.setDefaultStyles()
        plots.drawPlot(pTT, hName, **_kwargs)
        SavePlot(pTT, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
        
    # ------------------------------------------------------------------------------
    # (2) Find the normalization factor using SR
    # ------------------------------------------------------------------------------
    n_TTinData = rhDict_den["TTinData-SR-Inclusive"].Integral()
    n_TTinMC   = rhDict_den["TT-SR-Inclusive"].Integral()
    f2 = float(n_TTinData)/float(n_TTinMC)
    Print("TT Normalization factor: = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f2, ShellStyles.NormalStyle()), True)
    
    # ------------------------------------------------------------------------------
    # (3) Normalize TT (MC) in all regions
    # -------------------------------------------------------------------------------
    labels = ["Inclusive", "Fake", "Genuine"]
    for la in labels:
        for re in regions:
            rhDict_den["NormTT-"+re+"-"+la] = rhDict_den["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_den["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num["NormTT-"+re+"-"+la] = rhDict_num["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num["NormTT-"+re+"-"+la].Scale(f2)
            
    # ------------------------------------------------------------------------------
    # (4) Plot all regions after applying the normalization factor    
    # ------------------------------------------------------------------------------
    for re in regions:
        
        hName = "TT_"+re+"_After_Normalization"
        
        # Reset histograms
        h0.Reset()
        h1.Reset()

        h0 = rhDict_den["TTinData-"+re+"-Inclusive"].Clone("t#bar{t} (Data)")
        h1 = rhDict_den["NormTT-"+re+"-Inclusive"].Clone("t#bar{t} (MC)")
    
        h_TTinData = histograms.Histo( h0, "t#bar{t} (Data)", "TT");     h_TTinData.setIsDataMC(isData=True, isMC=False)
        h_TTinMC_After = histograms.Histo( h1, "t#bar{t} (MC)", "TT");   h_TTinMC_After.setIsDataMC(isData=False, isMC=True)
        
        p1 = plots.ComparisonManyPlot(h_TTinMC_After, [h_TTinData], saveFormats=[])
        p1.setLuminosity(intLumi)
        p1.setDefaultStyles()
        plots.drawPlot(p1, hName, **_kwargs)
        SavePlot(p1, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
    

    return


def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h     = tefficiency.GetCopyTotalHisto()
    n     = h.GetNbinsX()

    # For-loop: All bins
    for i in range(1, n+1):
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
        
    graph = ROOT.TGraphAsymmErrors(n, array.array("d",x), array.array("d",y),
                                   array.array("d",xerrl), array.array("d",xerrh),
                                   array.array("d",yerrl), array.array("d",yerrh)) 
    return graph



def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Print(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
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
    ANALYSISNAME = "SystTopBDT"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    SIGNALMASS   = []
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    URL          = True
    NOERROR      = True
    SAVEDIR      = None
    VERBOSE      = False
    HISTOLEVEL   = "Vital"
    NORMALISE    = False  
    FOLDER       = "SystTopBDT_" 
    SUBDIR       = "NormalizationFactors"

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

    parser.add_option("--subDir", dest="subDir", type="string", default = SUBDIR,
                      help="Save plots to directory in respect of the MVA cut value [default: %s]" % (SUBDIR) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix=opts.analysisName+"/", postfix="")


    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getNormalization.py: Press any key to quit ROOT ...")
