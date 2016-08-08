#!/usr/bin/env python
'''

Usage:
./plotTemplate.py -m <pseudo_mcrab_directory>

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

#================================================================================================
# Variable Definition
#================================================================================================
analysis    = "Kinematics"
#myPath      = "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_xAugust2016/figures/signal/"
myPath      = None
kwargs      = {
    "referenceHisto" : "M_200",
    "ignoreHistos"   : ["M_300", "M_400"],
    "saveFormats"    : [".png"],
    "normalizeTo"    : "One",
    "rebin"          : 1,
    "createRatio"    : False,
    "removeNegatives": False,
    "removeErrorBars": False
}

hNames = [
    "genMET_Et",
    "genMET_Phi",
    "genHT_GenJets",
    "genHT_GenParticles",
    "SelGenJet_Multiplicity",
    "MaxDiJetMass_Pt",
    "MaxDiJetMass_Eta",
    "MaxDiJetMass_Mass",
    "MaxDiJetMass_Rap",
    "MaxDiJetMass_dR",
    "MaxDiJetMass_dRrap",
    "MaxDiJetMass_dEta",
    "MaxDiJetMass_dPhi",
    "BQuarkPair_dRMin_pT",
    "BQuarkPair_dRMin_dEta",
    "BQuarkPair_dRMin_dPhi",
    "BQuarkPair_dRMin_dR",
    "BQuarkPair_dRMin_Mass",
    "Htb_tbW_bqq_Pt",
    "Htb_tbW_bqq_Rap",
    "Htb_tbW_bqq_Mass",
    "gtt_tbW_bqq_Pt",
    "gtt_tbW_bqq_Rap",
    "gtt_tbW_bqq_Mass",
]

#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()
    savePath = myPath
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)
    
    # Get all datasets from the mcrab dir
    datasets  = GetDatasetsFromDir(parseOpts.mcrab, analysis)
    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = 0.0
    if len(datasets.getDataDatasets()) != 0:
        # Load Luminosity JSON file
        datasets.loadLuminosities(fname="lumi.json")

        # Load RUN range
        # runRange = datasets.loadRunRange(fname="runrange.json")

        # Calculate Integrated Luminosity
        intLumi = GetLumi(datasets)
    
                  
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        plotName = hName
        if savePath == None:
            savePath = GetSavePath(analysis)
        else:
            pass
        saveName = os.path.join(savePath, plotName)
                
        # Get customised histos
        rootHistos, histos    = GetCustomisedHistos(datasets, hName, **kwargs)
        refHisto, otherHistos = GetHistosForPlot(histos, rootHistos, **kwargs)            

        # Create a comparison plot
        p = plots.ComparisonManyPlot(refHisto, otherHistos)
        
        # Create a frame
        opts      = {"ymin": 0.0, "binWidthX": histos[0].GetXaxis().GetBinWidth(0)}#, "xUnits": getUnitsX(hName)}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0 , "binWidthX": histos[0].GetXaxis().GetBinWidth(0)}
        fileName = os.path.join(savePath, plotName)
        p.createFrame(fileName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)

        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.1}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        # Customise text
        if intLumi > 0.0:
            histograms.addStandardTexts(lumi=intLumi)
        else:
            histograms.addStandardTexts()
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasets.loadRunRange(), 17)

        # Customise frame
        p.setEnergy("13")
        p.getFrame().GetYaxis().SetTitle( getTitleY(kwargs.get("normalizeTo"), hName, opts) )
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        #  Draw plots
        p.draw()
    
        # Save canvas under custom dir
        if counter == 0:
            Print("Saving plots in %s format(s)" % (len(kwargs.get("saveFormats"))) )
        SavePlotterCanvas(p, saveName, savePath, **kwargs)

    return

#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def GetDatasetsFromDir(mcrab, analysis):

    datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], analysisName=analysis)
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")

    # Inform user of datasets retrieved
    Print("Got following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        print "\t", d.getName()
    return datasets


def GetHistosForPlot(histos, rootHistos, **kwargs):
    refHisto     = None
    otherHistos  = []
    ignoreHistos = []

    # For-loop: histos
    for rh in rootHistos:
        hName = rh.getName()
        for iName in kwargs.get("ignoreHistos"):
            if iName in hName:
                ignoreHistos.append(hName)
                break

    # For-loop: histos
    for rh, h in zip(rootHistos, histos):
        legName = "m_{H^{#pm}} = %s GeV/c^{2}" % (rh.getName().split("_M_")[-1])
        
        if kwargs.get("referenceHisto") in rh.getName():
            refHisto = histograms.Histo(h, legName, "p", "P")
        elif rh.getName() in ignoreHistos:
            continue
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
    
    # Apply styles
    styleDict = {
        "ChargedHiggs_HplusTB_HplusToTB_M_500": styles.signal500Style, 
        "ChargedHiggs_HplusTB_HplusToTB_M_400": styles.signal400Style,
        "ChargedHiggs_HplusTB_HplusToTB_M_300": styles.signal300Style,
        "ChargedHiggs_HplusTB_HplusToTB_M_200": styles.signal200Style}

    # For-loop: All root histos
    for rh in rootHistos:
        h = rh.getHistogram()
        styleDict[rh.getName()].apply(h)

        # Rebinning
        if not isinstance(h, ROOT.TH2F):
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


def GetSavePath(analysis):
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath


def SavePlotterCanvas(p, saveName, savePath, **kwargs):
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
        p.save(formats)
    return

        
def GetLumi(datasets):
    '''
    '''
    Print("Determining integrated luminosity from data-datasets")

    # For-loop: All Data datasets
    for d in datasets.getDataDatasets():
        print "\tluminosity", d.getName(), d.getLuminosity()
        intLumi += d.getLuminosity()
    print "\tluminosity, sum", intLumi
    return intLumi


def removeNegatives(histo):
    for bin in range(histo.GetNbinsX()):
        if histo.GetBinContent(bin) < 0:
            histo.SetBinContent(bin, 0.0)
    return


def removeErrorBars(histo):
    for bin in range(histo.GetNbinsX()):
        histo.SetBinError(bin, 0.0)
    return


def getUnitsFormatX(hName):

    VarsToNDecimals = {
        "genMET_Et"                      : "%0.0f",
        "genMET_Phi"                     : "%0.3f",
        "genHT_GenJets"                  : "%0.0f",
        "genHT_GenParticles"             : "%0.0f",
        "SelGenJet_Multiplicity"         : "%0.0f",
        "MaxDiJetMass_Mass"              : "%0.0f",
        "MaxDiJetMass_Pt"                : "%0.0f",
        "MaxDiJetMass_Eta"               : "%0.2f",
        "MaxDiJetMass_dR"                : "%0.2f",
        "MaxDiJetMass_Rap"               : "%0.2f",
        "MaxDiJetMass_dRrap"             : "%0.2f",
        "MaxDiJetMass_dEta"              : "%0.2f",
        "MaxDiJetMass_dPhi"              : "%0.2f",
        "MaxDiJetMass_dEta_Vs_dPhi"      : "%0.2f",
        "MaxDiJetMass_dRrap"             : "%0.2f",
        "BQuarkPair_dRMin_pT"            : "%0.0f",
        "BQuarkPair_dRMin_dEta"          : "%0.2f",
        "BQuarkPair_dRMin_dPhi"          : "%0.2f",
        "BQuarkPair_dRMin_dR"            : "%0.2f",
        "BQuarkPair_dRMin_Mass"          : "%0.0f",
        "Htb_tbW_bqq_Pt"                 : "%0.0f",
        "Htb_tbW_bqq_Rap"                : "%0.2f",
        "Htb_tbW_bqq_Mass"               : "%0.0f",
        "gtt_tbW_bqq_Pt"                 : "%0.0f",
        "gtt_tbW_bqq_Rap"                : "%0.2f",
        "gtt_tbW_bqq_Mass"               : "%0.0f",
    }
    return VarsToNDecimals[hName]


def getSymbolY(normalizeTo):
    isValidNorm(normalizeTo)
    NormToSymbols = {"One": "Arbitrary Units", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]"}
    
    return NormToSymbols[normalizeTo]
    

def getTitleY(normalizeTo, kinVar, opts):    
    if opts.get("xUnits")!=None:
        titleY = getSymbolY(normalizeTo) + " / %s %s" % ( getUnitsFormatX(kinVar) % opts.get("binWidthX"), opts.get("xUnits") )
    else:
        titleY = getSymbolY(normalizeTo) + " / %s" % ( getUnitsFormatX(kinVar) % opts.get("binWidthX") )
    return titleY

    
def isValidVar(kinVar):
    validVars = ["Pt", "Eta", "Phi", "dR"]
    if kinVar not in validVars:
        raise Exception("Invalid kinematics variable \"%s\". Please choose one of the following: %s" % (kinVar, "\"" + "\", \"".join(validVars) ) + "\"")
    return


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


#"MaxDiJetMass_dEta_Vs_dPhi",
#"MaxDiJetMass_dRap_Vs_dPhi",
#"BQuark1_BQuark2_dEta_Vs_dPhi",
#"BQuark1_BQuark3_dEta_Vs_dPhi",
#"BQuark1_BQuark4_dEta_Vs_dPhi",
#"BQuark2_BQuark3_dEta_Vs_dPhi",
#"BQuark2_BQuark4_dEta_Vs_dPhi",
#"BQuark3_BQuark4_dEta_Vs_dPhi",
#"Jet1Jet2_dEta_Vs_Jet3Jet4_dEta",
#"Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi",
#"Jet1Jet2_dEta_Vs_Jet1Jet2_Mass",
#"Jet3Jet4_dEta_Vs_Jet3Jet4_Mass",
