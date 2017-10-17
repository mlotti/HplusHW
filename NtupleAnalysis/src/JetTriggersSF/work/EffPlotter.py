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
xVariables    = ["pt6thJet", "eta6thJet", "phi6thJet", "Ht", "nBTagJets", "pu", "JetMulti", "BJetMulti"]
reHLT_samples = "JetHT|TT_ext3"

kwargs = {
    "verbose"          : False,
    "dataEra"          : "Run2016",#None,
    "searchMode"       : "80to1000",#None,
    "analysis"         : "JetTriggersSF",
    "trigger"          : "HLT_PFHT450_SixJet40_BTagCSV_p056", #"HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",  # 
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf",".png", ".eps", ".C"],
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


def main(opts):
    
    global RunEra
    mcrabName = opts.mcrab
    print("mcrabNAME ISSSSSS     ", mcrabName)
    RunEra = mcrabName.split("_")[1]
    
    print "    Run Era is: ", RunEra
    print "    Plotting efficiency for trigger:", kwargs.get("trigger")

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

    print "Run Range = ", minRunRange, "     -      ", maxRunRange
    

    runRange = minRunRange+" - "+maxRunRange
    intLumi = GetLumi(datasetsMgr)
    print "intLumi=",intLumi

    # Update to PU 
    datasetsMgr.updateNAllEventsToPUWeighted()
    
    # Load Luminosities
    datasetsMgr.loadLuminosities()

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


    SigSel = ["1BTag", "2BTag", "OR", "OR_PFJet450"]
    for s in SigSel:
        for xVar in xVariables:
            print s , xVar

            #if xVar == "pt6thJet":
            #    cutValue = 40
            #    cutLine = True



            #for den,num
            num_name = "hNum_"+xVar+"_RefTrg_OfflineSel_Signal"+s
            den_name = "hDen_"+xVar+"_RefTrg_OfflineSel"
        # Get the save path and name        
            plotName = "Eff"+"_"+xVar+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
    
        # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 

        
            if xVar == "pt6thJet":
                xMin = 29.0
                xMax = 125.0
            elif xVar == "eta6thJet":
                xMin = -2.5
                xMax = 2.5
            elif xVar == "phi6thJet":
                xMin = -3.2
                xMax = 3.2
            elif xVar == "Ht":
                xMin = 350
                xMax = 2000
            elif xVar == "nBTagJets":
                xMin = 0
                xMax = 10
            elif xVar == "pu":
                xMin= 0
                xMax= 50
            elif xVar == "CSV":
                xMin= 0
                xMax= 1
            elif xVar == "JetMulti":
                xMin= 4
                xMax= 15
            elif xVar == "BJetMulti":
                xMin= 0
                xMax= 8
                
        # Apply Styles
            styles.dataStyle.apply(eff_Data)
            styles.mcStyle.apply(eff_MC)
        
        # Marker Style
            eff_Data.SetMarkerSize(1)
                
        # Create Comparison Plot
            p = plots.ComparisonPlot(histograms.HistoGraph(eff_Data, "eff_Data","p","P"),
                                     histograms.HistoGraph(eff_MC,   "eff_MC", "p", "P"))
                
            opts       = {"ymin": 0  , "ymax": 1.1, "xmin":xMin, "xmax":xMax}
            opts2      = {"ymin": 0.8, "ymax": 1.05}
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
                p.getFrame().GetXaxis().SetTitle("p_{T,6thJet} (Gev/c)")
            elif xVar == "eta6thJet":
                p.getFrame().GetXaxis().SetTitle("#eta_{6thJet}")
            elif xVar == "phi6thJet":
                p.getFrame().GetXaxis().SetTitle("#phi_{6thJet}")
            elif xVar == "Ht":
                p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")
            elif xVar == "nBTagJets":
                p.getFrame().GetXaxis().SetTitle("nB-Jet")
            elif xVar == "pu":
                p.getFrame().GetXaxis().SetTitle("nPU")
            elif xVar == "CSV":
                p.getFrame().GetXaxis().SetTitle("CSV")
            elif xVar == "JetMulti":
                p.getFrame().GetXaxis().SetTitle("Jet Multiplicity")
            elif xVar == "BJetMulti":
                p.getFrame().GetXaxis().SetTitle("B-Jet Multiplicity")

            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                
                
            #if xVar == "pt6thJet" and s == "OR":
            #    plist = [0.7, 0.99, 1000, 0.16, 28.0]
            #    Fit_Richards(30.0, 120.0, p, eff_Data, plist)
            #    plist = [0.72, 0.91, 0.212, 0.15, 50.0]
            #    Fit_Richards(30.0, 120.0, p, eff_MC, plist)
            #elif xVar == "Ht" and s == "OR":
            #    plist = [0.00005, 0.988, 0.000000109, 0.15, 29.0]
            #    Fit_Richards(350.0, 2000.0, p, eff_Data, plist)
                #plist = [0.0003, 0.97, 0.45, 0.24, 43.0]
                #Fit_Richards(500.0, 2000.0, p, eff_MC, plist)
            #elif xVar == "nBTagJets":
                #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
                #Fit_Richards(30.0, 120.0, p, eff_Data, plist)
            #elif xVar == "pu":
                #plist = [0.07, 0.984, 0.45, 0.24, 43.0]
                #Fit_Richards(30.0, 120.0, p, eff_Data, plist)
            
                            
            # Draw
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
            
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
        

            '''
            # IN SLICES OF HT
    HTSlices = ["450ht600","600ht800","800ht1000", "1000ht1250", "1250ht1500", "1500ht2000"]
    for s in SigSel:
        for hsl in HTSlices:
            num_name = "Num_pt6thJet_Vs_"+hsl+"_RefTrg_OfflineSel_"+s
            den_name = "Den_pt6thJet_Vs_"+hsl+"_RefTrg_OfflineSel"
            # Get the save path and name        
            plotName = "Eff_pt6thJet_Vs_"+hsl+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 
            
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
            opts2      = {"ymin": 0.7, "ymax": 1.3}
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
            p.getFrame().GetXaxis().SetTitle("p_{T} (Gev/c)")
                    
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
            # Draw
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
        
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)

    
    PTSlices = ["40pt50","50pt60", "60pt70", "70pt90", "90pt120"]
    for s in SigSel:
        for psl in PTSlices:
            num_name = "Num_ht_Vs_"+psl+"_HLT_PFHT350_"+s
            den_name = "Den_ht_Vs_"+psl+"_HLT_PFHT350"
            # Get the save path and name        
            plotName = "Eff_ht_Vs_"+psl+"_"+s
            savePath, saveName = GetSavePathAndName(plotName, **kwargs)
        
            # Get Efficiency Plots
            eff_Data     = getEfficiency(datasetsMgr, dataset_Data, num_name, den_name , **kwargs)
            eff_MC       = getEfficiency(datasetsMgr, dataset_MC, num_name, den_name, **kwargs) 

            xMin = 450
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
            opts2      = {"ymin": 0.7, "ymax": 1.3}
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
            p.getFrame().GetXaxis().SetTitle("H_{T} (Gev/c)")
                    
            if createRatio:
                p.getFrame2().GetYaxis().SetTitle("Ratio")
                p.getFrame2().GetYaxis().SetTitleOffset(1.6)
                            
            # Draw
            histograms.addText(0.30, 0.10, "Runs "+runRange, 17)
            histograms.addText(0.30, 0.15, "2016", 17)
            histograms.addStandardTexts(lumi=lumi)
            p.draw()
        
            # Save the canvas to a file
            SaveAs(p, kwargs.get("savePath"), saveName, kwargs.get("saveFormats"), True)
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
