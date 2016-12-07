#!/usr/bin/env python
'''
Usage:
Launch default script
./plotEvtShapeVars.py -m <pseudo_mcrab_directory>

Launch but exclude the M_180 sample
./plotEvtShapeVars.py -m Kinematics_161025_020335 -e M_180

Launch but exclude the multiple signal samples
./plotEvtShapeVars.py -m Kinematics_161025_020335 -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400"
Launch but only include the QCD_Pt samples
./plotEvtShapeVars.py -m Kinematics_0819_full -i QCD_Pt

Launch but exclude various samples
./plotEvtShapeVars.py -m Kinematics_0819_full/ -e "M_200|M_220|M_250|M_300|M_350|M_400|QCD_Pt|JetHT"
or 
./plotEvtShapeVars.py -m Kinematics_0819_full/ -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400|M_500|ZZTo4Q"

Last Used:
./plotEvtShapeVars.py -m Kinematics_0819_full/ -e "ZJets|TTTT_ext1|ttbb"
./plotEvtShapeVars.py -m Kinematics_0819_full/ -e "ZJets|TTTT_ext1"
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

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
kwargs = {
    "verbose"          : False,
    "dataEra"          : "Run2016",
    "searchMode"       : "80to1000",
    "analysis"         : "Kinematics",
    "optMode"          : "",
    "savePath"         : os.getcwd() + "/Plots/", #"/Users/attikis/latex/talks/post_doc.git/HPlus/HIG-XY-XYZ/2016/Kinematics_06September2016/figures/all/",
    #"savePath"         : "/publicweb/a/aattikis/EvtShapeVars/",
    "saveFormats"      : [".png", ".pdf"],
    "xlabel"           : None,
    "ylabel"           : "Arbitrary Units / %.2f",
    "rebinX"           : 1,
    "rebinY"           : 1,
    "xlabelsize"       : None, #10, #None, #10
    "ratio"            : False,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "stackMCHistograms": False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logY"             : True,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Preliminary", #"Preliminary" "Simulation"
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": 0.0, "dh": +0.0},
    "cutValue"         : None, #1.2,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
}


hNames = [
#     "dRMinDiJet_NoBJets_Pt",
#     "dRMinDiJet_NoBJets_Eta",
#     "dRMinDiJet_NoBJets_Rap",
#     "dRMinDiJet_NoBJets_Mass",
#     "dRMinDiJet_NoBJets_dR",
#     "dRMinDiJet_NoBJets_dEta",
#     "dRMinDiJet_NoBJets_dPhi",
#     "GenJet1_BJetsFirst_Pt",
#     "GenJet2_BJetsFirst_Pt",
#     "GenJet3_BJetsFirst_Pt",
#     "GenJet4_BJetsFirst_Pt",
#     "GenJet5_BJetsFirst_Pt",
#     "GenJet6_BJetsFirst_Pt",
#     "y23",
#     "Sphericity",
#     "SphericityT",
#     "Y",
#     "Aplanarity",
#     "Planarity",
#     "CParameter",
#     "DParameter",
#     "H2",
#     "Circularity",
#     "Centrality",
#     "HT",
#     "JT",
#     "MHT",
    "AlphaT",
#    "BQuarkPair_dRMin_Pt",
#    "BQuarkPair_dRMin_Eta",
#    "BQuarkPair_dRMin_Rap",
#    "BQuarkPair_dRMin_Phi",
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
#    "MaxDiJetMass_Pt",
#    "MaxDiJetMass_Eta",
#    "MaxDiJetMass_Mass",
#    "MaxDiJetMass_Rap",
#    "MaxDiJetMass_dR",
#    "MaxDiJetMass_dRrap",
#    "MaxDiJetMass_dEta",
#    "MaxDiJetMass_dRap",
#    "MaxDiJetMass_dPhi",
#    "BQuarkPair_dR",
#    "BQuarkPair_dEta",
#    "BQuarkPair_dPhi",
#    "BQuarkPair_dRAverage",
#    "BQuarkPair_dEtaAverage",
#    "BQuarkPair_dPhiAverage",
#    "BQuarkPair_MaxPt_Pt",
#    "BQuarkPair_MaxPt_Eta",
#    "BQuarkPair_MaxPt_Phi",
#    "BQuarkPair_MaxPt_M",
#    "BQuarkPair_MaxPt_dEta",
#    "BQuarkPair_MaxPt_dPhi",
#    "BQuarkPair_MaxPt_dR",
#    "BQuarkPair_MaxPt_jet1_dR",
#    "BQuarkPair_MaxPt_jet1_dEta",
#    "BQuarkPair_MaxPt_jet1_dPhi",
#    "BQuarkPair_MaxPt_jet2_dR",
#    "BQuarkPair_MaxPt_jet2_dEta",
#    "BQuarkPair_MaxPt_jet2_dPhi",
#    "BQuarkPair_MaxMass_Pt",
#    "BQuarkPair_MaxMass_Eta",
#    "BQuarkPair_MaxMass_Phi",
#    "BQuarkPair_MaxMass_M",
#    "BQuarkPair_MaxMass_dEta",
#    "BQuarkPair_MaxMass_dPhi",
#    "BQuarkPair_MaxMass_dR",
#    "BQuarkPair_MaxMass_jet1_dR",
#    "BQuarkPair_MaxMass_jet1_dEta",
#    "BQuarkPair_MaxMass_jet1_dPhi",
#    "BQuarkPair_MaxMass_jet2_dR",
#    "BQuarkPair_MaxMass_jet2_dEta",
#    "BQuarkPair_MaxMass_jet2_dPhi",
#    "BQuarks_N",
#    "BQuark1_Pt",
#    "BQuark2_Pt",
#    "BQuark3_Pt",
#    "BQuark4_Pt",
#    "BQuark1_Eta",
#    "BQuark2_Eta",
#    "BQuark3_Eta",
#    "BQuark4_Eta",
#    "GenJet1_Pt",
#    "GenJet2_Pt",
#    "GenJet3_Pt",
#    "GenJet4_Pt",
#    "GenJet5_Pt",
#    "GenJet6_Pt",
#    "GenJet1_Eta",
#    "GenJet2_Eta",
#    "GenJet3_Eta",
#    "GenJet4_Eta",
#    "GenJet5_Eta",
#    "GenJet6_Eta",
#    "MaxTriJetPt_Pt",
#    "MaxTriJetPt_Eta",
#    "MaxTriJetPt_Rap",
#    "MaxTriJetPt_Mass",
#    "MaxTriJetPt_dEtaMax",
#    "MaxTriJetPt_dPhiMax",
#    "MaxTriJetPt_dRMax",
#    "MaxTriJetPt_dEtaMin",
#    "MaxTriJetPt_dPhiMin",
#    "MaxTriJetPt_dRMin",
#    "MaxTriJetPt_dEtaAverage",
#    "MaxTriJetPt_dPhiAverage",
#    "MaxTriJetPt_dRAverage",
    ]



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
    if not verbose:
        return
    Print(msg, printHeader)
    return


def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return


def GetDatasetsFromDir(mcrab, opts, **kwargs):

    dataEra    = kwargs.get("dataEra")
    searchMode = kwargs.get("searchMode")
    analysis   = kwargs.get("analysis")
    optMode    = kwargs.get("optMode")

    if opts.includeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, includeOnlyTasks=opts.includeTasks, optimizationMode=optMode)
    elif opts.excludeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, excludeTasks=opts.excludeTasks, optimizationMode=optMode)
        # excludeTasks="M_180|M_220|M_250"
    else:
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
    return datasets


def main(hName, opts):

    # Setup the style
    style = tdrstyle.TDRStyle()
    
    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(opts.batchMode)

    # Setup & configure the dataset manager
    datasetsMgr = GetDatasetsFromDir(opts.mcrab, opts, **kwargs)
    datasetsMgr.updateNAllEventsToPUWeighted()
    # datasetsMgr.PrintCrossSections()
    # datasetsMgr.PrintLuminosities()

    # Set/Overwrite cross-sections
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
    
    # Merge datasets: All JetHT to "Data", QCD_Pt to "QCD", QCD_bEnriched to "QCD_b",  single-top to "SingleTop", WW, WZ, ZZ to "Diboson"           
    plots.mergeRenameReorderForDataMC(datasetsMgr)

    # Remove datasets
    # datasetsMgr.remove("QCD-b") 
    
    # Print dataset information
    # datasetsMgr.PrintInfo()
    
    # Create  plot, with the default 
    s = {"normalizeToOne": True}
    p = plots.MCPlot(datasetsMgr, hName, **s)
    p.histoMgr.setHistoLegendStyleAll("LP")
    p.histoMgr.setHistoDrawStyleAll("EP")
    p.histoMgr.setHistoLegendStyle("ChargedHiggs_HplusTB_HplusToTB_M_500", "F")
    p.histoMgr.setHistoDrawStyle ("ChargedHiggs_HplusTB_HplusToTB_M_500", "HIST")
    #datasetsMgr.getDataset("ZJetsToQQ_HT600toInf").getDatasetRootHisto(hName).getHistogram().SetMarkerColor(ROOT.kBlack)


    # Create a comparison plot
    ratioOpts = {"ymin": 0.0, "ymax": 2.0}
    if kwargs.get("logY")==True:
        canvOpts = {"xmin": 0.0, "ymin": 1e-5, "ymaxfactor": 10}
    else:
        canvOpts = {"ymin": 0.0, "ymaxfactor": 1.2}

    # Draw a customised plot & Save it
    plots.drawPlot(p, 
                   os.path.join(kwargs.get("savePath"), hName.replace("/", "_").replace(" ", "_").replace("(", "_").replace(")", "") ),
                   xlabel=kwargs.get("xlabel"), 
                   ylabel=kwargs.get("ylabel"),
                   rebinX=kwargs.get("rebinX"), 
                   rebinY=kwargs.get("rebinY"),
                   xlabelsize=kwargs.get("xlabelsize"),
                   ratio=kwargs.get("ratio"), 
                   stackMCHistograms=kwargs.get("stackMCHistograms"), 
                   ratioYlabel=kwargs.get("ratioYlabel"),
                   ratioInvert=kwargs.get("ratioInvert"),
                   addMCUncertainty=kwargs.get("addMCUncertainty"), 
                   addLuminosityText=kwargs.get("addLuminosityText"),
                   addCmsText=kwargs.get("addCmsText"),
                   opts=canvOpts, opts2=ratioOpts, 
                   log=kwargs.get("logY"), 
                   errorBarsX=kwargs.get("errorBarsX"),
                   cmsExtraText=kwargs.get("cmsExtraText"),
                   moveLegend=kwargs.get("moveLegend"),
                   drawStyle="P",
                   legendStyle="LP",
                   #cutLine=kwargs.get("cutValue"),
                   cutBox={"cutValue": kwargs.get("cutValue"), "fillColor": kwargs.get("cutFillColour"), "box": kwargs.get("cutBox"), "line": kwargs.get("cutLine"), "lessThan": kwargs.get("cutLessthan")},
                   )
    
    # Remove legend?
    if kwargs.get("removeLegend"):
        p.removeLegend()

    # Additional text
    # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
    # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)
    
    if not opts.batchMode:
        raw_input("=== plotTest.py:\n\tPress any key to quit ROOT ...")

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
    for histo in hNames:
        main(histo, opts)

    if not opts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")
