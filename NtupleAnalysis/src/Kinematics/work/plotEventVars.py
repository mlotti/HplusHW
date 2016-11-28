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
signal = [
    "ChargedHiggs_HplusTB_HplusToTB_M_180",
    "ChargedHiggs_HplusTB_HplusToTB_M_200",
    "ChargedHiggs_HplusTB_HplusToTB_M_220",
    "ChargedHiggs_HplusTB_HplusToTB_M_250",
    "ChargedHiggs_HplusTB_HplusToTB_M_300",
    "ChargedHiggs_HplusTB_HplusToTB_M_350",
    "ChargedHiggs_HplusTB_HplusToTB_M_400",
    "ChargedHiggs_HplusTB_HplusToTB_M_500",
    ]
signal200 = filter(lambda x: "M_200" not in x, signal)
signal500 = filter(lambda x: "M_500" not in x, signal)
signal2   = [s for s in signal if s not in ["ChargedHiggs_HplusTB_HplusToTB_M_200", "ChargedHiggs_HplusTB_HplusToTB_M_500"] ]

kwargs = {
    "analysis"       : "Kinematics",
    #"savePath"       : "/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/all/",
    #"savePath"       : None,
    "savePath"       : os.getcwd() + "/Plots/",
    "refDataset"     : "ChargedHiggs_HplusTB_HplusToTB_M_200", #ChargedHiggs_HplusTB_HplusToTB_M_200
    "saveFormats"    : [".png"],#, ".pdf"],
    "normalizeTo"    : "One", #One", "XSection", "Luminosity"
    "createRatio"    : False,
    "logX"           : False,
    "logY"           : True,
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
}


hNames = [
    "BQuarkPair_dRMin_pT",
    "BQuarkPair_dRMin_dEta",
    "BQuarkPair_dRMin_dPhi",
    "BQuarkPair_dRMin_dR",
    "BQuarkPair_dRMin_Mass",
    "BQuarkPair_dRMin_jet1_dR",
    "BQuarkPair_dRMin_jet1_dEta",
    "BQuarkPair_dRMin_jet1_dPhi",
    "BQuarkPair_dRMin_jet2_dR",
    "BQuarkPair_dRMin_jet2_dEta",
    "BQuarkPair_dRMin_jet2_dPhi",
#    "tbWMinus_bqq_Pt",
#    "tbWMinus_bqq_Rap",
#    "tbWMinus_bqq_Mass",
#    "tbWMinus_bqq_dRMax_dR",
#    "tbWMinus_bqq_dRMax_dRap",
#    "tbWMinus_bqq_dRMax_dPhi",
#    "tbWPlus_bqq_Pt",
#    "tbWPlus_bqq_Rap",
#    "tbWPlus_bqq_Mass",
#    "tbWPlus_bqq_dRMax_dR",
#    "tbWPlus_bqq_dRMax_dRap",
#    "tbWPlus_bqq_dRMax_dPhi",
#    "MaxDiJetMass_Pt",
#    "MaxDiJetMass_Eta",
#    "MaxDiJetMass_Mass",
#    "MaxDiJetMass_Rap",
#    "MaxDiJetMass_dR",
#    "MaxDiJetMass_dRrap",
#    "MaxDiJetMass_dEta",
#    "MaxDiJetMass_dRap",
#    "MaxDiJetMass_dPhi",
#    "SelGenJet_N_AfterLeptonVeto",
]


#hNames = [
#    "genMET_Et",
#    "genMET_Phi",
#    "genHT_GenJets",
#    "genHT_GenParticles",
#    "SelGenJet_N_NoPreselections",
#    "SelGenJet_N_AfterLeptonVeto",
#    "SelGenJet_N_AfterLeptonVetoNJetsCut",
#    "SelGenJet_N_AfterPreselections", 
#    "MaxDiJetMass_Pt",
#    "MaxDiJetMass_Eta",
#    "MaxDiJetMass_Mass",
#    "MaxDiJetMass_Rap",
#    "MaxDiJetMass_dR",
#    "MaxDiJetMass_dRrap",
#    "MaxDiJetMass_dEta",
#    "MaxDiJetMass_dRap",
#    "MaxDiJetMass_dPhi",
#    "BQuarkPair_dRMin_pT",
#    "BQuarkPair_dRMin_dEta",
#    "BQuarkPair_dRMin_dPhi",
#    "BQuarkPair_dRMin_dR",
#    "BQuarkPair_dRMin_Mass",
#    "BQuarkPair_dRMin_jet1_dR",
#    "BQuarkPair_dRMin_jet1_dEta",
#    "BQuarkPair_dRMin_jet1_dPhi",
#    "BQuarkPair_dRMin_jet2_dR",
#    "BQuarkPair_dRMin_jet2_dEta",
#    "BQuarkPair_dRMin_jet2_dPhi",
#    "Htb_tbW_bqq_Pt",
#    "Htb_tbW_bqq_Rap",
#    "Htb_tbW_bqq_Mass",
#    "Htb_tbW_bqq_dRMax_dR",
#    "Htb_tbW_bqq_dRMax_dRap",
#    "Htb_tbW_bqq_dRMax_dPhi",
#    "gtt_tbW_bqq_Pt",
#    "gtt_tbW_bqq_Rap",
#    "gtt_tbW_bqq_Mass",
#    "gtt_tbW_bqq_dRMax_dR",
#    "gtt_tbW_bqq_dRMax_dRap",
#    "gtt_tbW_bqq_dRMax_dPhi",
#]


#================================================================================================
# Main
#================================================================================================
def main(opts):

    style    = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)
    
    # Get all datasets from the mcrab dir
    # def GetDatasetsFromDir(mcrab, opts, **kwargs): #iro
    datasetsMgr  = GetDatasetsFromDir(opts.mcrab, opts, **kwargs) #kwargs.get("analysis"))

    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = GetLumi(datasetsMgr)
    
    # Update to PU
    datasetsMgr.updateNAllEventsToPUWeighted()

    # Remove datasets
    #print kwargs.get("rmDataset")
    #datasetsMgr.remove(kwargs.get("rmDataset"))
    # datasetsMgr.remove(filter(lambda name: not "QCD" in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "QCD" in name in name, datasetsMgr.getAllDatasetNames()))
    
    # Set custom XSections
    #datasetsMgr.getDataset("QCD_bEnriched_HT1000to1500").setCrossSection(1.0)
    #datasetsMgr.getDataset("QCD_bEnriched_HT1500to2000").setCrossSection(1.0)
    #datasetsMgr.getDataset("QCD_bEnriched_HT2000toInf").setCrossSection(1.0)
    #datasetsMgr.getDataset("QCD_bEnriched_HT300to500").setCrossSection(1.0)
    #datasetsMgr.getDataset("QCD_bEnriched_HT500to700").setCrossSection(1.0)
    #datasetsMgr.getDataset("QCD_bEnriched_HT700to1000").setCrossSection(1.0)
    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
    plots.mergeRenameReorderForDataMC(datasetsMgr) #WARNING: Merged MC histograms must be normalized to something!

    # Remove datasets (for merged names)
    # datasetsMgr.remove(kwargs.get("rmDataset"))
    
    # Print the cross
    datasetsMgr.PrintCrossSections()

    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        
        # Get the save path and name
        savePath, saveName = GetSavePathAndName(hName, **kwargs)
        
        # Get Histos for Plotter
        refHisto, otherHistos = GetHistosForPlotter(datasetsMgr, hName, **kwargs)
        
        # Create a comparison plot
        p = plots.ComparisonManyPlot(refHisto, otherHistos)

        # Remove negative contributions
        #RemoveNegativeBins(datasetsMgr, hName, p)

        # Create a frame
        if kwargs.get("logY")==True:
            opts = {"ymin": 1e-4, "ymaxfactor": 10}
            #opts = {"ymin": 1e-3, "ymax": 1}
        else:
            opts = {"ymin": 0.0, "ymaxfactor": 1.2}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0}
        p.createFrame(saveName, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)
        
        # Customise Legend
        moveLegend = {"dx": -0.2, "dy": +0.0, "dh": -0.1}
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
        histograms.addStandardTexts(lumi=intLumi)
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
    parser.add_option("-m", "--mcrab"    , dest="mcrab"    , action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", 
                      default=True, help="Enables batch mode (canvas creation does NOT generates a window)")

    parser.add_option("-v", "--verbose"  , dest="verbose"  , action="store_true", default=False, 
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
