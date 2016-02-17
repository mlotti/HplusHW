// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"
#include "DataFormat/interface/GenParticleGenerated.h"
#include "TDirectory.h"
#include "Math/GenVector/VectorUtil.h"

class CorrelationAnalysis: public BaseSelector {
public:
  explicit CorrelationAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~CorrelationAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters

  /// Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  Count cFakeTauSFCounter;
  Count cTauTriggerSFCounter;
  Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  AngularCutsCollinear fAngularCutsCollinear;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  AngularCutsBackToBack fAngularCutsBackToBack;
  GenParticleGeneratedCollection fGenParticleGeneratedCollection;
  Count cSelected;
    
  // Non-common histograms
 WrappedTH1 *hMet;
  WrappedTH1 *hTauPt;
  WrappedTH1 *hTauEta;
  WrappedTH1 *hPt3Jets;
  WrappedTH1 *hPt2Jets; 
  WrappedTH1 *h3jetPtcut; 
  WrappedTH2 *hDPhiTauMetVsPt3jets;
  WrappedTH2 *hDPhiTauMetVsDrTau3Jets;
  WrappedTH1 *hM3jets;
  WrappedTH1 *hM2jets;
  WrappedTH2 *hPtVsM3jets;
  WrappedTH1 *hDeltaPhiTauMet;
  WrappedTH1 *htransverseMass;
  WrappedTH1 *htransverseMassGenuineTau;
  WrappedTH1 *htransverseMass3Jet150;
  WrappedTH1 *htransverseMass1Tau;
  WrappedTH1 *htransverseMassTriangleCut; 
  WrappedTH1 *htransverseMass3JetCut;
  WrappedTH1 *htransverseMassDeltaR3JetsTauCut;
  WrappedTH1 *htransverseMassWith3JetAndJetSumCut;
  WrappedTH1 *htransverseMassDeltaRCorrCut;
  WrappedTH1 *htransverseMassTopMtCut;
  WrappedTH1 *htransverhtransverseMassWith3JetBjetVsJetSumCut;
  WrappedTH1 *htransverseMassWith3JeTopPtVSDrCut;
  WrappedTH1 *htransverseMassDeltaPhiVsMaxPtCut;
  WrappedTH1 *htransverseMass3jetsMtCut;
  WrappedTH1 *htransverseMassMtTopMetCut;
  WrappedTH1 *htransverseMassTopAndWMassCut;
  WrappedTH1 *htransverseMassTopMassCut;
  WrappedTH1 *htransverseMassWCandFound;
  WrappedTH1 *htransverseMassTopMass3jetsMtCut;
  WrappedTH1 *htransverseMassTopAndWPtCut;
  WrappedTH1 *htransverseMassDeltaPhi3jetPtCutDiff;
  WrappedTH1 *hWCandMass;
  WrappedTH1 *hdeltaPhiVSmaxPtCut;
  WrappedTH1 *hmt_top_met;
  WrappedTH1 *hmt_3jets_met;
  WrappedTH1 *hgenJetPt;
  WrappedTH1 *hgenJetEta;
  WrappedTH1 *hgenJetPhi;
  WrappedTH1 *hSelectedJets;
  WrappedTH1 *hSelectedNonBJets;
  WrappedTH1 *hSelectedBJets;
  WrappedTH2 *hgenjetEtaVsDeltaPt; 
  WrappedTH2 *hgenjetPhiVsDeltaPt; 
  WrappedTH2 *hgenjetPtVsDeltaPt; 
  WrappedTH2 *hM3jetsVSM2jets; 
  WrappedTH1 *hM3jetsVSM2jetsCut;
  WrappedTH1 *hDeltaRJetGenJet; 
  WrappedTH1 *hDeltaPt;
  WrappedTH2 *hJetEtSumVsJetTauMetEtSum;
  WrappedTH2 *hDPhiTauMetVsTransverseMass;
  WrappedTH1 *hJetTauMetEtSum;
  WrappedTH1 *hDrTau3Jets;
  WrappedTH1 *hJetTauEtSum;
  WrappedTH1 *hJetEtSum;
  WrappedTH1 *hDPhi3JetsMet;
  WrappedTH1 *hDphiMinus3jetcut;
  WrappedTH1 *hJetEtSumVsJetTauMetEtSum3JetCut;
  WrappedTH1 *hconstantEtSum; 
  WrappedTH1 *hslopeEtSum; 
  WrappedTH1 *htopPt;
  WrappedTH1 *htopMass;
  WrappedTH1 *htopMassIdAllJets; 
  WrappedTH1 *htopMassIdBjet; 
  WrappedTH1 *htopEta;
  WrappedTH1 *hWPt;
  WrappedTH1 *hWMass;
  WrappedTH1 *hWEta;
  WrappedTH1 *hTopPtVSDrCut;
  WrappedTH2 *hDPhiTauMetVsPtMaxJet;
  WrappedTH1 *hPtMaxJet;
  WrappedTH1 *hdeltaR_W_tau;
  WrappedTH1 *hdeltaR_Wb;
  WrappedTH1 *hdeltaR_top_tau;
  WrappedTH1 *hdeltaR_jets;
  WrappedTH2 *hdeltaR_Wb_VS_topPt;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(CorrelationAnalysis);

CorrelationAnalysis::CorrelationAnalysis(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
  cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
  cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
  fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
  fJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
  fMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }

void CorrelationAnalysis::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fAngularCutsBackToBack.bookHistograms(dir);
  // Book non-common histograms
  //hExample =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);
  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 200, 0, 1000);
  hMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0, 1000);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hPt3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pt3Jets", "Pt3Jets", 200, 0., 1000.);
  hPt2Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pt2Jets", "Pt2Jets", 200, 0., 1000.);
  h3jetPtcut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TheeJetPtcut", "TheeJetPtcut", 200, 0., 400.);
  hDphiMinus3jetcut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DphiMinus3jetcut", "TDphiMinus3jetcut", 500, -500., 500.);
  hM3jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M3Jets", "M3Jets", 200, 0., 1000.);
  hM2jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M2Jets", "M3Jets", 200, 0., 600.);
  hPtVsM3jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "PtVsM3jets", "PtVsM3jets", 100, 0., 1000, 100, 0., 1000.);
  hDeltaPhiTauMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiTauMet", "DeltaPhiTauMet", 90, 0., 180);
  hDPhiTauMetVsPt3jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsPt3jets", "Pt3jets;#Delta#phi(#tau jet,MET) (^{o});p_{T}^{3 jets}(GeV)", 180, 0., 180, 100, 0., 500.);
  hDrTau3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DrTau3Jets", "DrTau3Jets", 100, 0.,5);
  hJetEtSum =fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetEtSum", "JetEtSum", 200, 0, 2000);
  hJetTauEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetTauEtSum", "JetTauEtSum", 200, 0, 2000);
  hJetTauMetEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetTauMetEtSum", "JetTauMetEtSum", 200, 0, 2000);
  hDPhi3JetsMet= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DPhi3JetsMet", "DPhi3JetsMet", 90, 0., 180);
  hDPhiTauMetVsTransverseMass=fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsTransverseMass", "DPhiTauMetVsTransverseMass", 90, 0., 180, 100, 0., 1000.);
  hJetEtSumVsJetTauMetEtSum = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "JetEtSumVsJetTauMetEtSum", "JetEtSumVsJetTauMetEtSum", 100, 0., 1000, 100, 0., 1000.);
  hJetEtSumVsJetTauMetEtSum3JetCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetEtSumVsJetTauMetEtSum3JetCut", "JetEtSumVsJetTauMetEtSum3JetCut", 100, 0., 1000.);
  hDPhiTauMetVsDrTau3Jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDrTau3Jets", "DPhiTauMetVsDrTau3Jets", 180, 0., 180, 100, 0., 5.);
  hDPhiTauMetVsPtMaxJet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsPtMaxJet", "DPhiTauMetVsPtMaxJet", 180, 0., 180, 100, 0., 500.);
  hPtMaxJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "PtMaxJet", "PtMaxJet", 100, 0., 500.);
  hM3jetsVSM2jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "M3jetsVSM2jets", "M3jetsVSM2jets", 100, 0., 1000, 100, 0., 600.);
  hM3jetsVSM2jetsCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M3jetsVSM2jetsCut", "M3jetsVSM2jetsCut", 100, -500., 500);
  htransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass", "transverseMass", 200, 0., 800);
  htransverseMassGenuineTau = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassGenuineTau", "transverseMasGenuineTaus", 200, 0., 800);
  htransverseMass3Jet150 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass3Jet150", "transverseMass3Jet150", 200, 0., 800);  
  htransverseMass1Tau = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass1Tau", "transverseMass1Tau", 200, 0., 800);

  htransverseMassTriangleCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTriangleCut", "transverseMassTriangleCut", 200, 0., 800);  
  htransverseMass3JetCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass3JetCut", "transverseMass3JetCut", 200, 0., 800); 
  htransverseMassDeltaR3JetsTauCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassDeltaR3JetsTauCut", "transverseMassDeltaR3JetsTauCut", 200, 0., 800);
  htransverseMassDeltaRCorrCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassDeltaRCorrCut", "transverseMassDeltaRCorrCut", 200, 0., 800);
  htransverseMassWith3JetAndJetSumCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassWith3JetAndJetSumCut", "transverseMassWith3JetAndJetSumCut",200, 0., 800);
  htransverseMassWith3JeTopPtVSDrCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassWith3TopPtVSDrCut", "transverseMassWithTopPtVSDrCut",200, 0., 800);
  htransverseMassDeltaPhiVsMaxPtCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassDeltaPhiVsMaxPtCut", "transverseMassDeltaPhiVsMaxPtCut",200, 0., 800);
  htransverseMassMtTopMetCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassMtTopMetCut", "transverseMassMtTopMetCut",200, 0., 800);
  htransverseMass3jetsMtCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass3jetsMtCut", "transverseMass3jetsMtCut",200, 0., 800);
  hdeltaPhiVSmaxPtCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaPhiVSmaxPtCut", "deltaPhiVSmaxPtCut",100, -500., 500);
  htransverseMassTopMassCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTopMassCut", "transverseMassTopMassCut",200, 0., 800);
  htransverseMassTopMass3jetsMtCut= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTopMass3jetsMtCut", "transverseMassTopMass3jetsMtCut",200, 0., 800);
   htransverseMassTopAndWMassCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTopAndWMassCut", "transverseMassTopAndWMassCut",200, 0., 800);
   htransverseMassTopAndWPtCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTopAndWPtCut", "transverseMassTopAndWPtCut",200, 0., 800);
   htransverseMassWCandFound = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassWCandFound", "transverseMassWCandFound",200, 0., 800);
  htransverseMassTopMtCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTopMtCut", "transverseMassTopMtCut",200, 0., 800);
  htransverseMassDeltaPhi3jetPtCutDiff= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassDeltaPhi3jetPtCutDiff", "transverseMassDeltaPhi3jetPtCutDiff",200, 0., 800);
  hmt_top_met= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "mt_top_met", "mt_top_met",200, 0., 800);
  hmt_3jets_met= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "mt_3jets_met", "mt_3jets_met",200, 0., 800);
  htransverhtransverseMassWith3JetBjetVsJetSumCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "htransverseMassWith3JetBjetVsJetSumCut", "transverseMassWith3JetAndJetSumCut",200, 0., 800);
  hconstantEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "constantEtSum", "constantEtSum", 100, 0., 400);
  hslopeEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "slopeEtSum", "slopeEtSum", 100, 0., 2);
  hSelectedNonBJets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedNonBJets", "SelectedAllJets", 20, 0., 20);
  hSelectedBJets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedBJets", "SelectedBJets", 20, 0., 20);
  hSelectedJets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedJets", "SelectedJets", 20, 0., 20);
  //  hNtrueBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NtrueBjets", "NtrueBjets", 20, 0, 20);
  hgenJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPt", "genJet pT", 200, 0, 1000);
  hgenJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetEta", "genJet eta", 100, -5, 5);
  hgenJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPhi", "genJet phi", 90, 0, 180);
  //  hrealBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realBJetPt", "trueBJet pT", 200, 0, 1000);
  //  hrealBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realBJetEta", "trueBJet eta", 100, -2.5, 2.5);
  //  hrealMaxBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realMaxBJetPt", "trueMaxBJet pT", 200, 0, 1000);
  //  hrealMaxBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realMaxBJetEta", "trueMaxBJet eta", 100, -5, 5);  
  hgenjetEtaVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetEtaVsDeltaPt", "genjetEtaVsDeltaPt", 250, -2.5, 2.5,100,-1.5,1.5);
  hgenjetPhiVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPhiVsDeltaPt", "genjetPhiVsDeltaPt", 90, 0., 180,100,-1.5,1.5);
  hWCandMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "WCandMass", "WCandMass", 100, 0, 500);
  hgenjetPtVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPtVsDeltaPt", "genjetPtVsDeltaPt", 200, 0., 1000,100,-1.5,1.5);
  hDeltaRJetGenJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaRJetGenJet", "deltaRJetGenJet", 100, 0.,5);  
  hDeltaPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPt", "DeltaPt", 100, -1.5, 1.5);
  htopPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "topPt", "top pT", 100, 0, 1000);
  htopMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "topMass", "top mass", 100, 0, 500);
  htopMassIdAllJets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "topMassIdAllJets", "top mass IdAllJets", 100, 0, 500);
  htopMassIdBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "topMassIdBjet", "top mass IdBJet", 100, 0, 500);
  htopEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "topEta", "top Eta", 100, -5, 5);
  hWPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "WPt", "W pT", 100, 0, 1000);
  hWMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "WMass", "W mass", 100, 0, 500);
  hWEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "WEta", "W Eta", 100, -5, 5);
  hdeltaR_W_tau = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaR_W_tau", "deltaR_W_tau", 100, 0, 5);
  hdeltaR_Wb = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaR_Wb", "deltaR_Wb", 100, 0, 5);
  hdeltaR_top_tau = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaR_top_tau", "deltaR_top_tau", 100, 0, 5);
  hdeltaR_jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaR_jets", "deltaR_jets", 100, 0, 5);
  hdeltaR_Wb_VS_topPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "deltaR_Wb_VS_topPt", "deltaR_Wb_VS_topP", 100, 0, 5,100,0,1000);
  hTopPtVSDrCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TopPtVSDrCut", "TopPtVSDrCut", 100, -500, 500);
}

void CorrelationAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void CorrelationAnalysis::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

//====== MET filters to remove events with spurious sources of fake MET
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection())
    return;
  
//====== GenParticle analysis
  // if needed
  
//====== Check that primary vertex exists
  if (nVertices < 1)
    return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
//====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;
  
//====== Fake tau SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    cFakeTauSFCounter.increment();
  }

//====== Tau trigger SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
    cTauTriggerSFCounter.increment();
  }

//====== MET trigger SF
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cMetTriggerSFCounter.increment();
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  //std::cout << tauData.getSelectedTau().pt() << ":" << tauData.getTauMisIDSF() << ", " << tauData.getTauTriggerSF() << ", met=" << silentMETData.getMET().R() << ", SF=" << silentMETData.getMETTriggerSF() << std::endl;
  
//====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

//====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons())
    return;

//====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection())
    return;

//====== Collinear angular cuts
  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(fEvent, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return;

//====== b tag SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
  }
  cBTaggingSFCounter.increment();

//====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.analyze(fEvent, tauData.getSelectedTau(), jetData, METData);
  if (!backToBackData.passedSelection())
    return;

//====== All cuts passed
  cSelected.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);



//====== Experimental selection code
  // if necessary

  // std::vector<GenParticleGeneratedCollection> topdecay;
  // fGenTop.getGenTopDecayMode();

  for (size_t i = 0; i <  fGenParticleGeneratedCollection.getGenTopDecayMode().size(); ++i) {
    // topdecay.push_back(fGenTop.getGenTopDecayMode()[i]); 
    //     std::cout << "  topdecay " << fGenParticleGeneratedCollection.getGenTopDecayMode()[i]  << std::endl;
   }

  /*
  size_t i = 0;
  for(Jet jet: event.jets()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
    if (myDeltaR < myMinDeltaR) {
      myMinDeltaR = myDeltaR;
      mySelectedIndex = i;
    }
    i += 1;
  }
  */









  // Correlation cuts
  std::vector<Jet> selectedJets;
  std::vector<Jet> selectedBJets;
  std::vector<Jet> selectedNonBJets;
  std::vector<Jet> selectedRealBJets;
  std::vector<Jet> selectedLightJets;

  Jet maxPTjet;
  double maxPT=0;

  //  size_t maxIndex = jetData.getSelectedJets().size();
  for (size_t i = 0; i < jetData.getSelectedJets().size(); ++i) {
    int flavor = std::abs(jetData.getSelectedJets()[i].pdgId());
    if (flavor == 5) { // b jet                                                                                                              
      selectedRealBJets.push_back(jetData.getSelectedJets()[i]); 
    } else {
      selectedLightJets.push_back(jetData.getSelectedJets()[i]);
    }                           
    
      
    for (size_t j = 0; j <  bjetData.getSelectedBJets().size(); ++j) {
      double drJetBjet = ROOT::Math::VectorUtil::DeltaR(jetData.getSelectedJets()[i].p4(),bjetData.getSelectedBJets()[j].p4());
           if (drJetBjet > 0.5 ) selectedNonBJets.push_back(jetData.getSelectedJets()[i]);
           if (drJetBjet < 0.5 ) selectedBJets.push_back(bjetData.getSelectedBJets()[j]);
    } 
    if (jetData.getSelectedJets()[i].pt() > maxPT ) {
      maxPT = jetData.getSelectedJets()[i].pt();
      maxPTjet = jetData.getSelectedJets()[i];
    }
//    double dphi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(jetData.getSelectedJets()[i].p4(), metData.getMET())*57.29578);
//  for(Jet jet: fEvent.jets()) {
    //    hJetPt->Fill(jet.pt());
    //    if(jet.pt() > 30) hJetEta->Fill(jet.eta());
    //   hJetPhi->Fill(jet.phi()* 180/3.14159265);
    //    double jetID = jet.pdgId();
    //    if(jet.pt() > 30 && std::abs(jet.eta()) < 2.4) {
      selectedJets.push_back(jetData.getSelectedJets()[i]);
  }

  //  for (size_t i = 0; i <  bjetData.getSelectedBJets().size(); ++i) {
  //  selectedBJets.push_back(bjetData.getSelectedBJets()[i]);
  // } 

  hSelectedJets->Fill(jetData.getSelectedJets().size()); 
  hSelectedBJets->Fill(bjetData.getSelectedBJets().size()); 
  hSelectedNonBJets->Fill(selectedNonBJets.size()); 

  if(selectedNonBJets.size() < 2)
    return;

  if(selectedBJets.size() < 1)
    return;

  //  Jet jet1 = selectedNonBJets[0];
  //  Jet jet2 = selectedNonBJets[1];
  //  Jet jet3 = selectedBJets[0];

  Jet jet1 = selectedJets[0];
  Jet jet2 = selectedJets[1];
  Jet jet3 = selectedJets[2];

  double jet1ID = jet1.pdgId();
  double jet2ID = jet2.pdgId();
  double jet3ID = jet3.pdgId();
  //    std::cout << "  jet1ID "<<   fGenTop.getGenTopDecayMode() << "  jet2ID "<<   jet2ID <<  "  jet3ID "<<   jet3ID << std::endl;
  math::XYZTLorentzVector threeJets;
  threeJets = jet1.p4() + jet2.p4() + jet3.p4();

  math::XYZTLorentzVector twoJets;
  twoJets = jet1.p4() + jet2.p4();

  hPt3Jets->Fill(threeJets.pt());
  hPt2Jets->Fill(twoJets.pt());
  hM3jets->Fill(threeJets.M());
  hM2jets->Fill(twoJets.M());
  hPtVsM3jets->Fill(threeJets.pt(),threeJets.M());
  hM3jetsVSM2jets->Fill(threeJets.M(),twoJets.M());
  double M3jetsVSM2jetsCut = twoJets.M() - 0.6 * threeJets.M();
  if (threeJets.M() > 300) hM3jetsVSM2jetsCut->Fill(M3jetsVSM2jetsCut);
  //  std::cout << "   threeJets.M()"<<   threeJets.M()   << std::endl;


  Tau tau = tauData.getSelectedTau();
  
  hTauPt->Fill(tau.pt());
  hTauEta->Fill(tau.eta());

  double DeltaPhiTauMET = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(tau.p4(), METData.getMET())*57.29578);
  double DeltaPhi3jetsMET = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(threeJets, METData.getMET())*57.29578);
  double transverseMass = TransverseMass::reconstruct(tau,METData.getMET() );

  hDeltaPhiTauMet->Fill(std::abs(DeltaPhiTauMET));
  hDPhi3JetsMet->Fill(std::abs(DeltaPhi3jetsMET));
  hDPhiTauMetVsPt3jets->Fill(std::abs(DeltaPhiTauMET),threeJets.pt());
  hDPhiTauMetVsPtMaxJet->Fill(std::abs(DeltaPhiTauMET),maxPTjet.pt());
  hPtMaxJet->Fill(maxPTjet.pt());
  hDPhiTauMetVsTransverseMass->Fill(std::abs(DeltaPhiTauMET),transverseMass);


  double ptcut = 400.0 * (1.0 - DeltaPhiTauMET/180.0);
  double ptConstant =  threeJets.pt() /(1.0 - DeltaPhiTauMET/180.0);
  h3jetPtcut->Fill(ptConstant);
  hDphiMinus3jetcut->Fill(DeltaPhiTauMET -threeJets.pt() );  

  double drTau3Jets = ROOT::Math::VectorUtil::DeltaR(tauData.getSelectedTau().p4(),threeJets);
  hDrTau3Jets->Fill(drTau3Jets); 
  hDPhiTauMetVsDrTau3Jets->Fill(std::abs(DeltaPhiTauMET),drTau3Jets);
  htransverseMass->Fill(transverseMass);
  if (tauData.isGenuineTau())   htransverseMassGenuineTau->Fill(transverseMass);
  // const size_t getFakeTauID() const { return getSelectedTau().pdgId(); }
  if (tauData.getSelectedTaus().size() == 1)  htransverseMass1Tau->Fill(transverseMass);
 // mt with 3jet and  triangle cut
  if (threeJets.pt()  > ptcut )    htransverseMass3JetCut->Fill(transverseMass);
  if (threeJets.pt()  > 150 )    htransverseMass3Jet150->Fill(transverseMass);

  if (!(threeJets.pt()  < ptcut && DeltaPhiTauMET  > 60)) { 
    htransverseMassTriangleCut->Fill(transverseMass);
  }
  if ((DeltaPhiTauMET -threeJets.pt()) > -100)    htransverseMassDeltaPhi3jetPtCutDiff->Fill(transverseMass);
  double deltaPhiVSmaxPtCut = maxPTjet.pt() + 200*DeltaPhiTauMET/180 - 400.;
  hdeltaPhiVSmaxPtCut-> Fill(deltaPhiVSmaxPtCut);

  if (deltaPhiVSmaxPtCut > 0 ) { 
    htransverseMassDeltaPhiVsMaxPtCut->Fill(transverseMass);
  }

  if ( drTau3Jets < 3 ) {
    htransverseMassDeltaR3JetsTauCut->Fill(transverseMass);
    if (DeltaPhiTauMET  > 90) {
      htransverseMassDeltaRCorrCut->Fill(transverseMass);
    }
  }
  double myMet=std::sqrt(METData.getMET().X()*METData.getMET().X()+METData.getMET().Y()*METData.getMET().Y());
  double JetEtSum = jet1.pt() + jet2.pt() + jet3.pt();
  double JetTauEtSum = JetEtSum + tau.pt();
  double JetTauMetEtSum = JetEtSum + tau.pt() + myMet;
  hMet->Fill(myMet);
  hJetEtSum->Fill(JetEtSum);
  hJetTauEtSum->Fill(JetTauEtSum);
  hJetTauMetEtSum->Fill(JetTauMetEtSum);
  hJetEtSumVsJetTauMetEtSum3JetCut->Fill(JetEtSum,JetTauMetEtSum);
  double JetTauMetEtSumCut = 1.4 * JetEtSum + 100.;
  //  double bJetEtSum = jetMetCorrelationsData.getbJetEtSum();
  //  hbJetEtSumVsJetTauMetEtSum3JetCut->Fill(bJetEtSum,JetTauMetEtSum);
  //  hbJetEtSumVsJetEtSum3JetCut->Fill(bJetEtSum,JetEtSum);
  //  double bJetEtSumCut = 1.35 * bJetEtSum + 60.;
  //  double bJetEtSumCut2 = 75.0 * bJetEtSum/35.0 + 250.;
  if ( JetTauMetEtSum > JetTauMetEtSumCut )  {
    htransverseMassWith3JetAndJetSumCut->Fill(transverseMass);
    // increment(fThreeJetAndJetEtSumCutCounter);
    //    if ( JetEtSum > bJetEtSumCut )  {
      //      htransverseMassWith3JetBjetVsJetSumCut->Fill(transverseMass);
      // increment(fThreeJetbJetVsJetEtSumCutCounter);
    // }
  }
 // assume known slope                                                                                                                
  double constantEtSum = JetTauMetEtSum - 1.4 *  JetEtSum;
  // assume known constant term                                                                                                        
  double slopeEtSum = (JetTauMetEtSum - 100)/JetEtSum;
  hconstantEtSum->Fill(constantEtSum);
  hslopeEtSum->Fill(slopeEtSum);


   // Reset variables                                                                                                                 
    double chi2Min = 999999;
    double nominalTop = 172.5; //value used in simulation (used to be 172.9)                                                                   
    double nominalW = 80.4; //value used in simulation (unchanged)                                                                              
    double sigmaTop = 26.9; //RMS of Gaussian fit to 2012 TTJets_SemiLept (used to be 18.0)                                                 
    double sigmaW = 14.4; //RMS of Gaussian fit to 2012 TTJets_SemiLept (used to be 11.0)                                         
    bool topmassfound = false;
    double topMass = -999;
    double WMass = -999;
    double dR_jets;
    double dR_top_tau;
    double dR_Wb;
    double dR_W_tau;
    Jet Jet1;
    Jet Jet2;
    Jet Jetb;
 //for all combos of 3 jets...                                                                                                               
    math::XYZTLorentzVector candW;
    math::XYZTLorentzVector candTop;
    math::XYZTLorentzVector recoW;
    math::XYZTLorentzVector recoTop;
    bool WCandFound = false;

  //  size_t maxIndex = jetData.getSelectedJets().size();
  for (size_t i = 0; i < selectedJets.size(); ++i) {
    Jet jet1 = selectedJets[i];
    for (size_t i2 = 0; i2 < selectedJets.size(); ++i2) {
      Jet jet2 = selectedJets[i2];
      if (ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4()) < 0.4) continue;
      candW = jet1.p4() + jet2.p4();
      WMass = candW.M();
      hWCandMass->Fill(recoW.M()); 
      if (candW.M() < 120 && candW.M() > 50)  WCandFound = true;

      for (size_t i3 = 0; i3 < selectedBJets.size(); ++i3) {
	Jet jet3 = selectedBJets[i3];
        candTop = jet1.p4() + jet2.p4() + jet3.p4();
	//	hjjbMass->Fill(candTop.M());
        double chi2 = ((candTop.M() - nominalTop)/sigmaTop)*((candTop.M() - nominalTop)/sigmaTop) + ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW);

     
	if (chi2 < chi2Min ) {
          chi2Min = chi2;
          Jet1 = jet1;
          Jet2 = jet2;
          Jetb = jet3;
          topMass = candTop.M();
          topmassfound = true;
	  recoTop = candTop;
	  recoW = candW;
	  dR_jets = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
	  dR_top_tau = ROOT::Math::VectorUtil::DeltaR(candTop, tau.p4());
	  dR_Wb = ROOT::Math::VectorUtil::DeltaR(candW, jet3.p4());
	  dR_W_tau = ROOT::Math::VectorUtil::DeltaR(candW, tau.p4());

	}
	
      }        
    }
  } 

  htopPt->Fill(recoTop.Pt());
  htopMass->Fill(recoTop.M());
  htopEta->Fill(recoTop.Eta());
  hWPt->Fill(recoW.Pt());
  hWMass->Fill(recoW.M());
  hWEta->Fill(recoW.Eta());
  double IDjet1 = std::abs(Jet1.pdgId());
  double IDjet2 = std::abs(Jet2.pdgId());
  double IDjetb = std::abs(Jetb.pdgId());


  if ( IDjet1 < 5 && IDjet2 < 5 && IDjetb == 5 ) {
    htopMassIdBjet->Fill(recoTop.M());
  }
  if (((IDjet1 == 1 && IDjet2 == 2) || (IDjet1 == 2 && IDjet2 ==1)) && IDjetb == 5 ) {
    htopMassIdAllJets->Fill(recoTop.M());
  }
  //angular hisrograms                                                                                                                                                
  hdeltaR_W_tau->Fill(dR_W_tau);
  hdeltaR_Wb->Fill(dR_Wb);
  
  hdeltaR_top_tau->Fill(dR_top_tau);
  hdeltaR_jets->Fill(dR_jets);
  hdeltaR_Wb_VS_topPt->Fill(dR_Wb,recoTop.Pt());
  double TopPtVSDrCut = 500*(1 - dR_Wb/4);
  hTopPtVSDrCut->Fill(recoTop.Pt()-TopPtVSDrCut);
  if (recoTop.Pt() > TopPtVSDrCut ) htransverseMassWith3JeTopPtVSDrCut->Fill(transverseMass);
  if (recoTop.Pt() < 400 && recoW.Pt() < 250 ) htransverseMassTopAndWPtCut->Fill(transverseMass);
  

   double myCosPhi = 100;
  if (myMet > 0.0 && recoTop.Pt()  > 0.0)
    myCosPhi = (recoTop.X()*METData.getMET().X() + recoTop.Y()*METData.getMET().Y()) / (recoTop.Pt() *myMet);
  double mt_top_met  = -999;
  double myTransverseMassSquared = 0;
  if (myCosPhi < 10)
    myTransverseMassSquared = 2 *recoTop.Pt()   * myMet * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    mt_top_met  = std::sqrt(myTransverseMassSquared);

  myCosPhi = 100;
  if (myMet > 0.0 && threeJets.Pt()  > 0.0)
    myCosPhi = (threeJets.X()*METData.getMET().X() + threeJets.Y()*METData.getMET().Y()) / (threeJets.Pt() *myMet);
  double mt_3jets_met  = -999;
  myTransverseMassSquared = 0;
  if (myCosPhi < 10)
    myTransverseMassSquared = 2 *threeJets.Pt()   * myMet * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    mt_3jets_met  = std::sqrt(myTransverseMassSquared);

  hmt_3jets_met->Fill(mt_3jets_met);
  hmt_top_met->Fill(mt_top_met);
  if ( WCandFound) htransverseMassWCandFound->Fill(transverseMass);
  if ( mt_top_met > 100) htransverseMassTopMtCut->Fill(transverseMass);
  if ( mt_3jets_met > 150) htransverseMass3jetsMtCut->Fill(transverseMass);
  if ( recoTop.M() < 220 && recoTop.M() > 120) {
    htransverseMassTopMassCut->Fill(transverseMass);
    if ( mt_3jets_met > 150) htransverseMassTopMass3jetsMtCut->Fill(transverseMass);
    if ( recoW.M() < 120 && recoW.M() > 50) {
      htransverseMassTopAndWMassCut->Fill(transverseMass);
    }
  }

 
//====== Finalize
  fEventSaver.save();
}
