#!/usr/bin/env python
'''
  Usage:
  
  ./plotJetTriggersEfficiency.py -m <multicrab directory> 
  
'''
# ======================================================
#   Imports
# ======================================================
import os
import sys
import ROOT
import array

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

from optparse import OptionParser
import getpass
import socket

from PythonWriter import PythonWriter
from plotAux import *

# ===========================================================
#   Variable Definition
# ===========================================================
# Run on:
xVariables    = ["pt6thJet", "ht", "nBTagJets", "pu"]
reHLT_samples = "JetHT|TT_ext3"

kwargs = {
    "verbose"          : False,
    "dataEra"          : None,
    "searchMode"       : None,
    "analysis"         : "JetTriggers",
    "trigger"          : "HLT_PFHT450_SixJet40_BTagCSV_p056", #"HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",  # 
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf"],
    "xlabel"           : None, 
    "ylabel"           : "HLT Efficiency",
    "rebinX"           : 1,
    "rebinY"           : 1,
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
    "cmsExtraText"     : "Preliminary", # "Simulation" 
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": +0.0, "dh": +0.1},
    "cutValue"         : None, 
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
    }

pythonWriter = PythonWriter()

# Lumis must be read from the JSON file!!
#lumis={ "JetHT_Run2016B_23Sep2016_v3_273150_275376": 5886.295, 
#        "JetHT_Run2016C_23Sep2016_v1_275420_276283": 2645.968, 
#        "JetHT_Run2016D_23Sep2016_v1_276315_276811": 4353.449, 
#        "JetHT_Run2016E_23Sep2016_v1_276824_277420": 4049.255, 
#        "JetHT_Run2016F_23Sep2016_v1_277816_278800": 2749.622, 
#        "JetHT_Run2016F_23Sep2016_v1_278801_278808": 410.467, 
#        "JetHT_Run2016G_23Sep2016_v1_278816_280385": 7115.786, 
#        "JetHT_Run2016H_PromptReco_v2_281207_284035": 8545.04, 
#        "JetHT_Run2016H_PromptReco_v3_271036_284044": 216.783
#        }

# =====================================================================
#   Main
# =====================================================================
def main(opts):
    
    global RunEra
    mcrabName = opts.mcrab
    RunEra = mcrabName.split("_")[1]
    
    print "    Run Era is: ", RunEra
    print "    Plotting efficiency for trigger:", kwargs.get("trigger")
    print "    Running on samples:", reHLT_samples
    ext = "ReHLT"

    # Setup the style
    style = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)
    
    # Setup & configure the dataset manager
    datasetsMgr   = GetSpecificDatasetsFromDir(opts.mcrab, opts, RunEra, reHLT_samples, **kwargs)
    
    minRunRange = None
    maxRunRange = None
    
    Counter = 0
    nDataDatasets = len(datasetsMgr.getDataDatasets())

    for d in datasetsMgr.getDataDatasets():
        Counter = Counter + 1
        if Counter == 1:
            minRunRange = d.getName().split("_")[-2]
        if Counter == nDataDatasets:
            maxRunRange = d.getName().split("_")[-1]
        print "Data Name==> ", d.getName()
        print "RunRange ==> ", d.getName().split("_")[-2], " - ", d.getName().split("_")[-1]
        #Lumi = lumis.get(d.getName())
    #    print d.getName(), " Lumi=", Lumi
    
        #intLumi = GetLumi(datasetsMgr)
        #d.setLuminosity(Lumi)
    
    print "Run Range = ", minRunRange, "     -      ", maxRunRange
    runRange = minRunRange+" - "+maxRunRange
    intLumi = GetLumi(datasetsMgr)
    print "intLumi=",intLumi

    # Update to PU 
    datasetsMgr.updateNAllEventsToPUWeighted()
    
    # Load Luminosities
    datasetsMgr.loadLuminosities()

    # Load Run Range
#    runRange  = datasetsMgr.loadRunRange()
    print "runRange" , runRange

    datasetsMgr.PrintLuminosities() 
    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"      
    #plots.mergeRenameReorderForDataMC(datasetsMgr) #WARNING: Merged MC histograms must be normalized to something!     
    
    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities() 
    
    dataset_Data = datasetsMgr.getDataDatasets()
    dataset_MC   = None
    dataset_MC   = datasetsMgr.getMCDatasets()
    
    lumi = 0.0
    for d in datasetsMgr.getDataDatasets():
        lumi += d.getLuminosity()
        
    for xVar in xVariables:
        
        # Get the save path and name        
        plotName = "Run"+RunEra+"_"+xVar+"_"+ext+"_"+trg.get(kwargs.get("trigger"))
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
    
        # Get Efficiency Plots
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, numerator_names.get(xVar), denominator_names.get(xVar), **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   numerator_names.get(xVar), denominator_names.get(xVar), **kwargs)
    
        if xVar == "pt6thJet":
            xMin = 29.0
            xMax = 125.0
        elif xVar == "ht":
            xMin = 450
            xMax = 2000
        elif xVar == "nBTagJets":
            xMin = 2
            xMax = 10
        elif xVar == "pu":
            xMin= 0
            xMax= 50
        
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
    
        # Marker Style
        eff_Data.SetMarkerSize(1)
                        
        # Create Comparison Plot
        p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                 histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))

        # -----------------------------------------------------------
        # Fitting Data:
        # ------------------------------------------------------------
        if xVar == "pt6thJet":
            plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        elif xVar == "ht":
            plist = [0.0, 0.63, 0.45, 0.24, 400.0]
        else:
            plist = []
        # x - Range, frame, Efficiency plot, Parameter List 
        print "xVar=",xVar
        print " Fitting Data:"
        Fit_Richards(xMin, xMax, p, eff_Data, plist)
        # -----------------------------------------------------------
        # Fitting MC:
        # -----------------------------------------------------------
        if xVar == "pt6thJet":
            if "Double" in kwargs.get("trigger"):
                plist = [ 0.0, 0.906, 0.001, 0.005, 22]
            else:
                plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        elif xVar == "ht":
            plist = [0.0, 0.82, 0.45, 0.24, 400.0]
        else:
            plist = []
        
        # x - Range, frame, Efficiency plot, Parameter List 
        print " Fitting MC"    
        Fit_Richards(xMin, xMax, p, eff_MC, plist)
        
        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.4, "ymax": 1.6}
        if xVar == "pu":
            moveLegend = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }
        else:
            moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }

        p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
        createRatio = False #kwargs.get("ratio")
        p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
        
        # Set Legend
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
        SetLogAndGrid(p, **kwargs)

        # Set Titles
        p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        p.getFrame().GetXaxis().SetTitle(xTitles.get(xVar))
        
        if createRatio:
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        # Additional text
        if xVar == "pu":
            histograms.addText(0.30, 0.06, kwargs.get("trigger"), 17)
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
        else:
            histograms.addText(0.30, 0.10, kwargs.get("trigger"), 17)
            histograms.addText(0.30, 0.15, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.20, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
        
        # Draw
        p.draw()
        
        # Save the canvas to a file
        SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        
        # --------------------------------------------------------------------------------
        # Python Writer
        #pythonWriter.addParameters(kwargs.get("savePath"), "2016", runRange, lumi, eff_Data)
        #pythonWriter.addMCParameters("2016", eff_MC)
        #pythonWriter.writeJSON(os.path.join(kwargs.get("savePath"),"TriggerEfficiency_BTag_"+xVar+"2016"+".json"))
        
        

    # ------------------------------------------------------------------------------------
    #  Plotting pt of the 6th Jet for different numbers of reco vertices
    # ------------------------------------------------------------------------------------
    nvs = ["1nv10", "10nv20", "20nv30", "30nv40", "40nvInf"]
    
    for nv in nvs:
        
        hNumName = "Num_pt6thJet_"+nv
        hDenName = "Den_pt6thJet_"+nv
        
        plotName = "Run"+RunEra+"_pt_"+ext+"_"+trg.get(kwargs.get("trigger"))+"_"+nv
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
        # Get Efficiency Plots
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, hNumName, hDenName, **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   hNumName, hDenName, **kwargs)
    
        xMin = 30.0
        xMax = 120.0
        
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
    
        # Marker Style
        eff_Data.SetMarkerSize(1)
        
        # Create Comparison Plot
        z = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                 histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        # Fitting Data
        #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        #Fit_Richards(xMin, xMax, z, eff_Data, plist)
        # Fitting MC:
        #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        #Fit_Richards(xMin, xMax, z, eff_MC, plist)
                
        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.5, "ymax": 1.5}
        moveLegend = {"dx": -0.40, "dy": -0.57, "dh": -0.2}
                
        legend1 = "Data"
        legend2 = "Simulation"
        
        z.histoMgr.setHistoLegendLabelMany({"eff_Data": legend1, "eff_MC": legend2})
        createRatio = kwargs.get("ratio")
        z.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
        
        # Set Legend
        z.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Titles
        z.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        z.getFrame().GetXaxis().SetTitle("p_{T}^{6th Jet}")
        
        if createRatio:
            z.getFrame2().GetYaxis().SetTitle("Ratio")
            z.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
        # Additional text
        histograms.addText(0.35, 0.10, kwargs.get("trigger"), 17)
        histograms.addText(0.35, 0.40, nv, 17) 
        histograms.addText(0.35, 0.20, "2016", 17)
        histograms.addText(0.35, 0.15, "Runs "+runRange, 17)
        histograms.addStandardTexts(lumi=lumi)

        #SetLogAndGrid(z, **kwargs)
        
        z.draw()
              
        xmin = z.getFrame().GetXaxis().GetXmin()
        xmax = z.getFrame().GetXaxis().GetXmax()
        
        # Save the canvas to a file
        SaveAs(z, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        
    # New Plots 2D:
    
    ht_low = ["450", "600", "800","1000","1250", "1500"]
    ht_up  = ["600", "800","1000","1250","1500","2000"]

    for i, HT in enumerate(ht_low):
        print i, HT, ht_up[i]

        ht_min = HT
        ht_max = ht_up[i]
        
        #if ht_min == "600" and ht_max == "800":
        #    continue
        hNumName = "Num_pt6thJet_Vs_"+ht_min+"ht"+ht_max
        hDenName = "Den_pt6thJet_Vs_"+ht_min+"ht"+ht_max

        plotName = "Run"+RunEra+"_pt_Vs_"+ht_min+"ht"+ht_max+"_"+ext+"_"+trg.get(kwargs.get("trigger"))
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, hNumName, hDenName, **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   hNumName, hDenName, **kwargs)
        

        SF_hist = plots._createRatio(eff_Data, eff_MC, "Scale_Factors")
        
        p0 = plots.PlotBase([histograms.HistoGraph(SF_hist, "Scale_Factors","p","P")])
        p0.createFrame(saveName, opts=opts2)
        p0.getFrame().GetYaxis().SetTitle("Scale Factor")
        p0.getFrame().GetXaxis().SetTitle("p_{T}^{6th} Jet (GeVc^{-1})")
        
        #p0.getPad().SetGridx(kwargs.get("gridX"))
        #p0.getPad().SetGridy(kwargs.get("gridY"))
        
        histograms.addText(0.35, 0.18, kwargs.get("trigger"), 17)
        histograms.addText(0.35, 0.30, ht_min+" < H_{T} < "+ht_max,17)
        histograms.addText(0.35, 0.26, "2016", 17)
        histograms.addText(0.35, 0.22, "Runs "+runRange, 17)
        histograms.addStandardTexts(lumi=lumi)

        p0.draw()
        
        p0.getFrame().GetXaxis().SetRangeUser(30, 120.0)
        SaveAs(p0, kwargs.get("savePath"), saveName+"_SF", kwargs.get("saveFormats"), True)
        
        # ---------------------------------------------------------------
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
        
        # Marker Style
        eff_Data.SetMarkerSize(1)
        

        # Create Comparison Plot
        p1 = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                  histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.5, "ymax": 1.5}
        moveLegend = {"dx": -0.40, "dy": -0.57, "dh": -0.2}
                
        legend1 = "Data"
        legend2 = "Simulation"
        
        #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        #Fit_Richards(30.0, 120.0, p1, eff_MC, plist)
        
        #if(ht_min != "1500"):
        #    plist = [0.07, 0.984, 0.45, 0.24, 43.0]
        #    Fit_Richards(30.0, 120.0, p1, eff_Data, plist)
            
            
        p1.histoMgr.setHistoLegendLabelMany({"eff_Data": legend1, "eff_MC": legend2})
        createRatio = kwargs.get("ratio")
        p1.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
        
        # Set Legend
        p1.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Titles
        p1.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        p1.getFrame().GetXaxis().SetTitle("p_{T}^{6th Jet} (GeVc^{-1})")
        
        if createRatio:
            p1.getFrame2().GetYaxis().SetTitle("Ratio")
            p1.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
        # Additional text
        histograms.addText(0.35, 0.10, kwargs.get("trigger"), 17)
        histograms.addText(0.35, 0.36, ht_min+" < H_{T} < "+ht_max,17)
        histograms.addText(0.35, 0.20, "2016", 17)
        histograms.addText(0.35, 0.15, "Runs "+runRange, 17)
        histograms.addStandardTexts(lumi=lumi)

        SetLogAndGrid(p1, **kwargs)
        
        p1.draw()
        
        # Save the canvas to a file
        SaveAs(p1, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        
        
        
    pt_low = ["30","40","50", "60", "70", "90"]
    pt_up  = ["40","50","60", "70", "90","120"]

    for i, PT in enumerate(pt_low):
        print i, PT, pt_up[i]

        pt_min = PT
        pt_max = pt_up[i]
        
        hNumName = "Num_ht_Vs_"+pt_min+"pt"+pt_max
        hDenName = "Den_ht_Vs_"+pt_min+"pt"+pt_max

        plotName = "Run"+RunEra+"_ht_Vs_"+pt_min+"pt"+pt_max+"_"+ext+"_"+trg.get(kwargs.get("trigger"))
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, hNumName, hDenName, **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   hNumName, hDenName, **kwargs)
        
        SF_hist = plots._createRatio(eff_Data, eff_MC, "Scale_Factors")
        
        p2 = plots.PlotBase([histograms.HistoGraph(SF_hist, "Scale_Factors","p","P")])
        p2.createFrame(saveName, opts=opts2)
        p2.getFrame().GetYaxis().SetTitle("Scale Factor")
        p2.getFrame().GetXaxis().SetTitle("H_{T} (GeVc^{-1})")
        
        #p2.getPad().SetGridx(kwargs.get("gridX"))
        #p2.getPad().SetGridy(kwargs.get("gridY"))
        
        histograms.addText(0.20, 0.88, pt_min+" < p_{T} < "+pt_max,17)
        histograms.addText(0.20, 0.84, "2016", 17)
        histograms.addText(0.20, 0.80, "Runs "+runRange, 17)
        histograms.addText(0.20, 0.76, kwargs.get("trigger"), 17)
        histograms.addStandardTexts(lumi=lumi)

        p2.draw()
        
        p2.getFrame().GetXaxis().SetRangeUser(30, 120.0)
        SaveAs(p2, kwargs.get("savePath"), saveName+"_SF", kwargs.get("saveFormats"), True)
        
        # =========================================================================== #
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
        
        # Marker Style
        eff_Data.SetMarkerSize(1)
        
        # Create Comparison Plot
        p3 = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                  histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        xMin= 450.0
        xMax= 2000.0

        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.5, "ymax": 1.5}
        
        if pt_min == "30":
            moveLegend = {"dx": -0.55, "dy": -0.20, "dh": -0.2}
        else:
            moveLegend = {"dx": -0.55, "dy": -0.57, "dh": -0.2}
            
        legend1 = "Data"
        legend2 = "Simulation"
        
        #plist = [0.0, 0.86, 0.45, 0.24, 400.0]
        #Fit_Richards(450.0, 2000.0, p3, eff_MC, plist)
        #plist = [0.0, 0.82, 0.45, 0.24, 400.0]
        #Fit_Richards(450.0, 2000.0, p3, eff_Data, plist)
        
            
        p3.histoMgr.setHistoLegendLabelMany({"eff_Data": legend1, "eff_MC": legend2})
        createRatio = kwargs.get("ratio")
        p3.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
        
        # Set Legend
        p3.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Titles
        p3.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        p3.getFrame().GetXaxis().SetTitle("H_{T} (GeVc^{-1})")
        
        if createRatio:
            p3.getFrame2().GetYaxis().SetTitle("Ratio")
            p3.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
        # Additional text
        
        if pt_min == "30":
            histograms.addText(0.20, 0.89, kwargs.get("trigger"), 17)
            histograms.addText(0.20, 0.83, pt_min+" < p_{T} < "+pt_max,17)
            histograms.addText(0.20, 0.79, "2016", 17)
            histograms.addText(0.20, 0.75, "Runs "+runRange, 17)
        else:
            histograms.addText(0.20, 0.05, kwargs.get("trigger"), 17)
            histograms.addText(0.20, 0.10, pt_min+" < p_{T} < "+pt_max,17)
            histograms.addText(0.20, 0.15, "Runs "+runRange, 17)
            histograms.addText(0.20, 0.20, "2016", 17)
        
        histograms.addStandardTexts(lumi=lumi)

        SetLogAndGrid(p3, **kwargs)
        
        p3.draw()
        
        # Save the canvas to a file
        SaveAs(p3, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)

 
    # Print the links for all the plots
    Print_html()
    
    print "\n"
    print " ========================= REMINDER ============================= "
    print "       Use the correct multicrab directory for each trigger       "
    print "       and change the trigger name in kwargs.                     "
    print " ================================================================ "
    print "\n"
   
    

    return



#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    
    parser.add_option("-m", "--mcrab", dest="mcrab", action="store",
                      help="Path to the multicrab directory for input")
    
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True,
                      help="Enables batch mode (canvas creation  NOT generates a window)")
    
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
