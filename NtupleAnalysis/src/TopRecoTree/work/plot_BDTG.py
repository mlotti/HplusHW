#!/usr/bin/env python
'''
DESCRIPTION:
Reproduces the TMVA BDTG classifier output and ROC curves in CMS style


USAGE:
./plot_BDTG.py -r <TMVAoutput_rootFile> --reff mvaeffs.root [opts]


EXAMPLES:
./plot_BDTG.py -r TopReco_DR0p3_DPtOverPt0p32.root --reff mvaeffs.root --url
./plot_BDTG.py -r /uscms_data/d3/skonstan/workspace/rootfiles/TopReco_DR0p3_DPtOverPt0p32.root --reff /uscms_data/d3/skonstan/workspace/rootfiles/mvaeffs.root --url
./plot_BDTG.py -r /uscms_data/d3/skonstan/workspace/rootfiles/TopRecoTree_180523_DeltaR0p3_DeltaPtOverPt0p32_TopPtRew13TeV.root --reff /uscms_data/d3/skonstan/workspace/rootfiles/mvaeffs_TopPtRew13TeV_DeltaPtOverPt0p32.root --url

LAST USED:
./plot_BDTG.py -r /uscms_data/d3/aattikis/workspace/rootfiles/TopReco_DR0p3_DPtOverPt0p32.root --reff /uscms_data/d3/aattikis/workspace/rootfiles/mvaeffs.root --url

'''


#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import getpass
from optparse import OptionParser

import ROOT
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

kwargs = {
    "verbose"          : False,
    "dataEra"          : None,
    "searchMode"       : None,
    "analysis"         : "MyHplus2tbKInematics",
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf"],
    "xlabel"           : None,
    "ylabel"           : "Probability",
    "rebinX"           : 2,
    "rebinY"           : 2,
    "xlabelsize"       : None,
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : False,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Simulation",
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": +0.0, "dh": +0.1},
    "cutValue"         : None,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
    }

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
    
def main(opts, signalMass):

        # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(False)
    style.setGridY(False)

    # Do the topSelection histos
    folder      = ""

    #=== Define styles: Fixme: Put in function

    #styles_S    = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=928, markerSizes=None, markerStyle=ROOT.kFullDiamond),
     #                                   styles.StyleLine(lineColor=928, lineStyle=ROOT.kSolid, lineWidth=3),
     #                                   styles.StyleFill(fillColor=38)])
    styles_S    = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=928, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                        styles.StyleLine(lineColor=928, lineStyle=ROOT.kSolid, lineWidth=3)])                                       


    styles_B    = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=2, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                        styles.StyleLine(lineColor=2, lineStyle=ROOT.kSolid, lineWidth=3),
                                        styles.StyleFill(fillColor=2, fillStyle=3005)])

    styles_SEff = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=ROOT.kBlue, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                        styles.StyleLine(lineColor=ROOT.kBlue, lineStyle=ROOT.kSolid, lineWidth=3),])

    styles_BEff = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=ROOT.kRed, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                        styles.StyleLine(lineColor=ROOT.kRed, lineStyle=ROOT.kSolid, lineWidth=3),])

    styles_Signif = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=ROOT.kGreen+2, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                          styles.StyleLine(lineColor=ROOT.kGreen+2, lineStyle=ROOT.kSolid, lineWidth=3),])

    styles_pur = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=ROOT.kOrange+7, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                       styles.StyleLine(lineColor=ROOT.kOrange+7, lineStyle=ROOT.kSolid, lineWidth=3),])

    styles_pureff = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=ROOT.kOrange, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                          styles.StyleLine(lineColor=ROOT.kOrange, lineStyle=ROOT.kSolid, lineWidth=3),])


    #=== Histo Names ============================================
    hN_SignalEff = "sigEffi"
    hN_BgdEff    = "bgdEffi"
    hN_signif    = "significance_BDTG"
    hN_purS      = "purS_BDTG"
    hN_effpurS   = "effpurS_BDTG"

    hN_BDTs      = "MVA_BDTG_S"
    hN_BDTb      = "MVA_BDTG_B"

    #=== Directories ============================================
    inpfile_eff = ROOT.TFile(opts.effFile, "R")
    inpfile     = ROOT.TFile(opts.rootfile, "R") #To be fixed!
    inpfile_dir = inpfile.Get("Method_BDT/BDTG")


    #=== Get histograms from directories=========================
    h_SignalEffi = inpfile_eff.Get(hN_SignalEff)
    h_BgdEffi    = inpfile_eff.Get(hN_BgdEff)
    h_signif     = inpfile_eff.Get(hN_signif)
    h_purS       = inpfile_eff.Get(hN_purS)
    h_effpurS    = inpfile_eff.Get(hN_effpurS)

    h_BDTs       = inpfile_dir.Get(hN_BDTs)
    h_BDTb       = inpfile_dir.Get(hN_BDTb)
    
    #=== Scale Significance
    h_signifScaled = h_signif.Clone("signif")
    maxSignif = h_signif.GetMaximum()
    h_signifScaled.Scale(1/maxSignif)

    histo_signalEff    = histograms.Histo(h_SignalEffi,   "sEff",     legendStyle = "LP", drawStyle="LP")
    histo_bgdEff       = histograms.Histo(h_BgdEffi,      "bEff",     legendStyle = "LP", drawStyle="LP")
    histo_signifScaled = histograms.Histo(h_signifScaled, "signif",   legendStyle = "LP", drawStyle="LP")
    histo_purS         = histograms.Histo(h_purS,         "purity",   legendStyle = "LP", drawStyle="LP")
    histo_effpurS      = histograms.Histo(h_effpurS,      "pureff",   legendStyle = "LP", drawStyle="LP")

    histo_BDTs         = histograms.Histo(h_BDTs,         "bdtS",     legendStyle = "LP", drawStyle="LP")
    histo_BDTb         = histograms.Histo(h_BDTb,         "bdtB",     legendStyle = "LP", drawStyle="LP")



    #=== Efficiency - Purity - Significance=================================
    histoList_Eff = [histo_bgdEff, histo_signifScaled, histo_purS, histo_effpurS]
    p_Eff = plots.ComparisonManyPlot(histo_signalEff, histoList_Eff,
                                     saveFormats=[])

    p_Eff.histoMgr.setHistoLegendLabelMany({"sEff": "Signal efficiency", 
                                        "bEff": "Bkg efficiency", 
                                        "signif": "S/#sqrt{S+B}", 
                                        #"signif": "#frac{S}{#sqrt{S+B}}", 
                                        "purity": "Signal purity", 
                                        "pureff": "Signal eff*purity",})



    # Define Right Axis (Significance)
    signifColor = ROOT.kGreen+2
    #rightAxis = ROOT.TGaxis(0.5, 0.17, 0.97, 0.34, 0, 1.1*maxSignif, 510, "+L")
    '''
    TGaxis::TGaxis(Double_t xmin, Double_t ymin, Double_t xmax, Double_t ymax,
                   Double_t wmin, Double_t wmax, Int_t ndiv, Option_t *chopt,
                   Double_t gridlength)
    '''
    rightAxis = ROOT.TGaxis(1, 0, 1, 1.1, 0, 1.1*maxSignif, 510, "+L")
    rightAxis.SetWmax(1.1*maxSignif)
    rightAxis.SetLineColor ( signifColor )
    rightAxis.SetLabelColor( signifColor )
    rightAxis.SetTitleColor( signifColor )

    # rightAxis.SetTitleSize( info->sSig->GetXaxis()->GetTitleSize() )
    # rightAxis.SetLabelOffset(0.9)
    # This will only be be visible if we use a wide canvas (but we don't want that)
    if 0:
        style.setWide(True, 0.15) #to make way for significane label
        rightAxis.SetTitle( "Significance" )
        # rightAxis.SetTitleOffset(1.1)

    #=== BDTG output ========================================================
    histo_BDTs         = histograms.Histo(h_BDTs,         "bdtS",     legendStyle = "LP", drawStyle="LP")
    histo_BDTb         = histograms.Histo(h_BDTb,         "bdtB",     legendStyle = "F", drawStyle="LP")

    #p_BDT = plots.ComparisonPlot(histo_BDTb, histo_BDTs, saveFormats=[])
    p_BDT = plots.ComparisonPlot(histo_BDTs, histo_BDTb, saveFormats=[])
    p_BDT.histoMgr.setHistoLegendLabelMany({"bdtS": "Signal", "bdtB": "Background"})
    
    p_Eff.histoMgr.forHisto("sEff", styles_SEff)
    p_Eff.histoMgr.setHistoDrawStyle("sEff", "L")
    p_Eff.histoMgr.setHistoLegendStyle("sEff", "L")

    p_Eff.histoMgr.forHisto("bEff", styles_BEff)
    p_Eff.histoMgr.setHistoDrawStyle("bEff", "L")
    p_Eff.histoMgr.setHistoLegendStyle("bEff", "L")

    p_Eff.histoMgr.forHisto("signif", styles_Signif)
    p_Eff.histoMgr.setHistoDrawStyle("signif", "L")
    p_Eff.histoMgr.setHistoLegendStyle("signif", "L")

    p_Eff.histoMgr.forHisto("purity", styles_pur)
    p_Eff.histoMgr.setHistoDrawStyle("purity", "L")
    p_Eff.histoMgr.setHistoLegendStyle("purity", "L")

    p_Eff.histoMgr.forHisto("pureff", styles_pureff)
    p_Eff.histoMgr.setHistoDrawStyle("pureff", "L")
    p_Eff.histoMgr.setHistoLegendStyle("pureff", "L")


    p_BDT.histoMgr.forHisto("bdtS", styles_S)
    p_BDT.histoMgr.setHistoDrawStyle("bdtS", "HIST")
    p_BDT.histoMgr.setHistoLegendStyle("bdtS", "L")

    p_BDT.histoMgr.forHisto("bdtB", styles_B)
    p_BDT.histoMgr.setHistoDrawStyle("bdtB", "HIST")
    p_BDT.histoMgr.setHistoLegendStyle("bdtB", "F")


    saveName_eff = "mvaeff"
    saveName     = "mva"
    savePath = os.path.join(opts.saveDir, opts.optMode)

    _kwargs = {
        "xlabel"           : "BDTG", #"Cut value applied on BDTG output",
        "ylabel"           : "Efficiency (Purity)",
        "ratioYlabel"      : "Ratio ",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"xmin": -1.0, "xmax": 1.01, "ymin": 0.0, "ymax": 1.1},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        "createLegend"     : {"x1": 0.45, "y1": 0.45, "x2": 0.70, "y2": 0.70},
        }
    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X") #ROOT.gStyle.SetNdivisions(8, "X")
    plots.drawPlot(p_Eff, savePath, **_kwargs)
    rightAxis.Draw()
    SavePlot(p_Eff, saveName_eff, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf", ".C"])

    _kwargs["log"]  = True
    _kwargs["opts"]["ymin"] = 3e-2
    _kwargs["opts"]["ymax"] = 20
    _kwargs["xlabel"] = "BDTG"# response"
    _kwargs["ylabel"] = "(1/N) dN/dx"
    _kwargs["createLegend"] = {"x1": 0.25, "y1": 0.75, "x2": 0.50, "y2": 0.9}
    style.setWide(False, 0.15)
    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")
    plots.drawPlot(p_BDT, savePath, **_kwargs)
    SavePlot(p_BDT, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf", ".C"])
    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/%s/%s" % (getpass.getuser()[0], getpass.getuser()), "http://home.fnal.gov/~%s" % (getpass.getuser()))
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
    ANALYSISNAME = "TopRecoTree"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [200, 500, 800, 2000]
    #SIGNALMASS   = [300, 500, 800, 1000]
    SIGNALMASS   = []
    #SIGNALMASS   = [200, 500, 800, 1000, 2000, 3000]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"

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

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

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
    
    
    parser.add_option("-r", "--rootfile", dest="rootfile", action="store",
                      help="root file with results")
    
    parser.add_option("--reff", "--effFile", dest="effFile", action="store",
                      help="root file with efficiency plots")
    
    (opts, parseArgs) = parser.parse_args()

    if opts.rootfile == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        print __doc__
        sys.exit(1)

    if opts.effFile == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()

    # Sanity check
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plot_BDTG.py: Press any key to quit ROOT ...")
