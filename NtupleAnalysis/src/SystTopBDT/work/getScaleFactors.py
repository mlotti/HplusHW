#!/usr/bin/env python
'''
DESCRIPTION:
This script calculates the normalization factors of the QCD and EWK events.
Using an ABCD method, the phase space is divided into four regions:

Signal Region (SR)    : Events with high MET (> 50 GeV/c^2) and low muon Isolation (muIso < 0.1)
Control Region 1 (CR1): Events with low MET (< 30 GeV/c^2) and low muon Isolation  (muIso < 0.1)
Control Region 2 (CR2): Events with low MET (< 30 GeV/c^2) and high muon Isolation (muIso > 0.2) --- Dominated by QCD background
Verification Region   : Events with high MET (> 50GeV/c^2) and high muon Isolation (muIso > 0.2)

-----
The QCD normalization factor (f1) is calculated in the CR2 as follows:

NQCD_CR2_data = Data_CR2 - EWK_CR2  - ttbar_CR2
The result of the previous step is the QCD data
    
f1 = NQCD_CR2_data/NQCD_CR2_MC
-----
The TT normalization factor (f2) is calculated in the SR as follows:

N_ttbar_SR_data = data - EWK_SR*f1 - QCD_SR *f1 
The result of the previous step is the ttbar data

f2 = N_ttbar_Data_SR/N_ttbar_MC_SR

The normalization factors are applies on the events in order to measure the mistagginig efficiency of the top-tagger 
in the two control regions (CR1, CR2) in MC and data. 

1) Mistagging efficiency in CR2 (QCD mistag rate)
     eff_qcd_CR2 = [QCD_CR2_MC_passBDT] / [QCD_CR2_MC]         
     eff_data_CR2 = [Data_CR2_pass_BDT - EWK_CR2_passBDT - f2*ttbar_CR2_MC_passBDT ] /[Data - EWK_CR2 - f2*ttbar_MC_CR2]  

2) Mistagging efficiency in CR1 (EWK and fake ttbar mistag rate)
     eff_MC_CR1 = [EWK_CR1_MC_passBDR + f2 * tt_fakes_CR1_MC_passBDT]/[EWK_CR1_MC + f2 * tt_fakes_CR1_MC]
     eff_data_CR1 = [N_CR1_Data_passBDT - f1 * QCD_MC_CR1_passBDT*SF_CR2 - f2 * ttbar_CR1_genuine_passBDT]/[DATA -  f1 * QCD_MC_CR1 - f2 * ttbar_CR1*genuine]
     
Finally, the script produces the json files which will be used to calculate the scale factors and measure the tagging efficiency



USAGE:
./plot/getScaleFactors.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot/getScaleFactors.py -m SystTopBDT_180417_102133_noSF_withTopPtRew --folder SystTopBDT_ -e "TTW"

LAST USD:
./plot/getScaleFactors.py -m SystTopBDT_180417_102133_noSF_withTopPtRew --folder SystTopBDT_ -e "TTW"

STATISTICS OPTIONS:
https://iktp.tu-dresden.de/~nbarros/doc/root/TEfficiency.html
statOption = ROOT.TEfficiency.kFCP       # Clopper-Pearson
statOption = ROOT.TEfficiency.kFNormal   # Normal Approximation
statOption = ROOT.TEfficiency.kFWilson   # Wilson
statOption = ROOT.TEfficiency.kFAC       # Agresti-Coull
statOption = ROOT.TEfficiency.kFFC       # Feldman-Cousins
statOption = ROOT.TEfficiency.kBJeffrey # Jeffrey
statOption = ROOT.TEfficiency.kBUniform # Uniform Prior
statOption = ROOT.TEfficiency.kBayesian # Custom Prior
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

#def GetListOfQCDatasets():
#    Verbose("Getting list of QCD datasets")
#    return ["QCD_HT1000to1500", "QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000"]

#def GetListOfEwkDatasets():
#    Verbose("Getting list of EWK datasets")
#    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


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
    #_moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}                                                                                        
    #moveLegend =  {"dx": -0.08, "dy": -0.01, "dh": -0.1 } 
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
        "ratioYlabel"      : "Data/Bkg. ",
        "ratio"            : True,
        "ratioCreateLegend": True,
        "ratioType"        : "errorScale",
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.05},
        "stackMCHistograms": False, #not opts.nostack,
        "ratioInvert"      : False,
        "addMCUncertainty" : False,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": yMin, "ymaxfactor": yMaxF},
        #"opts2"            : {"ymin": 0.0, "ymax": 2.0},                                                                                                                                                                                                          
        "opts2"            : {"ymin": 0.59, "ymax": 1.41},
        "log"              : logY,
        "moveLegend"       : _moveLegend,
        }

    kwargs = copy.deepcopy(_kwargs)

    print "h=", h

    if "pt" in h.lower():
        units            = "(GeV/c)"
        kwargs["ylabel"] = _yLabel + units
        kwargs["xlabel"] = "p_{T}" + units
        kwargs["rebinX"] = 2
        
    return kwargs


def main(opts, signalMass):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(True)
    
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
        datasetsMgr.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)


        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        #plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Print dataset information before removing anything?
        if 1:
            datasetsMgr.PrintInfo()

        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        # Remove datasets
        filterKeys = ["TTW"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
        else:
            intLumi = 35920
        # Remove datasets
        #filterKeys = ["Data",  "TTZToQQ", "TTWJets", "TTTT", "QCD"]
        #filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
        

        if 1:
            datasetsMgr.PrintInfo()

        # Re-order datasets
        datasetOrder = []
        haveQCD = False
        for d in datasetsMgr.getAllDatasets():
            if "Charged" in d.getName():
                if d not in signalMass:
                    continue
            if "QCD" in d.getName():
                haveQCD = True
            datasetOrder.append(d.getName())
            
        # Append signal datasets
        for m in signalMass:
            datasetOrder.insert(0, m)
        datasetsMgr.selectAndReorder(datasetOrder)

        # Define the mapping histograms in numerator->denominator pairs
        VariableList = [
            #"MET",
            #"HT",
            #"NJets",
            #"NBJets",
            #"Muon_Pt",
            #"Muon_Eta",
            #"Muon_Phi",
            "LeadingTrijet_Pt",
            #"LeadingTrijet_Eta",
            #"LeadingTrijet_Phi",
            #"LeadingTrijet_BJet_Pt",
            #"LeadingTrijet_BJet_CSV",
            #"WMass",
            ]

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        EWKlist = [
            "WJetsHT",
            "DYJetsToLL",
            "Diboson"
            ]

        datasetsMgr.merge("EWK", EWKlist)
        datasetsMgr.PrintInfo()
        # Get datasets                                                                                                                             
        '''
        datasetsMgr.mergeMC()
        dataset_Data = datasetsMgr.getDataDatasets()
        dataset_MC   = datasetsMgr.getMCDatasets()
        '''

        # For-loop: All numerator-denominator pairs
        counter =  0
        nPlots  = len(VariableList)

        for var in VariableList:
            histoN = "AfterAllSelections_"+var+"_CR2"
            histoD = "AfterStandardSelections_"+var+"_CR2"

            hName   = os.path.join(opts.folder, histoD)

            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s" % (var))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            
            GetScaleFactors(datasetsMgr, hName, intLumi)
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


def GetScaleFactors(datasetsMgr, hName_CR2, intLumi):  
    _kwargs = GetHistoKwargs(hName_CR2, opts)        

   # Definition                                                                                                                                                                         
    hPathDict = {}
    rhDict    = {}

    hName_CR2_sel = hName_CR2.replace("Standard", "All")

    #Define histo names in signal region
    hName_SR         = hName_CR2
    hName_SR         = hName_SR.replace("CR2","SR")
    hName_SR_fake    = hName_SR.replace("SystTopBDT_", "SystTopBDT_Fake")
    hName_SR_genuine = hName_SR.replace("SystTopBDT_", "SystTopBDT_Genuine")

    hName_SR_sel     = hName_CR2_sel
    hName_SR_sel     = hName_SR_sel.replace("CR2","SR")
    hName_SR_fake_sel    = hName_SR_fake.replace("Standard", "All")
    hName_SR_genuine_sel = hName_SR_genuine.replace("Standard", "All")


    #Define histo names in control region 1
    hName_CR1         = hName_CR2
    hName_CR1         = hName_CR1.replace("CR2","CR1")
    hName_CR1_fake    = hName_CR1.replace("SystTopBDT_", "SystTopBDT_Fake")
    hName_CR1_genuine = hName_CR1.replace("SystTopBDT_", "SystTopBDT_Genuine")

    hName_CR1_sel     = hName_CR2_sel
    hName_CR1_sel     = hName_CR1_sel.replace("CR2","CR1")
    hName_CR1_fake_sel    = hName_CR1_fake.replace("Standard", "All")
    hName_CR1_genuine_sel = hName_CR1_genuine.replace("Standard", "All")
    

    #Get histograms from datasets

    #===Data===
    hPathDict["Data-CR2"] = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_CR2).getHistogram()
    hPathDict["Data-CR1"] = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_CR1).getHistogram()
    hPathDict["Data-SR"]  = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_SR).getHistogram()

    hPathDict["Data-CR2-num"] = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_CR2_sel).getHistogram()
    hPathDict["Data-CR1-num"] = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_CR1_sel).getHistogram()
    hPathDict["Data-SR-num"]  = datasetsMgr.getDataset("Data").getDatasetRootHisto(hName_SR_sel).getHistogram()

    #===EWK===
    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_CR2)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-CR2"] = n.getHistogram()

    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_CR1)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-CR1"] = n.getHistogram()

    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_SR)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-SR"] = n.getHistogram()

    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_CR2_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-CR2-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_CR1_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-CR1-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("EWK").getDatasetRootHisto(hName_SR_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["EWK-SR-num"] = n.getHistogram()


    #===QCD===
    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_CR2)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-CR2"] = n.getHistogram()

    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_CR1)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-CR1"] = n.getHistogram()

    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_SR)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-SR"] = n.getHistogram()

    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_CR2_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-CR2-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_CR1_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-CR1-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("QCD").getDatasetRootHisto(hName_SR_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["QCD-SR-num"] = n.getHistogram()


    #===TT===
    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR2)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR2"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR"] = n.getHistogram()

    # Genuine - Fake TT
    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1_fake)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1-fake"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR_fake)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR-fake"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1_genuine)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1-genuine"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR_genuine)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR-genuine"] = n.getHistogram()


    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR2_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR2-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR-num"] = n.getHistogram()

    # Genuine - Fake TT
    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1_fake_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1-fake-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR_fake_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR-fake-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_CR1_genuine_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-CR1-genuine-num"] = n.getHistogram()

    n = datasetsMgr.getDataset("TT").getDatasetRootHisto(hName_SR_genuine_sel)
    n.normalizeToLuminosity(intLumi)
    hPathDict["TT-SR-genuine-num"] = n.getHistogram()

    #=======
    
    # Why do I need them?
    # Clone and Save the root histograms
    #Data
    rhDict["Data-CR2"] = hPathDict["Data-CR2"].Clone("Data-CR2")
    rhDict["Data-CR1"] = hPathDict["Data-CR1"].Clone("Data-CR1")
    rhDict["Data-SR"]  = hPathDict["Data-SR"].Clone("Data-SR")

    rhDict["Data-CR2-num"] = hPathDict["Data-CR2-num"].Clone("Data-CR2-num")
    rhDict["Data-CR1-num"] = hPathDict["Data-CR1-num"].Clone("Data-CR1-num")
    rhDict["Data-SR-num"]  = hPathDict["Data-SR-num"].Clone("Data-SR-num")

    #EWK
    rhDict["EWK-CR2"] = hPathDict["EWK-CR2"].Clone("EWK-CR2")
    rhDict["EWK-CR1"] = hPathDict["EWK-CR1"].Clone("EWK-CR1")
    rhDict["EWK-SR"]  = hPathDict["EWK-SR"].Clone("EWK-SR")

    rhDict["EWK-CR2-num"] = hPathDict["EWK-CR2-num"].Clone("EWK-CR2-num")
    rhDict["EWK-CR1-num"] = hPathDict["EWK-CR1-num"].Clone("EWK-CR1-num")
    rhDict["EWK-SR-num"]  = hPathDict["EWK-SR-num"].Clone("EWK-SR-num")

    #QCD
    rhDict["QCD-CR2"] = hPathDict["QCD-CR2"].Clone("QCD-CR2")
    rhDict["QCD-CR1"] = hPathDict["QCD-CR1"].Clone("QCD-CR1")
    rhDict["QCD-SR"]  = hPathDict["QCD-SR"].Clone("QCD-SR")

    rhDict["QCD-CR2-num"] = hPathDict["QCD-CR2-num"].Clone("QCD-CR2-num")
    rhDict["QCD-CR1-num"] = hPathDict["QCD-CR1-num"].Clone("QCD-CR1-num")
    rhDict["QCD-SR-num"]  = hPathDict["QCD-SR-num"].Clone("QCD-SR-num")

    #TT
    rhDict["TT-CR2"] = hPathDict["TT-CR2"].Clone("TT-CR2")
    rhDict["TT-CR1"] = hPathDict["TT-CR1"].Clone("TT-CR1")
    rhDict["TT-SR"]  = hPathDict["TT-SR"].Clone("TT-SR")

    rhDict["TT-CR1-fake"] = hPathDict["TT-CR1-fake"].Clone("TT-CR1-fake")
    rhDict["TT-SR-fake"]  = hPathDict["TT-SR-fake"].Clone("TT-SR-fake")
    rhDict["TT-CR1-genuine"] = hPathDict["TT-CR1-genuine"].Clone("TT-CR1-genuine")
    rhDict["TT-SR-genuine"]  = hPathDict["TT-SR-genuine"].Clone("TT-SR-genuine")

    rhDict["TT-CR2-num"] = hPathDict["TT-CR2-num"].Clone("TT-CR2-num")
    rhDict["TT-CR1-num"] = hPathDict["TT-CR1-num"].Clone("TT-CR1-num")
    rhDict["TT-SR-num"]  = hPathDict["TT-SR-num"].Clone("TT-SR-num")

    rhDict["TT-CR1-fake-num"] = hPathDict["TT-CR1-fake-num"].Clone("TT-CR1-fake-num")
    rhDict["TT-SR-fake-num"]  = hPathDict["TT-SR-fake-num"].Clone("TT-SR-fake-num")
    rhDict["TT-CR1-genuine-num"] = hPathDict["TT-CR1-genuine-num"].Clone("TT-CR1-genuine-num")
    rhDict["TT-SR-genuine-num"]  = hPathDict["TT-SR-genuine-num"].Clone("TT-SR-genuine-num")


    #===============================================================
    # QCD Normalization Factor: CR2
    #===============================================================
    #Subtract EWK, ttbar (MC) from Data to get QCD (= Data - EWK - ttbar)
    #Define QCD_data
    rhDict["QCD_data-CR2"] = rhDict["Data-CR2"].Clone("QCD_data-CR2")
    rhDict["EWK_TT-CR2"] = rhDict["EWK-CR2"].Clone("EWK_TT-CR2")
    # Add tt in EWK (CR2)
    rhDict["EWK_TT-CR2"].Add(rhDict["TT-CR2"], +1)
    #Subtract EWK inclusive from data                                                                                                                                                  
    rhDict["QCD_data-CR2"].Add( rhDict["EWK_TT-CR2"], -1 )

    plots._plotStyles["Data"].apply(hPathDict["Data-CR2"])
    plots._plotStyles["EWK"].apply(hPathDict["EWK-CR2"])
    plots._plotStyles["TT"].apply(hPathDict["TT-CR2"])
    plots._plotStyles["QCD"].apply(hPathDict["QCD-CR2"])

    plots._plotStyles["Data"].apply(rhDict["Data-CR2"])
    plots._plotStyles["EWK"].apply(rhDict["EWK-CR2"])
    plots._plotStyles["TT"].apply(rhDict["TT-CR2"])
    plots._plotStyles["QCD"].apply(rhDict["QCD-CR2"])
    plots._plotStyles["WJets"].apply(rhDict["QCD_data-CR2"])
    rhDict["QCD_data-CR2"].SetMarkerSize(1.2)

    #stylesEWK_TT.apply(rhDict["EWK_TT-CR2"])
    #stylesQCD_data.apply(rhDict["QCD_data-CR2"])

    if 1:
        #p = plots.ComparisonManyPlot(rhDict["Data-CR2"], [rhDict["EWK-CR2"], rhDict["QCD_data-CR2"], rhDict["QCD-CR2"]], saveFormats=[])

        #Compare (Data-EWK-TT in CR2) to QCD-MC in CR2
        p_QCD = plots.ComparisonManyPlot(histograms.Histo(rhDict["QCD_data-CR2"], "Data-EWK-TT", drawStyle = "l"), 
                                        [histograms.Histo(rhDict["QCD-CR2"], "QCD", drawStyle = "l")], saveFormats=[])

        p_QCD.setLuminosity(intLumi)
        nQCD_CR2_data = rhDict["QCD_data-CR2"].Integral(0, rhDict["QCD_data-CR2"].GetXaxis().GetNbins()+1)
        nQCD_CR2_MC   = rhDict["QCD-CR2"].Integral(0, rhDict["QCD-CR2"].GetXaxis().GetNbins()+1)

        #Calculate Normalization factor of QCD: f1
        f1 = float(nQCD_CR2_data)/float(nQCD_CR2_MC)
        
        print "==============================================================="
        Print("QCD Normalization factor: = %s%0.6f%s in CR2" % (ShellStyles.NoteStyle(), f1, ShellStyles.NormalStyle()), True)
        print "==============================================================="

        # Apply QCD normalization factor (CR2)
        rhDict["QCD-CR2"].Scale(f1)

        # Create empty histogram stack list
        myStackList_CR2 = []

        # Add the (Data - EWK - TT) MC background to the histogram list (CR2)
        hQCD_data_CR2 = histograms.Histo(rhDict["QCD_data-CR2"], "QCD (Data-EWK)", "QCD-data")
        hQCD_data_CR2.setIsDataMC(isData=False, isMC=True)
        #myStackList.append(hQCD_data_CR2)

        # Add the Normalizes QCD MC background to the histogram list (CR2)
        hQCD_CR2 = histograms.Histo(rhDict["QCD-CR2"], "QCD (Norm)", "QCD-MC")
        hQCD_CR2.setIsDataMC(isData=False, isMC=True)
        myStackList_CR2.append(hQCD_CR2)

        # Add the TT MC background to the histogram list
        hTT_CR2 = histograms.Histo(rhDict["TT-CR2"], "TT", "TT")
        hTT_CR2.setIsDataMC(isData=False, isMC=True)
        myStackList_CR2.append(hTT_CR2)

        # Add the EWK MC background to the histogram list
        hEWK_CR2 = histograms.Histo(rhDict["EWK-CR2"], "EWK", "EWK")
        hEWK_CR2.setIsDataMC(isData=False, isMC=True)
        myStackList_CR2.append(hEWK_CR2)
        
        # Add the collision datato the histogram list
        hData_CR2 = histograms.Histo(rhDict["Data-CR2"], "Data", "Data")
        hData_CR2.setIsDataMC(isData=True, isMC=False)
        myStackList_CR2.insert(0, hData_CR2)        
        
        _kwargs["ratio"]             = True
        _kwargs["ratioInvert"]       = True
        _kwargs["cutBoxY"]           = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
        _kwargs["stackMCHistograms"] = True

        p_normQCD = plots.DataMCPlot2( myStackList_CR2, saveFormats=[])
        p_normQCD.setLuminosity(intLumi)
        p_normQCD.setDefaultStyles()
    
        #savePath = os.path.join(opts.saveDir, hName_CR2.split("/")[0], opts.optMode)
        #save_path = savePath + opts.subDir
        save_path = os.path.join(opts.saveDir, opts.subDir, opts.optMode)
        saveName = "QCDNorm_" + hName_CR2.split("/")[-1]
        plots.drawPlot(p_normQCD, saveName, **_kwargs)
        SavePlot(p_normQCD, saveName, save_path, saveFormats = [".png", ".pdf"])

    # Save plot in all formats
    #savePath = os.path.join(opts.saveDir, hName_CR2.split("/")[0], opts.optMode)
    #save_path = savePath + opts.subDir
    save_path = os.path.join(opts.saveDir, opts.subDir, opts.optMode)
    # Draw and save the plot               
    _kwargs["stackMCHistograms"] = False
    _kwargs["ratio"] = True
    _kwargs["ratioInvert"] = True
    _kwargs["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
    saveName = "QCD_" + hName_CR2.split("/")[-1]
    plots.drawPlot(p_QCD, saveName, **_kwargs)
    #SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf"])
    SavePlot(p_QCD, saveName, save_path, saveFormats = [".png", ".pdf"])

    #===============================================================
    # TT Normalization Factor: SR
    #===============================================================

    #Subtract normQCD, EWK from Data to get TT (TT = Data - f1*QCD - EWK)
    #Define QCD_data
    rhDict["TT_data-SR"]     = rhDict["Data-SR"].Clone("TT_data-SR")
    rhDict["EWK_normQCD-SR"] = rhDict["EWK-SR"].Clone("EWK_normQCD-SR")
    rhDict["normQCD-SR"]     = rhDict["QCD-SR"].Clone("normQCD-SR")

    #Apply QCD normalizatio factor in QCD-MC (SR)
    rhDict["normQCD-SR"].Scale(f1)
    #Add EWK and normalized QCD (SR)
    rhDict["EWK_normQCD-SR"].Add(rhDict["normQCD-SR"], +1)
    #Subtract EWK, norm QCD inclusive from data
    rhDict["TT_data-SR"].Add(rhDict["EWK_normQCD-SR"], -1)

    plots._plotStyles["Data"].apply(hPathDict["Data-SR"])
    plots._plotStyles["EWK"].apply(hPathDict["EWK-SR"])
    plots._plotStyles["TT"].apply(hPathDict["TT-SR"])
    plots._plotStyles["QCD"].apply(hPathDict["QCD-SR"])

    plots._plotStyles["Data"].apply(rhDict["Data-SR"])
    plots._plotStyles["EWK"].apply(rhDict["EWK-SR"])
    plots._plotStyles["TT"].apply(rhDict["TT-SR"])
    plots._plotStyles["TT"].apply(rhDict["TT-SR-genuine"])
    plots._plotStyles["QCD"].apply(rhDict["QCD-SR"])

    plots._plotStyles["QCD"].apply(rhDict["normQCD-SR"])
    #stylesEWK_TT.apply(rhDict["TT_data-SR"])
    #stylesQCD_data.apply(rhDict["QCD_data-SR"])
    plots._plotStyles["FakeB"].apply(rhDict["TT_data-SR"])
    rhDict["TT_data-SR"].SetMarkerSize(1.2)
    rhDict["TT_data-SR"].SetLineStyle(ROOT.kSolid)
    #rhDict["normQCD-SR"].SetLineStyle(ROOT.kSolid)

    if 1:
        #p = plots.ComparisonManyPlot(rhDict["Data-SR"], [rhDict["EWK-SR"], rhDict["QCD_data-SR"], rhDict["QCD-SR"]], saveFormats=[])
        
        #Compare (Data-EWK-TT in SR) to QCD-MC in SR
        p_TT = plots.ComparisonManyPlot(histograms.Histo(rhDict["TT_data-SR"], "Data-EWK-QCD(norm)", drawStyle = "l"), 
                                        [histograms.Histo(rhDict["TT-SR"], "TT", drawStyle = "l")], saveFormats=[])

        p_TT.setLuminosity(intLumi)
        nTT_SR_data = rhDict["TT_data-SR"].Integral(0, rhDict["TT_data-SR"].GetXaxis().GetNbins()+1)
        nTT_SR_MC   = rhDict["TT-SR"].Integral(0, rhDict["TT-SR"].GetXaxis().GetNbins()+1)

        #Calculate Normalization factor of QCD: f1
        f2 = float(nTT_SR_data)/float(nTT_SR_MC)
        
        print "==============================================================="
        Print("TT Normalization factor: = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f2, ShellStyles.NormalStyle()), True)
        print "==============================================================="

        # Apply TT normalization factor (SR)
        rhDict["TT-SR"].Scale(f2)
        rhDict["TT-SR-fake"].Scale(f2)

        # Create empty histogram stack list
        myStackList_SR = []

        # Add the (Data - EWK - f1*QCD) MC background to the histogram list (SR)
        hTT_data_SR = histograms.Histo(rhDict["TT_data-SR"], "TT (Data-EWK-QCD(norm))", "TT-data")
        hTT_data_SR.setIsDataMC(isData=False, isMC=True)
        #myStackList.append(hQCD_data_SR)

        # Add the TT MC background to the histogram list
        hTT_SR = histograms.Histo(rhDict["TT-SR"], "TT (Norm)", "TT (Norm)")
        hTT_SR.setIsDataMC(isData=False, isMC=True)
        #myStackList_SR.append(hTT_SR)

        hTT_fake_SR = histograms.Histo( rhDict["TT-SR-fake"], "TT (fake)", "TT (fake)")
        hTT_fake_SR.setIsDataMC(isData=False, isMC=True)
        myStackList_SR.append(hTT_fake_SR)

        hTT_genuine_SR = histograms.Histo(rhDict["TT-SR-genuine"], "TT", "TT (genuine)")
        hTT_genuine_SR.setIsDataMC(isData=False, isMC=True)
        myStackList_SR.append(hTT_genuine_SR)


        hTT_SR = histograms.Histo(rhDict["TT-SR"], "TT (Norm)", "TT (Norm)")
        hTT_SR.setIsDataMC(isData=False, isMC=True)
        #myStackList_SR.append(hTT_SR)


        # Add the Normalizes QCD MC background to the histogram list (SR)
        hNormQCD_SR = histograms.Histo(rhDict["normQCD-SR"], "QCD", "QCD-norm")
        hNormQCD_SR.setIsDataMC(isData=False, isMC=True)
        myStackList_SR.append(hNormQCD_SR)

        # Add the EWK MC background to the histogram list
        hEWK_SR = histograms.Histo(rhDict["EWK-SR"], "EWK", "EWK")
        hEWK_SR.setIsDataMC(isData=False, isMC=True)
        myStackList_SR.append(hEWK_SR)
        
        # Add the collision datato the histogram list
        hData_SR = histograms.Histo(rhDict["Data-SR"], "Data", "Data")
        hData_SR.setIsDataMC(isData=True, isMC=False)
        myStackList_SR.insert(0, hData_SR)        
        
        _kwargs["ratio"] = True
        _kwargs["ratioInvert"] = True
        _kwargs["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
        _kwargs["stackMCHistograms"] = True

        p_normTT = plots.DataMCPlot2( myStackList_SR, saveFormats=[])
        p_normTT.setLuminosity(intLumi)
        p_normTT.setDefaultStyles()
    
        #savePath = os.path.join(opts.saveDir, hName_SR.split("/")[0], opts.optMode)
        #save_path = savePath + opts.subDir
        save_path = os.path.join(opts.saveDir, opts.subDir, opts.optMode)
        saveName = "TTNorm_" + hName_SR.split("/")[-1]
        plots.drawPlot(p_normTT, saveName, **_kwargs)
        SavePlot(p_normTT, saveName, save_path, saveFormats = [".png", ".pdf"])

    # Save plot in all formats
    #savePath = os.path.join(opts.saveDir, hName_SR.split("/")[0], opts.optMode)
    #save_path = savePath + opts.subDir
    save_path = os.path.join(opts.saveDir, opts.subDir, opts.optMode)
    # Draw and save the plot               
    _kwargs["stackMCHistograms"] = False
    _kwargs["ratio"] = True
    _kwargs["ratioInvert"] = True
    _kwargs["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
    saveName = "TT_" + hName_SR.split("/")[-1]
    plots.drawPlot(p_TT, saveName, **_kwargs)
    #SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf"])
    SavePlot(p_TT, saveName, save_path, saveFormats = [".png", ".pdf"])


    # =========================================================================================
    # Mistag rate: CR2:
    # =========================================================================================
    
    #======= QCD efficiency
    denom_QCD_CR2 = rhDict["QCD-CR2"]
    #Get numerator plot
    rhDict["normQCD-CR2-num"]    = hPathDict["QCD-CR2-num"].Clone("QCD-CR2-num")
    rhDict["normQCD-CR2-num"].Scale(f1)
    numer_QCD_CR2 = rhDict["normQCD-CR2-num"]
    
    
    #======= Data efficiency (Data - EWK - f2*TT = QCD-data)

    rhDict["QCD_data-CR2"] = rhDict["Data-CR2"].Clone("QCD_data-CR2")
    ###############################################################################
    #Test: Normalize EWK with QCD normalization factor (f1)
    rhDict["normEWK-CR2"] = rhDict["EWK-CR2"].Clone("normEWK-CR2")
    rhDict["normEWK-CR2"].Scale(f1)
    #rhDict["QCD_data-CR2"].Add(rhDict["normEWK-CR2"], -1)
    # Subtract EWK from data
    rhDict["QCD_data-CR2"].Add(rhDict["EWK-CR2"], -1)    
    ###############################################################################

    # Normalize TT
    rhDict["normTT-CR2"] = rhDict["TT-CR2"].Clone("normTT-CR2")
    rhDict["normTT-CR2"].Scale(f2)
    # Subtract TT from data
    rhDict["QCD_data-CR2"].Add(rhDict["normTT-CR2"], -1)
    
    #Define denominator
    denom_data_CR2 = rhDict["QCD_data-CR2"]

    #Get numerator plot
    rhDict["QCD_data-CR2-num"] = rhDict["Data-CR2-num"].Clone("QCD_data-CR2-num")
    ###############################################################################
    #Test: Normalize EWK with QCD normalization factor (f1)
    rhDict["normEWK-CR2-num"] = rhDict["EWK-CR2-num"].Clone("normEWK-CR2-num")
    rhDict["normEWK-CR2-num"].Scale(f1)
    #rhDict["QCD_data-CR2-num"].Add(rhDict["normEWK-CR2-num"], -1)
    # Subtract EWK from data
    rhDict["Data-CR2-num"].Add(hPathDict["EWK-CR2-num"], -1)
    ###############################################################################
    rhDict["QCD_data-CR2-num"].Add(hPathDict["TT-CR2-num"], -1)

    numer_data_CR2 = rhDict["QCD_data-CR2-num"]

    # Calculate Efficiencies
    eff_QCD_CR2  = PlotEfficiency(datasetsMgr, numer_QCD_CR2,  denom_QCD_CR2,  intLumi)
    eff_data_CR2 = PlotEfficiency(datasetsMgr, numer_data_CR2, denom_data_CR2, intLumi)

    #Apply Styles
    styles.dataStyle.apply(eff_data_CR2)
    styles.mcStyle.apply(eff_QCD_CR2)
    
    #Create the plot
    p_eff_CR2 = plots.ComparisonPlot(histograms.HistoGraph(eff_data_CR2,   "eff_data_CR2"  , "p", "P"),
                                     histograms.HistoGraph(eff_QCD_CR2,    "eff_QCD_CR2", "p", "P"),
                                     saveFormats=[])

    # Define legend entries
    p_eff_CR2.histoMgr.setHistoLegendLabelMany(
        {
            "eff_QCD_CR2"   : "QCD (MC)",
            "eff_data_CR2"  : "Data"
            }
        )

    # Draw and save the plot
    plotName     = "Eff_" + hName_CR2.replace("AfterStandardSelections_", "").split("/")[-1]

    p_eff_CR2.setLuminosity(intLumi)
    _kwargs_eff = GetHistoKwargs_Efficiency(hName_CR2, opts)
    _kwargs_eff["ratio"] = True
    _kwargs_eff["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
    
    plots.drawPlot(p_eff_CR2, plotName, **_kwargs_eff)
    savePath = os.path.join(opts.saveDir, "MistagRate", opts.optMode)
    SavePlot(p_eff_CR2, plotName, savePath, saveFormats = [".png", ".pdf"])

    runRange = "273150-284044"

    analysis = opts.analysisName
    label = "2016_CR2"
    plotDir =  os.path.join(opts.folder, "Efficiency_LdgTrijet"+label+"_bin.json")
    pythonWriter.addParameters(plotDir, label, runRange, intLumi, eff_data_CR2)
    pythonWriter.addMCParameters(label, eff_QCD_CR2)
    fileName_json = "Efficiency_LdgTrijet"+label+"_bin.json"
    pythonWriter.writeJSON(fileName_json)


    # =========================================================================================
    # Mistag rate: CR1:
    # =========================================================================================
  
    #======= EWK + f2*TTfake efficiency
    #Denominator MC:
    rhDict["EWK_TT-CR1-fake"] =  rhDict["EWK-CR1"].Clone("EWK_TT_CR1-fake")
    rhDict["normTT-CR1-fake"] =  rhDict["TT-CR1-fake"].Clone("normTT_CR1-fake")
    rhDict["normTT-CR1-fake"].Scale(f2)
    rhDict["EWK_TT-CR1-fake"].Add(rhDict["normTT-CR1-fake"], +1)
    
    denom_EWK_TTfake_CR1 = rhDict["EWK_TT-CR1-fake"]

    #Get numerator plot
    rhDict["EWK_TT-CR1-fake-num"] =  rhDict["EWK-CR1"].Clone("EWK_TT_CR1-fake-num")
    rhDict["normTT-CR1-fake-num"]    = hPathDict["TT-CR1-fake-num"].Clone("normTT-CR1-fake-num")
    rhDict["normTT-CR1-fake-num"].Scale(f2)
    rhDict["EWK_TT-CR1-fake-num"].Add(rhDict["normTT-CR1-fake-num"], +1)

    numer_EWK_TTfake_CR1 = rhDict["EWK_TT-CR1-fake-num"]

    #======= Data efficiency (Data - f1*QCD - f2*tt_genuine)
    rhDict["EWK_TT_data-CR1-fake"] = rhDict["Data-CR1"].Clone("EWK_TT_data-CR1-fake")
    # Subtract QCD from data
    rhDict["normQCD-CR1"] = rhDict["QCD-CR1"].Clone("normQCD-CR1")
    rhDict["normQCD-CR1"].Scale(f1)
    rhDict["EWK_TT_data-CR1-fake"].Add(rhDict["normQCD-CR1"], -1)
    
    #rhDict["EWK_TTfake_data-CR1"].Add(

    # Normalize TT
    rhDict["normTT-CR1-genuine"]    = hPathDict["TT-CR1-genuine"].Clone("normTT-CR1-genuine")    
    rhDict["normTT-CR1-genuine"].Scale(f2)

    # Subtract TT from data
    rhDict["EWK_TT_data-CR1-fake"].Add(rhDict["normTT-CR1-genuine"], -1)
    
    # Num
    rhDict["EWK_TT_data-CR1-fake-num"] =    rhDict["Data-CR1-num"].Clone("EWK_TT_data-CR1-fake-num")
    rhDict["normQCD-CR1-num"] = hPathDict["QCD-CR1-num"].Clone("normQCD-CR1-num")

    rhDict["normQCD-CR1-num"].Scale(f1)
    rhDict["EWK_TT_data-CR1-fake-num"].Add(rhDict["normQCD-CR1-num"], -1)

    rhDict["normTT-CR1-genuine-num"] = hPathDict["TT-CR1-genuine-num"].Clone("normTT-CR1-genuine-num")

    rhDict["normTT-CR1-genuine-num"].Scale(f2)
    rhDict["EWK_TT_data-CR1-fake-num"].Add(rhDict["normTT-CR1-genuine-num"], -1)

    #Define denominator
    denom_data_CR1 = rhDict["EWK_TT_data-CR1-fake"]
    numer_data_CR1 = rhDict["EWK_TT_data-CR1-fake-num"]

    styles.mcStyle.apply(denom_data_CR1)
    p_test = plots.ComparisonManyPlot(histograms.Histo(denom_data_CR1, "denom", drawStyle = "l"),
                                     [histograms.Histo(numer_data_CR1, "num", drawStyle = "l")], saveFormats=[])
    
    p_test.setLuminosity(intLumi)
    saveName = "test_" + hName_CR1.split("/")[-1]
    plots.drawPlot(p_test, saveName, **_kwargs)
    #SavePlot(p, saveName, save_path, saveFormats = [".png", ".pdf"])                                                                                                                   
    SavePlot(p_test, saveName, save_path, saveFormats = [".png", ".pdf"])

    # Calculate Efficiencies
    eff_EWK_TTfake_CR1  = PlotEfficiency(datasetsMgr, numer_EWK_TTfake_CR1,  denom_EWK_TTfake_CR1,  intLumi)
    eff_data_CR1 = PlotEfficiency(datasetsMgr, numer_data_CR1, denom_data_CR1, intLumi)

    #Apply Styles
    styles.mcStyle.apply(eff_EWK_TTfake_CR1)
    styles.dataStyle.apply(eff_data_CR1)
    
    #Create the plot
    p_eff_CR1 = plots.ComparisonPlot(histograms.HistoGraph(eff_data_CR1,   "eff_data_CR1"  , "p", "P"),
                                     histograms.HistoGraph(eff_EWK_TTfake_CR1,    "eff_EWK_TTfake_CR1", "p", "P"),
                                     saveFormats=[])

    # Define legend entries
    p_eff_CR1.histoMgr.setHistoLegendLabelMany(
        {
            "eff_EWK_TTfake_CR1"   : "EWK+TT(fake)",
            "eff_data_CR1"  : "Data"
            }
        )

    # Draw and save the plot
    plotName     = "Eff_" + hName_CR1.replace("AfterStandardSelections_", "").split("/")[-1]



    p_eff_CR1.setLuminosity(intLumi)
    _kwargs_eff = GetHistoKwargs_Efficiency(hName_CR1, opts)
    _kwargs_eff["ratio"] = True
    _kwargs_eff["cutBoxY"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
    
    plots.drawPlot(p_eff_CR1, plotName, **_kwargs_eff)
    savePath = os.path.join(opts.saveDir, "MistagRate", opts.optMode)
    SavePlot(p_eff_CR1, plotName, savePath, saveFormats = [".png", ".pdf"])

    runRange = "273150-284044"

    analysis = opts.analysisName
    label = "2016"
    plotDir =  os.path.join(opts.folder, "Efficiency_LdgTrijet"+label+"_bin.json")
    #pythonWriter.addParameters(plotDir, label, runRange, intLumi, eff_data_CR1)
    #pythonWriter.addMCParameters(label, eff_EWK_TTfake_CR1)
    #fileName_json = "Efficiency_LdgTrijet"+label+"_bin_CR1.json"
    #pythonWriter.writeJSON(fileName_json)


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


def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf"]):
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    savePath = os.path.join(saveDir, saveName)
    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
#        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s" % (getpass.getuser()))
        saveNameURL = saveNameURL.replace("/publicweb/%s/%s" % (getpass.getuser()[0], getpass.getuser()), "http://home.fnal.gov/~%s" % (getpass.getuser()))
        #SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
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
    ANALYSISNAME = "SystTopBDT"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [300, 500, 1000]
    SIGNALMASS   = []
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"
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

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
