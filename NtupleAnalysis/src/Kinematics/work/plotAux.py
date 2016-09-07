#!/usr/bin/env python

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket
import math

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

import ROOT
import array


#================================================================================================
# Variable Definition
#================================================================================================
htb = "ChargedHiggs_HplusTB_HplusToTB_"
styleDict = {
    htb + "M_500"      : styles.signal500Style, 
    htb + "M_400"      : styles.signal400Style,
    htb + "M_300"      : styles.signal300Style,
    htb + "M_200"      : styles.signal200Style,
    "QCD"              : styles.qcdFillStyle, #qcdStyle, #qcdFillStyle,
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
    "TT"               : styles.ttStyle,
    #"TT"               : styles.ewkStyle,
}


#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return


def SetLogAndGrid(p, **kwargs):
    '''
    '''
    HasKeys(["createRatio", "logX", "logY", "gridX", "gridY"], **kwargs)
    ratio = kwargs.get("createRatio")
    logX  = kwargs.get("logX")
    logY  = kwargs.get("logY")
    logZ  = kwargs.get("logZ")
    gridX = kwargs.get("gridX")
    gridY = kwargs.get("gridY")
    
    if ratio:
        p.getPad1().SetLogx(logX)
        p.getPad1().SetLogy(logY)
        #
        p.getPad2().SetLogx(logX)
        p.getPad2().SetLogy(logY)
        #
        p.getPad1().SetGridx(gridX)
        p.getPad1().SetGridy(gridY)
        #
        p.getPad2().SetGridx(gridX)
        p.getPad2().SetGridy(gridY)
    else:
        p.getPad().SetLogx(logX)
        p.getPad().SetLogy(logY)
        if logZ != None:
            p.getPad().SetLogz(logZ)
        p.getPad().SetGridx(gridX)
        p.getPad().SetGridy(gridY)
    return

    
def GetSavePath(**kwargs):
    '''
    '''
    HasKeys(["savePath", "analysis", "verbose"], **kwargs)
    savePath = kwargs.get("savePath")
    analysis = kwargs.get("analysis")
    verbose  = kwargs.get("verbose")
    
    Verbose("Constructing path where plots will be saved", verbose)    
    if savePath != None:
        return savePath
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def GetSaveName(savePathNew, hName, **kwargs):
    '''
    '''
    HasKeys(["savePath", "verbose"], **kwargs)
    verbose      = kwargs.get("verbose")
    cutDirection = kwargs.get("cutDirection")

    Verbose("Constructing name of plot to  be saved", verbose)    
    forbidden   = ["/"]
    replacement = "_"
    for f in forbidden:
        if f in hName:
            Print("Replacing forbidden character \"%s\" with \"%s\" in saveName  \"%s\"" % (f, replacement, hName))
            hName = hName.replace(f, replacement)
            
    if cutDirection == None:
        saveName = os.path.join(savePathNew, hName)
    elif cutDirection == ">":
        saveName = os.path.join(savePathNew, hName + "_GreaterThan")
    else:
        saveName = os.path.join(savePathNew, hName + "_LessThan")
        
    return saveName



def GetSavePathAndName(hName, **kwargs):
    '''
    '''
    HasKeys(["verbose"], **kwargs)
    verbose  = kwargs.get("verbose")

    Verbose("Getting save path and name", verbose)
    savePathNew = GetSavePath(**kwargs)
    saveName    = GetSaveName(savePathNew, hName, **kwargs)
    return savePathNew, saveName



def GetCutEfficiencyTGraphs(datasetsMgr, histoName, statOpt, **kwargs):
    '''
    '''
    HasKeys(["refDataset", "drawStyle", "legStyle", "cutDirection"], **kwargs)
    refGraph     = None
    otherGraphs  = []
    refDataset   = kwargs.get("refDataset")
    drawStyle    = kwargs.get("drawStyle")
    legStyle     = kwargs.get("legStyle")
    legLabel     = plots._legendLabels[refDataset]
    
    refHisto, otherHistos = GetCutEfficiencyHistos(datasetsMgr, histoName, statOpt, **kwargs)
    refGraph = histograms.HistoGraph(refHisto, legLabel, legStyle, drawStyle)

    # For-loop: All efficiency histos
    for h in otherHistos:
        legLabel = plots._legendLabels[h.GetName()]
        otherGraphs.append(histograms.HistoGraph(h, legLabel, legStyle, drawStyle))

    if refGraph == None:
        raise Exception("The \"reference\" graph is None!")
    elif len(otherGraphs) < 1:
        raise Exception("The \"other\" graph list empty!")    
    else:
        return refGraph, otherGraphs



def GetCutEfficiencyHistos(datasetsMgr, histoName, statOpt, **kwargs):
    '''
    '''
    HasKeys(["verbose", "refDataset", "cutDirection"], **kwargs)
    refDataset  = kwargs.get("refDataset")
    refHisto    = None
    otherHistos = []

   # For-loop: All dataset objects            
    for d in datasetsMgr.getAllDatasets():

        histo = GetCutEfficiencyHisto(datasetsMgr.getDataset(d.getName()), histoName, statOpt, **kwargs)
        if d.getName() == refDataset:
            refHisto = histo
        else:
            otherHistos.append(histo)
    return refHisto, otherHistos

    
    
def GetCutEfficiencyHisto(dataset, histoName, statOpt, **kwargs):
    '''
    See https://root.cern.ch/doc/master/classTEfficiency.html
    '''
    HasKeys(["verbose", "normalizeTo", "cutDirection"], **kwargs)
    verbose     = kwargs.get("verbose")
    normalizeTo = kwargs.get("normalizeTo")
    cutDirection= kwargs.get("cutDirection")
    Verbose("Calculating the cut-efficiency (%s) for histo with name %s" % (cutDirection, histoName) )
        
    # Choose statistics options
    statOpts = ["kFCP", "kFNormal", "KFWilson", "kFAC", "kFFC", "kBJeffrey", "kBUniform", "kBayesian"]
    if statOpt not in statOpts:
        raise Exception("Invalid statistics option \"%s\". Please choose one from the following:\n\t%s" % (statOpt, "\n\t".join(statOpts)))

    if statOpt == "kFCP":
        statOption = ROOT.TEfficiency.kFCP      # Clopper-Pearson
    elif statOpt == "kFNormal":
        statOption = ROOT.TEfficiency.kFNormal  # Normal Approximation
    elif statOpt == "kFWilson":
        statOption = ROOT.TEfficiency.kFWilson  # Wilson
    elif statOpt == "kFAC":
        statOption = ROOT.TEfficiency.kFAC      # Agresti-Coull
    elif statOpt == "kFFC":
        statOption = ROOT.TEfficiency.kFFC      # Feldman-Cousins
    elif statOpt == "kBJeffrey":
        statOption = ROOT.TEfficiency.kBJeffrey # Jeffrey
    elif statOpt == "kBUniform":
        statOption = ROOT.TEfficiency.kBUniform # Uniform Prior
    elif statOpt == "kBayesian":
        statOption = ROOT.TEfficiency.kBayesian # Custom Prior
    else:
        raise Exception("This should never be reached")    
        

    # Declare variables & options
    first  = True
    isData = False
    teff   = ROOT.TEfficiency()

    # Get the ROOT histogram
    rootHisto = dataset.getDatasetRootHisto(histoName)

    # Normalise the histogram
    NormalizeRootHisto(rootHisto, dataset.isMC(), normalizeTo)

    ## Get a clone of the wrapped histogram normalized as requested.
    h = rootHisto.getHistogram()
    titleX   = h.GetXaxis().GetTitle()
    binWidth = h.GetXaxis().GetBinWidth(0)
    titleY   = "efficiency (%s) / %s" % (cutDirection, GetBinwidthDecimals(binWidth) % (binWidth) )
    
    # If empty return
    if h.GetEntries() == 0:
        return

    # Create the numerator/denominator histograms
    numerator   = h.Clone("Numerator")
    denominator = h.Clone("Denominator")

    # Reset the numerator/denominator histograms
    numerator.Reset()
    denominator.Reset()

    # Calculate the instances passing a given cut (all bins)
    nBinsX = h.GetNbinsX()+1
    for iBin in range(1, nBinsX):

        nTotal = h.Integral(0, nBinsX)

        if cutDirection == ">":
            nPass  = h.Integral(iBin+1, nBinsX)
        elif cutDirection == "<":
            nPass  = nTotal - h.Integral(iBin+1, nBinsX)
        else:
            raise Exception("Invalid cut direction  \"%s\". Please choose either \">\" or \"<\"" % (cutDirection))

        # Sanity check
        if nPass < 0:
            nPass = 0
            
        # Fill the numerator/denominator histograms
        # print "iBin = %s, nPass = %s, nTotal = %s" % (iBin, nPass, nTotal)
        numerator.SetBinContent(iBin, nPass)
        numerator.SetBinError(iBin, math.sqrt(nPass)/10)
        #
        denominator.SetBinContent(iBin, nTotal)
        denominator.SetBinError(iBin, math.sqrt(nTotal)/10)
        
    # Check for negative values
    CheckNegatives(numerator, denominator)

    # Create TEfficiency object using the two histos
    eff = ROOT.TEfficiency(numerator, denominator)
    eff.SetStatisticOption(statOption)
    Verbose("The statistic option was set to %s" % (eff.GetStatisticOption()) )

    # Save info in a table (debugging)
    table    = []
    hLine    = "="*70
    msgAlign = '{:<5} {:<20} {:<20} {:<20}'
    title    = msgAlign.format("Bin", "Efficiency", "Error-Low", "Error-Up")
    table.append("\n" + hLine)
    table.append(title)
    table.append(hLine)
    for iBin in range(1, nBinsX):
        e      = eff.GetEfficiency(iBin)
        errLow = eff.GetEfficiencyErrorLow(iBin)
        errUp  = eff.GetEfficiencyErrorUp(iBin)
        values = msgAlign.format(iBin, e, errLow, errUp)
        table.append(values)
    table.append(hLine)

    # Verbose mode
    if verbose:
        for l in table:
            print l

    weight = 1
    if dataset.isMC():
        weight = dataset.getCrossSection()
    eff.SetWeight(weight)
        
    if first:
        teff = eff
        if dataset.isData():
            tn = numerator
            td = denominator
        first = False
    else:
        teff.Add(eff)
        if dataset.isData():
            tn.Add(numerator)
            td.Add(denominator)
    if isData:
        teff = ROOT.TEfficiency(tn, td)
        teff.SetStatisticOption(self.statOption)

    style = styleDict[dataset.getName()]
    return Convert2TGraph(teff, dataset, style, titleX, titleY)


def getEfficiency(datasets, numerator="Numerator", denominator="Denominator"):
    '''
    '''
    statOption = ROOT.TEfficiency.kFNormal
    # statOption = ROOT.TEfficiency.kFCP # Clopper-Pearson
    # statOption = ROOT.TEfficiency.kFFC # Feldman-Cousins

    first  = True
    isData = False
    teff   = ROOT.TEfficiency()

    for dataset in datasets:
        n = dataset.getDatasetRootHisto(numerator).getHistogram()                                               
        d = dataset.getDatasetRootHisto(denominator).getHistogram()

        if d.GetEntries() == 0:
            continue

        CheckNegatives(n, d, True)
        RemoveNegatives(n)
        print dataset.getName(),"entries",n.GetEntries(),d.GetEntries()
        print "    bins",n.GetNbinsX(),d.GetNbinsX()
        print "    lowedge",n.GetBinLowEdge(1),d.GetBinLowEdge(1)
        eff = ROOT.TEfficiency(n,d)
        eff.SetStatisticOption(statOption)

        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
            for i in range(1,d.GetNbinsX()+1):
                print "    bin",i,d.GetBinLowEdge(i),n.GetBinContent(i),d.GetBinContent(i)
        eff.SetWeight(weight)

        if first:
            teff = eff
            if dataset.isData():
                tn = nPass
                td = nTotal
            first = False
        else:
            teff.Add(eff)
            if dataset.isData():
                tn.Add(nPass)
                td.Add(nTotal)
    if isData:
        teff = ROOT.TEfficiency(tn, td)
        teff.SetStatisticOption(self.statOption)
    return Convert2TGraph(teff)


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
        nBin = n.GetBinContent(i)
        dBin = d.GetBinContent(i)

        table.append(txtAlign.format(i, "%0.8f" % (nBin), "%0.8f" % (dBin) ))

        # Numerator > Denominator
        if nBin > dBin:
            n.SetBinContent(i, dBin)

        # Numerator < 0
        if nBin < 0:
            n.SetBinContent(i, 0)

        # Denominator < 0
        if dBin < 0:
            n.SetBinContent(i, 0)
            d.SetBinContent(i, 0)

    if verbose:
        for r in table:
            print r
    return


def RemoveNegatives(histo):
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return


def Convert2TGraph(tefficiency, dataset, style, titleX, titleY):
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

    tgraph = ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                    array.array("d",y),
                                    array.array("d",xerrl),
                                    array.array("d",xerrh),
                                    array.array("d",yerrl),
                                    array.array("d",yerrh))

    tgraph.SetName(dataset.getName())
    tgraph.GetXaxis().SetTitle(titleX)
    tgraph.GetYaxis().SetTitle(titleY)

    style.apply(tgraph)
    return tgraph


def GetDatasetsFromDir(mcrab, analysis):

    datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], analysisName=analysis)
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="M_180|M_220|M_250")

    # Inform user of datasets retrieved
    Verbose("Got the following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        Verbose( "\t", d.getName(), False)
    return datasets



def GetHistosForPlotter(datasetsMgr, histoName, **kwargs):
    '''
    '''
    HasKeys(["refDataset", "drawStyle", "legStyle"], **kwargs)
    refHisto     = None
    otherHistos  = []
    refDataset   = kwargs.get("refDataset")
    drawStyle    = kwargs.get("drawStyle")
    legStyle     = kwargs.get("legStyle")
    normalizeTo  = kwargs.get("normalizeTo")
    histoType    = None

    # For-loop: All dataset objects
    for d in datasetsMgr.getAllDatasets():
        rootHisto = datasetsMgr.getDataset(d.getName()).getDatasetRootHisto(histoName)

        # Apply Normalization
        NormalizeRootHisto(rootHisto, d.isMC(), normalizeTo)

        # Get the histogram
        histo     = rootHisto.getHistogram()
        histoType = type(histo)
        legName   = plots._legendLabels[d.getName()]

        # Apply Styling
        styleDict[d.getName()].apply(histo)
        
        if d.getName() == refDataset:
            #histo.SetFillStyle(3001)
            refHisto = histograms.Histo(histo, legName, legStyle, drawStyle)
        else:
            #otherHisto = histograms.Histo(histo, legName, legStyle, drawStyle)
            #otherHisto = histograms.Histo(histo, legName, "F", "HIST9")
            otherHisto = histograms.Histo(histo, legName, "LP", "P") # fixme alex
            otherHistos.append(otherHisto)

    if refHisto == None:
        raise Exception("The \"reference\" histogram is None!")
    if len(otherHistos) < 1:
        if( "TH2" in str(histoType) ):
            otherHistos.append("EMPTY") # fixme: temporary fix, otherwise crash for TH2
        else:
            raise Exception("The \"other\" histogram list empty!")
    return refHisto, otherHistos



def ApplyHistoStyles(datasetsMgr, histoName, **kwargs):
    '''
    FIXME: Does not seem to apply the styles.
    '''
    Print("Applying style to histograms for all datasets:")

    # For-loop: All-Datasets
    datasets    = datasetsMgr.getAllDatasets()
    for d in datasets:
        Print("\t" + d.getName(), False)
        rootHisto = datasetsMgr.getDataset(d.getName()).getDatasetRootHisto(histoName)
        histo     = rootHisto.getHistogram()
        styleDict[d.getName()].apply(histo)
    return



def GetCustomisedHistos(datasetsMgr, histoName, **kwargs):
    '''
    '''
    rootHistos = []
    histos     = []
    # For-loop: All-Datasets
    datasets    = datasetsMgr.getAllDatasets()
    for d in datasets:
        Print("\t" + d.getName(), False)
        rootHisto = datasetsMgr.getDataset(d.getName()).getDatasetRootHisto(histoName)
        histo     = rootHisto.getHistogram()
        styleDict[d.getName()].apply(histo)
        rootHistos.append(rootHisto)
        histos.append(histo)
    return rootHistos, histos
        

def GetSelfName():
    return __file__.split("/")[-1]


def Print(msg, printHeader=True):
    if printHeader:
        print "=== %s: %s" % (GetSelfName(), msg)
    else:
        print msg 
    return


def Verbose(msg, printHeader=True, verbose=False):
    if not verbose:
        return
    Print (msg, printHeader)
    return


def SaveAs(p, savePath, saveName, saveFormats):
    '''
    '''
    Verbose("Saving plots in %s format(s)" % (len(saveFormats)))

    # For-loop: All formats to save file
    for ext in saveFormats:        
        sName = saveName + ext

        # Change print name if saved under html
        if "html" in sName:
            user    = getpass.getuser()
            initial = getpass.getuser()[0]
            sName   = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
            sName   = sName.replace("%s/public/html/" % (user), "%s/" % (user))
            
        # Print save name
        print "\t", sName

        # Check if dir exists
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        # Save the plots
        p.saveAs(saveName, saveFormats)
    return

        
def GetLumi(datasetsMgr):
    Print("Determining integrated luminosity from data-datasets")

    intLumi = -1
    if len(datasetsMgr.getDataDatasets()) == 0:
        intLumi = None

    datasets = datasetsMgr.getAllDatasetNames()

    # Either get luminosity from merged data, or load luminosity from JSON file (before merging datasets)
    if "Data" in datasets:
        intLumi = datasetsMgr.getDataset("Data").getLuminosity()
    else:
        if "DatasetManager" not in str(datasetsMgr.__class__):
            datasetsMgr.loadLuminosities(fname="lumi.json")

    # Load RUN range
    # runRange = datasets.loadRunRange(fname="runrange.json")

    # For-loop: All Data datasets
    if intLumi == None:
        for d in datasetsMgr.getDataDatasets():
            print "\tluminosity", d.getName(), d.getLuminosity()
            intLumi += d.getLuminosity()
    print "\tIntegrated Luminosity is %s (pb)" % (intLumi)
    return intLumi


def RemoveNegativeBins(hList, p):
    for h in hList:        
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                if h.GetBinContent(i, j) < 0:
                    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetBinContent(i, j, 0))
    return


def RemoveNegativeBins(datasetsMgr, histoName, p):
    Print("Removing negative bins in histograms for all datasets:")

    # For-loop: All-Datasets
    datasets = datasetsMgr.getAllDatasets()
    for d in datasets:
        Print("\t" + d.getName(), False)
        rootHisto = datasetsMgr.getDataset(d.getName()).getDatasetRootHisto(histoName)
        histo     = rootHisto.getHistogram()
        for i in range(histo.GetNbinsX()):
            for j in range(histo.GetNbinsY()):
                if histo.GetBinContent(i, j) < 0:
                    p.histoMgr.forEachHisto(lambda histo: histo.getRootHisto().SetBinContent(i, j, 0))
    return



def NormalizeRootHistos(datasetsMgr, histoName, **kwargs):
    '''
    FIXME: Does not seem to apply the styles.
    # \li \a normalizeToOne           Normalize the histograms to one (True/False)
    # \li \a normalizeByCrossSection  Normalize the histograms by the dataset cross sections (True/False)
    # \li \a normalizeToLumi          Normalize the histograms to a given luminosity (number)
    '''
    HasKeys(["normalizeTo"], **kwargs)
    normalizeTo = kwargs.get("normalizeTo")
    datasets    = datasetsMgr.getAllDatasets()
    
    Print("Normalising all datasets to \"%s\":" % (normalizeTo))
    for d in datasets:
        Print("\t" + d.getName(), False)
        rootHisto = datasetsMgr.getDataset(d.getName()).getDatasetRootHisto(histoName)
        NormalizeRootHisto(rootHisto, d.isMC(), normalizeTo) #alex
        
    return


def NormalizeRootHisto(rootHisto, isMC, normalizeTo):
    '''
    # \li \a normalizeToOne           Normalize the histograms to one (True/False)
    # \li \a normalizeByCrossSection  Normalize the histograms by the dataset cross sections (True/False)
    # \li \a normalizeToLumi          Normalize the histograms to a given luminosity (number)
    '''    
    if normalizeTo == "One":
        rootHisto.normalizeToOne()
    elif normalizeTo == "XSection":
        if isMC:
            rootHisto.normalizeByCrossSection()
    elif normalizeTo == "Luminosity":
        rootHisto.normalizeToLumi(intLumi)
    else:
        IsValidNorm(normalizeTo)
    return


def GetBinwidthDecimals(binWidth):
    if binWidth < 1:
        return " %0.1f"
    elif binWidth < 0.1:
        return " %0.2f"
    elif binWidth < 0.01:
        return " %0.3f"
    elif binWidth < 0.001:
        return " %0.4f"
    elif binWidth < 0.0001:
        return " %0.5f"
    else:
        return " %0.0f"


def getTitleX(histo, title=None, **kwargs):
    HasKeys(["normalizeTo"], **kwargs)

    if title == None:
        title = histo.getRootHisto().GetXaxis().GetTitle()
        
    if isinstance(histo, (ROOT.TGraphAsymmErrors, ROOT.TGraph)):
        return title
    
    # Include the binwidth in the y-title
    binWidth = histo.getRootHisto().GetYaxis().GetBinWidth(1)
    title    = title + " / %s" % (GetBinwidthDecimals(binWidth) % (binWidth) )
    return title


def getTitleY(histo, title=None, **kwargs):
    HasKeys(["normalizeTo"], **kwargs)

    if title == None:
        if isinstance(histo, (ROOT.TH1)):
            title = getSymbolY(kwargs.get("normalizeTo"))
            if title == None:
                title = "Events"
        else:
            title = histo.getRootHisto().GetYaxis().GetTitle()            
        
    if isinstance(histo, (ROOT.TGraphAsymmErrors, ROOT.TGraph)):
        return title
    
    # Include the binwidth in the title
    binWidth = histo.getRootHisto().GetXaxis().GetBinWidth(1)
    title    = title + " / %s" % (GetBinwidthDecimals(binWidth) % (binWidth) )
    return title


def getTitleZ(histo, title=None, **kwargs):
    '''
    '''
    HasKeys(["normalizeTo"], **kwargs)
    
    if title == None:
        title = getSymbolY(kwargs.get("normalizeTo"))
    return title
        
    if isinstance(histo, (ROOT.TGraphAsymmErrors, ROOT.TGraph)):
        return title

    
def getSymbolY(normalizeTo):
    IsValidNorm(normalizeTo)
    NormToSymbols = {"One": "Arbitrary Units", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]"}
    
    return NormToSymbols[normalizeTo]
    

def IsValidNorm(normalizeTo):
    validNorms = ["One", "XSection", "Luminosity", ""]

    if normalizeTo not in validNorms:
        raise Exception("Invalid normalization option \"%s\". Please choose one of the following: %s" % (normalizeTo, "\"" + "\", \"".join(validNorms) ) + "\"")
    return
        
