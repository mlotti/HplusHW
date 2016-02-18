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

#from InvertedTauID import *
analysis = "CorrelationAnalysis"


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

    #print datasets
    # Check multicrab consistency
    consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="CorrelationAnalysis")
   
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
    datasets.remove(filter(lambda name: "TTJets_FullLept" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "WJetsToLNu" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "DYJetsToLL" in name, datasets.getAllDatasetNames()))
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
    if False:
        datasets.merge("EWK", [
            "TTJets",
            "WJetsHT",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)


    dataMCExample(datasets)
    MtComparison(datasets)
#    MetComparison(datasets)
#    TauPtComparison(datasets)

   # Print counters

    doCounters(datasets)



    # Script execution can be paused like this, it will continue after
    # user has given some input (which must include enter)
    if drawToScreen:
        raw_input("Hit enter to continue")


def dataMCExample(datasets):
    # Create data-MC comparison plot, with the default
    # - legend labels (defined in plots._legendLabels)
    # - plot styles (defined in plots._plotStyles, and in styles)
    # - drawing styles ('HIST' for MC, 'EP' for data)
    # - legend styles ('L' for MC, 'P' for data)
    plot = plots.DataMCPlot(datasets,
                            #"ForDataDrivenCtrlPlots/SelectedTau_pT_AfterStandardSelections"
                            "tauPt",
                            # Since the data datasets were removed, we have to set the luminosity by hand

                            # normalizeToLumi=20000

    )

    # Same as below, but more compact
    plots.drawPlot(plot, "taupt", xlabel="Tau p_{T} (GeV/c)", ylabel="Number of events",

                   rebin=10, stackMCHistograms=True, addMCUncertainty=False, addLuminosityText=True,
                   opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True, ratio=True)


    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=False, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 1})

    def createDrawPlot(name, **kwargs):
        drawPlot( plots.DataMCPlot(datasets, name), name, **kwargs)
        
    createDrawPlot("tauSelection_/tauEtaTriggerMatched", xlabel="#eta^{#tau jet}", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("tauEta", xlabel="#eta^{#tau jet}", ylabel="Number of events", rebin=2, log=False, ratio=True)
#    createDrawPlot("tauPhi", xlabel="#phi^{#tau jet}", ylabel="Number of events", rebin=2, log=False)
#    createDrawPlot("Rtau", xlabel="p_{T}^{leading track}/p_{T}^{#tau jet}", ylabel="Number of events", rebin=1, log=True)

    createDrawPlot("Met", xlabel="E_{T}^{miss} (GeV)", ylabel="Number of events", rebin=5, log=True, ratio=True, opts={"ymin": 1e-1, "ymaxfactor": 10})
    createDrawPlot("tauPt", xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
    if False:
        createDrawPlot("electronPt", xlabel="p_{T}^{electron} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
        createDrawPlot("electronEta", xlabel="#eta^{electron}", ylabel="Number of events", rebin=2, log=False)
        createDrawPlot("muonPt", xlabel="p_{T}^{muon} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
        createDrawPlot("muonEta", xlabel="#eta^{muon}", ylabel="Number of events", rebin=2, log=False)
        createDrawPlot("Nelectrons", xlabel="N_{electrons}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("Nmuons", xlabel="N_{muons}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("bJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
        createDrawPlot("bjetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("realBJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
        createDrawPlot("realBJetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("realMaxBJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
        createDrawPlot("realMaxBJetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("jetEta", xlabel="#eta^{jet}", ylabel="Number of events", rebin=1, log=False)
        createDrawPlot("jetPhi", xlabel="#phi^{jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("SelectedJets", xlabel="Number All Jets", ylabel="Number of events", rebin=1, log=False, ratio=True)
    createDrawPlot("SelectedBJets", xlabel="Number of B-jets", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("SelectedNonBJets", xlabel="Number of Light Jets", ylabel="Number of events", rebin=1, log=False)
    
    createDrawPlot("DeltaPhiTauMet", xlabel="#Delta#Phi(#tau,MET)", ylabel="Number of events", rebin=2, log=False, opts={"ymin": 0, "xmin":0})        
    createDrawPlot("M3jetsVSM2jetsCut", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=5, log=False)
    createDrawPlot("Pt3Jets", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=5, log=False)
    createDrawPlot("M3Jets", xlabel="M^{3jets} (GeV)", ylabel="Number of events", rebin=5, log=False)
    createDrawPlot("Pt2Jets", xlabel="p_{T}^{2jets} (GeV/c)", ylabel="Number of events", rebin=5, log=False)
    createDrawPlot("M2Jets", xlabel="M^{2jets} (GeV)", ylabel="Number of events", rebin=5, log=False) 
    createDrawPlot("TheeJetPtcut", xlabel="ThreeJetPtcut (GeV/c)", ylabel="Number of events", rebin=4, log=True, opts={"xmax":450, "xmin":0})
    createDrawPlot("DPhi3JetsMet", xlabel="#Delta#phi(3 jets, MET)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("DrTau3Jets", xlabel="#DeltaR(3 jets, #tau jet)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("DphiMinus3jetcut", xlabel="#DeltaR(3 jets, #tau jet)", ylabel="Number of events", rebin=10, log=False, opts={"xmax":200})

    createDrawPlot("JetTauEtSum", xlabel="#Sigma(Jets,#tau jet) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("JetEtSum", xlabel="#Sigma(Jets) (GeV)", ylabel="Number of events", rebin=5, log=False)
    createDrawPlot("JetTauMetEtSum", xlabel="#Sigma(Jets,#tau jet, MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("JetEtSumVsJetTauMetEtSum3JetCut", xlabel="#Sigma(E_{T}) cut (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("JetTauMetEtSum", xlabel="#Sigma(E_{T}) cut (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("PtMaxJet", xlabel="p_{T}^{max jet} (GeV)", ylabel="Number of events", rebin=2, log=False)
#    createDrawPlot("transverseMass", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=1, log=False, opts={"ymin": 0, "xmin":5, "ymaxfactor": 0.1})
    createDrawPlot("transverseMass", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassTriangleCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMass3JetCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMass1Tau", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassGenuineTau", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMass3Jet150", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassDeltaPhiVsMaxPtCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassDeltaR3JetsTauCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassDeltaRCorrCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassWith3JetAndJetSumCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassWith3TopPtVSDrCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassTopMtCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMass3jetsMtCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassTopAndWMassCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassTopMassCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassTopMass3jetsMtCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassWCandFound", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("transverseMassDeltaPhi3jetPtCutDiff", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)    
    createDrawPlot("mt_top_met", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("mt_3jets_met", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=5, log=True)
    createDrawPlot("TopPtVSDrCut", xlabel="TopPtVSDrCut", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("deltaPhiVSmaxPtCut", xlabel="deltaPhiVSmaxPt", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("topPt", xlabel="p_{T}^{top}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("topEta", xlabel="#eta^{top}) ", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("topMass", xlabel="M_{top}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("topMassIdAllJets", xlabel="M_{top}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("topMassIdBjet", xlabel="M_{top}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("WPt", xlabel="p_{T}^{W}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("WEta", xlabel="#eta^{W}) ", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("WMass", xlabel="M_{W}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("WCandMass", xlabel="M_{W}) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("deltaR_W_tau", xlabel="#DeltaR(W,tau)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("deltaR_Wb", xlabel="#DeltaR(W,b)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("deltaR_top_tau", xlabel="#DeltaR(top,tau)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("deltaR_jets", xlabel="#DeltaR(jet,jet)", ylabel="Number of events", rebin=2, log=False)
#    createDrawPlot("constantEtSum", xlabel="Constant term (GeV)", ylabel="Number of events", rebin=2, log=True)
#    createDrawPlot("slopeEtSum", xlabel="Slope", ylabel="Number of events", rebin=2, log=True)

#    plots.drawPlot( plots.DataMCPlot(datasets, "Pt3Jets", normalizeToLumi=20000), "Pt3Jets", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
#    plots.drawPlot( plots.DataMCPlot(datasets, "DeltaPhiTauMet", normalizeToLumi=20000), "DeltaPhiTauMet", xlabel="#Delta#Phi(#tau,MET)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)



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
    mt = plots.PlotBase(getHistos(datasets,"transverseMass", "transverseMassTriangleCut", "transverseMass3JetCut"))
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
            "transverseMass": "m_{T}(#tau jet, E_{T}^{miss})",
            "transverseMassTriangleCut": "m_{T}(#tau jet, E_{T}^{miss}) with Triangle Cut",
            "transverseMass3JetCut": "m_{T}(#tau jet, E_{T}^{miss}) with 3-jet Cut"
            })
#    mt.histoMgr.setHistoDrawStyleAll("P")

    mt.appendPlotObject(histograms.PlotText(300, 50, "p_{T}^{jet} > 50 GeV/c", size=20))
    xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=False,
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

    print eventCounter.getSubCounterTable("tau selection").format(cellFormat)
    print eventCounter.getSubCounterTable("e selection").format(cellFormat)
    print eventCounter.getSubCounterTable("mu selection").format(cellFormat)
    print eventCounter.getSubCounterTable("jetselection").format(cellFormat)
    print eventCounter.getSubCounterTable("angular cuts / Collinear").format(cellFormat)
    print eventCounter.getSubCounterTable("bjetselection").format(cellFormat)
    print eventCounter.getSubCounterTable("angular cuts / BackToBack").format(cellFormat)                                                                                                                                





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

