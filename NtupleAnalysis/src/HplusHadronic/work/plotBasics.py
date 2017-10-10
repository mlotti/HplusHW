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
from plotAux import *

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
kwargs = {
    "analysis"       : "HplusHadronic",
    #"savePath"       : "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/all/",
    "savePath"       : "/publicweb/s/skonstan/Plots/",
    "refDataset"     : "ChargedHiggs_HplusTB_HplusToTB_M_200",
    "rmDataset"      : [], #["QCD"],
    "saveFormats"    : [".pdf"],#, ".pdf"],
    "normalizeTo"    : "One", #One", "XSection", "Luminosity"
    "createRatio"    : False,
    "logX"           : False,
    "logY"           : False,
    "gridX"          : True,
    "gridY"          : True,
    "drawStyle"      : "HIST9", # "P",  #"HIST9"
    "legStyle"       : "F",     # "LP", "F"
    "verbose"        : False,
    "cutValue"       : 5,
    "cutBox"         : False,
    "cutLine"        : False,
    "cutLessthan"    : False,
    "cutFillColour"  : ROOT.kAzure-4,
    "rebinX"         : 1,
}

hNames  = ["DPhi_LdgTrijet_SubldgTrijet","Rapidity_LdgTrijet","Rapidity_SubldgTrijet","Rapidity_Tetrajet","SumPt_LdgTrijet_SubldgTrijet","CosTheta_Bjet1TopCM_TrijetLab","CosTheta_Bjet1TopCM_Zaxis","CosTheta_Bjet2TopCM_TrijetLab","CosTheta_Bjet2TopCM_Zaxis","CosTheta_Bjet3TopCM_TrijetLab","CosTheta_Bjet3TopCM_Zaxis","METoverSqrtHT","CosTheta_LdgTrijetLdgJetTopCM_TrijetLab","CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab","CosTheta_LdgTrijetBjetTopCM_TrijetLab","CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab","CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab","CosTheta_SubldgTrijetBjetTopCM_TrijetLab","DEta_LdgTrijetDijet_TetrajetB","DPhi_TetrajetB_LdgTrijetB","BJetPair_dPhiAvg","BJetPair_MaxMass_M","BJetPair_dRMin_Mass",
]



#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()

    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)
    
    # Get all datasets from the mcrab dir
    datasetsMgr  = GetDatasetsFromDir(parseOpts.mcrab, kwargs.get("analysis"))

    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = GetLumi(datasetsMgr)
    
    # Update to PU
    datasetsMgr.updateNAllEventsToPUWeighted()

    # Remove datasets
    datasetsMgr.remove(kwargs.get("rmDataset"))
    #datasetsMgr.remove(filter(lambda name: not "TT" in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "180" in name in name, datasetsMgr.getAllDatasetNames()))
    #datasetsMgr.remove(filter(lambda name: "200" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "220" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "250" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "350" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "400" in name in name, datasetsMgr.getAllDatasetNames()))
    #datasetsMgr.remove(filter(lambda name: "500" in name in name, datasetsMgr.getAllDatasetNames()))
    #datasetsMgr.remove(filter(lambda name: "800" in name in name, datasetsMgr.getAllDatasetNames()))
#    datasetsMgr.remove(filter(lambda name: "1000" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "2000" in name in name, datasetsMgr.getAllDatasetNames()))
    datasetsMgr.remove(filter(lambda name: "3000" in name in name, datasetsMgr.getAllDatasetNames()))

    # Set custom XSections
    # d.getDataset("TT_ext3").setCrossSection(831.76)
    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
    plots.mergeRenameReorderForDataMC(datasetsMgr) #WARNING: Merged MC histograms must be normalized to something!

    # Remove datasets (for merged names)
    datasetsMgr.remove(kwargs.get("rmDataset"))

    
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        
        # Get the save path and name
        savePath, saveName = GetSavePathAndName(hName, **kwargs)

        saveName = saveName 
        # Get Histos for Plotter
        refHisto, otherHistos = GetHistosForPlotter(datasetsMgr, hName, **kwargs)
        
        # Create a comparison plot
        p = plots.ComparisonManyPlot(refHisto, otherHistos)

        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))

        # Remove negative contributions
        #RemoveNegativeBins(datasetsMgr, hName, p)

        # Create a frame
        if kwargs.get("logY"):
            opts = {"ymin": 1e-3, "ymaxfactor": 5}
        else:
            opts = {"ymin": 0.0, "ymaxfactor": 1.2}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0}
        p.createFrame(saveName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)
        
        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.0}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        #p.removeLegend()

        # Customise frame
        p.getFrame().GetYaxis().SetTitle( getTitleY(refHisto, **kwargs) )
        #p.setEnergy("13")
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        # SetLog
        SetLogAndGrid(p, **kwargs)
 
        # Add cut line/box
        _kwargs = { "lessThan": kwargs.get("cutLessThan")}
        p.addCutBoxAndLine(cutValue=kwargs.get("cutValue"), fillColor=kwargs.get("cutFillColour"), box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)

        # Move the refDataset to first in the draw order (back)
        histoNames = [h.getName() for h in p.histoMgr.getHistos()]
        p.histoMgr.reorder(filter(lambda n: plots._legendLabels[kwargs.get("refDataset") ] not in n, histoNames))
                
        #  Draw plots
        p.draw()

        # Customise text
        #histograms.addStandardTexts(lumi=intLumi)
        histograms.addStandardTexts()
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)

        # Save canvas under custom dir                                                                                                        
        SaveAs(p, savePath, saveName, kwargs.get("saveFormats"))

  
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
        
