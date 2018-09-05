#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_Efficiency.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Efficiency.py -m TopTaggerEfficiency_180529_TopEfficiency_vs_mass --folder topbdtSelection_ -v -e "220"


LAST USED:
./plot_Efficiency.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency_180610_Efficiencies_BDT0p4 --folder topbdtSelection_ -v --url

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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
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
    

def GetHistoKwargs(histoName, opts):
    '''
    Dictionary with
    key   = histogram name
    value = kwargs
    '''
    h = histoName.lower()
    kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "Efficiency / ", #/ %.1f ",
        # "rebinX"           : 1,
        "ratioYlabel"      : "Ratio",
        "ratio"            : True,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"opts"             : {"ymin": 0.0, "ymax": 1.09},
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
#        "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": -0.08},
        "moveLegend"       : {"dx": -0.08, "dy": -0.005, "dh": -0.08},
#        "moveLegend"       : {"dx": -0.57, "dy": -0.007, "dh": -0.18},
        #"cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": True}
        }

    if "pt" in h:
        units   = "GeV/c"
        xlabel  = "candidate p_{T} (%s)" % (units)
        #myBins  = [0, 100, 150, 200, 250, 300, 400, 500, 800]
        myBins  = [0, 50, 100, 150, 250, 350, 450]
        #myBins  = [0, 50, 100, 150, 200, 300, 400, 500]
        #myBins  = [0, 100, 150, 200, 300, 400, 500, 600, 800]
        kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        
        #if "all" in h:
        #    myBins  = [0, 50, 100, 150, 200, 300, 450]
        if "topquark" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.08, "dy": -0.65, "dh": -0.08}
            xlabel = "generated top p_{T} (%s)" % (units)
        if 0:
            ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

        if "fake" in h:
            xlabel = "candidate p_{T} (%s)" % (units)
            kwargs["ylabel"] = "Misidentification rate / " #+ units
            kwargs["opts"]   = {"ymin": 0.0, "ymaxfactor": 1.2}
            kwargs["moveLegend"] = {"dx": -0.08, "dy": -0.65, "dh": -0.08}
            #myBins  = [0, 50, 100, 150, 250, 350, 450, 550]
        if "event" in h:
            #kwargs["moveLegend"] = {"dx": -0.55, "dy": -0.55, "dh": -0.08}
            kwargs["moveLegend"] = {"dx": -0.08, "dy": -0.65, "dh": -0.08}
            #myBins  = [0, 50, 100, 150, 250, 350, 400, 500]
            #myBins  = [0, 100, 200, 300, 400, 500, 800]
        if "_matched" in h:
            myBins  = [0, 100, 200, 300, 500]
        if "_ldg_" in h:
            myBins  = [0, 150, 250, 350, 500]
        if "_sldg_" in h:
            myBins  = [100, 350]

        if 0:
            ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    kwargs["xlabel"]  = xlabel
    kwargs["ylabel"] += units
    if len(myBins) > 0:
        kwargs["binList"] = array.array('d', myBins)
    return kwargs


def main(opts, signalMass):

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
        datasetsMgr.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        datasetsMgr.PrintInfo()
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print dataset information before removing anything?
        if 0:
            datasetsMgr.PrintInfo()

        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        else:
            intLumi = 35920
        # Remove datasets
        filterKeys = ["Data", "QCD", "TTZToQQ", "TTWJets", "TTTT", "ZJetsToQQ_HT600toInf", "DYJetsToQQHT", "SingleTop", "WJetsToQQ_HT_600ToInf", "Diboson"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            #if "TT" in d.getName():
            #    continue
            if "M_" in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())
            
            
        for m in signalMass:
            datasetOrder.insert(0, m)
            #datasetsMgr.selectAndReorder(datasetOrder)

        # Append signal datasets
        #for m in signalMass:
        #    if "_ext1"in signalMass:
        #        continue
        datasetOrder.insert(0, "TT")
        #datasetsMgr.selectAndReorder(datasetOrder)

        # Print dataset information
        datasetsMgr.PrintInfo()


        # Define list with Numerators - Denominators
        '''
        Numerator = ["AllTopQuarkPt_MatchedBDT",
                     "TrijetFakePt_BDT",
                     "AssocTopQuarkPt_MatchedBDT",
                     "HiggsTopQuarkPt_MatchedBDT",
                     "AssocTopQuarkPt_Matched",                       
                     "HiggsTopQuarkPt_Matched",                       
                     "AllTopQuarkPt_MatchedBDT",
                     "AllTopQuarkPt_Matched",
                     ]
        Denominator = ["AllTopQuarkPt_Matched",
                       "TrijetFakePt",
                       "AssocTopQuarkPt_Matched",                       
                       "HiggsTopQuarkPt_Matched",                       
                       "AssocTopQuarkPt",                       
                       "HiggsTopQuarkPt",                       
                       "TopQuarkPt",
                       "TopQuarkPt",
                       ]
        '''

        Numerator = [#"AllTopQuarkPt_MatchedBDT",
                     #"TrijetFakePt_BDT",
                     #"AssocTopQuarkPt_MatchedBDT",
                     #"HiggsTopQuarkPt_MatchedBDT",
                     #"AllTopQuarkPt_MatchedBDT",
                     #"AllTopQuarkPt_Matched",
                     "TrijetPt_LdgOrSldg_Matched",
                     ##"TrijetPt_LdgOrSldg_Unmatched",
                     "TrijetPt_LdgOrSldg_MatchedBDT",
                     "TrijetPt_LdgOrSldg_MatchedBDT",
                     "TrijetPt_LdgOrSldg_UnmatchedBDT",
                     "TrijetPt_LdgOrSldg_UnmatchedBDT",
                     "TrijetPt_Ldg_Matched",
                     "TrijetPt_Ldg_MatchedBDT",
                     ##"TrijetPt_Ldg_MatchedBDT",
                     "TrijetPt_Ldg_UnmatchedBDT",
                     #"TrijetPt_Sldg_Matched",
                     #"TrijetPt_Sldg_MatchedBDT",
                     #"TrijetPt_Sldg_MatchedBDT",
                     #"TrijetPt_Sldg_UnmatchedBDT",
                     
                     ]
        Denominator = [#"AllTopQuarkPt_Matched",
                       #"TrijetFakePt",
                       #"AssocTopQuarkPt_Matched",                       
                       #"HiggsTopQuarkPt_Matched",                       
                       #"TopQuarkPt",
                       #"TopQuarkPt",
                       "TrijetPt_LdgOrSldg",
                       ##"TrijetPt_LdgOrSldg",
                       "TrijetPt_LdgOrSldg",
                       "TrijetPt_LdgOrSldg_Matched",
                       "TrijetPt_LdgOrSldg",
                       "TrijetPt_LdgOrSldg_Unmatched",
                       "TrijetPt_Ldg",
                       "TrijetPt_Ldg",
                       ##"TrijetPt_Ldg_Matched",
                       "TrijetPt_Ldg_Unmatched",
                       #"TrijetPt_Subldg",
                       #"TrijetPt_Subldg",
                       #"TrijetPt_Sldg_Matched",
                       #"TrijetPt_Sldg_Unmatched",
                       ]

        # For-loop: All numerator-denominator pairs
        for i in range(len(Numerator)):
            numerator   = os.path.join(opts.folder, Numerator[i])
            denominator = os.path.join(opts.folder, Denominator[i])
            PlotEfficiency(datasetsMgr, numerator, denominator, intLumi)
            #CalcEfficiency(datasetsMgr, numerator, denominator, intLumi)
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
    table.append("{:^50}".format(hNum.GetName()))
    table.append(txtAlign.format("Bin #", "Numerator (4f)", "Denominator (4f)"))
    table.append(hLine)

    # For-loop: All bins in x-axis
    for i in range(1, hNum.GetNbinsX()+1):
        nbin = hNum.GetBinContent(i)
        dbin = hDen.GetBinContent(i)
        #table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))

        # Numerator > Denominator
        if nbin > dbin:
            hNum.SetBinContent(i, dbin)
        # Numerator < 0 
        if nbin < 0:
            #hNum.SetBinContent(i,0)
            hNum.SetBinContent(i, abs(nbin) )
        # Denominator < 0
        if dbin < 0:
            #hNum.SetBinContent(i,0)
            #hDen.SetBinContent(i,0)
            hDen.SetBinContent(i, abs(dbin))
        # Save updated info to table
        nbin = hNum.GetBinContent(i)
        dbin = hDen.GetBinContent(i)
        table.append(txtAlign.format(i, "%0.4f" % (nbin), "%0.4f" % (dbin) ))

    if verbose:
        for i,row in enumerate(table, 1):
            Print(row, i==1)

    return


def RemoveNegatives(histo):
    '''
    Removes negative bins from histograms
    '''
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return


def PlotEfficiency(datasetsMgr, numPath, denPath, intLumi):
  
    # Definitions
    myList  = []
    myBckList = []
    index   = 0
    _kwargs = GetHistoKwargs(denPath, opts)        
    counter = 0
    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():
        name_N = numPath
        name_D = denPath
        # Get the histograms
        #num = dataset.getDatasetRootHisto(numPath).getHistogram()
        #den = dataset.getDatasetRootHisto(denPath).getHistogram()
        #if "TT" in dataset.getName():
        #    numPath = numPath.replace("HiggsTop", "AllTop")
        #    denPath = denPath.replace("HiggsTop", "AllTop")
        #    numPath = numPath.replace("AssocTop", "AllTop")
        #    denPath = denPath.replace("AssocTop", "AllTop")
                
        n = dataset.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num = n.getHistogram()
        d = dataset.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den = d.getHistogram()


        if "binList" in _kwargs:
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)


        for i in range(1, num.GetNbinsX()+1):
            nbin = num.GetBinContent(i)
            dbin = den.GetBinContent(i)
            #print dataset.getName(), nbin, dbin
            if (nbin > dbin):
                print "error"

        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
            continue
        if num.GetEntries() > den.GetEntries():
            continue

        # Remove negative bins and ensure numerator bin <= denominator bin
        #CheckNegatives(num, den, False)
        #CheckNegatives(num, den, True)
        #RemoveNegatives(num)
        #RemoveNegatives(den)
        # Sanity check (Histograms are valid and consistent) - Always false!
        # if not ROOT.TEfficiency.CheckConsistency(num, den):
        #    continue
        
        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) # fixme: investigate warnings
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #
        
        # Set the weights - Why is this needed?
        if 0:
            weight = 1
            if dataset.isMC():
                weight = dataset.getCrossSection()
                eff.SetWeight(weight)
                
        # Convert to TGraph
        eff = convert2TGraph(eff)
    
        # Apply default style (according to dataset name)
        plots._plotStyles[dataset.getName()].apply(eff)
        # Apply random histo styles and append
        if "charged" in dataset.getName().lower():
            counter +=1
            mass = dataset.getName().split("M_")[-1]    
            styles.markerStyles[counter].apply(eff)
            if "300" in mass or "650" in mass:
                s = styles.getSignalStyleHToTB_M(mass)
                s.apply(eff)
                eff.SetLineStyle(ROOT.kSolid)
                eff.SetLineWidth(3)
                eff.SetMarkerSize(1.2)
                '''
                mass = dataset.getName().split("M_")[-1]
                mass = mass.replace("650", "1000")
                s = styles.getSignalStyleHToTB_M(mass)
                s.apply(eff)
                '''
        '''
        ttStyle = styles.getEWKLineStyle()
        if "tt" in dataset.getName().lower():
            ttStyle.apply(eff)
        '''

        
        # Append in list
        #if "charged" in dataset.getName().lower():
        #    if "m_500" in dataset.getName().lower():
        if 1:
            if "tt" in dataset.getName().lower():
                eff_ref = histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P")
            else:
                myList.append(histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P"))
        #elif "tt" in dataset.getName().lower():
        #    eff_ref = histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P")
            
    # Define save name
    saveName = "Eff_" + name_N.split("/")[-1] + "Over"+ name_D.split("/")[-1]

    # Plot the efficiency
    #p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    p = plots.ComparisonManyPlot(eff_ref, myList, saveFormats=[])
    plots.drawPlot(p, saveName, **_kwargs)

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, name_N.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath, saveFormats = [".png", ".C", ".pdf"])#, ".pdf"])
    return




def CalcEfficiency(datasetsMgr, numPath, denPath, intLumi):
    # Definitions
    myList  = []
    index   = 0
    _kwargs = GetHistoKwargs(numPath, opts)        

    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():
        x = []
        y = []

        n = dataset.getDatasetRootHisto(numPath)
        n.normalizeToLuminosity(intLumi)
        num = n.getHistogram()
        d = dataset.getDatasetRootHisto(denPath)
        d.normalizeToLuminosity(intLumi)
        den = d.getHistogram()

        if "binList" in _kwargs:
            xBins   = _kwargs["binList"]
            nx      = len(xBins)-1
            num     = num.Rebin(nx, "", xBins)
            den     = den.Rebin(nx, "", xBins)


        for i in range(1, num.GetNbinsX()+1):
            nbin = num.GetBinContent(i)
            dbin = den.GetBinContent(i)

            if nbin < 0:
                nbin = 0
            if dbin < 0:
                nbin = 0
                dbin = 1
            if nbin > dbin:
                nbin = dbin

            x.append(num.GetBinLowEdge(i)+0.5*num.GetBinWidth(i))
            y.append(nbin/dbin)

        n     = num.GetNbinsX()
        eff = ROOT.TGraph(n, array.array("d",x), array.array("d",y))

        # Apply default style (according to dataset name)
        plots._plotStyles[dataset.getName()].apply(eff)
                          
        # Apply random histo styles and append
                          
        if "charged" in dataset.getName().lower():                              
            mass = dataset.getName().split("M_")[-1]
            s = styles.getSignalStyleHToTB_M(mass)
            s.apply(eff)

        # Append in list
        myList.append(histograms.HistoGraph(eff, plots._legendLabels[dataset.getName()], "lp", "P"))
            
    # Define save name
    saveName = "Eff_" + numPath.split("/")[-1] + "Over" + denPath.split("/")[-1]

    # Plot the efficiency
    p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    plots.drawPlot(p, saveName, **_kwargs)

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir, numPath.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath, saveFormats = [".png"])#, ".pdf"])
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
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists                                                                                                                                                                               
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved                                                                                                                                                        
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = saveName.replace("(", "_")
    saveName = saveName.replace(")", "")
    saveName = saveName.replace(" ", "")

    # For-loop: All save formats                                                                                                                                                                            
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, i==0)
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
    ANALYSISNAME = "TopTaggerEfficiency"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    SIGNALMASS   = [300, 500]
    #SIGNALMASS   = [500]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = None #"/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
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

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f_ext1" % m)
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
