#!/usr/bin/env python
'''
Usage:
Launch default script
./plotTemplate.py -m <pseudo_mcrab_directory>

Launch but exclude the M_180 sample
./plotTest.py -m Kinematics_161025_020335 -e M_180

Launch but exclude the multiple signal samples
./plotTest.py -m Kinematics_161025_020335 -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400"

Launch but only include the QCD_Pt samples
./plotTest.py -m Kinematics_161025_020335 -i QCD_Pt

Launch but exclude various samples
./plotTest.py -m Kinematics_161025_020335 -e "M_200|M_220|M_250|M_300|M_350|M_400|QCD_Pt|JetHT"
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
from plotAux import *

import ROOT


#================================================================================================
# Variable Definition
#================================================================================================
kwargs = {
    "verbose"        : False,
    "dataEra"        : "Run2016",
    "searchMode"     : "80to1000",
    "analysis"       : "Hplus2tbAnalysis",
    "optMode"        : "",
    #"savePath"       : "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/all/",
    #"savePath"       : None,
    "savePath"       : os.getcwd() + "/Plots/",
    "refDataset"     : "Data",
    "saveFormats"    : [".png"],
    "normalizeTo"    : "Luminosity", #One", "XSection", "Luminosity"
    "createRatio"    : False,
    "logX"           : False,
    "logY"           : True,
    "gridX"          : True,
    "gridY"          : True,
    "drawStyle"      : "P", # "P",  #"HIST9"
    "legStyle"       : "LP",     # "LP", "F"
    "cutValue"       : 15,
    "cutLine"        : False,
    "cutBox"         : False,
    "cutLessthan"    : False,
    "cutFillColour"  : ROOT.kAzure-4,
}


hNames = ["counters/weighted/counter",
          #"counters/weighted/METFilter selection",
          #"counters/weighted/e selection",
          #"counters/weighted/mu selection",
          #"counters/weighted/jet selection",
          #"counters/weighted/bjet selection",
          ]


#================================================================================================
# Main
#================================================================================================
def main(opts):

    # Setup the style
    style = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)

    # ========================================
    # Datasets
    # ========================================
    # Setup & configure the dataset manager
    datasetsMgr = GetDatasetsFromDir(opts.mcrab, opts, **kwargs)
    intLumi     = GetLumi(datasetsMgr)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities()

    # Set/Overwrite cross-sections
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
    
    # Merge datasets:All JetHT to "Data", QCD_Pt to "QCD", 
    # QCD_bEnriched to "QCD_b",  single-top to "SingleTop", WW, WZ, ZZ to "Diboson"           
    plots.mergeRenameReorderForDataMC(datasetsMgr)

    # Remove datasets
    if 0:
        datasetsMgr.remove("TTJets")
        datasetsMgr.remove(filter(lambda name: not "QCD" in name, datasetsMgr.getAllDatasetNames()))
    
    # Print dataset information
    datasetsMgr.PrintInfo()

    # ========================================
    # Histograms
    # ========================================
    for counter, hName in enumerate(hNames):
        
        # Get the save path and name, Get Histos for Plotter
        savePath, saveName    = GetSavePathAndName(hName, **kwargs)
        refHisto, otherHistos = GetHistosForPlotter(datasetsMgr, hName, **kwargs)
        
        # Create a comparison plot
        #p = plots.ComparisonManyPlot(refHisto, otherHistos)
        p = plots.DataMCPlot(datasetsMgr, hName)

        # Remove negative contributions
        if 0:
            RemoveNegativeBins(datasetsMgr, hName, p)

        # Y-axis
        ratioOpts = {"ymin": 0.0, "ymax": 2.0}
        if kwargs.get("logY")==True:
            opts = {"ymin": 1e-2, "ymaxfactor": 100}
        else:
            opts = {"ymin": 0.0, "ymaxfactor": 1.2}

        # ========================================
        # Frame
        # ========================================
        p.createFrame(saveName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)

        # Legend
        moveLegend = {"dx": -0.11, "dy": +0.0, "dh": +0.2}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        # Move the refDataset to first in the draw order (back)
        histoNames = [h.getName() for h in p.histoMgr.getHistos()]
        p.histoMgr.reorder(filter(lambda n: plots._legendLabels[kwargs.get("refDataset") ] not in n, histoNames))
        if 0:
            p.removeLegend()

        # Axes
        #p.getFrame().GetYaxis().SetTitle( getTitleY(refHisto, **kwargs) )
        #p.getFrame().GetYaxis().SetTitle( getTitleY(p.histoMgr.getHistos()[0], **kwargs) )
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        # Set Log and Grid
        SetLogAndGrid(p, **kwargs)

        # Cut line / Cut box
        _kwargs = {"lessThan": kwargs.get("cutLessthan")}
        p.addCutBoxAndLine(cutValue=kwargs.get("cutValue"), fillColor=kwargs.get("cutFillColour"), box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)

        # Draw the final plot
        p.draw()


        # ========================================
        # Add Text
        # ========================================
        histograms.addStandardTexts(lumi=intLumi)
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)

        # Save the canvas to a file
        SaveAs(p, savePath, saveName, kwargs.get("saveFormats"), counter==0)

    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, 
                      help="Enables batch mode (canvas creation does NOT generates a window)")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, 
                      help="Enables verbose mode (for debugging purposes)")

    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string",
                      help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks" , default="", type="string",
                      help="Exclude this dataset(s) from action [default: '']")

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")
