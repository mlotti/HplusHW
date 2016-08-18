#!/usr/bin/env python

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket

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
    "QCD"              : styles.qcdStyle,
    "QCD_Pt_15to30"    : styles.qcdStyle, 
    "QCD_Pt_30to50"    : styles.qcdStyle, 
    "QCD_Pt_50to80"    : styles.qcdStyle,
    "QCD_Pt_80to120"   : styles.qcdStyle, 
    "QCD_Pt_120to170"  : styles.qcdStyle, 
    "QCD_Pt_170to300"  : styles.qcdStyle, 
    "QCD_Pt_300to470"  : styles.qcdStyle, 
    "QCD_Pt_470to600"  : styles.qcdStyle,         
    "QCD_Pt_600to800"  : styles.qcdStyle, 
    "QCD_Pt_800to1000" : styles.qcdStyle, 
    "QCD_Pt_1000to1400": styles.qcdStyle, 
    "QCD_Pt_1400to1800": styles.qcdStyle, 
    "QCD_Pt_1800to2400": styles.qcdStyle, 
    "QCD_Pt_2400to3200": styles.qcdStyle, 
    "QCD_Pt_3200toInf" : styles.qcdStyle,
}


#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def GetSavePath(analysis, savePath):
    '''
    '''
    if savePath != None:
        return savePath
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def GetSaveName(savePath, hName, cutDirection=None):
    '''
    '''
    if cutDirection == None:
        saveName = os.path.join(savePath, hName)
    elif cutDirection == ">":
        saveName = os.path.join(savePath, hName + "_GreaterThan")
    else:
        saveName = os.path.join(savePath, hName + "_LessThan")
    return saveName


def GetCutEfficiencyTGraph(dataset, histoName, cutDirection, statOpt="C-P", verbose=False):
    '''
    '''
    effHisto = GetCutEfficiencyHisto(dataset, histoName, cutDirection)
    effGraph = histograms.HistoGraph(effHisto, plots._legendLabels[dataset.getName()], "p", "P")
    return effGraph


def GetCutEfficiencyHisto(dataset, histoName, cutDirection, statOpt="C-P", verbose=False):
    '''
    '''

    # Choose statistics options
    if statOpt == "C-P":
        statOption = ROOT.TEfficiency.kFCP # Clopper-Pearson
    elif statOpt == "F-C":
        statOption = ROOT.TEfficiency.kFFC # Feldman-Cousins
    elif statOpt == "Normal":
        statOption = ROOT.TEfficiency.kFNormal
    else:
        raise Exception("Invalid statistics option \"%s\". Please choose from  \"C-P\", \"F-C\", and \"Normal\"" % (statOpt))

    # Declare variables & options
    first  = True
    isData = False
    teff   = ROOT.TEfficiency()

    h = dataset.getDatasetRootHisto(histoName).getHistogram()
    if h.GetEntries() == 0:
        return
    RemoveNegatives(h)
        
    numerator = h.Clone("Numerator")
    numerator.Reset()

    denominator = h.Clone("denominator")
    denominator.Reset()
        
    table    = []
    hLine    = "="*140
    msgAlign = '{:<5} {:<10} {:<10} {:<20} {:<20} {:<20} {:<20} {:<20}'
    title    = msgAlign.format("Bin", "LowEdge", "Center", "HighEdge", "BinContent", "Pass", "Total", "Efficiency")
    table.append(hLine)
    table.append(title)
    table.append(hLine)
    
    nBinsX = h.GetNbinsX()+1
    titleX =  h.GetXaxis().GetTitle()
    for iBin in range(1, nBinsX):

        binLowEdge = h.GetBinLowEdge(iBin)
        binCenter  = h.GetBinCenter(iBin)
        binWidth   = h.GetBinWidth(iBin)
        binHighEdge= binLowEdge + binWidth
        binContent = h.GetBinContent(iBin)
        nTotal     = h.Integral( 0, nBinsX )
        if cutDirection == ">":
            nPass  = h.Integral(iBin+1, nBinsX)
        elif cutDirection == "<":
            nPass  = nTotal - h.Integral(iBin+1, nBinsX)
        else:
            raise Exception("Invalid cut direction  \"%s\". Please choose either \">\" or \"<\"" % (cutDirection))
        numerator.SetBinContent(iBin, nPass)
        denominator.SetBinContent(iBin, nTotal)
        
        eff    = nPass/nTotal
        values = msgAlign.format(iBin, binLowEdge, binCenter, binHighEdge, binContent, nPass, nTotal, eff)
        table.append(values)
    table.append(hLine)
        
    if verbose:
        for l in table:
            print l

    n = numerator
    d = denominator
    CheckNegatives(n, d)
    eff = ROOT.TEfficiency(n, d)
    eff.SetStatisticOption(statOption)
    weight = 1
    if dataset.isMC():
        weight = dataset.getCrossSection()
    eff.SetWeight(weight)
        
    if first:
        teff = eff
        if dataset.isData():
            tn = n
            td = d
        first = False
    else:
        teff.Add(eff)
        if dataset.isData():
            tn.Add(n)
            td.Add(d)
    if isData:
        teff = ROOT.TEfficiency(tn, td)
        teff.SetStatisticOption(self.statOption)

    style = styleDict[dataset.getName()]
    return Convert2TGraph(teff, dataset, style, titleX)


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

        CheckNegatives(n, d)
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
    '''
    '''
    # For-loop: All bins in x-axis
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return


def Convert2TGraph(tefficiency, dataset, style, titleX):
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

    style.apply(tgraph)
    return tgraph


def GetDatasetsFromDir(mcrab, analysis):

    datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], analysisName=analysis)
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="M_180|M_220|M_250")

    # Inform user of datasets retrieved
    Print("Got following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        print "\t", d.getName()
    return datasets


def GetHistosForPlot(histos, rootHistos, **kwargs):
    refHisto     = None
    otherHistos  = []

    # For-loop: histos
    for rh in rootHistos:
        hName = rh.getName()

    # For-loop: histos
    for rh, h in zip(rootHistos, histos):
        legName = "m_{H^{#pm}} = %s GeV/c^{2}" % (rh.getName().split("_M_")[-1])

        if rh.getName() == kwargs.get("referenceDataset"):
            refHisto = histograms.Histo(h, legName, "p", "P")
        else:
            otherHistos.append( histograms.Histo(h, legName,  "F", "HIST,E,9") )
    return refHisto, otherHistos


def GetCustomisedHistos(datasets, hName, **kwargs):
    # Declarations
    rootHistos = []
    histos     = []

    # Get Data or MC datasets
    myDatasets = datasets.getAllDatasets()
    # myDatasets = datasets.getDataDatasets()
    # myDatasets   = datasets.getMCDatasets()

    
    # For-loop: All-Datasets
    for d in myDatasets:
        
        # Build ROOT histos from individual datasets
        h = datasets.getDataset(d.getName()).getDatasetRootHisto(hName)

        # Set the cross-section
        # d.getDataset("TT_ext3").setCrossSection(831.76)        

        # Append to ROOT histos list
        rootHistos.append(h)
        

    # Normalise ROOT histograms
    for h in rootHistos:
        if kwargs.get("normalizeTo") == "One":
            h.normalizeToOne()
        elif kwargs.get("normalizeTo") == "XSection":
            h.normalizeByCrossSection()
        elif kwargs.get("normalizeTo") == "Luminosity":
            h.normalizeToLumi(intLumi)
        else:
            isValidNorm(normalizeTo)
    

    # For-loop: All root histos
    for rh in rootHistos:
        h = rh.getHistogram()
        styleDict[rh.getName()].apply(h)

        # Rebinning
        h.Rebin(kwargs.get("rebin"))

        # Remove negative histo entries
        if kwargs.get("removeNegatives"):
            RemoveNegatives(h)

        # Remove error bars 
        if kwargs.get("removeErrorBars"):
            removeErrorBars(h)

        # Append the histogram
        histos.append(h)
        
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


def GetSavePath(analysis, savePath):
    if savePath != None:
        return savePath
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def GetSaveName(savePath, hName, cutDirection):
    if cutDirection == ">":
        saveName = os.path.join(savePath, hName + "_GreaterThan")
    else:
        saveName = os.path.join(savePath, hName + "_LessThan")
    return saveName


def SaveAs(p, savePath, saveName, **kwargs):
    formats  = kwargs.get("saveFormats")
    Verbose("Saving plots in %s format(s)" % (len(formats)) )

    # For-loop: All formats to save file
    for ext in formats:        
        sName = saveName + ext

        # Change print name if saved under html
        if "html" in sName:
            sName = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
            sName = sName.replace("%s/public/html/" % (user), "%s/" % (user))
            
        # Print save name
        print "\t", sName

        # Check if dir exists
        if not os.path.exists(savePath):
            os.mkdir(savePath)

        # Save the plots
        p.saveAs(saveName, formats)
    return

        
def GetLumi(datasets):
    Print("Determining integrated luminosity from data-datasets")

    intLumi = None
    if len(datasets.getDataDatasets()) == 0:
        return intLumi

    # Load Luminosity JSON file
    datasets.loadLuminosities(fname="lumi.json")

    # Load RUN range
    # runRange = datasets.loadRunRange(fname="runrange.json")

    # For-loop: All Data datasets
    for d in datasets.getDataDatasets():
        print "\tluminosity", d.getName(), d.getLuminosity()
        intLumi += d.getLuminosity()
    print "\tluminosity, sum", intLumi
    return intLumi


def RemoveNegativeBins(hList, p):
    for h in hList:        
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                if h.GetBinContent(i, j) < 0:
                    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetBinContent(i, j, 0))
    return


def getTitleY(histo, **kwargs):
    binWidthY = histo.getHistogram().GetXaxis().GetBinWidth(1)*kwargs.get("rebin")

    if binWidthY < 1:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.1f" %  float(binWidthY)
    elif binWidthY < 0.1:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.2f" %  float(binWidthY)
    elif binWidthY < 0.01:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.3f" %  float(binWidthY)
    else:
        titleY    = getSymbolY(kwargs.get("normalizeTo")) + " / %0.0f" %  float(binWidthY)
    return titleY


def getSymbolY(normalizeTo):
    isValidNorm(normalizeTo)
    NormToSymbols = {"One": "Arbitrary Units", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]"}
    
    return NormToSymbols[normalizeTo]
    

def isValidNorm(normalizeTo):
    validNorms = ["One", "XSection", "Luminosity", ""]

    if normalizeTo not in validNorms:
        raise Exception("Invalid normalization option \"%s\". Please choose one of the following: %s" % (normalizeTo, "\"" + "\", \"".join(validNorms) ) + "\"")
    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"    , dest="mcrab"    , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, help="Enables batch mode (canvas creation does NOT generates a window)")
    parser.add_option("-v", "--verbose"  , dest="verbose"  , action="store_true", default=False, help="Enables verbose mode (for debugging purposes)")
    (parseOpts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if parseOpts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main()

    if not parseOpts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")
        
