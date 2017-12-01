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
  // Input parameters
  const DirectionalCut<double> cfg_PrelimTopMVACut;
  const DirectionalCut<int> cfg_NumberOfBJets;
  const DirectionalCut<int> cfg_NumberOfInvertedBJets;
  const std::string cfg_InvertedBJetsDiscriminator;
  const std::string cfg_InvertedBJetsDiscriminatorWP;
  const DirectionalCut<double> cfg_InvertedBJetsDiscrMax;
  const std::string cfg_InvertedBJetsSortType;
  const std::string cfg_BaselineBJetsDiscriminator;
  const std::string cfg_BaselineBJetsDiscriminatorWP;

  // Common plots
  CommonPlots fCommonPlots;
  // CommonPlots fNormalizationSystematicsSignalRegion;  // todo
  // CommonPlots fNormalizationSystematicsControlRegion; // todo

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  // Baseline selection      
  Count cBaselineBTaggingCounter;
  Count cBaselineBTaggingSFCounter;
  METSelection fBaselineMETSelection;
  TopologySelection fBaselineTopologySelection;
  TopSelectionBDT fBaselineTopSelection;
  Count cBaselineSelected;
  // Inverted selection
  Count cInvertedBTaggingCounter;
  Count cInvertedBTaggingSFCounter;
  METSelection fInvertedMETSelection;
  TopologySelection fInvertedTopologySelection;
  TopSelectionBDT fInvertedTopSelection;
  Count cInvertedSelected;

  void DoInvertedAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const std::vector<Jet> invertedBJets, const int nVertices);
  void DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  const std::vector<Jet> GetInvertedBJets(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  bool IsGenuineBEvent(const std::vector<Jet>& bJets);

  // Sanity checks
  WrappedTH1 *hBaseline_IsGenuineB; 
  WrappedTH1 *hInverted_IsGenuineB; 

  // Normalisation Triplets
  WrappedTH1Triplet *hBaseline_LdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetMass_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetMass_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetMass_AfterAllSelections;
  
  // Triplets for Failed (aka inverted) Bjets 
  WrappedTH1Triplet *hInverted_FailedBJet1BDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1PdgId_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1PartonFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1HadronFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Ancestry_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2BDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2PdgId_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2PartonFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2HadronFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Ancestry_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3BDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3PdgId_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3PartonFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3HadronFlavour_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Ancestry_AfterStandardSelections;
  //
  WrappedTH1Triplet *hInverted_FailedBJet1BDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1PdgId_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1PartonFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1HadronFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet1Ancestry_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2BDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2PdgId_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2PartonFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2HadronFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet2Ancestry_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3BDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Pt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Eta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3PdgId_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3PartonFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3HadronFlavour_AfterAllSelections;
  WrappedTH1Triplet *hInverted_FailedBJet3Ancestry_AfterAllSelections;

  // FakeB Triplets (Baseline)
  WrappedTH1Triplet *hBaseline_NBjets_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet1BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet2BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Bjet3BtagDisc_AfterStandardSelections;
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
  WrappedTH1Triplet *hBaseline_Jet1BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet2BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet3BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet4BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet5BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet6BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_Jet7BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_MVAmax1_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_MVAmax2_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetM_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetEta_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetM_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetM_AfterStandardSelections;
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
  WrappedTH1Triplet *hBaseline_Bjet1BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet2BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Bjet3BtagDisc_AfterAllSelections;
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
  WrappedTH1Triplet *hBaseline_Jet1BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet2BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet3BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet4BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet5BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet6BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_Jet7BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_MVAmax1_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_MVAmax2_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_SubLdgDijetM_AfterAllSelections;

  // FakeB Triplets (Inverted)
  WrappedTH1Triplet *hInverted_NBjets_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3Pt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3Eta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet1BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet2BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Bjet3BtagDisc_AfterStandardSelections;
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
  WrappedTH1Triplet *hInverted_Jet1BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet2BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet3BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet4BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet5BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet6BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_Jet7BtagDisc_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_MVAmax1_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_MVAmax2_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetM_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetEta_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetM_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetPt_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetM_AfterStandardSelections;
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
  WrappedTH1Triplet *hInverted_Bjet1BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet2BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Bjet3BtagDisc_AfterAllSelections;
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
  WrappedTH1Triplet *hInverted_Jet1BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet2BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet3BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet4BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet5BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet6BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_Jet7BtagDisc_AfterAllSelections;
  WrappedTH1Triplet *hInverted_MVAmax1_AfterAllSelections;
  WrappedTH1Triplet *hInverted_MVAmax2_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_SubLdgDijetM_AfterAllSelections;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(FakeBMeasurement);

FakeBMeasurement::FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PrelimTopMVACut(config, "FakeBMeasurement.prelimTopMVACut"),
    cfg_NumberOfBJets(config, "FakeBMeasurement.numberOfBJetsCut"),
    cfg_NumberOfInvertedBJets(config, "FakeBMeasurement.numberOfInvertedBJetsCut"),
    cfg_InvertedBJetsDiscriminator(config.getParameter<std::string>("FakeBMeasurement.invertedBJetsDiscr")),
    cfg_InvertedBJetsDiscriminatorWP(config.getParameter<std::string>("FakeBMeasurement.invertedBJetsWorkingPoint")),
    cfg_InvertedBJetsDiscrMax(config, "FakeBMeasurement.invertedBJetsDiscrMaxCut"),
    cfg_InvertedBJetsSortType(config.getParameter<std::string>("FakeBMeasurement.invertedBJetsSortType")),
    cfg_BaselineBJetsDiscriminator(config.getParameter<std::string>("BJetSelection.bjetDiscr")),
    cfg_BaselineBJetsDiscriminatorWP(config.getParameter<std::string>("BJetSelection.bjetDiscrWorkingPoint")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kFakeBMeasurement, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("Passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    // Baseline selection
    cBaselineBTaggingCounter(fEventCounter.addCounter("Baseline: passed b-jet selection")),
    cBaselineBTaggingSFCounter(fEventCounter.addCounter("Baseline: b tag SF")),
    fBaselineMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    cBaselineSelected(fEventCounter.addCounter("Baseline: selected events")),
    // Inverted selection
    cInvertedBTaggingCounter(fEventCounter.addCounter("Inverted: passed b-jet selection")),
    cInvertedBTaggingSFCounter(fEventCounter.addCounter("Inverted: b tag SF")),
    fInvertedMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    cInvertedSelected(fEventCounter.addCounter("Inverted: selected events"))
{ }


FakeBMeasurement::~FakeBMeasurement() {
  // fCommonPlots.getHistoSplitter().deleteHistograms(hNormalizationBaselineTauAfterStdSelections);
  // fCommonPlots.getHistoSplitter().deleteHistograms(hMtBaselineTauAfterStdSelections);

  delete hBaseline_IsGenuineB;
  delete hInverted_IsGenuineB;

  // Normalization Triplets
  delete hBaseline_LdgTrijetMass_AfterStandardSelections;
  delete hBaseline_LdgTrijetMass_AfterAllSelections;
  delete hInverted_LdgTrijetMass_AfterStandardSelections;
  delete hInverted_LdgTrijetMass_AfterAllSelections;

  // Triplets for Failed (aka inverted) Bjets 
  delete hInverted_FailedBJet1BDisc_AfterStandardSelections;
  delete hInverted_FailedBJet1Pt_AfterStandardSelections;
  delete hInverted_FailedBJet1Eta_AfterStandardSelections;
  delete hInverted_FailedBJet1PdgId_AfterStandardSelections;
  delete hInverted_FailedBJet1PartonFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet1HadronFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet1Ancestry_AfterStandardSelections;
  delete hInverted_FailedBJet2BDisc_AfterStandardSelections;
  delete hInverted_FailedBJet2Pt_AfterStandardSelections;
  delete hInverted_FailedBJet2Eta_AfterStandardSelections;
  delete hInverted_FailedBJet2PdgId_AfterStandardSelections;
  delete hInverted_FailedBJet2PartonFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet2HadronFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet2Ancestry_AfterStandardSelections;
  delete hInverted_FailedBJet3BDisc_AfterStandardSelections;
  delete hInverted_FailedBJet3Pt_AfterStandardSelections;
  delete hInverted_FailedBJet3Eta_AfterStandardSelections;
  delete hInverted_FailedBJet3PdgId_AfterStandardSelections;
  delete hInverted_FailedBJet3PartonFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet3HadronFlavour_AfterStandardSelections;
  delete hInverted_FailedBJet3Ancestry_AfterStandardSelections;
  delete hInverted_FailedBJet1BDisc_AfterAllSelections;
  delete hInverted_FailedBJet1Pt_AfterAllSelections;
  delete hInverted_FailedBJet1Eta_AfterAllSelections;
  delete hInverted_FailedBJet1PdgId_AfterAllSelections;
  delete hInverted_FailedBJet1PartonFlavour_AfterAllSelections;
  delete hInverted_FailedBJet1HadronFlavour_AfterAllSelections;
  delete hInverted_FailedBJet1Ancestry_AfterAllSelections;
  delete hInverted_FailedBJet2BDisc_AfterAllSelections;
  delete hInverted_FailedBJet2Pt_AfterAllSelections;
  delete hInverted_FailedBJet2Eta_AfterAllSelections;
  delete hInverted_FailedBJet2PdgId_AfterAllSelections;
  delete hInverted_FailedBJet2PartonFlavour_AfterAllSelections;
  delete hInverted_FailedBJet2HadronFlavour_AfterAllSelections;
  delete hInverted_FailedBJet2Ancestry_AfterAllSelections;
  delete hInverted_FailedBJet3BDisc_AfterAllSelections;
  delete hInverted_FailedBJet3Pt_AfterAllSelections;
  delete hInverted_FailedBJet3Eta_AfterAllSelections;
  delete hInverted_FailedBJet3PdgId_AfterAllSelections;
  delete hInverted_FailedBJet3PartonFlavour_AfterAllSelections;
  delete hInverted_FailedBJet3HadronFlavour_AfterAllSelections;
  delete hInverted_FailedBJet3Ancestry_AfterAllSelections;

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
  delete hBaseline_Bjet1BtagDisc_AfterStandardSelections;
  delete hBaseline_Bjet2BtagDisc_AfterStandardSelections;
  delete hBaseline_Bjet3BtagDisc_AfterStandardSelections;
  // hBaseline_BjetsBtagDisc_AfterStandardSelections.clear();
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
  delete hBaseline_Jet1BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet2BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet3BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet4BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet5BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet6BtagDisc_AfterStandardSelections;
  delete hBaseline_Jet7BtagDisc_AfterStandardSelections;
  // hBaseline_JetsBtagDisc_AfterStandardSelections.clear();
  delete hBaseline_MVAmax1_AfterStandardSelections;
  delete hBaseline_MVAmax2_AfterStandardSelections;
  delete hBaseline_LdgTetrajetPt_AfterStandardSelections;
  delete hBaseline_LdgTetrajetM_AfterStandardSelections;
  delete hBaseline_TetrajetBJetPt_AfterStandardSelections;
  delete hBaseline_TetrajetBJetEta_AfterStandardSelections;
  delete hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hBaseline_LdgTrijetPt_AfterStandardSelections;
  delete hBaseline_LdgTrijetM_AfterStandardSelections;
  delete hBaseline_SubLdgTrijetPt_AfterStandardSelections;
  delete hBaseline_SubLdgTrijetM_AfterStandardSelections;
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
  delete hBaseline_Bjet1BtagDisc_AfterAllSelections;
  delete hBaseline_Bjet2BtagDisc_AfterAllSelections;
  delete hBaseline_Bjet3BtagDisc_AfterAllSelections;
  //  hBaseline_BjetsBtagDisc_AfterAllSelections.clear();
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
  delete hBaseline_Jet1BtagDisc_AfterAllSelections;
  delete hBaseline_Jet2BtagDisc_AfterAllSelections;
  delete hBaseline_Jet3BtagDisc_AfterAllSelections;
  delete hBaseline_Jet4BtagDisc_AfterAllSelections;
  delete hBaseline_Jet5BtagDisc_AfterAllSelections;
  delete hBaseline_Jet6BtagDisc_AfterAllSelections;
  delete hBaseline_Jet7BtagDisc_AfterAllSelections;
  //  hBaseline_JetsBtagDisc_AfterAllSelections.clear();

  delete hBaseline_MVAmax1_AfterAllSelections;
  delete hBaseline_MVAmax2_AfterAllSelections;
  delete hBaseline_LdgTetrajetPt_AfterAllSelections;
  delete hBaseline_LdgTetrajetM_AfterAllSelections;
  delete hBaseline_TetrajetBJetPt_AfterAllSelections;
  delete hBaseline_TetrajetBJetEta_AfterAllSelections;
  delete hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_LdgTrijetPt_AfterAllSelections;
  delete hBaseline_LdgTrijetM_AfterAllSelections;
  delete hBaseline_SubLdgTrijetPt_AfterAllSelections;
  delete hBaseline_SubLdgTrijetM_AfterAllSelections;
  delete hBaseline_LdgDijetPt_AfterAllSelections;
  delete hBaseline_LdgDijetM_AfterAllSelections;
  delete hBaseline_SubLdgDijetPt_AfterAllSelections;
  delete hBaseline_SubLdgDijetM_AfterAllSelections;

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
  delete hInverted_Bjet1BtagDisc_AfterStandardSelections;
  delete hInverted_Bjet2BtagDisc_AfterStandardSelections;
  delete hInverted_Bjet3BtagDisc_AfterStandardSelections;
  //  hInverted_JetsBtagDisc_AfterStandardSelections.clear();
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
  delete hInverted_Jet1BtagDisc_AfterStandardSelections;
  delete hInverted_Jet2BtagDisc_AfterStandardSelections;
  delete hInverted_Jet3BtagDisc_AfterStandardSelections;
  delete hInverted_Jet4BtagDisc_AfterStandardSelections;
  delete hInverted_Jet5BtagDisc_AfterStandardSelections;
  delete hInverted_Jet6BtagDisc_AfterStandardSelections;
  delete hInverted_Jet7BtagDisc_AfterStandardSelections;

  //  hInverted_JetsBtagDisc_AfterStandardSelections.clear();
  delete hInverted_MVAmax1_AfterStandardSelections;
  delete hInverted_MVAmax2_AfterStandardSelections;
  delete hInverted_LdgTetrajetPt_AfterStandardSelections;
  delete hInverted_LdgTetrajetM_AfterStandardSelections;
  delete hInverted_TetrajetBJetPt_AfterStandardSelections;
  delete hInverted_TetrajetBJetEta_AfterStandardSelections;
  delete hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections;
  delete hInverted_LdgTrijetPt_AfterStandardSelections;
  delete hInverted_LdgTrijetM_AfterStandardSelections;
  delete hInverted_SubLdgTrijetPt_AfterStandardSelections;
  delete hInverted_SubLdgTrijetM_AfterStandardSelections;
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
  delete hInverted_Bjet1BtagDisc_AfterAllSelections;
  delete hInverted_Bjet2BtagDisc_AfterAllSelections;
  delete hInverted_Bjet3BtagDisc_AfterAllSelections;
  //  hInverted_BjetsBtagDisc_AfterAllSelections.clear();
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
  delete hInverted_Jet1BtagDisc_AfterAllSelections;
  delete hInverted_Jet2BtagDisc_AfterAllSelections;
  delete hInverted_Jet3BtagDisc_AfterAllSelections;
  delete hInverted_Jet4BtagDisc_AfterAllSelections;
  delete hInverted_Jet5BtagDisc_AfterAllSelections;
  delete hInverted_Jet6BtagDisc_AfterAllSelections;
  delete hInverted_Jet7BtagDisc_AfterAllSelections;
  //  hInverted_JetsBtagDisc_AfterAllSelections.clear();

  delete hInverted_MVAmax1_AfterAllSelections;
  delete hInverted_MVAmax2_AfterAllSelections;
  delete hInverted_LdgTetrajetPt_AfterAllSelections;
  delete hInverted_LdgTetrajetM_AfterAllSelections;
  delete hInverted_TetrajetBJetPt_AfterAllSelections;
  delete hInverted_TetrajetBJetEta_AfterAllSelections;
  delete hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_LdgTrijetPt_AfterAllSelections;
  delete hInverted_LdgTrijetM_AfterAllSelections;
  delete hInverted_SubLdgTrijetPt_AfterAllSelections;
  delete hInverted_SubLdgTrijetM_AfterAllSelections;
  delete hInverted_LdgDijetPt_AfterAllSelections;
  delete hInverted_LdgDijetM_AfterAllSelections;
  delete hInverted_SubLdgDijetPt_AfterAllSelections;
  delete hInverted_SubLdgDijetM_AfterAllSelections;

}

void FakeBMeasurement::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  // Baseline selection
  fBaselineMETSelection.bookHistograms(dir);
  fBaselineTopologySelection.bookHistograms(dir);
  fBaselineTopSelection.bookHistograms(dir);
  // Inverted selection
  fInvertedMETSelection.bookHistograms(dir);
  fInvertedTopologySelection.bookHistograms(dir);
  fInvertedTopSelection.bookHistograms(dir);
  
  // ====== Normalization histograms
  // HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();

  // Obtain binning
  const int nNBins        = fCommonPlots.getNjetsBinSettings().bins();
  const float fNMin       = fCommonPlots.getNjetsBinSettings().min();
  const float fNMax       = fCommonPlots.getNjetsBinSettings().max();

  const int nBtagBins     = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBtagMin    = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBtagMax    = fCommonPlots.getBJetDiscBinSettings().max();

  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = fCommonPlots.getPtBinSettings().min();
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

  // Create directories for normalization
  std::string myInclusiveLabel  = "ForFakeBNormalization";
  std::string myFakeLabel       = myInclusiveLabel+"EWKFakeB";
  std::string myGenuineLabel    = myInclusiveLabel+"EWKGenuineB";
  TDirectory* myNormDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myNormEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myNormGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeBDir, myNormGenuineBDir};

  hBaseline_LdgTrijetMass_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs, 
				      "Baseline_LdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgTrijetMass_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs, 
				      "Baseline_LdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgTrijetMass_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs, 
				      "Inverted_LdgTrijetMass_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgTrijetMass_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs, 
				      "Inverted_LdgTrijetMass_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  // Purity histograms [(Data-EWK)/Data]
  myInclusiveLabel = "FailedBJet";
  myFakeLabel      = myInclusiveLabel + "FakeB";
  myGenuineLabel   = myInclusiveLabel + "GenuineB";

  // Create directories
  TDirectory* myFailedDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myPurityEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myPurityGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFailedDirs = {myFailedDir, myPurityEWKFakeBDir, myPurityGenuineBDir};

  // Create histograms
  hInverted_FailedBJet1BDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1BDisc_AfterStandardSelections",
				      "Inverted_FailedBJet1BDisc_AfterStandardSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1Pt_AfterStandardSelections",
				      "Inverted_FailedBJet1Pt_AfterStandardSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1Eta_AfterStandardSelections",
				      "Inverted_FailedBJet1Eta_AfterStandardSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet1PdgId_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1PdgId_AfterStandardSelections",
				      "Inverted_FailedBJet1PdgId_AfterStandardSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1PartonFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1PartonFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet1PartonFlavour_AfterStandardSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1HadronFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1HadronFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet1HadronFlavour_AfterStandardSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1Ancestry_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1Ancestry_AfterStandardSelections",
				      "Inverted_FailedBJet1Ancestry_AfterStandardSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)
  
  hInverted_FailedBJet2BDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2BDisc_AfterStandardSelections",
				      "Inverted_FailedBJet2BDisc_AfterStandardSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2Pt_AfterStandardSelections",
				      "Inverted_FailedBJet2Pt_AfterStandardSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2Eta_AfterStandardSelections",
				      "Inverted_FailedBJet2Eta_AfterStandardSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet2PdgId_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2PdgId_AfterStandardSelections",
				      "Inverted_FailedBJet2PdgId_AfterStandardSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2PartonFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2PartonFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet2PartonFlavour_AfterStandardSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2HadronFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2HadronFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet2HadronFlavour_AfterStandardSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2Ancestry_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2Ancestry_AfterStandardSelections",
				      "Inverted_FailedBJet2Ancestry_AfterStandardSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)

  hInverted_FailedBJet3BDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3BDisc_AfterStandardSelections",
				      "Inverted_FailedBJet3BDisc_AfterStandardSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3Pt_AfterStandardSelections",
				      "Inverted_FailedBJet3Pt_AfterStandardSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3Eta_AfterStandardSelections",
				      "Inverted_FailedBJet3Eta_AfterStandardSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet3PdgId_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3PdgId_AfterStandardSelections",
				      "Inverted_FailedBJet3PdgId_AfterStandardSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3PartonFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3PartonFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet3PartonFlavour_AfterStandardSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3HadronFlavour_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3HadronFlavour_AfterStandardSelections",
				      "Inverted_FailedBJet3HadronFlavour_AfterStandardSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3Ancestry_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3Ancestry_AfterStandardSelections",
				      "Inverted_FailedBJet3Ancestry_AfterStandardSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)


  // Create histograms (AllSelections) 
  hInverted_FailedBJet1BDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1BDisc_AfterAllSelections",
				      "Inverted_FailedBJet1BDisc_AfterAllSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1Pt_AfterAllSelections",
				      "Inverted_FailedBJet1Pt_AfterAllSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1Eta_AfterAllSelections",
				      "Inverted_FailedBJet1Eta_AfterAllSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet1PdgId_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1PdgId_AfterAllSelections",
				      "Inverted_FailedBJet1PdgId_AfterAllSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1PartonFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1PartonFlavour_AfterAllSelections",
				      "Inverted_FailedBJet1PartonFlavour_AfterAllSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1HadronFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet1HadronFlavour_AfterAllSelections",
				      "Inverted_FailedBJet1HadronFlavour_AfterAllSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet1Ancestry_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet1Ancestry_AfterAllSelections",
				      "Inverted_FailedBJet1Ancestry_AfterAllSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)
  
  hInverted_FailedBJet2BDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2BDisc_AfterAllSelections",
				      "Inverted_FailedBJet2BDisc_AfterAllSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2Pt_AfterAllSelections",
				      "Inverted_FailedBJet2Pt_AfterAllSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2Eta_AfterAllSelections",
				      "Inverted_FailedBJet2Eta_AfterAllSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet2PdgId_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2PdgId_AfterAllSelections",
				      "Inverted_FailedBJet2PdgId_AfterAllSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2PartonFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2PartonFlavour_AfterAllSelections",
				      "Inverted_FailedBJet2PartonFlavour_AfterAllSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2HadronFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet2HadronFlavour_AfterAllSelections",
				      "Inverted_FailedBJet2HadronFlavour_AfterAllSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet2Ancestry_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet2Ancestry_AfterAllSelections",
				      "Inverted_FailedBJet2Ancestry_AfterAllSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)

  hInverted_FailedBJet3BDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3BDisc_AfterAllSelections",
				      "Inverted_FailedBJet3BDisc_AfterAllSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3Pt_AfterAllSelections",
				      "Inverted_FailedBJet3Pt_AfterAllSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3Eta_AfterAllSelections",
				      "Inverted_FailedBJet3Eta_AfterAllSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJet3PdgId_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3PdgId_AfterAllSelections",
				      "Inverted_FailedBJet3PdgId_AfterAllSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3PartonFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3PartonFlavour_AfterAllSelections",
				      "Inverted_FailedBJet3PartonFlavour_AfterAllSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3HadronFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myFailedDirs,
				      "Inverted_FailedBJet3HadronFlavour_AfterAllSelections",
				      "Inverted_FailedBJet3HadronFlavour_AfterAllSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJet3Ancestry_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFailedDirs,
				      "Inverted_FailedBJet3Ancestry_AfterAllSelections",
				      "Inverted_FailedBJet3Ancestry_AfterAllSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)
  
  // Other histograms
  myInclusiveLabel = "ForFakeBMeasurement";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";
  // Create directories
  TDirectory* myFakeBDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeBEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myFakeBGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFakeBDirs = {myFakeBDir, myFakeBEWKFakeBDir, myFakeBGenuineBDir};


  hBaseline_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Baseline_IsGenuineB", ";is genuine-b event;Events / %0.f", 2, 0.0, 2.0);
  hInverted_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Inverted_IsGenuineB", ";is genuine-b event;Events / %0.f", 2, 0.0, 2.0);

  // Baseline selection (StandardSelections)
  hBaseline_NBjets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_NBjets_AfterStandardSelections", ";b-jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);

  hBaseline_Bjet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Bjet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Bjet1BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet2BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet3BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_Njets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Njets_AfterStandardSelections", ";jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);
  hBaseline_Jet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet4Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet5Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet6Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet7Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Jet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet4Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet5Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet6Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet7Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Jet1BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet2BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet3BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet4BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet5BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet6BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet7BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_MVAmax1_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax1_AfterStandardSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);
  hBaseline_MVAmax2_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax2_AfterStandardSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);

  hBaseline_LdgTetrajetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_LdgTetrajetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetMass_AfterStandardSelections", ";m_{jjbb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TetrajetBJetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TetrajetBJetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TetrajetBJetEta_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetEta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
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
				      "Baseline_LdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgTrijetM_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetM_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_SubLdgTrijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgTrijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetM_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgDijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_SubLdgDijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Baseline selection (AllSelections)
  hBaseline_NBjets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_NBjets_AfterAllSelections", ";b-jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);

  hBaseline_Bjet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Bjet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Bjet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Bjet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Bjet1BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet1BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet2BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet2BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Bjet3BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Bjet3BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_Njets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Njets_AfterAllSelections", ";jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);
  hBaseline_Jet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet4Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet5Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet6Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hBaseline_Jet7Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hBaseline_Jet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet4Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet5Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet6Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hBaseline_Jet7Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hBaseline_Jet1BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet1BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet2BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet2BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet3BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet3BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet4BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet4BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet5BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet5BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet6BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet6BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hBaseline_Jet7BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_Jet7BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hBaseline_MVAmax1_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax1_AfterAllSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);
  hBaseline_MVAmax2_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_MVAmax2_AfterAllSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);

  hBaseline_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TetrajetBJetEta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
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
				      "Baseline_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection (StandardSelections)
  hInverted_NBjets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_NBjets_AfterStandardSelections", ";b-jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);

  hInverted_Bjet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Bjet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Bjet1BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet2BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet3BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_Njets_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Njets_AfterStandardSelections", ";jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);
  hInverted_Jet1Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet2Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet3Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet4Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet5Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet6Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet7Pt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Pt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Jet1Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet2Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet3Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet4Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet5Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet6Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet7Eta_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Eta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Jet1BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet2BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet3BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet4BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet5BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet6BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet7BtagDisc_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7BtagDisc_AfterStandardSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_MVAmax1_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax1_AfterStandardSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);
  hInverted_MVAmax2_AfterStandardSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax2_AfterStandardSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);

  hInverted_LdgTetrajetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_LdgTetrajetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetMass_AfterStandardSelections", ";m_{jjjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TetrajetBJetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TetrajetBJetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TetrajetBJetEta_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetEta_AfterStandardSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
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
				      "Inverted_LdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgTrijetM_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetM_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_SubLdgTrijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgTrijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetM_AfterStandardSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgDijetPt_AfterStandardSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_SubLdgDijetPt_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetPt_AfterStandardSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgDijetM_AfterStandardSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetM_AfterStandardSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection (AllSelections)
  hInverted_NBjets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_NBjets_AfterAllSelections", ";b-jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);

  hInverted_Bjet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Bjet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Bjet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Bjet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Bjet1BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet1BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet2BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet2BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Bjet3BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Bjet3BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_Njets_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Njets_AfterAllSelections", ";jet multiplicity;Events / %.0f", nNBins, fNMin, fNMax);
  hInverted_Jet1Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet2Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet3Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet4Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet5Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet6Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);
  hInverted_Jet7Pt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Pt_AfterAllSelections", ";p_{T} (GeV/c);Events / %.0f", nPtBins, fPtMin, fPtMax);

  hInverted_Jet1Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet2Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet3Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet4Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet5Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet6Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  hInverted_Jet7Eta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7Eta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);

  hInverted_Jet1BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet1BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet2BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet2BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet3BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet3BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet4BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet4BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet5BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet5BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet6BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet6BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);
  hInverted_Jet7BtagDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_Jet7BtagDisc_AfterAllSelections", ";b tag discriminator;Events / %.2f", nBtagBins, fBtagMin, fBtagMax);

  hInverted_MVAmax1_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax1_AfterAllSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);
  hInverted_MVAmax2_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_MVAmax2_AfterAllSelections", ";#BDT discriminant;Events / %.2f", 40, -1.0, +1.0);

  hInverted_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgTetrajetMass_AfterAllSelections", ";m_{jjjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TetrajetBJetEta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
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
				      "Inverted_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_LdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  return;
}


void FakeBMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void FakeBMeasurement::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

  if (0) std::cout << "\nentry = " << entry << std::endl;

  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;

  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
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
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  
  //================================================================================================  
  // 8) BJet Selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  // Enable histogram filling and counter with silent analyze
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  // Disable histogram filling and counter with silent analyze
  // const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);


  // Baseline Selection
  if (bjetData.passedSelection())
    {
      DoBaselineAnalysis(jetData, bjetData, nVertices);
    }
  else // Inverted Selection
    {
 
      // CSVv2-Medium (Selected)
      bool passSelected = cfg_NumberOfBJets.passedCut(bjetData.getNumberOfSelectedBJets());
      if (!passSelected) return;

      // CSVv2-Loose (Inverted)
      const std::vector<Jet> invertedBJets = GetInvertedBJets(jetData, bjetData);
      bool passInverted = cfg_NumberOfInvertedBJets.passedCut(invertedBJets.size());
      if (!passInverted) return;

      // Do the inverted analysis
      DoInvertedAnalysis(jetData, bjetData, invertedBJets, nVertices);
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


const std::vector<Jet> FakeBMeasurement::GetInvertedBJets(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData)
{
  
  if (0) std::cout << "=== FakeBMeasurement::GetInvertedBJets()" << std::endl;
  
  // Apply requirement on selected b-jets (CSVv2-Medium)
  std::vector<Jet> invertedBJets;
  
  // Apply requirement on inverted b-jets (CSVv2-Loose)
  float invertedBJetDiscrMin = fBJetSelection.getDiscriminatorWP(cfg_InvertedBJetsDiscriminator, cfg_InvertedBJetsDiscriminatorWP);
  // float baselineBJetDiscr = fBJetSelection.getDiscriminatorWP(cfg_BaselineBJetsDiscriminator, cfg_BaselineBJetsDiscriminatorWP);
  
  // Get the failed b-jets (pass pT and eta cuts, failed bDiscriminator cut)
  std::vector<Jet> failedBJets;
  if (cfg_InvertedBJetsSortType.compare("Random") == 0 ) failedBJets = bjetData.getFailedBJetCandsShuffled();
  else if (cfg_InvertedBJetsSortType.compare("AscendingPt") == 0 ) failedBJets = bjetData.getFailedBJetCandsAscendingPt();
  else if (cfg_InvertedBJetsSortType.compare("DescendingPt") == 0 ) failedBJets = bjetData.getFailedBJetCandsDescendingPt();
  else if (cfg_InvertedBJetsSortType.compare("AscendingBDiscriminator") == 0 ) failedBJets = bjetData.getFailedBJetCandsAscendingDiscr();
  else if (cfg_InvertedBJetsSortType.compare("DescendingBDiscriminator") == 0 ) failedBJets = bjetData.getFailedBJetCandsDescendingDiscr();
  else
    {
      throw hplus::Exception("logic") << "Uknown jet sort type \"" << cfg_InvertedBJetsSortType << "\" passed to TopSelection class. "
				      << "Please select one of the following:\n\t\"Random\", \"AscendingPt\", \"DescendingPt\", \"AscendingBDiscriminator\", \"DescendingBDiscriminator\".";
    }
  
  // For-loop: All failed b-jets 
  for(const Jet& jet: failedBJets)
    {
      
      // Apply discriminator WP cuts (min and max)
      bool passBjetDiscrMin = (jet.bjetDiscriminator() > invertedBJetDiscrMin);
      bool passBjetDiscrMax = cfg_InvertedBJetsDiscrMax.passedCut(jet.bjetDiscriminator());
      
      // Skip jets with a b-discrininator below min allowed value
      if (!passBjetDiscrMin) continue;
      
      // Skip events if a jet has a b-discrininator above max allowed value
      if (!passBjetDiscrMax) break;
      
      // Save jets satisfying inverted b-jet criteria
      invertedBJets.push_back(jet);
      
      // Sanity check
      if (0) std::cout << "\tjet.bjetDiscriminator() = " << jet.bjetDiscriminator() << " (nInvertedBJets = " << invertedBJets.size() << ")" << std::endl;
      
    }
  
   return invertedBJets;
 }
 
void FakeBMeasurement::DoBaselineAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){
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
  const METSelection::Data METData = fBaselineMETSelection.analyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology
  //================================================================================================
  if (0) std::cout << "=== Baseline: Topology selection" << std::endl;
  const TopologySelection::Data topologyData = fBaselineTopologySelection.analyze(fEvent, jetData);

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  bool passPrelimMVACut = cfg_PrelimTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passPrelimMVACut) return;

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB  
  bool isGenuineB = IsGenuineBEvent(bjetData.getSelectedBJets());
  hBaseline_IsGenuineB->Fill(isGenuineB);
  if (0) std::cout << "=== FakeBMeasurement::DoBaselineAnalysis()\n\tisGenuineB = " << isGenuineB << std::endl;
  
  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Baseline: Standard Selections" << std::endl;
  // NB: CtrlPlotsAfterStandardSelections should only be called for Inverted!
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, bjetData.isGenuineB());

  // Fill Triplets  (Baseline)
  hBaseline_LdgTrijetMass_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().M());
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
	  hBaseline_Bjet1BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Bjet2Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet2Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet2BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Bjet3Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet3Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet3BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
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
	  hBaseline_Jet1BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Jet2Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet2Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet2BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Jet3Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet3Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet3BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hBaseline_Jet4Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet4Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet4BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hBaseline_Jet5Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet5Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet5BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hBaseline_Jet6Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet6Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet6BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hBaseline_Jet7Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet7Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet7BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hBaseline_MVAmax1_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hBaseline_MVAmax2_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax2());
  
  hBaseline_LdgTetrajetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hBaseline_LdgTetrajetM_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hBaseline_TetrajetBJetPt_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hBaseline_TetrajetBJetEta_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  double dEta = std::abs( topData.getTetrajetBJet().p4().eta() - topData.getLdgTrijetBJet().p4().eta() );
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4() ) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dEta);
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dPhi);
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dR);
  hBaseline_LdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hBaseline_LdgTrijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hBaseline_SubLdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hBaseline_SubLdgTrijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hBaseline_LdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hBaseline_LdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hBaseline_SubLdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hBaseline_SubLdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );


  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topologyData.passedSelection()) return;
  if (!topData.passedSelection()) return;

  if (0) std::cout << "=== Baseline: All Selections" << std::endl;
  cBaselineSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  hBaseline_LdgTrijetMass_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().M());

  // Fill Triplets  (Baseline)
  hBaseline_Njets_AfterAllSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hBaseline_NBjets_AfterAllSelections->Fill(isGenuineB, bjetData.getSelectedBJets().size());

  index = -1;
  // For-loop: All selected bjets
  for (auto bjet: bjetData.getSelectedBJets()) 
    {
      index++;
      if (index > 2) break;

      if (index == 0)
	{
	  hBaseline_Bjet1Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet1Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet1BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Bjet2Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet2Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet2BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 2)
	{
	  hBaseline_Bjet3Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hBaseline_Bjet3Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hBaseline_Bjet3BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

    }

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
	  hBaseline_Jet1BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hBaseline_Jet2Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet2Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet2BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hBaseline_Jet3Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet3Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet3BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hBaseline_Jet4Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet4Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet4BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hBaseline_Jet5Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet5Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet5BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hBaseline_Jet6Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet6Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet6BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hBaseline_Jet7Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hBaseline_Jet7Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hBaseline_Jet7BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hBaseline_MVAmax1_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hBaseline_MVAmax2_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hBaseline_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hBaseline_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hBaseline_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hBaseline_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hBaseline_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hBaseline_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hBaseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hBaseline_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hBaseline_LdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hBaseline_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hBaseline_SubLdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hBaseline_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hBaseline_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hBaseline_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hBaseline_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

void FakeBMeasurement::DoInvertedAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
					  const std::vector<Jet> invertedBJets,
					  const int nVertices){
  // Increment counter
  cInvertedBTaggingCounter.increment();

  //================================================================================================  
  // The b-jets (selected + inverted)
  //================================================================================================  
  const std::vector<Jet> selectedBJets = bjetData.getSelectedBJets();
  std::vector<Jet> myBJets;
  
  // Append the selected b-jets (CSVc2-M)
  myBJets.insert(myBJets.end(), selectedBJets.begin(), selectedBJets.end());

  // Append the inverted b-jets (CSVc2-L)
  myBJets.insert(myBJets.end(), invertedBJets.begin(), invertedBJets.end());

  // Sort all b-jets by descending pt value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(myBJets.begin(), myBJets.end(), [](const Jet& a, const Jet& b){return a.pt() > b.pt();});

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cInvertedBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.analyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology
  //================================================================================================
  if (0) std::cout << "=== Inverted: Topology selection" << std::endl;
  const TopologySelection::Data topologyData = fInvertedTopologySelection.analyze(fEvent, jetData);

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fInvertedTopSelection.analyzeWithoutBJets(fEvent, jetData.getSelectedJets(), myBJets, true);
  bool passPrelimMVACut = cfg_PrelimTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passPrelimMVACut) return;

  
  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  bool isGenuineB = IsGenuineBEvent(myBJets);
  hInverted_IsGenuineB->Fill(isGenuineB);
  if (0) std::cout << "=== FakeBMeasurement::DoInvertedAnalysis()\n\tisGenuineB = " << isGenuineB << std::endl;

  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Inverted: Standard Selections" << std::endl;
  fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, isGenuineB);

  // Fill Triplets  (Inverted)
  hInverted_LdgTrijetMass_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().M());
  hInverted_Njets_AfterStandardSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hInverted_NBjets_AfterStandardSelections->Fill(isGenuineB, myBJets.size());

  int index = -1;
  // For-loop: All inverted b-jets
  for (auto bjet: invertedBJets)
    {
      index++;
      
      // Only consider the first 3 b-jets
      if (index > 2) break;

      // NOTE: Definition change of boolean used in filling (now jet-by-jet, not event)
      bool isNotFakeB = (abs(bjet.hadronFlavour()) == 5);

      // Construct ancestry bit (Z, W, top, H+, Other)
      int ancestryBit = ( pow(2, 0)*bjet.originatesFromZ() +
			  pow(2, 1)*bjet.originatesFromW() +
			  pow(2, 2)*bjet.originatesFromTop() +
			  pow(2, 3)*bjet.originatesFromChargedHiggs() +
			  pow(2, 4)*bjet.originatesFromUnknown() );
      
      // Triplets (Inverted)
      if (index == 0)
	{
      	  hInverted_FailedBJet1BDisc_AfterStandardSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet1Pt_AfterStandardSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet1Eta_AfterStandardSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet1PdgId_AfterStandardSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet1PartonFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet1HadronFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet1Ancestry_AfterStandardSelections->Fill(isNotFakeB, ancestryBit);
	}

      // Use case: >= 2 inverted b-jets
      if (index == 1)
	{
	  hInverted_FailedBJet2BDisc_AfterStandardSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet2Pt_AfterStandardSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet2Eta_AfterStandardSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet2PdgId_AfterStandardSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet2PartonFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet2HadronFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet2Ancestry_AfterStandardSelections->Fill(isNotFakeB, ancestryBit);
	}

      // Use case: >= 3 inverted b-jets
      if (index == 2)
	{
	  hInverted_FailedBJet3BDisc_AfterStandardSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet3Pt_AfterStandardSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet3Eta_AfterStandardSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet3PdgId_AfterStandardSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet3PartonFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet3HadronFlavour_AfterStandardSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet3Ancestry_AfterStandardSelections->Fill(isNotFakeB, ancestryBit);
	}

    }

  index = -1;
  // For-loop: All BJets (Real or Inverted) used in top fit
  for (auto bjet: myBJets)
    {
      // std::cout << "bjet.bjetDiscriminator() = " << bjet.bjetDiscriminator() << std::endl;
      index++;
      if (index > 2) break;
      
      // NOTE: What is the point of using the "isGenuineB" here? Inclusive = FakeB (approx.)
      if (index == 0)
	{
	  hInverted_Bjet1Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet1Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet1BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Bjet2Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet2Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet2BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Bjet3Pt_AfterStandardSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet3Eta_AfterStandardSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet3BtagDisc_AfterStandardSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
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
	  hInverted_Jet1BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Jet2Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet2Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet2BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Jet3Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet3Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet3BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hInverted_Jet4Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet4Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet4BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hInverted_Jet5Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet5Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet5BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hInverted_Jet6Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet6Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet6BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hInverted_Jet7Pt_AfterStandardSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet7Eta_AfterStandardSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet7BtagDisc_AfterStandardSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hInverted_MVAmax1_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hInverted_MVAmax2_AfterStandardSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hInverted_LdgTetrajetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hInverted_LdgTetrajetM_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hInverted_TetrajetBJetPt_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hInverted_TetrajetBJetEta_AfterStandardSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  double dEta = std::abs( topData.getTetrajetBJet().eta() - topData.getLdgTrijetBJet().eta());
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dEta);
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dPhi);
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections->Fill(isGenuineB, dR);
  hInverted_LdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hInverted_LdgTrijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hInverted_SubLdgTrijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hInverted_SubLdgTrijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hInverted_LdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hInverted_LdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hInverted_SubLdgDijetPt_AfterStandardSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hInverted_SubLdgDijetM_AfterStandardSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topologyData.passedSelection()) return;
  if (!topData.passedSelection()) return;

  if (0) std::cout << "=== Inverted: All Selections" << std::endl;
  cInvertedSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, 1);

  index = -1;
  // For-loop: Only failed BJets used as bjets in top fit
     for (auto bjet: invertedBJets)
    {
      index++;
      
      // Only consider the first 3 b-jets
      if (index > 2) break;

      // NOTE: Definition change of boolean used in filling (now jet-by-jet, not event)
      bool isNotFakeB = (abs(bjet.pdgId()) == 5);

      // Construct ancestry bit (Z, W, top, H+, Other)
      int ancestryBit = ( pow(2, 0)*bjet.originatesFromZ() +
			  pow(2, 1)*bjet.originatesFromW() +
			  pow(2, 2)*bjet.originatesFromTop() +
			  pow(2, 3)*bjet.originatesFromChargedHiggs() +
			  pow(2, 4)*bjet.originatesFromUnknown() );

      // Triplets (Inverted)
      if (index == 0)
	{
	  hInverted_FailedBJet1BDisc_AfterAllSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet1Pt_AfterAllSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet1Eta_AfterAllSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet1PdgId_AfterAllSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet1PartonFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet1HadronFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet1Ancestry_AfterAllSelections->Fill(isNotFakeB, ancestryBit);
	}

      // Use case: >= 2 inverted b-jets
      if (index == 1)
	{
	  hInverted_FailedBJet2BDisc_AfterAllSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet2Pt_AfterAllSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet2Eta_AfterAllSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet2PdgId_AfterAllSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet2PartonFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet2HadronFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet2Ancestry_AfterAllSelections->Fill(isNotFakeB, ancestryBit);
	}

      // Use case: >= 3 inverted b-jets
      if (index == 2)
	{

	  hInverted_FailedBJet3BDisc_AfterAllSelections->Fill(isNotFakeB, bjet.bjetDiscriminator());
	  hInverted_FailedBJet3Pt_AfterAllSelections->Fill(isNotFakeB, bjet.pt());
	  hInverted_FailedBJet3Eta_AfterAllSelections->Fill(isNotFakeB, bjet.eta());
	  hInverted_FailedBJet3PdgId_AfterAllSelections->Fill(isNotFakeB, bjet.pdgId());
	  hInverted_FailedBJet3PartonFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.partonFlavour());
	  hInverted_FailedBJet3HadronFlavour_AfterAllSelections->Fill(isNotFakeB, bjet.hadronFlavour());
	  hInverted_FailedBJet3Ancestry_AfterAllSelections->Fill(isNotFakeB, ancestryBit);
	}

    }

  // Fill Triplets (Inverted)
  hInverted_LdgTrijetMass_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().M());
  hInverted_Njets_AfterAllSelections->Fill(isGenuineB, jetData.getSelectedJets().size());
  hInverted_NBjets_AfterAllSelections->Fill(isGenuineB, myBJets.size()); //bjetData.getSelectedBJets().size()); 
  
  index = -1;
  // For-loop: All BJets (bjets and failed bjets) sorted by pT
  for (auto bjet: myBJets)
    {
      index++;
      if (index > 2) break;

      if (index == 0)
	{
	  hInverted_Bjet1Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet1Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet1BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Bjet2Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet2Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet2BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Bjet3Pt_AfterAllSelections->Fill(isGenuineB, bjet.pt() );
	  hInverted_Bjet3Eta_AfterAllSelections->Fill(isGenuineB, bjet.eta() );
	  hInverted_Bjet3BtagDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator() );
	}
    }

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
	  hInverted_Jet1BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 1)
	{
	  hInverted_Jet2Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet2Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet2BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	} 

      if (index == 2)
	{
	  hInverted_Jet3Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet3Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet3BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 3)
	{
	  hInverted_Jet4Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet4Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet4BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 4)
	{
	  hInverted_Jet5Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet5Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet5BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 5)
	{
	  hInverted_Jet6Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet6Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet6BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}

      if (index == 6)
	{
	  hInverted_Jet7Pt_AfterAllSelections->Fill(isGenuineB, jet.pt() );
	  hInverted_Jet7Eta_AfterAllSelections->Fill(isGenuineB, jet.eta() );
	  hInverted_Jet7BtagDisc_AfterAllSelections->Fill(isGenuineB, jet.bjetDiscriminator() );
	}
    }

  hInverted_MVAmax1_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax1());
  hInverted_MVAmax2_AfterAllSelections ->Fill(isGenuineB, topData.getMVAmax2());
  hInverted_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hInverted_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hInverted_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hInverted_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  hInverted_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hInverted_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hInverted_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hInverted_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hInverted_LdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hInverted_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hInverted_SubLdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hInverted_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hInverted_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hInverted_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hInverted_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

bool FakeBMeasurement::IsGenuineBEvent(const std::vector<Jet>& bjets)
{ 
  if (!fEvent.isMC()) return false;
  
  // GenuineB=All selected b-jets in the event are genuine (using pat::Jet hadronFlavour() from MC)
  // jet is considered a b-jet if hadronFlavour=5
  // jet is considered a c-jet if hadronFlavour=4
  // jet is considered a light-flavour or gluon jet if hadronFlavour=0

  unsigned int nFakes=0;

  // For-loop: Selected BJets
  for(const Jet& bjet: bjets)
    {
      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
      // bool isFakeB = (abs(bjet.pdgId()) != 5);

      // See: https://hypernews.cern.ch/HyperNews/CMS/get/btag/1482.html
      bool isFakeB = (abs(bjet.hadronFlavour()) != 5); // For data hadronFlavour = 0
      if (isFakeB) nFakes++;

    }
  
  return (nFakes==0);
}
