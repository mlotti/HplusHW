// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "FWCore/Framework/interface/Event.h"

namespace HPlus {
  HistogramSettings::HistogramSettings(const edm::ParameterSet& iConfig)
  : fBins(iConfig.getUntrackedParameter<uint32_t>("nBins")),
    fAxisMin(iConfig.getUntrackedParameter<double>("axisMin")),
    fAxisMax(iConfig.getUntrackedParameter<double>("axisMax")) { }
  HistogramSettings::~HistogramSettings() { }

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, AnalysisType analysisType, bool isEmbeddedData) :
    bOptionEnableTauFakeRateAnalysis(iConfig.getUntrackedParameter<bool>("enableTauFakeRateAnalysis")),
    bOptionEnableNormalisationAnalysis(iConfig.getUntrackedParameter<bool>("enableNormalisationAnalysis")),
    bOptionEnableMETOscillationAnalysis(iConfig.getUntrackedParameter<bool>("enableMETOscillationAnalysis")),
    bDisableCommonPlotsFilledAtEveryStep(false),
    fAnalysisType(analysisType),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fSplittedHistogramHandler(iConfig.getUntrackedParameter<edm::ParameterSet>("histogramSplitting"), histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fTauFakeRateAnalysis(0),
    fTauSelection(0),
    fFakeTauIdentifier(0),
    fMetTrgSF(0),
    fPtBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("ptBins")),
    fEtaBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("etaBins")),
    fPhiBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("phiBins")),
    fRtauBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("rtauBins")),
    fNjetsBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("njetsBins")),
    fMetBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("metBins")),
    fTailKiller1DSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("tailKiller1DBins")),
    fTopMassBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("topMassBins")),
    fWMassBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("WMassBins")),
    fMtBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("mtBins")),
    fInvmassBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("invmassBins")),
    fMETPhiOscillationCorrectionAfterTaus(0),
    fMETPhiOscillationCorrectionAfterLeptonVeto(0),
    fMETPhiOscillationCorrectionAfterNjets(0),
    fMETPhiOscillationCorrectionAfterBjets(0),
    fMETPhiOscillationCorrectionAfterAllSelections(0),
    fMETPhiOscillationCorrectionEWKControlRegion(0) {
    // Update analysis type for embedding
    if (isEmbeddedData)
      fAnalysisType = kEmbedding;
    // Create histograms
    createHistograms();
    // Create tau fake rate analysis if asked
    if (bOptionEnableTauFakeRateAnalysis) {
      fTauFakeRateAnalysis = new TauFakeRateAnalysis(histoWrapper);
    }
    // Create objects for normalisation analysis if asked
    if (bOptionEnableNormalisationAnalysis) {
      fNormalisationAnalysisObjects.push_back(new NormalisationDYEnrichedWithGenuineTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationDYEnrichedWithFakeTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationWJetsEnrichedWithGenuineTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationWJetsEnrichedWithFakeTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationTTJetsEnrichedWithGenuineTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationWJetsEnrichedBoostedWH(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationTTJetsEnrichedWithFakeTaus(eventCounter, histoWrapper));
      fNormalisationAnalysisObjects.push_back(new NormalisationTTJetsEnrichedBoostedWH(eventCounter, histoWrapper));
    }
    // Create objects for MET phi oscillation analysis
    if (bOptionEnableMETOscillationAnalysis) {
      fMETPhiOscillationCorrectionAfterTaus = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterTaus");
      fMETPhiOscillationCorrectionAfterLeptonVeto = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterLeptonVeto");
      fMETPhiOscillationCorrectionAfterNjets = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterNjets");
      fMETPhiOscillationCorrectionAfterMETSF = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterMETSF");
      fMETPhiOscillationCorrectionAfterCollinearCuts = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterCollinearCuts");
      fMETPhiOscillationCorrectionAfterBjets = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterBjets");
      fMETPhiOscillationCorrectionAfterAllSelections = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterAllSelections");
      fMETPhiOscillationCorrectionEWKControlRegion = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterAllSelections_EKWControlRegion");
    }
  }

  void CommonPlots::createHistograms() {
    // Create directories for data driven control plots
    TFileDirectory myCtrlDir = fs->mkdir("ForDataDrivenCtrlPlots");
    TFileDirectory myCtrlEWKFakeTausDir = fs->mkdir("ForDataDrivenCtrlPlotsFakeTaus");

    // Create histograms

    // vertex

    // tau selection

    // tau trigger SF
    TFileDirectory myTauDir = fCommonBaseDirectory.mkdir("TausWithSF");
    hTauPhiOscillationX = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationX", "TauPhiOscillationX;N_{vertices};#tau p_{x}, GeV/c", 60, 0., 60., 1200, -300, 300);
    hTauPhiOscillationY = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationY", "TauPhiOscillationY;N_{vertices};#tau p_{y}, GeV/c", 60, 0., 60., 1200, -300, 300);

    // veto tau selection

    // electron veto

    // muon veto

    // jet selection
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNjets,            "Njets", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjets, "Njets", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // MET trigger SF
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNjetsAfterJetSelectionAndMETSF,            "NjetsAfterJetSelectionAndMETSF", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF, "NjetsAfterJetSelectionAndMETSF", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // improved delta phi collinear cuts (currently the point of the std. selections)
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet1,            "ImprovedDeltaPhiCutsJet1Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet2,            "ImprovedDeltaPhiCutsJet2Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet3,            "ImprovedDeltaPhiCutsJet3Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{3},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet4,            "ImprovedDeltaPhiCutsJet4Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{4},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet1, "ImprovedDeltaPhiCutsJet1Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet2, "ImprovedDeltaPhiCutsJet2Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet3, "ImprovedDeltaPhiCutsJet3Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{3},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet4, "ImprovedDeltaPhiCutsJet4Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{4},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    }

    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPtAfterStandardSelections, "SelectedTau_pT_AfterStandardSelections", "#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauEtaAfterStandardSelections, "SelectedTau_eta_AfterStandardSelections", "#tau #eta;N_{events} / 0.1", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPhiAfterStandardSelections, "SelectedTau_phi_AfterStandardSelections", "#tau #phi;N_{events} / 0.087", fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
    hSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(), fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauLeadingTrkPtAfterStandardSelections, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauRtauAfterStandardSelections, "SelectedTau_Rtau_AfterStandardSelections", "R_{#tau};N_{events} / 0.1", fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPAfterStandardSelections, "SelectedTau_p_AfterStandardSelections", "#tau p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauLeadingTrkPAfterStandardSelections, "SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlNjetsAfterStandardSelections, "Njets_AfterStandardSelections", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections, "SelectedTau_pT_AfterStandardSelections", "#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections, "SelectedTau_eta_AfterStandardSelections", "#tau #eta;N_{events} / 0.1", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections, "SelectedTau_phi_AfterStandardSelections", "#tau #phi;N_{events} / 0.087", fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
      hEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_etavsphi_AfterStandardSelections", "#tau #eta;#tau #phi", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(), fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections, "SelectedTau_Rtau_AfterStandardSelections", "R_{#tau};N_{events} / 0.1", fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPAfterStandardSelections, "SelectedTau_p_AfterStandardSelections", "#tau p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections, "SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjetsAfterStandardSelections, "Njets_AfterStandardSelections", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    }

    // MET selection
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlMET,            "MET", "MET, GeV;N_{events}", fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausMET, "MET", "MET, GeV;N_{events}", fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());

    // b tagging
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNbjets,            "NBjets", "Number of identified b jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNbjets, "NBjets", "Number of identified b jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // improved delta phi back to back cuts
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet1,           "ImprovedDeltaPhiCutsJet1BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet2,           "ImprovedDeltaPhiCutsJet2BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet3,           "ImprovedDeltaPhiCutsJet3BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet4,           "ImprovedDeltaPhiCutsJet4BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet1,"ImprovedDeltaPhiCutsJet1BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet2,"ImprovedDeltaPhiCutsJet2BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet3,"ImprovedDeltaPhiCutsJet3BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet4,"ImprovedDeltaPhiCutsJet4BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    }

    // top selection
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital,       myCtrlDir,            hCtrlTopMass, "TopMass", "m_{bqq'}, GeV/c^{2};N_{events}", fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir,            hCtrlTopPt,   "TopPt", "p_{T}(bqq'), GeV/c;N_{events}", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital,       myCtrlDir,            hCtrlWMass,   "WMass", "m_{qq'}, GeV/c^{2};N_{events}", fWMassBinSettings.bins(), fWMassBinSettings.min(), fWMassBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir,            hCtrlWPt,     "WPt", "p_{T}(qq'), GeV/c;N_{events}", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital,       myCtrlEWKFakeTausDir, hCtrlEWKFakeTausTopMass, "TopMass", "m_{bqq'}, GeV/c^{2};N_{events}", fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausTopPt,   "TopPt", "p_{T}(bqq'), GeV/c;N_{events}", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital,       myCtrlEWKFakeTausDir, hCtrlEWKFakeTausWMass,   "WMass", "m_{qq'}, GeV/c^{2};N_{events}", fWMassBinSettings.bins(), fWMassBinSettings.min(), fWMassBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausWPt,     "WPt", "p_{T}(qq'), GeV/c;N_{events}", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    }

    // evt topology

    // all selections
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeTransverseMass,            "shapeTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}", fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeEWKFakeTausTransverseMass, "shapeEWKFakeTausTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}", fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());

    // all selections with full mass
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeFullMass,            "shapeInvariantMass", "m_{H+}, GeV/c^{2};N_{events}", fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeEWKFakeTausFullMass, "shapeEWKFakeTausInvariantMass", "m_{H+}, GeV/c^{2};N_{events}", fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());
  }

  CommonPlots::~CommonPlots() {
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it < hEveryStepHistograms.end(); ++it)
      delete (*it);
    hEveryStepHistograms.clear();
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               VertexSelection::Data& vertexData,
                               TauSelection& tauSelection,
                               FakeTauIdentifier& fakeTauIdentifier,
                               ElectronSelection& eVeto,
                               MuonSelection& muonVeto,
                               JetSelection& jetSelection,
                               METTriggerEfficiencyScaleFactor& metTrgSF,
                               METSelection& metSelection,
                               BTagging& bTagging,
                               QCDTailKiller& qcdTailKiller,
                               BjetSelection& bjetSelection,
                               TopSelectionManager& topSelectionManager,
                               EvtTopology& evtTopology,
                               FullHiggsMassCalculator& fullHiggsMassCalculator) {
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauSelection = &tauSelection;
    fTauData = tauSelection.silentAnalyze(iEvent, iSetup, vertexData.getSelectedVertex()->z());
    initialize(iEvent,iSetup,
               vertexData,
               fTauData,
               fakeTauIdentifier,
               eVeto,
               muonVeto,
               jetSelection,
               metTrgSF,
               metSelection,
               bTagging,
               qcdTailKiller,
               bjetSelection,
               topSelectionManager,
               evtTopology,
               fullHiggsMassCalculator);
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               VertexSelection::Data& vertexData,
                               TauSelection::Data& tauData,
                               FakeTauIdentifier& fakeTauIdentifier,
                               ElectronSelection& eVeto,
                               MuonSelection& muonVeto,
                               JetSelection& jetSelection,
                               METTriggerEfficiencyScaleFactor& metTrgSF,
                               METSelection& metSelection,
                               BTagging& bTagging,
                               QCDTailKiller& qcdTailKiller,
                               BjetSelection& bjetSelection,
                               TopSelectionManager& topSelectionManager,
                               EvtTopology& evtTopology,
                               FullHiggsMassCalculator& fullHiggsMassCalculator) {
    fSplittedHistogramHandler.initialize();
    fFakeTauIdentifier = &fakeTauIdentifier;
    metTrgSF.setRun(iEvent.id().run());
    fMetTrgSF = &metTrgSF;
    // Obtain data objects
    fVertexData = vertexData;
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauData = tauData;
    if (fTauData.passedEvent())
      fFakeTauData = fakeTauIdentifier.silentMatchTauToMC(iEvent, *(fTauData.getSelectedTau()));
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);
    fMuonData = muonVeto.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex());
    if (fTauData.passedEvent())
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fVertexData.getNumberOfAllVertices());
    else
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices());
    fBJetData = bTagging.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());

    // Need to require one tau in the event
    if (fTauData.getSelectedTau().isNull()) {
      fMETData = metSelection.silentAnalyzeNoIsolatedTaus(iEvent, iSetup);
      // Plots do not make sense if no tau has been found
      edm::Ptr<pat::Tau> myZeroTauPointer;
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(&fVertexData, 0, 0, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, 0, 0, 0);
      }
      return;
    }
    // A tau exists beyond this point, now obtain MET with residual type I MET
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, vertexData.getNumberOfAllVertices(), fTauData.getSelectedTau(), fJetData.getAllJets());
    // Obtain improved delta phi cut data object
    fQCDTailKillerData = qcdTailKiller.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getSelectedJetsIncludingTau(), fMETData.getSelectedMET());
    // Obtain top selection object
    BjetSelection::Data bjetSelectionData = bjetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets(), fTauData.getSelectedTau(), fMETData.getSelectedMET());
    fTopData = topSelectionManager.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
    // Do full higgs mass only if tau and b jet was found
    if (fBJetData.passedEvent()) {
      fFullHiggsMassData = fullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fBJetData, fMETData);
    }
//FIXME : add met SF also to every set plots
    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size() && !bDisableCommonPlotsFilledAtEveryStep)
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(&fVertexData, &fTauData, &fFakeTauData, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, &fQCDTailKillerData, &fTopData, &fFullHiggsMassData);
    }
  }

  CommonPlotsFilledAtEveryStep* CommonPlots::createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) {
    // Create and return object, but sneakily save the pointer for later use
    CommonPlotsFilledAtEveryStep* myObject = new CommonPlotsFilledAtEveryStep(fHistoWrapper, fEveryStepDirectory, label, enterSelectionFlowPlot, selectionFlowPlotLabel);
    hEveryStepHistograms.push_back(myObject);
    return myObject;
  }

//------ Control plot filling
  void CommonPlots::fillControlPlotsAfterVertexSelection(const edm::Event& iEvent, const VertexSelection::Data& data) {
    //----- MET phi oscillation
    //fMETData = metSelection.silentAnalyzeNoIsolatedTaus(iEvent, iSetup, fJetData.getAllJets());
    if (bOptionEnableTauFakeRateAnalysis && fTauSelection && fFakeTauIdentifier) {
      fTauFakeRateAnalysis->analyseTauFakeRate(iEvent, fVertexData, *fTauSelection, fTauData, *fFakeTauIdentifier, fJetData);
    }
  }

  void CommonPlots::fillControlPlotsAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData, JetSelection& jetSelection, METSelection& metSelection, BTagging& btagging, QCDTailKiller& qcdTailKiller) {
    fTauData = tauData;
    fFakeTauData = fakeTauData;
    // Obtain all other objects, whose selection depends on the tau
    fJetData = jetSelection.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), fVertexData.getNumberOfAllVertices());
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau(), fJetData.getAllJets());
    fBJetData = btagging.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJetsPt20());
    fQCDTailKillerData = qcdTailKiller.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getSelectedJetsIncludingTau(), fMETData.getSelectedMET());
    // Set splitted bin info
    setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, fTauData, metSelection);
    // Obtain new MET object corresponding to the selected tau
    if (bOptionEnableTauFakeRateAnalysis) {
      // e->tau normalisation
      fTauFakeRateAnalysis->analyseEToTauFakes(fVertexData, tauData, fakeTauData, fElectronData, fMuonData, fJetData, fMETData);
    }
  }

  void CommonPlots::setSplittingOfPhaseSpaceInfoAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, METSelection& metSelection) {
    METSelection::Data metData = metSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau(), fJetData.getAllJets());
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees    
    fSplittedHistogramHandler.setFactorisationBinForEvent(tauData.getSelectedTau()->pt(), tauData.getSelectedTau()->eta(), fVertexData.getNumberOfAllVertices(), myDeltaPhiTauMET);
  }

  void CommonPlots::fillControlPlotsAfterTauTriggerScaleFactor(const edm::Event& iEvent) {
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterTaus->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
    hTauPhiOscillationX->Fill(fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau()->px());
    hTauPhiOscillationY->Fill(fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau()->py());

    // Do normalisation analyses
    if (bOptionEnableNormalisationAnalysis) {
      for (std::vector<NormalisationAnalysis*>::iterator it = fNormalisationAnalysisObjects.begin(); it != fNormalisationAnalysisObjects.end(); ++it) {
        (*it)->analyse(iEvent, fTauData, fFakeTauData, fElectronData, fMuonData, fJetData, fMetTrgSF, fQCDTailKillerData, fMETData, fBJetData);
      }
    }
  }

  void CommonPlots::fillControlPlotsAtTauVetoSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const VetoTauSelection::Data& tauVetoData) {

  }

  void CommonPlots::fillControlPlotsAtElectronSelection(const edm::Event& iEvent, const ElectronSelection::Data& data) {
    fElectronData = data;
  }

  void CommonPlots::fillControlPlotsAtMuonSelection(const edm::Event& iEvent, const MuonSelection::Data& data) {
    fMuonData = data;
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterLeptonVeto->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtJetSelection(const edm::Event& iEvent, const JetSelection::Data& data) {
    fJetData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjets, data.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjets, data.getHadronicJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterNjets->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const edm::Event& iEvent) {
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjetsAfterJetSelectionAndMETSF, fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF, fJetData.getHadronicJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterMETSF->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtCollinearDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i == 0 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet1, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet1, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 1 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet2, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet2, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 2 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet3, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet3, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 3 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet4, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet4, data.getRadiusFromCollinearCorner(i)); // Make control pl
      }
      if (!data.passCollinearCutForJet(i))
        myPassStatus = false;
    }
    // Fill control plots for selected taus after standard selections
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauRtauAfterStandardSelections, fTauData.getSelectedTauRtauValue());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauLeadingTrkPtAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPtAfterStandardSelections, fTauData.getSelectedTau()->pt());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauEtaAfterStandardSelections, fTauData.getSelectedTau()->eta());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPhiAfterStandardSelections, fTauData.getSelectedTau()->phi());
    hSelectedTauEtaVsPhiAfterStandardSelections->Fill(fTauData.getSelectedTau()->eta(), fTauData.getSelectedTau()->phi());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPAfterStandardSelections, fTauData.getSelectedTau()->p());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauLeadingTrkPAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->p());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections, fTauData.getSelectedTauRtauValue());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections, fTauData.getSelectedTau()->pt());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections, fTauData.getSelectedTau()->eta());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections, fTauData.getSelectedTau()->phi());
      hEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections->Fill(fTauData.getSelectedTau()->eta(), fTauData.getSelectedTau()->phi());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPAfterStandardSelections, fTauData.getSelectedTau()->p());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->p());
    }
    // Fill other control plots
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjetsAfterStandardSelections, fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjetsAfterStandardSelections, fJetData.getHadronicJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterCollinearCuts->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtMETSelection(const edm::Event& iEvent, const METSelection::Data& data) {
    fMETData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlMET, data.getSelectedMET()->et());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausMET, data.getSelectedMET()->et());
  }

  void CommonPlots::fillControlPlotsAtBtagging(const edm::Event& iEvent, const BTagging::Data& data) {
    fBJetData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNbjets, data.getBJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNbjets, data.getBJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterBjets->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtBackToBackDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i == 0 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet1, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet1, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 1 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet2, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet2, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 2 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet3, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet3, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 3 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet4, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet4, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      }
    }
  }

  void CommonPlots::fillControlPlotsAtTopSelection(const edm::Event& iEvent, const TopSelectionManager::Data& data) {
    fTopData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlTopMass, data.getTopMass());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlTopPt, data.getTopP4().pt());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlWMass, data.getWMass());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlWPt, data.getWP4().pt());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausTopMass, data.getTopMass());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausTopPt, data.getTopP4().pt());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausWMass, data.getWMass());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausWPt, data.getWP4().pt());
    }
  }

  void CommonPlots::fillControlPlotsAtEvtTopology(const edm::Event& iEvent, const EvtTopology::Data& data) {
    
  }

  void CommonPlots::fillControlPlotsAfterAllSelections(const edm::Event& iEvent, double transverseMass) {
    if (bOptionEnableMETOscillationAnalysis) {
      fMETPhiOscillationCorrectionAfterAllSelections->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
      if (transverseMass < 80.0) {
        fMETPhiOscillationCorrectionEWKControlRegion->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
      }
    }
    //double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fTauData.getSelectedTau()), *(fMETData.getSelectedMET())) * 57.3; // converted to degrees
    fSplittedHistogramHandler.fillShapeHistogram(hShapeTransverseMass, transverseMass);
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hShapeEWKFakeTausTransverseMass, transverseMass);
  }

  void CommonPlots::fillControlPlotsAfterAllSelectionsWithFullMass(const edm::Event& iEvent, FullHiggsMassCalculator::Data& data) {
    fFullHiggsMassData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hShapeFullMass, data.getHiggsMass());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hShapeEWKFakeTausFullMass, data.getHiggsMass());
  }
}
