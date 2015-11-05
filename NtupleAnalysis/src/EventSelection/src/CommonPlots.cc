#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/TransverseMass.h"
#include "DataFormat/interface/Event.h"

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

void CommonPlots::book(TDirectory *dir, bool isData) { 
  fHistoSplitter.bookHistograms(dir);
  // Create directories for data driven control plots
  std::string myLabel = "ForDataDrivenCtrlPlots";
  std::string myFakeLabel = "ForDataDrivenCtrlPlotsEWKFakeTaus";
  std::string myGenuineLabel = "ForDataDrivenCtrlPlotsEWKGenuineTaus";
  if (fAnalysisType == kQCDNormalizationSystematicsSignalRegion) {
    myLabel += "QCDNormalizationSignal";
    myFakeLabel += "QCDNormalizationSignal";
    myGenuineLabel += "QCDNormalizationSignal";
  }
  if (fAnalysisType == kQCDNormalizationSystematicsControlRegion) {
    myLabel += "QCDNormalizationControl";
    myFakeLabel += "QCDNormalizationControl";
    myGenuineLabel += "QCDNormalizationControl";
  }
  TDirectory* myCtrlDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myLabel);
  TDirectory* myCtrlEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myFakeLabel);
  TDirectory* myCtrlGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs2 = {myCtrlDir, myCtrlEWKFakeTausDir};
  std::vector<TDirectory*> myDirs3 = {myCtrlDir, myCtrlEWKFakeTausDir, myCtrlGenuineTausDir};
  std::vector<TDirectory*> myDirs;
  if (fEnableGenuineTauHistograms) {
    for (auto& p: myDirs3)
      myDirs.push_back(p);
  } else {
    for (auto& p: myDirs2)
      myDirs.push_back(p);
  }
    
  // Create histograms
  
  // vertex

  // tau selection

  // tau trigger SF

  // veto tau selection
  
  // electron veto
  
  // muon veto

  // jet selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNjets, 
    "Njets", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // MET trigger SF
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNjetsAfterJetSelectionAndMETSF,
    "NjetsAfterJetSelectionAndMETSF", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // collinear angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlCollinearAngularCutsMinimum, 
    "CollinearAngularCutsMinimum", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet1, 
    "CollinearAngularCutsJet1", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet2, 
    "CollinearAngularCutsJet2", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet3, 
    "CollinearAngularCutsJet3", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet4, 
    "CollinearAngularCutsJet4", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  // this is the point of "standard selections"
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterStdSelections, 
    "NVertices_AfterStandardSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterStdSelections, 
    "SelectedTau_pT_AfterStandardSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterStdSelections, 
    "SelectedTau_eta_AfterStandardSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterStdSelections, 
    "SelectedTau_phi_AfterStandardSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterStdSelections, 
    "SelectedTau_etaphi_AfterStandardSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterStdSelections, 
    "SelectedTau_ldgTrkPt_AfterStandardSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterStdSelections, 
    "SelectedTau_DecayMode_AfterStandardSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterStdSelections, 
    "SelectedTau_Nprongs_AfterStandardSelections", ";N_{prongs};N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterStdSelections, 
    "SelectedTau_Rtau_AfterStandardSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauSourceAfterStdSelections, 
    "SelectedTau_source_AfterStandardSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());
  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) {
    fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterStdSelections, i+1, fHelper.getTauSourceBinLabel(i));
  }
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNJetsAfterStdSelections, 
    "Njets_AfterStandardSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetPtAfterStdSelections, 
    "JetPt_AfterStandardSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterStdSelections, 
    "JetEta_AfterStandardSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterStdSelections, 
    "JetEtaPhi_AfterStandardSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // MET
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMET, 
    "MET", ";MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETPhi, 
    "METPhi", ";MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // b tagging
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNBJets, 
    "NBjets", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetPt, 
    "BJetPt", ";Selected b jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetEta, 
    "BJetEta", ";Selected b jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBDiscriminator, 
    "BtagDiscriminator", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  // back-to-back angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBackToBackAngularCutsMinimum, 
    "BackToBackAngularCutsMinimum", ";min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet1, 
    "BackToBackAngularCutsJet1", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet2, 
    "BackToBackAngularCutsJet2", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet3, 
    "BackToBackAngularCutsJet3", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet4, 
    "BackToBackAngularCutsJet4", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  // control plots after all selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNVerticesAfterAllSelections, 
    "NVertices_AfterAllSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPtAfterAllSelections, 
    "SelectedTau_pT_AfterAllSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauEtaAfterAllSelections, 
    "SelectedTau_eta_AfterAllSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauPhiAfterAllSelections, 
    "SelectedTau_phi_AfterAllSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterAllSelections, 
    "SelectedTau_etaphi_AfterAllSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauLdgTrkPtAfterAllSelections, 
    "SelectedTau_ldgTrkPt_AfterAllSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauDecayModeAfterAllSelections, 
    "SelectedTau_DecayMode_AfterAllSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauNProngsAfterAllSelections, 
    "SelectedTau_Nprongs_AfterAllSelections", ";N_{prongs};N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauRtauAfterAllSelections, 
    "SelectedTau_Rtau_AfterAllSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauSourceAfterAllSelections, 
    "SelectedTau_source_AfterAllSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());
  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) {
    fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterAllSelections, i+1, fHelper.getTauSourceBinLabel(i));
  }
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlSelectedTauIPxyAfterAllSelections, 
    "SelectedTau_IPxy_AfterAllSelections", ";IP_{T} (cm);N_{events}",
    100, 0, 0.2);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNJetsAfterAllSelections, 
    "Njets_AfterAllSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetPtAfterAllSelections, 
    "JetPt_AfterAllSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlJetEtaAfterAllSelections, 
    "JetEta_AfterAllSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterAllSelections, 
    "JetEtaPhi_AfterAllSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlCollinearAngularCutsMinimumAfterAllSelections, 
    "CollinearAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETAfterAllSelections, 
    "MET_AfterAllSelections", ";MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlMETPhiAfterAllSelections,
    "METPhi_AfterAllSelections", ";MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlNBJetsAfterAllSelections,
    "NBjets_AfterAllSelections", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetPtAfterAllSelections,
    "BJetPt_AfterAllSelections", ";Selected b jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBJetEtaAfterAllSelections,
    "BJetEta_AfterAllSelections", ";Selected b jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBDiscriminatorAfterAllSelections, 
    "BtagDiscriminator_AfterAllSelections", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlBackToBackAngularCutsMinimumAfterAllSelections, 
    "BackToBackAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fDeltaPhiBinSettings.bins(), fDeltaPhiBinSettings.min(), fDeltaPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kVital, myDirs, hCtrlDeltaPhiTauMetAfterAllSelections, 
    "DeltaPhiTauMet_AfterAllSelections", ";#Delta#phi(#tau,MET), {}^{#circ};N_{events}", 
    36, 0, 180);
  
  // shape plots after all selections
  if (fAnalysisType != kQCDNormalizationSystematicsSignalRegion && fAnalysisType != kQCDNormalizationSystematicsControlRegion) {
    fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeTransverseMass, 
      "shapeTransverseMass", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
      fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
    fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeProbabilisticBtagTransverseMass, 
      "shapeTransverseMassProbabilisticBTag", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
      fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
  }
  if (isData) {
    hNSelectedVsRunNumber = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, 
      "NSelectedVsRunNumber", "NSelectedVsRunNumber;Run number;N_{events}", 14000, 246000, 260000);
  }
}

void CommonPlots::initialize() {
  iVertices = -1;
  fTauData = TauSelection::Data();
  //FakeTauIdentifier::Data fFakeTauData;
  bIsFakeTau = false;
  fElectronData = ElectronSelection::Data();
  fMuonData = MuonSelection::Data();
  fJetData = JetSelection::Data();
  fCollinearAngularCutsData = AngularCutsBackToBack::Data();
  fBJetData = BJetSelection::Data();
  fMETData = METSelection::Data();
  fBackToBackAngularCutsData = AngularCutsCollinear::Data();
  fHistoSplitter.initialize();
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
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminator, bIsFakeTau, p.bjetDiscriminator());
  }
  for (auto& p: fBJetData.getSelectedBJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPt, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEta, bIsFakeTau, p.eta());
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
void CommonPlots::fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data) {
  // Code logic: if there is no identified tau (or anti-isolated tau for QCD), the code will for sure crash later
  // This piece of code is called from TauSelection, so there one cannot judge if things go right or not, 
  // that kind of check needs to be done in the analysis code (i.e. cut away event if tau selection is not passed)
  fTauData = data;
  if (event.isData()) {
    bIsFakeTau = false;
    return;
  }
  if (isQCDMeasurement()) {
    if (data.hasAntiIsolatedTaus()) {
      bIsFakeTau = !(data.getAntiIsolatedTauIsGenuineTau());
    }
  } else {
    if (data.hasIdentifiedTaus()) {
      bIsFakeTau = !(data.isGenuineTau());
    }
  }
}

void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjetsAfterJetSelectionAndMETSF, bIsFakeTau, fJetData.getNumberOfSelectedJets());
}

void CommonPlots::fillControlPlotsAfterTopologicalSelections(const Event& event) {
  // I.e. plots after standard selections
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterStdSelections, bIsFakeTau, iVertices);
  if (isQCDMeasurement()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, bIsFakeTau, fTauData.getRtauOfAntiIsolatedTau());
    for (auto p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, bIsFakeTau, p);
    }
  } else {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, bIsFakeTau, fTauData.getSelectedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, bIsFakeTau, fTauData.getRtauOfSelectedTau());
    for (auto p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, bIsFakeTau, p);
    }
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterStdSelections, bIsFakeTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterStdSelections, bIsFakeTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterStdSelections, bIsFakeTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterStdSelections, bIsFakeTau, p.eta(), p.phi());
  }
}

void CommonPlots::fillControlPlotsAfterAllSelections(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, bIsFakeTau, iVertices);
  if (isQCDMeasurement()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, bIsFakeTau, fTauData.getRtauOfAntiIsolatedTau());
    for (auto p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, bIsFakeTau, p);
    }
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, bIsFakeTau, fTauData.getAntiIsolatedTau().IPxy());
  } else {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().lChTrkPt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().decayMode());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().nProngs());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, bIsFakeTau, fTauData.getRtauOfSelectedTau());
    for (auto p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, bIsFakeTau, p);
    }
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, bIsFakeTau, fTauData.getSelectedTau().IPxy());
  }
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
  double myTransverseMass = -1.0;
  if (isQCDMeasurement()) {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getAntiIsolatedTau(), fMETData.getMET());
  } else {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getSelectedTau(), fMETData.getMET());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hShapeTransverseMass, bIsFakeTau, myTransverseMass);
  
  if (event.isData()) {
    hNSelectedVsRunNumber->Fill(event.eventID().run());
  }
}

void CommonPlots::fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight) {
  double myTransverseMass = -1.0;
  if (isQCDMeasurement()) {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getAntiIsolatedTau(), metData.getMET());
  } else {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getSelectedTau(), metData.getMET());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hShapeProbabilisticBtagTransverseMass, bIsFakeTau, myTransverseMass, btagWeight);
}
