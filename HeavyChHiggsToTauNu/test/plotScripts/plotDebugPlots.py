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

from optparse import OptionParser

# Configuration
#analysis = "signalOptimisation"TauID_Rtau.png
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"

#treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False

removeQCD = False

optionBr = 0.01

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

# main function
def main(opts,era):
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(dataEra=era)
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()




    datasets.updateNAllEventsToPUWeighted()

    # Take QCD from data
    if opts.noMCQCD:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    # Remove signal
    if opts.noSignal:
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "Hplus_taunu" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

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
    if not opts.noSignal:
        print "norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    # Remove signals other than M120
#    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "QCD_Pt20_MuEnriched" in name, datasets.getAllDatasetNames()))
    
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
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
        print "Creating plot:",name
        if mcOnly:
            # If 'normalizeToOne' is given in kwargs, we don't need the normalizeToLumi (or actually the library raises an Exception)
            args = {}
            args.update(kwargs)
            if not ("normalizeToOne" in args and args["normalizeToOne"]):
                args["normalizeToLumi"] = mcOnlyLumi
            #return plots.MCPlot(datasets, analysis+"/"+name, **args)
            return plots.MCPlot(datasets, name, **args)
        else:
            return plots.DataMCPlot(datasets, name, **kwargs)
            #return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)

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
    myDrawer = plots.PlotDrawer(ylabel="N_{events}", log=True, ratio=True, ratioYlabel="Data/MC", stackMCHistograms=True, addMCUncertainty=True)
    
    # Common plots
    myCommonPlotDirs = ["VertexSelection","TauSelection","TauWeight","ElectronVeto","MuonVeto","JetSelection","MET","BTagging","Selected","FakeTaus_BTagging","FakeTaus_Selected"]
    for item in myCommonPlotDirs:
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/nVertices"%item), "CommonPlot_EveryStep_nVertices_%s"%item, xlabel="N_{Vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/tau_fakeStatus"%item), "CommonPlot_EveryStep_tau_fakeStatus_%s"%item, xlabel="Fake tau status", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/tau_pT"%item), "CommonPlot_EveryStep_tau_pT_%s"%item, xlabel="#tau p_{T}, GeV/c", ylabel="N_{events}", log=True, rebinToWidthX=10, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/tau_eta"%item), "CommonPlot_EveryStep_tau_eta_%s"%item, xlabel="#tau #eta", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/tau_phi"%item), "CommonPlot_EveryStep_tau_phi_%s"%item, xlabel="#tau #phi", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/tau_Rtau"%item), "CommonPlot_EveryStep_tau_Rtau_%s"%item, xlabel="R_{#tau}", ylabel="N_{events}", log=True, rebinToWidthX=0.5, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/electrons_N"%item), "CommonPlot_EveryStep_electrons_N_%s"%item, xlabel="N_{electrons}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/muons_N"%item), "CommonPlot_EveryStep_muons_N_%s"%item, xlabel="N_{muons}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/jets_N"%item), "CommonPlot_EveryStep_jets_N_%s"%item, xlabel="N_{jets}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/jets_N_allIdentified"%item), "CommonPlot_EveryStep_jets_N_allIdentified_%s"%item, xlabel="N_{all identified jets}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        #myDrawer(createPlot("CommonPlots/AtEveryStep/%s/MET_Raw"%item), "CommonPlot_EveryStep_MET_Raw_%s"%item, xlabel="Raw MET, GeV", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/MET_MET"%item), "CommonPlot_EveryStep_MET_MET_%s"%item, xlabel="MET, GeV", ylabel="N_{events}", rebinToWidthX=20, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/MET_phi"%item), "CommonPlot_EveryStep_MET_phi_%s"%item, xlabel="MET #phi", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/bjets_N"%item), "CommonPlot_EveryStep_bjets_N_%s"%item, xlabel="N_{b jets}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/DeltaPhi_TauMET"%item), "CommonPlot_EveryStep_DeltaPhi_TauMET_%s"%item, xlabel="#Delta#phi(#tau,MET)", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet1MET"%item), "CommonPlot_EveryStep_DeltaR_TauMETJet1MET_%s"%item, xlabel="#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{1})^{2})", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet2MET"%item), "CommonPlot_EveryStep_DeltaR_TauMETJet2MET_%s"%item, xlabel="#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{2})^{2})", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet3MET"%item), "CommonPlot_EveryStep_DeltaR_TauMETJet3MET_%s"%item, xlabel="#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{3})^{2})", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet4MET"%item), "CommonPlot_EveryStep_DeltaR_TauMETJet4MET_%s"%item, xlabel="#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{4})^{2})", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        myDrawer(createPlot("CommonPlots/AtEveryStep/%s/transverseMass"%item), "CommonPlot_EveryStep_transverseMass_%s"%item, xlabel="m_{T}(#tau,MET)", ylabel="N_{events}", rebinToWidthX=20, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))

    myDir = "Vertices"
    myDrawer(createPlot(myDir+"/verticesBeforeWeight"), "verticesBeforeWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22)) 
    myDrawer(createPlot(myDir+"/verticesBeforeWeight"), "verticesBeforeWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/verticesAfterWeight"), "verticesAfterWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/verticesTriggeredBeforeWeight"), "verticesTriggeredBeforeWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/verticesTriggeredAfterWeight"), "verticesTriggeredAfterWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "TauSelection"
    myDrawer(createPlot(myDir+"/N_TriggerMatchedTaus"), "tauID0_N_TriggerMatchedTaus", xlabel="N_{trg. matched taus}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/N_TriggerMatchedSeparateTaus"), "tauID0_N_TriggerMatchedSeparateTaus", xlabel="N_{trg. matched separate taus}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauCand_DecayModeFinding"), "tauID0_HPSDecayMode", xlabel="HPS Decay Mode", opts={"xmax": 15}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_all_tau_candidates_N"), "tauID1_TauSelection_all_tau_candidates_N", xlabel="N_{tau candidates}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_all_tau_candidates_pt"), "tauID1_TauSelection_all_tau_candidates_pt", xlabel="p_{T} of all tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_all_tau_candidates_eta"), "tauID1_TauSelection_all_tau_candidates_eta", xlabel="#eta of all tau candiates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_all_tau_candidates_phi"), "tauID1_TauSelection_all_tau_candidates_phi", xlabel="#phi of all tau candidates", ylabel="N_{events}",  rebinToWidthX=0.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_all_tau_candidates_MC_purity"), "tauID1_TauSelection_all_tau_candidates_MC_purity", xlabel="MC purity of all tau candidates", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauCand_JetPt"), "tauID2_TauCand_JetPt", xlabel="p_{T} of tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauCand_JetEta"), "tauID2_TauCand_JetEta", xlabel="#eta of tau candidates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauCand_LdgTrackPtCut"), "tauID2_TauCand_LdgTrackPtCut", xlabel="p_{T}^{ldg.ch.particle} of tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    #myDrawer(createPlot(myDir+"/TauCand_EMFractionCut"), "tauID2_TauCand_EMFractionCut", xlabel="EM energy fraction of tau candidates", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_N"), "tauID3_TauSelection_cleaned_tau_candidates_N", xlabel="N_{cleaned tau candidates}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_pt"), "tauID3_TauSelection_cleaned_tau_candidates_pt", xlabel="p_{T} of cleaned tau candidates, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_eta"), "tauID3_TauSelection_cleaned_tau_candidates_eta", xlabel="#eta of cleaned tau candidates", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_phi"), "tauID3_TauSelection_cleaned_tau_candidates_phi", xlabel="#phi of cleaned tau candidates", ylabel="N_{events}", rebinToWidthX=0.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_cleaned_tau_candidates_MC_purity"), "tauID3_TauSelection_cleaned_tau_candidates_MC_purity", xlabel="MC purity of cleaned tau candidates", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/IsolationPFChargedHadrCandsPtSum"), "tauID4_IsolationPFChargedHadrCandsPtSum", xlabel="#sum p_{T} of PF ch. hadr. candidates, GeV/c", opts={"xmax": 40}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/IsolationPFGammaCandEtSum"), "tauID4_IsolationPFGammaCandEtSum", xlabel="#sum p_{T} of PF gamma candidates, GeV/c", opts={"xmax": 40}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauID_NProngsCut"), "tauID4_TauID_NProngsCut", xlabel="N_{prongs}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    #myDrawer(createPlot(myDir+"/TauID_ChargeCut"), "tauID4_TauID_ChargeCut", xlabel="Q_{tau}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauID_RtauCut"), "tauID4_TauID_RtauCut", xlabel="R_{#tau}", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_selected_taus_N"), "tauID5_TauSelection_selected_taus_N", xlabel="N_{selected taus}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_selected_taus_pt"), "tauID5_TauSelection_selected_taus_pt", xlabel="p_{T} of selected taus", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_selected_taus_eta"), "tauID5_TauSelection_selected_taus_eta", xlabel="#eta of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_selected_taus_phi"), "tauID5_TauSelection_selected_taus_phi", xlabel="#phi of selected taus", ylabel="N_{events}", rebinToWidthX=.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection_selected_taus_MC_purity"), "tauID5_TauSelection_selected_taus_MC_purity", xlabel="MC purity of selected taus", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "FakeTauIdentifier_TauID"
    myDrawer(createPlot(myDir+"/TauMatchType"), "TauID6_SelectedTau_Fakes_TauMatchType", xlabel="MC #tau decay", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauOrigin"), "TauID6_SelectedTau_Fakes_TauOrigin", xlabel="MC #tau origin", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuOrigin"), "TauID6_SelectedTau_Fakes_MuOrigin", xlabel="MC #mu origin", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/ElectronOrigin"), "TauID6_SelectedTau_Fakes_ElectronOrigin", xlabel="MC e origin", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "SelectedTau"
    myDrawer(createPlot(myDir+"/SelectedTau_pT_AfterTauID"), "tauID7_SelectedTau_SelectedTau_pT_AfterTauID", xlabel="p_{T} of selected taus, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_eta_AfterTauID"), "tauID7_SelectedTau_SelectedTau_eta_AfterTauID", xlabel="#eta of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_phi_AfterTauID"), "tauID7_SelectedTau_SelectedTau_pT_phi_AfterTauID", xlabel="#phi of selected taus", ylabel="N_{events}", rebinToWidthX=.087266, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_Rtau_AfterTauID"), "tauID7_SelectedTau_SelectedTau_Rtau_AfterTauID", xlabel="R_{#tau} of selected taus", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_pT_AfterCuts"), "tauID8_SelectedTau_SelectedTau_pT_AfterTauID", xlabel="p_{T} of tau after selections, GeV/c", ylabel="N_{events}", rebinToWidthX=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_eta_AfterCuts"), "tauID8_SelectedTau_SelectedTau_eta_AfterTauID", xlabel="#eta of tau after selections", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/SelectedTau_Rtau_AfterCuts"), "tauID8_SelectedTau_SelectedTau_Rtau_AfterTauID", xlabel="R_{#tau} of tau after selections", ylabel="N_{events}", rebinToWidthX=0.1, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "ElectronSelection"
    myDrawer(createPlot(myDir+"/ElectronPt_all"), "electronCandPt", xlabel="p_{T} of electron candidates, GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/ElectronEta_all"), "electronCandEta", xlabel="#eta of electron candidates", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/ElectronPt_veto"), "electronPt_veto", xlabel="p_{T}^{veto electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=True,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
    myDrawer(createPlot(myDir+"/ElectronEta_veto"), "electronEta_veto", xlabel="#eta^{veto electron}", ylabel="Identified electrons / %.1f", ratio=True, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])
    myDrawer(createPlot(myDir+"/NumberOfVetoElectrons"), "electronN_veto", xlabel="Number of selected veto electrons", ylabel="Events", ratio=True, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)
    myDrawer(createPlot(myDir+"/ElectronPt_tight"), "electronPt_tight", xlabel="p_{T}^{tight electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=True,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
    myDrawer(createPlot(myDir+"/ElectronEta_tight"), "electronEta_tight", xlabel="#eta^{tight electron}", ylabel="Identified electrons / %.1f", ratio=True, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])
    myDrawer(createPlot(myDir+"/NumberOfTightElectrons"), "electronN_tight", xlabel="Number of selected tight electrons", ylabel="Events", ratio=True, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)
    myDir = "MuonSelection"
    myDrawer(createPlot(myDir+"/LooseMuonPt"), "MuonCandPt", xlabel="p_{T} of #mu candidates, GeV/c", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/LooseMuonEta"), "MuonCandEta", xlabel="#eta of #mu candidates", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonTransverseImpactParameter"), "MuonIPT", xlabel="IP_{T} of #mu candidates, mm", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonDeltaIPz"), "MuonDeltaIPz", xlabel="IP_{z} - PV_{z} of #mu candidates, cm", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonRelIsol"), "MuonRelIsol", xlabel="#mu rel. isol.", ylabel="N_{muons}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/NumberOfLooseMuons"), "Muon_NLooseMuons", xlabel="Number of loose #mus", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/NumberOfTightMuons"), "Muon_NTightMuons", xlabel="Number of tight #mus", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonPt_BeforeIsolation"), "MuonPtBeforeIsolation", xlabel="#mu p_{T} before isolation, GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonEta_BeforeIsolation"), "MuonEtaBeforeIsolation", xlabel="#mu #eta before isolation", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection"
    myDrawer(createPlot(myDir+"/jet_pt"), "JetCands_pt", xlabel="p_{T} of jet candidates, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_pt_central"), "JetCands_pt_central", xlabel="p_{T} of central jet candidates, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_eta"), "JetCands_eta", xlabel="#eta of jet candidates", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_phi"), "JetCands_phi", xlabel="#phi of jet candidates", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/firstJet_pt"), "JetSelected_1jet_pt", xlabel="p_{T} of first jet, GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/firstJet_eta"), "JetSelected_1jet_eta", xlabel="#eta of first jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/firstJet_phi"), "JetSelected_1jet_phi", xlabel="#phi of first jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/secondJet_pt"), "JetSelected_2jet_pt", xlabel="p_{T} of second jet, GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/secondJet_eta"), "JetSelected_2jet_eta", xlabel="#eta of second jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/secondJet_phi"), "JetSelected_2jet_phi", xlabel="#phi of second jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/thirdJet_pt"), "JetSelected_3jet_pt", xlabel="p_{T} of third jet, GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/thirdJet_eta"), "JetSelected_3jet_eta", xlabel="#eta of third jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/thirdJet_phi"), "JetSelected_3jet_phi", xlabel="#phi of third jet", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/NumberOfSelectedJets"), "JetSelected_N", xlabel="N_{selected jets}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection/SelectedJets"
    myDrawer(createPlot(myDir+"/jet_pt"), "JetAccepted_pt", xlabel="p_{T} of accepted jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_eta"), "JetAccepted_eta", xlabel="#eta of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_phi"), "JetAccepted_phi", xlabel="#phi of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralEmEnergyFraction"), "JetAccepted_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralHadronFraction"), "JetAccepted_NeutralHadronFraction", xlabel="NeutralHadronFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PhotonEnergyFraction"), "JetAccepted_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_ChargedHadronEnergyFraction"), "JetAccepted_ChargedEnergyFraction", xlabel="ChargedEnergyFraction of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralHadronMultiplicity"), "JetAccepted_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PhotonMultiplicity"), "JetAccepted_PhotonMultiplicity", xlabel="PhotonMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_ChargedMultiplicity"), "JetAccepted_ChargedMultiplicity", xlabel="ChargedMultiplicity of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PartonFlavour"), "JetAccepted_PartonFlavour", xlabel="PartonFlavour of accepted jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection/ExcludedJets"
    myDrawer(createPlot(myDir+"/jet_pt"), "JetRejected_pt", xlabel="p_{T} of rejected jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_eta"), "JetRejected_eta", xlabel="#eta of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_phi"), "JetRejected_phi", xlabel="#phi of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralEmEnergyFraction"), "JetRejected_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralHadronFraction"), "JetRejected_NeutralHadronFraction", xlabel="NeutralHadronFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PhotonEnergyFraction"), "JetRejected_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_ChargedHadronEnergyFraction"), "JetRejected_ChargedEnergyFraction", xlabel="ChargedEnergyFraction of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_NeutralHadronMultiplicity"), "JetRejected_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PhotonMultiplicity"), "JetRejected_PhotonMultiplicity", xlabel="PhotonMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_ChargedMultiplicity"), "JetRejected_ChargedMultiplicity", xlabel="ChargedMultiplicity of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_PartonFlavour"), "JetRejected_PartonFlavour", xlabel="PartonFlavour of rejected jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "JetSelection/ReferenceJetToTau"
    myDrawer(createPlot(myDir+"/MatchingDeltaR"), "JetMatchToTau_MatchingDeltaR", xlabel="#DeltaR(#tau,ref.jet)", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/PartonFlavour"), "JetMatchToTau_PartonFlavour", xlabel="pdgID", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/PtRatio"), "JetMatchToTau_pTRatio", xlabel="p_{T}^{#tau} / p_{T}^{ref.jet}", ylabel="N_{jets}", rebinToWidthX=0.05,log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "MET"
    myDrawer(createPlot(myDir+"/met"), "MET_MET", xlabel="MET, GeV", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/metPhi"), "MET_Phi", xlabel="MET #phi", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/metSignif"), "MET_significance", xlabel="MET significance", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/metSumEt"), "MET_SumET", xlabel="MET #sum E_{T}, GeV", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "Btagging"
    myDrawer(createPlot(myDir+"/NumberOfBtaggedJets"), "Btag_N", xlabel="N_{selected b jets}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/jet_bdiscriminator"), "Btag_discriminator", xlabel="b-taggind discriminator", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/RealBjet_discrim"), "Btag_discriminator_genuine_bjets", xlabel="b-tagging discriminator for genuine b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet_pt"), "Btag_pt", xlabel="p_{T} of selected b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet_eta"), "Btag_eta", xlabel="#eta of selected b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet1_pt"), "Btag_2pt", xlabel="p_{T} of first b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet1_eta"), "Btag_2eta", xlabel="#eta of first b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet2_pt"), "Btag_2pt", xlabel="p_{T} of second b jets, GeV/c", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/bjet2_eta"), "Btag_2eta", xlabel="#eta of second b jets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MCMatchForPassedJets"), "Btag_MCMatchForPassedJets", xlabel="MCMatchForPassedJets", ylabel="N_{jets}", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "CommonPlots/AtEveryStep"
    # Nvertices at every step
    myDrawer(createPlot(myDir+"/Trigger/nVertices"), "AtEveryStep_NverticesAfter1Trigger", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/VertexSelection/nVertices"), "AtEveryStep_NverticesAfter2PV", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauSelection/nVertices"), "AtEveryStep_NverticesAfter3TauSelection", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/TauWeight/nVertices"), "AtEveryStep_NverticesAfter4TauWeight", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/ElectronVeto/nVertices"), "AtEveryStep_NverticesAfter5ElectronVeto", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MuonVeto/nVertices"), "AtEveryStep_NverticesAfter6MuonVeto", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/JetSelection/nVertices"), "AtEveryStep_NverticesAfter7JetSelection", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/MET/nVertices"), "AtEveryStep_NverticesAfter8MET", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/BTagging/nVertices"), "AtEveryStep_NverticesAfter9Btagging", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/Selected/nVertices"), "AtEveryStep_NverticesSelected", xlabel="N_{vertices}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDir = "NormalisationAnalysis/eToTau"
    myDrawer(createPlot(myDir+"/etotau_mZ_all"), "Norm_etotau_mZ_all", xlabel="m_{ee} / GeV/c^{2}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_mZ_decayMode0"), "Norm_etotau_mZ_decayMode0", xlabel="m_{ee} / GeV/c^{2}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_mZ_decayMode1"), "Norm_etotau_mZ_decayMode1", xlabel="m_{ee} / GeV/c^{2}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_mZ_decayMode2"), "Norm_etotau_mZ_decayMode2", xlabel="m_{ee} / GeV/c^{2}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_taupT_all"), "Norm_etotau_taupT_all", xlabel="#tau p_{T} / GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_taupT_decayMode0"), "Norm_etotau_taupT_decayMode0", xlabel="#tau p_{T} / GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_taupT_decayMode1"), "Norm_etotau_taupT_decayMode1", xlabel="#tau p_{T}/ GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot(myDir+"/etotau_taupT_decayMode2"), "Norm_etotau_taupT_decayMode2", xlabel="#tau p_{T} / GeV/c", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    # main directory
    myDrawer(createPlot("deltaPhi"), "DeltaPhi_tauMET", xlabel="#Delta#phi(#tau jet, MET), ^{o}", ylabel="N_{events}", rebin=20, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("transverseMass"), "Mass_Transverse", xlabel="Transverse mass, GeV/c^{2}", ylabel="N_{events}", rebin=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("EWKFakeTausTransverseMass"), "Mass_Transverse_EWKFakeTaus", xlabel="Transverse mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=10, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("fullMass"), "Mass_Invariant", xlabel="Invariant mass, GeV/c^{2}", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("EWKFakeTausFullMass"), "Mass_Invariant_EWKFakeTaus", xlabel="Invariant mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=4, log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("alphaT"), "AlphaT", xlabel="#alpha_{T}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("deltaPhiJetMet"), "DeltaPhi_minJetMET", xlabel="min #Delta#phi(jet, MET), ^{o}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("maxDeltaPhiJetMet"), "DeltaPhi_maxJetMET", xlabel="max #Delta#phi(#tau jet, MET), ^{o}", textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    myDrawer(createPlot("SignalSelectionFlow"), "SelectionFlow", xlabel="Step", textFunction=lambda: addMassBRText(x=0.31, y=0.22))    
    #myDrawer(createPlot("SignalSelectionFlowVsVertices"), "SelectionFlow_vsVertices", xlabel="N_{vertices}", ylabel="Step", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    #myDrawer(createPlot("SignalSelectionFlowVsVerticesFakeTaus"), "SelectionFlow_vsVerticesFakeTaus", xlabel="N_{vertices}", ylabel="Step", log=True, ratio=True, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    
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




#    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
    print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("TauIDPassedJets::TauSelection_HPS").format(cellFormat)
    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    
    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MuonSelection").format(cellFormat)
    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat) 
    print eventCounter.getSubCounterTable("ElectronSelection").format(cellFormat)  
#    print eventCounter.getSubCounterTable("top").format(cellFormat) 

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)

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
        if rebin > 1:
            h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        else:
            print h
            #xmin = histograms.th1Xmin(th1)
            #xmax = histograms.th1Xmax(th1)
            #nbins = (xmax-xmin)/rebinWidth
            
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
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    parser.add_option("-t", dest="type", action="append", help="name of analysis type")
    parser.add_option("--noMCQCD", dest="noMCQCD", action="store_true", default=False, help="remove MC QCD")
    parser.add_option("--noSignal", dest="noSignal", action="store_true", default=False, help="remove MC QCD")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    if opts.era == None:
        print "Missing specification for era!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    for e in opts.era:
        main(opts,e)
    print "Plotting done. Now collecting garbages before exiting."
