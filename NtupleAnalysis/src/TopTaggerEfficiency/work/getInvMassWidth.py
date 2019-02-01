#!/usr/bin/env python
'''
DESCRIPTION:
This script calculates and plots the width of the fully matched invariant mass (FWHM) as a function of the signal mass by fitting the mass distribution to a Gauss function

USAGE:
./plotMC_InvMassSmearing.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./getInvMassWidth.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_190106_084255_BDT0p40_TopMassCut400_noTopPtRew/ --url
./getInvMassWidth.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_190106_084255_BDT0p40_TopMassCut400_noTopPtRew/ --signalMass 500  --url 

(The first example command produces the fitting plots for all the mass points and the FWHM vs signalMass plot
The second example will produce only the fitting plot for the given signal mass)

LAST USED:
./getInvMassWidth.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_190106_084255_BDT0p40_TopMassCut400_noTopPtRew/ --url

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
ROOT.gROOT.SetBatch(True)
from ROOT import *

import array
import math
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
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
    

def main(opts):

    optModes = [""]

    if opts.optMode != None:
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
            #if "ChargedHiggs_HplusTB_HplusToTB_M_%s" % (opts.signalMass) in d.getName():
            if "ChargedHiggs_HplusTB_HplusToTB_M_" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
            else:
                datasetsMgr.remove(d.getName())
                
        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        else:
            opts.intLumi = 35920

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            
            if str(opts.signalMass) not in d.getName():
                continue
            datasetOrder.append(d.getName())

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setGridX(False)
        style.setGridY(False)

        # Do the histograms
        if opts.signalMass > -1:
            r = Fit_Gaus(datasetsMgr, opts.signalMass)
        else:
            align  = "{:>25} {:>10} {:>10}"
            title  = align.format("m_{H^{+}}", "FWHM", "Error" )
            hLine  = 50*"="
            table = []
            table.append(hLine)
            table.append(title)
            table.append(hLine)    
            const = 2*math.sqrt(2*math.log(2))
            y     = []
            xerrl = []
            xerrh = []
            yerrl = []
            yerrh = []
            mass  = []
            for d in datasetsMgr.getAllDatasets():
                if "Charged" in d.getName():
                    dName = d.getName()
                    signalmass = dName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "")
                    signalmass = int(signalmass)
                    if (signalmass == 180):
                        continue
                    r = Fit_Gaus(datasetsMgr, signalmass)
                    mass.append(signalmass)
                    sigma = r.Parameter(2)
                    sigmaerror = r.ParError(2)
                    y.append(const*sigma)
                    xerrl.append(0.0)
                    xerrh.append(0.0)
                    yerrl.append(const*sigmaerror)
                    yerrh.append(const*sigmaerror)
                    table.append(align.format(" %.0f & " %(signalmass), " %.2f & " %(const*sigma), "+/- %.2f" %(const*sigmaerror)))
            table.append(hLine)
            # Print values
            for row in table:
                print row
            tgraph     = ROOT.TGraphAsymmErrors(len(mass) ,
                                                array.array("d",mass),
                                                array.array("d",y),
                                                array.array("d",xerrl),
                                                array.array("d",xerrh),
                                                array.array("d",yerrl),
                                                array.array("d",yerrh))
            testSigma = 0
            if testSigma:
                tgraph_s = ROOT.TGraphAsymmErrors(len(mass) ,
                                                  array.array("d",mass),
                                                  array.array("d",sigma),
                                                  array.array("d",xerrl),
                                                  array.array("d",xerrh),
                                                  array.array("d",sigmaerror),
                                                  array.array("d",sigmaerror))

            counter = 4
            styles.markerStyles[counter].apply(tgraph)
            legend = " "
            hlist = []
            saveName = "HPlusMass_vs_FWHM"
            ytitle = "Width (GeV/c^{2})"
    
            if testSigma:
                styles.markerStyles[2].apply(tgraph_s)
                styles.markerStyles[1].apply(tgraph_mu)
                hlist.append(histograms.HistoGraph(tgraph_s, "#sigma", "lp", "P"))   
                hlist.append(histograms.HistoGraph(tgraph, "FWHM = 2*#sqrt{2ln2}#sigma", "lp", "P"))
                saveName = "HPlusMass_vs_Width"
                ytitle = "Width (GeV/c^{2})"
   
            else:
                hlist.append(histograms.HistoGraph(tgraph, legend, "", "P"))
    
            p = plots.PlotBase(datasetRootHistos=hlist, saveFormats=[])
    
            _kwargs = {           
                "xlabel"           : "m_{H^{+}} (GeV/c^{2})",
                "ylabel"           : ytitle, #"Width (GeV/c^{2})", #/ %.1f ",                                                                
                "ratioYlabel"      : "Ratio",
                "ratio"            : False,
                "ratioInvert"      : False,
                "stackMCHistograms": False,
                "addMCUncertainty" : False,
                "addLuminosityText": False,
                "addCmsText"       : True,
                "cmsExtraText"     : "Preliminary",
                #"opts"             : {"ymin": 0.0, "ymax": 1.09},
                "opts"             : {"xmin": 150, "xmax": 950, "ymin": 0.0, "ymaxfactor": 1.2},
                "opts2"            : {"ymin": 0.6, "ymax": 1.4},
                "log"              : False,
                "moveLegend"       : {"dx": -0.25, "dy": -0.005, "dh": -0.2},
                "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
                }
            plots.drawPlot(p, saveName, **_kwargs)

            SavePlot(p, saveName, opts.saveDir, saveFormats = [".png", ".pdf", ".C"])

    return

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]


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
        Print(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return



def Fit_Gaus(datasetsMgr, signalMass):

    # Definitions
    kwargs = {}
    histos = []

    dName   =  "ChargedHiggs_HplusTB_HplusToTB_M_%s" % (signalMass)
    hName   = "AnalysisTripletsTrue/TetrajetMass_LdgTopIsHTop"
    dataset = datasetsMgr.getDataset(dName)
    dx      = signalMass/2 + 50
    xmin    = signalMass - dx;
    xmax    = signalMass + dx;
    _rebin  = 2

    # Get histograms
    pp = plots.MCPlot(datasetsMgr, hName, normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)

    myhist  = pp.histoMgr.getHisto(dName).getRootHisto().Clone("TetrajetMass_LdgTopIsHTop0")
    if (opts.normaliseToOne):
        myhist.Scale(1./myhist.Integral())
    myhist.Rebin(_rebin)    
    
    #Initialize parameters
    #===Gaus
    g_const = myhist.Integral() #myhist.GetMaximum()
    g_mean  = signalMass
    g_sigma = signalMass*0.1
    xminR   = signalMass - g_sigma
    xmaxR   = signalMass + g_sigma
    par     = array.array('f',[g_const, g_mean, g_sigma])

    xminR, xmaxR = GetFitRange(signalMass)
    G1      = ROOT.TF1("G1", "gaus", xminR , xmaxR)

    #Set parameters
    G1.SetParameters( par[0], par[1], par[2])

    # Fit my function to the histo (https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html)
    r = myhist.Fit("G1","WL Q R S")
    print "="*50
    print "***Fitting Results:***"
    print "Signal Mass = %.0f GeV" % (signalMass)
    if 0:
        print "chi2   = %.1f " %  (r.Chi2() )
        print "ndf    = %.0f " %  (r.Ndf() )
    print "chi2-N = %.1f " %  (r.Chi2() / r.Ndf())
    print "const  = %.2f " %  (r.Parameter(0) )
    print "constE = %.2f " %  (r.ParError(0) )
    print "mean   = %.1f  +/- %.1f GeV" %  (r.Parameter(1), r.ParError(1) )
    print "sigma  = %.1f +/- %.1f GeV" %  (r.Parameter(2), r.ParError(2) )
    FWHM   = 2*math.sqrt(2*math.log(2))*r.Parameter(2)
    FWHM_E = 2*math.sqrt(2*math.log(2))*r.ParError(2)
    print "FWHM   = %.1f +/- %.1f GeV" %  (FWHM, FWHM_E)
    print "="*50

    par = G1.GetParameters()
    myhist.GetFunction("G1").SetLineWidth(3);
    myhist.Draw()

    #Update parameters
    width  = myhist.GetXaxis().GetBinWidth(0) #bin width
    ibinmn = myhist.GetXaxis().FindBin(xmin)  #first bin
    ibinmx = myhist.GetXaxis().FindBin(xmax)  #last bin
    g1_integral = G1.Integral(xmin,xmax)/width
    g1_mean  = G1.GetParameter(1)
    g1_sigma = G1.GetParameter(2)

    myhist.SetMarkerStyle(20);
    myhist.SetMarkerSize(0.4);
    myhist.GetXaxis().SetRangeUser(xmin - 50, xmax + 50);
    
    G1.SetLineColor(kRed);
    G1.SetLineWidth(3)
    G1.Draw("same");

    ROOT.gStyle.SetOptFit(1);
    sb1 = ROOT.TPaveStats()
    ROOT.gPad.Update()
    sb1 = myhist.FindObject("stats")
    sb1.SetX1NDC(0.65)
    sb1.SetX2NDC(0.92)
    sb1.SetY1NDC(0.65)
    sb1.SetY2NDC(0.8)
    sb1.SetLineColor(2)

    p = plots.MCPlot(datasetsMgr, "AnalysisTripletsTrue/TetrajetMass_LdgTopIsHTop", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    hTopTrue = p.histoMgr.getHisto(dName).getRootHisto().Clone("Matched")
    histos.append(hTopTrue)

    p0 = plots.PlotBase(datasetRootHistos=[hTopTrue], saveFormats=[])
    p0.histoMgr.forHisto("Matched", styles.getGenuineBLineStyle()) 
    p0.histoMgr.setHistoDrawStyle("Matched", "AP")
    p0.histoMgr.setHistoLegendLabelMany({"Matched": "m_{H^{+}} = %s GeV" % (signalMass)})

    p0.appendPlotObject(G1)
    saveName = "TetrajetMass_G1"
    _units   = "GeV/c^{2}"

    if opts.normaliseToOne:
        yLabel = "Arbitrary Units / %0.0f " + _units
    else:
        yLabel = "Events / %0.0f " + _units

    #if signalMass > 500:
    if 0:
        _leg     = {"x1": 0.20, "y1": 0.65, "x2": 0.45, "y2": 0.87}
    else:
        _leg     = {"x1": 0.60, "y1": 0.65, "x2": 0.85, "y2": 0.87}

    if opts.logY:
        ymin  = 1e-3
        ymaxf = 5
    else:
        ymin  = 0.0
        ymaxf = 1.3

    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    plots.drawPlot(p0, 
                   saveName,
                   xlabel       = "m_{jjbb} (%s)" % (_units),
                   ylabel       = yLabel,
                   log          = opts.logY,
                   rebinX       = _rebin, #2, 5
                   cmsExtraText = "Preliminary",
                   createLegend = _leg,
                   opts         = {"xmin": signalMass - 5*g_sigma, "xmax":  signalMass + 5*g_sigma, "ymin": ymin, "ymaxfactor": ymaxf}, #xmin - 50, xmax + 50
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = {"cutValue": signalMass, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
                   )

    # Save plot in all formats    
    savePath = os.path.join(opts.saveDir, opts.optMode)
    SavePlot(p0, "%s_M%s" % (saveName, signalMass), savePath) 

    return r


def GetFitRange(signalMass):      
    if (signalMass == 200):
        xminR = 170
        xmaxR = 240
    elif (signalMass == 220):
        xminR = 150
        xmaxR = 260
    elif (signalMass == 250):
        xminR = 200
        xmaxR = 290
    elif (signalMass == 300):
        xminR = 260
        xmaxR = 330
    elif (signalMass == 350):
        xminR = 290
        xmaxR = 390
    elif (signalMass == 400):
        xminR = 340
        xmaxR = 440
    elif (signalMass == 500):
        xminR = 420
        xmaxR = 550
    elif (signalMass == 650):
        xminR = 560
        xmaxR = 680
    elif (signalMass == 800):
        xminR = 650
        xmaxR = 850
    elif (signalMass == 1000):
        xminR = 850
        xmaxR = 1050
    else:
        xminR = 0
        xmaxR = 1200
    return xminR, xmaxR
        
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
    OPTMODE      = ""
    BATCHMODE    = True
    SIGNALMASS   = -1
    INTLUMI      = -1.0
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    VERBOSE      = False
    NORMALISE    = False
    ANALYSISNAME = "TopTaggerEfficiency"
    SAVEDIR      = None #"/publicweb/a/aattikis/" + ANALYSISNAME
    LOGY         = False
    FUNC         = "crystalball"
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

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS,
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

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

    parser.add_option("--logY", dest="logY", action="store_true", 
                      help="Set y-axis to log scale [default: %s]" % (LOGY) )

    parser.add_option("--func", dest="func", type="string", default=FUNC,
                      help="Fitting function. Options: gaus1, gaus2, crystalball,  gaus_crystal. [default: %s]" % FUNC)



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

    # Sanity check
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    # Save directory
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 2000, 3000]
    if opts.signalMass not in allowedMass:
        if opts.signalMass > -1:
            raise Exception("Signal mass invalid")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotMC_InvMassSmearing.py: Press any key to quit ROOT ...")
