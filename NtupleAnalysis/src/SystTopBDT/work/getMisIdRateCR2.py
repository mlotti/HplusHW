#!/usr/bin/env python
'''
   DESCRIPTION:
   
   This script calculates the mis-identification rate of QCD+EWK+ST in the background region (CR2). BEFORE running this script make sure 
   you have the correct QCD and TT normalization factors, f1 and f2 (see: getNormalization.py)
   
   QCD+EWK+ST in Data:
   
   Numerator:    [ Data_{CR2} - F2*TT_{CR2} ] passing BDT
   Denominator:  [ Data_{CR2} - F2*TT_{CR2} ]

   QCD+EWK+ST in MC:   
   
   Numerator:    [ F1*QCD_{CR2} + EWK_{CR2} + ST_{CR2} ] passing BDT
   Denominator:  [ F1*QCD_{CR2} + EWK_{CR2} + ST_{CR2} ]

   MisID SF = Efficiency in Data / Efficiency in MC
   
   A json file with the Efficiencies in Data & MC is created.
   
 USAGE:
  ./getMisIdRateCR2.py -m <pseudo-multicrab> --folder <folder> 

 LAST USED:
 ./getMisIdRateCR2.py -m SystTopBDT_180524_074141_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
 
 OTHER SELECTIONS:
  Selection A) ./getMisIdRateCR2.py -m SystTopBDT_180513_100633_MET50_MuIso0p2_InvMET20_InvMuIso0p2_noSF -e "TTW|TTZ"
  Selection B) ./getMisIdRateCR2.py -m SystTopBDT_180513_101101_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection C) ./getMisIdRateCR2.py -m SystTopBDT_180513_101634_MET50_MuIso0p2_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
  Selection D) ./getMisIdRateCR2.py -m SystTopBDT_180513_102112_MET50_MuIso0p1_InvMET30_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection E) ./getMisIdRateCR2.py -m SystTopBDT_180514_110341_MET40_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection F) ./getMisIdRateCR2.py -m SystTopBDT_180514_115524_MET40_MuIso0p1_InvMET30_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection G) ./getMisIdRateCR2.py -m SystTopBDT_180514_115629_MET30_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection H) ./getMisIdRateCR2.py -m SystTopBDT_180517_102420_MET40_MuIso0p1_InvMET20_InvMuIso0p1_noSF -e "TTW|TTZ"
  Selection I) ./getMisIdRateCR2.py -m SystTopBDT_180517_102638_MET30_MuIso0p1_InvMET20_InvMuIso0p2_noSF -e "TTW|TTZ"
  Selection J) ./getMisIdRateCR2.py -m SystTopBDT_180517_102808_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF -e "TTW|TTZ"
  Selection K) ./getMisIdRateCR2.py -m SystTopBDT_180517_174526_TopDir_noSF -e "TTW|TTZ"
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

from PythonWriter import PythonWriter
pythonWriter = PythonWriter()

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
        #"opts2"            : {"ymin": 0.0, "ymax": 2.0},
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
        if 0:
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
         #"opts"             : {"ymin": 0.0, "ymax": 1.09},
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

     if 0:
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
    _kwargs["opts2"]     = {"ymin": 0.50, "ymax": 1.50}
    _kwargs["ratioType"] = "errorScale"
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    labels  = ["Genuine", "Fake", "Inclusive"]
    
    # Get Dictionaries 
    rhDict_num = GetRootHistos(datasetsMgr, num_pathList, regions)
    rhDict_den = GetRootHistos(datasetsMgr, den_pathList, regions)

    # Normalization Factors (see: getNormalization.py)
    f1=0.596314; f2=0.899518;
    
    # ------------------------------------------------------------------------------
    # (A) Normalize QCD and TT (MC) in all regions
    # -------------------------------------------------------------------------------
    
    for re in regions:
        rhDict_den["NormQCD-"+re+"-Inclusive"] = rhDict_den["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_den["NormQCD-"+re+"-Inclusive"].Scale(f1)
        
        rhDict_num["NormQCD-"+re+"-Inclusive"] = rhDict_num["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num["NormQCD-"+re+"-Inclusive"].Scale(f1)

        for la in labels:
            rhDict_den["NormTT-"+re+"-"+la] = rhDict_den["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_den["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num["NormTT-"+re+"-"+la] = rhDict_num["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num["NormTT-"+re+"-"+la].Scale(f2)

    # -----------------------------------------------------------------------------
    # (B) Calculate BKG=QCD+EWK+ST in Data (CR2)
    # -----------------------------------------------------------------------------
    # (B1) Denominator
    rhDict_den["BKG_Data-CR2-Inclusive"] = rhDict_den["Data-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2} (Data)")
    rhDict_den["BKG_Data-CR2-Inclusive"].Add( rhDict_den["NormTT-CR2-Inclusive"], -1)
    
    # (B2) Numerator
    rhDict_num["BKG_Data-CR2-Inclusive"] = rhDict_num["Data-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2} (Data)")
    rhDict_num["BKG_Data-CR2-Inclusive"].Add( rhDict_num["NormTT-CR2-Inclusive"], -1)
    
    # -----------------------------------------------------------------------------
    # (C) Calculate BKG=QCD+EWK+ST in MC (CR2)
    # -----------------------------------------------------------------------------
    # (C1) Denominator
    rhDict_den["BKG_MC-CR2-Inclusive"] = rhDict_den["NormQCD-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2}  (MC)")
    rhDict_den["BKG_MC-CR2-Inclusive"].Add( rhDict_den["EWK-CR2-Inclusive"], +1)
    rhDict_den["BKG_MC-CR2-Inclusive"].Add( rhDict_den["SingleTop-CR2-Inclusive"], +1)
    
    # (C2) Numerator
    rhDict_num["BKG_MC-CR2-Inclusive"] = rhDict_num["NormQCD-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2}  (MC)")
    rhDict_num["BKG_MC-CR2-Inclusive"].Add( rhDict_num["EWK-CR2-Inclusive"], +1)
    rhDict_num["BKG_MC-CR2-Inclusive"].Add( rhDict_num["SingleTop-CR2-Inclusive"], +1)
    
        
    # Rebinning
    bins  = [0, 100, 200, 300, 400, 500, 600, 800]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1
    
    Den_QCD = rhDict_den["NormQCD-CR2-Inclusive"].Clone("QCD")
    Den_EWK = rhDict_den["EWK-CR2-Inclusive"].Clone("EWK")
    Den_ST  = rhDict_den["SingleTop-CR2-Inclusive"].Clone("ST")
    
    Num_QCD = rhDict_num["NormQCD-CR2-Inclusive"].Clone("QCD")
    Num_EWK = rhDict_num["EWK-CR2-Inclusive"].Clone("EWK")
    Num_ST = rhDict_num["SingleTop-CR2-Inclusive"].Clone("ST")
    
    Num_QCD = Num_QCD.Rebin(nx, "", xBins)
    Num_EWK = Num_EWK.Rebin(nx, "", xBins)
    Num_ST  = Num_ST.Rebin(nx, "", xBins)
    
    Den_QCD = Den_QCD.Rebin(nx, "", xBins)
    Den_EWK = Den_EWK.Rebin(nx, "", xBins)
    Den_ST  = Den_ST.Rebin(nx, "", xBins)
    
    # ------------------------------------------------------------------------------
    # (D) Plot denominator & numerator (Data Vs MC)
    # ------------------------------------------------------------------------------
    # (D1) Denominator
    hName = "QCD_EWK_ST_Denominator_CR2"
    
    h0 = rhDict_den["BKG_Data-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2} (Data)")
    h1 = rhDict_den["BKG_MC-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2}  (MC)")

    hData = histograms.Histo( h0, "QCD+EWK (Data)", "Data", drawStyle="AP");    hData.setIsDataMC(isData=True, isMC=False)
    hMC   = histograms.Histo( h1, "QCD+EWK (MC)", "MC", drawStyle="HIST");     hMC.setIsDataMC(isData=False, isMC=True)
    
    _kwargs["createLegend"] = {"x1": 0.70, "y1": 0.60, "x2": 0.95, "y2": 0.92}
    
    pDen = plots.ComparisonManyPlot(hMC, [hData], saveFormats=[])
    pDen.setLuminosity(intLumi)
    pDen.setDefaultStyles()
    plots.drawPlot(pDen, hName, **_kwargs)
    SavePlot(pDen, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])

    # (D2) Numerator
    hName = "QCD_EWK_ST_Numerator_CR2"
    
    h2 = rhDict_num["BKG_Data-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2} (Data)")
    h3 = rhDict_num["BKG_MC-CR2-Inclusive"].Clone("QCD+EWK+ST_{CR2} (MC)")
    
    hDataNum = histograms.Histo( h2, "QCD+EWK (Data)", "Data", drawStyle="AP");    hDataNum.setIsDataMC(isData=True, isMC=False)
    hMCNum   = histograms.Histo( h3, "QCD+EWK (MC)", "MC", drawStyle="HIST");     hMCNum.setIsDataMC(isData=False, isMC=True)
    
    pNum = plots.ComparisonManyPlot(hMCNum, [hDataNum], saveFormats=[])
    pNum.setLuminosity(intLumi)
    pNum.setDefaultStyles()
    plots.drawPlot(pNum, hName, **_kwargs)
    SavePlot(pNum, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
    
    # -----------------------------------------------------------------------------------------------------
    # (E) Plot Mis-Identification rate in CR2
    # -----------------------------------------------------------------------------------------------------
    hName = "MisID_CR2"
    
    _kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Misidentification rate",
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioInvert"      : False,
        "ratioType"        : "errorScale",
        "ratioCreateLegend": True,
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False},
        "errorBarsX"       : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 2.0, "xmax" : 600},
        "opts2"            : {"ymin": 0.30, "ymax": 1.70},
        "log"              : False,
        "createLegend"     : {"x1": 0.55, "y1": 0.70, "x2": 0.95, "y2": 0.92},
        }

    hNum_Data = rhDict_num["BKG_Data-CR2-Inclusive"].Clone("Numerator (Data)")
    hDen_Data = rhDict_den["BKG_Data-CR2-Inclusive"].Clone("Denominator (Data)")
    hNum_MC   = rhDict_num["BKG_MC-CR2-Inclusive"].Clone("Numerator (MC)")
    hDen_MC   = rhDict_den["BKG_MC-CR2-Inclusive"].Clone("Denominator (MC)")

    # Rebinning
    bins  = [0, 100, 200, 300, 400, 500, 600, 800]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1
    
    hNum_Data = hNum_Data.Rebin(nx, "", xBins)
    hDen_Data = hDen_Data.Rebin(nx, "", xBins)
    hNum_MC   = hNum_MC.Rebin(nx, "", xBins)
    hDen_MC   = hDen_MC.Rebin(nx, "", xBins)
    
    num_data, den_data = GetHistosForEfficiency(hNum_Data, hDen_Data)
    num_mc, den_mc     = GetHistosForEfficiency(hNum_MC, hDen_MC)
    
    eff_Data = ROOT.TEfficiency(num_data, den_data)
    eff_Data.SetStatisticOption(ROOT.TEfficiency.kFCP)
    geff_Data = convert2TGraph(eff_Data)
    Graph_Data = histograms.HistoGraph(geff_Data, "QCD+EWK (Data)", "p", "P")
    
    eff_MC = ROOT.TEfficiency(num_mc, den_mc)
    eff_MC.SetStatisticOption(ROOT.TEfficiency.kFCP)
    geff_MC = convert2TGraph(eff_MC)
    styles.getABCDStyle("CR1").apply(geff_MC)
    Graph_MC = histograms.HistoGraph(geff_MC, "QCD+EWK (MC)", "p", "P")

    # Create efficiency plots
    p2 = plots.ComparisonManyPlot(Graph_MC, [Graph_Data], saveFormats=[])
    plots.drawPlot(p2, hName, **_kwargs)
    SavePlot(p2, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".C", ".pdf"])
    
    jsonName = "Efficiency_SystBDT_CR2_MET50_MuIso0p1_InvMET20_InvMuIso0p1.json"

    # Dump results in a JSON File
    runRange = "273150-284044"
    analysis = opts.analysisName
    label = "2016"
    plotDir =  os.path.join(opts.folder, jsonName)
    pythonWriter.addParameters(plotDir, label, runRange, intLumi, geff_Data)
    pythonWriter.addMCParameters(label, geff_MC)
    fileName_json = jsonName
    pythonWriter.writeJSON(fileName_json)
        
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
        #print __doc__
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix=opts.analysisName+"/", postfix="")
        
    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
