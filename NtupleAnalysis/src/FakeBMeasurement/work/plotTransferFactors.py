#!/usr/bin/env python
'''
DESCRIPTION:
This script loads and plots the transfer-factors of the Fake-b measurement (R_i) 
for all the bins considered onto a signle TGraphAsymmetry object

INSTRUCTIONS:


USAGE:
plotTransferFactors.py [opts]


EXAMPLES:
plotTransferFactors.py [opts]
plotTransferFactors.py --cutLine 500 --gridX --gridY --yMin 1e-3 --yMax 10
./plotTransferFactors.py -m FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm0p20to0p40_6BinsAbsEta_NoFatjetVeto_180318_085359 --gridX --gridY --yMax 10 --logy
./plotTransferFactors.py -m FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm0p20to0p40_6BinsAbsEta_NoFatjetVeto_180318_085359 --gridX --gridY 

LAST USED:
./plotTransferFactors.py -m FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm0p20to0p40_6BinsAbsEta_NoFatjetVeto_180318_085359 --gridX --gridY --yMin 0.0 --yMax 1

'''

#================================================================================================
# Import modules
#================================================================================================
import os
import getpass
import sys
from optparse import OptionParser
import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#================================================================================================
# Function definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def GetDatasetsFromDir(opts):
    
    datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                    dataEra=opts.dataEra,
                                                    searchMode=opts.searchMode, 
                                                    analysisName=opts.analysisName,
                                                    optimizationMode=opts.optMode)
    return datasets

def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(True)
    style.setGridY(True)

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities() # from lumi.json
    plots.mergeRenameReorderForDataMC(datasetsMgr) 
    opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()

    # Do the plot
    doPlot()

    # Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return


def doPlot():
    
    # Import the auto-generated file containing the transfer factors
    sys.path.append(opts.mcrab)
    import FakeBTransferFactors_Run2016_80to1000 as tf

    QCDNormalization = {
        "Inclusive": 0.441958,
        "1": 0.524575,
        "0": 0.600980,
        "3": 0.363374,
        "2": 0.457656,
        "5": 0.229395,
        "4": 0.315185,
        }

    xval  = []
    xerrl = []
    xerrh = []
    yval  = []
    yerrl = []
    yerrh = []

    # Fill TGraph arrays
    for i, k in enumerate(tf.QCDNormalization):
        xval.append(k)
        xerrl.append(0.001)
        xerrh.append(0.001)
        yval.append(QCDNormalization[k])
        yerrl.append(0.01*QCDNormalization[k])
        yerrh.append(0.01*QCDNormalization[k])

    # Create TGraph object
    tgraph= ROOT.TGraphAsymmErrors(len(xval),
                                   array.array("d", xval ),
                                   array.array("d", yval ),
                                   array.array("d", xerrl),
                                   array.array("d", xerrh),
                                   array.array("d", yerrl),
                                   array.array("d", yerrh)
                                   )
    # Apply styles
    setNominalStyle(tgraph)

    # Convert the TGraphs to HistoGraphs and append to a list
    graphs = []
    graphs.extend([
            #histograms.HistoGraph(tgraph, "Nominal", drawStyle="F", legendStyle="fl"),
            histograms.HistoGraph(tgraph, "Nominal", drawStyle="P", legendStyle="LP"),
            ])

    # Plot the TGraphs
    saveFormats = [".png", ".C", ".pdf"]
    plot = plots.PlotBase(graphs, saveFormats=saveFormats)
    plot.setLuminosity(opts.intLumi)

    # Customise legend entries
    plot.histoMgr.setHistoLegendLabelMany({
            #"Nominal" : "R_{i} #pm #sigma_{R_{i}}",
            "Nominal" : "Nominal #pm Stat.",
            })
    
    # Create legend
    xPos   = 0.65
    legend = getLegend(opts, xPos)
    plot.setLegend(legend)

    # Create a frame to be able to impose custom x- and y- range
    if opts.yMin != -1 and opts.yMax != -1:
        plot.createFrame("dumbie", opts={"ymin": opts.yMin, "ymax": opts.yMax})
    elif opts.yMin != -1:
        plot.createFrame("dumbie", opts={"ymin": opts.yMin})
    elif opts.yMax != -1:
        plot.createFrame("dumbie", opts={"ymax": opts.yMax})
    else:
        plot.createFrame("dumbie", saveFormats=[])

    # Add cut box?
    if opts.cutLine > 0:
        kwargs = {"greaterThan": True}
        plot.addCutBoxAndLine(cutValue=opts.cutLine, fillColor=ROOT.kRed, box=False, line=True, **kwargs)

    # Set x-axis title
    plot.frame.GetXaxis().SetTitle("bin") 

    plot.frame.GetYaxis().SetTitle("transfer factor (R_{i})")

    # Enable/Disable logscale for axes
    plot.getPad().SetLogy(opts.logY)
    plot.getPad().SetLogx(opts.logX)

    # Enable grids in x and y?
    plot.getPad().SetGridx(opts.gridX)
    plot.getPad().SetGridy(opts.gridY)

    # Draw the plot with standard texts
    plot.draw()
    plot.addStandardTexts()
    
    # Add text on canvas
    if 0:
        histograms.addText(0.55, 0.84, "fully hadronic final state", size=20)
    
    # Save the canvas
    plot.save()

    # Save the plots
    SavePlot(plot, "transferFactors", os.path.join(opts.saveDir, "") )
    return

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

def getLegend(opts, xLeg1=0.53):
    dy = -0.10

    # Create customised legend
    #xLeg1 = 0.53
    xLeg2 = 0.93
    yLeg1 = 0.78 + dy
    yLeg2 = 0.91 + dy

    # Adjust legend slightly to visually align with text
    legend = histograms.createLegend(xLeg1*.98, yLeg1, xLeg2, yLeg2) 
    legend.SetMargin(0.17)

    # Make room for the final state text
    # legend.SetFillStyle(1001) #legend.SetFillStyle(3001)
    return legend

def setNominalStyle(graph):
    graph.SetLineStyle(ROOT.kSolid)
    graph.SetLineWidth(3)
    graph.SetLineColor(ROOT.kRed)
    graph.SetMarkerStyle(ROOT.kFullCircle)
    graph.SetMarkerColor(ROOT.kRed)
    return

def setStyle1(graph):
    graph.SetFillColor(ROOT.kGreen-3)
    setExpectedStyle(graph)
    return    

def setStyle2(graph):
    graph.SetFillColor(ROOT.kYellow)
    setExpectedStyle(graph)
    return

if __name__ == "__main__":

    # Default Settings
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    VERBOSE     = False
    PAPER       = False
    CUTLINE     = 0
    LOGX        = False
    LOGY        = False
    GRIDX       = False
    GRIDY       = False
    MINY        = -1
    MAXY        = -1
    SAVEDIR     = None
    URL         = False
    OPTMODE     = ""

    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)


    parser.add_option("--logX", dest="logX", default=LOGX, action="store_true",
                      help="Enable x-axis log scale [default: %s]" % (LOGX))

    parser.add_option("--logY", dest="logY", default=LOGY, action="store_true",
                      help="Enable y-axis log scale [default: %s]" % (LOGY))

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)

    parser.add_option("--cutLine", dest="cutLine", type="int", default=CUTLINE,
                      help="Number of digits (precision) to print/save limit results [default: %s]" % (CUTLINE) )

    parser.add_option("--gridX", dest="gridX", default=GRIDX, action="store_true",
                      help="Enable the grid for the x-axis [default: %s]" % (GRIDX) )

    parser.add_option("--gridY", dest="gridY", default=GRIDY, action="store_true",
                      help="Enable the grid for the y-axis [default: %s]" % (GRIDY) )

    parser.add_option("--yMin", dest="yMin", default=MINY, type="float",
                      help="Overwrite automaticly calculated minimum value of y-axis [default: %s]" % (MINY) )

    parser.add_option("--yMax", dest="yMax", default=MAXY, type="float",
                      help="Overwrite automaticly calculated maximum value of y-axis [default: %s]" % (MAXY) )

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR,
                      help="Directory where all plots will be saved [default: %s]" % SAVEDIR)

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    (opts, args) = parser.parse_args()

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath("", prefix="", postfix="Test")


    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)

    main(opts)
    
