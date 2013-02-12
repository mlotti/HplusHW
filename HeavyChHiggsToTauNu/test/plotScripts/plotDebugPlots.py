#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
# Adapted from original for signal analysis debugging and validation
# by Lauri Wendland
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configuration
analysis = "signalAnalysis"
#analysis = "signalOptimisation"TauID_Rtau.png
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"
counters = analysis+"/counters"

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False

removeQCD = False

optionBr = 0.01

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

dataEra = "Run2011A"
#dataEra = "Run2011B"
#dataEra = "Run2011AB"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, dataEra=dataEra)
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()




    datasets.updateNAllEventsToPUWeighted()

    # Take QCD from data
    datasetsQCD = None
    if QCDfromData:
        datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysisJune/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_120705_162351/multicrab.cfg", counters=counters)
        datasetsQCD.loadLuminosities()
        datasetsQCD.mergeData()
        datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
        datasetsQCD.rename("Data", "QCD")
    
#Rtau =0
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110804_104313/multicrab.cfg", counters=counters)

#    datasetsSignal.selectAndReorder(["HplusTB_M200_Summer11"])
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_4_patch1/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110622_112321/multicrab.cfg", counters=counters)
    #datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_1_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/Signal_v11f_scaledb_424/multicrab.cfg", counters=counters)

    #datasetsSignal.selectAndReorder(["TTToHplusBWB_M120_Summer11", "TTToHplusBHminusB_M120_Summer11"])
    #datasetsSignal.renameMany({"TTToHplusBWB_M120_Summer11" :"TTToHplusBWB_M120_Spring11",
    #                           "TTToHplusBHminusB_M120_Summer11": "TTToHplusBHminusB_M120_Spring11"})
    #datasets.extend(datasetsSignal)

    plots.mergeRenameReorderForDataMC(datasets)

    if mcOnly:
        print "Int.Lumi (manually set)",mcOnlyLumi
    else:
        print "Int.Lumi",datasets.getDataset("Data").getLuminosity()
    print "norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    # Remove signals other than M120
#    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "QCD_Pt20_MuEnriched" in name, datasets.getAllDatasetNames()))
    
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    # Remove QCD
    if removeQCD:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.createLegend.moveDefaults(dh=-0.03)
    
    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=optionBr, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
########    datasets.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)

    # Replace signal dataset with EWK+signal
    if False:
        ttjets2 = datasets.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasets.getDataset("TTToHplus_M120").getCrossSection())
        datasets.append(ttjets2)
        datasets.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        datasets.merge("TTToHplus_M120", ["TTToHplus_M120", "EWKnoTT", "TTJets2"])
        plots._legendLabels["TTToHplus_M120"] = "with H^{#pm}#rightarrow#tau^{#pm}#nu"
#        plots._legendLabels["TTToHplus_M120"] = "m_{H^{#pm}} = 120 GeV/c^{2}"
#        plots._legendLabels["TTToHplus_M80"] = "m_{H^{#pm}} = 80 GeV/c^{2}"
#        plots._legendLabels["TTToHplus_M160"] = "m_{H^{#pm}} = 160 GeV/c^{2}"
      
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Print counters
    doCounters(datasets)
    
def doPlots(datasets):
    def createPlot(name, **kwargs):
        if mcOnly:
            # If 'normalizeToOne' is given in kwargs, we don't need the normalizeToLumi (or actually the library raises an Exception)
            args = {}
            args.update(kwargs)
            if not ("normalizeToOne" in args and args["normalizeToOne"]):
                args["normalizeToLumi"] = mcOnlyLumi
            return plots.MCPlot(datasets, analysis+"/"+name, **args)
        else:
            return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)

    def pickSliceX(th2, ybinName):
        th1 = ROOT.TH1D(th2.GetName(), th2.GetTitle(), th2.GetNbinsX(), histograms.th1Xmin(th2), histograms.th1Xmax(th2))
        th1.Sumw2()
        ybin = None
        for bin in xrange(1, th2.GetNbinsY()+1):
            if th2.GetYaxis().GetBinLabel(bin) == ybinName:
                ybin = bin
                break
        if ybin is None:
            raise Exception("Did not find y bin label %s from histogram %s" % (ybinName, th2.GetName()))
        for xbin in xrange(0, th2.GetNbinsX()+2): # include under/overflow bins
            th1.SetBinContent(xbin, th2.GetBinContent(xbin, ybin))
            th1.SetBinError(xbin, th2.GetBinError(xbin, ybin))
        return th1

    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    myDir = "Vertices"
    drawPlot(createPlot(myDir+"/verticesBeforeWeight"), "verticesBeforeWeight", xlabel="N_{vertices}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/verticesAfterWeight"), "verticesAfterWeight", xlabel="N_{vertices}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/verticesTriggeredBeforeWeight"), "verticesTriggeredBeforeWeight", xlabel="N_{vertices}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/verticesTriggeredAfterWeight"), "verticesTriggeredAfterWeight", xlabel="N_{vertices}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "TauSelection"
    drawPlot(createPlot(myDir+"/N_TriggerMatchedTaus"), "tauID0_N_TriggerMatchedTaus", xlabel="N_{trg. matched taus}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/N_TriggerMatchedSeparateTaus"), "tauID0_N_TriggerMatchedSeparateTaus", xlabel="N_{trg. matched separate taus}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/HPSDecayMode"), "tauID0_HPSDecayMode", xlabel="HPS Decay Mode", ylabel="N_{events}", log=True, ratio=True, opts={"xmax": 15}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_all_tau_candidates_N"), "tauID1_TauSelection_all_tau_candidates_N", xlabel="N_{tau candidates}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_all_tau_candidates_pt"), "tauID1_TauSelection_all_tau_candidates_pt", xlabel="p_{T} of all tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_all_tau_candidates_eta"), "tauID1_TauSelection_all_tau_candidates_eta", xlabel="#eta of all tau candiates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_all_tau_candidates_phi"), "tauID1_TauSelection_all_tau_candidates_phi", xlabel="#phi of all tau candidates", ylabel="N_{events}",  rebinToWidthX=0.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_all_tau_candidates_MC_purity"), "tauID1_TauSelection_all_tau_candidates_MC_purity", xlabel="MC purity of all tau candidates", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauCand_JetPt"), "tauID2_TauCand_JetPt", xlabel="p_{T} of tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauCand_JetEta"), "tauID2_TauCand_JetEta", xlabel="#eta of tau candidates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauCand_LdgTrackPtCut"), "tauID2_TauCand_LdgTrackPtCut", xlabel="p_{T}^{ldg.ch.particle} of tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    #drawPlot(createPlot(myDir+"/TauCand_EMFractionCut"), "tauID2_TauCand_EMFractionCut", xlabel="EM energy fraction of tau candidates", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_N"), "tauID3_TauSelection_cleaned_tau_candidates_N", xlabel="N_{cleaned tau candidates}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_pt"), "tauID3_TauSelection_cleaned_tau_candidates_pt", xlabel="p_{T} of cleaned tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_eta"), "tauID3_TauSelection_cleaned_tau_candidates_eta", xlabel="#eta of cleaned tau candidates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_phi"), "tauID3_TauSelection_cleaned_tau_candidates_phi", xlabel="#phi of cleaned tau candidates", ylabel="N_{events}", rebinToWidthX=0.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_MC_purity"), "tauID3_TauSelection_cleaned_tau_candidates_MC_purity", xlabel="MC purity of cleaned tau candidates", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/IsolationPFChargedHadrCandsPtSum"), "tauID4_IsolationPFChargedHadrCandsPtSum", xlabel="#sum p_{T} of PF ch. hadr. candidates, GeV/c", ylabel="N_{events}", log=True, ratio=True, opts={"xmax": 40}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/IsolationPFGammaCandEtSum"), "tauID4_IsolationPFGammaCandEtSum", xlabel="#sum p_{T} of PF gamma candidates, GeV/c", ylabel="N_{events}", log=True, ratio=True, opts={"xmax": 40}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauID_NProngsCut"), "tauID4_TauID_NProngsCut", xlabel="N_{prongs}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    #drawPlot(createPlot(myDir+"/TauID_ChargeCut"), "tauID4_TauID_ChargeCut", xlabel="Q_{tau}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauID_RtauCut"), "tauID4_TauID_RtauCut", xlabel="R_{#tau}", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_selected_taus_N"), "tauID5_TauSelection_selected_taus_N", xlabel="N_{selected taus}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_selected_taus_pt"), "tauID5_TauSelection_selected_taus_pt", xlabel="p_{T} of selected taus", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_selected_taus_eta"), "tauID5_TauSelection_selected_taus_eta", xlabel="#eta of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_selected_taus_phi"), "tauID5_TauSelection_selected_taus_phi", xlabel="#phi of selected taus", ylabel="N_{events}", rebinToWidthX=.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauSelection_selected_taus_MC_purity"), "tauID5_TauSelection_selected_taus_MC_purity", xlabel="MC purity of selected taus", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "FakeTauIdentifier_TauID"
    drawPlot(createPlot(myDir+"/TauMatchType"), "TauID6_SelectedTau_Fakes_TauMatchType", xlabel="MC #tau decay", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/TauOrigin"), "TauID6_SelectedTau_Fakes_TauOrigin", xlabel="MC #tau origin", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuOrigin"), "TauID6_SelectedTau_Fakes_MuOrigin", xlabel="MC #mu origin", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/ElectronOrigin"), "TauID6_SelectedTau_Fakes_ElectronOrigin", xlabel="MC e origin", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "SelectedTau"
    drawPlot(createPlot(myDir+"/SelectedTau_pT_AfterTauID"), "tauID7_SelectedTau_SelectedTau_pT_AfterTauID", xlabel="p_{T} of selected taus, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_eta_AfterTauID"), "tauID7_SelectedTau_SelectedTau_eta_AfterTauID", xlabel="#eta of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_phi_AfterTauID"), "tauID7_SelectedTau_SelectedTau_pT_phi_AfterTauID", xlabel="#phi of selected taus", ylabel="N_{events}", rebinToWidthX=.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_Rtau_AfterTauID"), "tauID7_SelectedTau_SelectedTau_Rtau_AfterTauID", xlabel="R_{#tau} of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_pT_AfterCuts"), "tauID8_SelectedTau_SelectedTau_pT_AfterTauID", xlabel="p_{T} of tau after selections, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_eta_AfterCuts"), "tauID8_SelectedTau_SelectedTau_eta_AfterTauID", xlabel="#eta of tau after selections", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/SelectedTau_Rtau_AfterCuts"), "tauID8_SelectedTau_SelectedTau_Rtau_AfterTauID", xlabel="R_{#tau} of tau after selections", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "ElectronSelection"
    drawPlot(createPlot(myDir+"/GlobalElectronPt"), "ElectronCandPt", xlabel="p_{T} of electron candidates, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/GlobalElectronEta"), "ElectronCandEta", xlabel="#eta of electron candidates", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/NumberOfSelectedElectrons"), "ElectronSelectedN", xlabel="Number of selected electrons", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/GlobalElectronPt_identified"), "ElectronSelectedPt", xlabel="p_{T} of selected electrons, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/GlobalElectronEta_identified"), "ElectronSelectedEta", xlabel="#eta of selected electrons", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "MuonSelection"
    drawPlot(createPlot(myDir+"/LooseMuonPt"), "MuonCandPt", xlabel="p_{T} of #mu candidates, GeV/c", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/LooseMuonEta"), "MuonCandEta", xlabel="#eta of #mu candidates", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuonTransverseImpactParameter"), "MuonIPT", xlabel="IP_{T} of #mu candidates, mm", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuonDeltaIPz"), "MuonDeltaIPz", xlabel="IP_{z} - PV_{z} of #mu candidates, cm", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuonRelIsol"), "MuonRelIsol", xlabel="#mu rel. isol.", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/NumberOfLooseMuons"), "NLooseMuons", xlabel="Number of loose #mus", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/NumberOfTightMuons"), "NTightMuons", xlabel="Number of tight #mus", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuonPt_BeforeIsolation"), "MuonPtBeforeIsolation", xlabel="#mu p_{T} before isolation, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MuonEta_BeforeIsolation"), "MuonEtaBeforeIsolation", xlabel="#mu #eta before isolation", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection"
    drawPlot(createPlot(myDir+"/jet_pt"), "JetCands_pt", xlabel="p_{T} of jet candidates, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_pt_central"), "JetCands_pt_central", xlabel="p_{T} of central jet candidates, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_eta"), "JetCands_eta", xlabel="#eta of jet candidates", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_phi"), "JetCands_phi", xlabel="#phi of jet candidates", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/firstJet_pt"), "JetSelected_1jet_pt", xlabel="p_{T} of first jet, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/firstJet_eta"), "JetSelected_1jet_eta", xlabel="#eta of first jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/firstJet_phi"), "JetSelected_1jet_phi", xlabel="#phi of first jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/secondJet_pt"), "JetSelected_2jet_pt", xlabel="p_{T} of second jet, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/secondJet_eta"), "JetSelected_2jet_eta", xlabel="#eta of second jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/secondJet_phi"), "JetSelected_2jet_phi", xlabel="#phi of second jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/thirdJet_pt"), "JetSelected_3jet_pt", xlabel="p_{T} of third jet, GeV/c", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/thirdJet_eta"), "JetSelected_3jet_eta", xlabel="#eta of third jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/thirdJet_phi"), "JetSelected_3jet_phi", xlabel="#phi of third jet", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/NumberOfSelectedJets"), "JetSelected_N", xlabel="N_{selected jets}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection/SelectedJets"
    drawPlot(createPlot(myDir+"/jet_pt"), "JetAccepted_pt", xlabel="p_{T} of accepted jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_eta"), "JetAccepted_eta", xlabel="#eta of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_phi"), "JetAccepted_phi", xlabel="#phi of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralEmEnergyFraction"), "JetAccepted_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralHadronFraction"), "JetAccepted_NeutralHadronFraction", xlabel="NeutralHadronFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PhotonEnergyFraction"), "JetAccepted_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_ChargedHadronEnergyFraction"), "JetAccepted_ChargedEnergyFraction", xlabel="ChargedEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralHadronMultiplicity"), "JetAccepted_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PhotonMultiplicity"), "JetAccepted_PhotonMultiplicity", xlabel="PhotonMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_ChargedMultiplicity"), "JetAccepted_ChargedMultiplicity", xlabel="ChargedMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PartonFlavour"), "JetAccepted_PartonFlavour", xlabel="PartonFlavour of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection/ExcludedJets"
    drawPlot(createPlot(myDir+"/jet_pt"), "JetRejected_pt", xlabel="p_{T} of rejected jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_eta"), "JetRejected_eta", xlabel="#eta of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_phi"), "JetRejected_phi", xlabel="#phi of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralEmEnergyFraction"), "JetRejected_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralHadronFraction"), "JetRejected_NeutralHadronFraction", xlabel="NeutralHadronFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PhotonEnergyFraction"), "JetRejected_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_ChargedHadronEnergyFraction"), "JetRejected_ChargedEnergyFraction", xlabel="ChargedEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_NeutralHadronMultiplicity"), "JetRejected_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PhotonMultiplicity"), "JetRejected_PhotonMultiplicity", xlabel="PhotonMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_ChargedMultiplicity"), "JetRejected_ChargedMultiplicity", xlabel="ChargedMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_PartonFlavour"), "JetRejected_PartonFlavour", xlabel="PartonFlavour of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "MET"
    drawPlot(createPlot(myDir+"/met"), "MET_MET", xlabel="MET, GeV", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/metPhi"), "MET_Phi", xlabel="MET #phi", ylabel="N_{events}", rebin=5, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/metSignif"), "MET_significance", xlabel="MET significance", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/metSumEt"), "MET_SumET", xlabel="MET #sum E_{T}, GeV", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "Btagging"
    drawPlot(createPlot(myDir+"/NumberOfBtaggedJets"), "Btag_N", xlabel="N_{selected b jets}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/jet_bdiscriminator"), "Btag_discriminator", xlabel="b-taggind discriminator", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/RealBjet_discrim"), "Btag_discriminator_genuine_bjets", xlabel="b-tagging discriminator for genuine b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet_pt"), "Btag_pt", xlabel="p_{T} of selected b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet_eta"), "Btag_eta", xlabel="#eta of selected b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet1_pt"), "Btag_2pt", xlabel="p_{T} of first b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet1_eta"), "Btag_2eta", xlabel="#eta of first b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet2_pt"), "Btag_2pt", xlabel="p_{T} of second b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/bjet2_eta"), "Btag_2eta", xlabel="#eta of second b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot(myDir+"/MCMatchForPassedJets"), "Btag_MCMatchForPassedJets", xlabel="MCMatchForPassedJets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    # main directory
    drawPlot(createPlot("deltaPhi"), "DeltaPhi_tauMET", xlabel="#Delta#phi(#tau jet, MET), ^{o}", ylabel="N_{events}", rebin=20, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("transverseMass"), "Mass_Transverse", xlabel="Transverse mass, GeV/c^{2}", ylabel="N_{events}", rebin=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("EWKFakeTausTransverseMass"), "Mass_Transverse_EWKFakeTaus", xlabel="Transverse mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("fullMass"), "Mass_Invariant", xlabel="Invariant mass, GeV/c^{2}", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("EWKFakeTausFullMass"), "Mass_Invariant_EWKFakeTaus", xlabel="Invariant mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("alphaT"), "AlphaT", xlabel="#alpha_{T}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("deltaPhiJetMet"), "DeltaPhi_minJetMET", xlabel="min #Delta#phi(jet, MET), ^{o}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("maxDeltaPhiJetMet"), "DeltaPhi_maxJetMET", xlabel="max #Delta#phi(#tau jet, MET), ^{o}", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("SignalSelectionFlow"), "SelectionFlow", xlabel="Step", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("SignalSelectionFlowVsVertices"), "SelectionFlow_vsVertices", xlabel="N_{vertices}", ylabel="Step", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    drawPlot(createPlot("SignalSelectionFlowVsVerticesFakeTaus"), "SelectionFlow_vsVerticesFakeTaus", xlabel="N_{vertices}", ylabel="Step", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    return
#        [["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts","signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts"], 10, "log"],
#        [["signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts","signalAnalysis/SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts"], 0.2, "log"],
    drawPlot(createPlot(myDir+"/"), "", xlabel="", ylabel="N_{events}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
   
    # Primary vertices

#    vertexCount(createPlot("verticesBeforeWeight", normalizeToOne=True), postfix="BeforeWeight")
#    vertexCount(createPlot("verticesAfterWeight", normalizeToOne=True), postfix="AfterWeight")
#    vertexCount(createPlot("Vertices/verticesTriggeredBeforeWeight", normalizeToOne=True), postfix="BeforeWeightTriggered")
#    vertexCount(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True), postfix="AfterWeightTriggered")
#    vertexCount(createPlot("SignalSelectionFlowVsVertices", normalizeToOne=True, datasetRootHistoArgs={"modify": lambda th2: pickSliceX(th2, "#tau ID")}), postfix="AfterTauIDScaleFactors")
#    vertexCount(createPlot("verticesTriggeredBeforeWeight", normalizeToOne=False), postfix="BeforeWeightTriggeredNorm")
#    vertexCount(createPlot("verticesTriggeredAfterWeight", normalizeToOne=False), postfix="AfterWeightTriggeredNorm")

#    met2(createPlot("MET"), "met1", rebin=50)
  
    # Tau
    tauPt(createPlot("SelectedTau/SelectedTau_pT_AfterTauID"), "SelectedTau_pT_AfterTauID", rebin=5, ratio=False, opts={"xmax": 300, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    tauEta(createPlot("SelectedTau/SelectedTau_eta_AfterTauID"),"SelectedTau_eta_AfterTauID", rebin=5, ratio=False, opts={"ymin": 1, "ymaxfactor": 50, "xmin": -2.5, "xmax": 2.5}, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.85))
 
#    tauPhi(createPlot("SelectedTau/SelectedTau_phi_AfterTauID"), "SelectedTau_phi_AfterTauID", rebin=10, opts={"ymin": 1, "ymaxfactor": 40})
    tauPt(createPlot("TauSelection/TauSelection_all_tau_candidates_pt"), "All_tau_candidates_pt", rebin=1, ratio=True,log=True, opts={"ymin": 10,"ymaxfactor": 1.1})
    tauEta(createPlot("TauSelection/TauSelection_all_tau_candidates_eta"), "All_tau_candidates_eta", rebin=1,  ratio=True, log=True, opts={"ymaxfactor": 5.0})
    
    drawPlot(createPlot("TauSelection/TauSelection_selected_taus_MC_purity"), "SelectedTausMCpurity",log=False,  xlabel="origin", ylabel="#tau jets", ratio=False, opts={"ymin": 10, "xmax": 6}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("TauSelection/TauSelection_all_tau_candidates_N"), "AllTauCandidates", log=False, xlabel="", ylabel="#tau candidates", ratio=False, opts={"xmax": 8}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("TauSelection/TauSelection_cleaned_tau_candidates_N"), "CleanedTauCandidates",  log=False, xlabel="", ylabel="#tau candidates", ratio=False, opts={ "xmax": 8}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("TauSelection/TauSelection_selected_taus_N"), "SelectedTaus", xlabel="", log=True,  ylabel="#tau jets", ratio=False, opts={ "xmax": 8}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
        
#    rtau(createPlot("SelectedTau/SelectedTau_Rtau_AfterTauID"), "SelectedTau_Rtau_AfterTauID", rebin=10, opts={"ymin": 1e-2, "ymaxfactor": 5, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.08}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
    rtau(createPlot("TauSelection/TauID_RtauCut"), "TauID_Rtau", rebin=1, ratio=False, opts={"ymin": 1e-2, "ymaxfactor": 50, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
     
#    rtau(createPlot("tauID/TauID_RtauCut"), "TauID_Rtau", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
    
    if False:
        rtau(createPlot("tauID/TauID_Rtau_DecayModeOneProng_ZeroPiZero"), "TauID_Rtau_DecayModeOneProng_ZeroPiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("tauID/TauID_Rtau_DecayModeOneProng_OnePiZero"), "TauID_Rtau_DecayModeOneProng_OnePiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("tauID/TauID_Rtau_DecayModeOneProng_TwoPiZero"), "TauID_Rtau_DecayModeOneProng_TwoPiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("tauID/TauID_Rtau_DecayModeOneProng_Other"), "TauID_Rtau_DecayModeOneProng_Other", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)

        
#    tauPt(createPlot("SelectedTau/SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=1, opts={"ymin": 1e-4})
#    tauEta(createPlot("SelectedTau/SelectedTau_eta_AfterCuts"),"SelectedTau_eta_AfterCuts", rebin=1)
#    rtau(createPlot("SelectedTau/SelectedTau_Rtau_AfterCuts"), "SelectedTau_Rtau_AfterCuts", rebin=10, opts={"ymin": 1e-2, "ymaxfactor": 5, "xmax": 1.1}, moveLegend={"dx": -0.5}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
    
#    leadingTrack(createPlot("TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
    
    selectionFlow(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, ratio=False)
#    selectionFlowTauCand(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, ratio=False)
#    selectionFlow(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, opts={"ymin": 1, "ymaxfactor": 5} ) 
    
#    leadingTrack(createPlot("SelectedTau/SelectedTau_TauLeadingTrackPt"),"SelectedTau_TauLeadingTrackPt", rebin=10)


   
#    rtau(createPlot("genRtau1ProngHp"), "genRtauTopMassWithChi.png1ProngHp")
#    rtau(createPlot("genRtau1ProngW"), "genRtau1ProngW")
   
#    tauCandPt(createPlot("TauSelection_all_tau_candidates_pt"), step="begin")
#    tauCandEta(createPlot("TauSelection_all_tau_candidates_eta"), step="begin" )
#    tauCandPhi(createPlot("TauSelection_all_tau_candidates_phi"), step="begin" )

    # Electron veto
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronPt_identified"), "electronPt", rebin=3, xlabel="p_{T}^{electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=False,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronEta_identified"), "electronEta", rebin=3, xlabel="#eta^{electron}", ylabel="Identified electrons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])

    drawPlot(createPlot("GlobalElectronVeto/NumberOfSelectedElectrons"), "NumberOfSelectedElectrons", xlabel="Number of selected electrons", ylabel="Events", ratio=False, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)
    
    # Muon veto
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonPt_identified_eta"), "muonPt", rebin=3, xlabel="p_{T}^{muon} (GeV/c)", ylabel="Identified muons / %.0f GeV/c", ratio=False, log=False, opts={"ymaxfactor": 2,"xmax": 250,"xmin": 0}, textFunction=lambda: addMassBRText(x=0.35, y=0.9), cutLine=15)
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonEta_identified"), "muonEta", rebin=3, xlabel="#eta^{muon}", ylabel="Identified muons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 20}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.30, y=0.87), cutLine=[-2.5, 2.5])
    drawPlot(createPlot("GlobalMuonVeto/NumberOfSelectedMuons"), "NumberOfSelectedMuons", xlabel="Number of selected muons", ylabel="Events", ratio=False, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)

    if False:
        # tau veto
        drawPlot(createPlot("TauVeto/TauSelection_selected_taus_pt"), "SelectedVetoTausPt", rebin=2, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
        drawPlot(createPlot("VetoTauSelection/SelectedFakeTauByPt"), "SelectedFakeVetoTauPt", rebin=2, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
        drawPlot(createPlot("VetoTauSelection/SelectedFakeTauByEta"), "SelectedFakeVetoTauEta", rebin=2, xlabel="#eta^{#tau jet}", ylabel="#tau jets / %.1f", opts={"ymaxfactor": 110}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])     
        drawPlot(createPlot("VetoTauSelection/SelectedGenuineTauByPt"), "SelectedGenuineVetoTauPt", rebin=2, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
        drawPlot(createPlot("VetoTauSelection/SelectedGenuineTauByEta"), "SelectedGenuineVetoTauEta", rebin=2, xlabel="#eta^{#tau jet}", ylabel="#tau jets / %.1f", opts={"ymaxfactor": 110}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])
        drawPlot(createPlot("VetoTauSelection/SelectedFakeTauDitauMass"), "SelectedFakeTauDitauMass", rebin=2, xlabel="m_{#tau#tau} (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87))
        drawPlot(createPlot("VetoTauSelection/SelectedGenuineTauDitauMass"), "SelectedGenuineTauDitauMass", rebin=2, xlabel="m_{#tau#tau} (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87))


        
    # Jet selection
    drawPlot(createPlot("JetSelection/jet_pt_central"), "centralJetPt", rebin=2, xlabel="p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", ratio=False, opts={"xmax": 500,"ymin": 0.1,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=30)
#    drawPlot(createPlot("JetSelection/jet_pt"), "jetPt", rebin=2, xlabel="p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", opts={"xmax": 500}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=30)
    drawPlot(createPlot("JetSelection/jet_eta"), "jetEta", rebin=2, xlabel="#eta^{jet}", ylabel="Jets / %.1f", ratio=False, opts={"xmin": -3.5, "xmax": 3.5, "ymaxfactor": 500}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])
##    drawPlot(createPlot("JetSelection/SelectedJets/deltaPtTauJet"), "deltaPtJetTau", rebin=3, log=True, xlabel="p_{T}^{jet}-p_{T}^{#tau jet}(GeV/c)", ylabel="Events / %.1f GeV/c", ratio=False, opts={"ymaxfactor": 2}, moveLegend={"dy":0.01, "dx":-0.5, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.2, y=0.52), cutLine=[-10.0, 10.0])
#    drawPlot(createPlot("JetSelection/jet_phi"), "jetPhi", rebin=1, xlabel="#phi^{jet}", ylabel="Jets / %.2f", opts={"ymin": 20},textFunction=lambda: addMassBRText(x=0.3, y=0.87))
    drawPlot(createPlot("ControlPlots/Njets"), "NumberOfJets", xlabel="Number of selected jets", ylabel="Events", ratio=False, opts={"xmax": 11,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=3)
    
    drawPlot(createPlot("JetSelection/betaGenuine"), "betaGenuine", rebin=5,xlabel="Beta", log=True, ylabel="Jets / %.0f GeV/c",  opts={"ymaxfactor": 2},  moveLegend={"dy":0.01, "dx":-0.5, "dh":-0.06},textFunction=lambda: addMassBRText(x=0.6, y=0.3), cutLine=30)
    drawPlot(createPlot("JetSelection/betaPU"), "betaPU", rebin=5,  xlabel="Beta", log=True, ylabel="Jets / %.0f GeV/c", opts={"ymaxfactor": 5},moveLegend={"dy":0.01, "dx":-0.5, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.6, y=0.25), cutLine=30)

        
    # MET
    drawPlot(createPlot("Met"), "Met", rebin=10, xlabel="Raw PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts={"xmin": 20, "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=40)
#    drawPlot(createPlot("ControlPlots/MET"), "Met", rebin=4, xlabel="PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", ratio=True, opts={"xmin": 0, "xmax": 500}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=60)
#    drawPlot(createPlot("MetWithBtagging"), "MetWithBtagging", rebin=10, xlabel="Raw PF E_{T}^{miss} (GeV)", ratio=True, ylabel="Events / %.0f GeV", opts={"xmin": 20, "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=40)
#    drawPlot(createPlot("Met_beforeJetCut"), "MetBeforeJets", rebin=10, xlabel="Raw PF E_{T}^{miss} (GeV)", ratio=True, ylabel="Events / %.0f GeV", opts={"xmin": 20, "xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))


    # b jets
    drawPlot(createPlot("Btagging/bjet_pt"), "bjetPt", rebin=4, xlabel="p_{T}^{b-tagged jet} (GeV/c)", ylabel="b-tagged jets / %.0f GeV/c", ratio=False, opts={"ymaxfactor": 2,"xmax": 500}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("Btagging/bjet_eta"), "bjetEta", rebin=2, xlabel="#eta^{b-tagged jet}", ylabel="b-tagged jets / %.1f", ratio=False, opts={"ymaxfactor": 20, "xmin": -2.4, "xmax": 2.59,"ymin": 0.1 }, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("ControlPlots/NBjets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 7}, ratio=False, textFunction=lambda: addMassBRText(x=0.45, y=0.87), cutLine=1)
#   

    if False:
        # top mass 
        drawPlot(createPlot("TopChiSelection/TopMass"), "TopMassWithChi", rebin=2, log=False, xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=300)
        
        drawPlot(createPlot("TopChiSelection/WMass"), "WMassWithChi", rebin=2, log=False, xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=50)
        
        drawPlot(createPlot("TopWithBSelection/TopMass"), "TopMassWithBsel", rebin=2, log=False,xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=250)
        drawPlot(createPlot("TopWithBSelection/WMass"), "WMassWithBsel", rebin=20, log=False,xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
        
        drawPlot(createPlot("TopWithMHSelection/TopMass"), "TopMassWithMHSel", rebin=2, log=False,xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))

    drawPlot(createPlot("genWmass"), "genWmass", rebin=5, log=True,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=False, opts={"xmax": 400,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))

    drawPlot(createPlot("FullHiggsMass/HiggsMass"), "HiggsMass", rebin=5, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=True, opts={"xmax": 400,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))
    drawPlot(createPlot("FullHiggsMass/HiggsMassReal"), "HiggsMassReal", rebin=5, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=False, opts={"xmax": 400,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))  
    drawPlot(createPlot("FullHiggsMass/HiggsMassImaginary"), "HiggsMassImaginary", rebin=5, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=False, opts={"xmax": 400,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))
    drawPlot(createPlot("FullHiggsMass/SolutionMinPzDifference"), "SolutionMinPzDifference", rebin=5, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=False, opts={"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))
    drawPlot(createPlot("FullHiggsMass/SolutionMaxPzDifference"), "SolutionMaxPzDifference", rebin=5, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", ratio=False, opts={"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))
      
#    drawPlot(createPlot("FullHiggsMass/HiggsMassTauBmatch"), "HiggsMassTauBmatch", rebin=2, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
#    drawPlot(createPlot("FullHiggsMass/HiggsMassTauBMETmatch"), "HiggsMassTauBMETmatch", rebin=2, log=False,xlabel="m_{Higgs} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))    
#    topMass(createPlot("TopChiSelection/TopMass"), "TopMassWithChi", rebin=10)   
    # Transverse mass
#    transverseMass(createPlot("TauEmbeddingAnalysis_afterTauId_TransverseMass"))
#    transverseMass2(createPlot("transverseMass"), "transverseMass_standard", rebin=10)
#    transverseMass2(createPlot("transverseMassMET70"), "transverseMassMET70", rebin=20)
#    transverseMass2(createPlot("NonQCDTypeIITransverseMassAfterDeltaPhi160"), "NonQCDTypeIITransverseMassAfterDeltaPhi160", rebin=20)    
#    transverseMass2(createPlot("transverseMassAfterDeltaPhi160"), "transverseMassAfterDeltaPhi160", rebin=20)
#    transverseMass2(createPlot("transverseMassAfterDeltaPhi130"), "transverseMassAfterDeltaPhi130", rebin=20)
#    transverseMass2(createPlot("transverseMassFakeMetVeto"), "transverseMassFakeMetVeto", rebin=20)

    transverseMass2(createPlot("transverseMass"), "transverseMass", rebin=10, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
##    transverseMass2(createPlot("transverseMassDeltaPtCut"), "transverseMassDeltaPtCut", rebin=10, ratio=True,log=False, opts={"xmax": 300,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))

#    transverseMass2(createPlot("transverseMassNoBtaggingWithRtau"), "transverseMassNoBtaggingWithRtau", rebin=10, ratio=True,log=False, opts={"xmax": 300,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))
###    transverseMass2(createPlot("transverseMassAfterDeltaPhi160"), "transverseMassAfterDeltaPhi160", rebin=20, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
#    transverseMass2(createPlot("transverseMassTopChiSelection"), "transverseMassTopChiSelection", rebin=10, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
###    transverseMass2(createPlot("transverseMassTopSelection"), "transverseMassTopSelection", rebin=20, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
##    transverseMass2(createPlot("transverseMassTopBjetSelection"), "transverseMassTopBjetSelection", rebin=20, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
###    transverseMass2(createPlot("transverseMassTauVeto"), "transverseMassWithTauVeto", rebin=20, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    
    if QCDfromData:
        plot = replaceQCDfromData(createPlot("transverseMass"), datasetsQCD, analysis+"/MTInvertedTauIdBtag")
        transverseMass2(plot, "transverseMass", rebin=20)


    # Delta phi
#    deltaPhi(createPlot("TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
    deltaPhi2(createPlot("deltaPhi"), "DeltaPhiTauMet", rebin=10, ratio=False, opts={"ymaxfactor": 50}, moveLegend={"dx":-0.21}, textFunction=lambda: addMassBRText(x=0.2, y=0.87), cutLine=[160])
#    deltaPhi2(createPlot("deltaPhiNoBtagging"), "DeltaPhiTauMetNoBtagging", rebin=10, ratio=True, opts={"ymaxfactor": 100}, moveLegend={"dx":-0.21}, textFunction=lambda: addMassBRText(x=0.2, y=0.87), cutLine=[160, 130])
#    deltaPhi2(createPlot("FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet", rebin=2, opts={"ymaxfactor": 20}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))


    # Set temporarily the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)
#    datasets.getDataset("TTToHplusBHminusB_M120").setCrossSection(0.2*165)
#    datasets.getDataset("TTToHplusBWB_M120").setCrossSection(0.2*165)


#    path = analysis+"/transverseMassWithRtauFakeMet"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassWithRtauFakeMet", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassWithRtauFakeMetQCDFromData", rebin=20)
    
#    path = analysis+"/transverseMassDeltaPhiUpperCut"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassDeltaPhiUpperCut", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassDeltaPhiUpperCutQCDFromData", rebin=20)


#    jetEMFraction(createPlot("JetSelection/jetMaxEMFraction"), "jetMaxEMFraction", rebin=10)
#    jetEMFraction(createPlot("JetSelection/jetEMFraction"), "jetEMFraction", rebin=20)
#    jetEMFraction(createPlot("JetSelection/chargedJetEMFraction"), "chargedJetEMFraction", rebin=20)
   
    
   
#    jetPt(createPlot("ForwardJetVeto/MaxForwJetEt"), "maxForwJetPt")

#    etSumRatio(createPlot("ForwardJetVeto/EtSumRatio"), "etSumRatio")
#    tauJetMass(createPlot("TauJetMass"), "TauJetMass")
#    topMass(createPlot("TopSelection/jjbMass"), "jjbMass")

#    topMass(createPlot("TopSelection/Mass_Top"), "topMass_realTop")
#    topMass(createPlot("TopSelection/Mass_bFromTop"), "topMass_bFromTop") 
#    ptTop(createPlot("TopSelection/Pt_jjb"), "pt_jjb")
#    ptTop(createPlot("TopSelection/Pt_jjbmax"), "ptTop")
#    ptTop(createPlot("TopSelection/Pt_top"), "ptTop_realTop")
#    met2(createPlot("MET_BaseLineTauId"), "MET_BaseLineTauId", rebin=10)
#    met2(createPlot("MET_InvertedTauId"), "MET_InvertedTauId", rebin=10)
#    met2(createPlot("MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)   
#    met2(createPlot("MET_BaseLineTauIdAllCuts"), "MET_BaseLineTauIdAllCuts", rebin=10)
#    met2(createPlot("MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)    
    
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
#    topMass(plots.DataMCPlot(datasets, treeDraw.clone(varexp="topreco_p4.M()>>dist(20,0,800)", selection=pasJuly)), "topMass", rebin=1)

    #met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="met_p4.Et()>>dist(20,0,400)")), "metRaw", rebin=1)
    #met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="metType1_p4.Et()>>dist(20,0,400)")), "metType1", rebin=1)

    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)

#    genComparison(datasets)
#    zMassComparison(datasets)
#    genQuarkComparison(datasets)
#    topMassComparison(datasets)
    
#    topMassPurity(datasets) 
#    vertexComparison(datasets)
#    mtComparison(datasets)
#    MetComparison(datasets)
#    BetaComparison(datasets)
#    HiggsMassComparison(datasets)
#    InvMassComparison(datasets)
#    rtauComparison(datasets)
    

def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
#    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default
#    cellFormat = counter.TableFormatText()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=False))
    print mainTable.format(cellFormat)



#    print eventCounter.getSubCounterTable("GlobalMuon_ID").format()

#    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
    print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("TauIDPassedJets::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    
    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MuonSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat) 
#    print eventCounter.getSubCounterTable("GlobalElectron ID").format(cellFormat)
    print eventCounter.getSubCounterTable("GlobalElectron Selection").format(cellFormat)  
#    print eventCounter.getSubCounterTable("top").format(cellFormat) 

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)


def vertexComparison(datasets):
    signal = "TTToHplusBWB_M120"
    background = "TTToHplusBWB_M120"
    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
            "vertices_H120")

def mtComparison(datasets):
    mt = plots.PlotBase([
#        datasets.getDataset("TTToHplusBWB_M150").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplusBWB_M90").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplusBWB_M100").getDatasetRootHisto(analysis+"/transverseMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/transverseMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/transverseMassTauVeto"),
#        datasets.getDataset("TTToHplusBWB_M140").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplusBWB_M150").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplusBWB_M155").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplusBWB_M160").getDatasetRootHisto(analysis+"/transverseMass"),
        ############ 
        datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/transverseMassNoBtagging"),
        datasets.getDataset("QCD").getDatasetRootHisto(analysis+"/transverseMassNoBtaggingWithRtau"),        
        ])
    
    #   plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section MUST BE OFF
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("TTToHplus_M150", st1)
    mt.histoMgr.forHisto("TTToHplus_M120", st2)
    mt.histoMgr.forHisto("TTToHplus_M160", st3)
#    mt.histoMgr.setHistoDrawStyleAll("P")
#    rtauGen(mt, "transverseMass_vs_mH", rebin=20, defaultStyles=False)
    rtauGen(mt, "transverseMassTauVeto", rebin=5, defaultStyles=False)
    rtauGen(mt, "transverseRtau", rebin=5, ratio=True, defaultStyles=False)

    
def MetComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/Met"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MetWithBtagging")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt.histoMgr.normalizeToOne()
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("Met", st1)
    mt.histoMgr.forHisto("MetWithBtagging", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "Met"
#    mt.createFrameFraction(name, opts=opts, opts2=opts2)

    rtauGen(mt, "MetComparison", rebin=2, defaultStyles=False)


def BetaComparison(datasets):
    if mcOnly:
        return

    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/JetSelection/betaGenuine"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/JetSelection/betaPU"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/JetSelection/betaPU")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
#    mt.histoMgr.forHisto("betaGenuine", st1)
#    mt.histoMgr.forHisto("betaPU", st2)
    mt.histoMgr.forHisto(datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/JetSelection/betaGenuine"), st1)
    mt.histoMgr.forHisto(datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/JetSelection/betaPU"), st2)
    mt.histoMgr.forHisto(datasets.getDataset("Data").getDatasetRootHisto(analysis+"/JetSelection/betaPU"), st3) 
    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "BetaComparison_H120", rebin=5, defaultStyles=False)

    
def HiggsMassComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M80").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M160").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMass")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))

    mt.histoMgr.forHisto("TTToHplusBWB_M80", st1)
    mt.histoMgr.forHisto("TTToHplusBWB_M120", st2)
    mt.histoMgr.forHisto("TTToHplusBWB_M160", st3) 
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "HiggsMassVsMass", rebin=2, defaultStyles=False)

def InvMassComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMassTauBmatch"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMassTauBMETmatch")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("HiggsMass", st1)
    mt.histoMgr.forHisto("HiggsMassTauBmatch", st2)
    mt.histoMgr.forHisto("HiggsMassTauBMETmatch", st3)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "HiggsMass_matching", rebin=2, defaultStyles=False)

    
def rtauComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/tauID/TauID_Rtau_DecayModeOneProng_ZeroPiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/tauID/TauID_Rtau_DecayModeOneProng_OnePiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/tauID/TauID_Rtau_DecayModeOneProng_TwoPiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/tauID/TauID_Rtau_DecayModeOneProng_Other")])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("TTToHplus_M80", st1)
    mt.histoMgr.forHisto("TTToHplus_M120", st2)
    mt.histoMgr.forHisto("TTToHplus_M160", st3)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "rtau_vs_DecayModes", rebin=1, defaultStyles=False)



def topMassComparison(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+path)
        drh.setName(name)
        return drh
    
    top = plots.PlotBase([
        createHisto("/TopSelection/TopMass", "Max(p_{T}^{jjb}) method"),
        createHisto("/TopChiSelection/TopMass", "Min(#chi^{2}) method"),
        createHisto("/TopWithBSelection/TopMass", "Min(#chi^{2}) with b-jet sel.")]) 
    top.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    top._setLegendStyles()
    top._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    top.histoMgr.forHisto("Max(p_{T}^{jjb}) method", st3)
    top.histoMgr.forHisto("Min(#chi^{2}) method", st1)
    top.histoMgr.forHisto("Min(#chi^{2}) with b-jet sel.", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")

    rtauGen(top, "topMass120", rebin=10, defaultStyles=False)

def topMassPurity(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+path)
        drh.setName(name)
        return drh
    
    top = plots.PlotBase([
        createHisto("/TopChiSelection/TopMass", "All combinations"),
        createHisto("/TopChiSelection/TopMass_fullMatch", "Matched jets"),
        createHisto("/TopChiSelection/TopMass_bMatch", "Matched b jet")]) 
    top.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    top._setLegendStyles()
    top._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    top.histoMgr.forHisto("All combinations", st3)
    top.histoMgr.forHisto("Matched jets", st1)
    top.histoMgr.forHisto("Matched b jet", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    histograms.addText(0.35, 0.5, "Normalized to unit area", 17)
    rtauGen(top, "topMassPurity", rebin=10, defaultStyles=False)

    
def genQuarkComparison(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+path)
        drh.setName(name)
        return drh
    
    quark = plots.PlotBase([
        createHisto("/BjetSelection/PtBquarkFromTopSide", "b quark from top side"),
        createHisto("/BjetSelection/PtQquarkFromTopSide", "q quark from top"),]) 
    quark.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    quark._setLegendStyles()
    quark._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    quark.histoMgr.forHisto("b quark from top side", st3)
    quark.histoMgr.forHisto("q quark from top", st1)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(quark, "ptQuarks", rebin=3, defaultStyles=False)

    
##############def genComparison(datasets):
#    rtau = plots.PlotBase([
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngHp"),
#        datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngW")
#        ])
#    rtau.histoMgr.normalizeToOne()
#    rtau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    rtau._setLegendStyles()
#    rtau._setLegendLabels()
#    st1 = styles.getDataStyle().clone()
#    st2 = st1.clone()
#    st2.append(styles.StyleLine(lineColor=ROOT.kRed))
#    rtau.histoMgr.forHisto(datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngHp"), st1)
#    rtau.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngW"), st2)
    
#    rtau.histoMgr.setHistoDrawStyleAll("P")
################    rtauGen(rtau, "RtauGenerated", rebin=1)


    
#def genComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTJets_TuneZ2"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/genRtau1ProngHp"),
#                                 datasets.getDataset(bagkground).getDatasetRootHisto(analysis+"/genRtau1ProngW")),
#          "RtauGen_Hp_vs_tt")

    
#def zMassComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "DYJetsToLL"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/TauJetMass"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/TauJetMass")),
#            "TauJetMass_Hp_vs_Zll")
    

#def topPtComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTToHplusBWB_M120"
#    rtauGen(plots.PlotBase([datasets.getDataset(signal).getDatasetRootHisto(analysis+"/TopSelection/Pt_jjb"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/TopSelection/Pt_jjbmax"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/TopSelection/Pt_top")]),
#             "topPt_all_vs_real")

def scaleMC(histo, scale):
    if histo.isMC():
        th1 = histo.getRootHisto()
        th1.Scale(scale)

def scaleMCHistos(h, scale):
    h.histoMgr.forEachHisto(lambda histo: scaleMC(histo, scale))

def scaleMCfromWmunu(h):
    # Data/MC scale factor from AN 2011/053
#    scaleMCHistos(h, 1.736)
    scaleMCHistos(h, 1.0)

def replaceQCDfromData(plot, datasetsQCD, path):
#    normalization = 0.00606 * 0.86
    normalization = 0.025
    drh = datasetsQCD.getDatasetRootHistos(path)
    if len(drh) != 1:
        raise Exception("There should only one DatasetRootHisto, got %d", len(drh))
    histo = histograms.HistoWithDatasetFakeMC(drh[0].getDataset(), drh[0].getHistogram(), drh[0].getName())
    histo.getRootHisto().Scale(normalization)
    plot.histoMgr.replaceHisto("QCD", histo)
    return plot

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    tmp = name.split("_")
    return tmp[-1] + "_" + tmp[-2]

# Common drawing function
def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, rebinToWidthX=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin or rebinToWidthX > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()


    scaleMCfromWmunu(h)     
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
    histograms.addCmsPreliminaryText()
    h.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    if textFunction != None:
        textFunction()
    h.save()

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.

def vertexCount(h, prefix="", postfix="", ratio=True):
        xlabel = "Number of good vertices"
        ylabel = "Number of events"

        if h.normalizeToOne:
            ylabel = "Arbitrary units."

        h.stackMCHistograms()

        stack = h.histoMgr.getHisto("StackedMC")
        #hsum = stack.getSumRootHisto()
        #total = hsum.Integral(0, hsum.GetNbinsX()+1)
        #for rh in stack.getAllRootHistos():
        #    dataset._normalizeToFactor(rh, 1/total)
        #dataset._normalizeToOne(h.histoMgr.getHisto("Data").getRootHisto())

        h.addMCUncertainty()


        opts = {"xmax": 40}
        opts_log = {"ymin": 1e-10, "ymaxfactor": 10, "xmax": 40}
        opts_log.update(opts)

        opts2 = {"ymin": 0, "ymax": 3}
        opts2_log = opts2
        #opts2_log = {"ymin": 5e-2, "ymax": 5e2}
        
        h.createFrame(prefix+"vertices"+postfix, opts=opts, createRatio=False, opts2=opts2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        h.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        else:
            h.histoMgr.addLuminosityText()
        h.save()

        h.createFrame(prefix+"vertices"+postfix+"_log", opts=opts_log, createRatio=ratio, opts2=opts2_log)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.getPad().SetLogy(True)
        #h.getPad2().SetLogy(True)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        h.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        else:
            h.histoMgr.addLuminosityText()
        h.save()

def rtauGen(h, name, rebin=2, ratio=False, defaultStyles=True):
    if defaultStyles:
        h.setDefaultStyles()
        h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    
    xlabel = "p^{leading track} / p^{#tau jet}"
    xlabel = "#beta^{jet}"
    ylabel = "Events / %.2f" % h.binWidth()
    if "Mass" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
#        xlabel = "m (GeV/c^{2})"
    if "HiggsMass" in name:
        xlabel = "m_{H^{#pm}} (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
#        xlabel = "m (GeV/c^{2})"
    if "topMass" in name:
        xlabel = "m_{top} (GeV/c^{2})"
    if "vertex" in name:
        xlabel = "Raw PF E_{T}^{miss} (GeV)"
    if "Quark" in name:
        xlabel = "p_{T} (GeV)"
    if "Beta" in name:
        xlabel = "#beta^{jet}"
    if "Rtau" in name:
        ylabel = "A.u."
    elif "Pt" in name:
        xlabel = "p_{T}(GeV/c)"
    elif "vertices" in name:
        xlabel = "N_{vertices}"


        
    kwargs = {"ymin": 0.1, "xmax": 1.0}

  
    if "Rtau" in name:
        kwargs = {"ymin": 0.0001, "xmax": 1.1}   
        kwargs = {"ymin": 0.1, "xmax": 1.1}     
        h.getPad().SetLogy(True)
    elif "Pt" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
        h.getPad().SetLogy(True)
    elif "Mass" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
    elif "DecayMode" in name:
        kwargs = {"ymin": 0.1, "xmax": 1.1}
    elif "Beta" in name:
        kwargs = {"ymin": 0.01, "xmax": 1.0}     
#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"

    h.createFrame(name, **kwargs)

#    histograms.addText(0.65, 0.7, "BR(t #rightarrow bH^{#pm})=0.05", 20)
#    h.getPad().SetLogy(True)
    

    h.getPad().SetLogy(True)
    if "Mass" in name:
        h.getPad().SetLogy(False)
    if "Quark" in name:
        h.getPad().SetLogy(False)
    leg = histograms.createLegend(0.6, 0.75, 0.8, 0.9)
    if "topMass" in name:
        leg = histograms.moveLegend(leg, dx=0.2)
    h.setLegend(leg)
    
    if  "vertex" in name:
        histograms.addText(0.75, 0.9, "Data", 22) 
        plots._legendLabels["Data"] = "vertex3"

    common(h, xlabel, ylabel, addLuminosityText=False)

    

def selectionFlow(h, name, rebin=1, ratio=False):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"
    
    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    
    h.addMCUncertainty()



    njets = 5
    lastSelection = njets
    
    
    opts = {"xmax": lastSelection, "ymin": 0.1, "ymaxfactor": 20, "nbins": lastSelection}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "Trigger")
    xaxis.SetBinLabel(2, "#tau ID+R_{#tau}")
    xaxis.SetBinLabel(3, "e veto")
    xaxis.SetBinLabel(4, "#mu veto")
    xaxis.SetBinLabel(5, "N_{jets}")
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    h.addEnergyText()
    h.addLuminosityText()
    addMassBRText(x=0.4, y=0.87)
    h.save()
    
def selectionFlowTauCand(h, name, rebin=1, ratio=True):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"
    
    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    
    h.addMCUncertainty()


    
    deltaphi = 8
    lastSelection = deltaphi
    
    opts = {"xmax": lastSelection, "ymin": 1.0, "ymaxfactor": 20, "nbins": lastSelection}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "Trigger")
    xaxis.SetBinLabel(2, "#tau candidate")
    xaxis.SetBinLabel(3, "e veto")
    xaxis.SetBinLabel(4, "#mu veto")
    xaxis.SetBinLabel(5, "N_{jets}")
    xaxis.SetBinLabel(6, "MET")
    xaxis.SetBinLabel(7, "b tagging")
    xaxis.SetBinLabel(8, "#Delta#phi")
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    addMassBRText(x=0.4, y=0.87)
    h.save()    

def tauCandPt(h, step="", rebin=2):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = "Events /%.0f GeV/c" % h.binWidth()   
    xlabel = "p_{T}^{#tau candidate} (GeV/c)"
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           

    name = "tauCandidatePt_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    h.addEnergyText()
    #h.addLuminosityText()
    h.save()
    
def tauCandEta(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           
#    opts = {"xmax": 2.5,"xmin":-2.5}
#    opts["xmin"] = -2.7
#    opts["xmax"] =  2.7    
    name = "tauCandidateEta_%s_log" % step
#    h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend(0.5, 0.2, 0.7, 0.5))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    h.addEnergyText()
    #h.addLuminosityText()
    h.save()

def tauCandPhi(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.01
           

    name = "tauCandidatePhi_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    h.addEnergyText()
    #h.addLuminosityText()
    h.save()
    


def tauPt(h, name, **kwargs):
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    drawPlot(h, name, xlabel, **kwargs)

def tauEta(h, name, **kwargs):
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
    
def tauPhi(h, name, **kwargs):
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
    
def leadingTrack(h, name, rebin=5, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{leading track} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.001,"xmin": 10.0, "ymaxfactor": 5}
    name = "leadingTrackPt"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.93))
    common(h, xlabel, ylabel)

def rtau(h, name, **kwargs):
    xlabel = "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}"
    ylabel = "Events / %.2f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

def met(h, rebin=20, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    
    ylabel = "Events / %.0f GeV" % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "MET"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)


    
def met2(h, name, rebin=10, ratio=True):
#    name = h.getRootHistoPath()
#    name = "met"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    ylabel = "Events / %.0f GeV" % h.binWidth()
    xlabel = "E_{T}^{miss} (GeV)"
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.0, "ymax": 2.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.93))
    common(h, xlabel, ylabel)



def deltaPhi(h, rebin=40, ratio=False):
    name = flipName(h.getRootHistoPath())

    particle = "#tau jet"
    if "Original" in name:
        particle = "#mu"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(%s, MET) (rad)" % particle
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    #h.createFrameFraction(name)
    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)
    
def deltaPhi2(h, name, **kwargs):
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss})^{#circ}"
    ylabel = "Events / %.0f^{#circ}"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

def transverseMass(h, rebin=20):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "Mt")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "Mt")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)     
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()

    opts = {"xmax": 200}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def transverseMass2(h, name, **kwargs):
    xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})" 
    ylabel = "Events / %.0f GeV/c^{2}"

    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
       
def jetPt(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    opts = {"ymin": 0.001,"xmax": 500.0, "ymaxfactor": 2}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
        opts["xmax"] = 400
    if "muon" in name:
        particle = "muon"
        opts["xmax"] = 400
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
#    xlabel = "p_{T}^{muon} (GeV/c)" 
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()


    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.6, 0.65, 0.9, 0.92))
    common(h, xlabel, ylabel)

    
def jetEta(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
    if "muon" in name:
        particle = "muon"
    xlabel = "#eta^{%s}" % particle
#    xlabel = "#eta^{muon}"
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01,"xmin": -5,"xmax": 5, "ymaxfactor": 10}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.7, 0.9, 0.95))
#    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def jetPhi(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#phi^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.2, 0.9, 0.5))
    common(h, xlabel, ylabel)
    
def jetEMFraction(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "EMfraction in jets" 
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.6, 0.6, 0.9, 0.92))
    common(h, xlabel, ylabel)
    
def numberOfJets(h, name, rebin=1, ratio=False):
    opts = {"ymin": 0.01,"xmax": 10.0, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.05, "ymax": 1.5}

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "BJets" in name:
        particle = "b jet"
        opts["xmax"] = 6
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.92))
    common(h, xlabel, ylabel)


def etSumRatio(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def tauJetMass(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 1.5}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)



def topMass(h, name, rebin=20, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "m_{top} (GeV/c^{2})"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def ptTop(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{top} (GeV/c)"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "xmax": 500, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)   

class AddMassBRText:
    def __init__(self):
        self.mass = 120
        self.br = 0.01
        self.size = 20
        self.separation = 0.04

    def setMass(self, mass):
        self.mass = mass

    def setBR(self, br):
        self.br = br

    def __call__(self, x, y):
        mass = "m_{H^{#pm}} = %d GeV/c^{2}" % self.mass
        br = "BR(t #rightarrow bH^{#pm})=%.2f" % self.br

        histograms.addText(x, y, mass, size=self.size)
        histograms.addText(x, y-self.separation, br, size=self.size)

addMassBRText = AddMassBRText()
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
