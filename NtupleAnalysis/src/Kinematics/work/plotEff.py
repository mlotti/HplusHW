#!/usr/bin/env python
'''

Usage:
./plotTemplate.py -m <pseudo_mcrab_directory>

ROOT:
The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000
'''

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
# User Options
#================================================================================================
analysis    = "Kinematics"
cutDirection= ">"
#myPath      = "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_16August2016/figures/signal/"
myPath      = None
verbose     = False
kwargs      = {
    "referenceDataset": "ChargedHiggs_HplusTB_HplusToTB_M_500",
    "saveFormats"     : [".png"], #, ".pdf"],
    "normalizeTo"     : "One",
    "rebin"           : 1,
    "createRatio"     : True,
}


#================================================================================================
# Variable Definition
#================================================================================================
styleDict = {
    "ChargedHiggs_HplusTB_HplusToTB_M_500": styles.signal500Style, 
    "ChargedHiggs_HplusTB_HplusToTB_M_400": styles.signal400Style,
    "ChargedHiggs_HplusTB_HplusToTB_M_300": styles.signal300Style,
    "ChargedHiggs_HplusTB_HplusToTB_M_200": styles.signal200Style
}

hNames  = [
#    "genMET_Et",
#    #"genMET_Phi",
#    "genHT_GenJets",
#    "genHT_GenParticles",
    "SelGenJet_Multiplicity",
#    "MaxDiJetMass_Pt",
#    "MaxDiJetMass_Eta",
#    "MaxDiJetMass_Mass",
#    "MaxDiJetMass_Rap",
#    "MaxDiJetMass_dR",
#    "MaxDiJetMass_dRrap",
#    "MaxDiJetMass_dEta",
#    "MaxDiJetMass_dRap",
#    "MaxDiJetMass_dPhi",
#    "BQuarkPair_dRMin_pT",
#    "BQuarkPair_dRMin_dEta",
#    "BQuarkPair_dRMin_dPhi",
#    "BQuarkPair_dRMin_dR",
#    "BQuarkPair_dRMin_Mass",
#    "BQuarkPair_dRMin_jet1_dR",
#    "BQuarkPair_dRMin_jet1_dEta",
#    "BQuarkPair_dRMin_jet1_dPhi",
#    "BQuarkPair_dRMin_jet2_dR",
#    "BQuarkPair_dRMin_jet2_dEta",
#    "BQuarkPair_dRMin_jet2_dPhi",
#    "Htb_tbW_bqq_Pt",
#    "Htb_tbW_bqq_Rap",
#    "Htb_tbW_bqq_Mass",
#    "Htb_tbW_bqq_dRMax_dR",
#    "Htb_tbW_bqq_dRMax_dRap",
#    "Htb_tbW_bqq_dRMax_dPhi",
#    "gtt_tbW_bqq_Pt",
#    "gtt_tbW_bqq_Rap",
#    "gtt_tbW_bqq_Mass",
#    "gtt_tbW_bqq_dRMax_dR",
#    "gtt_tbW_bqq_dRMax_dRap",
#    "gtt_tbW_bqq_dRMax_dPhi",
]

kinVar  = ["Pt"] #, "Eta", "Rap"]
distVar = ["dR", "dEta", "dRap", "dPhi"]
#for var in kinVar:
#    hNames.append("gtt_TQuark_"            + var)
#    hNames.append("gbb_BQuark_"            + var)
#    hNames.append("gtt_tbW_WBoson_"        + var)
#    hNames.append("gtt_tbW_BQuark_"        + var)
#    hNames.append("gtt_tbW_Wqq_Quark_"     + var)
#    hNames.append("gtt_tbW_Wqq_AntiQuark_" + var)
#    hNames.append("tbH_HPlus_"             + var)
#    hNames.append("tbH_TQuark_"            + var)
#    hNames.append("tbH_BQuark_"            + var)
#    hNames.append("tbH_tbW_WBoson_"        + var)
#    hNames.append("tbH_tbW_BQuark_"        + var)
#    hNames.append("Htb_tbW_Wqq_Quark_"     + var)
#    hNames.append("Htb_tbW_Wqq_AntiQuark_" + var)
#    if var not in ["Rap"]:
#        hNames.append("BQuark1_" + var)
#        hNames.append("BQuark2_" + var)
#        hNames.append("BQuark3_" + var)
#        hNames.append("BQuark4_" + var)
#        hNames.append("GenJet1_" + var)
#        hNames.append("GenJet2_" + var)
#        hNames.append("GenJet3_" + var)
#        hNames.append("GenJet4_" + var)
#        hNames.append("GenJet5_" + var)
#        hNames.append("GenJet6_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet1_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet2_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet3_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet4_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet5_" + var)
#        hNames.append("AL3CJetsFromHPlus_GenJet6_" + var)
#for var in distVar:
#    hNames.append("Htb_TQuark_Htb_BQuark_"                + var)
#    hNames.append("Htb_TQuark_gtt_TQuark_"                + var)
#    hNames.append("Htb_TQuark_gbb_BQuark_"                + var)
#    hNames.append("Htb_BQuark_Htb_tbW_BQuark_"            + var)
#    hNames.append("Htb_BQuark_Htb_tbW_Wqq_Quark_"         + var)
#    hNames.append("Htb_BQuark_Htb_tbW_Wqq_AntiQuark_"     + var)
#    hNames.append("Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_"     + var)
#    hNames.append("Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_" + var)
#    hNames.append("gtt_TQuark_gbb_BQuark_"                + var)
#    hNames.append("gtt_TQuark_gtt_tbW_BQuark_"            + var)
#    hNames.append("gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_"     + var)
#    hNames.append("gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_" + var)


#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()
    savePath = myPath

    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)
    ROOT.gErrorIgnoreLevel = 3000
    

    # Get all datasets from the mcrab dir
    datasets  = GetDatasetsFromDir(parseOpts.mcrab, analysis)
    # datasets      = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_200")
    # otherDatasets = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="M_200")

    
    # Determine Integrated Luminosity
    intLumi = GetLumi(datasets)
    
                  
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
    
        # Get the save path
        savePath = GetSavePath(analysis, savePath)
        
        # Get the save name (according to cut direction)
        saveName = GetSaveName(savePath, hName, cutDirection)
        
        # Get customised histos
        rootHistos, histos    = GetCustomisedHistos(datasets, hName, **kwargs)
        refHisto, otherHistos = GetHistosForPlot(histos, rootHistos, **kwargs)            
        
        # ERROR BARS?
        
        # Get the referece TGraph
        #refEfftmp = getCutEfficiency(datasets.getDataset("ChargedHiggs_HplusTB_HplusToTB_%s" % kwargs.get("referenceDataset")), hName, cutDirection)
        #refEff    = histograms.HistoGraph(refEfftmp, plots._legendLabels["ChargedHiggs_HplusTB_HplusToTB_%s" % kwargs.get("referenceDataset")], "p", "P")
        refEff = getCutEfficiencyTGraph(datasets.getDataset(kwargs.get("referenceDataset")), hName, cutDirection)


        # Get the referece TGraph
        otherEff  = []
        for d in datasets.getMCDatasets():
            if d.getName() == kwargs.get("referenceDataset"):
                continue
            else:
                #h = getCutEfficiencyHisto(d, hName, cutDirection)
                t = getCutEfficiencyTGraph(d, hName, cutDirection)
                otherEff.append(t) #histograms.HistoGraph(h, plots._legendLabels[d.getName()], "p", "P"))
                
        # Plot the efficiencies
        p = plots.ComparisonManyPlot(refEff, otherEff)        
        

        # Create a frame
        opts      = {"ymin": 0.0, "ymaxfactor": 1.2} #"ymax": 5e-1}
        ratioOpts = {"ymin": 0.0, "ymaxfactor": 1.2} #"ymax": 2.0}
        fileName = os.path.join(savePath, hName)
        p.createFrame(fileName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)

        
        # Customise Legend
        moveLegend = {"dx": -0.1 , "dy": +0.0, "dh": -0.2}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        #p.removeLegend()

        
        # Customise frame
        p.getFrame().GetYaxis().SetTitle( getTitleY(rootHistos[0], **kwargs).replace("Arbitrary Units", "efficiency (%s)" % (cutDirection)))
        #p.setEnergy("13")
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        # SetLog
        p.getPad().SetLogy(False)
        p.getPad().SetLogx(False)
        p.getPad().SetLogz(False)
        
        # Add cut line/box
        _kwargs = { "lessThan": False}
        p.addCutBoxAndLine(cutValue=6, fillColor=ROOT.kAzure-4, box=False, line=True, **_kwargs)

        
        #  Draw plots
        p.draw()

        # Customise text
        histograms.addStandardTexts(lumi=intLumi)
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasets.loadRunRange(), 17)

        
        # Save canvas under custom dir
        if counter == 0:
            Print("Saving plots in %s format(s)" % (len(kwargs.get("saveFormats"))) )
        SaveAs(p, savePath, saveName, **kwargs)

    return

#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def getCutEfficiencyTGraph(dataset, histoName, cutDirection):
    effHisto = getCutEfficiencyHisto(dataset, histoName, cutDirection)
    effGraph = histograms.HistoGraph(effHisto, plots._legendLabels[dataset.getName()], "p", "P")
    return effGraph


def getCutEfficiencyHisto(dataset, histoName, cutDirection):

    # Choose statistics options
    #statOption = ROOT.TEfficiency.kFNormal
    statOption = ROOT.TEfficiency.kFCP # Clopper-Pearson
    # statOption = ROOT.TEfficiency.kFFC # Feldman-Cousins

    # Declare variables & options
    first  = True
    isData = False
    teff   = ROOT.TEfficiency()

    h = dataset.getDatasetRootHisto(histoName).getHistogram()
    if h.GetEntries() == 0:
        return
    removeNegatives(h)
        
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
    checkNegatives(n, d)
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
    return convert2TGraph(teff, dataset, style, titleX)


def getEfficiency(datasets, numerator="Numerator", denominator="Denominator"):
    
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

        checkNegatives(n, d)
        removeNegatives(n)
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
    return convert2TGraph(teff)


def checkNegatives(n,d):
    for i in range(1,n.GetNbinsX()+1):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)
        if 0:
            print "Bin",i,"Numerator=",nbin,", denominator=",dbin
        if nbin > dbin:
            n.SetBinContent(i,dbin)
        if nbin < 0:
            n.SetBinContent(i,0)
        if dbin < 0:
            n.SetBinContent(i,0)
            d.SetBinContent(i,0)
    return


def removeNegatives(histo):
    for bin in range(histo.GetNbinsX()):
        if histo.GetBinContent(bin) < 0:
            histo.SetBinContent(bin,0.)
    return


def convert2TGraph(tefficiency, dataset, style, titleX):
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
            removeNegatives(h)

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


def Verbose(msg, printHeader=True):
    if not parseOpts.verbose:
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
        
