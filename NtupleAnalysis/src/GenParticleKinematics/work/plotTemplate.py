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
plotDir     = "Plots"
formats     = [".png"] #,".pdf",".C"]
analysis    = "GenParticleKinematics"
kinVar      = "Pt"  # "Pt", "Eta", "Phi"
normalizeTo = "One" # "", "One", "XSection", "Luminosity"
rebinFactor = 2     # 5
ratio       = False


#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()
    hNames   = getHistoNames(kinVar)
    # hName    = hNames[0]

    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)

    # Get all datasets from the mcrab dir
    datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis)
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTauB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTauB_M_")
    # datasets  = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=analysis, excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")

    
    # Inform user of datasets retrieved
    Print("Got following datasets from multicrab dir \"%s\"" % parseOpts.mcrab)
    for d in datasets.getAllDatasets():
        print "\t", d.getName()


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
    for hName in hNames:
        plotName = hName #analysis + "_" + hName
        saveName = os.path.join(plotDir, plotName)
        
        # Get Data or MC datasets
        # dataDatasets = datasets.getDataDatasets()
        # mcDatasets   = datasets.getMCDatasets()

        # Build ROOT histos from individual datasets
        dataset1 = datasets.getDataset("ChargedHiggs_HplusTB_HplusToTauB_M_400").getDatasetRootHisto(hName)
        dataset2 = datasets.getDataset("TT_ext3").getDatasetRootHisto(hName)
        # datasets.getDataset("TT_ext3").setCrossSection(831.76)
        
        
        # Normalise datasets
        if normalizeTo == "One":
            dataset1.normalizeToOne()
            dataset2.normalizeToOne()
        elif normalizeTo == "XSection":
            dataset1.normalizeByCrossSection()
            dataset2.normalizeByCrossSection()
        elif normalizeTo == "Luminosity":
            dataset1.normalizeToLumi(intLumi)
            dataset2.normalizeToLumi(intLumi)
        else:
            isValidNorm(normalizeTo)
        
    
        # Customise histos
        histo1 = dataset1.getHistogram()
        styles.signal200Style.apply(histo1)
        # histo1.SetMarkerStyle(ROOT.kFullCircle)
        # histo1.SetFillStyle(3001)
        # histo1.SetFillColor(histo2.GetMarkerColor())
        removeNegatives(histo1)
        # removeErrorBars(histo1)
        histo1.Rebin(rebinFactor)
        
        # Customise histos
        histo2 = dataset2.getHistogram()
        styles.ttStyle.apply(histo2)
        # histo2.SetMarkerStyle(ROOT.kFullCross)
        histo2.SetFillStyle(3001)
        histo2.SetFillColor(styles.ttStyle.color)
        removeNegatives(histo2)
        # removeErrorBars(histo2)
        histo2.Rebin(rebinFactor)


        # Create a comparison plot
        p = plots.ComparisonPlot(histograms.Histo(histo1, "m_{H^{#pm}} = 400 GeV/c^{2}", "p", "P"),
                                 #histograms.Histo(histo2, "t#bar{t}", "p", "P"))
                                 histograms.Histo(histo2, "t#bar{t}", "F", "HIST,E,9"))
        
        # Create a comparison plot (One histogram is treated as a reference histogram, and all other histograms are compared with respect to that)
        # p = plots.ComparisonManyPlot(histograms.Histo(histo1, "m_{H^{#pm}} = 200 GeV/c^{2}", "p", "P"),
        #                             [histograms.Histo(histo2, "m_{H^{#pm}} = 300 GeV/c^{2}", "F", "HIST9"),
        #                              histograms.Histo(histo3, "t#bar{t}", "F", "HIST9")])

    
        # Customise plots
        opts      = {"ymin": 0.0, "binWidthX": histo1.GetXaxis().GetBinWidth(0), "xUnits": getUnitsX(kinVar)}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0 , "binWidthX": histo1.GetXaxis().GetBinWidth(0), "xUnits": getUnitsX(kinVar)}
        p.createFrame(os.path.join(plotDir, plotName), createRatio=ratio, opts=opts, opts2=ratioOpts)
        

        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.2}
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
        p.getFrame().GetYaxis().SetTitle( getTitleY(normalizeTo, kinVar, opts) )
        p.getFrame().GetXaxis().SetTitle( getTitleX(kinVar, opts) )
        if ratio:
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)


        #  Draw plots
        p.draw()

    
        # Save canvas under custom dir
        SavePlotterCanvas(p, plotDir, saveName, formats)

    return

#================================================================================================
# Auxiliary Function Definition
#================================================================================================
def Print(msg, printHeader=True):
    if printHeader:
        print "=== plotTemplate.py:", msg
    else:
        print msg 
    return


def SavePlotterCanvas(p, plotDir, saveName, formats):
    '''
    '''
    Print("Saving plots in %s format(s)" % (len(formats)) )
    for ext in formats:
        print "\t", saveName + ext

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)
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

def getHistoNames(kinVar):

    isValidVar(kinVar)

    hNames = []
    hNames.append("gtt_TQuark_" + kinVar)
    hNames.append("gtt_tbW_WBoson_" + kinVar)
    hNames.append("gtt_tbW_BQuark_" + kinVar)
    hNames.append("tbH_HPlus_" + kinVar)
    hNames.append("tbH_TQuark_" + kinVar)
    hNames.append("tbH_BQuark_" + kinVar)
    hNames.append("tbH_tbW_WBoson_" + kinVar)
    hNames.append("tbH_tbW_BQuark_" + kinVar)
    hNames.append("gtt_BQuark_" + kinVar)
    return hNames


def getUnitsX(kinVar):

    isValidVar(kinVar)    
    VarsToUnits = {"Pt": "GeV/c", "Eta": "", "Phi": "rads"}

    return VarsToUnits[kinVar]


def getSymbolX(kinVar):

    isValidVar(kinVar)
    VarsToSymbols = {"Pt": "p_{T}", "Eta": "#eta", "Phi": "#phi"}

    return VarsToSymbols[kinVar]


def getUnitsFormatX(kinVar):

    isValidVar(kinVar)
    VarsToNDecimals = {"Pt": "%0.0f", "Eta": "%0.2f", "Phi": "%0.03f"}

    return VarsToNDecimals[kinVar]


def getTitleX(kinVar, opts):
    unitsX = opts.get("xUnits")
    if unitsX != "":
        titleX = getSymbolX(kinVar) + " (%s)" % unitsX
    else:
        titleX = getSymbolX(kinVar)
    return titleX


def getSymbolY(normalizeTo):
    isValidNorm(normalizeTo)
    NormToSymbols = {"One": "Probability", "Luminosity": "Events", "": "Arbitrary Units", "XSection": "#sigma [pb]"}
    
    return NormToSymbols[normalizeTo]
    

def getTitleY(normalizeTo, kinVar, opts):

    titleY = getSymbolY(normalizeTo) + " / %s %s" % ( getUnitsFormatX(kinVar) % opts.get("binWidthX"), opts.get("xUnits") )
    return titleY

    
def isValidVar(kinVar):
    validVars = ["Pt", "Eta", "Phi"]
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

