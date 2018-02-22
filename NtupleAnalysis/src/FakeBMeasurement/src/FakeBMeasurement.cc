// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/BJetSelection.h"

#include "TDirectory.h"
#include "Math/VectorUtil.h"

class FakeBMeasurement: public BaseSelector {
public:
  explicit FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters);
  virtual ~FakeBMeasurement();

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
  virtual bool isBJet(const Jet& jet, const std::vector<Jet>& bjets);
  virtual bool areSameJets(const Jet& jet1, const Jet& jet2);

private:
  // Input parameters (Baseline Bjets)
  const DirectionalCut<int> cfg_BaselineNumberOfBJets;
  const std::string cfg_BaselineBJetsDiscr;
  const std::string cfg_BaselineBJetsDiscrWP;
  const DirectionalCut<double> cfg_LdgTopMVACut;
  const DirectionalCut<double> cfg_SubldgTopMVACut;
  const DirectionalCut<double> cfg_MinTopMVACut;
  const std::string cfg_BjetDiscr;

  // Common plots
  CommonPlots fCommonPlots;
  // CommonPlots fNormalizationSystematicsSignalRegion;  // fixme
  // CommonPlots fNormalizationSystematicsControlRegion; // fixme

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  // Baseline selection      
  Count cBaselineBTaggingCounter;
  Count cBaselineBTaggingSFCounter;
  BJetSelection fBaselineBJetSelection;
  METSelection fBaselineMETSelection;
  TopSelectionBDT fBaselineTopSelection;
  Count cBaselineSelected;
  Count cBaselineSelectedCR;
  // Inverted selection
  Count cInvertedBTaggingCounter;
  Count cInvertedBTaggingSFCounter;
  BJetSelection fInvertedBJetSelection;
  METSelection fInvertedMETSelection;
  TopSelectionBDT fInvertedTopSelection;
  Count cInvertedSelected;
  Count cInvertedSelectedCR;

  void DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  void DoInvertedAnalysis(const JetSelection::Data& jetData, const int nVertices);

  // Splitted histograms
  HistoSplitter::SplittedTripletTH1s hLdgTrijetPt_CRone;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetMass_CRone;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetBJetBdisc_CRone;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetPt_CRone;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetEta_CRone;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetBdisc_CRone;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetPt_CRone;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetMass_CRone;
  //
  HistoSplitter::SplittedTripletTH1s hLdgTrijetPt_SR;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetMass_SR;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetBJetBdisc_SR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetPt_SR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetEta_SR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetBdisc_SR;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetPt_SR;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetMass_SR;
  //
  HistoSplitter::SplittedTripletTH1s hLdgTrijetPt_CRtwo;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetMass_CRtwo;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetBJetBdisc_CRtwo;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetPt_CRtwo;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetEta_CRtwo;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetBdisc_CRtwo;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetPt_CRtwo;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetMass_CRtwo;
  //
  HistoSplitter::SplittedTripletTH1s hLdgTrijetPt_VR;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetMass_VR;
  HistoSplitter::SplittedTripletTH1s hLdgTrijetBJetBdisc_VR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetPt_VR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetEta_VR;
  HistoSplitter::SplittedTripletTH1s hTetrajetBJetBdisc_VR;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetPt_VR;
  HistoSplitter::SplittedTripletTH1s hLdgTetrajetMass_VR;

  // Sanity checks
  WrappedTH1 *hBaseline_IsGenuineB; 
  WrappedTH1 *hInverted_IsGenuineB; 

  // Loose/Medium b-jets in all CRs
  WrappedTH1 *hNBJetsMedium_SR;
  WrappedTH1 *hNBJetsMedium_VR;
  WrappedTH1 *hNBJetsMedium_CRone;
  WrappedTH1 *hNBJetsMedium_CRtwo;
  WrappedTH1 *hBJetsPtMedium_SR;
  WrappedTH1 *hBJetsPtMedium_VR;
  WrappedTH1 *hBJetsPtMedium_CRone;
  WrappedTH1 *hBJetsPtMedium_CRtwo;
  WrappedTH1 *hBJetsEtaMedium_SR;
  WrappedTH1 *hBJetsEtaMedium_VR;
  WrappedTH1 *hBJetsEtaMedium_CRone;
  WrappedTH1 *hBJetsEtaMedium_CRtwo;
  WrappedTH1 *hBJetsBdiscMedium_SR;
  WrappedTH1 *hBJetsBdiscMedium_VR;
  WrappedTH1 *hBJetsBdiscMedium_CRone;
  WrappedTH1 *hBJetsBdiscMedium_CRtwo;
  WrappedTH1 *hNBJetsLoose_SR;
  WrappedTH1 *hNBJetsLoose_VR;
  WrappedTH1 *hNBJetsLoose_CRone;
  WrappedTH1 *hNBJetsLoose_CRtwo;
  WrappedTH1 *hBJetsPtLoose_SR;
  WrappedTH1 *hBJetsPtLoose_VR;
  WrappedTH1 *hBJetsPtLoose_CRone;
  WrappedTH1 *hBJetsPtLoose_CRtwo;
  WrappedTH1 *hBJetsEtaLoose_SR;
  WrappedTH1 *hBJetsEtaLoose_VR;
  WrappedTH1 *hBJetsEtaLoose_CRone;
  WrappedTH1 *hBJetsEtaLoose_CRtwo;
  WrappedTH1 *hBJetsBdiscLoose_SR;
  WrappedTH1 *hBJetsBdiscLoose_VR;
  WrappedTH1 *hBJetsBdiscLoose_CRone;
  WrappedTH1 *hBJetsBdiscLoose_CRtwo;

  // FakeB Triplets (Baseline)
  WrappedTH1Triplet *hBaseline_NBjets_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Njets_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet4Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet5Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet6Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet7Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet4Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet5Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet6Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet7Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet1Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet2Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet3Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet4Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet5Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet6Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet7Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_MET_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_HT_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_MVAmax1_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_MVAmax2_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetM_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetEta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetM_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetM_AfterStandardSelections;

  WrappedTH1Triplet *hBaseline_NBjets_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Njets_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet1Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet2Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet3Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet4Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet5Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet6Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet7Pt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet1Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet2Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet3Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet4Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet5Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet6Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet7Eta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet1Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet2Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet3Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet4Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet5Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet6Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet7Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_MET_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_HT_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_MVAmax1_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_MVAmax2_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetMass_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetMass_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetM_AfterAllSelections;

  WrappedTH1Triplet *hBaseline_NBjets_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Njets_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet1Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet2Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet3Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet4Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet5Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet6Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet7Pt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet1Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet2Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet3Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet4Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet5Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet6Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet7Eta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet1Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet2Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet3Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet4Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet5Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet6Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_Jet7Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_MET_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_HT_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_MVAmax1_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_MVAmax2_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetM_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetEta_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetMass_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetMass_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetM_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetPt_AfterCRSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetM_AfterCRSelections;

  // FakeB Triplets (Inverted)
  WrappedTH1Triplet *hInverted_NBjets_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Njets_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet4Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet5Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet6Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet7Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet4Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet5Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet6Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet7Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet1Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet2Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet3Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet4Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet5Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet6Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet7Bdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_MET_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_HT_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_MVAmax1_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_MVAmax2_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetM_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetEta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetBJetBdisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgDijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgDijetM_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetM_AfterStandardSelections;
  
  WrappedTH1Triplet *hInverted_NBjets_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet1Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet2Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet3Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet1Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet2Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet3Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet1Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet2Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet3Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Njets_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet1Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet2Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet3Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet4Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet5Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet6Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet7Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet1Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet2Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet3Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet4Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet5Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet6Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet7Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet1Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet2Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet3Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet4Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet5Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet6Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet7Bdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_MET_AfterAllSelections;
  WrappedTH1Triplet *hInverted_HT_AfterAllSelections;
  WrappedTH1Triplet *hInverted_MVAmax1_AfterAllSelections;
  WrappedTH1Triplet *hInverted_MVAmax2_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetMass_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetMass_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetBJetBdisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetM_AfterAllSelections;

  WrappedTH1Triplet *hInverted_NBjets_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet1Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet2Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet3Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet1Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet2Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet3Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet1Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet2Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Bjet3Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Njets_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet1Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet2Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet3Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet4Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet5Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet6Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet7Pt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet1Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet2Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet3Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet4Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet5Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet6Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet7Eta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet1Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet2Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet3Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet4Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet5Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet6Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_Jet7Bdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_MET_AfterCRSelections;
  WrappedTH1Triplet *hInverted_HT_AfterCRSelections;
  WrappedTH1Triplet *hInverted_MVAmax1_AfterCRSelections;
  WrappedTH1Triplet *hInverted_MVAmax2_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetM_AfterCRSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetEta_AfterCRSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetMass_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetMass_AfterCRSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetBJetBdisc_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgDijetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_LdgDijetM_AfterCRSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetPt_AfterCRSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetM_AfterCRSelections;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(FakeBMeasurement);

FakeBMeasurement::FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_BaselineNumberOfBJets(config, "FakeBMeasurement.baselineBJetsCut"),
    cfg_BaselineBJetsDiscr(config.getParameter<std::string>("FakeBMeasurement.baselineBJetsDiscr")),
    cfg_BaselineBJetsDiscrWP(config.getParameter<std::string>("FakeBMeasurement.baselineBJetsDiscrWP")),
    cfg_LdgTopMVACut(config, "FakeBMeasurement.LdgTopMVACut"),
    cfg_SubldgTopMVACut(config, "FakeBMeasurement.SubldgTopMVACut"),
    cfg_MinTopMVACut(config, "FakeBMeasurement.minTopMVACut"),
    cfg_BjetDiscr(config.getParameter<std::string>("FakeBBjetSelection.bjetDiscr")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kFakeBMeasurement, fHistoWrapper),
    // fNormalizationSystematicsSignalRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsSignalRegion, fHistoWrapper), // fixme
    // fNormalizationSystematicsControlRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsControlRegion, fHistoWrapper),// fixme
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("Passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBaselineBTaggingCounter(fEventCounter.addCounter("Baseline: passed b-jet selection")),
    cBaselineBTaggingSFCounter(fEventCounter.addCounter("Baseline: b tag SF")),
    fBaselineBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBaselineMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fBaselineTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    cBaselineSelected(fEventCounter.addCounter("Baseline: selected events")),
    cBaselineSelectedCR(fEventCounter.addCounter("Baseline: selected CR events")),
    cInvertedBTaggingCounter(fEventCounter.addCounter("Inverted: passed b-jet selection")),
    cInvertedBTaggingSFCounter(fEventCounter.addCounter("Inverted: b tag SF")),
    fInvertedBJetSelection(config.getParameter<ParameterSet>("FakeBBjetSelection")),//, fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fInvertedMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fInvertedTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    cInvertedSelected(fEventCounter.addCounter("Inverted: selected events")),
    cInvertedSelectedCR(fEventCounter.addCounter("Inverted: selected CR events"))
{ }


FakeBMeasurement::~FakeBMeasurement() {  
  // CRone (Baseline b-jets, Inverted Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetPt_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetMass_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetBJetBdisc_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetPt_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetEta_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetBdisc_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetPt_CRone);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetMass_CRone);
  // SR (Baseline b-jets, Baseline Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetPt_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetMass_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetBJetBdisc_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetPt_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetEta_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetBdisc_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetPt_SR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetMass_SR);
  // VR (Inverted b-jets, Inverted Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetPt_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetMass_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetBJetBdisc_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetPt_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetEta_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetBdisc_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetPt_CRtwo);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetMass_CRtwo);
  // VR (Inverted b-jets, Baseline Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetPt_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetMass_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTrijetBJetBdisc_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetPt_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetEta_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hTetrajetBJetBdisc_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetPt_VR);
  fCommonPlots.getHistoSplitter().deleteHistograms(hLdgTetrajetMass_VR);

  // Loose/Medium b-jets in all CRs
  delete hNBJetsMedium_SR;
  delete hNBJetsMedium_VR;
  delete hNBJetsMedium_CRone;
  delete hNBJetsMedium_CRtwo;
  delete hBJetsPtMedium_SR;
  delete hBJetsPtMedium_VR;
  delete hBJetsPtMedium_CRone;
  delete hBJetsPtMedium_CRtwo;
  delete hBJetsEtaMedium_SR;
  delete hBJetsEtaMedium_VR;
  delete hBJetsEtaMedium_CRone;
  delete hBJetsEtaMedium_CRtwo;
  delete hBJetsBdiscMedium_SR;
  delete hBJetsBdiscMedium_VR;
  delete hBJetsBdiscMedium_CRone;
  delete hBJetsBdiscMedium_CRtwo;
  delete hNBJetsLoose_SR;
  delete hNBJetsLoose_VR;
  delete hNBJetsLoose_CRone;
  delete hNBJetsLoose_CRtwo;
  delete hBJetsPtLoose_SR;
  delete hBJetsPtLoose_VR;
  delete hBJetsPtLoose_CRone;
  delete hBJetsPtLoose_CRtwo;
  delete hBJetsEtaLoose_SR;
  delete hBJetsEtaLoose_VR;
  delete hBJetsEtaLoose_CRone;
  delete hBJetsEtaLoose_CRtwo;
  delete hBJetsBdiscLoose_SR;
  delete hBJetsBdiscLoose_VR;
  delete hBJetsBdiscLoose_CRone;
  delete hBJetsBdiscLoose_CRtwo;

  // FakeB Triplets (Baseline)
  delete hBaseline_NBjets_AfterStandardSelections;
  delete hBaseline_Bjet1Pt_AfterStandardSelections;
  delete hBaseline_Bjet2Pt_AfterStandardSelections;
  delete hBaseline_Bjet3Pt_AfterStandardSelections;
  // hBaseline_BjetsPt_AfterStandardSelections.clear();
  delete hBaseline_Bjet1Eta_AfterStandardSelections;
  delete hBaseline_Bjet2Eta_AfterStandardSelections;
  delete hBaseline_Bjet3Eta_AfterStandardSelections;
  // hBaseline_BjetsEta_AfterStandardSelections.clear();
  delete hBaseline_Bjet1Bdisc_AfterStandardSelections;
  delete hBaseline_Bjet2Bdisc_AfterStandardSelections;
  delete hBaseline_Bjet3Bdisc_AfterStandardSelections;
  // hBaseline_BjetsBdisc_AfterStandardSelections.clear();
  delete hBaseline_Njets_AfterStandardSelections;
  delete hBaseline_Jet1Pt_AfterStandardSelections;
  delete hBaseline_Jet2Pt_AfterStandardSelections;
  delete hBaseline_Jet3Pt_AfterStandardSelections;
  delete hBaseline_Jet4Pt_AfterStandardSelections;
  delete hBaseline_Jet5Pt_AfterStandardSelections;
  delete hBaseline_Jet6Pt_AfterStandardSelections;
  delete hBaseline_Jet7Pt_AfterStandardSelections;
  // hBaseline_JetsPt_AfterStandardSelections.clear();
  delete hBaseline_Jet1Eta_AfterStandardSelections;
  delete hBaseline_Jet2Eta_AfterStandardSelections;
  delete hBaseline_Jet3Eta_AfterStandardSelections;
  delete hBaseline_Jet4Eta_AfterStandardSelections;
  delete hBaseline_Jet5Eta_AfterStandardSelections;
  delete hBaseline_Jet6Eta_AfterStandardSelections;
  delete hBaseline_Jet7Eta_AfterStandardSelections;
  // hBaseline_JetsEta_AfterStandardSelections.clear();
  delete hBaseline_Jet1Bdisc_AfterStandardSelections;
  delete hBaseline_Jet2Bdisc_AfterStandardSelections;
  delete hBaseline_Jet3Bdisc_AfterStandardSelections;
  delete hBaseline_Jet4Bdisc_AfterStandardSelections;
  delete hBaseline_Jet5Bdisc_AfterStandardSelections;
  delete hBaseline_Jet6Bdisc_AfterStandardSelections;
  delete hBaseline_Jet7Bdisc_AfterStandardSelections;
  // hBaseline_JetsBdisc_AfterStandardSelections.clear();
  delete hBaseline_MET_AfterStandardSelections;
  delete hBaseline_HT_AfterStandardSelections;
  delete hBaseline_MVAmax1_AfterStandardSelections;
  delete hBaseline_MVAmax2_AfterStandardSelections;
  delete hBaseline_LdgTetrajetPt_AfterStandardSelections;
  delete hBaseline_LdgTetrajetM_AfterStandardSelections;
  delete hBaseline_TetrajetBJetPt_AfterStandardSelections;
  delete hBaseline_TetrajetBJetEta_AfterStandardSelections;
  delete hBaseline_TetrajetBJetBdisc_AfterStandardSelections;
  delete hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_LdgTrijetPt_AfterStandardSelections;
  delete hBaseline_LdgTrijetMass_AfterStandardSelections;
  delete hBaseline_LdgTrijetBJetBdisc_AfterStandardSelections;
  delete hBaseline_SubLdgTrijetPt_AfterStandardSelections;
  delete hBaseline_SubLdgTrijetMass_AfterStandardSelections;
  delete hBaseline_SubLdgTrijetBJetBdisc_AfterStandardSelections;
  delete hBaseline_LdgDijetPt_AfterStandardSelections;
  delete hBaseline_LdgDijetM_AfterStandardSelections;
  delete hBaseline_SubLdgDijetPt_AfterStandardSelections;
  delete hBaseline_SubLdgDijetM_AfterStandardSelections;

  delete hBaseline_NBjets_AfterAllSelections;
  delete hBaseline_Bjet1Pt_AfterAllSelections;
  delete hBaseline_Bjet2Pt_AfterAllSelections;
  delete hBaseline_Bjet3Pt_AfterAllSelections;
  // hBaseline_BjetsPt_AfterAllSelections.clear();
  delete hBaseline_Bjet1Eta_AfterAllSelections;
  delete hBaseline_Bjet2Eta_AfterAllSelections;
  delete hBaseline_Bjet3Eta_AfterAllSelections;
  //  hBaseline_BjetsEta_AfterAllSelections.clear();
  delete hBaseline_Bjet1Bdisc_AfterAllSelections;
  delete hBaseline_Bjet2Bdisc_AfterAllSelections;
  delete hBaseline_Bjet3Bdisc_AfterAllSelections;
  //  hBaseline_BjetsBdisc_AfterAllSelections.clear();
  delete hBaseline_Njets_AfterAllSelections;
  delete hBaseline_Jet1Pt_AfterAllSelections;
  delete hBaseline_Jet2Pt_AfterAllSelections;
  delete hBaseline_Jet3Pt_AfterAllSelections;
  delete hBaseline_Jet4Pt_AfterAllSelections;
  delete hBaseline_Jet5Pt_AfterAllSelections;
  delete hBaseline_Jet6Pt_AfterAllSelections;
  delete hBaseline_Jet7Pt_AfterAllSelections;
  //  hBaseline_JetsPt_AfterAllSelections.clear();
  delete hBaseline_Jet1Eta_AfterAllSelections;
  delete hBaseline_Jet2Eta_AfterAllSelections;
  delete hBaseline_Jet3Eta_AfterAllSelections;
  delete hBaseline_Jet4Eta_AfterAllSelections;
  delete hBaseline_Jet5Eta_AfterAllSelections;
  delete hBaseline_Jet6Eta_AfterAllSelections;
  delete hBaseline_Jet7Eta_AfterAllSelections;
  //  hBaseline_JetsEta_AfterAllSelections.clear();
  delete hBaseline_Jet1Bdisc_AfterAllSelections;
  delete hBaseline_Jet2Bdisc_AfterAllSelections;
  delete hBaseline_Jet3Bdisc_AfterAllSelections;
  delete hBaseline_Jet4Bdisc_AfterAllSelections;
  delete hBaseline_Jet5Bdisc_AfterAllSelections;
  delete hBaseline_Jet6Bdisc_AfterAllSelections;
  delete hBaseline_Jet7Bdisc_AfterAllSelections;
  //  hBaseline_JetsBdisc_AfterAllSelections.clear();
  delete hBaseline_MET_AfterAllSelections;
  delete hBaseline_HT_AfterAllSelections;
  delete hBaseline_MVAmax1_AfterAllSelections;
  delete hBaseline_MVAmax2_AfterAllSelections;
  delete hBaseline_LdgTetrajetPt_AfterAllSelections;
  delete hBaseline_LdgTetrajetM_AfterAllSelections;
  delete hBaseline_TetrajetBJetPt_AfterAllSelections;
  delete hBaseline_TetrajetBJetEta_AfterAllSelections;
  delete hBaseline_TetrajetBJetBdisc_AfterAllSelections;
  delete hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_LdgTrijetPt_AfterAllSelections;
  delete hBaseline_LdgTrijetMass_AfterAllSelections;
  delete hBaseline_LdgTrijetBJetBdisc_AfterAllSelections;
  delete hBaseline_SubLdgTrijetPt_AfterAllSelections;
  delete hBaseline_SubLdgTrijetMass_AfterAllSelections;
  delete hBaseline_SubLdgTrijetBJetBdisc_AfterAllSelections;
  delete hBaseline_LdgDijetPt_AfterAllSelections;
  delete hBaseline_LdgDijetM_AfterAllSelections;
  delete hBaseline_SubLdgDijetPt_AfterAllSelections;
  delete hBaseline_SubLdgDijetM_AfterAllSelections;

  delete hBaseline_NBjets_AfterCRSelections;
  delete hBaseline_Bjet1Pt_AfterCRSelections;
  delete hBaseline_Bjet2Pt_AfterCRSelections;
  delete hBaseline_Bjet3Pt_AfterCRSelections;
  // hBaseline_BjetsPt_AfterCRSelections.clear();
  delete hBaseline_Bjet1Eta_AfterCRSelections;
  delete hBaseline_Bjet2Eta_AfterCRSelections;
  delete hBaseline_Bjet3Eta_AfterCRSelections;
  //  hBaseline_BjetsEta_AfterCRSelections.clear();
  delete hBaseline_Bjet1Bdisc_AfterCRSelections;
  delete hBaseline_Bjet2Bdisc_AfterCRSelections;
  delete hBaseline_Bjet3Bdisc_AfterCRSelections;
  //  hBaseline_BjetsBdisc_AfterCRSelections.clear();
  delete hBaseline_Njets_AfterCRSelections;
  delete hBaseline_Jet1Pt_AfterCRSelections;
  delete hBaseline_Jet2Pt_AfterCRSelections;
  delete hBaseline_Jet3Pt_AfterCRSelections;
  delete hBaseline_Jet4Pt_AfterCRSelections;
  delete hBaseline_Jet5Pt_AfterCRSelections;
  delete hBaseline_Jet6Pt_AfterCRSelections;
  delete hBaseline_Jet7Pt_AfterCRSelections;
  //  hBaseline_JetsPt_AfterCRSelections.clear();
  delete hBaseline_Jet1Eta_AfterCRSelections;
  delete hBaseline_Jet2Eta_AfterCRSelections;
  delete hBaseline_Jet3Eta_AfterCRSelections;
  delete hBaseline_Jet4Eta_AfterCRSelections;
  delete hBaseline_Jet5Eta_AfterCRSelections;
  delete hBaseline_Jet6Eta_AfterCRSelections;
  delete hBaseline_Jet7Eta_AfterCRSelections;
  //  hBaseline_JetsEta_AfterCRSelections.clear();
  delete hBaseline_Jet1Bdisc_AfterCRSelections;
  delete hBaseline_Jet2Bdisc_AfterCRSelections;
  delete hBaseline_Jet3Bdisc_AfterCRSelections;
  delete hBaseline_Jet4Bdisc_AfterCRSelections;
  delete hBaseline_Jet5Bdisc_AfterCRSelections;
  delete hBaseline_Jet6Bdisc_AfterCRSelections;
  delete hBaseline_Jet7Bdisc_AfterCRSelections;
  //  hBaseline_JetsBdisc_AfterCRSelections.clear();
  delete hBaseline_MET_AfterCRSelections;
  delete hBaseline_HT_AfterCRSelections;
  delete hBaseline_MVAmax1_AfterCRSelections;
  delete hBaseline_MVAmax2_AfterCRSelections;
  delete hBaseline_LdgTetrajetPt_AfterCRSelections;
  delete hBaseline_LdgTetrajetM_AfterCRSelections;
  delete hBaseline_TetrajetBJetPt_AfterCRSelections;
  delete hBaseline_TetrajetBJetEta_AfterCRSelections;
  delete hBaseline_TetrajetBJetBdisc_AfterCRSelections;
  delete hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hBaseline_LdgTrijetPt_AfterCRSelections;
  delete hBaseline_LdgTrijetMass_AfterCRSelections;
  delete hBaseline_LdgTrijetBJetBdisc_AfterCRSelections;
  delete hBaseline_SubLdgTrijetPt_AfterCRSelections;
  delete hBaseline_SubLdgTrijetMass_AfterCRSelections;
  delete hBaseline_SubLdgTrijetBJetBdisc_AfterCRSelections;
  delete hBaseline_LdgDijetPt_AfterCRSelections;
  delete hBaseline_LdgDijetM_AfterCRSelections;
  delete hBaseline_SubLdgDijetPt_AfterCRSelections;
  delete hBaseline_SubLdgDijetM_AfterCRSelections;

  // FakeB Triplets (Inverted)
  delete hInverted_NBjets_AfterStandardSelections;
  delete hInverted_Bjet1Pt_AfterStandardSelections;
  delete hInverted_Bjet2Pt_AfterStandardSelections;
  delete hInverted_Bjet3Pt_AfterStandardSelections;
  //  hInverted_BjetsPt_AfterStandardSelections.clear();
  delete hInverted_Bjet1Eta_AfterStandardSelections;
  delete hInverted_Bjet2Eta_AfterStandardSelections;
  delete hInverted_Bjet3Eta_AfterStandardSelections;
  //  hInverted_JetsEta_AfterStandardSelections.clear();
  delete hInverted_Bjet1Bdisc_AfterStandardSelections;
  delete hInverted_Bjet2Bdisc_AfterStandardSelections;
  delete hInverted_Bjet3Bdisc_AfterStandardSelections;
  //  hInverted_JetsBdisc_AfterStandardSelections.clear();
  delete hInverted_Njets_AfterStandardSelections;
  delete hInverted_Jet1Pt_AfterStandardSelections;
  delete hInverted_Jet2Pt_AfterStandardSelections;
  delete hInverted_Jet3Pt_AfterStandardSelections;
  delete hInverted_Jet4Pt_AfterStandardSelections;
  delete hInverted_Jet5Pt_AfterStandardSelections;
  delete hInverted_Jet6Pt_AfterStandardSelections;
  delete hInverted_Jet7Pt_AfterStandardSelections;
  //  hInverted_JetsPt_AfterStandardSelections.clear();
  delete hInverted_Jet1Eta_AfterStandardSelections;
  delete hInverted_Jet2Eta_AfterStandardSelections;
  delete hInverted_Jet3Eta_AfterStandardSelections;
  delete hInverted_Jet4Eta_AfterStandardSelections;
  delete hInverted_Jet5Eta_AfterStandardSelections;
  delete hInverted_Jet6Eta_AfterStandardSelections;
  delete hInverted_Jet7Eta_AfterStandardSelections;
  //  hInverted_JetsEta_AfterStandardSelections.clear();
  delete hInverted_Jet1Bdisc_AfterStandardSelections;
  delete hInverted_Jet2Bdisc_AfterStandardSelections;
  delete hInverted_Jet3Bdisc_AfterStandardSelections;
  delete hInverted_Jet4Bdisc_AfterStandardSelections;
  delete hInverted_Jet5Bdisc_AfterStandardSelections;
  delete hInverted_Jet6Bdisc_AfterStandardSelections;
  delete hInverted_Jet7Bdisc_AfterStandardSelections;
  //  hInverted_JetsBdisc_AfterStandardSelections.clear();
  delete hInverted_MET_AfterStandardSelections;
  delete hInverted_HT_AfterStandardSelections;
  delete hInverted_MVAmax1_AfterStandardSelections;
  delete hInverted_MVAmax2_AfterStandardSelections;
  delete hInverted_LdgTetrajetPt_AfterStandardSelections;
  delete hInverted_LdgTetrajetM_AfterStandardSelections;
  delete hInverted_TetrajetBJetPt_AfterStandardSelections;
  delete hInverted_TetrajetBJetEta_AfterStandardSelections;
  delete hInverted_TetrajetBJetBdisc_AfterStandardSelections;
  delete hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_LdgTrijetPt_AfterStandardSelections;
  delete hInverted_LdgTrijetMass_AfterStandardSelections;
  delete hInverted_LdgTrijetBJetBdisc_AfterStandardSelections;
  delete hInverted_SubLdgTrijetPt_AfterStandardSelections;
  delete hInverted_SubLdgTrijetMass_AfterStandardSelections;
  delete hInverted_SubLdgTrijetBJetBdisc_AfterStandardSelections;
  delete hInverted_LdgDijetPt_AfterStandardSelections;
  delete hInverted_LdgDijetM_AfterStandardSelections;
  delete hInverted_SubLdgDijetPt_AfterStandardSelections;
  delete hInverted_SubLdgDijetM_AfterStandardSelections;

  delete hInverted_NBjets_AfterAllSelections;
  delete hInverted_Bjet1Pt_AfterAllSelections;
  delete hInverted_Bjet2Pt_AfterAllSelections;
  delete hInverted_Bjet3Pt_AfterAllSelections;
  //  hInverted_BjetsPt_AfterAllSelections.clear();
  delete hInverted_Bjet1Eta_AfterAllSelections;
  delete hInverted_Bjet2Eta_AfterAllSelections;
  delete hInverted_Bjet3Eta_AfterAllSelections;
  //  hInverted_BjetsEta_AfterAllSelections.clear();
  delete hInverted_Bjet1Bdisc_AfterAllSelections;
  delete hInverted_Bjet2Bdisc_AfterAllSelections;
  delete hInverted_Bjet3Bdisc_AfterAllSelections;
  //  hInverted_BjetsBdisc_AfterAllSelections.clear();
  delete hInverted_Njets_AfterAllSelections;
  delete hInverted_Jet1Pt_AfterAllSelections;
  delete hInverted_Jet2Pt_AfterAllSelections;
  delete hInverted_Jet3Pt_AfterAllSelections;
  delete hInverted_Jet4Pt_AfterAllSelections;
  delete hInverted_Jet5Pt_AfterAllSelections;
  delete hInverted_Jet6Pt_AfterAllSelections;
  delete hInverted_Jet7Pt_AfterAllSelections;
  //  hInverted_JetsPt_AfterAllSelections.clear();
  delete hInverted_Jet1Eta_AfterAllSelections;
  delete hInverted_Jet2Eta_AfterAllSelections;
  delete hInverted_Jet3Eta_AfterAllSelections;
  delete hInverted_Jet4Eta_AfterAllSelections;
  delete hInverted_Jet5Eta_AfterAllSelections;
  delete hInverted_Jet6Eta_AfterAllSelections;
  delete hInverted_Jet7Eta_AfterAllSelections;
  //  hInverted_JetsEta_AfterAllSelections.clear();
  delete hInverted_Jet1Bdisc_AfterAllSelections;
  delete hInverted_Jet2Bdisc_AfterAllSelections;
  delete hInverted_Jet3Bdisc_AfterAllSelections;
  delete hInverted_Jet4Bdisc_AfterAllSelections;
  delete hInverted_Jet5Bdisc_AfterAllSelections;
  delete hInverted_Jet6Bdisc_AfterAllSelections;
  delete hInverted_Jet7Bdisc_AfterAllSelections;
  //  hInverted_JetsBdisc_AfterAllSelections.clear();
  delete hInverted_MET_AfterAllSelections;
  delete hInverted_HT_AfterAllSelections;
  delete hInverted_MVAmax1_AfterAllSelections;
  delete hInverted_MVAmax2_AfterAllSelections;
  delete hInverted_LdgTetrajetPt_AfterAllSelections;
  delete hInverted_LdgTetrajetM_AfterAllSelections;
  delete hInverted_TetrajetBJetPt_AfterAllSelections;
  delete hInverted_TetrajetBJetEta_AfterAllSelections;
  delete hInverted_TetrajetBJetBdisc_AfterAllSelections;
  delete hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_LdgTrijetPt_AfterAllSelections;
  delete hInverted_LdgTrijetMass_AfterAllSelections;
  delete hInverted_LdgTrijetBJetBdisc_AfterAllSelections;
  delete hInverted_SubLdgTrijetPt_AfterAllSelections;
  delete hInverted_SubLdgTrijetMass_AfterAllSelections;
  delete hInverted_SubLdgTrijetBJetBdisc_AfterAllSelections;
  delete hInverted_LdgDijetPt_AfterAllSelections;
  delete hInverted_LdgDijetM_AfterAllSelections;
  delete hInverted_SubLdgDijetPt_AfterAllSelections;
  delete hInverted_SubLdgDijetM_AfterAllSelections;

  delete hInverted_NBjets_AfterCRSelections;
  delete hInverted_Bjet1Pt_AfterCRSelections;
  delete hInverted_Bjet2Pt_AfterCRSelections;
  delete hInverted_Bjet3Pt_AfterCRSelections;
  //  hInverted_BjetsPt_AfterCRSelections.clear();
  delete hInverted_Bjet1Eta_AfterCRSelections;
  delete hInverted_Bjet2Eta_AfterCRSelections;
  delete hInverted_Bjet3Eta_AfterCRSelections;
  //  hInverted_BjetsEta_AfterCRSelections.clear();
  delete hInverted_Bjet1Bdisc_AfterCRSelections;
  delete hInverted_Bjet2Bdisc_AfterCRSelections;
  delete hInverted_Bjet3Bdisc_AfterCRSelections;
  //  hInverted_BjetsBdisc_AfterCRSelections.clear();
  delete hInverted_Njets_AfterCRSelections;
  delete hInverted_Jet1Pt_AfterCRSelections;
  delete hInverted_Jet2Pt_AfterCRSelections;
  delete hInverted_Jet3Pt_AfterCRSelections;
  delete hInverted_Jet4Pt_AfterCRSelections;
  delete hInverted_Jet5Pt_AfterCRSelections;
  delete hInverted_Jet6Pt_AfterCRSelections;
  delete hInverted_Jet7Pt_AfterCRSelections;
  //  hInverted_JetsPt_AfterCRSelections.clear();
  delete hInverted_Jet1Eta_AfterCRSelections;
  delete hInverted_Jet2Eta_AfterCRSelections;
  delete hInverted_Jet3Eta_AfterCRSelections;
  delete hInverted_Jet4Eta_AfterCRSelections;
  delete hInverted_Jet5Eta_AfterCRSelections;
  delete hInverted_Jet6Eta_AfterCRSelections;
  delete hInverted_Jet7Eta_AfterCRSelections;
  //  hInverted_JetsEta_AfterCRSelections.clear();
  delete hInverted_Jet1Bdisc_AfterCRSelections;
  delete hInverted_Jet2Bdisc_AfterCRSelections;
  delete hInverted_Jet3Bdisc_AfterCRSelections;
  delete hInverted_Jet4Bdisc_AfterCRSelections;
  delete hInverted_Jet5Bdisc_AfterCRSelections;
  delete hInverted_Jet6Bdisc_AfterCRSelections;
  delete hInverted_Jet7Bdisc_AfterCRSelections;
  //  hInverted_JetsBdisc_AfterCRSelections.clear();
  delete hInverted_MET_AfterCRSelections;
  delete hInverted_HT_AfterCRSelections;
  delete hInverted_MVAmax1_AfterCRSelections;
  delete hInverted_MVAmax2_AfterCRSelections;
  delete hInverted_LdgTetrajetPt_AfterCRSelections;
  delete hInverted_LdgTetrajetM_AfterCRSelections;
  delete hInverted_TetrajetBJetPt_AfterCRSelections;
  delete hInverted_TetrajetBJetEta_AfterCRSelections;
  delete hInverted_TetrajetBJetBdisc_AfterCRSelections;
  delete hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections;
  delete hInverted_LdgTrijetPt_AfterCRSelections;
  delete hInverted_LdgTrijetMass_AfterCRSelections;
  delete hInverted_LdgTrijetBJetBdisc_AfterCRSelections;
  delete hInverted_SubLdgTrijetPt_AfterCRSelections;
  delete hInverted_SubLdgTrijetMass_AfterCRSelections;
  delete hInverted_SubLdgTrijetBJetBdisc_AfterCRSelections;
  delete hInverted_LdgDijetPt_AfterCRSelections;
  delete hInverted_LdgDijetM_AfterCRSelections;
  delete hInverted_SubLdgDijetPt_AfterCRSelections;
  delete hInverted_SubLdgDijetM_AfterCRSelections;

}

void FakeBMeasurement::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  // fNormalizationSystematicsSignalRegion.book(dir, isData()); // fixme
  // fNormalizationSystematicsControlRegion.book(dir, isData()); // fixme

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  // Baseline selection
  fBaselineBJetSelection.bookHistograms(dir);
  fBaselineMETSelection.bookHistograms(dir);
  fBaselineTopSelection.bookHistograms(dir);
  // Inverted selection
  fInvertedBJetSelection.bookHistograms(dir);
  fInvertedMETSelection.bookHistograms(dir);
  fInvertedTopSelection.bookHistograms(dir);
  
  // ====== Histogram settings
  HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();

  // Obtain binning
  const int nNBins        = fCommonPlots.getNjetsBinSettings().bins();
  const float fNMin       = fCommonPlots.getNjetsBinSettings().min();
  const float fNMax       = fCommonPlots.getNjetsBinSettings().max();

  const int nBtagBins     = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBtagMin    = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBtagMax    = fCommonPlots.getBJetDiscBinSettings().max();

  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = 2*fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = 2*fCommonPlots.getPtBinSettings().max();

  const int  nEtaBins     = fCommonPlots.getEtaBinSettings().bins();
  const float fEtaMin     = fCommonPlots.getEtaBinSettings().min();
  const float fEtaMax     = fCommonPlots.getEtaBinSettings().max();

  const int  nBDiscBins   = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBDiscMin   = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBDiscMax   = fCommonPlots.getBJetDiscBinSettings().max();

  const int nDEtaBins     = fCommonPlots.getDeltaEtaBinSettings().bins();
  const double fDEtaMin   = fCommonPlots.getDeltaEtaBinSettings().min();
  const double fDEtaMax   = fCommonPlots.getDeltaEtaBinSettings().max();

  const int nDPhiBins     = fCommonPlots.getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots.getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots.getDeltaPhiBinSettings().max();

  const int nDRBins       = fCommonPlots.getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots.getDeltaRBinSettings().min();
  const double fDRMax     = fCommonPlots.getDeltaRBinSettings().max();

  const int nWMassBins    = fCommonPlots.getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots.getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots.getWMassBinSettings().max();

  const int nTopMassBins  = fCommonPlots.getTopMassBinSettings().bins();
  const float fTopMassMin = fCommonPlots.getTopMassBinSettings().min();
  const float fTopMassMax = fCommonPlots.getTopMassBinSettings().max();

  const int nInvMassBins  = fCommonPlots.getInvMassBinSettings().bins();
  const float fInvMassMin = fCommonPlots.getInvMassBinSettings().min();
  const float fInvMassMax = fCommonPlots.getInvMassBinSettings().max();

  const int nMetBins  = fCommonPlots.getMetBinSettings().bins();
  const float fMetMin = fCommonPlots.getMetBinSettings().min();
  const float fMetMax = fCommonPlots.getMetBinSettings().max();

  const int nHtBins  = fCommonPlots.getHtBinSettings().bins();
  const float fHtMin = fCommonPlots.getHtBinSettings().min();
  const float fHtMax = fCommonPlots.getHtBinSettings().max();

  // Create directories for normalization
  std::string myInclusiveLabel  = "ForFakeBSanity";
  std::string myFakeLabel       = myInclusiveLabel+"EWKFakeB";
  std::string myGenuineLabel    = myInclusiveLabel+"EWKGenuineB";
  // TDirectory* myNormDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  // TDirectory* myNormEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  // TDirectory* myNormGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  // std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeBDir, myNormGenuineBDir};


  // Other histograms
  TDirectory* MvL = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, "ForFakeBMediumVsLoose");
  hNBJetsMedium_SR        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsMedium_SR"       , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax);
  hNBJetsMedium_VR        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsMedium_VR"       , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hNBJetsMedium_CRone     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsMedium_CRone"    , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hNBJetsMedium_CRtwo     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsMedium_CRtwo"    , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hBJetsPtMedium_SR       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtMedium_SR"      , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtMedium_VR       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtMedium_VR"      , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtMedium_CRone    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtMedium_CRone"   , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtMedium_CRtwo    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtMedium_CRtwo"   , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsEtaMedium_SR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaMedium_SR"     , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaMedium_VR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaMedium_VR"     , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaMedium_CRone   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaMedium_CRone"  , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaMedium_CRtwo   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaMedium_CRtwo"  , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsBdiscMedium_SR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscMedium_SR"   , ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscMedium_VR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscMedium_VR"   , ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscMedium_CRone = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscMedium_CRone", ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscMedium_CRtwo = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscMedium_CRtwo", ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  //
  hNBJetsLoose_SR        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsLoose_SR"       , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax);
  hNBJetsLoose_VR        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsLoose_VR"       , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hNBJetsLoose_CRone     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsLoose_CRone"    , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hNBJetsLoose_CRtwo     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "NBJetsLoose_CRtwo"    , ";b-jet multiplicity;Occur / %0.0f", nNBins, fNMin, fNMax); 
  hBJetsPtLoose_SR       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtLoose_SR"      , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtLoose_VR       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtLoose_VR"      , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtLoose_CRone    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtLoose_CRone"   , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsPtLoose_CRtwo    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsPtLoose_CRtwo"   , ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  hBJetsEtaLoose_SR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaLoose_SR"     , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaLoose_VR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaLoose_VR"     , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaLoose_CRone   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaLoose_CRone"  , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsEtaLoose_CRtwo   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsEtaLoose_CRtwo"  , ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBJetsBdiscLoose_SR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscLoose_SR"   , ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscLoose_VR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscLoose_VR"   , ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscLoose_CRone = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscLoose_CRone", ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);
  hBJetsBdiscLoose_CRtwo = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, MvL, "BJetsBdiscLoose_CRtwo", ";b-tag discriminator;Occur / %.2f", nBDiscBins, fBDiscMin, fBDiscMax);

  // Other histograms
  myInclusiveLabel = "ForFakeBMeasurement";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";
  // Create directories
  TDirectory* myFakeBDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeBEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myFakeBGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFakeBDirs = {myFakeBDir, myFakeBEWKFakeBDir, myFakeBGenuineBDir};
  
  // Splitted Histo Triplets
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetPt_CRone, "LdgTrijetPt_CRone", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetMass_CRone, "LdgTrijetMass_CRone", 
  						  ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetBJetBdisc_CRone, "LdgTrijetBJetBdisc_CRone", 
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetPt_CRone, "TetrajetBJetPt_CRone", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetEta_CRone, "TetrajetBJetEta_CRone", 
  						  ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetBdisc_CRone, "TetrajetBJetBdisc_CR",
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetPt_CRone, "LdgTetrajetPt_CRone",
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetMass_CRone, "LdgTetrajetMass_CRone", 
						  ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);
  
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetPt_SR, "LdgTrijetPt_SR", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetMass_SR, "LdgTrijetMass_SR", 
  						  ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetBJetBdisc_SR, "LdgTrijetBJetBdisc_SR", 
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetPt_SR, "TetrajetBJetPt_SR", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetEta_SR, "TetrajetBJetEta_SR", 
  						  ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetBdisc_SR, "TetrajetBJetBdisc_SR",
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetPt_SR, "LdgTetrajetPt_SR", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetMass_SR, "LdgTetrajetMass_SR", 
  						  ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);
  
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetPt_CRtwo, "LdgTrijetPt_CRtwo", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetMass_CRtwo, "LdgTrijetMass_CRtwo", 
  						  ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetBJetBdisc_CRtwo, "LdgTrijetBJetBdisc_CRtwo", 
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetPt_CRtwo, "TetrajetBJetPt_CRtwo", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetEta_CRtwo, "TetrajetBJetEta_CRtwo",
  						  ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs,	hTetrajetBJetBdisc_CRtwo, "TetrajetBJetBdisc_CRtwo", 
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetPt_CRtwo, "LdgTetrajetPt_CRtwo", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetMass_CRtwo, "LdgTetrajetMass_CRtwo",
  						  ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetPt_VR, "LdgTrijetPt_VR", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetMass_VR, "LdgTrijetMass_VR", 
  						  ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTrijetBJetBdisc_VR, "LdgTrijetBJetBdisc_VR",
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetPt_VR, "TetrajetBJetPt_VR", 
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetEta_VR, "TetrajetBJetEta_VR", 
  						  ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hTetrajetBJetBdisc_VR, "TetrajetBJetBdisc_VR", 
  						  ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetPt_VR, "LdgTetrajetPt_VR",
  						  ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins, fPtMin, fPtMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hLdgTetrajetMass_VR, "LdgTetrajetMass_VR",
  						  ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);						 

  // Normal Histos
  hBaseline_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Baseline_IsGenuineB", ";is genuine-b;Events / %0.0f", 2, 0.0, 2.0);
  hInverted_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Inverted_IsGenuineB", ";is genuine-b;Events / %0.0f", 2, 0.0, 2.0);

  // Baseline selection (StandardSelections)
  hBaseline_NBjets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_NBjets_AfterStandardSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hBaseline_Bjet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Bjet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Bjet1Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet2Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet3Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_Njets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Njets_AfterStandardSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hBaseline_Jet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet4Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet5Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet6Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet7Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Jet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet4Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet5Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet6Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet7Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Jet1Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet2Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet3Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet4Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet5Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet6Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet7Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_MET_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MET_AfterStandardSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hBaseline_HT_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_HT_AfterStandardSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hBaseline_MVAmax1_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax1_AfterStandardSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hBaseline_MVAmax2_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax2_AfterStandardSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hBaseline_LdgTetrajetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_LdgTetrajetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetMass_AfterStandardSelections", ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TetrajetBJetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TetrajetBJetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TetrajetBJetEta_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetEta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_TetrajetBJetBdisc_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hBaseline_LdgTrijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgTrijetMass_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgTrijetBJetBdisc_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_SubLdgTrijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgTrijetMass_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_SubLdgTrijetBJetBdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_LdgDijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_SubLdgDijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Baseline selection (AllSelections)
  hBaseline_NBjets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_NBjets_AfterAllSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hBaseline_Bjet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Bjet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Bjet1Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet2Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet3Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_Njets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Njets_AfterAllSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hBaseline_Jet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet4Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet5Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet6Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet7Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Jet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet4Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet5Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet6Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet7Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Jet1Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet2Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet3Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet4Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet5Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet6Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet7Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_MET_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MET_AfterAllSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hBaseline_HT_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_HT_AfterAllSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hBaseline_MVAmax1_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax1_AfterAllSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hBaseline_MVAmax2_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax2_AfterAllSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hBaseline_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetEta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_TetrajetBJetBdisc_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hBaseline_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgTrijetMass_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgTrijetBJetBdisc_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgTrijetMass_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_SubLdgTrijetBJetBdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Baseline selection (CRSelections)
  hBaseline_NBjets_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_NBjets_AfterCRSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hBaseline_Bjet1Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet2Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet3Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Bjet1Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet2Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet3Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Bjet1Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet2Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet3Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_Njets_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Njets_AfterCRSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hBaseline_Jet1Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet2Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet3Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet4Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet5Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet6Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet7Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Jet1Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet2Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet3Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet4Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet5Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet6Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet7Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Jet1Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet2Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet3Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet4Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet5Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet6Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet7Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_MET_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MET_AfterCRSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hBaseline_HT_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_HT_AfterCRSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hBaseline_MVAmax1_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax1_AfterCRSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hBaseline_MVAmax2_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax2_AfterCRSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hBaseline_LdgTetrajetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_LdgTetrajetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetMass_AfterCRSelections", ";m_{jjbb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TetrajetBJetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TetrajetBJetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TetrajetBJetEta_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetEta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_TetrajetBJetBdisc_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hBaseline_LdgTrijetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTrijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgTrijetMass_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetMass_AfterCRSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgTrijetBJetBdisc_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_SubLdgTrijetPt_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgTrijetMass_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetMass_AfterCRSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_SubLdgTrijetBJetBdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_LdgDijetPt_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgDijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgDijetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgDijetM_AfterCRSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_SubLdgDijetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgDijetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetM_AfterCRSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection (StandardSelections)
  hInverted_NBjets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_NBjets_AfterStandardSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hInverted_Bjet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Bjet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Bjet1Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet2Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet3Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_Njets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Njets_AfterStandardSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hInverted_Jet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet4Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet5Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet6Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet7Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Pt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Jet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet4Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet5Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet6Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet7Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Eta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Jet1Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet2Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet3Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet4Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet5Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet6Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet7Bdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Bdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_MET_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MET_AfterStandardSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hInverted_HT_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_HT_AfterStandardSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hInverted_MVAmax1_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax1_AfterStandardSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hInverted_MVAmax2_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax2_AfterStandardSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hInverted_LdgTetrajetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_LdgTetrajetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetMass_AfterStandardSelections", ";m_{jjjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TetrajetBJetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TetrajetBJetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TetrajetBJetEta_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetEta_AfterStandardSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_TetrajetBJetBdisc_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hInverted_LdgTrijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgTrijetMass_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgTrijetBJetBdisc_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_SubLdgTrijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgTrijetMass_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_SubLdgTrijetBJetBdisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetBJetBdisc_AfterStandardSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_LdgDijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_SubLdgDijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection (AllSelections)
  hInverted_NBjets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_NBjets_AfterAllSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hInverted_Bjet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Bjet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Bjet1Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet2Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet3Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_Njets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Njets_AfterAllSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hInverted_Jet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet4Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet5Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet6Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet7Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Pt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Jet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet4Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet5Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet6Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet7Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Eta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Jet1Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet2Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet3Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet4Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet5Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet6Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet7Bdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Bdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_MET_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MET_AfterAllSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hInverted_HT_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_HT_AfterAllSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hInverted_MVAmax1_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax1_AfterAllSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hInverted_MVAmax2_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax2_AfterAllSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hInverted_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetMass_AfterAllSelections", ";m_{jjjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetEta_AfterAllSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_TetrajetBJetBdisc_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hInverted_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgTrijetMass_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgTrijetBJetBdisc_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgTrijetMass_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_SubLdgTrijetBJetBdisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetBJetBdisc_AfterAllSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection (CRSelections)
  hInverted_NBjets_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_NBjets_AfterCRSelections", ";b-jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);

  hInverted_Bjet1Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet2Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet3Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Bjet1Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet2Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet3Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Bjet1Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet2Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet3Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_Njets_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Njets_AfterCRSelections", ";jet multiplicity;Occur / %.0f", nNBins, fNMin, fNMax);
  hInverted_Jet1Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet2Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet3Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet4Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet5Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet6Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet7Pt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Pt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Jet1Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet2Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet3Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet4Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet5Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet6Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet7Eta_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Eta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Jet1Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet2Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet3Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet4Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet5Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet6Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet7Bdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Bdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_MET_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MET_AfterCRSelections", ";E_{T}^{miss};Occur / %.1f", nMetBins, fMetMin, fMetMax);
  hInverted_HT_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_HT_AfterCRSelections", ";H_{T};Occur / %.1f", nHtBins, fHtMin, fHtMax);
  hInverted_MVAmax1_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax1_AfterCRSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);
  hInverted_MVAmax2_AfterCRSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax2_AfterCRSelections", ";#BDT discriminant;Occur / %.2f", 40, -1.0, +1.0);

  hInverted_LdgTetrajetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_LdgTetrajetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetMass_AfterCRSelections", ";m_{jjjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TetrajetBJetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TetrajetBJetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TetrajetBJetEta_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetEta_AfterCRSelections", ";#eta;Occur / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
  hInverted_TetrajetBJetBdisc_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);
  
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hInverted_LdgTrijetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgTrijetMass_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetMass_AfterCRSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgTrijetBJetBdisc_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_SubLdgTrijetPt_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgTrijetMass_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetMass_AfterCRSelections", ";m_{jjb} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_SubLdgTrijetBJetBdisc_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetBJetBdisc_AfterCRSelections", ";b-tag discriminator;Occur / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_LdgDijetPt_AfterCRSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgDijetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetM_AfterCRSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_SubLdgDijetPt_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetPt_AfterCRSelections", ";p_{T} (GeV/c);Occur / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgDijetM_AfterCRSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetM_AfterCRSelections", ";m_{jj} (GeV/c^{2});Occur / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  return;
}


void FakeBMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void FakeBMeasurement::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  // fNormalizationSystematicsSignalRegion.initialize();  // fixme
  // fNormalizationSystematicsControlRegion.initialize(); // fixme

  cAllEvents.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);

  if (0) std::cout << "\nentry = " << entry << std::endl;

  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;

  cTrigger.increment();
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

  //================================================================================================   
  // 2) MET filters (to remove events with spurious sources of fake MET)
  //================================================================================================   
  if (0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  

  //================================================================================================   
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================   
  if (0) std::cout << "=== Vertices" << std::endl;
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  //================================================================================================   
  // 4) Electron veto (Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================
  // 5) Muon veto (Orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 7) Jet Selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.silentAnalyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  
  //================================================================================================  
  // 8) BJet Selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBaselineBJetSelection.silentAnalyze(fEvent, jetData);

  // Baseline Selection
  if (bjetData.passedSelection()) 
    {
      DoBaselineAnalysis(jetData, bjetData, nVertices);
    }
  else
    {
      DoInvertedAnalysis(jetData, nVertices); 
    }
 
  return;
}
      

bool FakeBMeasurement::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool FakeBMeasurement::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}


void FakeBMeasurement::DoBaselineAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){

  if (0) std::cout << "\n=== FakeBMeasurement::DoBaselineAnalysis()" << std::endl;

  // Increment counter
  cBaselineBTaggingCounter.increment();

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Baseline: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBaselineBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: MET selection" << std::endl;
  const METSelection::Data METData = fBaselineMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;
 
  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  // fNormalizationSystematicsSignalRegion.setFactorisationBinForEvent(myFactorisationInfo); //fixme

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB  
  bool isGenuineB = bjetData.isGenuineB();
  hBaseline_IsGenuineB->Fill(isGenuineB);
  
  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Baseline: Standard Selections" << std::endl;
  // NB: CtrlPlotsAfterStandardSelections should only be called for Inverted!
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, bjetData.isGenuineB());

  // Fill Triplets  (Baseline)
  hBaseline_Njets_AfterStandardSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hBaseline_NBjets_AfterStandardSelections->Fill(isGenuineB, bjetData.getSelectedBJets().size());

  int index = -1;
  // For-loop: All selected bjets
  for (auto bjet: bjetData.getSelectedBJets()) 
    {
      index++;     
      
      if (index > 2) break;

      if (index == 0)
	{
	  hBaseline_Bjet1Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet1Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet1Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Bjet2Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet2Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet2Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Bjet3Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet3Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet3Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}
    }

  index = -1;
  // For-loop: All selected jets
  for (auto jet: jetData.getSelectedJets()) 
    {
      index++;
      // std::cout << "index = " << index << std::endl;
      if (index > 6) break;

      if (index == 0)
	{
	  hBaseline_Jet1Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet1Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet1Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Jet2Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet2Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet2Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Jet3Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet3Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet3Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hBaseline_Jet4Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet4Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet4Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hBaseline_Jet5Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet5Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet5Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hBaseline_Jet6Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet6Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet6Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hBaseline_Jet7Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet7Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet7Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hBaseline_MET_AfterStandardSelections ->Fill(isGenuineB, METData.getMET().R());
  hBaseline_HT_AfterStandardSelections ->Fill(isGenuineB, jetData.HT());
  hBaseline_MVAmax1_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hBaseline_MVAmax2_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hBaseline_LdgTetrajetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hBaseline_LdgTetrajetM_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hBaseline_TetrajetBJetPt_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hBaseline_TetrajetBJetEta_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hBaseline_TetrajetBJetBdisc_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator());
  double dEta = std::abs( topData.getTetrajetBJet().p4().eta() - topData.getLdgTrijetBJet().p4().eta() );
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4() ) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dEta);
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dPhi);
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dR);
  hBaseline_LdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hBaseline_LdgTrijetMass_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hBaseline_LdgTrijetBJetBdisc_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  hBaseline_SubLdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hBaseline_SubLdgTrijetMass_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hBaseline_SubLdgTrijetBJetBdisc_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
  hBaseline_LdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hBaseline_LdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hBaseline_SubLdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hBaseline_SubLdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );


  //================================================================================================
  // All Selections
  //================================================================================================  
  if (!topData.passedSelection()) 
    {
      // If top fails fill determine if it qualifies for Control Region 1 (CRone)
      bool passLdgTopMVA    = cfg_LdgTopMVACut.passedCut( topData.getMVAmax1() );
      bool passSubldgTopMVA = cfg_SubldgTopMVACut.passedCut( topData.getMVAmax2() );
      bool passInvertedTop  = passLdgTopMVA * passSubldgTopMVA;
      if (!passInvertedTop) return;

      if (0) std::cout << "=== Baseline: Control Region 1 (CRone)" << std::endl;
      cBaselineSelectedCR.increment();

      // Fill histos (CR1)
      hBaseline_Njets_AfterCRSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
      hBaseline_NBjets_AfterCRSelections->Fill(isGenuineB, bjetData.getSelectedBJets().size());

      index = -1;
      unsigned int nLoose  = 0;
      unsigned int nMedium = 0;
      // For-loop: All selected bjets
      for (auto bjet: bjetData.getSelectedBJets()) 
	{
	  index++;
	  // Declare variables
	  double pt    = bjet.pt();
	  double eta   = bjet.eta();
	  double bdisc = bjet.bjetDiscriminator();
	  bool bLoose  = (bjet.bjetDiscriminator() > fBaselineBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Loose"));
	  bool bMedium = (bjet.bjetDiscriminator() > fBaselineBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Medium"));
	  if (bLoose)
	    {
	      if (bMedium)
		{
		  nMedium++;
		  hBJetsPtMedium_CRone->Fill(pt);
		  hBJetsEtaMedium_CRone->Fill(eta);
		  hBJetsBdiscMedium_CRone->Fill(bdisc);
		}
	      else
		{
		  nLoose++;
		  hBJetsPtLoose_CRone->Fill(pt);
		  hBJetsEtaLoose_CRone->Fill(eta);
		  hBJetsBdiscLoose_CRone->Fill(bdisc);
		}
	    }

	  if (index == 0)
	    {
	      hBaseline_Bjet1Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hBaseline_Bjet1Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hBaseline_Bjet1Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    }
	  
	  if (index == 1)
	    {
	      hBaseline_Bjet2Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hBaseline_Bjet2Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hBaseline_Bjet2Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    }
	  
	  if (index == 2)
	    {
	      hBaseline_Bjet3Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hBaseline_Bjet3Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hBaseline_Bjet3Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    }
	}
      hNBJetsLoose_CRone ->Fill(nLoose);
      hNBJetsMedium_CRone->Fill(nMedium);
      

      index = -1;
      // For-loop: All selected jets
      for (auto jet: jetData.getSelectedJets()) 
	{
	  index++;
	  if (index > 6) break;
	  
	  if (index == 0)
	    {
	      hBaseline_Jet1Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet1Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet1Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 1)
	    {
	      hBaseline_Jet2Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet2Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet2Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    } 
	  
	  if (index == 2)
	    {
	      hBaseline_Jet3Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet3Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet3Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 3)
	    {
	      hBaseline_Jet4Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet4Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet4Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 4)
	    {
	      hBaseline_Jet5Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet5Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet5Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 5)
	    {
	      hBaseline_Jet6Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet6Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet6Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 6)
	    {
	      hBaseline_Jet7Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hBaseline_Jet7Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hBaseline_Jet7Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	}
      
      hBaseline_MET_AfterCRSelections ->Fill(isGenuineB, METData.getMET().R());
      hBaseline_HT_AfterCRSelections ->Fill(isGenuineB, jetData.HT());
      hBaseline_MVAmax1_AfterCRSelections ->Fill(isGenuineB, topData.getMVAmax1());
      hBaseline_MVAmax2_AfterCRSelections ->Fill(isGenuineB, topData.getMVAmax2());
      hBaseline_LdgTetrajetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
      hBaseline_LdgTetrajetM_AfterCRSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
      hBaseline_TetrajetBJetPt_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
      hBaseline_TetrajetBJetEta_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
      hBaseline_TetrajetBJetBdisc_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
      hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dEta);
      hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dPhi);
      hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dR);
      hBaseline_LdgTrijetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
      hBaseline_LdgTrijetMass_AfterCRSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
      hBaseline_LdgTrijetBJetBdisc_AfterCRSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
      hBaseline_SubLdgTrijetPt_AfterCRSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
      hBaseline_SubLdgTrijetMass_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
      hBaseline_SubLdgTrijetBJetBdisc_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
      hBaseline_LdgDijetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
      hBaseline_LdgDijetM_AfterCRSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
      hBaseline_SubLdgDijetPt_AfterCRSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
      hBaseline_SubLdgDijetM_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );
      
      // Splitted histos
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetPt_CRone, isGenuineB, topData.getLdgTrijet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetMass_CRone, isGenuineB, topData.getLdgTrijet().M() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetBJetBdisc_CRone, isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetPt_CRone, isGenuineB, topData.getTetrajetBJet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetEta_CRone, isGenuineB, topData.getTetrajetBJet().eta() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetBdisc_CRone, isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetPt_CRone, isGenuineB, topData.getLdgTetrajet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetMass_CRone, isGenuineB, topData.getLdgTetrajet().M());
      
      return;
    }

  if (0) std::cout << "=== Baseline: Signal Region (SR)" << std::endl;
  cBaselineSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  hBaseline_Njets_AfterAllSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hBaseline_NBjets_AfterAllSelections->Fill(isGenuineB, bjetData.getSelectedBJets().size());

  index = -1;
  unsigned int nLoose  = 0;
  unsigned int nMedium = 0;
  // For-loop: All selected bjets
  for (auto bjet: bjetData.getSelectedBJets()) 
    {
      index++;
     
      // Declare variables
      double pt    = bjet.pt();
      double eta   = bjet.eta();
      double bdisc = bjet.bjetDiscriminator();
      bool bLoose  = (bjet.bjetDiscriminator() > fBaselineBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Loose"));
      bool bMedium = (bjet.bjetDiscriminator() > fBaselineBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Medium"));
      if (bLoose)
	{
	  if (bMedium)
	    {
	      nMedium++;
	      hBJetsPtMedium_SR->Fill(pt);
	      hBJetsEtaMedium_SR->Fill(eta);
	      hBJetsBdiscMedium_SR->Fill(bdisc);
	    }
	  else
	    {
	      nLoose++;
	      hBJetsPtLoose_SR->Fill(pt);
	      hBJetsEtaLoose_SR->Fill(eta);
	      hBJetsBdiscLoose_SR->Fill(bdisc);
	    }
	}
	  
      if (index == 0)
	{
	  hBaseline_Bjet1Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hBaseline_Bjet1Eta_AfterAllSelections->Fill(isGenuineB, eta );
	  hBaseline_Bjet1Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc );
	}

      if (index == 1)
	{
	  hBaseline_Bjet2Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hBaseline_Bjet2Eta_AfterAllSelections->Fill(isGenuineB, eta);
	  hBaseline_Bjet2Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc);
	}

      if (index == 2)
	{
	  hBaseline_Bjet3Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hBaseline_Bjet3Eta_AfterAllSelections->Fill(isGenuineB, eta);
	  hBaseline_Bjet3Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc);
	}
    }
  hNBJetsLoose_SR ->Fill(nLoose);
  hNBJetsMedium_SR->Fill(nMedium);


  index = -1;
  // For-loop: All selected jets
  for (auto jet: jetData.getSelectedJets()) 
    {
      index++;
      if (index > 6) break;

      if (index == 0)
	{
	  hBaseline_Jet1Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet1Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet1Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Jet2Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet2Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet2Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Jet3Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet3Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet3Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hBaseline_Jet4Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet4Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet4Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hBaseline_Jet5Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet5Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet5Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hBaseline_Jet6Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet6Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet6Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hBaseline_Jet7Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet7Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet7Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hBaseline_MET_AfterAllSelections ->Fill(isGenuineB, METData.getMET().R());
  hBaseline_HT_AfterAllSelections ->Fill(isGenuineB, jetData.HT());
  hBaseline_MVAmax1_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hBaseline_MVAmax2_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hBaseline_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hBaseline_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hBaseline_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hBaseline_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hBaseline_TetrajetBJetBdisc_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hBaseline_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hBaseline_LdgTrijetMass_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hBaseline_LdgTrijetBJetBdisc_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  hBaseline_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hBaseline_SubLdgTrijetMass_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hBaseline_SubLdgTrijetBJetBdisc_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
  hBaseline_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hBaseline_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hBaseline_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hBaseline_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Splitted Histos
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetPt_SR, isGenuineB, topData.getLdgTrijet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetMass_SR, isGenuineB, topData.getLdgTrijet().M() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetBJetBdisc_SR, isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetPt_SR, isGenuineB, topData.getTetrajetBJet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetEta_SR, isGenuineB, topData.getTetrajetBJet().eta() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetBdisc_SR, isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetPt_SR, isGenuineB, topData.getLdgTetrajet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetMass_SR, isGenuineB, topData.getLdgTetrajet().M());

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

void FakeBMeasurement::DoInvertedAnalysis(const JetSelection::Data& jetData,
					  const int nVertices){

  if (0) std::cout << "\n=== FakeBMeasurement::DoInvertedAnalysis()" << std::endl;

  //================================================================================================  
  // 8) BJet Selections
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet selection" << std::endl;
  const BJetSelection::Data invBjetData = fInvertedBJetSelection.silentAnalyze(fEvent, jetData);
  if (!invBjetData.passedSelection()) return;

   // CSVv2-Medium requirement
   unsigned int nBaselineBjets = 0;
   for (auto bjet: invBjetData.getSelectedBJets())
     {
        double discWP = fInvertedBJetSelection.getDiscriminatorWP( cfg_BaselineBJetsDiscr, cfg_BaselineBJetsDiscrWP);
       if (bjet.bjetDiscriminator() < discWP) continue;
       nBaselineBjets++;
     }
   bool passBaselineBjetCuts = cfg_BaselineNumberOfBJets.passedCut(nBaselineBjets); 
   if (!passBaselineBjetCuts) return;
  
  // Increment counter
  cInvertedBTaggingCounter.increment();

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    { 
      fEventWeight.multiplyWeight(invBjetData.getBTaggingScaleFactorEventWeight());
    }
  cInvertedBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fInvertedTopSelection.analyzeWithoutBJets(fEvent, jetData.getSelectedJets(), invBjetData.getSelectedBJets(), true);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  // fNormalizationSystematicsControlRegion.setFactorisationBinForEvent(myFactorisationInfo); //fixme
  // fNormalizationSystematicsControlRegion.fillControlPlotsAfterTauSelection(fEvent, tauData); //fixme

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  bool isGenuineB = invBjetData.isGenuineB();
  hInverted_IsGenuineB->Fill(isGenuineB);

  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Inverted: Preselections" << std::endl;
  fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, invBjetData, METData, TopologySelection::Data(), topData, isGenuineB);

  // Fill Triplets  (Inverted)
  hInverted_Njets_AfterStandardSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hInverted_NBjets_AfterStandardSelections->Fill(isGenuineB, invBjetData.getSelectedBJets().size());

  int index = -1;
  // For-loop: All BJets (Real or Inverted) used in top fit
  for (auto bjet: invBjetData.getSelectedBJets())
    {
      // std::cout << "bjet.bjetDiscriminator() = " << bjet.bjetDiscriminator() << std::endl;
      index++;
      if (index > 2) break;
      
      // NOTE: What is the point of using the "isGenuineB" here? Inclusive = FakeB (approx.)
      if (index == 0)
	{
	  hInverted_Bjet1Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet1Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet1Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Bjet2Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet2Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet2Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Bjet3Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet3Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet3Bdisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}
    }
  // std::cout << "\n" << std::endl;

  index = -1;
  // For-loop: All selected jets
  for (auto jet: jetData.getSelectedJets()) 
    {
      index++;
      // std::cout << "index = " << index << std::endl;
      if (index > 6) break;

      // NOTE: What is the point of using the "isGenuineB" here? Inclusive = FakeB (approx.)
      if (index == 0)
	{
	  hInverted_Jet1Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet1Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet1Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Jet2Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet2Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet2Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Jet3Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet3Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet3Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hInverted_Jet4Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet4Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet4Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hInverted_Jet5Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet5Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet5Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hInverted_Jet6Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet6Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet6Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hInverted_Jet7Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet7Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet7Bdisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hInverted_MET_AfterStandardSelections ->Fill(isGenuineB, METData.getMET().R());
  hInverted_HT_AfterStandardSelections ->Fill(isGenuineB, jetData.HT());
  hInverted_MVAmax1_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hInverted_MVAmax2_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hInverted_LdgTetrajetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hInverted_LdgTetrajetM_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hInverted_TetrajetBJetPt_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hInverted_TetrajetBJetEta_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hInverted_TetrajetBJetBdisc_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
  double dEta = std::abs( topData.getTetrajetBJet().eta() - topData.getLdgTrijetBJet().eta());
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dEta);
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dPhi);
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dR);
  hInverted_LdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hInverted_LdgTrijetMass_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hInverted_LdgTrijetBJetBdisc_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  hInverted_SubLdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hInverted_SubLdgTrijetMass_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hInverted_SubLdgTrijetBJetBdisc_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
  hInverted_LdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hInverted_LdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hInverted_SubLdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hInverted_SubLdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topData.passedSelection()) 
    {
      // If top fails determine if event fall into  Control Region 2 (CR2)
      bool passLdgTopMVA    = cfg_LdgTopMVACut.passedCut( topData.getMVAmax1() );
      bool passSubldgTopMVA = cfg_SubldgTopMVACut.passedCut( topData.getMVAmax2() );
      bool passInvertedTop  = passLdgTopMVA * passSubldgTopMVA;
      if (!passInvertedTop) return;

      if (0) std::cout << "=== Inverted: Control Region 2 (CR2)" << std::endl;
      cInvertedSelectedCR.increment();

      // Fill plots (CR2)
      hInverted_Njets_AfterCRSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
      hInverted_NBjets_AfterCRSelections->Fill(isGenuineB, invBjetData.getSelectedBJets().size()); //invBjetData.getSelectedBJets().size()); 
      
      index   = -1;
      unsigned int nLoose  = 0;
      unsigned int nMedium = 0;
      // For-loop: All b-jets
      for (auto bjet: invBjetData.getSelectedBJets())
	{

	  index++;

	  // Declare variables
	  double pt    = bjet.pt();
	  double eta   = bjet.eta();
	  double bdisc = bjet.bjetDiscriminator();
	  bool bLoose  = (bjet.bjetDiscriminator() > fInvertedBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Loose"));
	  bool bMedium = (bjet.bjetDiscriminator() > fInvertedBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Medium"));
	  if (bLoose)
	    {
	      if (bMedium)
		{
		  nMedium++;
		  hBJetsPtMedium_CRtwo->Fill(pt);
		  hBJetsEtaMedium_CRtwo->Fill(eta);
		  hBJetsBdiscMedium_CRtwo->Fill(bdisc);
		}
	      else
		{
		  nLoose++;
		  hBJetsPtLoose_CRtwo->Fill(pt);
		  hBJetsEtaLoose_CRtwo->Fill(eta);
		  hBJetsBdiscLoose_CRtwo->Fill(bdisc);
		}
	    }
	  
	  if (index == 0)
	    {
	      hInverted_Bjet1Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hInverted_Bjet1Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hInverted_Bjet1Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    }
	  
	  if (index == 1)
	    {
	      hInverted_Bjet2Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hInverted_Bjet2Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hInverted_Bjet2Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    } 
	  
	  if (index == 2)
	    {
	      hInverted_Bjet3Pt_AfterCRSelections->Fill(isGenuineB, pt);
	      hInverted_Bjet3Eta_AfterCRSelections->Fill(isGenuineB, eta);
	      hInverted_Bjet3Bdisc_AfterCRSelections->Fill(isGenuineB, bdisc);
	    }
	}
      hNBJetsLoose_CRtwo ->Fill(nLoose);
      hNBJetsMedium_CRtwo->Fill(nMedium);


      index = -1;
      for (auto jet: jetData.getSelectedJets()) 
	{
	  index++;
	  // std::cout << "index = " << index << std::endl;
	  if (index > 6) break;
	  
	  if (index == 0)
	    {
	      hInverted_Jet1Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet1Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet1Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 1)
	    {
	      hInverted_Jet2Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet2Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet2Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    } 
	  
	  if (index == 2)
	    {
	      hInverted_Jet3Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet3Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet3Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 3)
	    {
	      hInverted_Jet4Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet4Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet4Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 4)
	    {
	      hInverted_Jet5Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet5Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet5Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 5)
	    {
	      hInverted_Jet6Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet6Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet6Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	  
	  if (index == 6)
	    {
	      hInverted_Jet7Pt_AfterCRSelections->Fill(isGenuineB, jet.pt() );
	      hInverted_Jet7Eta_AfterCRSelections->Fill(isGenuineB, jet.eta() );
	      hInverted_Jet7Bdisc_AfterCRSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	    }
	}
      
      hInverted_MET_AfterCRSelections ->Fill(isGenuineB, METData.getMET().R());
      hInverted_HT_AfterCRSelections ->Fill(isGenuineB, jetData.HT());
      hInverted_MVAmax1_AfterCRSelections ->Fill(isGenuineB, topData.getMVAmax1());
      hInverted_MVAmax2_AfterCRSelections ->Fill(isGenuineB, topData.getMVAmax2());
      hInverted_LdgTetrajetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
      hInverted_LdgTetrajetM_AfterCRSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
      hInverted_TetrajetBJetPt_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
      hInverted_TetrajetBJetEta_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
      hInverted_TetrajetBJetBdisc_AfterCRSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
      hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dEta);
      hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dPhi);
      hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections->Fill(isGenuineB, dR);
      hInverted_LdgTrijetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
      hInverted_LdgTrijetMass_AfterCRSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
      hInverted_LdgTrijetBJetBdisc_AfterCRSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
      hInverted_SubLdgTrijetPt_AfterCRSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
      hInverted_SubLdgTrijetMass_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
      hInverted_SubLdgTrijetBJetBdisc_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
      hInverted_LdgDijetPt_AfterCRSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
      hInverted_LdgDijetM_AfterCRSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
      hInverted_SubLdgDijetPt_AfterCRSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
      hInverted_SubLdgDijetM_AfterCRSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );
      
      // Splitted Histos
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetPt_CRtwo, isGenuineB, topData.getLdgTrijet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetMass_CRtwo, isGenuineB, topData.getLdgTrijet().M() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetBJetBdisc_CRtwo, isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetPt_CRtwo, isGenuineB, topData.getTetrajetBJet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetEta_CRtwo, isGenuineB, topData.getTetrajetBJet().eta() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetBdisc_CRtwo, isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetPt_CRtwo, isGenuineB, topData.getLdgTetrajet().pt() );
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetMass_CRtwo, isGenuineB, topData.getLdgTetrajet().M());
      
      return;
    }

  if (0) std::cout << "=== Inverted: Verification Region (VR)" << std::endl;
  cInvertedSelected.increment();

  //================================================================================================
  // Fill final plots (VR)
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, (int) isGenuineB);

  // Fill plots (VR)
  hInverted_Njets_AfterAllSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hInverted_NBjets_AfterAllSelections->Fill(isGenuineB, invBjetData.getSelectedBJets().size()); //invBjetData.getSelectedBJets().size()); 
  
  index   = -1;
  unsigned int nLoose = 0;
  unsigned int nMedium = 0;
  // For-loop: All b-jets
  for (auto bjet: invBjetData.getSelectedBJets())
    {
      index++;

      // Declare variables
      double pt    = bjet.pt();
      double eta   = bjet.eta();
      double bdisc = bjet.bjetDiscriminator();
      bool bLoose  = (bjet.bjetDiscriminator() > fInvertedBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Loose"));
      bool bMedium = (bjet.bjetDiscriminator() > fInvertedBJetSelection.getDiscriminatorWP(cfg_BjetDiscr, "Medium"));
      if (bLoose)
	{
	  if (bMedium)
	    {
	      nMedium++;
	      hBJetsPtMedium_VR->Fill(pt);
	      hBJetsEtaMedium_VR->Fill(eta);
	      hBJetsBdiscMedium_VR->Fill(bdisc);
	    }
	  else
	    {
	      nLoose++;
	      hBJetsPtLoose_VR->Fill(pt);
	      hBJetsEtaLoose_VR->Fill(eta);
	      hBJetsBdiscLoose_VR->Fill(bdisc);
	    }
	}

      if (index == 0)
	{
	  hInverted_Bjet1Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hInverted_Bjet1Eta_AfterAllSelections->Fill(isGenuineB, eta);
	  hInverted_Bjet1Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc);
	}

      if (index == 1)
	{
	  hInverted_Bjet2Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hInverted_Bjet2Eta_AfterAllSelections->Fill(isGenuineB, eta);
	  hInverted_Bjet2Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc);
	} 

      if (index == 2)
	{
	  hInverted_Bjet3Pt_AfterAllSelections->Fill(isGenuineB, pt);
	  hInverted_Bjet3Eta_AfterAllSelections->Fill(isGenuineB, eta);
	  hInverted_Bjet3Bdisc_AfterAllSelections->Fill(isGenuineB, bdisc);
	}
    }
  hNBJetsLoose_VR ->Fill(nLoose);
  hNBJetsMedium_VR->Fill(nMedium);


  index = -1;
  for (auto jet: jetData.getSelectedJets()) 
    {
      index++;
      // std::cout << "index = " << index << std::endl;
      if (index > 6) break;

      if (index == 0)
	{
	  hInverted_Jet1Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet1Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet1Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Jet2Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet2Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet2Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Jet3Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet3Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet3Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hInverted_Jet4Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet4Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet4Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hInverted_Jet5Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet5Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet5Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hInverted_Jet6Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet6Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet6Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hInverted_Jet7Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet7Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet7Bdisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hInverted_MET_AfterAllSelections ->Fill(isGenuineB, METData.getMET().R());
  hInverted_HT_AfterAllSelections ->Fill(isGenuineB, jetData.HT());
  hInverted_MVAmax1_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hInverted_MVAmax2_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hInverted_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hInverted_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hInverted_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hInverted_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hInverted_TetrajetBJetBdisc_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hInverted_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hInverted_LdgTrijetMass_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hInverted_LdgTrijetBJetBdisc_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  hInverted_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hInverted_SubLdgTrijetMass_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hInverted_SubLdgTrijetBJetBdisc_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijetBJet().bjetDiscriminator() );
  hInverted_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hInverted_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hInverted_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hInverted_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Splitted histos
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetPt_VR, isGenuineB, topData.getLdgTrijet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetMass_VR, isGenuineB, topData.getLdgTrijet().M() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTrijetBJetBdisc_VR, isGenuineB, topData.getLdgTrijetBJet().bjetDiscriminator() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetPt_VR, isGenuineB, topData.getTetrajetBJet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetEta_VR, isGenuineB, topData.getTetrajetBJet().eta() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hTetrajetBJetBdisc_VR, isGenuineB, topData.getTetrajetBJet().bjetDiscriminator() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetPt_VR, isGenuineB, topData.getLdgTetrajet().pt() );
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hLdgTetrajetMass_VR, isGenuineB, topData.getLdgTetrajet().M());

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}
