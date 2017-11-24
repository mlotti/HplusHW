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
    "verbose"        : False,
    "dataEra"        : "Run2016",
    "searchMode"     : "80to1000",
    "analysis"       : "Hplus2tbAnalysis",
    "optMode"        : "",
    #"savePath"       : "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/M_200/",
    #"savePath"       : None,
    "refDataset"     : "ChargedHiggs_HplusTB_HplusToTB_M_1000",#"ChargedHiggs_HplusTB_HplusToTB_M_500",
#    "savePath"       : "/publicweb/s/skonstan/MyPlots/CorrelationPlots/",
    "savePath"       : "/publicweb/s/skonstan/Hplus2tbAnalysis/HplusMasses/topbdtSelectionTH2_/",
    #"savePath"       : "/publicweb/a/aattikis/EvtShapeVars/",
    "saveFormats"    : ["_1000"+".pdf"],
    "normalizeTo"    : "One", #One", "XSection", "Luminosity"
    "zMin"           : None,
    "zMax"           : None,
    "rebinX"         : 1,
    "rebinY"         : 1,
    "createRatio"    : False,
    "logX"           : False,
    "logY"           : False,
    "logZ"           : True,
    "gridX"          : True,
    "gridY"          : True,
    "drawStyle"      : "COLZ", #"CONT4" "COLZ" "COL"
    "legStyle"       : "F",     # "LP", "F"
    "cutValue"       : None,
    "cutBox"         : False,
    "cutLine"        : False,
    "cutLessthan"    : False,
    "cutFillColour"  : ROOT.kAzure-4,
    "addLuminosityText": False,
#    "MVAcut" : "MVA",
}


hNames = [
#    "TrijetCandidate/TrijetPtDr_TrijetMass","TrijetCandidateGenuine/TrijetPtDr_TrijetMass","TrijetCandidateFake/TrijetPtDr_TrijetMass",
#    "TrijetCandidate/TrijetPtDr_BjetLdgJetMass","TrijetCandidateGenuine/TrijetPtDr_BjetLdgJetMass","TrijetCandidateFake/TrijetPtDr_BjetLdgJetMass",
#    "TrijetCandidate/DijetPtDr_DijetMass","TrijetCandidateGenuine/DijetPtDr_DijetMass","TrijetCandidateFake/DijetPtDr_DijetMass",
#    "TrijetCandidate/DijetPtDr_TrijetMass","TrijetCandidateGenuine/DijetPtDr_TrijetMass","TrijetCandidateFake/DijetPtDr_TrijetMass",
#    "TrijetCandidate/TrijetMass_BjetLdgJetMass","TrijetCandidateGenuine/TrijetMass_BjetLdgJetMass","TrijetCandidateFake/TrijetMass_BjetLdgJetMass",
#    "TrijetCandidate/TrijetMass_BjetSubldgJetMass","TrijetCandidateGenuine/TrijetMass_BjetSubldgJetMass","TrijetCandidateFake/TrijetMass_BjetSubldgJetMass",
#    "TrijetCandidate/TrijetMass_DijetMass","TrijetCandidateGenuine/TrijetMass_DijetMass","TrijetCandidateFake/TrijetMass_DijetMass",
    "topbdtSelectionTH2_/TrijetCountVsBDTcuts","topbdtSelectionTH2_/NjetsVsNTrijets_beforeBDT", "topbdtSelectionTH2_/NjetsVsNTrijets_afterBDT","topbdtSelectionTH2_/DeltaBDTmaxVsTrijetPassBDTvalue","topbdtSelectionTH2_/DeltaBDTminVsTrijetPassBDTvalue", 
"topbdtSelectionTH2_/TopFromHiggsPtVSAssocTopPt",
"topbdtSelectionTH2_/DEta_Dijet1TetrajetBjet_Vs_DEta_Dijet2TetrajetBjet",
"topbdtSelectionTH2_/DPhi_Dijet1TetrajetBjet_Vs_DPhi_Dijet2TetrajetBjet",
"topbdtSelectionTH2_/DR_Dijet1TetrajetBjet_Vs_DR_Dijet2TetrajetBjet",
"topbdtSelectionTH2_/DEta_WFromHBjetFromH_Vs_DEta_WFromAssocTopBjetFromH",
"topbdtSelectionTH2_/DPhi_WFromHBjetFromH_Vs_DPhi_WFromAssocTopBjetFromH",
"topbdtSelectionTH2_/DR_WFromHBjetFromH_Vs_DR_WFromAssocTopBjetFromH",
    
]



#================================================================================================
# Main
#================================================================================================
def main(opts):
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setWide(True, 0.15)

###    style = tdrstyle.TDRStyle()
###    #style.setWide(True)
###    style.setPaletteMy()
###    ROOT.gStyle.SetNumberContours(20)
    # tdrstyle.setDeepSeaPalette()
    # tdrstyle.setRainBowPalette()
    # tdrstyle.setDarkBodyRadiatorPalette()
    # tdrstyle.setGreyScalePalette()
    # tdrstyle.setTwoColorHuePalette()
    style.setWide(True, 0.15)
    
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
    #datasetsMgr.PrintLuminosities()

    # Set/Overwrite cross-sections
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
    
    # Merge datasts (Note: Merged MC histograms must be normalized to something)
    plots.mergeRenameReorderForDataMC(datasetsMgr)

    # Remove datasets
    if 0:
        datasetsMgr.remove("TTJets")
        datasetsMgr.remove(filter(lambda name: not "QCD" in name, datasetsMgr.getAllDatasetNames()))
    
    # Print dataset information
    datasetsMgr.PrintInfo()
                  
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        savePath, saveName = GetSavePathAndName(hName, **kwargs)                

        # Get Histos for Plotter
        refHisto, otherHistos = GetHistosForPlotter(datasetsMgr, hName, **kwargs)

        # Create a plot
        p = plots.PlotBase([refHisto], kwargs.get("saveFormats"))
        
        # Remove negative contributions
        #RemoveNegativeBins(datasetsMgr, hName, p)

        # Customize
        # p.histoMgr.setHistoDrawStyleAll("COL") #"CONT4" "COLZ" "COL"
        
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinY(kwargs.get("rebinY")))
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetXaxis().SetRangeUser(1.0, 5.0))
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetYaxis().SetRangeUser(1.0, 5.0))
        # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetRangeUser(0.0, 0.015))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(0.00001))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(0.05))

#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(2))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinY(2))

#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(0.0009))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(0.0041))

#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(0.0012))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(0.00435))
        if "before" in hName: 
            p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetYaxis().SetTitle("Trijet multiplicity - Before BDT"))
        if "after" in hName: 
            p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetYaxis().SetTitle("Trijet multiplicity - After BDT"))

        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle("Arbitrary Units"))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(2.))
    #ROOT.gPad.RedrawAxis()                                                                                                                                                              
        
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMinimum(kwargs.get("zMin")))
#        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMaximum(kwargs.get("zMax")))


        
        # Create a frame
        opts = {"ymin": 0.0, "ymaxfactor": 1.0}
        p.createFrame(saveName, opts=opts)


        # Customise frame
        p.getFrame().GetXaxis().SetTitle( getTitleX(refHisto, **kwargs) )
        #p.getFrame().GetYaxis().SetTitle( getTitleY(refHisto, **kwargs) )
        
        # SetLog
        SetLogAndGrid(p, **kwargs)

        # Add cut line/box
        _kwargs = { "lessThan": kwargs.get("cutLessThan")}
        p.addCutBoxAndLine(cutValue=kwargs.get("cutValue"), fillColor=kwargs.get("cutFillColour"), box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)
        
        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": +0.0, "dh": -0.1}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        p.removeLegend()

        # Add MC Uncertainty (Invalid method for a 2-d histogram)
        #p.addMCUncertainty()
            # Customise histogram (after frame is created)                                                                                                                                       
        #  Draw plots
        p.draw()

        # Customise text
#Soti lumitext        histograms.addStandardTexts(lumi=intLumi)
        # histograms.addText(0.17, 0.95, plots._legendLabels[kwargs.get("refDataset")], 22)
        histograms.addText(0.17, 0.88, plots._legendLabels[kwargs.get("refDataset")], 17)
        
        # Save canvas under custom dir
        save_path = savePath #+ opts.MVAcut Soti
        SaveAs(p, save_path, saveName, kwargs.get("saveFormats"), counter==0)
#        SaveAs(p, savePath, saveName, kwargs.get("saveFormats"), counter==0)

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

#    parser.add_option("--MVAcut", dest="MVAcut", type="string", default = "MVACUT", action = "store",
#                      help="Save plots to directory in respect of the MVA cut value [default: %s]")

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


#        args = {
#            "xlabel": "x",
#            "ylabel": "y",
#            "zlabel": "z",
#            "xlabelsize": None,
#            "ylabelsize": None,
#            "zhisto": None,
#            "log": False,
#            "ratio": False,
#            "ratioYlabel": None, 
#            "ratioInvert": False,
#            "ratioType": None,
#            #"ratioErrorOptions": 
#            "ratioCreateLegend": True,
#            #"ratioMoveLegend":
#            #"opts":
#            #"optsLog":
#            #"opts2":
#            #"canvasOpts":
#            "backgroundColor": ROOT.kRed,
#            "rebin": 1,
#            "rebinX": 1,
#            "rebinY": 1,
#            "rebinToWidthX": None,
#            "rebinToWidthY": None,
#            "divideByBinWidth": None,
#            "errorBarsX": True,
#            "createLegend": None,
#            #"moveLegend": 
#            #"customizeBeforeFrame":
#            #"customizeBeforeDraw":
#            #"customizeBeforeSave":
#            #"addLuminosityText":
#            "stackMCHistograms": True,
#            "addMCUncertainty": True,
#            "cmsText": True,
#            "cmsExtraText": True,
#            "addCmsText": True,
#            "cmsTextPosition": None,
#            "cmsExtraTextPosition": None,
#        }
#        
#        p.setDrawOptions(**args)
