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
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

from optparse import OptionParser

# Configuration
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

    plots.mergeRenameReorderForDataMC(datasets)

    if mcOnly:
        print "Int.Lumi (manually set)",mcOnlyLumi
    else:
        print "Int.Lumi",datasets.getDataset("Data").getLuminosity()
    if not opts.noSignal:
        print "norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    datasets.remove(filter(lambda name: "QCD_Pt20_MuEnriched" in name, datasets.getAllDatasetNames()))
    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    histograms.createLegend.moveDefaults(dx=-0.05)
    histograms.createSignalText.set(xmin=0.4, ymax=0.93, mass=120)
    
    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=optionBr, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    #plots.replaceLightHplusWithSignalPlusBackground(datasets)
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets, opts)

    # Print counters
    #doCounters(datasets)
    
def doPlots(datasets, opts):
    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    drawPlot = plots.PlotDrawer(ylabel="N_{events}", log=True, ratio=True, ratioYlabel="Data/MC", opts2={"ymin": 0, "ymax": 2}, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True)

    global plotIndex
    plotIndex = 1
    def createDrawPlot(name, moveSignalText={}, fullyBlinded=False, addBlindedText=True, moveBlindedText={}, **kwargs):
        # Create the plot object
        print "Creating plot:",name
        args = {}
        if mcOnly:
            args["normalizeToLumi"] = mcOnlyLumi
        p = plots.DataMCPlot(datasets, name, **args)

        # Remove data if fully blinded
        if not mcOnly and fullyBlinded and p.histoMgr.hasHisto("Data"):
            p.histoMgr.removeHisto("Data")
            if addBlindedText:
                tb = histograms.PlotTextBox(xmin=0.4, ymin=None, xmax=0.6, ymax=0.84, size=17)
                tb.addText("Data blinded")
                tb.move(**moveBlindedText)
                p.appendPlotObject(tb)

        # Add the signal information text box
        if not opts.noSignal:
            st = histograms.createSignalText()
            st.move(**moveSignalText)
            p.appendPlotObject(st)

        # Set the file name
        global plotIndex
        filename = ("%03d_"%plotIndex) + name.replace("/", "_")
        plotIndex += 1

        # Draw the plot
        drawPlot(p, filename, **kwargs)

    # common arguments for plots which make sense only for MC
    mcArgs = {"fullyBlinded": True, "addBlindedText": False}

    # Common plots
    myCommonPlotDirs = ["VertexSelection","TauSelection","TauWeight","ElectronVeto","MuonVeto","JetSelection","MET","BTagging","Selected","FakeTaus_BTagging","FakeTaus_Selected"]
    def createDrawCommonPlot(path, **kwargs):
        for plotDir in myCommonPlotDirs:
            args = {}
            args.update(kwargs)
            if "transverseMass" in path:
                if "BTagging" in plotDir or "Selected" in plotDir:
                    args["customizeBeforeFrame"] = lambda p: plots.partiallyBlind(p, maxShownValue=60)
            elif "Selected" in plotDir:
                args["fullyBlinded"] = True
            if "FakeTaus" in plotDir:
                args.update(mcArgs)
            createDrawPlot(path%plotDir, **args)

    #phiBinWidth = 2*3.14159/72
    phiBinWidth = 2*3.14159/36

    createDrawPlot("CommonPlots/AtEveryStep/Trigger/nVertices", xlabel="N_{Vertices}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/nVertices", xlabel="N_{Vertices}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_fakeStatus", xlabel="Fake tau status", **mcArgs)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_pT", xlabel="#tau p_{T}, GeV/c", rebinToWidthX=10)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_eta", xlabel="#tau #eta")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_phi", xlabel="#tau #phi", rebinToWidthX=phiBinWidth)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/tau_Rtau", xlabel="R_{#tau}", rebinToWidthX=0.05, opts={"xmin": 0.5, "xmax": 1}, moveLegend={"dx": -0.5})
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/electrons_N", xlabel="N_{electrons}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/muons_N", xlabel="N_{muons}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/jets_N", xlabel="N_{jets}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/jets_N_allIdentified", xlabel="N_{all identified jets}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/MET_Raw", xlabel="Raw MET, GeV", rebinToWidthX=20)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/MET_MET", xlabel="MET, GeV", rebinToWidthX=20)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/MET_phi", xlabel="MET #phi", rebinToWidthX=phiBinWidth)
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/bjets_N", xlabel="N_{b jets}", opts={"xmax": 8})
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/DeltaPhi_TauMET", xlabel="#Delta#phi(#tau,MET)")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet1MET", xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{1})^{2}}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet2MET", xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{2})^{2}}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet3MET", xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{3})^{2}}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/hDeltaR_TauMETJet4MET", xlabel="#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2} + #Delta#phi(MET,jet_{4})^{2}}")
    createDrawCommonPlot("CommonPlots/AtEveryStep/%s/transverseMass", xlabel="m_{T}(#tau,MET)", rebinToWidthX=20)


    myDir = "Vertices"
    createDrawPlot(myDir+"/verticesBeforeWeight", xlabel="N_{vertices}")
    createDrawPlot(myDir+"/verticesBeforeWeight", xlabel="N_{vertices}")
    createDrawPlot(myDir+"/verticesAfterWeight", xlabel="N_{vertices}")
    createDrawPlot(myDir+"/verticesTriggeredBeforeWeight", xlabel="N_{vertices}")
    createDrawPlot(myDir+"/verticesTriggeredAfterWeight", xlabel="N_{vertices}")
    myDir = "TauSelection"
    createDrawPlot(myDir+"/N_TriggerMatchedTaus", xlabel="N_{trg. matched taus}")
    createDrawPlot(myDir+"/N_TriggerMatchedSeparateTaus", xlabel="N_{trg. matched separate taus}")
    createDrawPlot(myDir+"/TauCand_DecayModeFinding", xlabel="HPS Decay Mode", opts={"xmax": 16, "nbinsx": 16}, customizeBeforeDraw=tauEmbedding.decayModeCheckCustomize)
    createDrawPlot(myDir+"/TauSelection_all_tau_candidates_N", xlabel="N_{tau candidates}", opts={"xmax": 8})
    createDrawPlot(myDir+"/TauSelection_all_tau_candidates_pt", xlabel="p_{T} of all tau candidates, GeV/c", rebinToWidthX=10)
    createDrawPlot(myDir+"/TauSelection_all_tau_candidates_eta", xlabel="#eta of all tau candiates", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/TauSelection_all_tau_candidates_phi", xlabel="#phi of all tau candidates", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/TauSelection_all_tau_candidates_MC_purity", xlabel="MC purity of all tau candidates", **mcArgs)
    createDrawPlot(myDir+"/TauCand_JetPt", xlabel="p_{T} of tau candidates, GeV/c", rebinToWidthX=10)
    createDrawPlot(myDir+"/TauCand_JetEta", xlabel="#eta of tau candidates", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/TauCand_LdgTrackPtCut", xlabel="p_{T}^{ldg.ch.particle} of tau candidates, GeV/c", rebinToWidthX=10)
    #createDrawPlot(myDir+"/TauCand_EMFractionCut", xlabel="EM energy fraction of tau candidates")
    createDrawPlot(myDir+"/TauSelection_cleaned_tau_candidates_N", xlabel="N_{cleaned tau candidates}", opts={"xmax": 8})
    createDrawPlot(myDir+"/TauSelection_cleaned_tau_candidates_pt", xlabel="p_{T} of cleaned tau candidates, GeV/c", rebinToWidthX=10)
    createDrawPlot(myDir+"/TauSelection_cleaned_tau_candidates_eta", xlabel="#eta of cleaned tau candidates", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/TauSelection_cleaned_tau_candidates_phi", xlabel="#phi of cleaned tau candidates", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/TauSelection_cleaned_tau_candidates_MC_purity", xlabel="MC purity of cleaned tau candidates", **mcArgs)
    createDrawPlot(myDir+"/IsolationPFChargedHadrCandsPtSum", xlabel="#sum p_{T} of PF ch. hadr. candidates, GeV/c", opts={"xmax": 40})
    createDrawPlot(myDir+"/IsolationPFGammaCandEtSum", xlabel="#sum p_{T} of PF gamma candidates, GeV/c", opts={"xmax": 40})
    createDrawPlot(myDir+"/TauID_NProngsCut", xlabel="N_{prongs}", opts={"xmax": 5})
    #createDrawPlot(myDir+"/TauID_ChargeCut", xlabel="Q_{tau}")
    createDrawPlot(myDir+"/TauID_RtauCut", xlabel="R_{#tau}", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/TauSelection_selected_taus_N", xlabel="N_{selected taus}", opts={"xmax": 8})
    createDrawPlot(myDir+"/TauSelection_selected_taus_pt", xlabel="p_{T} of selected taus", rebinToWidthX=10)
    createDrawPlot(myDir+"/TauSelection_selected_taus_eta", xlabel="#eta of selected taus", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/TauSelection_selected_taus_phi", xlabel="#phi of selected taus", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/TauSelection_selected_taus_MC_purity", xlabel="MC purity of selected taus", **mcArgs)
    myDir = "FakeTauIdentifier_TauID"
    createDrawPlot(myDir+"/TauMatchType", xlabel="MC #tau decay", **mcArgs)
    createDrawPlot(myDir+"/TauOrigin", xlabel="MC #tau origin", **mcArgs)
    createDrawPlot(myDir+"/MuOrigin", xlabel="MC #mu origin", **mcArgs)
    createDrawPlot(myDir+"/ElectronOrigin", xlabel="MC e origin", **mcArgs)
    myDir = "SelectedTau"
    createDrawPlot(myDir+"/SelectedTau_pT_AfterTauID", xlabel="p_{T} of selected taus, GeV/c", rebinToWidthX=10)
    createDrawPlot(myDir+"/SelectedTau_eta_AfterTauID", xlabel="#eta of selected taus", rebinToWidthX=0.1, opts={"xmin": -2.4, "xmax": 2.4})
    createDrawPlot(myDir+"/SelectedTau_phi_AfterTauID", xlabel="#phi of selected taus", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/SelectedTau_Rtau_AfterTauID", xlabel="R_{#tau} of selected taus", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/SelectedTau_pT_AfterCuts", xlabel="p_{T} of tau after selections, GeV/c", rebinToWidthX=10)
    createDrawPlot(myDir+"/SelectedTau_eta_AfterCuts", xlabel="#eta of tau after selections", rebinToWidthX=0.1)
    createDrawPlot(myDir+"/SelectedTau_Rtau_AfterCuts", xlabel="R_{#tau} of tau after selections", rebinToWidthX=0.1, moveLegend={"dx": -0.5})
    myDir = "ElectronSelection"
    createDrawPlot(myDir+"/ElectronPt_all", xlabel="p_{T} of electron candidates, GeV/c", rebinToWidthX=5)
    createDrawPlot(myDir+"/ElectronEta_all", xlabel="#eta of electron candidates")
    createDrawPlot(myDir+"/ElectronPt_veto", xlabel="p_{T}^{veto electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, cutLine=15)
    createDrawPlot(myDir+"/ElectronEta_veto", xlabel="#eta^{veto electron}", ylabel="Identified electrons / %.1f", opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, cutLine=[-2.5, 2.5])
    createDrawPlot(myDir+"/NumberOfVetoElectrons", xlabel="Number of selected veto electrons", ylabel="Events", opts={"xmax": 6,"ymaxfactor": 2})
    createDrawPlot(myDir+"/ElectronPt_tight", xlabel="p_{T}^{tight electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", opts={"xmax": 250,"xmin": 0, "ymaxfactor": 2}, cutLine=15)
    createDrawPlot(myDir+"/ElectronEta_tight", xlabel="#eta^{tight electron}", ylabel="Identified electrons / %.1f", opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 10}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, cutLine=[-2.5, 2.5])
    createDrawPlot(myDir+"/NumberOfTightElectrons", xlabel="Number of selected tight electrons", ylabel="Events", opts={"xmax": 6,"ymaxfactor": 2}, cutLine=1)
    myDir = "MuonSelection"
    createDrawPlot(myDir+"/LooseMuonPt", xlabel="p_{T} of #mu candidates, GeV/c", ylabel="N_{muons}", rebinToWidthX=5)
    createDrawPlot(myDir+"/LooseMuonEta", xlabel="#eta of #mu candidates", ylabel="N_{muons}")
    createDrawPlot(myDir+"/MuonTransverseImpactParameter", xlabel="IP_{T} of #mu candidates, mm", ylabel="N_{muons}")
    createDrawPlot(myDir+"/MuonDeltaIPz", xlabel="IP_{z} - PV_{z} of #mu candidates, cm", ylabel="N_{muons}")
    createDrawPlot(myDir+"/MuonRelIsol", xlabel="#mu rel. isol.", ylabel="N_{muons}")
    createDrawPlot(myDir+"/NumberOfLooseMuons", xlabel="Number of loose #mus", opts={"xmax": 8})
    createDrawPlot(myDir+"/NumberOfTightMuons", xlabel="Number of tight #mus", opts={"xmax": 8})
    createDrawPlot(myDir+"/MuonPt_BeforeIsolation", xlabel="#mu p_{T} before isolation, GeV/c")
    createDrawPlot(myDir+"/MuonEta_BeforeIsolation", xlabel="#mu #eta before isolation")
    myDir = "JetSelection"
    createDrawPlot(myDir+"/jet_pt", xlabel="p_{T} of jet candidates, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_pt_central", xlabel="p_{T} of central jet candidates, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_eta", xlabel="#eta of jet candidates", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_phi", xlabel="#phi of jet candidates", ylabel="N_{jets}", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/firstJet_pt", xlabel="p_{T} of first jet, GeV/c")
    createDrawPlot(myDir+"/firstJet_eta", xlabel="#eta of first jet")
    createDrawPlot(myDir+"/firstJet_phi", xlabel="#phi of first jet", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/secondJet_pt", xlabel="p_{T} of second jet, GeV/c")
    createDrawPlot(myDir+"/secondJet_eta", xlabel="#eta of second jet")
    createDrawPlot(myDir+"/secondJet_phi", xlabel="#phi of second jet", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/thirdJet_pt", xlabel="p_{T} of third jet, GeV/c")
    createDrawPlot(myDir+"/thirdJet_eta", xlabel="#eta of third jet")
    createDrawPlot(myDir+"/thirdJet_phi", xlabel="#phi of third jet", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/NumberOfSelectedJets", xlabel="N_{selected jets}")
    myDir = "JetSelection/SelectedJets"
    createDrawPlot(myDir+"/jet_pt", xlabel="p_{T} of accepted jets, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_eta", xlabel="#eta of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_phi", xlabel="#phi of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralHadronFraction", xlabel="NeutralHadronFraction of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_ChargedHadronEnergyFraction", xlabel="ChargedEnergyFraction of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of accepted jets", ylabel="N_{jets}", opts={"xmax": 10})
    createDrawPlot(myDir+"/jet_PhotonMultiplicity", xlabel="PhotonMultiplicity of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_ChargedMultiplicity", xlabel="ChargedMultiplicity of accepted jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_PartonFlavour", xlabel="PartonFlavour of accepted jets", ylabel="N_{jets}", **mcArgs)
    myDir = "JetSelection/ExcludedJets"
    createDrawPlot(myDir+"/jet_pt", xlabel="p_{T} of rejected jets, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_eta", xlabel="#eta of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_phi", xlabel="#phi of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralEmEnergyFraction", xlabel="NeutralEmEnergyFraction of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralHadronFraction", xlabel="NeutralHadronFraction of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_PhotonEnergyFraction", xlabel="PhotonEnergyFraction of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_ChargedHadronEnergyFraction", xlabel="ChargedEnergyFraction of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_NeutralHadronMultiplicity", xlabel="NeutralHadronMultiplicity of rejected jets", ylabel="N_{jets}", opts={"xmax": 10})
    createDrawPlot(myDir+"/jet_PhotonMultiplicity", xlabel="PhotonMultiplicity of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_ChargedMultiplicity", xlabel="ChargedMultiplicity of rejected jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/jet_PartonFlavour", xlabel="PartonFlavour of rejected jets", ylabel="N_{jets}", **mcArgs)
    myDir = "JetSelection/ReferenceJetToTau"
    createDrawPlot(myDir+"/MatchingDeltaR", xlabel="#DeltaR(#tau,ref.jet)", ylabel="N_{jets}")
    createDrawPlot(myDir+"/PartonFlavour", xlabel="pdgID", ylabel="N_{jets}", **mcArgs)
    createDrawPlot(myDir+"/PtRatio", xlabel="p_{T}^{#tau} / p_{T}^{ref.jet}", ylabel="N_{jets}")
    myDir = "MET"
    createDrawPlot(myDir+"/met", xlabel="MET, GeV", ylabel="N_{events}", rebin=4)
    createDrawPlot(myDir+"/metPhi", xlabel="MET #phi", rebinToWidthX=phiBinWidth)
    createDrawPlot(myDir+"/metSignif", xlabel="MET significance")
    createDrawPlot(myDir+"/metSumEt", xlabel="MET #sum E_{T}, GeV")
    myDir = "Btagging"
    createDrawPlot(myDir+"/NumberOfBtaggedJets", xlabel="N_{selected b jets}")
    createDrawPlot(myDir+"/jet_bdiscriminator", xlabel="b-taggind discriminator", ylabel="N_{jets}")
    createDrawPlot(myDir+"/RealBjet_discrim", xlabel="b-tagging discriminator for genuine b jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet_pt", xlabel="p_{T} of selected b jets, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet_eta", xlabel="#eta of selected b jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet1_pt", xlabel="p_{T} of first b jets, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet1_eta", xlabel="#eta of first b jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet2_pt", xlabel="p_{T} of second b jets, GeV/c", ylabel="N_{jets}")
    createDrawPlot(myDir+"/bjet2_eta", xlabel="#eta of second b jets", ylabel="N_{jets}")
    createDrawPlot(myDir+"/MCMatchForPassedJets", xlabel="MCMatchForPassedJets", ylabel="N_{jets}")
    myDir = "NormalisationAnalysis/eToTau"
    createDrawPlot(myDir+"/etotau_mZ_all", xlabel="m_{ee} / GeV/c^{2}")
    createDrawPlot(myDir+"/etotau_mZ_decayMode0", xlabel="m_{ee} / GeV/c^{2}")
    createDrawPlot(myDir+"/etotau_mZ_decayMode1", xlabel="m_{ee} / GeV/c^{2}")
    createDrawPlot(myDir+"/etotau_mZ_decayMode2", xlabel="m_{ee} / GeV/c^{2}")
    createDrawPlot(myDir+"/etotau_taupT_all", xlabel="#tau p_{T} / GeV/c")
    createDrawPlot(myDir+"/etotau_taupT_decayMode0", xlabel="#tau p_{T} / GeV/c")
    createDrawPlot(myDir+"/etotau_taupT_decayMode1", xlabel="#tau p_{T}/ GeV/c")
    createDrawPlot(myDir+"/etotau_taupT_decayMode2", xlabel="#tau p_{T} / GeV/c")
    # main directory
    createDrawPlot("deltaPhi", xlabel="#Delta#phi(#tau jet, MET), ^{o}", ylabel="N_{events}", rebin=20)
    createDrawPlot("transverseMass", xlabel="Transverse mass, GeV/c^{2}", ylabel="N_{events}", rebinToWidthX=20, customizeBeforeFrame=lambda p: plots.partiallyBlind(p, maxShownValue=60))
    createDrawPlot("EWKFakeTausTransverseMass", xlabel="Transverse mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=10, **mcArgs)
    createDrawPlot("fullMass", xlabel="Invariant mass, GeV/c^{2}", ylabel="N_{events}", rebin=4, fullyBlinded=True)
    createDrawPlot("EWKFakeTausFullMass", xlabel="Invariant mass EWK fake taus, GeV/c^{2}", ylabel="N_{events}", rebin=4, **mcArgs)
    createDrawPlot("alphaT", xlabel="#alpha_{T}", opts={"xmax": 2}, customizeBeforeFrame=lambda p: plots.partiallyBlind(p, maxShownValue=0.5))
    createDrawPlot("deltaPhiJetMet", xlabel="min #Delta#phi(jet, MET), ^{o}", fullyBlinded=True)
    createDrawPlot("maxDeltaPhiJetMet", xlabel="max #Delta#phi(#tau jet, MET), ^{o}", fullyBlinded=True)
    createDrawPlot("SignalSelectionFlow", xlabel="Step", opts={"xmax": 7})

    #createDrawPlot("SignalSelectionFlowVsVertices"", xlabel="N_{vertices}", ylabel="Step",)
    #createDrawPlot("SignalSelectionFlowVsVerticesFakeTaus", xlabel="N_{vertices}", ylabel="Step")
    
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
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", "--dataEra", dest="era", action="append", help="name of era")
    parser.add_option("-t", dest="type", action="append", help="name of analysis type")
    parser.add_option("--noMCQCD", dest="noMCQCD", action="store_true", default=False, help="remove MC QCD")
    parser.add_option("--noSignal", dest="noSignal", action="store_true", default=False, help="remove MC QCD")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    if opts.era == None:
        parser.print_help()
        print
        parser.error("Missing specification for era!")

    # Arguments are ok, proceed to run
    for e in opts.era:
        main(opts,e)
    print "Plotting done. Now collecting garbages before exiting."
