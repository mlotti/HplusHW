#include "EventSelection/interface/CommonPlots.h"

CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper)
: fEnableGenuineTauHistograms(config.getParameter<bool>("enableGenuineTauHistograms")),
  // Analysis type
  fAnalysisType(type),
  // HistoWrapper
  fHistoWrapper(histoWrapper),
  // Histogram splitter
  fHistoSplitter(config, histoWrapper),
  // Settings for histogram binning
  fNVerticesBinSettings(config.getParameter<ParameterSet>("nVerticesBins")),
  fPtBinSettings(config.getParameter<ParameterSet>("ptBins")),
  fEtaBinSettings(config.getParameter<ParameterSet>("etaBins")),
  fPhiBinSettings(config.getParameter<ParameterSet>("phiBins")),
  fDeltaPhiBinSettings(config.getParameter<ParameterSet>("deltaPhiBins")),
  fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
  fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
  fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
  fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins")),
  fAngularCuts1DSettings(config.getParameter<ParameterSet>("angularCuts1DBins")),
  //fTopMassBinSettings(config.getParameter<ParameterSet>("topMassBins")),
  //fWMassBinSettings(config.getParameter<ParameterSet>("WMassBins")),
  fMtBinSettings(config.getParameter<ParameterSet>("mtBins"))
  //fInvmassBinSettings(config.getParameter<ParameterSet>("invmassBins")),
{ }

CommonPlots::~CommonPlots() { }

void CommonPlots::book(TDirectory *dir) { 
  fHistoSplitter.bookHistograms(dir);
  // Create directories for data driven control plots
  std::string myLabel = "ForDataDrivenCtrlPlots";
  std::string myFakeLabel = "ForDataDrivenCtrlPlotsEWKFakeTaus";
  if (fAnalysisType == kQCDNormalizationSystematicsSignalRegion) {
    myLabel += "QCDNormalizationSignal";
    myFakeLabel += "QCDNormalizationSignal";
  }
  if (fAnalysisType == kQCDNormalizationSystematicsControlRegion) {
    myLabel += "QCDNormalizationControl";
    myFakeLabel += "QCDNormalizationControl";
  }
  TDirectory* myCtrlDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myLabel);
  TDirectory* myCtrlEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myFakeLabel);
  std::vector<TDirectory*> myDirs = {myCtrlDir, myCtrlEWKFakeTausDir};
  // Create histograms
  
  // vertex

  // tau selection

  // tau trigger SF

  // veto tau selection
  
  // electron veto
  
  // muon veto

  // jet selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNjets, 
    "Njets", "Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // MET trigger SF
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNjetsAfterJetSelectionAndMETSF,
    "NjetsAfterJetSelectionAndMETSF", "Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // collinear angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlCollinearAngularCutsMinimum, 
    "CollinearAngularCutsMinimum", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet1, 
    "CollinearAngularCutsJet1", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet2, 
    "CollinearAngularCutsJet2", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet3, 
    "CollinearAngularCutsJet3", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet4, 
    "CollinearAngularCutsJet4", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  // this is the point of "standard selections"
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterStdSelections, 
    "NVertices_AfterStandardSelections", "N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterStdSelections, 
    "SelectedTau_pT_AfterStandardSelections", "#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterStdSelections, 
    "SelectedTau_eta_AfterStandardSelections", "#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterStdSelections, 
    "SelectedTau_phi_AfterStandardSelections", "#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterStdSelections, 
    "SelectedTau_etaphi_AfterStandardSelections", "#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterStdSelections, 
    "SelectedTau_ldgTrkPt_AfterStandardSelections", "#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterStdSelections, 
    "SelectedTau_DecayMode_AfterStandardSelections", "#tau decay mode;N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterStdSelections, 
    "SelectedTau_Rtau_AfterStandardSelections", "R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNJetsAfterStdSelections, 
    "Njets_AfterStandardSelections", "Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetPtAfterStdSelections, 
    "JetPt_AfterStandardSelections", "Selected jets p_{T}, GeV/c;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterStdSelections, 
    "JetEta_AfterStandardSelections", "Selected jets #eta;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterStdSelections, 
    "JetEtaPhi_AfterStandardSelections", "Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // MET
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMET, 
    "MET", "MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETPhi, 
    "METPhi", "MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // b tagging
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNBJets, 
    "NBjets", "Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetPt, 
    "BJetPt", "Selected b jets p_{T}, GeV/c;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetEta, 
    "BJetEta", "Selected b jets #eta;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBDiscriminator, 
    "BtagDiscriminator", "b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  // back-to-back angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBackToBackAngularCutsMinimum, 
    "BackToBackAngularCutsMinimum", "min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet1, 
    "BackToBackAngularCutsJet1", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet2, 
    "BackToBackAngularCutsJet2", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet3, 
    "BackToBackAngularCutsJet3", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet4, 
    "BackToBackAngularCutsJet4", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  // control plots after all selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterAllSelections, 
    "NVertices_AfterAllSelections", "N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterAllSelections, 
    "SelectedTau_pT_AfterAllSelections", "#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterAllSelections, 
    "SelectedTau_eta_AfterAllSelections", "#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterAllSelections, 
    "SelectedTau_phi_AfterAllSelections", "#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterAllSelections, 
    "SelectedTau_etaphi_AfterAllSelections", "#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterAllSelections, 
    "SelectedTau_ldgTrkPt_AfterAllSelections", "#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterAllSelections, 
    "SelectedTau_DecayMode_AfterAllSelections", "#tau decay mode;N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterAllSelections, 
    "SelectedTau_Rtau_AfterAllSelections", "R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNJetsAfterAllSelections, 
    "Njets_AfterAllSelections", "Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetPtAfterAllSelections, 
    "JetPt_AfterAllSelections", "Selected jets p_{T}, GeV/c;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterAllSelections, 
    "JetEta_AfterAllSelections", "Selected jets #eta;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterAllSelections, 
    "JetEtaPhi_AfterAllSelections", "Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlCollinearAngularCutsMinimumAfterAllSelections, 
    "CollinearAngularCutsMinimum_AfterAllSelections", "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETAfterAllSelections, 
    "MET_AfterAllSelections", "MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETPhiAfterAllSelections,
    "METPhi_AfterAllSelections", "MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNBJetsAfterAllSelections,
    "NBjets_AfterAllSelections", "Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetPtAfterAllSelections,
    "BJetPt_AfterAllSelections", "Selected b jets p_{T}, GeV/c;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetEtaAfterAllSelections,
    "BJetEta_AfterAllSelections", "Selected b jets #eta;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBDiscriminatorAfterAllSelections, 
    "BtagDiscriminator_AfterAllSelections", "b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBackToBackAngularCutsMinimumAfterAllSelections, 
    "BackToBackAngularCutsMinimum_AfterAllSelections", "min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlDeltaPhiTauMetAfterAllSelections, 
    "DeltaPhiTauMet_AfterAllSelections", "#Delta#phi(#tau,MET), {}^{#circ};N_{events}", 
    36, 0, 180);
  
  // shape plots after all selections
  if (fAnalysisType != kQCDNormalizationSystematicsSignalRegion && fAnalysisType != kQCDNormalizationSystematicsControlRegion) {
    fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hShapeTransverseMass, 
      "shapeTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}",
      fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
    fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kVital, myDirs, hShapeProbabilisticBtagTransverseMass, 
      "shapeTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}",
      fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
  }
}

//===== unique filling methods (to be called inside the event selection routine only)
void CommonPlots::fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data) {
  fElectronData = data;
}

void CommonPlots::fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data) {
  fMuonData = data;
}

void CommonPlots::fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data) {
  fJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjets, bIsFakeTau, fJetData.getNumberOfSelectedJets());
}

void CommonPlots::fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data) {
  fCollinearAngularCutsData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsMinimum, bIsFakeTau, fCollinearAngularCutsData.getMinimumCutValue()); 
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet1, bIsFakeTau, fCollinearAngularCutsData.get1DCutVariable(0));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet2, bIsFakeTau, fCollinearAngularCutsData.get1DCutVariable(1));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet3, bIsFakeTau, fCollinearAngularCutsData.get1DCutVariable(2));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet4, bIsFakeTau, fCollinearAngularCutsData.get1DCutVariable(3));
}

void CommonPlots::fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data) {
  fBJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJets, bIsFakeTau, fBJetData.getNumberOfSelectedBJets());
  for (auto& p: fBJetData.getSelectedBJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPt, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEta, bIsFakeTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminator, bIsFakeTau, p.bjetDiscriminator());
  }
}

void CommonPlots::fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data) {
  fMETData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMET, bIsFakeTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhi, bIsFakeTau, fMETData.getMET().phi());
}

void CommonPlots::fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data) {
  fBackToBackAngularCutsData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsMinimum, bIsFakeTau, fBackToBackAngularCutsData.getMinimumCutValue());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet1, bIsFakeTau, fBackToBackAngularCutsData.get1DCutVariable(0));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet2, bIsFakeTau, fBackToBackAngularCutsData.get1DCutVariable(1));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet3, bIsFakeTau, fBackToBackAngularCutsData.get1DCutVariable(2));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet4, bIsFakeTau, fBackToBackAngularCutsData.get1DCutVariable(3));
}

//===== unique filling methods (to be called AFTER return statement from analysis routine)
void CommonPlots::fillControlPlotsAfterTauTriggerScaleFactor(const Event& event, const TauSelection::Data& data, bool isFakeTau) {
  fTauData = data;
  bIsFakeTau = isFakeTau;
}

void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjetsAfterJetSelectionAndMETSF, bIsFakeTau, fJetData.getNumberOfSelectedJets());
}

void CommonPlots::fillControlPlotsAfterTopologicalSelections(const Event& event) {
  // I.e. plots after standard selections
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterStdSelections, bIsFakeTau, iVertices);
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().eta());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().phi());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().lTrkPt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().decayModeFinding());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, bIsFakeTau, fTauData.getRtauOfSelectedTau());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterStdSelections, bIsFakeTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterStdSelections, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterStdSelections, bIsFakeTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterStdSelections, bIsFakeTau, p.eta(), p.phi());
  }
}

void CommonPlots::fillControlPlotsAfterAllSelections(const Event& event, double transverseMass) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, bIsFakeTau, iVertices);
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().eta());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().phi());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().lTrkPt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().decayModeFinding());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, bIsFakeTau, fTauData.getRtauOfSelectedTau());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterAllSelections, bIsFakeTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterAllSelections, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterAllSelections, bIsFakeTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterAllSelections, bIsFakeTau, p.eta(), p.phi());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsMinimumAfterAllSelections, bIsFakeTau, fCollinearAngularCutsData.getMinimumCutValue());

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETAfterAllSelections, bIsFakeTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhiAfterAllSelections, bIsFakeTau, fMETData.getMET().phi());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJetsAfterAllSelections, bIsFakeTau, fBJetData.getNumberOfSelectedBJets());
  for (auto& p: fBJetData.getSelectedBJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPtAfterAllSelections, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEtaAfterAllSelections, bIsFakeTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterAllSelections, bIsFakeTau, p.bjetDiscriminator());
  }
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsMinimumAfterAllSelections, bIsFakeTau, fBackToBackAngularCutsData.getMinimumCutValue());

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlDeltaPhiTauMetAfterAllSelections, bIsFakeTau, fBackToBackAngularCutsData.getDeltaPhiTauMET());
  
  fHistoSplitter.fillShapeHistogramTriplet(hShapeTransverseMass, bIsFakeTau, transverseMass);
}

void CommonPlots::fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, double transverseMass) {
  fHistoSplitter.fillShapeHistogramTriplet(hShapeProbabilisticBtagTransverseMass, bIsFakeTau, transverseMass);
}

