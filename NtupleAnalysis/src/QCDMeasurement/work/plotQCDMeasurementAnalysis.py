#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

drawToScreen = True
drawToScreen = False

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck

from old_InvertedTauID import *
analysis = "QCDMeasurement"


#dataEra = "Run2015C"
#dataEra = "Run2015D"
#dataEra = "Run2015CD"
dataEra = "Run2015"

searchMode = "80to1000"


def usage():
    print "\n"
    print "### Usage:   InvertedTauID_Normalization_QCDFromData.py <multicrab dir>\n"
    print "\n"
    sys.exit()

def main(argv):
    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    comparisonList = ["AfterStdSelections"]
    
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis)
    #print datasets.getDatasetNames()

    print " dirs ",dirs[0]
    # Check multicrab consistency
#    consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="CorrelationAnalysis")
   
  # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    datasets.updateNAllEventsToPUWeighted()

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    #datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTToHplusBWB" in name, datasets.getAllDatasetNames()))

    datasets.remove(filter(lambda name: "HplusTB" in name and not "M_500" in name, datasets.getAllDatasetNames()))
   # datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets" in name, datasets.getAllDatasetNames()))
    #datasets.remove(filter(lambda name: "DYJetsToLL_M_50_HT" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    #datasets.remove(filter(lambda name: "WJetsToLNu" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: ("DYJetsToLL_M_10to50" in name or "DYJetsToLL_M_50" in name) and not "DYJetsToLL_M_50_HT" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "WJetsToLNu" in name and not "WJetsToLNu_HT" in name, datasets.getAllDatasetNames()))  
    # Default merging nad ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Set BR(t->H) to 0.05, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH datasets to one (for each mass bin)
    # TTToHplusBWB_MXXX and TTToHplusBHminusB_MXXX to "TTToHplus_MXXX"
    plots.mergeWHandHH(datasets)

#    datasets.getDataset("TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6").setCrossSection(0.336902*2*0.955592) # pb   

    # At the moment the collision energy must be set by hand
#    for dset in datasets.getMCDatasets():
#        dset.setEnergy("13")

    # At the moment the cross sections must be set by hand
    #xsect.setBackgroundCrossSections(datasets)


#    datasets.merge("EWK", [
#        "TT",
#        "WJetsHT",
#        "DYJetsToLLHT",
#        "SingleTop",
#            "Diboson"
#        ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)


    dataMCExample(datasets)
#    MtComparison(datasets)
#    MtComparisonBaseline(datasets)
#    MetComparison(datasets)
#    TauPtComparison(datasets)

   # Print counters
    doCounters(datasets)



    # Script execution can be paused like this, it will continue after
    # user has given some input (which must include enter)
    if drawToScreen:
        raw_input("Hit enter to continue")

        
try:
    from QCDNormalizationFactors_AfterStdSelections_Run2015_80to1000 import *
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print



def normalisationInclusive():

    norm_inc = QCDPlusEWKFakeTausNormalization["Inclusive"]
 #   normEWK_inc = QCDInvertedNormalization["inclusiveEWK"]

    print "inclusive norm", norm_inc
    return norm_inc



def dataMCExample(datasets):
     # Create data-MC comparison plot, with the default
     # - legend labels (defined in plots._legendLabels)
     # - plot styles (defined in plots._plotStyles, and in styles)
     # - drawing styles ('HIST' for MC, 'EP' for data)
     # - legend styles ('L' for MC, 'P' for data)
#     plot = plots.DataMCPlot(datasets, "QCDPurity/InvertedTauTauPtAfterAllSelections",
#                             #"tauPt",
#                             # Since the data datasets were removed,we have to set the luminosity by hand
#                             # normalizeToLumi=20000
#     )




        
    plots.drawPlot(plots.DataMCPlot(datasets, "QCDPurity/InvertedTauTauPtAfterAllSelections"),"InvertedTauTauPtAfterAllSelections",
                    xlabel="Tau p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/jetPtAll"), "jetPtAll",
                    xlabel="Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
  
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/jetEtaAll"), "jetEtaAll",
                    xlabel="Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsFirstJetPt"), "selectedJetsFirstJetPt",
                    xlabel="First Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsFirstJetEta"), "selectedJetsFirstJetEta",
                    xlabel="First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsSecondJetPt"), "selectedJetsSecondJetPt",
                    xlabel="Second Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsSecondJetEta"), "selectedJetsSecondJetEta",
                    xlabel="First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsThirdJetPt"), "selectedJetsThirdJetPt",
                    xlabel="Third Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "jetSelection_InvertedTau/selectedJetsThirdJetEta"), "selectedJetsThirdJetEta",
                    xlabel="Third Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

     
    plots.drawPlot(plots.DataMCPlot(datasets, "eSelection_VetoInvertedTau/electronPtPassed"), "electronPtPassed",
                    xlabel="Passed electron p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "eSelection_VetoInvertedTau/electronEtaPassed"), "electronEtaPassed",
                    xlabel="Passed electron #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "muSelection_VetoInvertedTau/IsolPtBefore"), "IsolPtBefore",
                    xlabel="Muon p_{T} (GeV/c) before isolation", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "muSelection_VetoInvertedTau/IsolEtaBefore"), "IsolEtaBefore",
                    xlabel="Muon #eta before isolation", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
         
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsFirstJetPt"), "selectedBJetsFirstJetPt",
                    xlabel="selected B Jets First Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsSecondJetPt"), "selectedBJetsSecondJetPt",
                    xlabel="selected B Jets Second Jet p_{T} (GeV/c)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsFirstJetEta"), "selectedBJetsFirstJetEta",
                    xlabel="selected B Jets First Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "bjetSelection_InvertedTau/selectedBJetsSecondJetEta"), "selectedBJetsSecondJetEta",
                    xlabel="selected B Jets Second Jet #eta", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1, "ymaxfactor": 1}, log=False)

#####################################################################
     
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterTau_realTau"), "TauPt_inv_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    """     
     inverted = plots.DataMCPlot(datasets,"TauPt_inv_afterTau")
     invertedData = inverted.histoMgr.getHisto("Data").getRootHisto().Clone("TauPt_inv_afterTau")
     invertedRealTau = plots.DataMCPlot(datasets,"TauPt_inv_afterTau_realTau")
     invertedEWKRealTau = invertedRealTau.histoMgr.getHisto("EWK").getRootHisto().Clone("TauPt_inv_afterTau_realTau")
     dataMinusRealTau = invertedData.Clone()
     dataMinusRealTau.SetName("dataMinusRealTau")
     dataMinusRealTau.Add(invertedEWKRealTau,-1)
    """
     
     
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterTau"), "TauPt_inv_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau"), "Met_inv_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau_realTau"), "Met_inv_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterJets_realTau"), "TauPt_inv_afterJets_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)


    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_baseline_afterTau"), "TauPt_baseline_afterTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_baseline_afterTau_realTau"), "TauPt_baseline_afterTau_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterJets"), "TauPt_inv_afterJets",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)


    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterBtag_realTau"), "TauPt_inv_afterBtag_realTau",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "TauPt_inv_afterBtag"), "TauPt_inv_afterBtag",
                    xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)


    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau_realTau"), "Met_inv_afterTau_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterTau"), "Met_inv_afterTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterJets_realTau"), "Met_inv_afterJets_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterJets"), "Met_inv_afterJets",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)


    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterBtag_realTau"), "Met_inv_afterBtag_realTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
    plots.drawPlot(plots.DataMCPlot(datasets, "Met_inv_afterBtag"), "Met_inv_afterBtag",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
  ####################################################################################        
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/MET/METInclusive"), "METInclusive_ForDataDrivenCrlPlots",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
         
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/MET_AfterAllSelections/MET_AfterAllSelectionsInclusive"), "MET_AfterAllSelectionsInclusive_ForDataDrivenCrlPlots",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
         
    plots.drawPlot(plots.DataMCPlot(datasets, "ForDataDrivenCtrlPlots/shapeTransverseMass/shapeTransverseMassInclusive"), "shapeTransverseMassInclusive",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10.0}, log=True)
     
  
         
    plots.drawPlot(plots.DataMCPlot(datasets, "metSelection_InvertedTau/Met"), "MetInvertedTau",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=2, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)   
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "MetInvertedTauAfterStdSelectionsInclusive",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=15, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelectionsInclusive",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKFakeTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "MetInvertedTauAfterStdSelectionsInclusiveFakeTaus",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKFakeTaus/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelectionsInclusiveFakeTaus",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalization/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelections",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=5, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 500, "ymaxfactor": 10}, log=True)

    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKGenuineTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"), "MetInvertedTauAfterStdSelectionsInclusiveGenuineTaus",
                    xlabel="MET (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)
     
    plots.drawPlot(plots.DataMCPlot(datasets, "ForQCDNormalizationEWKGenuineTaus/NormalizationMtInvertedTauAfterStdSelections/NormalizationMtInvertedTauAfterStdSelectionsInclusive"), "MtInvertedTauAfterStdSelectionsInclusiveGenuineTaus",
                    xlabel="m_{T} (GeV)", ylabel="Number of events",
                    rebin=4, stackMCHistograms=True,
                    addMCUncertainty=False, ratio=True, createRatio=True,
                    addLuminosityText=True, 
                    opts={"ymin": 1e-1,"xmax": 800, "ymaxfactor": 10}, log=True)



                         
def getHistos(datasets,name1, name2, name3):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto(name1)
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto(name2)
     drh3 = datasets.getDataset("TTJets").getDatasetRootHisto(name3)
     drh1.setName("transverseMass")
     drh2.setName("transverseMassTriangleCut")
     drh3.setName("transverseMass3JetCut")
     return [drh1, drh2, drh3]

#mt = plots.PlotBase(getHistos("MetNoJetInHole", "MetJetInHole"))

def MtComparison(datasets):
    mt = plots.PlotBase(getHistos(datasets,"ForQCDNormalization/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKFakeTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKGenuineTaus/NormalizationMETInvertedTauAfterStdSelections/NormalizationMETInvertedTauAfterStdSelectionsInclusive"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[3]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("transverseMass", st1)
    mt.histoMgr.forHisto("transverseMassTriangleCut", st2)
    mt.histoMgr.forHisto("transverseMass3JetCut", st3)

    mt.histoMgr.setHistoLegendLabelMany({
            "transverseMass": "All inverted Taus",
            "transverseMassTriangleCut": "Inverted Fake Taus",
            "transverseMass3JetCut": "Inverted Genuine Taus"
            })
#    mt.histoMgr.setHistoDrawStyleAll("P")

    mt.appendPlotObject(histograms.PlotText(50, 1, "3-prong Taus", size=20))
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=10, log=True,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
          
#    rtauGen(mt, "MetComparison", rebin=1, ratio=True, defaultStyles=False)

def MtComparisonBaseline(datasets):
    mt = plots.PlotBase(getHistos(datasets,"ForQCDNormalization/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKFakeTaus/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive", "ForQCDNormalizationEWKGenuineTaus/NormalizationMETBaselineTauAfterStdSelections/NormalizationMETBaselineTauAfterStdSelectionsInclusive"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[3]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("transverseMass", st1)
    mt.histoMgr.forHisto("transverseMassTriangleCut", st2)
    mt.histoMgr.forHisto("transverseMass3JetCut", st3)

    mt.histoMgr.setHistoLegendLabelMany({
            "transverseMass": "All baseline Taus",
            "transverseMassTriangleCut": "Baseline Fake Taus",
            "transverseMass3JetCut": "Baseline Genuine Taus"
            })
#    mt.histoMgr.setHistoDrawStyleAll("P")

    mt.appendPlotObject(histograms.PlotText(50, 1, "3-prong Taus", size=20))
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparisonBaseline", xlabel=xlabel, ylabel=ylabel, rebinX=1, log=True,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
          
#    rtauGen(mt, "MetComparison", rebin=1, ratio=True, defaultStyles=False)

def getHistos2(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("Met")
     #drh2 = datasets.getDataset("TT_pythia8").getDatasetRootHisto("Met")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("Met")

     drh1.setName("Met_madgraph")
     drh2.setName("Met_pythia8")
     return [drh1, drh2]

#mt = plots.PlotBase(getHistos("MetNoJetInHole", "MetJetInHole"))                                                                                                                                                                                                      

def MetComparison(datasets):
    mt = plots.ComparisonPlot(*getHistos2(datasets,"Met","Met"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())                                                                                                                                                                                  
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("Met_madgraph", st1)
    mt.histoMgr.forHisto("Met_pythia8", st2)
    mt.histoMgr.setHistoLegendLabelMany({
            "Met_madgraph": "Met from Madgraph",
            "Met_pythia8": "Met from Pythia8"
            })
    mt.histoMgr.setHistoDrawStyleAll("PE")


    mt.appendPlotObject(histograms.PlotText(100, 0.01, "tt events", size=20))
    xlabel = "PF E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MetComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=True,
                   createLegend={"x1": 0.6, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 50}, opts={"xmax": 500})


def getHistos3(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")
    # drh2 = datasets.getDataset("TT_pythia8").getDatasetRootHisto("tauPt")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")

     drh1.setName("Taupt_madgraph")
     drh2.setName("Taupt_pythia8")
     return [drh1, drh2]

def TauPtComparison(datasets):
    mt = plots.ComparisonPlot(*getHistos3(datasets,"tauPt","tauPt"))
                                                                                                                                                                                                                                                                       
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("Taupt_madgraph", st1)
    mt.histoMgr.forHisto("Taupt_pythia8", st2)
    mt.histoMgr.setHistoLegendLabelMany({
            "Taupt_madgraph": "Tau pt from Madgraph",
            "Taupt_pythia8": "Tau pt from Pythia8"
            })
    mt.histoMgr.setHistoDrawStyleAll("PE")

    mt.appendPlotObject(histograms.PlotText(100, 0.01, "tt events", size=20))
    xlabel = "p_{T}^{#tau jet} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "TauPtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=True,
                   createLegend={"x1": 0.6, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 50}, opts={"xmax": 800, "ymin":1, "ymax":1000000})






def rtauGen(h, name, rebin=2, ratio=False, defaultStyles=True):
    if defaultStyles:
        h.setDefaultStyles()
        h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))


    xlabel = "PF E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f" % h.binWidth()
    if "LeptonsInMt" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "NoLeptonsRealTau" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "Mass" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()

        
    kwargs = {"ymin": 0.1, "ymax": 1000}
    if "LeptonsInMt" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "NoLeptonsRealTau" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "Rtau" in name:
        kwargs = {"ymin": 0.0001, "xmax": 1.1}   
        kwargs = {"ymin": 0.1, "xmax": 1.1}     
        h.getPad().SetLogy(True)

#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"

    h.createFrame(name, **kwargs)

#    histograms.addText(0.65, 0.7, "BR(t #rightarrow bH^{#pm})=0.05", 20)
    h.getPad().SetLogy(True)
    
    leg = histograms.createLegend(0.6, 0.75, 0.8, 0.9)
 
    if "LeptonsInMt" in name:
        h.getPad().SetLogy(False)
        leg = histograms.moveLegend(leg, dx=-0.18)
        histograms.addText(0.5, 0.65, "TailKiller cut: Tight", 20)
  
    h.setLegend(leg)
    plots._legendLabels["MetNoJetInHole"] = "Jets outside dead cells"
    plots._legendLabels["MetJetInHole"] = "Jets within dead cells"
    histograms.addText(300, 300, "p_{T}^{jet} > 50 GeV/c", 20)
    kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
    kwargs["createRatio"] = True
#    if ratio:
#        h.createFrameFraction(name, opts=opts, opts2=opts2)
#    h.setLegend(leg)

    common(h, xlabel, ylabel)



def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)
    ewkDatasets = [
        "WJets", "TTJets",
#        "WJets",                                                                                                                      
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

#    if mcOnly:
#        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
#    else:
    eventCounter.normalizeMCByLuminosity()

    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
#    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default                                                                                                                                                                                                                                                      
#    cellFormat = counter.TableFormatText()                                                                                                                                                                                                                        
    # No uncertainties                                                                                                                                                                                                                                             
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)
    print eventCounter.getSubCounterTable("TauSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("e selection").format(cellFormat)
    print eventCounter.getSubCounterTable("mu selection").format(cellFormat)
    print eventCounter.getSubCounterTable("jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("angular cuts / Collinear").format(cellFormat)
    print eventCounter.getSubCounterTable("bjet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("angular cuts / BackToBack").format(cellFormat)                                                                                                                                
# Common drawing function
def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()


#    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    if addMCUncertainty:
        h.addMCUncertainty()
        
    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
##    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts2 = {"ymin": 0.0, "ymax": 2.0}
    _opts.update(opts)
    _opts2.update(opts2)

    #if log:
    #    name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    if log:
        h.getPad().SetLogy(log)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    common(h, xlabel, ylab, textFunction=textFunction)



# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
#    h.addStandardTexts(addLuminosityText=addLuminosityText)
#    if textFunction != None:
#        textFunction()
    h.save()


if __name__ == "__main__":
    main(sys.argv)
