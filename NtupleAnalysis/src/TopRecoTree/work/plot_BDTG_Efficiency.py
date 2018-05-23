#!/usr/bin/env python
'''
Description:

Usage:
./plot_BDTG_Efficiency.py -r <TMVAoutput_rootFile> --reff mvaeffs.root [opts]

Examples:
./plot_BDTG_Efficiency.py -r TopReco_DR0p3_DPtOverPt0p32.root --reff mvaeffs.root --url

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
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
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(False)
    style.tdrStyle.SetPadRightMargin(0.11)

        # Do the topSelection histos
    folder      = ""

    #=== Define styles: Fixme: Put in function

    styles_S    = styles.StyleCompound([styles.StyleMarker(markerSize=0.4, markerColor=928, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                        styles.StyleLine(lineColor=928, lineStyle=ROOT.kSolid, lineWidth=3),
                                        styles.StyleFill(fillColor=38)])

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

    p_Eff.histoMgr.setHistoLegendLabelMany({"sEff": "Signal Efficiency", 
                                        "bEff": "Bkg Efficiency", 
                                        "signif": "S/ #sqrt{S+B}", 
                                        "purity": "Signal Purity", 
                                        "pureff": "Signal Eff*Purity",})



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

    #rightAxis.SetTitleSize( info->sSig->GetXaxis()->GetTitleSize() )
    rightAxis.SetTitle( "Significance" )

    #=== BDTG output ========================================================
    histo_BDTs         = histograms.Histo(h_BDTs,         "bdtS",     legendStyle = "LP", drawStyle="LP")
    histo_BDTb         = histograms.Histo(h_BDTb,         "bdtB",     legendStyle = "LP", drawStyle="LP")

    p_BDT = plots.ComparisonPlot(histo_BDTb, histo_BDTs,
                                 saveFormats=[])

    p_BDT.histoMgr.setHistoLegendLabelMany({"bdtS": "Signal", 
                                            "bdtB": "Background"})
    
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
    p_BDT.histoMgr.setHistoLegendStyle("bdtB", "L")


    saveName_eff = "mvaeff"
    saveName     = "mva"
    savePath = os.path.join(opts.saveDir, opts.optMode)

    _kwargs = {
        "xlabel"           : "Cut value applied on BDTG output",
        "ylabel"           : "Efficiency (Purity)",
        "ratioYlabel"      : "Ratio ",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymax": 1.1},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        #"createLegend"     : {"x1": 0.5, "y1": 0.75, "x2": 0.9, "y2": 0.9},
        "createLegend"     : {"x1": 0.52, "y1": 0.17, "x2": 0.92, "y2": 0.34},
        }
    
    plots.drawPlot(p_Eff, savePath, **_kwargs)
    rightAxis.Draw()
    SavePlot(p_Eff, saveName_eff, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    _kwargs["log"]  = True
    _kwargs["opts"] = {"ymin": 1e-2, "ymax": 20}
    _kwargs["createLegend"] = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.82}
    _kwargs["xlabel"] = "BDTG response"
    _kwargs["ylabel"] = "(1/N) dN/dx"


    plots.drawPlot(p_BDT, savePath, **_kwargs)
    SavePlot(p_BDT, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])


    return


def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}

    if "ChiSqr" in histo:
        _rebinX = 1
        logY    = True
        _units  = ""
        _format = "%0.1f " + _units
        _xlabel = "#chi^{2}"
        _cutBox = {"cutValue": 10.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 100
    elif "trijetmass" in histo.lower():
        _rebinX = 4
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 805 #1005
    elif "ht" in histo.lower():
        _rebinX = 2
        logY    = False
        _units  = "GeV"
        _format = "%0.0f " + _units
        _xlabel = "H_{T} (%s)" % _units
        _cutBox = {"cutValue": 500, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        #_opts["xmin"] = 500
        _opts["xmax"] = 2000
    elif "tetrajetmass" in histo.lower():
        _rebinX = 5 #5 #10 #4
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500 #3500.0
        #_rebinX = 10
        #_opts["xmax"] = 3500
    elif "tetrajetbjetpt" in histo.lower():
        _rebinX = 2
        logY    = False
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T}  (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 600
    elif "foxwolframmoment" in histo.lower():
        _format = "%0.1f"
        _cutBox = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    else:
        pass

    if logY:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.2

    _opts["ymaxfactor"] = yMaxFactor
    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
        #_opts   = {"ymin": 1e-3, "ymaxfactor": yMaxFactor, "xmax": None}
    else:
        _opts["ymin"] = 1e0
        #_opts["ymaxfactor"] = yMaxFactor
        #_opts   = {"ymin": 1e0, "ymaxfactor": yMaxFactor, "xmax": None}

    # Customise styling
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    if "QCD" in datasetsMgr.getAllDatasets():
        p.histoMgr.forHisto("QCD", styles.getQCDFillStyle() )
        p.histoMgr.setHistoDrawStyle("QCD", "HIST")
        p.histoMgr.setHistoLegendStyle("QCD", "F")

    if "TT" in datasetsMgr.getAllDatasets():
        p.histoMgr.setHistoDrawStyle("TT", "AP")
        p.histoMgr.setHistoLegendStyle("TT", "LP")

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))

    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath) 
    return

#Fit(datasetsMgr.getAllDatasets(), folder+"/"+HistoFit[i], "gaus")
def Fit (datasets, histo, function):
    
    
    FitList = []
    for dataset in datasets:

        datasetName = dataset.getName()
        print "Dataset = ", datasetName
        hh = dataset.getDatasetRootHisto(histo)
 
        hh.normalizeToOne()
        h = hh.getHistogram()

        #h = dataset.getDatasetRootHisto(histo).getHistogram()
        xMin  = h.GetXaxis().GetXmin()
        xMax  = h.GetXaxis().GetXmax()
        yMin  = 0
        yMax  = 1.2
        #statOption = ROOT.TEfficiency.kFNormal
        if "TT" in datasetName:
            if function == "gaus":
                fitGauss = ROOT.TF1("fitGauss", "gaus", -2.5, 2.5)
#                TF1 *fitBoFreq = new TF1("fitBoFreq","[0]*x+[1]",0,20);
#                h.Fit("gaus")
                #fitTest = ROOT.TF1("fitTest", "0.01", -2.5, 2.5)
                
                h.Fit("fitGauss","SRBM")
                #h.GetListOfFunctions().Add(fitTest)
                legend = "TT"

        legend = "a legend"
        print "Legend", legend
        saveName = histo.split("/")[-1]+"_Fit"

        print saveName

        xTitle = "fixXTitle"
        yTitle = "fixYTitle"
    
        yMin = 0.
        yMax = 0.03
        xMin = -2.3
        xMax = 2.3
        kwargs = {}

        options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
        FitList.append(h)
        #p = plots.MCPlot(dataset, h, normalizeToLumi=0, saveFormats=[], **kwargs)

        p = plots.PlotBase(datasetRootHistos=FitList, saveFormats=kwargs.get("saveFormats"))
        p.createFrame(saveName, opts=options)
        
        p.getFrame().GetXaxis().SetTitle(xTitle)
        p.getFrame().GetYaxis().SetTitle(yTitle)
        #p.histoMgr.setHistoDrawStyle(datasetName, "AP")
        
# Set range                                                                                                                                                                          
        p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)

        
        moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}

        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        # Add Standard Texts to plot        
        histograms.addStandardTexts()
    
        p.draw()
    
    # Save plot in all formats                                                                                                                                                           
        savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
        save_path = savePath 
        SavePlot(p, saveName, save_path)
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
        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s/" % (getpass.getuser()))
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
        raw_input("=== plotMC_HPlusMass.py: Press any key to quit ROOT ...")
