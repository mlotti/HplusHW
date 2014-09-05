#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisInvertedTau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConfigInfo.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace {
  template <typename T>
  void copyPtrToVector(const edm::PtrVector<T>& src, std::vector<T>& dst) {
    dst.reserve(src.size());
    for(typename edm::PtrVector<T>::const_iterator i = src.begin(); i != src.end(); ++i) {
      dst.push_back(**i);
    }
  }
}

namespace HPlus {
  SignalAnalysisInvertedTau::SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    bSelectOnlyGenuineTausForMC(iConfig.getUntrackedParameter<bool>("selectOnlyGenuineTausForMC")),
    fLowBoundForQCDInvertedIsolation(iConfig.getUntrackedParameter<std::string>("lowBoundForQCDInvertedIsolation")),
    bMakeEtaCorrectionStatus(iConfig.getUntrackedParameter<bool>("makeQCDEtaCorrectionStatus")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    // Common counters
    fAllCounter(eventCounter.addCounter("All events")),
    fTopPtWeightCounter(eventCounter.addCounter("Top pt reweight")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),  
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fVertexFilterCounter(eventCounter.addCounter("Vertex number filter")),
    fTauCandidateCounter(eventCounter.addCounter("Tau candidates found")),
    fNprongsAfterTauIDCounter(eventCounter.addCounter("Nprongs cut, all tau candidates")),
    fRtauAfterTauIDCounter(eventCounter.addCounter("Rtau cut, all tau candidates")),
    // Baseline counters
    fBaselineTauIDCounter(eventCounter.addCounter("Baseline: at least one tau")),
    fBaselineTauFakeScaleFactorCounter(eventCounter.addCounter("Baseline:tau fake scale factor, all passed taus")),
    fBaselineTauTriggerScaleFactorCounter(eventCounter.addCounter("Baseline:tau trig scale factor, all passed taus")),  
    fBaselineOneTauCounter(eventCounter.addCounter("Baseline: one tau candidate only")),
    fBaselineEvetoCounter(eventCounter.addCounter("Baseline: electron veto")),
    fBaselineMuvetoCounter(eventCounter.addCounter("Baseline: muon veto")),
    fBaselineJetsCounter(eventCounter.addCounter("Baseline: njets")),
    fBaselinePreMETCutCounter(eventCounter.addCounter("Baseline: pre-MET cut")),
    fBaselineMetTriggerScaleFactorCounter(eventCounter.addCounter("Baseline: MET SF")),
    fBaselineQCDTailKillerCollinearCounter(eventCounter.addCounter("Baseline: QCD tail killer collinear")),
    fBaselineMetCounter(eventCounter.addCounter("Baseline: MET")),
    fBaselineBtagCounter(eventCounter.addCounter("Baseline: btagging")),
    fBaselineBTaggingScaleFactorCounter(eventCounter.addCounter("Baseline: btagging scale factor")),
    fBaselineQCDTailKillerBackToBackCounter(eventCounter.addCounter("Baseline: QCD tail killer back-to-back")),
    fBaselineTopSelectionCounter(eventCounter.addCounter("Baseline: top reco")),
    fBaselineDeltaPhiTauMETCounter(eventCounter.addCounter("Baseline: -> DeltaPhi(Tau,MET) upper limit")),
    fBaselineSelectedEventsCounter(eventCounter.addCounter("Baseline: Selected events")),
    fBaselineSelectedEventsInvariantMassCounter(eventCounter.addCounter("Baseline: Selected events invariant mass")),
    // Inverted counters
    fInvertedTauIDCounter(eventCounter.addCounter("Inverted: Taus found")),
    fInvertedTauFakeScaleFactorCounter(eventCounter.addCounter("Inverted: tau fake scale factor, all cands")),
    fInvertedTauTriggerScaleFactorCounter(eventCounter.addCounter("Inverted: tau trigger scale factor, all cands")),
    fInvertedOneTauCounter(eventCounter.addCounter("Inverted: one tau candidate only")),
    fInvertedElectronVetoCounter(eventCounter.addCounter("Inverted: electron veto")),
    fInvertedMuonVetoCounter(eventCounter.addCounter("Inverted: muon veto")),
    fInvertedNJetsCounter(eventCounter.addCounter("Inverted: njets")),
    fInvertedPreMETCutCounter(eventCounter.addCounter("Inverted: pre-MET cut")),
    fInvertedMetTriggerScaleFactorCounter(eventCounter.addCounter("Inverted: MET SF")),
    fInvertedQCDTailKillerCollinearCounter(eventCounter.addCounter("Inverted: QCD tail killer collinear")),
    fInvertedBTaggingBeforeMETCounter(eventCounter.addCounter("Inverted: btagging before MET")),
    fInvertedBjetVetoCounter(eventCounter.addCounter("Inverted: -> Veto on b jets before MET")),
    fInvertedMetCounter(eventCounter.addCounter("Inverted: MET")),
    fInvertedBvetoCounter(eventCounter.addCounter("Inverted: -> Veto on b jets after MET")),
    fInvertedBvetoDeltaPhiCounter(eventCounter.addCounter("Inverted: -> Veto on b jets after MET and Dphi")),
    fInvertedBTaggingCounter(eventCounter.addCounter("Inverted: btagging")),
    fInvertedBTaggingScaleFactorCounter(eventCounter.addCounter("Inverted: btagging scale factor")),
    fInvertedQCDTailKillerBackToBackCounter(eventCounter.addCounter("Inverted: QCD tail killer back-to-back")),
    fInvertedTopSelectionCounter(eventCounter.addCounter("Inverted: top reco")),
    fInvertedDeltaPhiTauMETCounter(eventCounter.addCounter("Inverted: -> DeltaPhi(Tau,MET) upper limit")),
    fInvertedSelectedEventsCounter(eventCounter.addCounter("Inverted: Selected events")),
    fInvertedSelectedEventsInvariantMassCounter(eventCounter.addCounter("Inverted: Selected events invariant mass")),
    // Other counters
//     fDeltaPhiVSDeltaPhiMETJet1CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet1,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet2CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet2,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet3CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet3,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet4CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet4,MET) vs DeltaPhi cut")), 
//     fHiggsMassCutCounter(eventCounter.addCounter("Inverted: HiggsMassCut")),
    ftransverseMassCut80Counter(eventCounter.addCounter("Inverted: -> transverseMass > 80")),
    ftransverseMassCut100Counter(eventCounter.addCounter("Inverted: -> transverseMass > 100")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET", fTauSelection.getIsolationDiscriminator()),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fTopSelectionManager(iConfig, eventCounter, fHistoWrapper, iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    fFullHiggsMassCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("invMassReco"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper, "HistoName"),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WjetsWeight"),
    fTopPtWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("topPtWeightReader"), fHistoWrapper, "TopPtWeight"),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), fHistoWrapper, "TauID"),
    // Common plots
    fCommonPlots(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDInverted),
    fNormalizationSystematicsSignalRegion(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDNormalizationSystematicsSignalRegion),
    fNormalizationSystematicsControlRegion(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDNormalizationSystematicsControlRegion),
    // Common plots at every step for baseline
    fCommonPlotsBaselineAfterMetSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetSF",false,"")),
    fCommonPlotsBaselineAfterCollinearCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCuts",false,"")),
    fCommonPlotsBaselineAfterCollinearCutsPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCutsPlusBackToBackCuts",false,"")),
    fCommonPlotsBaselineAfterCollinearCutsPlusBtag(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCutsPlusBtag",false,"")),
    fCommonPlotsBaselineAfterCollinearCutsPlusBtagPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCutsPlusBtagPlusBackToBackCuts(",false,"")),
    fCommonPlotsBaselineAfterCollinearCutsPlusBveto(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCutsPlusBveto",false,"")),
    fCommonPlotsBaselineAfterCollinearCutsPlusBvetoPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterCollinearCutsPlusBvetoPlusBackToBackCuts",false,"")),
    fCommonPlotsBaselineAfterMet(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMet",false,"")),
    fCommonPlotsBaselineAfterMetPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetPlusBackToBackCuts",false,"")),
    fCommonPlotsBaselineAfterMetPlusBveto(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetPlusBveto",false,"")),
    fCommonPlotsBaselineAfterMetPlusBvetoPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetPlusBvetoPlusBackToBackCuts",false,"")),
    fCommonPlotsBaselineAfterMetPlusSoftBtaggingPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetPlusSoftBtaggingPlusBackToBackCuts",false,"")),
    fCommonPlotsBaselineAfterMETAndBtagWithSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMETAndBtagWithSF",false,"")),
    fCommonPlotsBaselineAfterBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterBackToBackCuts",false,"")),
    // Common plots at every step for baseline
    fCommonPlotsInvertedAfterMetSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMetSF",false,"")),
    fCommonPlotsInvertedAfterCollinearCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCuts",false,"")),
    fCommonPlotsInvertedAfterCollinearCutsPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCutsPlusBackToBackCuts",false,"")),
    fCommonPlotsInvertedAfterCollinearCutsPlusBtag(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCutsPlusBtag",false,"")),
    fCommonPlotsInvertedAfterCollinearCutsPlusBtagPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCutsPlusBtagPlusBackToBackCuts(",false,"")),
    fCommonPlotsInvertedAfterCollinearCutsPlusBveto(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCutsPlusBveto",false,"")),
    fCommonPlotsInvertedAfterCollinearCutsPlusBvetoPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterCollinearCutsPlusBvetoPlusBackToBackCuts",false,"")),
    fCommonPlotsInvertedAfterMet(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMet",false,"")),
    fCommonPlotsInvertedAfterMetPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMetPlusBackToBackCuts",false,"")),
    fCommonPlotsInvertedAfterMetPlusBveto(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMetPlusBveto",false,"")),
    fCommonPlotsInvertedAfterMetPlusBvetoPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMetPlusBvetoPlusBackToBackCuts",false,"")),
    fCommonPlotsInvertedAfterMetPlusSoftBtaggingPlusBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMetPlusSoftBtaggingPlusBackToBackCuts",false,"")),
    fCommonPlotsInvertedAfterMETAndBtagWithSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterMETAndBtagWithSF",false,"")),
    fCommonPlotsInvertedAfterBackToBackCuts(fCommonPlots.createCommonPlotsFilledAtEveryStep("InvertedAfterBackToBackCuts",false,"")),

    // Other
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyGenuineTaus", false))
  {
    edm::Service<TFileService> fs;
    ConfigInfo::writeConfigInfo(iConfig, *fs);
 
    TFileDirectory myInvertedDir = fs->mkdir("Inverted");
    TFileDirectory myBaselineDir = fs->mkdir("baseline");
    // Book histograms filled in the analysis body

    // Obtain common plot dimension specifications
    const int myMtBins = fCommonPlots.getMtBinSettings().bins();
    const double myMtMin = fCommonPlots.getMtBinSettings().min();
    const double myMtMax = fCommonPlots.getMtBinSettings().max();
    const int myMassBins = fCommonPlots.getInvmassBinSettings().bins();
    const double myMassMin = fCommonPlots.getInvmassBinSettings().min();
    const double myMassMax = fCommonPlots.getInvmassBinSettings().max();
    const int myMetBins = fCommonPlots.getMetBinSettings().bins();
    const double myMetMin = fCommonPlots.getMetBinSettings().min();
    const double myMetMax = fCommonPlots.getMetBinSettings().max();
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();

    hOneProngRtauPassedInvertedTaus = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "OneProngRtauPassedInvertedTaus", "OneProngRtauPassedInvertedTaus", 10, 0, 10);
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesBeforeWeight", "Number of vertices without weighting", 60, 0, 60);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesAfterWeight", "Number of vertices with weighting", 60, 0, 60);
    hTransverseMassVsDphi = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "transverseMassVsDphi", "transverseMassVsDphi;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.,180,0.,180.);

    // Tau properties for inverted selection after tau ID + tau SF's
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterTauID, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtaAfterTauID, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);   
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauPhiAfterTauID, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauRtauAfterTauID, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauLeadingTrackPtAfterTauID, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    // Tau properties for inverted selection after MET cut
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterMetCut, "SelectedTau_pT_AfterMetCut", "#tau p_{T}, GeV/c", 200, 0.0 , 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtaAfterMetCut, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauPhiAfterMetCut, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauRtauAfterMetCut, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 180, 0., 1.2);
    // Tau properties for inverted selection after all cuts
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterCuts, "SelectedInvertedTauAfterCuts", "SelectedInvertedTauAfterCuts", 100, 0.0, 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtaAfterCuts, "SelectedInvertedTau_eta_AfterCuts", "SelectedInvertedTau_eta_AfterCuts", 60, -3.0, 3.0);
    // Tau pt for inverted selection after a selection
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterTauVeto, "SelectedTau_pT_AfterTauVeto", "#tau p_{T}, GeV/c", 200, 0.0, 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterJetCut, "SelectedTau_pT_AfterJetCut", "#tau p_{T}, GeV/c", 200, 0.0 , 400.0 );
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterCollinearCuts, "SelectedTau_pT_CollinearCuts", "#tau p_{T}, GeV/c", 200, 0.0 , 400.0 );
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterBtagging, "SelectedTau_pT_AfterBtagging", "#tau p_{T}, GeV/c", 200, 0.0 , 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterBjetVeto, "SelectedTau_pT_AfterBveto", "#tau p_{T}, GeV/c", 200, 0.0, 400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterBjetVetoPhiCuts, "SelectedTau_pT_AfterBvetoPhiCuts", "#tau p_{T}, GeV/c", 200, 0.,400.0);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvertedTauIdSelectedTauEtAfterBackToBackCuts, "SelectedTau_pT_BackToBackCuts", "#tau p_{T}, GeV/c", 200, 0.0 , 400.0);


    // baseline MET histos
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterJets, "METBaselineTauIdAfterJets", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterMetSF, "METBaselineTauIdAfterMetSF", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterMetSFPlusBtag, "METBaselineTauIdAfterMetSFPlusBtag", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterMetSFPlusBveto, "METBaselineTauIdAfterMetSFPlusBveto", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hMETBaselineTauIdAfterCollinearCuts, "METBaselineTauIdAfterCollinearCuts", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, "METBaselineTauIdAfterCollinearCutsPlusBackToBackCuts", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hMETBaselineTauIdAfterCollinearCutsPlusBtag, "METBaselineTauIdAfterCollinearCutsPlusBtag", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMETBaselineTauIdAfterCollinearCutsPlusBveto, "METBaselineTauIdAfterCollinearCutsPlusBveto", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    // baseline MT histos
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMetSF, "MTBaselineTauIdAfterMetSF", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hMTBaselineTauIdAfterCollinearCuts, "MTBaselineTauIdAfterCollinearCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, "MTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterCollinearCutsPlusBtag, "MTBaselineTauIdAfterCollinearCutsPlusBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, "MTBaselineTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterCollinearCutsPlusBveto, "MTBaselineTauIdAfterCollinearCutsPlusBveto", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, "MTBaselineTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMet, "MTBaselineTauIdAfterMet", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMetPlusBackToBackCuts, "MTBaselineTauIdAfterMetPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMetPlusBveto, "MTBaselineTauIdAfterMetPlusBveto", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts, "MTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts, "MTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterBtag, "MTBaselineTauIdAfterBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterBackToBackCuts, "MTBaselineTauIdAfterBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hMTBaselineTauIdAfterTopReco, "MTBaselineTauIdAfterTopReco", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    // baseline MT histos for closure test in control region
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hMTBaselineTauIdFinalReversedBtag, "MTBaselineTauIdFinalReversedBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hMTBaselineTauIdFinalReversedBacktoBackDeltaPhi, "MTBaselineTauIdFinalReversedBacktoBackDeltaPhi", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    // baseline invariant mass histos
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hInvMassBaselineTauIdAfterCollinearCuts, "INVMASSBaselineTauIdAfterCollinearCuts", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myBaselineDir, hInvMassBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, "INVMASSBaselineTauIdAfterCollinearCutsPlusBackToBackCuts", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    // baseline invariant mass histos for closure test in control region
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hInvMassBaselineTauIdFinalReversedBtag, "INVMASSBaselineTauIdFinalReversedBtag", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myBaselineDir, hInvMassBaselineTauIdFinalReversedBacktoBackDeltaPhi, "INVMASSBaselineTauIdFinalReversedBacktoBackDeltaPhi", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    // inverted MET histos
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterJets, "METInvertedTauIdAfterJets", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterMetSF, "METInvertedTauIdAfterMetSF", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterMetSFPlusBtag, "METInvertedTauIdAfterMetSFPlusBtag", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterMetSFPlusBveto, "METInvertedTauIdAfterMetSFPlusBveto", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hMETInvertedTauIdAfterCollinearCuts, "METInvertedTauIdAfterCollinearCuts", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, "METInvertedTauIdAfterCollinearCutsPlusBackToBackCuts", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hMETInvertedTauIdAfterCollinearCutsPlusBtag, "METInvertedTauIdAfterCollinearCutsPlusBtag", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterCollinearCutsPlusBveto, "METInvertedTauIdAfterCollinearCutsPlusBveto", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMETInvertedTauIdAfterBackToBackCuts, "METInvertedTauIdAfterBackToBackCuts", "E_{T}^{miss}, GeV", myMetMax-myMetMin, myMetMin, myMetMax);
    // inverted MT histos

    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMetSF, "MTInvertedTauIdAfterMetSF", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hMTInvertedTauIdAfterCollinearCuts, "MTInvertedTauIdAfterCollinearCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, "MTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterCollinearCutsPlusBtag, "MTInvertedTauIdAfterCollinearCutsPlusBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, "MTInvertedTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterCollinearCutsPlusBveto, "MTInvertedTauIdAfterCollinearCutsPlusBveto", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, "MTInvertedTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMet, "MTInvertedTauIdAfterMet", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMetPlusBackToBackCuts, "MTInvertedTauIdAfterMetPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMetPlusBveto, "MTInvertedTauIdAfterMetPlusBveto", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts, "MTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts, "MTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterBtag, "MTInvertedTauIdAfterBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterBackToBackCuts, "MTInvertedTauIdAfterBackToBackCuts", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hMTInvertedTauIdAfterTopReco, "MTInvertedTauIdAfterTopReco", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    // inverted MT histos for closure test in control region
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hMTInvertedTauIdFinalReversedBtag, "MTInvertedTauIdFinalReversedBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hMTInvertedTauIdFinalReversedBacktoBackDeltaPhi, "MTInvertedTauIdFinalReversedBacktoBackDeltaPhi", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    // inverted invariant mass histos
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hInvMassInvertedTauIdAfterCollinearCuts, "INVMASSInvertedTauIdAfterCollinearCuts", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hInvMassInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, "INVMASSInvertedTauIdAfterCollinearCutsPlusBackToBackCuts", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    // inverted invariant mass histos for closure test in control region
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hInvMassInvertedTauIdFinalReversedBtag, "INVMASSInvertedTauIdFinalReversedBtag", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myInvertedDir, hInvMassInvertedTauIdFinalReversedBacktoBackDeltaPhi, "INVMASSInvertedTauIdFinalReversedBacktoBackDeltaPhi", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);

    //     myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hHiggsMassTailKiller, "HiggsMassTailKiller", 250, 0.0 , 500.0 );

    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hNBInvertedTauIdJet, "NBInvertedTauIdJet", "N_{b jets}", 10, 0.0 , 10.0 );
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hNBInvertedTauIdJetDphi, "NBInvertedTauIdJetDphi", "N_{b jets}", 10, 0.0 , 10.0 );
    // myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hNJetInvertedTauId, "NJetInvertedTauId", 10, 0.0 , 10.0 );
    // myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hNJetInvertedTauIdMet, "NJetInvertedTauIdMet", 10, 0.0 , 10.0 );
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hDeltaPhiInverted, "DeltaPhiInverted", "#Delta#phi, ^{o}", 180, 0., 180.);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myInvertedDir, hDeltaPhiInvertedNoB, "DeltaPhiInvertedNoB", "#Delta#phi, ^{o}",180, 0., 180.);

    //     hQCDTailKillerJet0BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet0BackToBackInverted","QCDTailKillerJet0BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet0BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet0BackToBackBaseline","QCDTailKillerJet0BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet0CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet0CollinearInverted","QCDTailKillerJet0CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet0CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet0CollinearBaseline","QCDTailKillerJet0CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet1BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet1BackToBackInverted","QCDTailKillerJet1BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet1BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet1BackToBackBaseline","QCDTailKillerJet1BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet1CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet1CollinearInverted","QCDTailKillerJet1CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet1CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet1CollinearBaseline","QCDTailKillerJet1CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet2BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet2BackToBackInverted","QCDTailKillerJet2BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet2BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet2BackToBackBaseline","QCDTailKillerJet2BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet2CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet2CollinearInverted","QCDTailKillerJet2CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet2CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet2CollinearBaseline","QCDTailKillerJet2CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet3BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet3BackToBackInverted","QCDTailKillerJet3BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet3BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet3BackToBackBaseline","QCDTailKillerJet3BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet3CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInvertedDir ,"QCDTailKillerJet3CollinearInverted","QCDTailKillerJet3CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet3CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaselineDir ,"QCDTailKillerJet3CollinearBaseline","QCDTailKillerJet3CollinearBaseline", 52, 0., 260.); 

    hNBBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaselineDir, "NBBaselineTauIdJet", "NBBaselineTauIdJet", 10, 0., 10.);
    //hNJetBaselineTauIdMet= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaselineDir, "NJetBaselineTauIdJetMet", "NJetBaselineTauIdJetMet", 10, 0., 10.);
    //hNJetBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaselineDir, "NJetBaselineTauIdJet", "NJetBaselineTauIdJet", 20, 0., 20.);
    hDeltaPhiBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaselineDir , "deltaPhiBaseline", "deltaPhi;#Delta#phi", 180, 0., 180.);

//     hDeltaR_TauMETJet1MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInvertedDir, "DeltaR_TauMETJet1MET", "DeltaR_TauMETJet1MET ", 65, 0., 260.);
//     hDeltaR_TauMETJet2MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInvertedDir, "DeltaR_TauMETJet2MET", "DeltaR_TauMETJet2MET ", 65, 0., 260.);
//     hDeltaR_TauMETJet3MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInvertedDir, "DeltaR_TauMETJet3MET", "DeltaR_TauMETJet3MET ", 65, 0., 260.);
//     hDeltaR_TauMETJet4MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInvertedDir, "DeltaR_TauMETJet4MET", "DeltaR_TauMETJet4MET ", 65, 0., 260.);

    // Shapes for closure test systematics for data-driven control plots are done via the extra Common plots objects
    fNormalizationSystematicsSignalRegion.disableCommonPlotsFilledAtEveryStep();
    fNormalizationSystematicsControlRegion.disableCommonPlotsFilledAtEveryStep();
    // Print info about number of booked histograms
    std::cout << iConfig.getParameter<std::string>("@module_label") << std::endl;
    fHistoWrapper.printHistoStatistics();
  }

  SignalAnalysisInvertedTau::~SignalAnalysisInvertedTau() { }

  void SignalAnalysisInvertedTau::produces(edm::EDFilter *producer) const {

  }

  bool SignalAnalysisInvertedTau::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();
    fEventWeight.beginEvent();

//------ Set prescale
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);

//------ Pileup weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
    }
    increment(fAllCounter);

//------ Top pT reweighting
    if(!iEvent.isRealData()) {
      const double topPtWeight = fTopPtWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(topPtWeight);
    }
    increment(fTopPtWeightCounter);

//------ For combining W+Jets inclusive and exclusive samples, do an event weighting here
    if(!iEvent.isRealData()) {
      const double wjetsWeight = fWJetsWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(wjetsWeight);
    }
    increment(fWJetsWeightCounter);

//------ MET (noise) filters for data (reject events with instrumental fake MET)
    if(iEvent.isRealData()) {
      if(!fMETFilters.passedEvent(iEvent, iSetup)) return false;
    }
    increment(fMETFiltersCounter);

//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    GenParticleAnalysis::Data genData;
    if (!iEvent.isRealData()) {
      genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);

    // test for pile-up dependence
    //    if (nVertices > 12 )  return false;
    //    if (nVertices < 13 || nVertices > 18 )  return false;
    //    if (nVertices < 19 )  return false;
    increment(fVertexFilterCounter);

    // Setup common plots

    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);

    fCommonPlots.fillControlPlotsAfterVertexSelection(iEvent, pvData);

//------ Tau candidate selection
    // Do tau-candidate selection
    TauSelection::Data tauCandidateDataTmp = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    if(!tauCandidateDataTmp.passedEvent()) return false; // Require at least one tau
    increment(fTauCandidateCounter);
    edm::PtrVector<pat::Tau> mySelectedTauList = tauCandidateDataTmp.getSelectedTausBeforeIsolation();
    // Apply nprongs cut
    edm::PtrVector<pat::Tau> myTmpVector;
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesNProngsStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    mySelectedTauList = myTmpVector;
    myTmpVector.clear();
    if (!mySelectedTauList.size()) return false; // Require at least one tau passed nprongs cut
    increment(fNprongsAfterTauIDCounter);
    // Apply Rtau cut
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesRtauStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    mySelectedTauList = myTmpVector;
    myTmpVector.clear();
    if (!mySelectedTauList.size()) return false; // Require at least one tau passed rtau cut
    increment(fRtauAfterTauIDCounter);
    // Dirty hack to make code crash if tauCandidateDataTmp.getSelectedTau() is called (i.e. don't use tauCandidateDataTmp beyond this line)
    const_cast<TauSelection::Data*>(&tauCandidateDataTmp)->invalidate();

//------ Select most likely tau candidate for baseline analysis (full tau ID)
    // Construct list of taus which pass isolation
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesIsolationStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    TauSelection::Data tauDataForBaseline;
    bool myMultipleTausPassForBaselineStatus = false;
    if (!myTmpVector.size()) {
      // No tau candidates pass isolation, construct data object
      edm::Ptr<pat::Tau> myZeroPointer;
      tauDataForBaseline = fTauSelection.setSelectedTau(myZeroPointer, false);
    } else {
      // One or more tau candidates pass isolation, construct data object
      edm::Ptr<pat::Tau> mySelectedTau = fTauSelection.selectMostLikelyTau(myTmpVector, pvData.getSelectedVertex()->z());
      tauDataForBaseline = fTauSelection.setSelectedTau(mySelectedTau, true);
      myMultipleTausPassForBaselineStatus = myTmpVector.size() != 1;
    }
    myTmpVector.clear();

//------ Select most likely tau candidate for inverted analysis (full tau ID)
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (!fTauSelection.getPassesIsolationStatusOfTauObject(*iTau)) {
        // Ok, does not pass tau isolation
        if (fLowBoundForQCDInvertedIsolation.size()) {
          if (!fTauSelection.getPassesIsolationStatusOfTauObject(*iTau, fLowBoundForQCDInvertedIsolation)) {
            // Does not pass tau isolation, but passes a looser isolation, select this tau
            myTmpVector.push_back(*iTau);
          }
        } else {
          // No low bound required, select this tau
          myTmpVector.push_back(*iTau);
        }
      }
    }
    TauSelection::Data tauDataForInverted;
    bool myMultipleTausPassForInvertedStatus = false;
    if (!myTmpVector.size() || myTmpVector.size() != mySelectedTauList.size()) {
      // No tau candidates or a tau candidate passes isolation (i.e. fails inversion), construct data object
      edm::Ptr<pat::Tau> myZeroPointer;
      tauDataForInverted = fTauSelection.setSelectedTau(myZeroPointer, false);
      hOneProngRtauPassedInvertedTaus->Fill(0);
    } else {
      // All tau candidates are non-isolated, construct data object
      edm::Ptr<pat::Tau> mySelectedTau = fTauSelection.selectMostLikelyTau(myTmpVector, pvData.getSelectedVertex()->z());
      tauDataForInverted = fTauSelection.setSelectedTau(mySelectedTau, true);
      myMultipleTausPassForInvertedStatus = myTmpVector.size() != 1;
      hOneProngRtauPassedInvertedTaus->Fill(myTmpVector.size());
    }
    myTmpVector.clear();

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // baseline (full tauID) selection (use same counters like for signal analysis to be able to cross-check)
    if (tauDataForBaseline.passedEvent()) {
      if (!fTauSelection.passesDecayModeFilter(tauDataForBaseline.getSelectedTau())) return false;
      increment(fBaselineTauIDCounter);
      // Match tau to MC
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauDataForBaseline.getSelectedTau()));
      // Require that genuine tau has been selected
      if (bSelectOnlyGenuineTausForMC && !iEvent.isRealData()) {
        if (!tauMatchData.isGenuineTau()) return false;
      }
      // Now re-initialize common plots with the correct selection for tau (affects jet selection, b-tagging, type I MET, delta phi cuts)
      fCommonPlots.initialize(iEvent, iSetup, pvData, tauDataForBaseline, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
      // Initialize also normalization systematics plotting
      fNormalizationSystematicsSignalRegion.initialize(iEvent, iSetup, pvData, tauDataForBaseline, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
      fNormalizationSystematicsSignalRegion.setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, tauDataForBaseline, fMETSelection);

      // Do not fill histograms (keep them for the inverted part), but set info for splitting the phase space
      fCommonPlots.setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, tauDataForBaseline, fMETSelection);
      // Apply scale factor for fake tau
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauDataForBaseline.getSelectedTau()->eta()));
      }
      increment(fBaselineTauFakeScaleFactorCounter);
      // Apply scale factor tau part of trigger
      if (!iEvent.isRealData()) {
        const TauTriggerEfficiencyScaleFactor::Data tauTriggerWeightData = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauDataForBaseline.getSelectedTau()), iEvent.isRealData(), fEventWeight);
      }
      increment(fBaselineTauTriggerScaleFactorCounter);
      // Check if multiple taus passed
      if (!myMultipleTausPassForBaselineStatus) increment(fBaselineOneTauCounter);
      // Do baseline analysis
      return doBaselineAnalysis(iEvent, iSetup, tauDataForBaseline.getSelectedTau(), tauMatchData, pvData, genData);
    }
    // end of baseline selection
    ////////////////////////////////////////////////////////////////////////////////////////////////

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // Inverted tau selection starts (do here common plots)
    if (tauDataForInverted.passedEvent()) {
      if (!fTauSelection.passesDecayModeFilter(tauDataForInverted.getSelectedTau())) return false;
      increment(fInvertedTauIDCounter);
      // Match tau to MC
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauDataForInverted.getSelectedTau()));
      // Require that genuine tau has been selected
      if (bSelectOnlyGenuineTausForMC && !iEvent.isRealData()) {
        if (!tauMatchData.isGenuineTau()) return false;
      }
      // Now re-initialize common plots with the correct selection for tau (affects jet selection, b-tagging, type I MET, delta phi cuts)
      fCommonPlots.initialize(iEvent, iSetup, pvData, tauDataForInverted, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
      fCommonPlots.fillControlPlotsAfterTauSelection(iEvent, iSetup, tauDataForInverted, tauMatchData, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller);
      // Initialize also normalization systematics plotting
      fNormalizationSystematicsControlRegion.initialize(iEvent, iSetup, pvData, tauDataForInverted, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
      fNormalizationSystematicsControlRegion.setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, tauDataForInverted, fMETSelection);

      // Apply scale factor for fake tau
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauDataForInverted.getSelectedTau()->eta()));
      }
      increment(fInvertedTauFakeScaleFactorCounter);
      // Apply scale factor tau part of trigger
      if (!iEvent.isRealData()) {
        const TauTriggerEfficiencyScaleFactor::Data tauTriggerWeightData = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauDataForInverted.getSelectedTau()), iEvent.isRealData(), fEventWeight);
      }
      increment(fInvertedTauTriggerScaleFactorCounter);
      // Check if multiple taus passed
      if (!myMultipleTausPassForInvertedStatus) increment(fInvertedOneTauCounter);

      fCommonPlots.fillControlPlotsAfterTauTriggerScaleFactor(iEvent);
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterTauID, tauDataForInverted.getSelectedTau()->pt());
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtaAfterTauID, tauDataForInverted.getSelectedTau()->eta());
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauPhiAfterTauID, tauDataForInverted.getSelectedTau()->phi());
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauRtauAfterTauID, tauDataForInverted.getSelectedTauRtauValue());
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauLeadingTrackPtAfterTauID, tauDataForInverted.getSelectedTau()->leadPFChargedHadrCand()->pt());

      // Apply additional weights
      if (bMakeEtaCorrectionStatus) {
        double myCorrectionWeight = getQCDEtaCorrectionFactor(tauDataForInverted.getSelectedTau()->eta());
        fEventWeight.multiplyWeight(myCorrectionWeight);
      }
      // tau decay mode reweighting
      fEventWeight.multiplyWeight(tauDataForInverted.getTauDecayModeReweightingFactor());
      // Do inverted analysis
      return doInvertedAnalysis(iEvent, iSetup, tauDataForInverted.getSelectedTau(), tauMatchData, pvData, genData);
    }
    // end of inverted selection
    ////////////////////////////////////////////////////////////////////////////////////////////////

    // Never reached
    return true;
  }

  bool SignalAnalysisInvertedTau::doBaselineAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const FakeTauIdentifier::Data& tauMatchData, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData) {
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();
//------ Veto against second tau in event
    // Implement only, if necessary

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.silentAnalyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false; 
    increment(fBaselineEvetoCounter);

//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.silentAnalyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fBaselineMuvetoCounter);

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.silentAnalyze(iEvent, iSetup, selectedTau, pvData.getNumberOfAllVertices());
    if(!jetData.passedEvent()) return false;
    increment(fBaselineJetsCounter);
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterJets, metDataTmp.getSelectedMET()->et());

//------ MET trigger scale factor (after this step, the MET and its derivatives, such as transverse mass, are physically meaningful)
    if(!metDataTmp.passedPreMetCut()) return false;
    increment(fBaselinePreMETCutCounter);
    if(iEvent.isRealData())
      fMETTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    increment(fBaselineMetTriggerScaleFactorCounter);
    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSF, metDataTmp.getSelectedMET()->et());
    fCommonPlotsBaselineAfterMetSF->fill();

    // Obtain transverse mass for plotting
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET()));
    double deltaPhi = DeltaPhi::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET())) * 57.3; // converted to degrees
    double invariantMass = -1.0;
    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    if (btagDataTmp.passedEvent()) {
      FullHiggsMassCalculator::Data fullHiggsMassData = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagDataTmp, metDataTmp, &genData);
      if (fullHiggsMassData.passedEvent()) {
        invariantMass = fullHiggsMassData.getHiggsMass();
      }
    }
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetSF, transverseMass);

    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();

    if (btagDataTmp.passedEvent()) {
     myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSFPlusBtag, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }
    if (btagDataTmp.getSelectedJets().size() < 1) {
     myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSFPlusBveto, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fBaselineQCDTailKillerCollinearCounter);

    // At this point, let's fill histograms for closure test and for normalisation
    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCuts, metDataTmp.getSelectedMET()->et()); // no btag scale factor needed
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCuts, transverseMass); // no btag scale factor needed
    if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassBaselineTauIdAfterCollinearCuts, invariantMass);
    fCommonPlotsBaselineAfterCollinearCuts->fill();
    if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, metDataTmp.getSelectedMET()->et());
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, transverseMass);
      if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, invariantMass);
      fCommonPlotsBaselineAfterCollinearCutsPlusBackToBackCuts->fill();
    }
    // Fill normalization systematics plots
    fNormalizationSystematicsSignalRegion.fillAllControlPlots(iEvent, transverseMass);
    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    //    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    // double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    hNBBaselineTauIdJet->Fill(btagDataTmp.getSelectedJets().size(), myWeightWithBtagSF);
    if (btagDataTmp.passedEvent()) {
      // mT with b veto in bins
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBtag, transverseMass, myWeightWithBtagSF);
      fCommonPlotsBaselineAfterCollinearCutsPlusBtag->fill();
      if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterCollinearCutsPlusBtagPlusBackToBackCuts->fill();
      }
    }
    if (btagDataTmp.getSelectedJets().size() < 1) {
      // mT with b veto in bins
      myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBveto, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBveto, transverseMass, myWeightWithBtagSF);
      fCommonPlotsBaselineAfterCollinearCutsPlusBveto->fill();
      if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterCollinearCutsPlusBvetoPlusBackToBackCuts->fill();
      }
    }

//------ b tagging cut
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    BjetSelection::Data bjetSelectionData = fBjetSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metDataTmp.getSelectedMET());
    TopSelectionManager::Data topSelectionData = fTopSelectionManager.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
    FullHiggsMassCalculator::Data fullHiggsMassDataTmp = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagData, metDataTmp, &genData);
    if (btagData.passedEvent()) increment(fBaselineBtagCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    // Beyond this point, the b tag scale factor has already been applied
    if(!btagData.passedEvent()) {
      // Inverted btag control region
      if (qcdTailKillerDataCollinear.passedBackToBackCuts() && metDataTmp.passedEvent() && topSelectionData.passedEvent()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdFinalReversedBtag, transverseMass);
        if (fullHiggsMassDataTmp.passedEvent()) {
          myHandler.fillShapeHistogram(hInvMassBaselineTauIdFinalReversedBtag, fullHiggsMassDataTmp.getHiggsMass());
        }
      }
      return false;
    }
    increment(fBaselineBTaggingScaleFactorCounter);
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterBtag, transverseMass);
    fCommonPlotsBaselineAfterMETAndBtagWithSF->fill();
    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBtag, metDataTmp.getSelectedMET()->et());

//------ MET cut
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    if(!metData.passedEvent()) return false;
    increment(fBaselineMetCounter);

    // mT after jets and met in bins
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMet, transverseMass);
    fCommonPlotsBaselineAfterMet->fill();
    if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetPlusBackToBackCuts, transverseMass);
      fCommonPlotsBaselineAfterMetPlusBackToBackCuts->fill();
    }

    // mT with b veto in bins
    if (btagDataTmp.getSelectedJets().size() < 1) { 
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetPlusBveto, transverseMass, myWeightWithBtagSF);
      fCommonPlotsBaselineAfterMetPlusBveto->fill();
      // mT with b veto and deltaPhi cuts in bins
      if (qcdTailKillerDataCollinear.passedEvent()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterMetPlusBvetoPlusBackToBackCuts->fill();
      }
    }

    // MT for closure test with soft b tagging  
    if (btagDataTmp.getSelectedSubLeadingJets().size() > 0) {
      if (qcdTailKillerDataCollinear.passedEvent()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterMetPlusSoftBtaggingPlusBackToBackCuts->fill();
      }
    }

//------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    if (!qcdTailKillerData.passedBackToBackCuts()) {
      // Inverted back-to-back delta phi control region
      if (topSelectionData.passedEvent()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdFinalReversedBacktoBackDeltaPhi, transverseMass);
        if (fullHiggsMassDataTmp.passedEvent()) {
          myHandler.fillShapeHistogram(hInvMassBaselineTauIdFinalReversedBacktoBackDeltaPhi, fullHiggsMassDataTmp.getHiggsMass());
        }
      }
      return false;
    }
    increment(fBaselineQCDTailKillerBackToBackCounter);

//    hQCDTailKillerJet0BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(0)); // Make control plot before cut
//    hQCDTailKillerJet1BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(1)); // Make control plot before cut
//    hQCDTailKillerJet2BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut
//    hQCDTailKillerJet3BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(3)); // Make control plot before cut

    // Top reconstruction
    if (!(topSelectionData.passedEvent())) return false;
    increment(fBaselineTopSelectionCounter);
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterTopReco, transverseMass);

    // top mass with possible event cuts


    // delta phi cuts
    hDeltaPhiBaseline->Fill(deltaPhi);
    if (deltaPhi < fDeltaPhiCutValue ) increment(fBaselineDeltaPhiTauMETCounter);

    // mT with b tagging and deltaPhi cuts 
    //    myHandler.fillShapeHistogram(hMTBaselineTauIdPhi, transverseMass);
    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterBackToBackCuts, transverseMass);

    increment(fBaselineSelectedEventsCounter);
    fCommonPlotsBaselineAfterBackToBackCuts->fill();
    return true;
  }

  ////////////////////////////////////////////////////////////////////////////////////

  bool SignalAnalysisInvertedTau::doInvertedAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const FakeTauIdentifier::Data& tauMatchData, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData) {
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();
//------ Veto against second tau in event
    // Implement only, if necessary
    //fCommonPlots.fillControlPlotsAtTauVetoSelection(iEvent, iSetup, vetoTauData);
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterTauVeto, selectedTau->pt());

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    fCommonPlots.fillControlPlotsAtElectronSelection(iEvent, electronVetoData);
    if (!electronVetoData.passedEvent()) return false;
    increment(fInvertedElectronVetoCounter);

//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    fCommonPlots.fillControlPlotsAtMuonSelection(iEvent, muonVetoData);
    if (!muonVetoData.passedEvent()) return false;
    increment(fInvertedMuonVetoCounter);

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, selectedTau, pvData.getNumberOfAllVertices());
    if(!jetData.passedEvent()) return false;
    fCommonPlots.fillControlPlotsAtJetSelection(iEvent, jetData);
    increment(fInvertedNJetsCounter);
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    myHandler.fillShapeHistogram(hMETInvertedTauIdAfterJets, metDataTmp.getSelectedMET()->et());

//------ MET trigger scale factor (after this step, the MET and its derivatives, such as transverse mass, are physically meaningful)
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    if(!metDataTmp.passedPreMetCut()) return false;
    increment(fInvertedPreMETCutCounter);
    if(iEvent.isRealData())
      fMETTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    increment(fInvertedMetTriggerScaleFactorCounter);

    //    hSelectedTauEtJetCut->Fill(selectedTau->pt());

    fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(iEvent);
    fCommonPlotsInvertedAfterMetSF->fill();
    // Obtain transverse mass and invariant mass for plotting
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET()));
    double deltaPhi = DeltaPhi::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET())) * 57.3; // converted to degrees
    double invariantMass = -1.0;
    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    if (btagDataTmp.passedEvent()) {
      FullHiggsMassCalculator::Data fullHiggsMassData = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagDataTmp, metDataTmp, &genData);
      if (fullHiggsMassData.passedEvent()) {
        invariantMass = fullHiggsMassData.getHiggsMass();
      }
    }
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterJetCut, selectedTau->pt());
    myHandler.fillShapeHistogram(hMETInvertedTauIdAfterMetSF, metDataTmp.getSelectedMET()->et());
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMetSF, transverseMass);

    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    if(btagDataTmp.passedEvent()) {
      myHandler.fillShapeHistogram(hMETInvertedTauIdAfterMetSFPlusBtag, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

    if( btagDataTmp.getSelectedJets().size() < 1) {
      myHandler.fillShapeHistogram(hMETInvertedTauIdAfterMetSFPlusBveto, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, qcdTailKillerDataCollinear);
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fInvertedQCDTailKillerCollinearCounter);
    fCommonPlotsInvertedAfterCollinearCuts->fill();

    // At this point, let's fill histograms for closure test and for normalisation
    BjetSelection::Data bjetSelectionDataTmp = fBjetSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagDataTmp.getSelectedJets(), selectedTau, metDataTmp.getSelectedMET());
    TopSelectionManager::Data topSelectionDataTmp = fTopSelectionManager.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagDataTmp.getSelectedJets(), bjetSelectionDataTmp.getBjetTopSide(), bjetSelectionDataTmp.passedEvent());
    FullHiggsMassCalculator::Data fullHiggsMassDataTmp = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagDataTmp, metDataTmp, &genData);

    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterCollinearCuts, selectedTau->pt());
    myHandler.fillShapeHistogram(hMETInvertedTauIdAfterCollinearCuts, metDataTmp.getSelectedMET()->et());
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCuts, transverseMass);
    if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassInvertedTauIdAfterCollinearCuts, invariantMass);
    if (qcdTailKillerDataCollinear.passedBackToBackCuts() && metDataTmp.passedEvent() && topSelectionDataTmp.passedEvent()) { // Pass also back-to-back cuts and MET cut
      myHandler.fillShapeHistogram(hMETInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, metDataTmp.getSelectedMET()->et());
      myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, transverseMass);
      if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassInvertedTauIdAfterCollinearCutsPlusBackToBackCuts, invariantMass);
      fCommonPlotsInvertedAfterCollinearCutsPlusBackToBackCuts->fill();
    }
    // Fill normalization systematics plots
    fNormalizationSystematicsControlRegion.fillAllControlPlots(iEvent, transverseMass);

    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    //    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    //    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    // MT with b tagging
    if(btagDataTmp.passedEvent()) {
      increment(fInvertedBTaggingBeforeMETCounter); // NOTE: Will not give correct value for MC because btag SF is not applied
      myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCutsPlusBtag, transverseMass, myWeightWithBtagSF);
      fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
      if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
      }
    }
    // MT with b veto
    if( btagDataTmp.getSelectedJets().size() < 1) {
      increment(fInvertedBjetVetoCounter);// NOTE: Will not give correct value for MC because btag SF is not applied
      myHandler.fillShapeHistogram(hMETInvertedTauIdAfterCollinearCutsPlusBveto, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
      myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCutsPlusBveto, transverseMass, myWeightWithBtagSF);
      fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
      if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        myHandler.fillShapeHistogram(hMTInvertedTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsInvertedAfterCollinearCutsPlusBvetoPlusBackToBackCuts->fill();
      }
    }

    //------ b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());

    // Apply scale factor as weight to event
    if (btagData.passedEvent()) increment(fInvertedBTaggingCounter);

    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    // Beyond this point, the b tag scale factor has already been applied
    fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
    if (!btagData.passedEvent()) {
      // Inverted btag control region
      if (metDataTmp.passedEvent() && qcdTailKillerDataCollinear.passedBackToBackCuts() && topSelectionDataTmp.passedEvent()) {
        myHandler.fillShapeHistogram(hMTInvertedTauIdFinalReversedBtag, transverseMass);
        if (fullHiggsMassDataTmp.passedEvent()) {
          myHandler.fillShapeHistogram(hInvMassInvertedTauIdFinalReversedBtag, fullHiggsMassDataTmp.getHiggsMass());
        }
      }
      return false;
    }
    increment(fInvertedBTaggingScaleFactorCounter);

    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterBtagging, selectedTau->pt());
    fCommonPlotsInvertedAfterMETAndBtagWithSF->fill();
    myHandler.fillShapeHistogram(hMETInvertedTauIdAfterCollinearCutsPlusBtag, metDataTmp.getSelectedMET()->et());

    // mt for inverted tau with b tagging
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterBtag, transverseMass);
    // deltaPhi with b tagging
    myHandler.fillShapeHistogram(hDeltaPhiInverted, deltaPhi);
    hTransverseMassVsDphi->Fill(transverseMass,deltaPhi);

    //------ ttbar topology selected
    fCommonPlots.fillControlPlotsAfterTopologicalSelections(iEvent);

    //------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
    if(!metData.passedEvent()) return false;
    increment(fInvertedMetCounter);


    // Tau properties for inverted selection after MET cut
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterMetCut, selectedTau->pt());
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtaAfterMetCut, selectedTau->eta());
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauPhiAfterMetCut, selectedTau->phi());
    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauRtauAfterMetCut, fTauSelection.getRtauOfTauObject(selectedTau));


    myHandler.fillShapeHistogram(hNBInvertedTauIdJet, btagDataTmp.getSelectedJets().size());

    // mt for inverted tau before b tagging
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMet, transverseMass);
    fCommonPlotsInvertedAfterMet->fill();
    // deltaPhi before b tagging
    myHandler.fillShapeHistogram(hDeltaPhiInvertedNoB, deltaPhi);
    if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      // mt  before b tagging with deltaPhi for factorising b tagging 
      myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMetPlusBackToBackCuts, transverseMass);
      myHandler.fillShapeHistogram(hNBInvertedTauIdJetDphi, btagDataTmp.getSelectedJets().size());
      fCommonPlotsInvertedAfterMetPlusBackToBackCuts->fill();
    }

    // mt with b veto
    if( btagDataTmp.getSelectedJets().size() < 1) {
      increment(fInvertedBvetoCounter); // NOTE: incorrect count because no btag scale factor has been applied
      myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterBjetVeto, selectedTau->pt(), myWeightWithBtagSF);
      myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMetPlusBveto, transverseMass, myWeightWithBtagSF);
      fCommonPlotsInvertedAfterMetPlusBveto->fill();
      // mt  with b veto and deltaPhi
      if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        //    if ( deltaPhiMetJet1 > Rcut && deltaPhiMetJet2 > Rcut && deltaPhiMetJet3 > Rcut  ) {
        increment(fInvertedBvetoDeltaPhiCounter);  // NOTE: incorrect count because no btag scale factor has been applied
        myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterBjetVetoPhiCuts, selectedTau->pt(), myWeightWithBtagSF);
        myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsInvertedAfterMetPlusBvetoPlusBackToBackCuts->fill();
      }
    }

    // MT for closure test with soft b tagging  
    if( btagDataTmp.getSelectedSubLeadingJets().size() > 0) {  
      if (qcdTailKillerDataCollinear.passedEvent()) {
        myHandler.fillShapeHistogram(hMTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsInvertedAfterMetPlusSoftBtaggingPlusBackToBackCuts->fill();
      }
    }

    //------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
    if (!qcdTailKillerData.passedBackToBackCuts()) {
      // Inverted back-to-back delta phi control region
      if (topSelectionDataTmp.passedEvent()) {
        myHandler.fillShapeHistogram(hMTInvertedTauIdFinalReversedBacktoBackDeltaPhi, transverseMass);
        if (fullHiggsMassDataTmp.passedEvent()) {
          myHandler.fillShapeHistogram(hInvMassInvertedTauIdFinalReversedBacktoBackDeltaPhi, fullHiggsMassDataTmp.getHiggsMass());
        }
      }
      return false;
    }
    increment(fInvertedQCDTailKillerBackToBackCounter);

//     hQCDTailKillerJet0BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(0)); // Make control plot before cut 
//     hQCDTailKillerJet1BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut 
//     hQCDTailKillerJet2BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut 
//     hQCDTailKillerJet3BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(3)); // Make control plot before cut 


    // mT with deltaPhi(tau,met)
    if (deltaPhi < fDeltaPhiCutValue) {
      increment(fInvertedDeltaPhiTauMETCounter);
    }


    myHandler.fillShapeHistogram(hInvertedTauIdSelectedTauEtAfterBackToBackCuts, selectedTau->pt());
    myHandler.fillShapeHistogram(hMETInvertedTauIdAfterBackToBackCuts, metData.getSelectedMET()->et());
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterBackToBackCuts, transverseMass);
    fCommonPlotsInvertedAfterBackToBackCuts->fill();

    // Top reconstruction
    BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metData.getSelectedMET());
    TopSelectionManager::Data topSelectionData = fTopSelectionManager.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
    fCommonPlots.fillControlPlotsAtTopSelection(iEvent, topSelectionData);
    if (!(topSelectionData.passedEvent())) return false;
    increment(fInvertedTopSelectionCounter);
    myHandler.fillShapeHistogram(hMTInvertedTauIdAfterTopReco, transverseMass);

    // top mass with possible event cuts

    // All selections passed
    fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, transverseMass);
    increment(fInvertedSelectedEventsCounter);

    //------ Invariant Higgs mass
    FullHiggsMassCalculator::Data fullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, selectedTau, btagData, metData, &genData);
    if (!fullHiggsMassData.passedEvent()) return false;
    fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, fullHiggsMassData);
    increment(fInvertedSelectedEventsInvariantMassCounter);
    //double HiggsMass = fullHiggsMassData.getHiggsMass();
    //if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);
    //hHiggsMass->Fill(selectedTau->pt(), HiggsMass);

    if(transverseMass < 80 ) increment(ftransverseMassCut80Counter);

    if(transverseMass < 100 ) increment(ftransverseMassCut100Counter);

    return true;
  }

  double SignalAnalysisInvertedTau::getQCDEtaCorrectionFactor(double tauEta) {
    // Experimental code
    Double_t xAxis[23] = {-2.5, -2, -1.8, -1.6, -1.4, -1.2, -1, -0.8, -0.6, -0.4, -0.2, -0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.5};
    if (tauEta < xAxis[1]) return 0.8767081;
    if (tauEta < xAxis[2]) return 0.9659707;
    if (tauEta < xAxis[3]) return 1.137967;
    if (tauEta < xAxis[4]) return 1.311167;
    if (tauEta < xAxis[5]) return 1.095265;
    if (tauEta < xAxis[6]) return 0.9898405;
    if (tauEta < xAxis[7]) return 0.9719643;
    if (tauEta < xAxis[8]) return 0.937053;
    if (tauEta < xAxis[9]) return 0.908424;
    if (tauEta < xAxis[10]) return 0.9101083;
    if (tauEta < xAxis[11]) return 0.8675937;
    if (tauEta < xAxis[12]) return 0.9433836;
    if (tauEta < xAxis[13]) return 0.8938621;
    if (tauEta < xAxis[14]) return 0.934237;
    if (tauEta < xAxis[15]) return 0.8606384;
    if (tauEta < xAxis[16]) return 0.9480098;
    if (tauEta < xAxis[17]) return 1.096861;
    if (tauEta < xAxis[18]) return 1.248765;
    if (tauEta < xAxis[19]) return 1.157337;
    if (tauEta < xAxis[20]) return 1.122231;
    if (tauEta < xAxis[21]) return 1.067155;
    if (tauEta < xAxis[22]) return 0.9381483;
    throw cms::Exception("eta correction factor") << "This part should not be reached! eta = " << tauEta;
    return 1.0;
  }

}
