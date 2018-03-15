#!/usr/bin/env python
'''
DESCRIPTION:
This script  produces trigger effciency plots. It takes as input the pseudo-multicrab
directory creating by running the JetTriggersSF analyser


USAGE:
./plotEfficiency.py  -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotEfficiency.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/Trigger/JetTriggersSF_170921_053850_FinalWithCut/ --url
./plotEfficiency.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/Trigger/JetTriggersSF_170921_053850_FinalWithCut/ --url -e ext


LAST USED:
./plotEfficiency.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/JetTriggersSF/JetTriggersSF_180308_194450/ -e "MuEnriched" --url

'''
#================================================================================================
#   Imports
#================================================================================================
import os
import sys
import ROOT
import array

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

from optparse import OptionParser
import getpass
import socket
import copy 

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
    Verbose("Luminosity = %s (pb)" % (lumi), True )
    return lumi

def GetRunRange(datasetsMgr):
    '''
    '''
    minRunRange = None
    maxRunRange = None
    nDataDatasets = len(datasetsMgr.getDataDatasets())

    # For-loop: All datasets
    for i, d in enumerate(datasetsMgr.getDataDatasets(), 1):
        if i == 1:
            minRunRange = d.getName().split("_")[-2]
        if i == nDataDatasets:
            maxRunRange = d.getName().split("_")[-1]
        runRange = d.getName().split("_")[-2] + " - " + d.getName().split("_")[-1]

        Verbose("Dataset   = %s" % (d.getName()), i==1)
        Verbose("Run Range = %s" % (runRange), False)

    runRange = minRunRange + " - " + maxRunRange
    Verbose("Run Range = %s - %s" % (minRunRange, maxRunRange), True)
    return minRunRange, maxRunRange, runRange


def Fit_Richards(xMin, xMax, p, histogram, par):
    '''
    Parameters:                                                     Limits:
    - p0 : Lower Asymptote                                        0  < p0 < 1
    - p1 : Upper Asymptote                                        0  < p1 < 1
    - p2 : Affects near which asymptote maximum growth occurs          p2 > 0
    - p3 : Growth rate
    - p4 : Inflection point                                       
    '''
    if len(par) == 0:
        return
    
    # Function 
    Richards = ROOT.TF1("Richards", "[0] + ( ([1]-[0]) / (1.0 +(   (2.0**[2]-1.0)* exp(-[3]*(x-[4]))))**(1.0/[2]))", xMin, xMax)
    
    # Limits
    Richards.SetParLimits(0, 0.0, 1.0)
    Richards.SetParLimits(1, 0.0, 1.0)
    Richards.SetParLimits(2, 0.0, 1.0)
    
    Richards.SetParName(0, "p0")
    Richards.SetParName(1, "p1")
    Richards.SetParName(2, "p2")
    Richards.SetParName(3, "p3")
    Richards.SetParName(4, "p4")
    
    p0 = par[0]
    p1 = par[1]
    p2 = par[2]
    p3 = par[3]
    p4 = par[4]
    
    Richards.SetParameter(0, p0)
    Richards.SetParameter(1, p1)
    Richards.SetParameter(2, p2)
    Richards.SetParameter(3, p3)
    Richards.SetParameter(4, p4)
    
    fitResult = histogram.Fit(Richards, "Richards")
    
    ROOT.gStyle.SetOptFit()

    chi2  = Richards.GetChisquare()
    ndf   = Richards.GetNDF()
    p0    = Richards.GetParameter(0)
    p1    = Richards.GetParameter(1)
    p2    = Richards.GetParameter(2)
    p3    = Richards.GetParameter(3)
    p4    = Richards.GetParameter(4)
    nPars = Richards.GetNpar()

    lines  = []
    align  = "{:<10} {:>20}"
    header = align.format("Variable", "Value")
    hLine  = "="*40
    lines.append(hLine)
    lines.append(header)
    lines.append(hLine)
    lines.append(align.format("chi2", chi2))
    lines.append(align.format("ndf", ndf))
    lines.append(align.format("chi2/dof", chi2/ndf))

    # For-loop: All parameters
    for i in range(0, nPars):
        l = align.format("p%s" % (i), Richards.GetParameter(i))
        lines.append(l)
    lines.append(hLine)
    lines.append("")    

    # For-loop: All lines
    if 0:
        for l in lines:
            print l

    aux.copyStyle(histogram, Richards)
    p.appendPlotObject(Richards)
    return

def GetHistoKwargs(histoName, opts):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    histoKwargs = {}
    #_moveLegend = {"dx": -0.10, "dy": -0.53, "dh": -0.2}
    _moveLegend = {"dx": -0.10, "dy": -0.68, "dh": -0.2}
    yMin1 = 0.5
    yMax1 = 1.05
    yMin2 = 0.75 #0.7
    yMax2 = 1.21 #1.3
    _kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "HLT Efficiency",
        "ratioYlabel"      : "Ratio",
        "ratio"            : True, 
        "stackMCHistograms": False,
        "ratioInvert"      : False, 
        "addMCUncertainty" : True, 
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": yMin1, "ymax": yMax1},
        "opts2"            : {"ymin": yMin2, "ymax": yMax2},
        "log"              : False,
        "moveLegend"       : _moveLegend,
        "cutBoxY"          : {"cutValue": 0.95, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": False, "ratioCanvas": True},
        }

    kwargs = copy.deepcopy(_kwargs)
    hName  = histoName.lower()

    ROOT.gStyle.SetNdivisions(510, "X") 
    if "pt6thjet" in hName:
        kwargs["xlabel"] = "p_{T} (GeV/c)"
        kwargs["opts"]   = {"xmin": 29.5, "xmax": 120, "ymin": yMin1, "ymax": yMax1}
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "eta6thjet" in hName:
        kwargs["xlabel"] = "#eta"
        kwargs["opts"]   = {"xmin": -2.49, "xmax": 2.49, "ymin": yMin1, "ymax": yMax1}
        #kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "phi6thjet" in hName:
        kwargs["xlabel"] = "#phi (rads)"
        kwargs["opts"]   = {"xmin": -3.0, "xmax": 3.0, "ymin": yMin1, "ymax": yMax1}

    if "ht" in hName:
        kwargs["xlabel"] = "H_{T} (GeV)"
        kwargs["opts"]   = {"xmin": 300.0, "ymin": yMin1, "ymax": yMax1}
        kwargs["cutBox"]  = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        n1 = 8 # primary divisions
        n2 = 5 # second order divisions
        n3 = 2 # third order divisions
        nDivs = n1 + 100*n2 + 10000*n3
        if 1:
            ROOT.gStyle.SetNdivisions(nDivs, "X")
        #ROOT.gStyle.SetNdivisions(8, "X")

    if "nbtagjets" in hName:
        kwargs["xlabel"] = "b-jet multiplicity"
        #kwargs["opts"]   = {"xmin": 0.0, "ymin": 0.0, "ymax": yMax1}
        kwargs["opts"]   = {"xmin": 2.0, "ymin": yMin1, "ymax": yMax1}
        kwargs["cutBox"] = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "pu" in hName:
        kwargs["xlabel"]     = "reco vertices"
        kwargs["opts"]       = {"xmin": 0.0, "ymin": yMin1, "ymax": yMax1}
        #kwargs["moveLegend"] = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }

    if "csv" in hName:
        kwargs["xlabel"] = "CSV"
        kwargs["opts"]   = {"xmin": 0.0, "ymin": yMin1, "ymax": yMax1}
 
    if "jetmulti" in hName:
        kwargs["xlabel"] = "jet multiplicity"
        kwargs["opts"]   = {"xmin": 6.0, "xmax": 14.0, "ymin": yMin1, "ymax": yMax1}
        kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "bjetmulti" in hName:
        kwargs["xlabel"] = "b-jet multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "ymin": yMin1, "ymax": yMax1}
        kwargs["cutBox"] = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    return kwargs


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


def GetEfficiency(datasetsMgr, datasets, numerator="Numerator",denominator="Denominator", **kwargs):
    '''
    TEfficiency method:
    See https://root.cern.ch/doc/master/classTEfficiency.html    
    
    '''
    lumi = GetLumi(datasetsMgr)

    # Select Statistic Options
    statOption = ROOT.TEfficiency.kFCP
    '''
    statOption = ROOT.TEfficiency.kFCP      # Clopper-Pearson
    statOption = ROOT.TEfficiency.kFNormal  # Normal Approximation
    statOption = ROOT.TEfficiency.kFWilson  # Wilson
    statOption = ROOT.TEfficiency.kFAC      # Agresti-Coull
    statOption = ROOT.TEfficiency.kFFC      # Feldman-Cousins
    statOption = ROOT.TEfficiency.kBBJeffrey # Jeffrey
    statOption = ROOT.TEfficiency.kBBUniform # Uniform Prior
    statOption = ROOT.TEfficiency.kBBayesian # Custom Prior
    '''
    
    first  = True
    teff   = ROOT.TEfficiency()
    #    teff.SetStatisticOption(statOption)

    # For-loop: All datasets
    for dataset in datasets:
        
        num = dataset.getDatasetRootHisto(numerator)
        den = dataset.getDatasetRootHisto(denominator)

        # 
        if dataset.isMC():
            num.normalizeToLuminosity(lumi)
            den.normalizeToLuminosity(lumi) 

        # Get Numerator and Denominator
        n = num.getHistogram()
        d = den.getHistogram()
        
        if d.GetEntries() == 0 or n.GetEntries() == 0:
            msg =  "Denominator Or Numerator has no entries"
            Print(ErrorStyle() + msg + NormalStyle(), True)
            continue
        
        # Check Negatives
        CheckNegatives(n, d, True)
        
        # Remove Negatives
        RemoveNegatives(n)
        #RemoveNegatives(d)
       
        NumeratorBins   = n.GetNbinsX()
        DenominatorBins = d.GetNbinsX()


        # Sanity Check
        if (NumeratorBins != DenominatorBins) :
            raise Exception("Numerator and Denominator Bins are NOT equal!")
        
        nBins = d.GetNbinsX()
        xMin  = d.GetXaxis().GetXmin()
        xMax  = d.GetXaxis().GetXmax()
        
        # ----------------------------------------------------------------------------------------- # 
        #      Ugly hack to ignore EMPTY (in the wanted range) histograms with overflows/underflows
        # ----------------------------------------------------------------------------------------- #
        if 0:
            print "\n"
            print "=========== getEfficiency:"
            print "Dataset             = ", dataset.getName()
            
            print "Numerator  :", n.GetName(), "   entries=", n.GetEntries(), " Bins=", n.GetNbinsX(), " Low edge=", n.GetBinLowEdge(1)
            print "Denominator:", d.GetName(), "   entries=", d.GetEntries(), " Bins=", d.GetNbinsX(), " Low edge=", d.GetBinLowEdge(1)
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

        Verbose("Passed the sanity check", True)
        
        eff = ROOT.TEfficiency(n, d)
        eff.SetStatisticOption(statOption)
        
        # For-loop: All bins
        if 0:
            for iBin in range(1, nBins+1):
                print iBin, "x=", n.GetBinLowEdge(iBin), " Num=", n.GetBinContent(iBin),  " Den=", d.GetBinContent(iBin)," Eff=", eff.GetEfficiency(iBin)
            
        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
        eff.SetWeight(weight)
        
        if first:
            teff  = eff
            first = False
            if dataset.isData():
                tn = n
                td = d
        else:
            teff.Add(eff)
            
            if dataset.isData():
                tn.Add(n)
                td.Add(d)
                
        if dataset.isData():
            teff = ROOT.TEfficiency(tn, td)
            teff.SetStatisticOption(statOption)
        
    Verbose("Final tEff", True)
    if 0:
        for iBin in range(1,nBins+1):
            print iBin, "x=", n.GetBinLowEdge(iBin)," Efficiency=", teff.GetEfficiency(iBin), " Weight = ", teff.GetWeight()
    return convert2TGraph(teff)


def convert2TGraph(tefficiency):
    '''
    '''
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()

    xMin= h.GetXaxis().GetXmin()
    xMax= h.GetXaxis().GetXmax()

    for i in range(1,n+1):
        #print "x = ", h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i), "      y = ",tefficiency.GetEfficiency(i)
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

        tgraph= ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                       array.array("d",y),
                                       array.array("d",xerrl),
                                       array.array("d",xerrh),
                                       array.array("d",yerrl),
                                       array.array("d",yerrh))
    return tgraph


def RemoveNegatives(histo):
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
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
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
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

def main(opts):
    
    # Suppress warnings about weight being re-applied
    ROOT.gErrorIgnoreLevel = ROOT.kError 

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)

    # Get list of eras, modes, and optimisation modes
    erasList      = dsetMgrCreator.getDataEras()
    modesList     = dsetMgrCreator.getSearchModes()
    optList       = dsetMgrCreator.getOptimizationModes()
    sysVarList    = dsetMgrCreator.getSystematicVariations()
    sysVarSrcList = dsetMgrCreator.getSystematicVariationSources()
    
    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        else:
            pass
        optModes = optList
    else:
        optModes = [opts.optMode]

    opts.optMode = ""
    mcrabName    = opts.mcrab
    RunEra       = mcrabName.split("_")[1]

    # Setup ROOT and style
    ROOT.gROOT.SetBatch(opts.batchMode)
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(True)
    
    # Setup & configure the dataset manager
    datasetsMgr = GetDatasetsFromDir(opts)

    # Get run-range 
    minRunRange, maxRunRange, runRange = GetRunRange(datasetsMgr)

    # Get int lumi
    intLumi  = GetLumi(datasetsMgr)

    # Update to PU & load luminosities 
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities()
    #datasetsMgr.normalizeMCByLuminosity()

    # Print luminisoties and cross-sections
    datasetsMgr.PrintLuminosities()
    datasetsMgr.PrintCrossSections()

    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
    plots.mergeRenameReorderForDataMC(datasetsMgr)
    
    # Get datasets
    datasetsMgr.mergeMC()
    dataset_Data = datasetsMgr.getDataDatasets()
    dataset_MC   = datasetsMgr.getMCDatasets()

    # Define lists of Triggers to be plotted and Variables 
    trgList = ["1BTag", "2BTag", "OR", "OR_PFJet450"]
    xVars   = ["pt6thJet", "eta6thJet", "phi6thJet", "Ht", "nBTagJets", "pu", "JetMulti", "BJetMulti"]
    nPlots  = len(trgList)*len(xVars)
    counter =  0

    # For-loop: All signal triggers
    for i, trg in enumerate(trgList, 1):
        
        # For-loop: All x-variables
        for j, xVar in enumerate(xVars, 1):
            counter+=1
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (nPlots), "%s Vs %s" % (trg, xVar))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)

            # Define names
            hNumerator   = "hNum_%s_RefTrg_OfflineSel_Signal%s" % (xVar, trg)
            hDenominator = "hDen_%s_RefTrg_OfflineSel" % (xVar)
            plotName     = "Eff_%s_%s" % (xVar, trg)
            print plotName
            # Get Efficiency Plots
            _kwargs  = GetHistoKwargs(xVar, opts)
            eff_Data = GetEfficiency(datasetsMgr, dataset_Data, hNumerator, hDenominator , **_kwargs)
            eff_MC   = GetEfficiency(datasetsMgr, dataset_MC, hNumerator, hDenominator, **_kwargs) 
                       
            # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
        
            # Create the plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data", "p", "P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC"  , "p", "P"),
                                     saveFormats=[])                  

            # Define the legend entries
            p.histoMgr.setHistoLegendLabelMany(
                {
                    "eff_Data": "Data", 
                    "eff_MC"  : "Simulation"
                    }
                )
            
            # Draw and save the plot
            p.setLuminosity(intLumi)
            plots.drawPlot(p, plotName, **_kwargs)
                                                   
            # Draw
            histograms.addText(0.65, 0.06, "Runs "+ runRange, 17)
            histograms.addText(0.65, 0.10, "2016", 17)

            # Save the canvas to a file
            SavePlot(p, plotName, os.path.join(opts.saveDir, opts.optMode), saveFormats=[".pdf", ".png", ".C"] )

    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
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
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    VERBOSE      = False
    BATCHMODE    = True
    SAVEDIR      = None
    OPTMODE      = None
    ANALYSISNAME = "JetTriggersSF"
    URL          = False

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    
    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store",
                      help="Path to the multicrab directory for input")
    
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE,
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)
    
    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store",
                      help="List of datasets in mcrab to include")
    
    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA,
                      help="Override default dataEra [default: %s]" % DATAERA)
    
    parser.add_option("-e", "--excludeTasks", dest="excludeTasks" , default="", type="string",
                      help="Exclude this dataset(s) from action [default: '']")
    
    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE,
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)
    
    (opts, parseArgs) = parser.parse_args()

    # Sanity check
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Efficiency")

    # Program execution
    main(opts)
        
    if not opts.batchMode:
        raw_input("=== plotEfficiency.py: Press any key to quit ROOT ...")
