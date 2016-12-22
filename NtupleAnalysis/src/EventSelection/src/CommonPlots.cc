#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/TransverseMass.h"
#include "EventSelection/interface/PUDependencyPlots.h"
#include "DataFormat/interface/Event.h"


CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper)
: fEnableGenuineTauHistograms(true), // Needed always for limits
  //fEnableGenuineTauHistograms(config.getParameter<bool>("enableGenuineTauHistograms")),
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
  fDeltaRBinSettings(config.getParameter<ParameterSet>("deltaRBins")),
  fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
  fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
  fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
  fHtBinSettings(config.getParameter<ParameterSet>("htBins")),
  fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins")),
  fAngularCuts1DSettings(config.getParameter<ParameterSet>("angularCuts1DBins")),
  //fTopMassBinSettings(config.getParameter<ParameterSet>("topMassBins")),
  //fWMassBinSettings(config.getParameter<ParameterSet>("WMassBins")),
  fMtBinSettings(config.getParameter<ParameterSet>("mtBins")),
  //fInvmassBinSettings(config.getParameter<ParameterSet>("invmassBins")),
  hNSelectedVsRunNumber(nullptr)
{ 
  // Create CommonPlotsBase objects
  bool enableStatus = config.getParameter<bool>("enablePUDependencyPlots");
  if (fAnalysisType == kQCDNormalizationSystematicsSignalRegion || fAnalysisType == kQCDNormalizationSystematicsControlRegion) {
    enableStatus = false;
  }
  fPUDependencyPlots = new PUDependencyPlots(histoWrapper, enableStatus, fNVerticesBinSettings);
  fBaseObjects.push_back(fPUDependencyPlots);
}

CommonPlots::~CommonPlots() {
  fHistoSplitter.deleteHistograms(hCtrlNjets);
  fHistoSplitter.deleteHistograms(hCtrlNjetsAfterJetSelectionAndMETSF);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsMinimum);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsJet1);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsJet2);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsJet3);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsJet4);
  fHistoSplitter.deleteHistograms(hCtrlNVerticesAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauEtaPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauLdgTrkPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauDecayModeAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauNProngsAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauRtauAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauSourceAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlNJetsAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlMET);
  fHistoSplitter.deleteHistograms(hCtrlMETPhi);
  fHistoSplitter.deleteHistograms(hCtrlNBJets);
  fHistoSplitter.deleteHistograms(hCtrlBJetPt);
  fHistoSplitter.deleteHistograms(hCtrlBJetEta);
  fHistoSplitter.deleteHistograms(hCtrlBDiscriminator);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsMinimum);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsJet1);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsJet2);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsJet3);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsJet4);
  fHistoSplitter.deleteHistograms(hCtrlNVerticesAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauPhiAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauEtaPhiAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauLdgTrkPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauDecayModeAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauNProngsAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauRtauAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauSourceAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedTauIPxyAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlNJetsAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaPhiAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMinDeltaPhiJetMHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMaxDeltaPhiJetMHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMinDeltaRJetMHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMinDeltaRReversedJetMHTAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlCollinearAngularCutsMinimumAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMETAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlMETPhiAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlNBJetsAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlBJetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlBJetEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlBDiscriminatorAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlBackToBackAngularCutsMinimumAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlDeltaPhiTauMetAfterAllSelections);
  fHistoSplitter.deleteHistograms(hShapeTransverseMass);
  fHistoSplitter.deleteHistograms(hShapeProbabilisticBtagTransverseMass);
  if (hNSelectedVsRunNumber != nullptr) delete hNSelectedVsRunNumber;
  for (auto p: fBaseObjects) delete p;
}

void CommonPlots::book(TDirectory *dir, bool isData) { 
  fHistoSplitter.bookHistograms(dir);
  // Create directories for data driven control plots
  std::string myLabel = "ForDataDrivenCtrlPlots";
  std::string myFakeLabel = "ForDataDrivenCtrlPlotsEWKFakeTaus";
  std::string myGenuineLabel = "ForDataDrivenCtrlPlotsEWKGenuineTaus";
  if (fAnalysisType == kQCDNormalizationSystematicsSignalRegion) {
    myLabel += "QCDNormalizationSignal";
    myFakeLabel += "QCDNormalizationSignalEWKFakeTaus";
    myGenuineLabel += "QCDNormalizationSignalEWKGenuineTaus";
  }
  if (fAnalysisType == kQCDNormalizationSystematicsControlRegion) {
    myLabel += "QCDNormalizationControl";
    myFakeLabel += "QCDNormalizationControlEWKFakeTaus";
    myGenuineLabel += "QCDNormalizationControlEWKGenuineTaus";
  }
  TDirectory* myCtrlDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myLabel);
  TDirectory* myCtrlEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myCtrlGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs2 = {myCtrlDir, myCtrlEWKFakeTausDir};
  std::vector<TDirectory*> myDirs3 = {myCtrlDir, myCtrlEWKFakeTausDir, myCtrlGenuineTausDir};
  std::vector<TDirectory*> myDirs;
  
  ////Needed for TauIDSyst
  auto dirName = dir->GetName();
  std::string str(dirName);

  tauIDup=false;
  tauIDdown=false;

  if(str.std::string::find("TauIDSystPlus") != std::string::npos){
        tauIDup=true;
  }
  if(str.std::string::find("TauIDSystMinus")!= std::string::npos){
        tauIDdown=true;
  }



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

  // tau veto

  // jet selection
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNjets, 
    "Njets", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // MET trigger SF
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNjetsAfterJetSelectionAndMETSF,
    "NjetsAfterJetSelectionAndMETSF", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  // collinear angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlCollinearAngularCutsMinimum, 
    "CollinearAngularCutsMinimum", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet1, 
    "CollinearAngularCutsJet1", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet2, 
    "CollinearAngularCutsJet2", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet3, 
    "CollinearAngularCutsJet3", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlCollinearAngularCutsJet4, 
    "CollinearAngularCutsJet4", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());

  // this is the point of "standard selections"
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNVerticesAfterStdSelections, 
    "NVertices_AfterStandardSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauPtAfterStdSelections, 
    "SelectedTau_pT_AfterStandardSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauEtaAfterStdSelections, 
    "SelectedTau_eta_AfterStandardSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauPhiAfterStdSelections, 
    "SelectedTau_phi_AfterStandardSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterStdSelections, 
    "SelectedTau_etaphi_AfterStandardSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauLdgTrkPtAfterStdSelections, 
    "SelectedTau_ldgTrkPt_AfterStandardSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauDecayModeAfterStdSelections, 
    "SelectedTau_DecayMode_AfterStandardSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauNProngsAfterStdSelections, 
    "SelectedTau_Nprongs_AfterStandardSelections", ";N_{prongs};N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauRtauAfterStdSelections, 
    "SelectedTau_Rtau_AfterStandardSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauSourceAfterStdSelections, 
    "SelectedTau_source_AfterStandardSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());
  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) {
    fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterStdSelections, i+1, fHelper.getTauSourceBinLabel(i));
  }
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNJetsAfterStdSelections, 
    "Njets_AfterStandardSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlJetPtAfterStdSelections, 
    "JetPt_AfterStandardSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlJetEtaAfterStdSelections, 
    "JetEta_AfterStandardSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterStdSelections, 
    "JetEtaPhi_AfterStandardSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // MET
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMET, 
    "MET", ";MET, GeV;N_{events}", 
    fHtBinSettings.bins(), fHtBinSettings.min(), fHtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETPhi, 
    "METPhi", ";MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  // b tagging
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNBJets, 
    "NBjets", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetPt, 
    "BJetPt", ";Selected b jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetEta, 
    "BJetEta", ";Selected b jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBDiscriminator, 
    "BtagDiscriminator", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  // back-to-back angular cuts
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBackToBackAngularCutsMinimum, 
    "BackToBackAngularCutsMinimum", ";min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet1, 
    "BackToBackAngularCutsJet1", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet2, 
    "BackToBackAngularCutsJet2", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{2},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet3, 
    "BackToBackAngularCutsJet3", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{3},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlBackToBackAngularCutsJet4, 
    "BackToBackAngularCutsJet4", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{4},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());

  // control plots after all selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNVerticesAfterAllSelections, 
    "NVertices_AfterAllSelections", ";N_{vertices};N_{events}",
    fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauPtAfterAllSelections, 
    "SelectedTau_pT_AfterAllSelections", ";#tau p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauEtaAfterAllSelections, 
    "SelectedTau_eta_AfterAllSelections", ";#tau #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauPhiAfterAllSelections, 
    "SelectedTau_phi_AfterAllSelections", ";#tau #phi;N_{events}",
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedTauEtaPhiAfterAllSelections, 
    "SelectedTau_etaphi_AfterAllSelections", ";#tau #eta;#tau #phi;",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauLdgTrkPtAfterAllSelections, 
    "SelectedTau_ldgTrkPt_AfterAllSelections", ";#tau ldg. trk p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauDecayModeAfterAllSelections, 
    "SelectedTau_DecayMode_AfterAllSelections", ";#tau decay mode;N_{events}",
    20, 0, 20);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauNProngsAfterAllSelections, 
    "SelectedTau_Nprongs_AfterAllSelections", ";N_{prongs};N_{events}",
    10, 0, 10);
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauRtauAfterAllSelections, 
    "SelectedTau_Rtau_AfterAllSelections", ";R_{#tau};N_{events}",
    fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauSourceAfterAllSelections, 
    "SelectedTau_source_AfterAllSelections", ";;N_{events}",
    fHelper.getTauSourceBinCount(), 0, fHelper.getTauSourceBinCount());
  for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) {
    fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterAllSelections, i+1, fHelper.getTauSourceBinLabel(i));
  }
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauIPxyAfterAllSelections, 
    "SelectedTau_IPxy_AfterAllSelections", ";IP_{T} (cm);N_{events}",
    100, 0, 0.2);

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNJetsAfterAllSelections, 
    "Njets_AfterAllSelections", ";Number of selected jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlJetPtAfterAllSelections, 
    "JetPt_AfterAllSelections", ";Selected jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlJetEtaAfterAllSelections, 
    "JetEta_AfterAllSelections", ";Selected jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlJetEtaPhiAfterAllSelections, 
    "JetEtaPhi_AfterAllSelections", ";Selected jets #eta;Selected jets #phi",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  
  // Experimental
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlHTAfterAllSelections, 
    "HT_AfterAllSelections", ";H_{T}, GeV;N_{events}",
     fHtBinSettings.bins(), fHtBinSettings.min(), fHtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMHTAfterAllSelections, 
    "MHT_AfterAllSelections", ";MHT, GeV;N_{events}",
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMinDeltaPhiJetMHTAfterAllSelections, 
    "MinDeltaPhiJetMHT_AfterAllSelections", ";min(#Delta#phi(jet_{i}, MHT-jet_{i}));N_{events}",
    fPhiBinSettings.bins(), 0.0, fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMaxDeltaPhiJetMHTAfterAllSelections, 
    "MaxDeltaPhiJetMHT_AfterAllSelections", ";max(#Delta#phi(jet_{i}, MHT-jet_{i}));N_{events}",
    fPhiBinSettings.bins(), 0.0, fPhiBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMinDeltaRJetMHTAfterAllSelections, 
    "MinDeltaRJetMHT_AfterAllSelections", ";min(#DeltaR(jet_{i}, MHT-jet_{i}));N_{events}",
    fDeltaRBinSettings.bins(), 0.0, fDeltaRBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMinDeltaRReversedJetMHTAfterAllSelections, 
    "MinDeltaRJetMHTReversed_AfterAllSelections", ";min(#DeltaR(-jet_{i}, MHT-jet_{i}));N_{events}",
    fDeltaRBinSettings.bins(), 0.0, fDeltaRBinSettings.max());
  // End of experimental
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlCollinearAngularCutsMinimumAfterAllSelections, 
    "CollinearAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETAfterAllSelections, 
    "MET_AfterAllSelections", ";MET, GeV;N_{events}", 
    fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETPhiAfterAllSelections,
    "METPhi_AfterAllSelections", ";MET #phi;N_{events}", 
    fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNBJetsAfterAllSelections,
    "NBjets_AfterAllSelections", ";Number of selected b jets;N_{events}",
    fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetPtAfterAllSelections,
    "BJetPt_AfterAllSelections", ";Selected b jets p_{T}, GeV/c;N_{events}",
    fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetEtaAfterAllSelections,
    "BJetEta_AfterAllSelections", ";Selected b jets #eta;N_{events}",
    fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBDiscriminatorAfterAllSelections, 
    "BtagDiscriminator_AfterAllSelections", ";b tag discriminator;N_{events}",
    fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());
  
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBackToBackAngularCutsMinimumAfterAllSelections, 
    "BackToBackAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
    fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlDeltaPhiTauMetAfterAllSelections, 
    "DeltaPhiTauMet_AfterAllSelections", ";#Delta#phi(#tau,MET), {}^{#circ};N_{events}", 
    36, 0, 180);
  
  // shape plots after all selections
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeTransverseMass, 
    "shapeTransverseMass", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
    fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeProbabilisticBtagTransverseMass, 
    "shapeTransverseMassProbabilisticBTag", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
    fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());

  if (isData) {
    hNSelectedVsRunNumber = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, 
      "NSelectedVsRunNumber", "NSelectedVsRunNumber;Run number;N_{events}", 14000, 246000, 260000);
  }
  
  for (auto& p: fBaseObjects) {
    p->book(dir, isData);
  }
}

void CommonPlots::initialize() {
  iVertices = -1;
  fTauData = TauSelection::Data();
  //FakeTauIdentifier::Data fFakeTauData;
  bIsGenuineTau = false;
  fElectronData = ElectronSelection::Data();
  fMuonData = MuonSelection::Data();
  fJetData = JetSelection::Data();
  fCollinearAngularCutsData = AngularCutsBackToBack::Data();
  fBJetData = BJetSelection::Data();
  fMETData = METSelection::Data();
  fBackToBackAngularCutsData = AngularCutsCollinear::Data();
  fHistoSplitter.initialize();
  
  for (auto& p: fBaseObjects) {
    p->reset();
  }
}

//===== unique filling methods (to be called inside the event selection routine only)
void CommonPlots::fillControlPlotsAtVertexSelection(const Event& event) {
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtVertexSelection(event);
  } 
}

void CommonPlots::fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data) {
  fElectronData = data;
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtElectronSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data) {
  fMuonData = data;
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtMuonSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data) {
  fTauData = data;
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtTauSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data) {
  fJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjets, bIsGenuineTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtJetSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data) {
  fCollinearAngularCutsData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsMinimum, bIsGenuineTau, fCollinearAngularCutsData.getMinimumCutValue()); 
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet1, bIsGenuineTau, fCollinearAngularCutsData.get1DCutVariable(0));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet2, bIsGenuineTau, fCollinearAngularCutsData.get1DCutVariable(1));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet3, bIsGenuineTau, fCollinearAngularCutsData.get1DCutVariable(2));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsJet4, bIsGenuineTau, fCollinearAngularCutsData.get1DCutVariable(3));
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtAngularCutsCollinear(event, data);
  }
}

void CommonPlots::fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data) {
  fBJetData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJets, bIsGenuineTau, fBJetData.getNumberOfSelectedBJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminator, bIsGenuineTau, p.bjetDiscriminator());
  }
  for (auto& p: fBJetData.getSelectedBJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPt, bIsGenuineTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEta, bIsGenuineTau, p.eta());
  }
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtBtagging(event, data);
  }
}

void CommonPlots::fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data) {
  fMETData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMET, bIsGenuineTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhi, bIsGenuineTau, fMETData.getMET().phi());
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtMETSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data) {
  fBackToBackAngularCutsData = data;
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsMinimum, bIsGenuineTau, fBackToBackAngularCutsData.getMinimumCutValue());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet1, bIsGenuineTau, fBackToBackAngularCutsData.get1DCutVariable(0));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet2, bIsGenuineTau, fBackToBackAngularCutsData.get1DCutVariable(1));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet3, bIsGenuineTau, fBackToBackAngularCutsData.get1DCutVariable(2));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsJet4, bIsGenuineTau, fBackToBackAngularCutsData.get1DCutVariable(3));
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAtAngularCutsBackToBack(event, data);
  }
}

//===== unique filling methods (to be called AFTER return statement from analysis routine)
void CommonPlots::fillControlPlotsAfterTrigger(const Event& event) {
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterTrigger(event);
  } 
}

void CommonPlots::fillControlPlotsAfterMETFilter(const Event& event) {
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterMETFilter(event);
  } 
}

void CommonPlots::fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data) {
  // Code logic: if there is no identified tau (or anti-isolated tau for QCD), the code will for sure crash later
  // This piece of code is called from TauSelection, so there one cannot judge if things go right or not, 
  // that kind of check needs to be done in the analysis code (i.e. cut away event if tau selection is not passed)
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterTauSelection(event, data);
  }
  fTauData = data;
  if (event.isData()) {
    bIsGenuineTau = true;
    return;
  }
  if (usesAntiIsolatedTaus()) {
    if (data.hasAntiIsolatedTaus()) {
      bIsGenuineTau = data.getAntiIsolatedTauIsGenuineTau();
    }
  } else {
    if (data.hasIdentifiedTaus()) {
      bIsGenuineTau = data.isGenuineTau();
    }
  }
}

void CommonPlots::fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data) {
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterAntiIsolatedTauSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjetsAfterJetSelectionAndMETSF, bIsGenuineTau, fJetData.getNumberOfSelectedJets());
}

void CommonPlots::fillControlPlotsAfterTopologicalSelections(const Event& event, bool withoutTau) {
  // I.e. plots after standard selections
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterStdSelections, bIsGenuineTau, iVertices);

  if (withoutTau == false)
    {
      if (usesAntiIsolatedTaus()) {
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().pt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().eta());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().lChTrkPt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().decayMode());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().nProngs());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, bIsGenuineTau, fTauData.getRtauOfAntiIsolatedTau());
	for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
	  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, bIsGenuineTau, p);
	}
      } else {
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().pt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().eta());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().lChTrkPt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().decayMode());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterStdSelections, bIsGenuineTau, fTauData.getSelectedTau().nProngs());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterStdSelections, bIsGenuineTau, fTauData.getRtauOfSelectedTau());
	for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
	  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterStdSelections, bIsGenuineTau, p);
	}
      }
    }// if (withoutTau == false)
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterStdSelections, bIsGenuineTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterStdSelections, bIsGenuineTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterStdSelections, bIsGenuineTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterStdSelections, bIsGenuineTau, p.eta(), p.phi());
  }
}

void CommonPlots::fillControlPlotsAfterAllSelections(const Event& event, bool withoutTau) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, bIsGenuineTau, iVertices);

  if (withoutTau == false)
    {
      if (usesAntiIsolatedTaus()) {
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().pt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().eta());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().eta(), fTauData.getAntiIsolatedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().lChTrkPt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().decayMode());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().nProngs());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, bIsGenuineTau, fTauData.getRtauOfAntiIsolatedTau());
	for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getAntiIsolatedTau())) {
	  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, bIsGenuineTau, p);
	}
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, bIsGenuineTau, fTauData.getAntiIsolatedTau().IPxy());
      } else {
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPtAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().pt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().eta());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauPhiAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauEtaPhiAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().eta(), fTauData.getSelectedTau().phi());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauLdgTrkPtAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().lChTrkPt());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauDecayModeAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().decayMode());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauNProngsAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().nProngs());
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauRtauAfterAllSelections, bIsGenuineTau, fTauData.getRtauOfSelectedTau());
	for (auto& p: fHelper.getTauSourceData(!event.isMC(), fTauData.getSelectedTau())) {
	  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauSourceAfterAllSelections, bIsGenuineTau, p);
	}
	fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedTauIPxyAfterAllSelections, bIsGenuineTau, fTauData.getSelectedTau().IPxy());
      }
    } // if (withoutTau == false)

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterAllSelections, bIsGenuineTau, fJetData.getNumberOfSelectedJets());
  for (auto& p: fJetData.getSelectedJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterAllSelections, bIsGenuineTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterAllSelections, bIsGenuineTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterAllSelections, bIsGenuineTau, p.eta(), p.phi());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlHTAfterAllSelections, bIsGenuineTau, fJetData.HT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMHTAfterAllSelections, bIsGenuineTau, std::sqrt(fJetData.MHT().perp2()));
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMinDeltaPhiJetMHTAfterAllSelections, bIsGenuineTau, fJetData.minDeltaPhiJetMHT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMaxDeltaPhiJetMHTAfterAllSelections, bIsGenuineTau, fJetData.maxDeltaPhiJetMHT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMinDeltaRJetMHTAfterAllSelections, bIsGenuineTau, fJetData.minDeltaRJetMHT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMinDeltaRReversedJetMHTAfterAllSelections, bIsGenuineTau, fJetData.minDeltaRReversedJetMHT());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlCollinearAngularCutsMinimumAfterAllSelections, bIsGenuineTau, fCollinearAngularCutsData.getMinimumCutValue());

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETAfterAllSelections, bIsGenuineTau, fMETData.getMET().R());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhiAfterAllSelections, bIsGenuineTau, fMETData.getMET().phi());
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJetsAfterAllSelections, bIsGenuineTau, fBJetData.getNumberOfSelectedBJets());
  for (auto& p: fBJetData.getSelectedBJets()) {
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPtAfterAllSelections, bIsGenuineTau, p.pt());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEtaAfterAllSelections, bIsGenuineTau, p.eta());
    fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterAllSelections, bIsGenuineTau, p.bjetDiscriminator());
  }
  
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlBackToBackAngularCutsMinimumAfterAllSelections, bIsGenuineTau, fBackToBackAngularCutsData.getMinimumCutValue());

  fHistoSplitter.fillShapeHistogramTriplet(hCtrlDeltaPhiTauMetAfterAllSelections, bIsGenuineTau, fBackToBackAngularCutsData.getDeltaPhiTauMET());
  double myTransverseMass = -1.0;


  if (withoutTau == false)
    {
      if (usesAntiIsolatedTaus()) {
	myTransverseMass = TransverseMass::reconstruct(fTauData.getAntiIsolatedTau(), fMETData.getMET());
      } else {
	myTransverseMass = TransverseMass::reconstruct(fTauData.getSelectedTau(), fMETData.getMET());
      }

      // Create the up and down variation for tau ID shape
      // Could probably be done in a nicer way elsewhere...
      
      if(tauIDup && fTauData.hasIdentifiedTaus() &&fTauData.getSelectedTau().pt()>=200){
	fHistoSplitter.fillShapeHistogramTriplet(hShapeTransverseMass, bIsGenuineTau, myTransverseMass, (hShapeTransverseMass[0]->UnprotectedGetWeight()*(1.0+0.2*fTauData.getSelectedTau().pt()/1000.0)));
      }else if(tauIDdown && fTauData.hasIdentifiedTaus() && fTauData.getSelectedTau().pt()>=200){
	fHistoSplitter.fillShapeHistogramTriplet(hShapeTransverseMass, bIsGenuineTau, myTransverseMass, (hShapeTransverseMass[0]->UnprotectedGetWeight()*(1.0-0.2*fTauData.getSelectedTau().pt()/1000.0)));
      }else{
	fHistoSplitter.fillShapeHistogramTriplet(hShapeTransverseMass, bIsGenuineTau, myTransverseMass);
      }
    }// if (withoutTau == false)

  if (event.isData()) {
    hNSelectedVsRunNumber->Fill(event.eventID().run());
  }
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterAllSelections(event);
  }
}

void CommonPlots::fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight) {
  double myTransverseMass = -1.0;
  if (usesAntiIsolatedTaus()) {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getAntiIsolatedTau(), metData.getMET());
  } else {
    myTransverseMass = TransverseMass::reconstruct(fTauData.getSelectedTau(), metData.getMET());
  }
  fHistoSplitter.fillShapeHistogramTriplet(hShapeProbabilisticBtagTransverseMass, bIsGenuineTau, myTransverseMass, btagWeight);
    for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(event, metData, btagWeight);
  }
}

//===== Filling of control plots for determining QCD shape uncertainty
void CommonPlots::fillControlPlotsForQCDShapeUncertainty(const Event& event,
                                                         const AngularCutsBackToBack::Data& collinearAngularCutsData,
                                                         const BJetSelection::Data& bJetData,
                                                         const METSelection::Data& metData,
                                                         const AngularCutsCollinear::Data& backToBackAngularCutsData) {
  fillControlPlotsAfterTopologicalSelections(event);
  // Note that the following methods store the data object as members
  fillControlPlotsAtAngularCutsCollinear(event, collinearAngularCutsData);
  fillControlPlotsAtMETSelection(event, metData);
  fillControlPlotsAtBtagging(event, bJetData);
  fillControlPlotsAtAngularCutsBackToBack(event, backToBackAngularCutsData);
  // Fill plots after final selection
  fillControlPlotsAfterAllSelections(event);
}
