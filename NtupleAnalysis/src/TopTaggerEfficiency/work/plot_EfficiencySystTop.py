#!/usr/bin/env python
'''
DESCRIPTION:
This scipt is used to investigate 
the top tagging differences when using 
different MC samples and generators to account
for various effects such as:
- ISR/FSR
- Event Generator
- ME-PS matching (high-pT radiation)
- Colour Reconnection
etc...


USAGE:
./plot_EfficiencySystTop.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type partonShower
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type showerScales
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180603_SystTop_hadronic_BDTtraining_ptRew13TeV --folder topbdtSelection_ --type mTop
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_195638_massCut400_All --folder topbdtSelection_ --type partonShower --url
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_194156_massCut300_All --folder topbdtSelection_ --type partonShower --url
./plot_EfficiencySystTop.py -m TopTaggerEfficiency_180608_200027_massCut1000_All --folder topbdtSelection_ --type colourReconnection


LAST USED: 
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All --type showerScales 
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All --type highPtRadiation
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All --type mTop 
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All --type partonShower
./plot_EfficiencySystTop.py -m /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All --type evtGen

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
    return ["QCD_bEnriched_HT200to300",
            "QCD_bEnriched_HT300to500",
            "QCD_bEnriched_HT500to700",
            "QCD_bEnriched_HT700to1000",
            #"QCD_HT1000to1500",
            "QCD_bEnriched_HT1000to1500",
            "QCD_bEnriched_HT1500to2000",
            "QCD_bEnriched_HT2000toInf",
            #"QCD_HT1500to2000_ext1",
            #"QCD_HT2000toInf",
            #"QCD_HT2000toInf_ext1",
            #"QCD_HT200to300",
            #"QCD_HT200to300_ext1",
            #"QCD_HT1000to1500_ext1",
            #"QCD_HT100to200",
            #"QCD_HT1500to2000",
            #"QCD_HT500to700_ext1",
            #"QCD_HT50to100",
            #"QCD_HT700to1000",
            #"QCD_HT700to1000_ext1",
            #"QCD_HT300to500",
            #"QCD_HT300to500_ext1",
            #"QCD_HT500to700"
            ]

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
    h     = histoName.lower()
    bins  = []
    units = ""
    kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "Efficiency", #/ %.1f ",
        "ratioYlabel"      : "Ratio ", #"TT/TT_X",
        "binList"          : [],
        "errorType"        : "errorPropagation", 
        "ratio"            : True,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "xmax":600, "ymaxfactor": 1.2},
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "moveLegend"       : {"dx": -0.12, "dy": -0.40, "dh": +0.05*(-4+opts.nDatasets)},  #"dh": +0.18}, 
        "cutBoxY"          : {"cutValue": 1.10, "fillColor": ROOT.kGray+1, "fillStyle": 3001, "box": False, "line": True, "greaterThan": True, "mainCanvas": False, "ratioCanvas": True, "mirror": True}
        }
    
    if "pt" in h:
        ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X") 
        units             = "GeV/c"
        kwargs["xlabel"]  = "p_{T} (%s)" % (units)
        bins              = [i for i in range(0, 1000+50, 50)]
        if opts.folder == "topbdtSelection_":
            #bins          = [i for i in range(0, 600+100, 100)] + [800]
            bins              = [0, 100, 200, 300, 400, 500, 600]
        else:
            bins          = []


    if units != "":
        kwargs["ylabel"] += (" / " + units)
    if len(bins) > 0:
        kwargs["binList"] = array.array('d', bins)
    return kwargs


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
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

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        if 0:
            plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Print dataset information before removing anything?
        if 0:
            datasetsMgr.PrintInfo()

        # Print datasets info summary
        datasetsMgr.PrintInfo()

        # Re-order datasets
        datasetOrder = []
        haveQCD = False
        for d in datasetsMgr.getAllDatasets():
            if "QCD" in d.getName():
                haveQCD = True
            datasetOrder.append(d.getName())
            
        # Append signal datasets
        datasetsMgr.selectAndReorder(datasetOrder)


        Numerator = ["AllTopQuarkPt_MatchedBDT",
                     "TrijetFakePt_BDT",
                     "AllTopQuarkPt_MatchedBDT",
                     "AllTopQuarkPt_Matched",
                     ]
        Denominator = ["AllTopQuarkPt_Matched",
                       "TrijetFakePt",
                       "TopQuarkPt",
                       "TopQuarkPt",
                       ]

        eff_def = ["genuineTop",
                   "fakeTop",
                   "inclusiveTop",
                   "matching",
                   ]
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        counter =  0
        opts.nDatasets = len(datasetsMgr.getAllDatasets())
        nPlots  = len(Numerator)
        # For-loop: All numerator-denominator pairs
        #for var in VariableList:
        for i in range(len(Numerator)):
            numerator   = os.path.join(opts.folder, Numerator[i])
            denominator = os.path.join(opts.folder, Denominator[i])
            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50} {:<2} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s" % (numerator), "/", "%s" % (denominator))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            PlotEfficiency(datasetsMgr, numerator, denominator, eff_def[i])

        if 0:
            hNumerator   = "AllTopQuarkPt_MatchedBDT"
            hDenominator = "AllTopQuarkPt_Matched"
            numerator    = os.path.join(opts.folder, hNumerator)
            denFolder    = opts.folder
            #denFolder    = denFolder.replace("Genuine", "")
            #print "denFolder", denFolder
            denominator  = os.path.join(denFolder, hDenominator)
            
            PlotEfficiency(datasetsMgr, numerator, denominator)            
            
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
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


def RemoveNegatives(histo):
    '''
    Removes negative bins from histograms
    '''
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return


def PlotEfficiency(datasetsMgr, numPath, denPath, eff_def):  
    # Definitions
    myList      = []
    _kwargs     = GetHistoKwargs(numPath, opts)        
    nx          = 0
    if len(_kwargs["binList"]) > 0:
        xBins   = _kwargs["binList"]
        nx      = len(xBins)-1
    counter     = 0

    # For-loop: All datasets
    for dataset in datasetsMgr.getAllDatasets():

        if dataset.isMC():
            n   = dataset.getDatasetRootHisto(numPath)
            d   = dataset.getDatasetRootHisto(denPath)
            num = n.getHistogram()
            den = d.getHistogram()

            if nx > 0:
                num = num.Rebin(nx, "", xBins)
                den = den.Rebin(nx, "", xBins)
        else:
            num = dataset.getDatasetRootHisto(numPath).getHistogram()
            den = dataset.getDatasetRootHisto(denPath).getHistogram()
            if nx > 0:
                num = num.Rebin(nx, "", xBins)
                den = den.Rebin(nx, "", xBins)

        # Calculations    
        total    = den.Integral(0, den.GetXaxis().GetNbins()+1)
        selected = num.Integral(0, num.GetXaxis().GetNbins()+1)

        if 0:
            print "Numerical Efficiency", numPath, dataset.getName(), ":", round(selected/total, 3)
            
        # Sanity checks
        if den.GetEntries() == 0 or num.GetEntries() == 0:
            continue
        if num.GetEntries() > den.GetEntries():
            continue
        
        # Create Efficiency plots with Clopper-Pearson stats
        eff = ROOT.TEfficiency(num, den) 
        eff.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP
        
        datasetTT = datasetsMgr.getDataset("TT")
        # Get the histograms
        numTT = datasetTT.getDatasetRootHisto(numPath).getHistogram()
        denTT = datasetTT.getDatasetRootHisto(denPath).getHistogram()
        if nx > 0:
            numTT = numTT.Rebin(nx, "", xBins) #num.Rebin(nx, "", xBins)
            denTT = denTT.Rebin(nx, "", xBins) #den.Rebin(nx, "", xBins)


        '''
        for i in range(1, num.GetNbinsX()+1):
            nbin = num.GetBinContent(i)
            dbin = den.GetBinContent(i)
            nbinTT = numTT.GetBinContent(i)
            dbinTT = denTT.GetBinContent(i)
            eps = nbin/dbin
            epsTT = nbinTT/dbinTT
            ratioTT = eps/epsTT
            if ratioTT > 1:
                ratioTT = 1/ratioTT
            #print "bin: ", i, "eps: ", round(eps,5) , "epsTT: ", round(epsTT,5)
            #print "bin: ", i, "eps/epsTT: ", (1.0 - round(ratioTT, 3))*100
        '''
        eff_ref = ROOT.TEfficiency(numTT, denTT) 
        eff_ref.SetStatisticOption(ROOT.TEfficiency.kFCP) #FCP

        # Convert to TGraph
        gEff    = convert2TGraph(eff)
        gEffRef = convert2TGraph(eff_ref)
            
        # Style definitions
        stylesDef = styles.ttStyle
        styles0 = styles.signalStyleHToTB300                                            
        styles1 = styles.signalStyleHToTB500
        styles2 = styles.signalStyleHToTB800
        styles3 = styles.signalStyleHToTB500
        styles4 = styles.signalStyleHToTB1000
        styles5 = styles.signalStyleHToTB2000
        styles6 = styles.signalStyleHToTB180
        styles7 = styles.signalStyleHToTB3000
        styles8 = styles.signalStyleHToTB200

        if dataset.getName() == "TT":
            styles.ttStyle.apply(gEffRef)
            legend_ref = "t#bar{t}"
            if opts.type == "partonShower":
                legend_ref = "t#bar{t} (Pythia8)"
            elif opts.type == "evtGen": 
                legend_ref = "t#bar{t} (Powheg)"
            refGraph = histograms.HistoGraph(gEffRef, legend_ref, "p", "P")
        else:
            styles.markerStyles[counter].apply(gEff)
            legend  = dataset.getName().replace("TT_", "t#bar{t} (").replace("isr", "ISR ").replace("fsr", "FSR ")
            legend  = legend.replace("hdamp", "hdamp ").replace("DOWN", "down").replace("UP", "up")
            legend  = legend.replace("mtop1665", "m_{t} = 166.5 GeV")
            legend  = legend.replace("mtop1695", "m_{t} = 169.5 GeV")
            legend  = legend.replace("mtop1715", "m_{t} = 171.5 GeV")
            legend  = legend.replace("mtop1735", "m_{t} = 173.5 GeV")
            legend  = legend.replace("mtop1755", "m_{t} = 175.5 GeV")
            legend  = legend.replace("mtop1785", "m_{t} = 178.5 GeV")
            legend  = legend.replace("TuneEE5C", "Herwig++")
            legend += ")"
            counter+=1
            #myList.append(histograms.HistoGraph(gEff, legend, "lp", "P"))
            myList.append(histograms.HistoGraph(gEff, legend, "p", "P"))
         
   
    units = "GeV/c"
    if eff_def == "fakeTop":
        _kwargs["xlabel"]  = "candidate p_{T} (%s)" % (units)
    elif eff_def == "inclusiveTop" or eff_def == "genuineTop":
        _kwargs["xlabel"]  = "generated top p_{T} (%s)" % (units)
    else:
        _kwargs["xlabel"]  = "p_{T} (%s)" % (units)



    # Define stuff
    numPath  = numPath.replace("AfterAllSelections_","")
    saveName = "Efficiency_%s_%s" % (eff_def, opts.type) 
    #saveName = saveName.replace("__", "_Inclusive_")

    # Plot the efficiency
    p = plots.ComparisonManyPlot(refGraph, myList, saveFormats=[])
    savePath = os.path.join(opts.saveDir, opts.optMode)    
    plots.drawPlot(p, savePath, **_kwargs)

    # Save plot in all formats
    SavePlot(p, saveName, savePath, saveFormats = [".png", ".pdf", ".C"])
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
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    NORMALISE    = False
    FOLDER       = "topbdtSelection_"
    TYPE         = "mtop"

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

    parser.add_option("--type", dest="type", type="string", default=TYPE, 
                      help="The type of comparison to perform wrt the default ttbar sample (showerScales, highPtRadiation, colourReconnection, mTop) [default: %s]" % TYPE)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

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

    # Append folder to save directory path
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="TopTagSystematics")

    # See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopSystematics
    allowedTypes = ["showerScales", "highPtRadiation", "colourReconnection", "mTop", "evtGen", "partonShower"]
    if opts.type not in allowedTypes:
        Print("Invalid type \"%s\" selected. Please choose one of the following: %s" % (opts.type, ", ".join(allowedTypes)), True)
        sys.exit()
    
    # Apply type-related changes
    # opts.saveDir = os.path.join(opts.saveDir, opts.type)
    if opts.type == "showerScales": #ISR/FSR
        opts.excludeTasks = "mtop|hdamp|evtgen|erdON|EE5C"
    elif opts.type == "highPtRadiation": #hdamp (TOP-16-021)
        opts.excludeTasks = "mtop|evtgen|erdON|fsr|isr|EE5C"
    elif opts.type == "colourReconnection": #erdON
        opts.excludeTasks = "mtop|hdamp|evtgen|fsr|isr|EE5C"
    elif opts.type == "mTop": #top mass
        opts.excludeTasks = "hdamp|evtgen|erdON|fsr|isr|EE5C"
    elif opts.type == "evtGen": #EvtGen is a MC event generator that simulates the decays of heavy flavour particles
        opts.excludeTasks = "mtop|hdamp|erdON|fsr|isr|EE5C"
    elif opts.type == "partonShower": #EE5C
        opts.excludeTasks = "mtop|hdamp|erdON|fsr|isr|evtgen"
    else:
        raise Exception("This should NEVER be reached!")
    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_EfficiencySystTop.py: Press any key to quit ROOT ...")
