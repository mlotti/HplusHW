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
    fDeltaEtaBinSettings(config.getParameter<ParameterSet>("deltaEtaBins")),
    fDeltaPhiBinSettings(config.getParameter<ParameterSet>("deltaPhiBins")),
    fDeltaRBinSettings(config.getParameter<ParameterSet>("deltaRBins")),
    fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
    fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
    fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
    fHtBinSettings(config.getParameter<ParameterSet>("htBins")),
    fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins")),
    fAngularCuts1DSettings(config.getParameter<ParameterSet>("angularCuts1DBins")),
    fWMassBinSettings(config.getParameter<ParameterSet>("wMassBins")),
    fTopMassBinSettings(config.getParameter<ParameterSet>("topMassBins")),
    fInvmassBinSettings(config.getParameter<ParameterSet>("invMassBins")),
    fMtBinSettings(config.getParameter<ParameterSet>("mtBins")),
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


CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper, bool test)
  : fEnableGenuineTauHistograms(config.getParameter<bool>("enableGenuineBHistograms")), // means GenuineB for Htb
    fAnalysisType(type),
    fHistoWrapper(histoWrapper),
    fHistoSplitter(config, histoWrapper),
    fNVerticesBinSettings(config.getParameter<ParameterSet>("nVerticesBins")),
    fPtBinSettings(config.getParameter<ParameterSet>("ptBins")),
    fEtaBinSettings(config.getParameter<ParameterSet>("etaBins")),
    fPhiBinSettings(config.getParameter<ParameterSet>("phiBins")),
    fDeltaEtaBinSettings(config.getParameter<ParameterSet>("deltaEtaBins")),
    fDeltaPhiBinSettings(config.getParameter<ParameterSet>("deltaPhiBins")),
    fDeltaRBinSettings(config.getParameter<ParameterSet>("deltaRBins")),
    fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
    fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
    fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
    fHtBinSettings(config.getParameter<ParameterSet>("htBins")),
    fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins")),
    fAngularCuts1DSettings(config.getParameter<ParameterSet>("angularCuts1DBins")),
    fWMassBinSettings(config.getParameter<ParameterSet>("wMassBins")),
    fTopMassBinSettings(config.getParameter<ParameterSet>("topMassBins")),
    fInvmassBinSettings(config.getParameter<ParameterSet>("invMassBins")),
    fMtBinSettings(config.getParameter<ParameterSet>("mtBins")),
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
  fHistoSplitter.deleteHistograms(hCtrlSelectedMuonPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedMuonEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedMuonPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSelectedMuonEtaPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlNJetsAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlJetEtaPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlMETAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlMETPhiAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlDeltaPhiTauMetAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlNBJetsAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlBJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlBJetEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlBDiscriminatorAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlHTAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlMHTAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetDijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetDijetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetTopMassWMassRatioAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetBJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetBJetEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetDijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetDijetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetTopMassWMassRatioAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetBJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetBJetEtaAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTetrajetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTetrajetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTetrajetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTetrajetMassAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlTetrajetBJetPtAfterStdSelections);
  fHistoSplitter.deleteHistograms(hCtrlTetrajetBJetEtaAfterStdSelections);
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
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetDijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetDijetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetTopMassWMassRatioAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetBJetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTrijetBJetEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetDijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetDijetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetTopMassWMassRatioAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetBJetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTrijetBJetEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTetrajetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlLdgTetrajetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTetrajetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlSubldgTetrajetMassAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlTetrajetBJetPtAfterAllSelections);
  fHistoSplitter.deleteHistograms(hCtrlTetrajetBJetEtaAfterAllSelections);
  fHistoSplitter.deleteHistograms(hShapeTransverseMass);
  fHistoSplitter.deleteHistograms(hShapeProbabilisticBtagTransverseMass);
  if (hNSelectedVsRunNumber != nullptr) delete hNSelectedVsRunNumber;
  for (auto p: fBaseObjects) delete p;
}

void CommonPlots::book(TDirectory *dir, bool isData) { 
  fHistoSplitter.bookHistograms(dir);
  // Create directories for data driven control plots
  std::string tausOrB = "Taus";
  if ( (fAnalysisType == kFakeBMeasurement) || (fAnalysisType == kHplus2tbAnalysis) ) tausOrB = "B";

  std::string myLabel = "ForDataDrivenCtrlPlots";
  std::string myFakeLabel = "ForDataDrivenCtrlPlotsEWKFake" + tausOrB;
  std::string myGenuineLabel = "ForDataDrivenCtrlPlotsEWKGenuine" + tausOrB;
  
  if (fAnalysisType == kQCDNormalizationSystematicsSignalRegion) {
    myLabel += "QCDNormalizationSignal";
    myFakeLabel += "QCDNormalizationSignalEWKFake" + tausOrB;
    myGenuineLabel += "QCDNormalizationSignalEWKGenuine" + tausOrB;
  }
  if (fAnalysisType == kQCDNormalizationSystematicsControlRegion) {
    myLabel += "QCDNormalizationControl";
    myFakeLabel += "QCDNormalizationControlEWKFake" + tausOrB;
    myGenuineLabel += "QCDNormalizationControlEWKGenuine" + tausOrB;
  }

  // Create the directories
  TDirectory* myCtrlDir            = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myLabel);
  TDirectory* myCtrlEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myCtrlGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs2 = {myCtrlDir, myCtrlEWKFakeTausDir};
  std::vector<TDirectory*> myDirs3 = {myCtrlDir, myCtrlEWKFakeTausDir, myCtrlGenuineTausDir};
  std::vector<TDirectory*> myDirs;
  
  /// Needed for TauIDSyst
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
  const bool hplus2tb = ( (fAnalysisType == kFakeBMeasurement) || (fAnalysisType == kHplus2tbAnalysis) );
  // vertex

  // tau selection

  // tau trigger SF

  // veto tau selection
  
  // electron veto
  
  // muon veto

  // tau veto


  //==========================================
  // jet selection
  //==========================================
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNjets, 
						   "Njets", ";Number of selected jets;N_{events}",
						   fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
  
  //==========================================
  // MET trigger SF
  //==========================================
  if (!hplus2tb)
    {
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNjetsAfterJetSelectionAndMETSF,
						       "NjetsAfterJetSelectionAndMETSF", ";Number of selected jets;N_{events}",
						       fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    }// if (!hplus2tb)

  
  //==========================================     
  // collinear angular cuts 
  //==========================================
  if (!hplus2tb)
    {
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
    }// if (!hplus2tb)

  //==========================================     
  // standard selections
  //==========================================     
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNVerticesAfterStdSelections, 
						   "NVertices_AfterStandardSelections", ";N_{vertices};N_{events}",
						   fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  //==========================================     
  // standard selections: tau 
  //==========================================     
  if (!hplus2tb)
    {
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
      
      for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) 
	{
	  fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterStdSelections, i+1, fHelper.getTauSourceBinLabel(i));
	}
    } // if (!hplus2tb)

  //========================================== 
  // standard selections: muon
  //==========================================
  if (!hplus2tb)
    {
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedMuonPtAfterStdSelections, 
						       "SelectedMu_pT_AfterStandardSelections", ";#mu p_{T}, GeV/c;N_{events}",
						       fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedMuonEtaAfterStdSelections, 
						       "SelectedMu_eta_AfterStandardSelections", ";#mu #eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedMuonPhiAfterStdSelections, 
						       "SelectedMu_phi_AfterStandardSelections", ";#mu #phi;N_{events}",
						       fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kInformative, myDirs, hCtrlSelectedMuonEtaPhiAfterStdSelections, 
						       "SelectedMu_etaphi_AfterStandardSelections", ";#mu #eta;#mu #phi;",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(),
						       fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
    }// if (!hplus2tb)

  //==========================================
  // standard selections: jets  
  //==========================================
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

  if (hplus2tb)
    {
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNBJetsAfterStdSelections, 
						       "NBjets_AfterStandardSelections", ";Number of selected b jets;N_{events}",
						       fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetPtAfterStdSelections, 
						       "BjetPt_AfterStandardSelections", ";Selected b jets p_{T}, GeV/c;N_{events}",
						       fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBJetEtaAfterStdSelections, 
						       "BjetEta_AfterStandardSelections", ";Selected b jets #eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBDiscriminatorAfterStdSelections, 
						       "BtagDiscriminator_AfterStandardSelections", ";b tag discriminator;N_{events}",
						       fBJetDiscriminatorBinSettings.bins(), fBJetDiscriminatorBinSettings.min(), fBJetDiscriminatorBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlHTAfterStdSelections, 
						       "HT_AfterStandardSelections", ";H_{T}, GeV;N_{events}",
						       fHtBinSettings.bins(), fHtBinSettings.min(), fHtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMHTAfterStdSelections, 
						       "MHT_AfterStandardSelections", ";MHT, GeV;N_{events}",
						       fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetPtAfterStdSelections,
						       "LdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}", 						       
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetDijetPtAfterStdSelections,
						       "LdgTrijetDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetDijetMassAfterStdSelections,
						       "LdgTrijetDijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetMassAfterStdSelections,
						       "LdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetTopMassWMassRatioAfterStdSelections,
						       "LdgTrijetTopMassWMassRatioAfterStandardSelections", ";R_{32}", 100 , 0.0, 10.0);

      fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterStdSelections, 
						       "LdgTrijetPt_Vs_LdgTrijetDijetPtAfterStandardSelections" ,";p_{T} (GeV/c);p_{T} (GeV/c)",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max(), 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetBJetPtAfterStdSelections,
						       "LdgTrijetBjetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetBJetEtaAfterStdSelections,
						       "LdgTrijetBjetEta_AfterStandardSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetPtAfterStdSelections,
						       "SubldgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}", 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetDijetPtAfterStdSelections,
						       "SubldgTrijetDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}", 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetDijetMassAfterStdSelections,
						       "SubldgTrijetDijetMass_AfterStandardSelections",";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetMassAfterStdSelections,
						       "SubldgTrijetMass_AfterStandardSelections",";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetTopMassWMassRatioAfterStdSelections,
						       "SubldgTrijetTopMassWMassRatioAfterStandardSelections", ";R_{32}", 100 , 0.0, 10.0);

      fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterStdSelections, 
						       "SubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterStandardSelections" ,";p_{T} (GeV/c);p_{T} (GeV/c)",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max(), 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetBJetPtAfterStdSelections,
						       "SubldgTrijetBjetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetBJetEtaAfterStdSelections,
						       "SubldgTrijetBjetEta_AfterStandardSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTetrajetPtAfterStdSelections,
						       "LdgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
						       
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTetrajetMassAfterStdSelections,
						       "LdgTetrajetMass_AfterStandardSelections", ";m_{jjbb} (GeV/c^{2});N_{events}",
						       fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTetrajetPtAfterStdSelections,
						       "SubldgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
						       
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTetrajetMassAfterStdSelections,
						       "SubldgTetrajetMass_AfterStandardSelections", ";m_{jjbb} (GeV/c^{2});N_{events}",
						       fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlTetrajetBJetPtAfterStdSelections,
						       "TetrajetBjetPt_AfterStandardSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlTetrajetBJetEtaAfterStdSelections,
						       "TetrajetBjetEta_AfterStandardSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

      // fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlTopFitChiSqrAfterAllSelections,
      // "TopFitChiSqr_AfterAllSelections", ";#chi^{2};N_{events}", 1000,  0.0, 1000.0);

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetPtAfterAllSelections,
						       "LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}", 						       
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetDijetPtAfterAllSelections,
						       "LdgTrijetDijetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}", 						       
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetDijetMassAfterAllSelections,
						       "LdgTrijetDijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetMassAfterAllSelections,
						       "LdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetTopMassWMassRatioAfterAllSelections,
						       "LdgTrijetTopMassWMassRatioAfterAllSelections", ";R_{32}", 100 , 0.0, 10.0);

      fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterAllSelections, 
						       "LdgTrijetPt_Vs_LdgTrijetDijetPtAfterAllSelections" ,";p_{T} (GeV/c);p_{T} (GeV/c)",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max(), 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetBJetPtAfterAllSelections,
						       "LdgTrijetBjetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTrijetBJetEtaAfterAllSelections,
						       "LdgTrijetBjetEta_AfterAllSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetPtAfterAllSelections,
						       "SubldgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}", 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetDijetPtAfterAllSelections,
						       "SubldgTrijetDijetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}", 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetDijetMassAfterAllSelections,
						       "SubldgTrijetDijetMass_AfterAllSelections",";m_{jj} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetMassAfterAllSelections,
						       "SubldgTrijetMass_AfterAllSelections",";m_{jjb} (GeV/c^{2});N_{events}",
						       fTopMassBinSettings.bins(), fTopMassBinSettings.min(), fTopMassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetTopMassWMassRatioAfterAllSelections,
						       "SubldgTrijetTopMassWMassRatioAfterAllSelections", ";R_{32}", 100 , 0.0, 10.0);

      fHistoSplitter.createShapeHistogramTriplet<TH2F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterAllSelections, 
						       "SubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterAllSelections" ,";p_{T} (GeV/c);p_{T} (GeV/c)",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max(), 
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetBJetPtAfterAllSelections,
						       "SubldgTrijetBjetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTrijetBJetEtaAfterAllSelections,
						       "SubldgTrijetBjetEta_AfterAllSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTetrajetPtAfterAllSelections,
						       "LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
						       
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlLdgTetrajetMassAfterAllSelections,
						       "LdgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});N_{events}",
						       fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTetrajetPtAfterAllSelections,
						       "SubldgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());
						       
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSubldgTetrajetMassAfterAllSelections,
						       "SubldgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});N_{events}",
						       fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlTetrajetBJetPtAfterAllSelections,
						       "TetrajetBjetPt_AfterAllSelections", ";p_{T} (GeV/c);N_{events}",
						       2*fPtBinSettings.bins(), fPtBinSettings.min(), 2*fPtBinSettings.max());

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlTetrajetBJetEtaAfterAllSelections,
						       "TetrajetBjetEta_AfterAllSelections", ";#eta;N_{events}",
						       fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
      
    }// if (hplus2tb)
  
  //==========================================
  // standard selections: MET
  //==========================================
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETAfterStdSelections, 
						   "MET_AfterStandardSelections", ";MET, GeV;N_{events}", 
						   fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max()); //FIXME: not filled anywhere (HToTau)

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETPhiAfterStdSelections, 
						   "METPhi_AfterStandardSelections", ";MET #phi;N_{events}", 
						   fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max()); //FIXME: not filled anywhere (HToTau)

  if (!hplus2tb)
    {
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlDeltaPhiTauMetAfterStdSelections, 
						       "DeltaPhiTauMet_AfterStandardSelections", ";#Delta#phi(#tau,MET), {}^{#circ};N_{events}", 
						       36, 0, 180); //FIXME: not filled anywhere
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlDeltaPhiMuMetAfterStdSelections, 
						       "DeltaPhiMuMet_AfterStandardSelections", ";#Delta#phi(#mu,MET), {}^{#circ};N_{events}", 
						       36, 0, 180); //FIXME: not filled anywhere
    }// if (!hplus2tb)
  
  //==========================================
  // MET selection
  //==========================================
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMET, 
						   "MET", ";MET, GeV;N_{events}", 
						   fHtBinSettings.bins(), fHtBinSettings.min(), fHtBinSettings.max());

  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlMETPhi, 
						   "METPhi", ";MET #phi;N_{events}", 
						   fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
  
  //==========================================
  // b tagging
  //==========================================
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
  
  //==========================================
  // back-to-back angular cuts
  //==========================================
  if (!hplus2tb)
    {      
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
    }// if (!hplus2tb)

  //==========================================
  // all selections: control plots
  //==========================================
  fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlNVerticesAfterAllSelections, 
						   "NVertices_AfterAllSelections", ";N_{vertices};N_{events}",
						   fNVerticesBinSettings.bins(), fNVerticesBinSettings.min(), fNVerticesBinSettings.max());

  if (!hplus2tb)
    {  
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
      
      for (int i = 0; i < fHelper.getTauSourceBinCount(); ++i) 
	{
	  fHistoSplitter.SetBinLabel(hCtrlSelectedTauSourceAfterAllSelections, i+1, fHelper.getTauSourceBinLabel(i));
	}
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlSelectedTauIPxyAfterAllSelections, 
						       "SelectedTau_IPxy_AfterAllSelections", ";IP_{T} (cm);N_{events}",
						       100, 0, 0.2);
    }// if (!hplus2tb)   
  
  
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
  
  //==========================================
  /// all selections: Experimental
  //==========================================
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

  //==========================================
  // all selections
  //========================================== 
  if (!hplus2tb)
    {
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlCollinearAngularCutsMinimumAfterAllSelections, 
						       "CollinearAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{#circ}-#Delta#phi(jet_{1..n},MET))^{2}}), ^{#circ};N_{events}", 
						       fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
    }// if (!hplus2tb)
      
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
  
  if (!hplus2tb)
    {

      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlBackToBackAngularCutsMinimumAfterAllSelections, 
						       "BackToBackAngularCutsMinimum_AfterAllSelections", ";min(#sqrt{(180^{#circ}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..n},MET)^{2}}), ^{#circ};N_{events}", 
						       fAngularCuts1DSettings.bins(), fAngularCuts1DSettings.min(), fAngularCuts1DSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(fEnableGenuineTauHistograms, HistoLevel::kSystematics, myDirs, hCtrlDeltaPhiTauMetAfterAllSelections, 
						       "DeltaPhiTauMet_AfterAllSelections", ";#Delta#phi(#tau,MET), {}^{#circ};N_{events}", 
						       36, 0, 180);
    }// if (!hplus2tb)
    
  //==========================================  
  // all selections: shape plots
  //==========================================
  if (!hplus2tb)
    {
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeTransverseMass, 
						       "shapeTransverseMass", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
						       fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
      
      fHistoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myDirs3, hShapeProbabilisticBtagTransverseMass, 
						       "shapeTransverseMassProbabilisticBTag", ";m_{T}(tau,MET), GeV/c^{2};N_{events}",
						       fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
    }
  

  if (isData) 
    {
      hNSelectedVsRunNumber = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, 
							 "NSelectedVsRunNumber", "NSelectedVsRunNumber;Run number;N_{events}", 14000, 246000, 260000);
    }
 
  for (auto& p: fBaseObjects) p->book(dir, isData);
  return;
}

void CommonPlots::initialize() {
  iVertices = -1;
  fTauData  = TauSelection::Data();
  //FakeTauIdentifier::Data fFakeTauData;
  bIsGenuineTau = false;
  bIsGenuineB   = false;
  fElectronData = ElectronSelection::Data();
  fMuonData = MuonSelection::Data();
  fJetData = JetSelection::Data();
  fCollinearAngularCutsData = AngularCutsBackToBack::Data();
  fBJetData = BJetSelection::Data();
  fMETData = METSelection::Data();
  fTopologyData = TopologySelection::Data();
  // fTopData = TopSelection::Data();
  fTopData = TopSelectionBDT::Data();
  fBackToBackAngularCutsData = AngularCutsCollinear::Data();
  // fFatJetData = FatJetSelection::Data();
  // fFatJetSoftDropData = FatJetSoftDropSelection::Data();
  fHistoSplitter.initialize();
  
  for (auto& p: fBaseObjects) p->reset();
  return;
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

void CommonPlots::fillControlPlotsAfterBjetSelection(const Event& event, const BJetSelection::Data& data) {
  fBJetData = data;
  for (auto& p: fBaseObjects) p->fillControlPlotsAfterBjetSelection(event, fBJetData);
  bIsGenuineTau = fBJetData.isGenuineB();
  return;
}

void CommonPlots::fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data) {
  for (auto& p: fBaseObjects) {
    p->fillControlPlotsAfterAntiIsolatedTauSelection(event, data);
  }
}

void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const Event& event) {
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNjetsAfterJetSelectionAndMETSF, bIsGenuineTau, fJetData.getNumberOfSelectedJets());
}

void CommonPlots::fillControlPlotsAfterStandardSelections(const Event& event, 
							  const JetSelection::Data& jetData,
							  const BJetSelection::Data& bjetData,
							  const METSelection::Data& METData,
							  const TopologySelection::Data& topologyData,
							  // const TopSelection::Data& topData, 
							  const TopSelectionBDT::Data& topData,
							  bool bIsGenuineB) {
  fJetData      = jetData;
  fBJetData     = bjetData;
  fTopologyData = topologyData;
  fTopData      = topData;
  fMETData      = METData;
  bIsGenuineB   = bjetData.isGenuineB();
  // if (bIsInverted) bIsGenuineB = topData.isGenuineB();
  // else bIsGenuineB = bjetData.isGenuineB();
  
  // Fill Histogram Triplets
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterStdSelections, bIsGenuineB, iVertices);
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterStdSelections    , bIsGenuineB, fJetData.getSelectedJets().size());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJetsAfterStdSelections   , bIsGenuineB, fBJetData.getSelectedBJets().size());

  // For-loop: All selected jets
  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterStdSelections         , bIsGenuineB, p.pt() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterStdSelections        , bIsGenuineB, p.eta() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterStdSelections     , bIsGenuineB, p.eta(), p.phi() );
      // fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterStdSelections, bIsGenuineB, p.bjetDiscriminator() );
    }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlHTAfterStdSelections , bIsGenuineB, fJetData.HT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMHTAfterStdSelections, bIsGenuineB, std::sqrt(fJetData.MHT().perp2()));
    
  // For-loop: All selected bjets
  for (auto& p: fBJetData.getSelectedBJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPtAfterStdSelections        , bIsGenuineB, p.pt() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEtaAfterStdSelections       , bIsGenuineB, p.eta() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterStdSelections, bIsGenuineB, p.bjetDiscriminator() );
    }

  // MET
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETAfterStdSelections   , bIsGenuineB, fMETData.getMET().R() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhiAfterStdSelections, bIsGenuineB, fMETData.getMET().Phi() );

  // TopSelection histograms
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetPtAfterStdSelections        , bIsGenuineB, fTopData.getLdgTrijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetDijetPtAfterStdSelections   , bIsGenuineB, fTopData.getLdgTrijetDijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetDijetMassAfterStdSelections , bIsGenuineB, fTopData.getLdgTrijetDijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetMassAfterStdSelections      , bIsGenuineB, fTopData.getLdgTrijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetTopMassWMassRatioAfterStdSelections, bIsGenuineB, fTopData.getLdgTrijetTopMassWMassRatio() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterStdSelections, bIsGenuineB, fTopData.getLdgTrijet().pt(), fTopData.getLdgTrijetDijet().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetBJetPtAfterStdSelections    , bIsGenuineB, fTopData.getLdgTrijetBJet().p4().pt() ); 
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetBJetEtaAfterStdSelections   , bIsGenuineB, fTopData.getLdgTrijetBJet().p4().eta() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetPtAfterStdSelections     , bIsGenuineB, fTopData.getSubldgTrijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetDijetPtAfterStdSelections, bIsGenuineB, fTopData.getSubldgTrijetDijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetDijetMassAfterStdSelections, bIsGenuineB, fTopData.getSubldgTrijetDijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetMassAfterStdSelections   , bIsGenuineB, fTopData.getSubldgTrijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetTopMassWMassRatioAfterStdSelections, bIsGenuineB, fTopData.getSubldgTrijetTopMassWMassRatio() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterStdSelections, bIsGenuineB, fTopData.getSubldgTrijet().pt(), fTopData.getSubldgTrijetDijet().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetBJetPtAfterStdSelections , bIsGenuineB, fTopData.getSubldgTrijetBJet().p4().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetBJetEtaAfterStdSelections, bIsGenuineB, fTopData.getSubldgTrijetBJet().p4().eta() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTetrajetPtAfterStdSelections      , bIsGenuineB, fTopData.getLdgTetrajet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTetrajetMassAfterStdSelections    , bIsGenuineB, fTopData.getLdgTetrajet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTetrajetPtAfterStdSelections   , bIsGenuineB, fTopData.getSubldgTetrajet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTetrajetMassAfterStdSelections , bIsGenuineB, fTopData.getSubldgTetrajet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlTetrajetBJetPtAfterStdSelections     , bIsGenuineB, fTopData.getTetrajetBJet().p4().pt() ); // caution! requires soft cut
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlTetrajetBJetEtaAfterStdSelections    , bIsGenuineB, fTopData.getTetrajetBJet().p4().eta() );
  return;
}

void CommonPlots::fillControlPlotsAfterAllSelections(const Event& event, int isGenuineB) {
  // NB: Call only afer fillControlPlotsAfterStandardSelections() has been called
  // Variables fJetData, fBJetData, fTopologyData, fTopData, fMETData, bIsGenuineB already set!
  
  // Store boolean  
  bIsGenuineB = isGenuineB;

  // NB: isInverted is a dumbie variable. Introduced to be able to overload the function
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, bIsGenuineTau, iVertices);

  // Fill Histogram Triplets
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNVerticesAfterAllSelections, bIsGenuineB, iVertices);
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNJetsAfterAllSelections    , bIsGenuineB, fJetData.getSelectedJets().size());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlNBJetsAfterAllSelections   , bIsGenuineB, fBJetData.getSelectedBJets().size());

  // For-loop: All selected jets
  for (auto& p: fJetData.getSelectedJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetPtAfterAllSelections         , bIsGenuineB, p.pt() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaAfterAllSelections        , bIsGenuineB, p.eta() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlJetEtaPhiAfterAllSelections     , bIsGenuineB, p.eta(), p.phi() );
      // fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterAllSelections, bIsGenuineB, p.bjetDiscriminator() );
    }
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlHTAfterAllSelections , bIsGenuineB, fJetData.HT());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMHTAfterAllSelections, bIsGenuineB, std::sqrt(fJetData.MHT().perp2()));
    
  // For-loop: All selected bjets
  for (auto& p: fBJetData.getSelectedBJets()) 
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetPtAfterAllSelections        , bIsGenuineB, p.pt() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBJetEtaAfterAllSelections       , bIsGenuineB, p.eta() );
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlBDiscriminatorAfterAllSelections, bIsGenuineB, p.bjetDiscriminator() );
    }

  // MET
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETAfterAllSelections   , bIsGenuineB, fMETData.getMET().R() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlMETPhiAfterAllSelections, bIsGenuineB, fMETData.getMET().Phi() );

  // TopSelection histograms
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetPtAfterAllSelections        , bIsGenuineB, fTopData.getLdgTrijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetDijetPtAfterAllSelections   , bIsGenuineB, fTopData.getLdgTrijetDijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetDijetMassAfterAllSelections , bIsGenuineB, fTopData.getLdgTrijetDijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetMassAfterAllSelections      , bIsGenuineB, fTopData.getLdgTrijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetBJetPtAfterAllSelections    , bIsGenuineB, fTopData.getLdgTrijetBJet().p4().pt() ); 
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetTopMassWMassRatioAfterAllSelections, bIsGenuineB, fTopData.getLdgTrijetTopMassWMassRatio() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetPt_Vs_LdgTrijetDijetPtAfterAllSelections, bIsGenuineB, fTopData.getLdgTrijet().pt(), fTopData.getLdgTrijetDijet().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTrijetBJetEtaAfterAllSelections   , bIsGenuineB, fTopData.getLdgTrijetBJet().p4().eta() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetPtAfterAllSelections     , bIsGenuineB, fTopData.getSubldgTrijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetDijetPtAfterAllSelections, bIsGenuineB, fTopData.getSubldgTrijetDijet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetDijetMassAfterAllSelections, bIsGenuineB, fTopData.getSubldgTrijetDijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetMassAfterAllSelections   , bIsGenuineB, fTopData.getSubldgTrijet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetTopMassWMassRatioAfterAllSelections, bIsGenuineB, fTopData.getSubldgTrijetTopMassWMassRatio() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetPt_Vs_SubldgTrijetDijetPtAfterAllSelections, bIsGenuineB, fTopData.getSubldgTrijet().pt(), fTopData.getSubldgTrijetDijet().pt());
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetBJetPtAfterAllSelections , bIsGenuineB, fTopData.getSubldgTrijetBJet().p4().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTrijetBJetEtaAfterAllSelections, bIsGenuineB, fTopData.getSubldgTrijetBJet().p4().eta() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTetrajetPtAfterAllSelections      , bIsGenuineB, fTopData.getLdgTetrajet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlLdgTetrajetMassAfterAllSelections    , bIsGenuineB, fTopData.getLdgTetrajet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTetrajetPtAfterAllSelections   , bIsGenuineB, fTopData.getSubldgTetrajet().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlSubldgTetrajetMassAfterAllSelections , bIsGenuineB, fTopData.getSubldgTetrajet().mass() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlTetrajetBJetPtAfterAllSelections     , bIsGenuineB, fTopData.getTetrajetBJet().p4().pt() );
  fHistoSplitter.fillShapeHistogramTriplet(hCtrlTetrajetBJetEtaAfterAllSelections    , bIsGenuineB, fTopData.getTetrajetBJet().p4().eta() );
  return;
}


void CommonPlots::fillControlPlotsAfterTopologicalSelections(const Event& event, bool withoutTau, bool withMu) {
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
  
  if (withMu) // muons for embedding studies
    {
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedMuonPtAfterStdSelections, bIsGenuineTau, fMuonData.getHighestSelectedMuonPt());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedMuonEtaAfterStdSelections, bIsGenuineTau, fMuonData.getHighestSelectedMuonEta());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedMuonPhiAfterStdSelections, bIsGenuineTau, fMuonData.getHighestSelectedMuonPhi());
      fHistoSplitter.fillShapeHistogramTriplet(hCtrlSelectedMuonEtaPhiAfterStdSelections, bIsGenuineTau, fMuonData.getHighestSelectedMuonEta(), fMuonData.getHighestSelectedMuonPhi());
    }

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
