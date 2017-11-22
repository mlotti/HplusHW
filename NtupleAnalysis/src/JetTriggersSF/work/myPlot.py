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

#from PythonWriter import PythonWriter
from plotAux import *

# ===========================================================
#   Variable Definition
# ===========================================================
# Run on:
xVariables    = ["pt6thJet", "Ht"]#, "nBTagJets", "pu"]
reHLT_samples = "JetHT|TT_ext3"

kwargs = {
    "verbose"          : False,
    "dataEra"          : "Run2016",#None,
    "searchMode"       : "80to1000",#None,
    "analysis"         : "JetTriggersSF",
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
    "addLuminosityText": True,
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

#pythonWriter = PythonWriter()

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
    Print(msg, printHeader)
    return


def GetLumi(datasetsMgr):
    Verbose("Determininig Integrated Luminosity")

    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True )
    return lumi

###ATHER
def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return


def GetDatasetsFromDir(mcrab, opts, **kwargs):

    HasKeys(["dataEra", "searchMode", "analysis", "optMode"], **kwargs)
    dataEra    = kwargs.get("dataEra")
    searchMode = kwargs.get("searchMode")
    analysis   = kwargs.get("analysis")
    optMode    = kwargs.get("optMode")

    if opts.includeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, includeOnlyTasks=opts.includeTasks, optimizationMode=optMode)
    elif opts.excludeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, excludeTasks=opts.excludeTasks, optimizationMode=optMode)

    else:
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)

    # Inform user of datasets retrieved                                                                                                        
    Verbose("Got the following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        Verbose( "\t", d.getName(), False)
    return datasets

###ATHER


def main(opts):
    
    global RunEra
    mcrabName = opts.mcrab
    print("mcrabNAME ISSSSSS     ", mcrabName)
    RunEra = mcrabName.split("_")[1]
    
    print "    Run Era is: ", RunEra
    print "    Plotting efficiency for trigger:", kwargs.get("trigger")
    #print "    Running on samples:", reHLT_samples
    #ext = "ReHLT"

    # Setup the style
    style = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)
    
    # Setup & configure the dataset manager
    #datasetsMgr   = GetSpecificDatasetsFromDir(opts.mcrab, opts, RunEra, reHLT_samples, **kwargs)
    datasetsMgr   = GetDatasetsFromDir(opts.mcrab, opts, **kwargs) 

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
    #print "runRange" , runRange

    datasetsMgr.PrintLuminosities() 
    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"      
    #plots.mergeRenameReorderForDataMC(datasetsMgr) #WARNING: Merged MC histograms must be normalized to something!     

    #dataset_MC.normalizeMCByLuminosity()

    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities() 

    plots.mergeRenameReorderForDataMC(datasetsMgr)

    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities()

    dataset_Data = datasetsMgr.getDataDatasets()
    
    datasetsMgr.mergeMC() #ATHER

    dataset_MC   = None
    dataset_MC   = datasetsMgr.getMCDatasets()

    #datasetsMgr.normalizeMCByLuminosity()

    #datasetsMgr.mergeMC()

    datasetsMgr.PrintCrossSections()
    datasetsMgr.PrintLuminosities()

    

    lumi = 0.0
    for d in datasetsMgr.getDataDatasets():
        lumi += d.getLuminosity()


        
    '''
    WrappedTH1* hDen_pT_Turnon_NoRef;
    WrappedTH1* hDen_HT_Turnon_NoRef;
    
    WrappedTH1* hNum_pT_Turnon_NoRef_PFHT300;
    WrappedTH1* hNum_HT_Turnon_NoRef_PFHT300;
    
    WrappedTH1* hNum_pT_Turnon_NoRef_PFHT350;
    WrappedTH1* hNum_HT_Turnon_NoRef_PFHT350;
    
    WrappedTH1* hNum_pT_Turnon_NoRef_PFHT400;
    WrappedTH1* hNum_HT_Turnon_NoRef_PFHT400;
    '''
    NewVar       = ["HT","pT"]      
    #NoRef
    NoRef = ["300", "350", "400"]
    for v in NewVar:
        for t in NoRef:
            print t
            num_name = "hNum_"+v+"_Turnon_NoRef_PFHT"+t
            den_name = "hDen_"+v+"_Turnon_NoRef"
            # Get the save path and name                                                 
            plotName = "Eff_"+v+"_Turnon_NoRef_PFHT"+t
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)

            # Get Efficiency Plots                                                       
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name ,**kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs)

            #if eff_Data == None or eff_MC == None:                                      
            #    continue                                                                

            if v == "pT":
                xMin = 29.0
                xMax = 125.0
            elif v == "HT":
                xMin = 100
                xMax = 2000

            # Apply Styles                                                               
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)

            # Marker Style                                                               
            eff_Data.SetMarkerSize(1)

            # Create Comparison Plot                                                     
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))

            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.3, "ymax": 1.7}
            moveLegend = {"dx": -0.24, "dy": -0.57, "dh": -0.2 }

            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")                                      
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)

            # Set Legend                                                                 
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

            # Set Log & Grid                                                             
            SetLogAndGrid(p, **kwargs)

            # Set Titles                                                                 
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            if v == "pT":
                p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            elif v == "HT":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")



            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)

            # Draw                                                                       
            #            p.finish()                                                      
            #plots.finish(p)                                                             
            #p.addLuminosityText()                                                       
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)                         
            histograms.addText(0.70, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.70, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()

            # Save the canvas to a file                                                  
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)

    '''
    WrappedTH1* hDen_pT_Turnon_PFHT400Ref;
    WrappedTH1* hDen_HT_Turnon_PFHT400Ref;
    WrappedTH1* hNum_pT_Turnon_PFHT400Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_HT_Turnon_PFHT400Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_pT_Turnon_PFHT400Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;
    WrappedTH1* hNum_HT_Turnon_PFHT400Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;


    '''
    

    #Ref1 = ["300","350","400"]
#    NewVar       = ["HT"] #"pT"
    NewSig400Ref = ["PFHT400_SixJet30","PFHT400_SixJet30_DoubleBTagCSV_p056"]
    
    for t in NewSig400Ref:
        for v in NewVar:
            
            print t
            num_name = "hNum_"+v+"_Turnon_PFHT400Ref_"+t
            den_name = "hDen_"+v+"_Turnon_PFHT400Ref"
            # Get the save path and name        
            plotName = "Eff_"+v+"_Turnon_PFHT400Ref_"+t
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            
            #if eff_Data == None or eff_MC == None:
            #    continue

            if v == "pT":
                xMin = 29.0
                xMax = 125.0
            elif v == "HT":
                xMin = 100
                xMax = 2000
        
            # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
            
            # Marker Style
            eff_Data.SetMarkerSize(1)
            
            # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
            
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.3, "ymax": 1.7}
            moveLegend = {"dx": -0.24, "dy": -0.57, "dh": -0.2 }
            
            
            
            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
            
            # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            
            # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
            
            # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            if v == "pT":
                p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            elif v == "HT":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")


            
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
            # Draw
            #            p.finish()
            #plots.finish(p)
            #p.addLuminosityText() 
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.70, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.70, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
            
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)


    '''
    WrappedTH1* hDen_pT_Turnon_PFHT300Ref;
    WrappedTH1* hDen_HT_Turnon_PFHT300Ref;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT350;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT350;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT400;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT400;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT475;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT475;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT450_SixJet40;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT450_SixJet40;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT450_SixJet40_BTagCSV_p056;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT450_SixJet40_BTagCSV_p056;
    WrappedTH1* hNum_pT_Turnon_PFHT300Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;
    WrappedTH1* hNum_HT_Turnon_PFHT300Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;

    '''

    #########

    NewSig400Ref = ["PFHT350","PFHT400","PFHT475","PFHT400_SixJet30","PFHT450_SixJet40","PFHT400_SixJet30_DoubleBTagCSV_p056","PFHT450_SixJet40_BTagCSV_p056"]
    
    for t in NewSig400Ref:
        for v in NewVar:
            
            print t
            num_name = "hNum_"+v+"_Turnon_PFHT300Ref_"+t
            den_name = "hDen_"+v+"_Turnon_PFHT300Ref"
            # Get the save path and name        
            plotName = "Eff_"+v+"_Turnon_PFHT300Ref_"+t
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            
            #if eff_Data == None or eff_MC == None:
            #    continue

            if v == "pT":
                xMin = 29.0
                xMax = 125.0
            elif v == "HT":
                xMin = 100
                xMax = 2000
        
            # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
            
            # Marker Style
            eff_Data.SetMarkerSize(1)
            
            # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
            
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.3, "ymax": 1.7}
            moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
            
            
            
            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
            
            # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            
            # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
            
            # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            if v == "pT":
                p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            elif v == "HT":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")


            
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
            # Draw
            #            p.finish()
            #plots.finish(p)
            #p.addLuminosityText() 
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
            
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)



    '''
    WrappedTH1* hDen_pT_Turnon_PFHT350Ref;
    WrappedTH1* hDen_HT_Turnon_PFHT350Ref;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT400;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT400;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT475;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT475;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT400_SixJet30;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT450_SixJet40;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT450_SixJet40;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT450_SixJet40_BTagCSV_p056;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT450_SixJet40_BTagCSV_p056;
    WrappedTH1* hNum_pT_Turnon_PFHT350Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;
    WrappedTH1* hNum_HT_Turnon_PFHT350Ref_PFHT400_SixJet30_DoubleBTagCSV_p056;

    '''

    NewSig400Ref = ["PFHT400","PFHT475","PFHT400_SixJet30","PFHT450_SixJet40","PFHT400_SixJet30_DoubleBTagCSV_p056","PFHT450_SixJet40_BTagCSV_p056"]
    
    for t in NewSig400Ref:
        for v in NewVar:
            
            print t
            num_name = "hNum_"+v+"_Turnon_PFHT350Ref_"+t
            den_name = "hDen_"+v+"_Turnon_PFHT350Ref"
            # Get the save path and name        
            plotName = "Eff_"+v+"_Turnon_PFHT350Ref_"+t
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            
            #if eff_Data == None or eff_MC == None:
            #    continue

            if v == "pT":
                xMin = 29.0
                xMax = 125.0
            elif v == "HT":
                xMin = 100
                xMax = 2000
        
            # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
            
            # Marker Style
            eff_Data.SetMarkerSize(1)
            
            # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
            
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.3, "ymax": 1.7}
            moveLegend = {"dx": -0.04, "dy": -0.57, "dh": -0.2 }
            
            
            
            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
            
            # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            
            # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
            
            # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            if v == "pT":
                p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            elif v == "HT":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")


            
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
            
            # Draw
            #            p.finish()
            #plots.finish(p)
            #p.addLuminosityText() 
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.70, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.70, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
            
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
    
    

    ####NewHistos
    #WrappedTH1* hDen_Ht_Turnon_IsoMu24Ref;
    #WrappedTH1* hNum_Ht_Turnon_IsoMu24Ref_PFHT300;
    #WrappedTH1* hNum_Ht_Turnon_IsoMu24Ref_PFHT350;
    #WrappedTH1* hNum_Ht_Turnon_IsoMu24Ref_PFHT400;
    #WrappedTH1* hNum_Ht_Turnon_IsoMu24Ref_PFHT450;
    #WrappedTH1* hNum_Ht_Turnon_IsoMu24Ref_PFHT475;







    '''
    TrgThresh = ["300","350","400","475"]
    
    for t in TrgThresh:
        print t
        num_name = "hNum_Ht_Turnon_IsoMu24Ref_PFHT"+t
        den_name = "hDen_Ht_Turnon_IsoMu24Ref"
        # Get the save path and name        
        plotName = "Eff_turnon_"+t+"_Trg"
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
        # Get Efficiency Plots
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
        
        #if eff_Data == None or eff_MC == None:
        #    continue
        
        xMin = 100
        xMax = 2000
                
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
        
        # Marker Style
        eff_Data.SetMarkerSize(1)
        
        # Create Comparison Plot
        p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                 histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.3, "ymax": 1.7}
        moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
   


        p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
        createRatio = True #kwargs.get("ratio")
        p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
        
        # Set Legend
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
        SetLogAndGrid(p, **kwargs)
        
        # Set Titles
        p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")
                    
        if createRatio:
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
        # Draw
        #            p.finish()
        #plots.finish(p)
        #p.addLuminosityText() 
        #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
        histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
        histograms.addText(0.30, 0.15, "2016", 17)
        histograms.addStandardTexts(lumi=lumi)
        p.draw()
        
        # Save the canvas to a file
        SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        
        ####ATHER .... below this are ususal eff plots
        '''    

    
    SigSel = ["1BTag","2BTag" ,"OR"]
    #SigSel = ["OR"]
    for s in SigSel:
        for xVar in xVariables:
            print s , xVar
#for den,num
            num_name = "hNum_"+xVar+"_CtrlTrg_HLT_PFHT350_Signal"+s
            den_name = "hDen_"+xVar+"_CtrlTrg_HLT_PFHT350"
        # Get the save path and name        
            plotName = "Eff"+"_"+xVar+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
    
        # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 

            #if eff_Data == None or eff_MC == None:
            #    continue
    

#eff_Data     = getEfficiency(datasetsMgr, dataset_Data, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)
        #eff_MC       = getEfficiency(datasetsMgr, dataset_MC, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)

    #eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   numerator_names.get(xVar), denominator_names.get(xVar), **kwargs)
        
            if xVar == "pt6thJet":
                xMin = 29.0
                xMax = 125.0
            elif xVar == "Ht":
                xMin = 450
                xMax = 2000
            elif xVar == "nBTagJets":
                xMin = 0
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
                
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.7, "ymax": 1.3}
            if xVar == "pu":
                moveLegend = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }
            else:
                moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
   

            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
                    
        # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
    
        # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            if xVar == "pt6thJet":
                p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            elif xVar == "Ht":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")
            elif xVar == "nBTagJets":
                p.getFrame().GetXaxis().SetTitle("nB-Jet")
            elif xVar == "pu":
                p.getFrame().GetXaxis().SetTitle("nPU")
                    
                    
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)

            
            #if xVar == "pt6thJet" and s == "OR":
               #plist = [0.8, 0.978, 0.99, 0.4, 48.0]
               #Fit_Richards(40.0, 120.0, p, eff_Data, plist)
               #plist = [0.00005, 0.988, 0.000000109, 0.15, 29.0]
               #Fit_Richards(40.0, 120.0, p, eff_MC, plist)
            #elif xVar == "Ht" and s == "OR":
                #plist = [0.0003, 0.94, 0.45, 0.45, 43.0]
                #Fit_Richards(500.0, 2000.0, p, eff_Data, plist)
                #plist = [0.0003, 0.97, 0.45, 0.24, 43.0]
                #Fit_Richards(500.0, 2000.0, p, eff_MC, plist)
            #elif xVar == "nBTagJets":
                #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
                #Fit_Richards(30.0, 120.0, p, eff_Data, plist)
            #elif xVar == "pu":
                #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
                #Fit_Richards(30.0, 120.0, p, eff_Data, plist)
                
                            
        # Draw
        #            p.finish()
            #plots.finish(p)
            #p.addLuminosityText() 
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
            
    # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        
    '''

    for s in SigSel:
        num_name = "hNum_nBTagJets_CtrlTrg_HLT_PFHT350_Signal"+s+"_NoBSelection"
        den_name = "hDen_nBTagJets_CtrlTrg_HLT_PFHT350_NoBSelection"

                # Get the save path and name        
        plotName = "Eff"+"_nBTagJets_"+s+"_NoBSelection"
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
    
        # Get Efficiency Plots
        eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
        eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
        
        xMin = 0
        xMax = 10
        
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
        
        # Marker Style
        eff_Data.SetMarkerSize(1)
                
        # Create Comparison Plot
        p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                 histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
        opts2      = {"ymin": 0.3, "ymax": 1.7}

        moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
   

        p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
        createRatio = True #kwargs.get("ratio")
        p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
                    
        # Set Legend
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
        SetLogAndGrid(p, **kwargs)
        
        # Set Titles
        p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
        p.getFrame().GetXaxis().SetTitle("nB-Jet")
            
        if createRatio:
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
            # Draw
            #            p.finish()
            #plots.finish(p)
            #p.addLuminosityText() 
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
        histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
        histograms.addText(0.30, 0.15, "2016", 17)
        histograms.addStandardTexts(lumi=lumi)
        p.draw()
        
        # Save the canvas to a file
        SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        '''



        

    '''
    #THis is addition of new histos for BTAG
    WithB   = ["","_NoBSelection"]
    VARI    = ["Pt","CSV"]
    EffType = ["PFHT450_1btagEff","PFHT400_2btagEff"]
    for v in VARI:
        for t in EffType:
            for b in WithB:
                num_name = "hNum_"+t+"_"+v+b
                den_name = "hDen_"+t+"_"+v+b
                #num_name = "hNum_PFHT450_1btagEff_CSV"   
                #den_name = "hDen_PFHT450_1btagEff_CSV"
                plotName = "Eff"+"_"+t+"_"+v+b
                #plotName = "EffTEST"
                savePath, saveName = GetSavePathAndName(plotName, **kwargs)
                # Get Efficiency Plots                                       
                eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
                eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs)

                if v == "CSV":
                    xMin = 0.0
                    xMax = 1.0 
                elif v == "Pt":    
                    xMin = 29.0
                    xMax = 125.0
                    # Apply Styles                              
                styles.dataStyle.apply(eff_Data)
                styles.mcStyle.apply(eff_MC)

                # Marker Style                                                                     
                eff_Data.SetMarkerSize(1)
                # Create Comparison Plot                                              
                p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                         histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))

                opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
                opts2      = {"ymin": 0.3, "ymax": 1.7}
                #if xVar == "pu":
                #    moveLegend = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }
                #else:
                moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
                p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
                createRatio = True #kwargs.get("ratio")          
                p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
                # Set Legend                                                    
                p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
                # Set Log & Grid                                         
                SetLogAndGrid(p, **kwargs)
                # Set Titles              
                p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
                if v == "CSV":
                    p.getFrame().GetXaxis().SetTitle("CSV")
                elif v == "Pt":
                    p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
          
            

                if createRatio:
                    p.getFrame2().GetYaxis().SetTitle("Ratio")
                    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

                # Draw                                                                                                        
                #            p.finish()                                                                                               
                #plots.finish(p)                                                                                          
                #p.addLuminosityText()                                                                                    
                #histograms.addText(0.30, 0.06,  "Trigger Name", 17)                                                      
                histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
                histograms.addText(0.30, 0.15, "2016", 17)
                histograms.addStandardTexts(lumi=lumi)
                p.draw()

                # Save the canvas to a file                                                                                   
                SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)

                '''
    
    '''
    # IN SLICES OF HT
    HTSlices = ["450ht600","600ht800","800ht1000", "1000ht1250", "1250ht1500", "1500ht2000"]
    for s in SigSel:
        for hsl in HTSlices:
            #den_name = "Den_pt6thJet_Vs_450ht600_HLT_PFHT300"
            #num_name = "Num_pt6thJet_Vs_450ht600_HLT_PFHT300_1BTag"
            num_name = "Num_pt6thJet_Vs_"+hsl+"_HLT_PFHT350_"+s
            den_name = "Den_pt6thJet_Vs_"+hsl+"_HLT_PFHT350"
            # Get the save path and name        
            plotName = "Eff_pt6thJet_Vs_"+hsl+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            #if eff_Data == None or eff_MC == None:
            #    continue

            #eff_Data     = getEfficiency(datasetsMgr, dataset_Data, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)
            #eff_MC       = getEfficiency(datasetsMgr, dataset_MC, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)
            
            #eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   numerator_names.get(xVar), denominator_names.get(xVar), **kwargs)
        
            #if xVar == "pt6thJet":
            xMin = 29.0
            xMax = 125.0
            #elif xVar == "Ht":
            #    xMin = 450
            #    xMax = 2000
            #elif xVar == "nBTagJets":
            #    xMin = 2
            #    xMax = 10
            #elif xVar == "pu":
            #    xMin= 0
            #    xMax= 50
                
        # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
        
        # Marker Style
            eff_Data.SetMarkerSize(1)
                
        # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
                
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.7, "ymax": 1.3}
            #if xVar == "pu":
            #    moveLegend = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }
            #else:
            moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
            
            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
                    
        # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
    
        # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            #if xVar == "pt6thJet":
            p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
            #elif xVar == "Ht":
             #   p.getFrame().GetXaxis().SetTitle("H_T (Gev/c)")
            #elif xVar == "nBTagJets":
            #    p.getFrame().GetXaxis().SetTitle("nB-Jet")
            #elif xVar == "pu":
            #    p.getFrame().GetXaxis().SetTitle("nPU")
                    
                    
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
                # Draw
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
        
        # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)

    
    PTSlices = ["40pt50","50pt60", "60pt70", "70pt90", "90pt120"]
    for s in SigSel:
        for psl in PTSlices:
            #den_name = "Den_pt6thJet_Vs_450ht600_HLT_PFHT300"
            #num_name = "Num_pt6thJet_Vs_450ht600_HLT_PFHT300_1BTag"
            num_name = "Num_ht_Vs_"+psl+"_HLT_PFHT350_"+s
            den_name = "Den_ht_Vs_"+psl+"_HLT_PFHT350"
            # Get the save path and name        
            plotName = "Eff_ht_Vs_"+psl+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            #if eff_Data == None or eff_MC == None:
            #    continue

            #eff_Data     = getEfficiency(datasetsMgr, dataset_Data, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)
            #eff_MC       = getEfficiency(datasetsMgr, dataset_MC, "hNum_pt6thJet_CtrlTrg_HLT_PFHT300_Signal1BTag", "hDen_pt6thJet_CtrlTrg_HLT_PFHT300", **kwargs)
            
            #eff_MC       = getEfficiency(datasetsMgr, dataset_MC,   numerator_names.get(xVar), denominator_names.get(xVar), **kwargs)
        
            #if xVar == "pt6thJet":
            #xMin = 29.0
            #xMax = 125.0
            #elif xVar == "Ht":
            xMin = 450
            xMax = 2000
            #elif xVar == "nBTagJets":
            #    xMin = 2
            #    xMax = 10
            #elif xVar == "pu":
            #    xMin= 0
            #    xMax= 50
                
        # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
        
        # Marker Style
            eff_Data.SetMarkerSize(1)
                
        # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
                
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xMax":xMax}
            opts2      = {"ymin": 0.7, "ymax": 1.3}
            #if xVar == "pu":
            #    moveLegend = {"dx": -0.44, "dy": -0.62, "dh": -0.2 }
            #else:
            moveLegend = {"dx": -0.44, "dy": -0.57, "dh": -0.2 }
                
            p.histoMgr.setHistoLegendLabelMany({"eff_Data": "Data", "eff_MC": "Simulation"})
            createRatio = True #kwargs.get("ratio")
            #if eff_Data != None and eff_MC != None:
            p.createFrame(saveName, createRatio=createRatio, opts=opts, opts2=opts2)
                    
        # Set Legend
            p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        
        # Set Log & Grid
            SetLogAndGrid(p, **kwargs)
    
        # Set Titles
            p.getFrame().GetYaxis().SetTitle(kwargs.get("ylabel"))
            #if xVar == "pt6thJet":
            #p.getFrame().GetXaxis().SetTitle("p_T (Gev/c)")
            #elif xVar == "Ht":
            p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")
            #elif xVar == "nBTagJets":
            #    p.getFrame().GetXaxis().SetTitle("nB-Jet")
            #elif xVar == "pu":
            #    p.getFrame().GetXaxis().SetTitle("nPU")
                    
                    
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
            # Draw
            #histograms.addText(0.30, 0.06,  "Trigger Name", 17)
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
        
        # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
            '''
    '''
    #2DPlots
    for s in SigSel:
        
        hNumName = "h_Num_ht_Vs_pt6thJet_CtrlTrg_HLT_PFHT350_"+s
        hDenName = "h_Den_ht_Vs_pt6thJet_CtrlTrg_HLT_PFHT350"

        plotName = "2DEff_ht_VS_pt"+s
        savePath, saveName = GetSavePathAndName(plotName, **kwargs)
       
 
        eff_Data     = getEfficiency2D(datasetsMgr, dataset_Data, hNumName, hDenName, **kwargs)
        eff_MC       = getEfficiency2D(datasetsMgr, dataset_MC,   hNumName, hDenName, **kwargs)
        

#        SF_hist = plots._createRatio(eff_Data, eff_MC, "Scale_Factors")
        
#        p0 = plots.PlotBase([histograms.HistoGraph(SF_hist, "Scale_Factors","p","P")])
 #       p0.createFrame(saveName, opts=opts2)
 #       p0.getFrame().GetYaxis().SetTitle("Scale Factor")
 #       p0.getFrame().GetXaxis().SetTitle("p_{T}^{6th} Jet (GeVc^{-1})")
        
 #       #p0.getPad().SetGridx(kwargs.get("gridX"))
 #       #p0.getPad().SetGridy(kwargs.get("gridY"))
        
 #       histograms.addText(0.35, 0.18, kwargs.get("trigger"), 17)
 #       histograms.addText(0.35, 0.30, ht_min+" < H_{T} < "+ht_max,17)
 #       histograms.addText(0.35, 0.26, "2016", 17)
 #       histograms.addText(0.35, 0.22, "Runs "+runRange, 17)
 #       histograms.addStandardTexts(lumi=lumi)

 #       p0.draw()
        
 #       p0.getFrame().GetXaxis().SetRangeUser(30, 120.0)
 #       SaveAs(p0, kwargs.get("savePath"), saveName+"_SF", kwargs.get("saveFormats"), True)
        
        # ---------------------------------------------------------------
        # Apply Styles
        styles.dataStyle.apply(eff_Data)
        styles.mcStyle.apply(eff_MC)
        
        # Marker Style
        eff_Data.SetMarkerSize(1)


        # Create Comparison Plot
        p1 = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                  histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
        
        opts       = {"ymin": 0  , "ymax": 120.0, "xmin":xMin, "xMax":xMax}
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
        #createRatio = kwargs.get("ratio")
        p1.createFrame(saveName)

        

        # Set Legend
        p1.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        p1.removeLegend()
        
        # Set Titles
        #p1.getFrame().GetYaxis().SetTitle("H_{T} (GeVc^{-1})")
        p1.getFrame().GetXaxis().SetTitle("p_{T}^{6th Jet} (GeVc^{-1})")
        
        
        #if createRatio:
        #    p1.getFrame2().GetYaxis().SetTitle("Ratio")
        #    p1.getFrame2().GetYaxis().SetTitleOffset(1.6)
        
        # Additional text
  #      histograms.addText(0.35, 0.10, kwargs.get("trigger"), 17)
   #     histograms.addText(0.35, 0.36, ht_min+" < H_{T} < "+ht_max,17)
        histograms.addText(0.35, 0.20, "2016", 17)
        histograms.addText(0.35, 0.15, "Runs "+runRange, 17)
        histograms.addStandardTexts(lumi=lumi)
        
#        SetLogAndGrid(p1, **kwargs)
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        p1.draw()
        
        # Save the canvas to a file
        SaveAs(p1, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), counter==0)

       
        ''' 
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
