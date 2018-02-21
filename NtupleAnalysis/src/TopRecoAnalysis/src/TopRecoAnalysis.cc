// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "DataFormat/interface/AK8Jet.h"
#include "DataFormat/interface/AK8JetsSoftDrop.h"

#include "TDirectory.h"

struct SelectedTrijet{
  Jet Jet1;
  Jet Jet2;
  Jet BJet;
  double MVA;
  math::XYZTLorentzVector TrijetP4;
  math::XYZTLorentzVector DijetP4;
};

class TopRecoAnalysis: public BaseSelector {
public:
  explicit TopRecoAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TopRecoAnalysis() {}

  bool foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets);
  TrijetSelection SortInMVAvalue(TrijetSelection TopCand);
  bool HasMother(const Event& event, const genParticle &p, const int mom_pdgId);
  Jet getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet);
  std::vector<int> SortInPt(std::vector<int> Vector);

  //Vector sorting according to the pt. - Descending order                                                                                                                                                              
  std::vector<math::XYZTLorentzVector> SortInPt(std::vector<math::XYZTLorentzVector> Vector);

  //returns the last copy of a gen particle                                                                                                                                                                             
  genParticle findLastCopy(int index);
  //is Bjet                                                                                                                                                                                                             
  bool isBJet(const Jet& jet, const std::vector<Jet>& bjets);

  bool isMatchedJet(const Jet& jet, const std::vector<Jet>& jets);

  bool isWsubjet(const Jet& jet, const std::vector<Jet>& jets1, const std::vector<Jet>& jets2);

  ///Are same Jets                                                                                                                                                                                                      
  bool areSameJets(const Jet& jet1, const Jet& jet2);

  const genParticle GetLastCopy(const vector<genParticle> genParticles, const genParticle &p);
  vector<genParticle> GetGenParticles(const vector<genParticle> genParticles, const int pdgId);
  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet);


  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  // const DirectionalCut<float> cfg_PrelimTopFitChiSqr;
  const DirectionalCut<double> cfg_PrelimTopMVACut;

  // Common plots
  CommonPlots fCommonPlots;
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
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  //  TopologySelection fTopologySelection;
  TopSelectionBDT fTopSelection;
  Count cSelected;
    
  // Non-common histograms
  // WrappedTH1 *hAssociatedTop_Pt;
  // WrappedTH1 *hAssociatedTop_Eta;
  WrappedTH2 *hMatchedTrijet_BDT_vs_Pt;
  WrappedTH2 *hMatchedTrijetBDT_vs_UnmatchedTrijetBDT;
  WrappedTH2 *hMatchedTrijetPt_vs_UnmatchedTrijetPt;

  WrappedTH2 *hLdgTrijetBDT_vs_SubldgTrijetBDT;
  WrappedTH2 *hLdgTrijetPt_vs_SubldgTrijetPt;
  
  WrappedTH2 *hLdgTrijetBDT_vs_LdgTrijetPt;
  WrappedTH2 *hSubldgTrijetBDT_vs_SubldgTrijetPt;

  WrappedTH2 *hMVA1TrijetBDT_vs_MVA2TrijetBDT;
  WrappedTH2 *hMVA1TrijetPt_vs_MVA2TrijetPt;
  
  WrappedTH2 *hMVA1TrijetBDT_vs_MVA1TrijetPt;
  WrappedTH2 *hMVA2TrijetBDT_vs_MVA2TrijetPt;

  WrappedTH2 *hDR_LdgTrijet_TetrajetB_vs_DR_SubldgTrijet_TetrajetB;
  WrappedTH2 *hDR_MVA1Trijet_TetrajetB_vs_DR_MVA2Trijet_TetrajetB;
  
  WrappedTH2 *hLdgTrijetBDT_vs_MVA1TrijetBDT;
  WrappedTH2 *hLdgTrijetPt_vs_MVA1TrijetPt;

  WrappedTH2 *hMatchedTrijetBDT_vs_LdgTrijetBDT;
  WrappedTH2 *hMatchedTrijetPt_vs_LdgTrijetPt;
  WrappedTH2 *hMatchedTrijetBDT_vs_MVA1TrijetBDT;
  WrappedTH2 *hMatchedTrijetPt_vs_MVA1TrijetPt;

  WrappedTH2 *hLdgTrijet_Eta_vs_DeltaR_LdgTrijet_LdgTrijetBjet;
  WrappedTH2 *hLdgTrijet_Phi_vs_DeltaR_LdgTrijet_LdgTrijetBjet;
  WrappedTH2 *hMVA1Trijet_Eta_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet;
  WrappedTH2 *hMVA1Trijet_Phi_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet;

  WrappedTH2 *hMatched_Q1Q2_Pt_Vs_Matched_Q1Q2B_Pt;

  WrappedTH2 *hLdgTrijetPt_Vs_TetrajetPt;
  WrappedTH2 *hSubldgTrijetPt_Vs_TetrajetPt;
  WrappedTH2 *hLdgTrijetDijetPt_Vs_TetrajetPt;
  WrappedTH2 *hSubldgTrijetDijetPt_Vs_TetrajetPt;
  WrappedTH2Triplet *hLdgTrijetPt_Vs_TetrajetBjetPt;
  WrappedTH2Triplet *hSubldgTrijetPt_Vs_TetrajetBjetPt;
  WrappedTH2Triplet *hLdgTrijetDijetPt_Vs_TetrajetBjetPt;
  WrappedTH2Triplet *hSubldgTrijetDijetPt_Vs_TetrajetBjetPt;


  //  WrappedTH1 *h_HT;
  WrappedTH1 *hBoostedLdgTrijet_Pt400;
  WrappedTH1 *hBoostedSubldgTrijet_Pt400;
  WrappedTH1 *hBoostedTrijets_Pt400;

  WrappedTH1 *hDeltaR_LdgTrijet_LdgTrijetBjet;
  WrappedTH1 *hDeltaR_SubldgTrijet_SubldgTrijetBjet;
  WrappedTH1 *hLdgTrijet_Eta;
  WrappedTH1 *hLdgTrijet_Phi;
  WrappedTH1 *hSubldgTrijet_Eta;
  WrappedTH1 *hSubldgTrijet_Phi;

  WrappedTH1 *hDeltaR_MVA1Trijet_MVA1TrijetBjet;
  WrappedTH1 *hDeltaR_MVA2Trijet_MVA2TrijetBjet;
  WrappedTH1 *hMVA1Trijet_Eta;
  WrappedTH1 *hMVA1Trijet_Phi;
  WrappedTH1 *hMVA2Trijet_Eta;
  WrappedTH1 *hMVA2Trijet_Phi;

  WrappedTH1 *hCEvts_BoostedTop;
  WrappedTH1 *hCEvts_MergedTop;
  WrappedTH1Triplet *hCEvts_mergedDijet;
  WrappedTH1Triplet *hCEvts_mergedTrijet_untaggedW;
  WrappedTH1Triplet *hCEvts_mergedTrijet;
  WrappedTH1Triplet *hCEvts_mergedJB;
  WrappedTH1Triplet *hMatched_DeltaRDijet_mergedJB;

  WrappedTH1 *hMatched_TopQuark_Pt;
  WrappedTH1 *hMatched_Q1Q2_Pt;
  WrappedTH1 *hMatched_Q1Q2B_Pt;

  WrappedTH1 *hMatched_DijetDeltaR;
  WrappedTH1Triplet *hMatched_DeltaR_DijetBjet;
  WrappedTH1Triplet *hMatched_DijetMass;
  WrappedTH1Triplet *hMatched_DijetPt;

  WrappedTH1 *hHiggsTop_DijetDeltaR;
  WrappedTH1Triplet *hHiggsTop_DeltaR_DijetBjet;
  WrappedTH1Triplet *hHiggsTop_DijetMass;
  WrappedTH1Triplet *hHiggsTop_DijetPt;
  
  WrappedTH1 *hCEvts_LdgTrijet_DeltaPhiWeighted_within08;
  WrappedTH1 *hCEvts_SubldgTrijet_DeltaPhiWeighted_within08;
  WrappedTH1 *hCEvts_Trijets_DeltaPhiWeighted_within08;

  WrappedTH1 *hCEvts_LdgTrijet_DeltaEtaWeighted_within08;
  WrappedTH1 *hCEvts_SubldgTrijet_DeltaEtaWeighted_within08;
  WrappedTH1 *hCEvts_Trijets_DeltaEtaWeighted_within08;
  WrappedTH1 *hCEvts_closeJetToTetrajetBjet_isBTagged;
  WrappedTH1 *hCevts_FatJet_Pt450;

  WrappedTH1Triplet *hLdgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaY_Trijet_TetrajetBjet ;
  WrappedTH1Triplet *hSubldgTrijet_DeltaR_Trijet_TetrajetBjet; 
  WrappedTH1Triplet *hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet; 
  WrappedTH1Triplet *hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1Triplet *hSubldgTrijet_DeltaY_Trijet_TetrajetBjet  ;
  WrappedTH1Triplet *hDeltaR_BDTtrijets_TetrajetBjet ;

  WrappedTH1Triplet *hLdgTrijetJets_DeltaRmin;
  WrappedTH1Triplet *hSubldgTrijetJets_DeltaRmin;
  WrappedTH1Triplet *hLdgTrijetJets_DeltaRmax;
  WrappedTH1Triplet *hSubldgTrijetJets_DeltaRmax;

  WrappedTH2Triplet *hLdgTrijetJets_DeltaRmin_Vs_BDT;
  WrappedTH2Triplet *hLdgTrijetJets_DeltaRmin_Vs_Pt;
  WrappedTH2Triplet *hSubldgTrijetJets_DeltaRmin_Vs_BDT;
  WrappedTH2Triplet *hSubldgTrijetJets_DeltaRmin_Vs_Pt;
  WrappedTH2Triplet *hLdgTrijetJets_DeltaRmax_Vs_BDT;
  WrappedTH2Triplet *hLdgTrijetJets_DeltaRmax_Vs_Pt;
  WrappedTH2Triplet *hSubldgTrijetJets_DeltaRmax_Vs_BDT;
  WrappedTH2Triplet *hSubldgTrijetJets_DeltaRmax_Vs_Pt;

  //new
  WrappedTH2Triplet *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2Triplet *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2Triplet *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;


  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1p5;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2p5;

  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p1;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p2;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p3;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p4;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p5;

  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800;
  WrappedTH2Triplet *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800;
  WrappedTH2Triplet *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800;
  WrappedTH2Triplet *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800;

  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB;
  WrappedTH2Triplet *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB;
  WrappedTH2Triplet *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB;
  WrappedTH2Triplet *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB;


  WrappedTH2Triplet *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth;    
  WrappedTH2Triplet *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth;  
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth;  
  WrappedTH2Triplet *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth;    

  WrappedTH2Triplet *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800;    
  WrappedTH2Triplet *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800;  
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800;  
  WrappedTH2Triplet *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800;    


  WrappedTH1Triplet *hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet;
  
  WrappedTH1Triplet *hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet *hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet;

  WrappedTH1Triplet *hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth;
  
  WrappedTH1Triplet *hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet *hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth;

  WrappedTH1Triplet *hTetrajetMass;
  WrappedTH1Triplet *hTetrajetMass_M800;
  WrappedTH1Triplet *hTetrajetMass_LdgTopIsHTop;
  WrappedTH1Triplet *hTetrajetMass_SubldgTopIsHTop;
  WrappedTH1 *hTetrajetMass_deltaPhiCond;
  WrappedTH1Triplet *hTetrajetMass_isGenuineB;
  WrappedTH1Triplet *hTetrajetMass_closeJetToTetrajetBjet;
  WrappedTH1Triplet *hTetrajetPtDPhi;
  WrappedTH1Triplet *hTetrajetPtDPhi_M800;
  WrappedTH1Triplet *hTetrajetPtDPhi_LdgTopIsHTop;
  WrappedTH1Triplet *hTetrajetPtDPhi_isGenuineB;


  WrappedTH1Triplet *hTetrajetPtDR;
  WrappedTH1Triplet *hTetrajetPtDR_M800;
  WrappedTH1Triplet *hTetrajetPtDR_LdgTopIsHTop;
  WrappedTH1Triplet *hTetrajetPtDR_isGenuineB;


  WrappedTH2 *hDeltaRqqMin_Vs_DeltaRjjMin;

  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_M800;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_LdgTopIsHTop;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_trueBoth;
  WrappedTH2Triplet *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_isGenuine;

  WrappedTH1Triplet *hTetrajetBjetBDisc;
  WrappedTH1Triplet *hLdgTrijetBjet_PtRel;
  WrappedTH1Triplet *hLdgTrijetPt;
  WrappedTH1Triplet *hLdgTrijetDijetPt;
  WrappedTH1Triplet *hSubldgTrijetPt;
  WrappedTH1Triplet *hSubldgTrijetDijetPt;



  //===================
  // Fat jets Analysis
  //===================

  WrappedTH1Triplet *hFatTop_LdgTrijet_Pt;
  WrappedTH1Triplet *hFatW_LdgTrijet_Pt;
  WrappedTH1Triplet *hFatJB_LdgTrijet_Pt;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_Pt;
  WrappedTH1Triplet *hFatW_SubldgTrijet_Pt;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_Pt;

  WrappedTH1 *hLdgFatJetPt;
  WrappedTH1 *hLdgFatJet_tau21;
  WrappedTH1 *hLdgFatJet_tau32;
  WrappedTH1 *hLdgFatJetPt_beforeTopSelection;
  WrappedTH1 *hLdgFatJet_tau21_beforeTopSelection;
  WrappedTH1 *hLdgFatJet_tau32_beforeTopSelection;

  WrappedTH1 *hSubldgFatJetPt;
  WrappedTH1 *hSubldgFatJet_tau21;
  WrappedTH1 *hSubldgFatJet_tau32;
  WrappedTH1 *hSubldgFatJetPt_beforeTopSelection;
  WrappedTH1 *hSubldgFatJet_tau21_beforeTopSelection;
  WrappedTH1 *hSubldgFatJet_tau32_beforeTopSelection;

  WrappedTH1Triplet *hFatTop_LdgTrijet_tau21;
  WrappedTH1Triplet *hFatW_LdgTrijet_tau21;
  WrappedTH1Triplet *hFatJB_LdgTrijet_tau21;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_tau21;
  WrappedTH1Triplet *hFatW_SubldgTrijet_tau21;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_tau21;

  WrappedTH1Triplet *hFatTop_LdgTrijet_tau32;
  WrappedTH1Triplet *hFatW_LdgTrijet_tau32;
  WrappedTH1Triplet *hFatJB_LdgTrijet_tau32;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_tau32;
  WrappedTH1Triplet *hFatW_SubldgTrijet_tau32;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_tau32;

  WrappedTH1Triplet *hFatTop_LdgTrijet_Pt_ht900;
  WrappedTH1Triplet *hFatW_LdgTrijet_Pt_ht900;
  WrappedTH1Triplet *hFatJB_LdgTrijet_Pt_ht900;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_Pt_ht900;
  WrappedTH1Triplet *hFatW_SubldgTrijet_Pt_ht900;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_Pt_ht900;

  WrappedTH1 *hLdgFatJetPt_ht900;
  WrappedTH1 *hLdgFatJet_tau21_ht900;
  WrappedTH1 *hLdgFatJet_tau32_ht900;
  WrappedTH1 *hLdgFatJetPt_ht900_beforeTopSelection;
  WrappedTH1 *hLdgFatJet_tau21_ht900_beforeTopSelection;
  WrappedTH1 *hLdgFatJet_tau32_ht900_beforeTopSelection;

  WrappedTH1 *hSubldgFatJetPt_ht900;
  WrappedTH1 *hSubldgFatJet_tau21_ht900;
  WrappedTH1 *hSubldgFatJet_tau32_ht900;
  WrappedTH1 *hSubldgFatJetPt_ht900_beforeTopSelection;
  WrappedTH1 *hSubldgFatJet_tau21_ht900_beforeTopSelection;
  WrappedTH1 *hSubldgFatJet_tau32_ht900_beforeTopSelection;


  WrappedTH1Triplet *hFatTop_LdgTrijet_tau21_ht900;
  WrappedTH1Triplet *hFatW_LdgTrijet_tau21_ht900;
  WrappedTH1Triplet *hFatJB_LdgTrijet_tau21_ht900;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_tau21_ht900;
  WrappedTH1Triplet *hFatW_SubldgTrijet_tau21_ht900;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_tau21_ht900;

  WrappedTH1Triplet *hFatTop_LdgTrijet_tau32_ht900;
  WrappedTH1Triplet *hFatW_LdgTrijet_tau32_ht900;
  WrappedTH1Triplet *hFatJB_LdgTrijet_tau32_ht900;
  WrappedTH1Triplet *hFatTop_SubldgTrijet_tau32_ht900;
  WrappedTH1Triplet *hFatW_SubldgTrijet_tau32_ht900;
  WrappedTH1Triplet *hFatJB_SubldgTrijet_tau32_ht900;


  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_categories;
  WrappedTH1 *hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther;
  WrappedTH1 *hCEvts_HTmodif900_BeforeAfterTopSelection;
  WrappedTH1Triplet *hCevts_HTmodif900;
  WrappedTH1 *hCEvts_LdgTrijet_MergedResolved;

  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt200;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt250;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt300;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt350;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt400;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt450;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt500;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt550;
  WrappedTH1 *hCEvts_LdgTrijetMatchedToFatJet_FatJetPt600;

  //fraction of trijets matched to fat jets for different fatjet.pt values
  vector<WrappedTH1*> hCEvts_LdgTrijetMatchedToFatJet_Ptcuts;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TopRecoAnalysis);

TopRecoAnalysis::TopRecoAnalysis(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    // cfg_PrelimTopFitChiSqr(config, "FakeBMeasurement.prelimTopFitChiSqrCut"),
    // cfg_PrelimTopMVACut(config, "FakeBMeasurement.prelimTopMVACut"),
    cfg_PrelimTopMVACut(config, "FakeBMeasurement.minTopMVACut"),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    //    fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void TopRecoAnalysis::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  //  fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);

  const int nWMassBins    = fCommonPlots.getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots.getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots.getWMassBinSettings().max();

  // const int nInvMassBins    = fCommonPlots.getInvMassBinSettings().bins();
  // const float fInvMassMin   = fCommonPlots.getInvMassBinSettings().min();
  // const float fInvMassMax   = fCommonPlots.getInvMassBinSettings().max();

  const int nPtBins_modif       =     fCommonPlots.getPtBinSettings().bins();
  const double fPtMin_modif     = 2 * fCommonPlots.getPtBinSettings().min();
  const double fPtMax_modif     = 2*4 * fCommonPlots.getPtBinSettings().max()/5.;

  const int nPtBins       = 2*fCommonPlots.getPtBinSettings().bins();
  const double fPtMin     = 2 *fCommonPlots.getPtBinSettings().min();
  const double fPtMax     = 2* fCommonPlots.getPtBinSettings().max();


  const int nEtaBins       = fCommonPlots.getEtaBinSettings().bins();
  const double fEtaMin     = fCommonPlots.getEtaBinSettings().min();
  const double fEtaMax     = fCommonPlots.getEtaBinSettings().max();

  const int nPhiBins       = fCommonPlots.getPhiBinSettings().bins();
  const double fPhiMin     = fCommonPlots.getPhiBinSettings().min();
  const double fPhiMax     = fCommonPlots.getPhiBinSettings().max();
  
  const int nDRBins       = fCommonPlots.getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots.getDeltaRBinSettings().min();
  const double fDRMax     = 3/5.*fCommonPlots.getDeltaRBinSettings().max();
  
  const int nDPhiBins     = fCommonPlots.getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots.getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots.getDeltaPhiBinSettings().max();
  
  const int nDEtaBins     = fCommonPlots.getDeltaEtaBinSettings().bins();
  const double fDEtaMin   = fCommonPlots.getDeltaEtaBinSettings().min();
  const double fDEtaMax   = fCommonPlots.getDeltaEtaBinSettings().max();
  
  const int nBDTBins  =  40;
  const double nBDTMin = 0.75;
  const double nBDTMax = 1.05;

  const int  nBDiscBins   = fCommonPlots.getBJetDiscBinSettings().bins();
  //  const float fBDiscMin   = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBDiscMax   = fCommonPlots.getBJetDiscBinSettings().max();



  TDirectory* subdirTH1 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "Analysis_");

  std::string myInclusiveLabel  = "AnalysisTriplets";
  std::string myFakeLabel       = myInclusiveLabel+"False";
  std::string myGenuineLabel    = myInclusiveLabel+"True";
  TDirectory* myInclusiveDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myGenuineDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs = {myInclusiveDir, myFakeDir, myGenuineDir};

  
  std::string myInclusiveLabelTH2  = "TopAnalysisTH2";
  std::string myFakeLabelTH2       = myInclusiveLabelTH2+"False";
  std::string myGenuineLabelTH2    = myInclusiveLabelTH2+"True";
  TDirectory* myInclusiveDirTH2         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabelTH2);
  TDirectory* myFakeDirTH2 = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabelTH2);
  TDirectory* myGenuineDirTH2 = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabelTH2);
  std::vector<TDirectory*> myDirsTH2 = {myInclusiveDirTH2, myFakeDirTH2, myGenuineDirTH2};

  //Top Reconstruction Variables                                                                                                                                                       
  //  hTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TrijetPt", ";p_{T} (GeV/c)", 2*nBinsPt, minPt , 2*maxPt);
  //  h_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "HT"         , ";H_{T}"      , 60, 0.0, 2500.0);
  hBoostedLdgTrijet_Pt400       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "BoostedLdgTrijet", ";Trijet Counter", 2,0,2);
  hBoostedSubldgTrijet_Pt400    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "BoostedSubldgTrijet", ";Trijet Counter", 2,0,2);
  hBoostedTrijets_Pt400         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "BoostedTrijets", "Trijet Counter", 2,0,2);
  hCEvts_BoostedTop             = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_BoostedTop",   ";", 2, 0, 2);
  hCEvts_MergedTop              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_MergedTop",    ";", 2, 0, 2);

  hCEvts_mergedDijet            = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CEvts_mergedDijet",  ";", 3, 0, 3);
  hCEvts_mergedTrijet_untaggedW = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CEvts_mergedTrijet_untaggedW", ";", 3, 0, 3); 
  hCEvts_mergedTrijet           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CEvts_mergedTrijet", ";", 3, 0, 3);
  hCEvts_mergedJB               = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CEvts_mergedJB", ";", 2,0,2);
  hMatched_DeltaRDijet_mergedJB = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "Matched_DeltaRDijet_mergedJB", ";#Delta R(j_{1},j_{2})", nDRBins     , fDRMin     , 4.0);

  hDeltaR_LdgTrijet_LdgTrijetBjet       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "DeltaR_LdgTrijet_LdgTrijetBjet", ";#Delta R", nDRBins, fDRMin, fDRMax);
  hDeltaR_SubldgTrijet_SubldgTrijetBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "DeltaR_SubldgTrijet_SubldgTrijetBjet", ";#Delta R", nDRBins, fDRMin, fDRMax);
  hLdgTrijet_Eta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "LdgTrijet_Eta", "#eta", nEtaBins, fEtaMin, fEtaMax);
  hLdgTrijet_Phi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "LdgTrijet_Phi", "#phi", nPhiBins, fPhiMin, fPhiMax);
  hSubldgTrijet_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "SubldgTrijet_Eta", "#eta", nEtaBins, fEtaMin, fEtaMax);
  hSubldgTrijet_Phi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "SubldgTrijet_Phi", "#phi", nPhiBins, fPhiMin, fPhiMax);

  hDeltaR_MVA1Trijet_MVA1TrijetBjet  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "DeltaR_MVA1Trijet_MVA1TrijetBjet", ";#Delta R", nDRBins, fDRMin, fDRMax);
  hDeltaR_MVA2Trijet_MVA2TrijetBjet  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "DeltaR_MVA2Trijet_MVA2TrijetBjet", ";#Delta R", nDRBins, fDRMin, fDRMax);
  hMVA1Trijet_Eta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "MVA1Trijet_Eta", "#eta", nEtaBins, fEtaMin, fEtaMax);
  hMVA1Trijet_Phi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "MVA1Trijet_Phi", "#phi", nPhiBins, fPhiMin, fPhiMax);
  hMVA2Trijet_Eta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "MVA2Trijet_Eta", "#eta", nEtaBins, fEtaMin, fEtaMax);
  hMVA2Trijet_Phi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "MVA2Trijet_Phi", "#phi", nPhiBins, fPhiMin, fPhiMax);

  hMatched_TopQuark_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "TopQuarkPt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hMatched_Q1Q2_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "Matched_Q1Q2_Pt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hMatched_Q1Q2B_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "Matched_Q1Q2B_Pt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);


  hMatched_DijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "Matched_DijetDeltaR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);
  hMatched_DeltaR_DijetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "Matched_DeltaR_DijetBjet", ";#Delta R(j_{1}j_{2},b)", nDRBins     , fDRMin     , fDRMax);
  hMatched_DijetMass = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "Matched_DijetMass", ";M(GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hMatched_DijetPt = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "Matched_DijetPt", ";p_{T}(GeV/c)", nPtBins, fPtMin, fPtMax);
  
  hHiggsTop_DijetDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "HiggsTop_DijetDeltaR"  , ";#Delta R(j_{1},j_{2})"  , nDRBins     , fDRMin     , fDRMax);

  hHiggsTop_DeltaR_DijetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "HiggsTop_DeltaR_DijetBjet", ";#Delta R(j_{1}j_{2},b)", nDRBins     , fDRMin     , fDRMax);
  hHiggsTop_DijetMass = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "HiggsTop_DijetMass", ";M(GeV/c^{2})", nWMassBins  , fWMassMin  , fWMassMax);
  hHiggsTop_DijetPt = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "HiggsTop_DijetPt", ";p_{T}(GeV/c)", nPtBins, fPtMin, fPtMax);

  hCEvts_LdgTrijet_DeltaPhiWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_LdgTrijet_DeltaPhiWeighted_within08", ";", 2, 0, 2);
  hCEvts_SubldgTrijet_DeltaPhiWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_SubldgTrijet_DeltaPhiWeighted_within08", ";", 2, 0, 2);
  hCEvts_Trijets_DeltaPhiWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_Trijets_DeltaPhiWeighted_within08", ";", 2, 0, 2);

  hCEvts_LdgTrijet_DeltaEtaWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_LdgTrijet_DeltaEtaWeighted_within08", ";", 2, 0, 2);
  hCEvts_SubldgTrijet_DeltaEtaWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_SubldgTrijet_DeltaEtaWeighted_within08", ";", 2, 0, 2);
  hCEvts_Trijets_DeltaEtaWeighted_within08 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "CEvts_Trijets_DeltaEtaWeighted_within08", ";", 2, 0, 2);
  hCEvts_closeJetToTetrajetBjet_isBTagged = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_closeJetToTetrajetBjet_isBTagged", ";", 2, 0, 2);

  hCevts_FatJet_Pt450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdirTH1, "Cevts_FatJet_Pt450", ";", 2, 0, 2);
  TDirectory* subdirTH2 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "AnalysisTH2_");
  // Book non-common histograms
  // hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  // hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta", nBinsEta, minEta, maxEta);
  hMatchedTrijet_BDT_vs_Pt   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijet_BDT_vs_Pt", ";BDT discr;p_{T}", nBDTBins, nBDTMin, nBDTMax,  nPtBins_modif, fPtMin_modif, fPtMax_modif);
  hMatchedTrijetBDT_vs_UnmatchedTrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetBDT_vs_UnmatchedTrijetBDT", ";BDT discr_{Htop};BDT discr",
								       nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);
  
  hMatchedTrijetPt_vs_UnmatchedTrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetPt_vs_UnmatchedTrijetPt", ";p_{T,Htop}; p_{T}", 
								     nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hLdgTrijetBDT_vs_SubldgTrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetBDT_vs_SubldgTrijetBDT", ";BDT discr_{LdgTop};BDT discr_{SubldgTop}",
								nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);
  hLdgTrijetPt_vs_SubldgTrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetPt_vs_SubldgTrijetPt", ";p_{T,LdgTop};p_{T,SubldgTop}",
							      nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);
  hLdgTrijetBDT_vs_LdgTrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetBDT_vs_LdgTrijetPt", ";BDT discr;p_{T}", nBDTBins, nBDTMin, nBDTMax,  nPtBins_modif, fPtMin_modif, fPtMax_modif);
  hSubldgTrijetBDT_vs_SubldgTrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "SubldgTrijetBDT_vs_SubldgTrijetPt", ";BDT discr;p_{T}", 
								  nBDTBins, nBDTMin, nBDTMax,  nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hMVA1TrijetBDT_vs_MVA2TrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA1TrijetBDT_vs_MVA2TrijetBDT", ";BDT discr_{MVA1Top};BDT discr_{MVA2Top}",
								nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);
  hMVA1TrijetPt_vs_MVA2TrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA1TrijetPt_vs_MVA2TrijetPt", ";p_{T,MVA1Top};p_{T,MVA2Top}",
							      nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);
  hMVA1TrijetBDT_vs_MVA1TrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA1TrijetBDT_vs_MVA1TrijetPt", ";BDT discr;p_{T}", nBDTBins, nBDTMin, nBDTMax,  nPtBins_modif, fPtMin_modif, fPtMax_modif);
  hMVA2TrijetBDT_vs_MVA2TrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA2TrijetBDT_vs_MVA2TrijetPt", ";BDT discr;p_{T}", 
								  nBDTBins, nBDTMin, nBDTMax,  nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hDR_LdgTrijet_TetrajetB_vs_DR_SubldgTrijet_TetrajetB = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DR_LdgTrijet_TetrajetB_vs_DR_SubldgTrijet_TetrajetB",
										    ";#Delta R(LdgTop,Bjet_{free});#Delta R(SubldgTop,Bjet_{free})", 
										    nDRBins, fDRMin, fDRMax,  nDRBins, fDRMin, fDRMax);

  hDR_MVA1Trijet_TetrajetB_vs_DR_MVA2Trijet_TetrajetB = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "DR_MVA1Trijet_TetrajetB_vs_DR_MVA2Trijet_TetrajetB",
										    ";#Delta R(MVA1Top,Bjet_{free});#Delta R(MVA2,Bjet_{free})", 
										    nDRBins, fDRMin, fDRMax,  nDRBins, fDRMin, fDRMax);

  hLdgTrijetBDT_vs_MVA1TrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetBDT_vs_MVA1TrijetBDT", ";BDT discr_{LdgTop};BDT discr_{MVA1Top}",
							     nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);

  hLdgTrijetPt_vs_MVA1TrijetPt   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetPt_vs_MVA1TrijetPt", ";p_{T,LdgTop};p_{T,MVA1Top}",
							      nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hMatchedTrijetBDT_vs_LdgTrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetBDT_vs_LdgTrijetBDT", ";BDT discr_{matched};BDT discr_{LdgTop}",
								 nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);
  hMatchedTrijetPt_vs_LdgTrijetPt   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetPt_vs_LdgTrijetPt", ";p_{T,matched};p_{T,LdgTop}",
								 nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hMatchedTrijetBDT_vs_MVA1TrijetBDT = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetBDT_vs_MVA1TrijetBDT", ";BDT discr_{matched};BDT discr_{MVA1Top}",
								  nBDTBins, nBDTMin, nBDTMax,  nBDTBins, nBDTMin, nBDTMax);

  hMatchedTrijetPt_vs_MVA1TrijetPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MatchedTrijetPt_vs_MVA1TrijetPt", ";p_{T,matched};p_{T,MVA1Top}",
								nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif, fPtMin_modif, fPtMax_modif);

  hLdgTrijet_Eta_vs_DeltaR_LdgTrijet_LdgTrijetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijet_Eta_vs_DeltaR_LdgTrijet_LdgTrijetBjet", ";#eta;#Delta R",
										nEtaBins, fEtaMin, fEtaMax, nDRBins, fDRMin, fDRMax);
  hLdgTrijet_Phi_vs_DeltaR_LdgTrijet_LdgTrijetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijet_Phi_vs_DeltaR_LdgTrijet_LdgTrijetBjet", ";#phi;#Delta R",
										nPhiBins, fPhiMin, fPhiMax, nDRBins, fDRMin, fDRMax);
  hMVA1Trijet_Eta_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA1Trijet_Eta_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet",";#eta;#Delta R",
										   nEtaBins, fEtaMin, fEtaMax, nDRBins, fDRMin, fDRMax);

  hMVA1Trijet_Phi_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "MVA1Trijet_Phi_vs_DeltaR_MVA1Trijet_MVA1TrijetBjet",";#phi;#Delta R",
										   nPhiBins, fPhiMin, fPhiMax, nDRBins, fDRMin, fDRMax);
  hMatched_Q1Q2_Pt_Vs_Matched_Q1Q2B_Pt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "Matched_Q1Q2_Pt_Vs_Matched_Q1Q2B_Pt", ";p_{T,q1q2};p_{T,q1q2b}", nPtBins, fPtMin, fPtMax, nPtBins, fPtMin, fPtMax);



  hLdgTrijetPt_Vs_TetrajetPt             = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetPt_Vs_TetrajetPt",
								      ";p_{T,jjb} (GeV/c);p_{jjbb}(GeV/c)", nPtBins_modif, fPtMin_modif, fPtMax_modif, nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hSubldgTrijetPt_Vs_TetrajetPt          = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "SubldgTrijetPt_Vs_TetrajetPt",
								      ";p_{T,jjb}(GeV/c);p_{jjbb}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hLdgTrijetDijetPt_Vs_TetrajetPt        = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijetDijetPt_Vs_TetrajetPt",
								      ";p_{T,W}(GeV/c);p_{jjbb}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hSubldgTrijetDijetPt_Vs_TetrajetPt     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "SubldgTrijetDijetPt_Vs_TetrajetPt",
								      ";p_{T,W}(GeV/c);p_{jjbb}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hLdgTrijetPt_Vs_TetrajetBjetPt         = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetPt_Vs_TetrajetBjetPt",
                                                                             ";p_{T,jjb} (GeV/c);p_{T,b_{free}}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hSubldgTrijetPt_Vs_TetrajetBjetPt      = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetPt_Vs_TetrajetBjetPt",
                                                                             ";p_{T,jjb} (GeV/c);p_{T,b_{free}}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hLdgTrijetDijetPt_Vs_TetrajetBjetPt    = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetDijetPt_Vs_TetrajetBjetPt",
                                                                             ";p_{T,W} (GeV/c);p_{T,b_{free}}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hSubldgTrijetDijetPt_Vs_TetrajetBjetPt = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetDijetPt_Vs_TetrajetBjetPt",
                                                                             ";p_{T,W} (GeV/c);p_{T,b_{free}}(GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif,nPtBins_modif,fPtMin_modif,fPtMax_modif);


  //===================================================

  hLdgTrijet_DeltaR_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);

  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);

  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth"  , ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth"  , ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);


  hDeltaR_BDTtrijets_TetrajetBjet  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "DeltaR_BDTtrijets_TetrajetBjet"  , ";#Delta R"  , nDRBins     , fDRMin     , fDRMax/2.);
  // hTrijetJets_DeltaRmin            = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TrijetJets_DeltaRmin"            , ";#Delta R"  , nDRBins     , fDRMin     , fDRMax/2.);

  hLdgTrijetJets_DeltaRmin       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetJets_DeltaRmin"    , ";#Delta R"  , 60     , fDRMin     , 3.);
  hSubldgTrijetJets_DeltaRmin    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetJets_DeltaRmin"    , ";#Delta R"  , 60     , fDRMin     , 3.);
  hLdgTrijetJets_DeltaRmax       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetJets_DeltaRmax"    , ";#Delta R"  , 120     , fDRMin     , 6.);
  hSubldgTrijetJets_DeltaRmax    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetJets_DeltaRmax"    , ";#Delta R"  , 120     , fDRMin     , 6.);

  hLdgTrijetJets_DeltaRmin_Vs_BDT = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetJets_DeltaRmin_Vs_BDT", ";#Delta R;BDTG response", nDRBins, fDRMin, fDRMax/2.,  nBDTBins, nBDTMin, nBDTMax);
  hLdgTrijetJets_DeltaRmin_Vs_Pt  = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetJets_DeltaRmin_Vs_Pt", ";#Delta R;p_{T,jjb} (GeV/c)", nDRBins, fDRMin, fDRMax/2.,  nPtBins, fPtMin, fPtMax);
  hSubldgTrijetJets_DeltaRmin_Vs_BDT = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetJets_DeltaRmin_Vs_BDT", ";#Delta R;BDTG response", nDRBins, fDRMin, fDRMax/2.,  nBDTBins, nBDTMin, nBDTMax);
  hSubldgTrijetJets_DeltaRmin_Vs_Pt = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetJets_DeltaRmin_Vs_Pt", ";#Delta R;p_{T,jjb} (GeV/c)", nDRBins, fDRMin, fDRMax/2.,  nPtBins, fPtMin, fPtMax);

  hLdgTrijetJets_DeltaRmax_Vs_BDT = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetJets_DeltaRmax_Vs_BDT", ";#Delta R;BDTG response", nDRBins, fDRMin, fDRMax/2.,  nBDTBins, nBDTMin, nBDTMax);
  hLdgTrijetJets_DeltaRmax_Vs_Pt = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "LdgTrijetJets_DeltaRmax_Vs_Pt", ";#Delta R;p_{T,jjb} (GeV/c)", nDRBins, fDRMin, fDRMax/2.,  nPtBins, fPtMin, fPtMax);
  hSubldgTrijetJets_DeltaRmax_Vs_BDT = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetJets_DeltaRmax_Vs_BDT", ";#Delta R;BDTG response", nDRBins, fDRMin, fDRMax/2.,  nBDTBins, nBDTMin, nBDTMax);
  hSubldgTrijetJets_DeltaRmax_Vs_Pt = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "SubldgTrijetJets_DeltaRmax_Vs_Pt", ";#Delta R;p_{T,jjb} (GeV/c)", nDRBins, fDRMin, fDRMax/2.,  nPtBins, fPtMin, fPtMax);


  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet",
                                                                                             ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet",
                                                                                             ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet",
                                                                                             ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);


  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);

  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1p5 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1p5",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2p5 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2p5",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);

  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p1 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p1",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p2 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p2",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p3 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p3",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p4 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p4",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p5 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p5",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);



  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800",
                                                                                             ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800",
                                                                                             ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800",
													 ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
													 nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800",
                                                                                             ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);



  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB",
                                                                                             ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB",
                                                                                             ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB",
													 ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
													 nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB",
                                                                                             ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);


  
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800",
														  ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
														  nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800",
													     ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})",
													     nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800",
													     ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})",
													     nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2,  "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800",
													     ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})",
													     nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  
  

  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth",
                                                                                             ";#Delta R (Trijet_{Ldg}, b_{free}^{ldg});#Delta R (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth",
                                                                                             ";#Delta #eta (Trijet_{Ldg}, b_{free}^{ldg}) ;#Delta #eta (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDEtaBins, fDEtaMin, 6., nDEtaBins, fDEtaMin, 6.);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth",
                                                                                             ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});#Delta #phi (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDPhiBins , fDPhiMin , fDPhiMax, nDPhiBins , fDPhiMin , fDPhiMax);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2,  "DeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth",
                                                                                             ";#Delta Y (Trijet_{Ldg}, b_{free}^{ldg});#Delta Y (Trijet_{Sbldg}, b_{free}^{ldg})",
                                                                                             nDRBins     , fDRMin     , 6., nDRBins     , fDRMin     , 6.);

  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt", 
										     ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});p_{T,jjbb}", 
										     nDPhiBins , fDPhiMin , fDPhiMax, nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_M800 = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_M800", 
										     ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});p_{T,jjbb}", 
										     nDPhiBins , fDPhiMin , fDPhiMax, nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_LdgTopIsHTop = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_LdgTopIsHTop", 
											  ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});p_{T,jjbb}", 
											  nDPhiBins , fDPhiMin , fDPhiMax, nPtBins_modif,fPtMin_modif,fPtMax_modif);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_isGenuine = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirsTH2, "DeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_isGenuine", 
										     ";#Delta #phi (Trijet_{Ldg}, b_{free}^{ldg});p_{T,jjbb}", 
										     nDPhiBins , fDPhiMin , fDPhiMax, nPtBins_modif,fPtMin_modif,fPtMax_modif);


  hTetrajetMass                     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass", ";m_{jjbb} (GeV/c^{2})",                 250,  0, 2500);
  hTetrajetMass_M800                     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_M800", ";m_{jjbb} (GeV/c^{2})",       250,  0, 2500);
  hTetrajetMass_LdgTopIsHTop        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_LdgTopIsHTop", ";m_{jjbb} (GeV/c^{2})",    250,  0, 2500);
  hTetrajetMass_SubldgTopIsHTop     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_SubldgTopIsHTop", ";m_{jjbb} (GeV/c^{2})", 250,  0, 2500);
  hTetrajetMass_deltaPhiCond        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TetrajetMass_deltaPhiCond", ";m_{jjbb} (GeV/c^{2})",              250,  0, 2500);
  hTetrajetMass_isGenuineB          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_isGenuineB", ";m_{jjbb} (GeV/c^{2})",      250,  0, 2500);


  hTetrajetMass_closeJetToTetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_closeJetToTetrajetBjet", ";m_{jjbb} (GeV/c^{2})",      250,  0, 2500);


  hTetrajetPtDPhi                     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDPhi", ";p_{T,jjbb}#Delta#phi(top,b) (GeV/c)",      nPtBins, fPtMin, fPtMax*fDPhiMax);
  hTetrajetPtDPhi_M800                = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDPhi_M800", ";p_{T,jjbb}#Delta#phi(top,b) (GeV/c)",  nPtBins, fPtMin, fPtMax*fDPhiMax);
  hTetrajetPtDPhi_LdgTopIsHTop        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDPhi_LdgTopIsHTop", ";p_{T,jjbb}#Delta#phi(top,b) (GeV/c)",   nPtBins, fPtMin, fPtMax*fDPhiMax);
  hTetrajetPtDPhi_isGenuineB          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDPhi_isGenuineB", ";p_{T,jjbb}#Delta#phi(top,b) (GeV/c)",     nPtBins, fPtMin, fPtMax*fDPhiMax);


  hTetrajetPtDR                     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDR", ";m_{jjbb}#Delta#phi(top,b) (GeV/c^{2})",       nPtBins, fPtMin, fPtMax*6);
  hTetrajetPtDR_M800                = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDR_M800", ";m_{jjbb}#Delta#phi(top,b) (GeV/c^{2})",  nPtBins, fPtMin, fPtMax*6);
  hTetrajetPtDR_LdgTopIsHTop        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDR_LdgTopIsHTop", ";m_{jjbb}#Delta#phi(top,b) (GeV/c^{2})",    nPtBins, fPtMin, fPtMax*6);
  hTetrajetPtDR_isGenuineB          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPtDR_isGenuineB", ";m_{jjbb}#Delta#phi(top,b) (GeV/c^{2})",     nPtBins, fPtMin, fPtMax*6);


  hDeltaRqqMin_Vs_DeltaRjjMin         = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2,  "DeltaRqqMin_Vs_DeltaRjjMin", ";#Delta R_{min,qq};#Delta R_{min,jj}", 60, -1.0, 3.0, 60, -1.0, 3.0);

  hTetrajetBjetBDisc  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetBJetBDisc",";b-tag discriminator", nBDiscBins  , 0.8 , fBDiscMax);
  hLdgTrijetBjet_PtRel = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetBjet_PtRel", "p_{T,rel} (GeV/c)", nPtBins_modif,fPtMin_modif,fPtMax_modif/4);


  hLdgTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetPt", ";p_{T}", 100, 0, 1000);
  hLdgTrijetDijetPt      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetDijetPt", ";p_{T}",100, 0,1000);
  hSubldgTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetPt", ";p_{T}", 100, 0, 1000);
  hSubldgTrijetDijetPt      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetDijetPt", ";p_{T}",100, 0,1000);


  hFatTop_LdgTrijet_Pt      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatW_LdgTrijet_Pt        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatJB_LdgTrijet_Pt      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatTop_SubldgTrijet_Pt   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatW_SubldgTrijet_Pt     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatJB_SubldgTrijet_Pt   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_Pt", ";p_{T} (GeV/c)", 100, 0, 1000);

  hLdgFatJetPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJetPt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hLdgFatJet_tau21  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hLdgFatJet_tau32  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hLdgFatJetPt_beforeTopSelection      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJetPt_beforeTopSelection", ";p_{T} (GeV/c)", 100, 0, 1000);
  hLdgFatJet_tau21_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau21_beforeTopSelection", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hLdgFatJet_tau32_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau32_beforeTopSelection", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);


  hSubldgFatJetPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJetPt", ";p_{T} (GeV/c)", 100, 0, 1000);
  hSubldgFatJet_tau21  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hSubldgFatJet_tau32  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hSubldgFatJetPt_beforeTopSelection      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJetPt_beforeTopSelection", ";p_{T} (GeV/c)", 100, 0, 1000);
  hSubldgFatJet_tau21_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau21_beforeTopSelection", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hSubldgFatJet_tau32_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau32_beforeTopSelection", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);


  hFatTop_LdgTrijet_tau21      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatW_LdgTrijet_tau21        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatJB_LdgTrijet_tau21      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatTop_SubldgTrijet_tau21   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatW_SubldgTrijet_tau21     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatJB_SubldgTrijet_tau21   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_tau21", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);




  hFatTop_LdgTrijet_tau32      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatW_LdgTrijet_tau32        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatJB_LdgTrijet_tau32      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatTop_SubldgTrijet_tau32   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatW_SubldgTrijet_tau32     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatJB_SubldgTrijet_tau32   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_tau32", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);



  //===============

  hFatTop_LdgTrijet_Pt_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatW_LdgTrijet_Pt_ht900        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatJB_LdgTrijet_Pt_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatTop_SubldgTrijet_Pt_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatW_SubldgTrijet_Pt_ht900     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hFatJB_SubldgTrijet_Pt_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_Pt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);

  hLdgFatJetPt_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJetPt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hLdgFatJet_tau21_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hLdgFatJet_tau32_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hLdgFatJetPt_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJetPt_ht900_beforeTopSelection", ";p_{T} (GeV/c)", 100, 0, 1000);
  hLdgFatJet_tau21_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau21_ht900_beforeTopSelection", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hLdgFatJet_tau32_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgFatJet_tau32_ht900_beforeTopSelection", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);

  hSubldgFatJetPt_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJetPt_ht900", ";p_{T} (GeV/c)", 100, 0, 1000);
  hSubldgFatJet_tau21_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hSubldgFatJet_tau32_ht900  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hSubldgFatJetPt_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJetPt_ht900_beforeTopSelection", ";p_{T} (GeV/c)", 100, 0, 1000);
  hSubldgFatJet_tau21_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau21_ht900_beforeTopSelection", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hSubldgFatJet_tau32_ht900_beforeTopSelection  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgFatJet_tau32_ht900_beforeTopSelection", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);


  hFatTop_LdgTrijet_tau21_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatW_LdgTrijet_tau21_ht900        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatJB_LdgTrijet_tau21_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatTop_SubldgTrijet_tau21_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatW_SubldgTrijet_tau21_ht900     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);
  hFatJB_SubldgTrijet_tau21_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_tau21_ht900", ";#tau_{21}(#tau_{2}/#tau_{1})", 50, 0, 1.0);

  hFatTop_LdgTrijet_tau32_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_LdgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatW_LdgTrijet_tau32_ht900        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_LdgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatJB_LdgTrijet_tau32_ht900      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_LdgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatTop_SubldgTrijet_tau32_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatTop_SubldgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatW_SubldgTrijet_tau32_ht900     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatW_SubldgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);
  hFatJB_SubldgTrijet_tau32_ht900   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "FatJB_SubldgTrijet_tau32_ht900", ";#tau_{32}(#tau_{3}/#tau_{2})", 50, 0, 1.0);


  hCEvts_LdgTrijetMatchedToFatJet_categories = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_categories", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther", ";", 3, 0, 3);
  hCEvts_HTmodif900_BeforeAfterTopSelection = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_HTmodif900_BeforeAfterTopSelection", ";", 2, 0, 2);
  hCevts_HTmodif900 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "Cevts_HTmodif900", ";", 2, 0, 2);

  hCEvts_LdgTrijet_MergedResolved  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijet_MergedResolved", ";", 2, 0, 2);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt200 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt200", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt250 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt250", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt300 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt300", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt350 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt350", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt400 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt400", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt450 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt450", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt500 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt500", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt550 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt550", ";", 3, 0, 3);
  hCEvts_LdgTrijetMatchedToFatJet_FatJetPt600 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "CEvts_LdgTrijetMatchedToFatJet_FatJetPt600", ";", 3, 0, 3);

  // To ease manipulation put in vector                                                                                                                                                                                 
  //fraction of trijets matched to fat jets for different fatjet.pt values                                                                                                                                                           
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt200);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt250);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt300);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt350);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt400);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt450);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt500);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt550);
  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.push_back(hCEvts_LdgTrijetMatchedToFatJet_FatJetPt600);


  return;
}

bool TopRecoAnalysis::foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets){

  int SumTrijet1 = isBJet(trijet1Jet1, bjets) + isBJet(trijet1Jet2, bjets) + isBJet(trijet1BJet, bjets);
  int SumTrijet2 = isBJet(trijet2Jet1, bjets) + isBJet(trijet2Jet2, bjets) + isBJet(trijet2BJet, bjets);

  if ((size_t)(SumTrijet1 + SumTrijet2) != bjets.size()) return true;

  return false;
}


TrijetSelection TopRecoAnalysis::SortInMVAvalue(TrijetSelection TopCand){
  size_t size = TopCand.MVA.size();

  if (size < 1) return TopCand;

  for (size_t i=0; i<size-1; i++)
    {

      for  (size_t j=i+1; j<size; j++)
        {
          Jet Jet1_i = TopCand.Jet1.at(i);
          Jet Jet2_i = TopCand.Jet2.at(i);
          Jet BJet_i = TopCand.BJet.at(i);
          double mva_i = TopCand.MVA.at(i);
	  math::XYZTLorentzVector TrijetP4_i = TopCand.TrijetP4.at(i);
	  math::XYZTLorentzVector DijetP4_i = TopCand.DijetP4.at(i);

          Jet Jet1_j = TopCand.Jet1.at(j);
          Jet Jet2_j = TopCand.Jet2.at(j);
          Jet BJet_j = TopCand.BJet.at(j);
          double mva_j = TopCand.MVA.at(j);
	  math::XYZTLorentzVector TrijetP4_j = TopCand.TrijetP4.at(j);
	  math::XYZTLorentzVector DijetP4_j = TopCand.DijetP4.at(j);

          if (mva_i >= mva_j) continue;
          TopCand.Jet1.at(i) = Jet1_j;
          TopCand.Jet2.at(i) = Jet2_j;
          TopCand.BJet.at(i) = BJet_j;
          TopCand.MVA.at(i)  = mva_j;
          TopCand.TrijetP4.at(i) = TrijetP4_j;
          TopCand.DijetP4.at(i) = DijetP4_j;
          TopCand.Jet1.at(j) = Jet1_i;
          TopCand.Jet2.at(j) = Jet2_i;
          TopCand.BJet.at(j) = BJet_i;
          TopCand.MVA.at(j)  = mva_i;
          TopCand.TrijetP4.at(j) = TrijetP4_i;
          TopCand.DijetP4.at(j) = DijetP4_i;

        }

    }

  return TopCand;
}


bool TopRecoAnalysis::HasMother(const Event& event, const genParticle &p, const int mom_pdgId){
  //  Description:                                                                                                                                                                                                      
  //  Returns true if the particle has a mother with pdgId equal to mom_pdgId.                                                                                                                                          

  // Ensure the particle has a mother!                                                                                                                                                                                  
  if (p.mothers().size() < 1) return false;

  // For-loop: All mothers                                                                                                                                                                                              
  for (size_t iMom = 0; iMom < p.mothers().size(); iMom++)
    {
      int mom_index =  p.mothers().at(iMom);
      const genParticle m = event.genparticles().getGenParticles()[mom_index];
      int motherID = m.pdgId();
      int particleID = p.pdgId();
      if (std::abs(motherID) == mom_pdgId) return true;
      if (std::abs(motherID) == std::abs(particleID)) return HasMother(event, m, mom_pdgId);
      //      else continue;                                                                                                                                                                                            
    }

  return false;
}

/*                                                                                                                                                                                                                      
  Get all gen particles by pdgId                                                                                                                                                                                        
*/
vector<genParticle> TopRecoAnalysis::GetGenParticles(const vector<genParticle> genParticles, const int pdgId)
{
  std::vector<genParticle> particles;

  // For-loop: All genParticles                                                                                                                                                                                         
  for (auto& p: genParticles){

    // Find last copy of a given particle                                                                                                                                                                               
    if (!p.isLastCopy()) continue;

    // Consider only particles                                                                                                                                                                                          
    if (std::abs(p.pdgId()) != pdgId) continue;

    // Save this particle                                                                                                                                                                                               
    particles.push_back(p);
  }
  return particles;
}

/*                                                                                                                                                                                                                      
  Get the last copy of a particle.                                                                                                                                                                                      
*/
const genParticle TopRecoAnalysis::GetLastCopy(const vector<genParticle> genParticles, const genParticle &p){

  int gen_pdgId = p.pdgId();

  for (size_t i=0; i<p.daughters().size(); i++){

    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();

    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}

Jet TopRecoAnalysis::getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet){
  if (selectedJet != "leading" && selectedJet!="subleading") std::cout<<"WARNING! Unknown option "<<selectedJet<<". Function getLeadingSubleadingJet returns leading Jet"<<std::endl;
  Jet leadingJet, subleadingJet;
  if (jet0.pt() > jet1.pt()){
    leadingJet    = jet0;
    subleadingJet = jet1;
  }
  else{
    leadingJet    = jet1;
    subleadingJet = jet0;
  }

  if (selectedJet == "subleading") return subleadingJet;
  return leadingJet;
}

genParticle TopRecoAnalysis::findLastCopy(int index){
  genParticle gen_particle = fEvent.genparticles().getGenParticles()[index];
  int gen_pdgId = gen_particle.pdgId();
  for (size_t i=0; i<gen_particle.daughters().size(); i++){

    genParticle genDau = fEvent.genparticles().getGenParticles()[gen_particle.daughters().at(i)];
    int genDau_index   = genDau.index();
    int genDau_pdgId   = genDau.pdgId();
    if (gen_pdgId == genDau_pdgId) return findLastCopy(genDau_index);
  }
  return gen_particle;
}

bool TopRecoAnalysis::isWsubjet(const Jet& jet , const std::vector<Jet>& jets1 , const std::vector<Jet>& jets2){
  return  (isMatchedJet(jet,jets1)||isMatchedJet(jet,jets2));
}

bool TopRecoAnalysis::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool TopRecoAnalysis::isMatchedJet(const Jet& jet, const std::vector<Jet>& jets) {
  for (auto Jet: jets)
    {
      if (areSameJets(jet, Jet)) return true;
    }
  return false;
}

bool TopRecoAnalysis::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}

bool TopRecoAnalysis::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet){

  bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet)       && areSameJets(trijetJet2, MCtrue_SubldgJet) && areSameJets(trijetBJet,  MCtrue_Bjet);
  bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet)    && areSameJets(trijetJet2, MCtrue_LdgJet)    && areSameJets(trijetBJet,  MCtrue_Bjet);
  if (same1 || same2) return true;
  return false;

}


void TopRecoAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}




void TopRecoAnalysis::process(Long64_t entry) {
  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  const double pi = acos(-1.);
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
  // 4) Electron veto (Fully hadronic + orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================
  // 5) Muon veto (Fully hadronic + orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 7) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  //  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
 
  //================================================================================================  
  // 8) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
  // fCommonPlots.fillControlPlotsAfterBJetSelection(fEvent, bjetData);

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology selection
  //================================================================================================
  if (0) std::cout << "=== Topology selection" << std::endl;
  //  const TopologySelection::Data topologyData = fTopologySelection.analyze(fEvent, jetData);
  // if (!topologyData.passedSelection()) return; 

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  /*
    if (0) std::cout << "=== Top (ChiSq) selection" << std::endl;
    const TopSelection::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);
    // Apply preliminary chiSq cut
    bool passPrelimChiSq = cfg_PrelimTopFitChiSqr.passedCut(topData.ChiSqr());
    if (!passPrelimChiSq) return;
  */

  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData, true);
  // bool passPrelimMVACut = cfg_PrelimTopMVACut.passedCut( std::max(topData.getMVAmax1(), topData.getMVAmax2()) ); //fixme?
  // bool hasFreeBJet      = topData.hasFreeBJet();
  // if (!hasFreeBJet) return;
  // if (!passPrelimMVACut) return;

  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Standard Selections" << std::endl;
  //fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, bjetData.isGenuineB());
  
  //================================================================================================
  // All Selections
  //================================================================================================
  //  if (!topologyData.passedSelection()) return;

  //Before TopSelection
  AK8Jet LdgFatJet, SubldgFatJet;
  double ldgFatJet_pt = -999.999, sldgFatJet_pt = -999.999;
  //  double HT = jetData.HT();

  hCevts_HTmodif900 -> Fill(false,"HT<900GeV", 0);
  hCevts_HTmodif900 -> Fill(false,"HT>900GeV", 0);
  hCevts_HTmodif900 -> Fill(true,"HT<900GeV", 0);
  hCevts_HTmodif900 -> Fill(true,"HT>900GeV", 0);

  double HT_modif = 0;
    for (auto& jet: jetData.getSelectedJets()){
      if (jet.pt() < 40) continue;
      HT_modif += jet.pt();
    }
    
    if (HT_modif > 900)
      {
	hCEvts_HTmodif900_BeforeAfterTopSelection -> Fill("Before", 1);	
	//If boolean == false, the plot is filled before Top Selection
	hCevts_HTmodif900 -> Fill(false, "HT>900GeV", 1);
      }
    else hCevts_HTmodif900 -> Fill(false,"HT<900GeV", 1);
      
    

  for(AK8Jet fatJet: fEvent.ak8jets())
    {
      if (fatJet.pt() < 170) continue;
      if (ldgFatJet_pt > fatJet.pt()) continue;
      ldgFatJet_pt = fatJet.pt();
      LdgFatJet = fatJet;
      //std::cout<<"here?"<<std::endl;
    }

  bool haveLdgFatJet = ldgFatJet_pt > -1;
  if (haveLdgFatJet)
    {
      for(AK8Jet fatJet: fEvent.ak8jets())
	{
	  if (fatJet.pt() < 170) continue;
	  if (LdgFatJet.index() == fatJet.index()) continue;
	  if (sldgFatJet_pt > fatJet.pt()) continue;
	  sldgFatJet_pt = fatJet.pt();
	  SubldgFatJet = fatJet;
	}
    }


  bool haveSubldgFatJet = sldgFatJet_pt > -1;

  //  std::cout<<ldgFatJet_pt<<" "<<sldgFatJet_pt<<std::endl;

  if (haveLdgFatJet)
    {
      hLdgFatJetPt_beforeTopSelection     -> Fill(LdgFatJet.pt());
      hLdgFatJet_tau21_beforeTopSelection -> Fill(LdgFatJet.NjettinessAK8CHStau2()/LdgFatJet.NjettinessAK8CHStau1());
      hLdgFatJet_tau32_beforeTopSelection -> Fill(LdgFatJet.NjettinessAK8CHStau3()/LdgFatJet.NjettinessAK8CHStau2());

      if (haveSubldgFatJet)
	{
	  hSubldgFatJetPt_beforeTopSelection     -> Fill(SubldgFatJet.pt());
	  hSubldgFatJet_tau21_beforeTopSelection -> Fill(SubldgFatJet.NjettinessAK8CHStau2()/SubldgFatJet.NjettinessAK8CHStau1());
	  hSubldgFatJet_tau32_beforeTopSelection -> Fill(SubldgFatJet.NjettinessAK8CHStau3()/SubldgFatJet.NjettinessAK8CHStau2());
	}
      if (HT_modif > 900)
	{
	  hLdgFatJetPt_ht900_beforeTopSelection     -> Fill(LdgFatJet.pt());
	  hLdgFatJet_tau21_ht900_beforeTopSelection -> Fill(LdgFatJet.NjettinessAK8CHStau2()/LdgFatJet.NjettinessAK8CHStau1());
	  hLdgFatJet_tau32_ht900_beforeTopSelection -> Fill(LdgFatJet.NjettinessAK8CHStau3()/LdgFatJet.NjettinessAK8CHStau2());
	  
	  if (haveSubldgFatJet)
	    {
	      hSubldgFatJetPt_ht900_beforeTopSelection     -> Fill(SubldgFatJet.pt());
	      hSubldgFatJet_tau21_ht900_beforeTopSelection -> Fill(SubldgFatJet.NjettinessAK8CHStau2()/SubldgFatJet.NjettinessAK8CHStau1());
	      hSubldgFatJet_tau32_ht900_beforeTopSelection -> Fill(SubldgFatJet.NjettinessAK8CHStau3()/SubldgFatJet.NjettinessAK8CHStau2());
	    }
	}
    }


  if (!topData.passedSelection()) return;
  if (0) std::cout << "=== All Selections" << std::endl;
  cSelected.increment();
  
  //After Top Selection
  if (HT_modif > 900)
    {
      hCEvts_HTmodif900_BeforeAfterTopSelection -> Fill("After", 1);	
      //If boolean == true, if event passes the Top Selection
      hCevts_HTmodif900 -> Fill(true, "HT>900GeV", 1);
    }
  else hCevts_HTmodif900 -> Fill(true,"HT<900GeV", 1);
  

  if (haveLdgFatJet)
    {
      hLdgFatJetPt     -> Fill(LdgFatJet.pt());
      hLdgFatJet_tau21 -> Fill(LdgFatJet.NjettinessAK8CHStau2()/LdgFatJet.NjettinessAK8CHStau1());
      hLdgFatJet_tau32 -> Fill(LdgFatJet.NjettinessAK8CHStau3()/LdgFatJet.NjettinessAK8CHStau2());

      if (haveSubldgFatJet)
	{
	  hSubldgFatJetPt     -> Fill(SubldgFatJet.pt());
	  hSubldgFatJet_tau21 -> Fill(SubldgFatJet.NjettinessAK8CHStau2()/SubldgFatJet.NjettinessAK8CHStau1());
	  hSubldgFatJet_tau32 -> Fill(SubldgFatJet.NjettinessAK8CHStau3()/SubldgFatJet.NjettinessAK8CHStau2());
	}
      if (HT_modif > 900)
	{
	  hLdgFatJetPt_ht900     -> Fill(LdgFatJet.pt());
	  hLdgFatJet_tau21_ht900 -> Fill(LdgFatJet.NjettinessAK8CHStau2()/LdgFatJet.NjettinessAK8CHStau1());
	  hLdgFatJet_tau32_ht900 -> Fill(LdgFatJet.NjettinessAK8CHStau3()/LdgFatJet.NjettinessAK8CHStau2());
	  
	  if (haveSubldgFatJet)
	    {	  
	      hSubldgFatJetPt_ht900     -> Fill(SubldgFatJet.pt());
	      hSubldgFatJet_tau21_ht900 -> Fill(SubldgFatJet.NjettinessAK8CHStau2()/SubldgFatJet.NjettinessAK8CHStau1());
	      hSubldgFatJet_tau32_ht900 -> Fill(SubldgFatJet.NjettinessAK8CHStau3()/SubldgFatJet.NjettinessAK8CHStau2());
	    }
	}
    }



  //Soti Analysis
  //================================================================================================                             
  // Gen Particle Selection                            
  //================================================================================================           
  //  h_HT -> Fill ( topologyData.HT() );

  if (!fEvent.isMC()) return;

  std::vector<genParticle> GenTops_test;  
  bool foundBoostedTop = false;
  GenTops_test = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
  // For-loop: All top quarks
  if (1){ 
    for (auto& top: GenTops_test){ 
      if (top.pt() > 500) foundBoostedTop = true;
      //if (top.pt() > 500) return; 
    }  
  }
  
  hCEvts_BoostedTop -> Fill(0.5);
  hCEvts_MergedTop -> Fill(0.5);
  if (foundBoostedTop) hCEvts_BoostedTop -> Fill(1.5);

  std::vector<genParticle> GenChargedHiggs;
  std::vector<genParticle> GenChargedHiggs_BQuark;
  std::vector<genParticle> GenTops;
  std::vector<genParticle> GenTops_BQuark;
  std::vector<genParticle> GenTops_SubldgQuark;
  std::vector<genParticle> GenTops_LdgQuark;
  
  vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, MC_BJets;
  vector <Jet> HiggsTop_LdgJet, HiggsTop_SubldgJet, HiggsTop_Bjet, HBjet, MCtrue_TopJets;
  vector <Jet> HiggsTop_2j_LdgJet, HiggsTop_2j_SubldgJet, HiggsTop_2j_Bjet;   //At least 2 jets matched to Higgs's side top decay products
  vector <Jet> AssocTop_LdgJet, AssocTop_SubldgJet, AssocTop_Bjet;
  std::vector<bool> FoundTop;
  
  const double twoSigmaDpt = 0.32;
  const double dRcut    = 0.4;
  
  int nGenuineTops = 0;
  GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
  

  hCevts_FatJet_Pt450 -> Fill("All", 1);
  bool foundFatJet_Pt450 =false;
  for(AK8Jet jet: fEvent.ak8jets())
    {
      if (jet.pt() > 450) foundFatJet_Pt450 = true;
    }
  
  if (foundFatJet_Pt450) hCevts_FatJet_Pt450 -> Fill("p_{T}>450GeV", 1);
  
  // For-loop: All top quarks                                                                                                      
  for (auto& top: GenTops){
    
    bool FoundBQuark = false;
    std::vector<genParticle> quarks;
    genParticle bquark;
    
    // For-loop: Top quark daughters (Nested)                                                                   
    for (size_t i=0; i<top.daughters().size(); i++)
      {
	
        int dau_index = top.daughters().at(i);
        genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
	
        // B-Quark                                                                                                        
        if (std::abs(dau.pdgId()) ==  5)
          {
            bquark = dau;
            FoundBQuark = true;
          }
	
        // W-Boson                                                                                                       
	if (std::abs(dau.pdgId()) == 24)
          {
	    // Get the last copy                                               
	    genParticle W = GetLastCopy(fEvent.genparticles().getGenParticles(), dau);
            // For-loop: W-boson daughters                                                                    
	    for (size_t idau=0; idau<W.daughters().size(); idau++)
              {
                // Find the decay products of W-boson                                                                                                                                                                   
                int Wdau_index = W.daughters().at(idau);
                genParticle Wdau = fEvent.genparticles().getGenParticles()[Wdau_index];
		
                // Consider only quarks as decaying products                                                     
                if (std::abs(Wdau.pdgId()) > 5) continue;
		
                // Save daughter                                                                                                
                quarks.push_back(Wdau);
              }//W-boson daughters                                                                                                                    
          }//W-boson                                                                                                                                       
      }//Top-quark daughters                                                                                           
    
    // Skip top if b-quark is not found (i.e. top decays to W and c)                                                                     
    if (!FoundBQuark) continue;
    // Skip top if it decays leptonically (the "quarks" vector will be empty causing errors)                               
    
    if (quarks.size() < 2) continue;
    // Fill vectors for b-quarks, leading and subleading quarks coming from tops                                                                                                                                        
    GenTops_BQuark.push_back(bquark);
    
    if (quarks.at(0).pt() > quarks.at(1).pt())
      {
        GenTops_LdgQuark.push_back(quarks.at(0));
        GenTops_SubldgQuark.push_back(quarks.at(1));
      }
    else
      {
        GenTops_LdgQuark.push_back(quarks.at(1));
        GenTops_SubldgQuark.push_back(quarks.at(0));
      }
    
  } // For-Loop over top quarks                                     
  GenChargedHiggs = GetGenParticles(fEvent.genparticles().getGenParticles(), 37);
  
  //Match bjet from Higgs                                                                                
  // For-loop: All top quarks                      
  for (auto& hplus: GenChargedHiggs)
    {
      genParticle bquark;
      // For-loop: Top quark daughters (Nested)                                                      
      for (size_t i=0; i<hplus.daughters().size(); i++)
        {
          int dau_index = hplus.daughters().at(i);
          genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
          // B-Quark                          
	  if (std::abs(dau.pdgId()) ==  5) GenChargedHiggs_BQuark.push_back(dau);
        }
    }
  
  // Skip matcing if top does not decay to b                                                                                                         
  bool doMatching = (GenTops_BQuark.size() == GenTops.size());
  
  // hCEvts_BoostedTop
  bool mergedTop = 0;

  if (doMatching)
    {
      size_t ntops = GenTops.size();

      for (size_t i=0; i< ntops; i++)
	{
	  genParticle bquark = GenTops_BQuark.at(i);
	  genParticle quark1 = GenTops_LdgQuark.at(i);
	  genParticle quark2 = GenTops_SubldgQuark.at(i);

	  double dR12 = ROOT::Math::VectorUtil::DeltaR(quark1.p4(), quark2.p4());
	  double dR1b = ROOT::Math::VectorUtil::DeltaR(quark1.p4(), bquark.p4());
	  double dR2b = ROOT::Math::VectorUtil::DeltaR(quark2.p4(), bquark.p4());

	  mergedTop += dR12 < 0.8 || dR1b < 0.8 || dR2b < 0.8;
	}
    }
  if (mergedTop)
    {
      hCEvts_MergedTop -> Fill(1.5);
      //      return;
    }
  // Matching criteria: Quarks-Jets matching with DR and DPt/Pt criteria                              

  //if (!topData.passedSelection()) return;   //Top Selection!!!


  vector <genParticle> MGen_LdgJet, MGen_SubldgJet, MGen_Bjet;
  vector <double> dRminB;
  Jet firstBjet;
  if (doMatching)
    {
      // ======= B jet matching (Loop over all Jets)                                         
      // For-loop: All top-quarks                                                                                           
      for (size_t i=0; i<GenTops.size(); i++)
        {
          genParticle BQuark = GenTops_BQuark.at(i);
          Jet mcMatched_BJet;
          double dRmin  = 99999.9;
          //double dPtOverPtmin = 99999.9;
	  
          // For-loop: All selected jets                                                                                    
	  for (auto& bjet: jetData.getSelectedJets())
            {
              double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
	      
              double dPtOverPt = std::abs((bjet.pt() - BQuark.pt())/BQuark.pt());
	      
              // Only consider dR < dRcut                                                                            
	      // if (dR > dRcut) continue;  at least two matched jets
	      
              // Find minimum dR                                                                                                  
	      if (dR > dRmin) continue;
	      
              // Find minimum dPtOverPt                                                                 
              if (dPtOverPt > twoSigmaDpt) continue;
	      
	      // Store values                                                                                                              
              dRmin  = dR;
              //dPtOverPtmin = dPtOverPt;
              mcMatched_BJet = bjet;
            }// For-loop: selected jets                                                                                                            
	  
          // Store match                                                                                                             
          dRminB.push_back(dRmin);
          MC_BJets.push_back(mcMatched_BJet);
	  
        }// For-loop: All top-quarks                                                                                                                             

      //======= Dijet matching (Loop over all Jets)                                                                                                                  
      //======= For-loop: All top-quarks                                                                                                                  
      
      for (size_t i=0; i<GenTops.size(); i++)
        {
	  
          genParticle top = GenTops.at(i);
          genParticle LdgQuark    = GenTops_LdgQuark.at(i);
          genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
	  
          Jet mcMatched_LdgJet;
          Jet mcMatched_SubldgJet;
	  
          double dR1min, dR2min, dPtOverPt1min, dPtOverPt2min;
          dR1min = dR2min = dPtOverPt1min = dPtOverPt2min = 99999.9;
	  
	  // For-loop: All selected jets                              
          for (auto& jet: jetData.getSelectedJets())
            {
              bool same = false;
              // For-loop: All top-quarks                                                                                 
	      for (size_t k=0; k<GenTops.size(); k++)
                {
                  if (dRminB.at(k) < dRcut)
                    {
                      // Skip the jets that are matched with bquarks                                                                                        
                      if( areSameJets(jet,MC_BJets.at(k))) same = true;
                    }
                }// For-loop: All top-quarks                                                                                                   
	      
              if (same) continue;
	      
              // Find dR for the two jets in top-decay dijet                                                                                          
              double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
              double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
	      
              // Require both jets to be within dR <= dRcut                                                                                             
              //if (std::min(dR1, dR2) > dRcut) continue; at least two matched jets
	      
              // Calculate dPtOverPt for each jet in top-decay dijet                                                                                                                    
              double dPtOverPt1 = std::abs((jet.pt() - LdgQuark.pt())/LdgQuark.pt());
              double dPtOverPt2 = std::abs((jet.pt() - SubldgQuark.pt())/SubldgQuark.pt());
	      
              // Find which of the two is the correct match                                                                              
              if (dR1 < dR2)
                {
                  // Is Jet1 closer in eta-phi AND has smaller pT difference?                                          
                  if (dR1 < dR1min)
                    {
                      if (dPtOverPt1 < twoSigmaDpt)
                        {
                          dR1min = dR1;
                          dPtOverPt1min= dPtOverPt1;
                          mcMatched_LdgJet = jet;
                        }
                    }
		  
                  // Is Jet2 closer in eta-phi AND has smaller pT difference?                                                                             
                  //else if (dR2 <= dRcut && dR2 < dR2min)  at least two matched jets
		  else if (dR2 < dR2min)                  //at least two matched jets
                    {
                      if (dPtOverPt2 < twoSigmaDpt)
                        {
                          dR2min  = dR2;
                          dPtOverPt2min = dPtOverPt2;
                          mcMatched_SubldgJet = jet;
                        }
                    }
                }
              else
                {
                  // Is Jet2 closer in eta-phi AND has smaller pT difference?                                                                                  
                  if (dR2 < dR2min)
                    {
                      if (dPtOverPt2 < twoSigmaDpt)
                        {
                          dR2min  = dR2;
                          dPtOverPt2min = dPtOverPt2;
                          mcMatched_SubldgJet = jet;
                        }
                    }

		  // Is Jet2 closer in eta-phi AND has smaller pT difference?                                                                           
		  // else if (dR1 <= dRcut && dR1 < dR1min)  at least two matched jets
		  else if (dR1 < dR1min)                //at least two matched jets
                    {
                      if  (dPtOverPt1 < twoSigmaDpt)
                        {
                          dR1min  = dR1;
                          dPtOverPt1min = dPtOverPt1;
                          mcMatched_LdgJet = jet;
                        }
                    }
                }
            }//For-loop: All selected jets    
	  
          // Check if TOP is genuine                                                                                                            
	  bool isGenuine = (dR1min<= dRcut && dR2min <= dRcut && dRminB.at(i) <= dRcut);
	  bool twoJMatched = isGenuine;  //at least two matched jets two top decay products (used for plots)
	  
	  if (!twoJMatched) twoJMatched = max(dR1min, dR2min) <= dRcut || max(dR1min, dRminB.at(i)) <= dRcut || max(dR2min, dRminB.at(i)) <= dRcut;
	  
	  // std::cout<<"DeltaR1: "<<dR1min<<" DeltaR2: "<<dR2min<<" DeltaRb: "<<dRminB.at(i)<<std::endl;
	  // std::cout<<" isGenuine "<<isGenuine<<" twoJMatched "<<twoJMatched<<std::endl;
	  // std::cout<<"==="<<std::endl;

          if (isGenuine)
            {
              // Increase the counter of genuine tops                                                                                                        
              nGenuineTops++;
              MCtrue_LdgJet.push_back(mcMatched_LdgJet);
              MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
              MCtrue_Bjet.push_back(MC_BJets.at(i));
              MGen_LdgJet.push_back(GenTops_LdgQuark.at(i));
              MGen_SubldgJet.push_back(GenTops_SubldgQuark.at(i));
              MGen_Bjet.push_back(GenTops_BQuark.at(i));
	      
              MCtrue_TopJets.push_back(mcMatched_LdgJet);
              MCtrue_TopJets.push_back(mcMatched_SubldgJet);
              MCtrue_TopJets.push_back(MC_BJets.at(i));
              if (HasMother(fEvent, top, 37))
                {
                  //decay products (jets) of H+ top                                                                                              
                  HiggsTop_LdgJet.push_back(mcMatched_LdgJet);
                  HiggsTop_SubldgJet.push_back(mcMatched_SubldgJet);
                  HiggsTop_Bjet.push_back(MC_BJets.at(i));
                }
              else
                {
                  //decay products (jets) of associated top                                                                     
                  AssocTop_LdgJet.push_back(mcMatched_LdgJet);
                  AssocTop_SubldgJet.push_back(mcMatched_SubldgJet);
                  AssocTop_Bjet.push_back(MC_BJets.at(i));
                }
            }// if (isGenuine)                                                                                                                          
          // Top quark matched with a trijet                                                                                                               

	  //at least two jets matched to 2 Higgs' side top decay products.
	  if (twoJMatched && HasMother(fEvent, top, 37))
	    {
	      //decay products (jets) of H+ top                                                                                              
	      HiggsTop_2j_LdgJet.push_back(mcMatched_LdgJet);
	      HiggsTop_2j_SubldgJet.push_back(mcMatched_SubldgJet);
	      HiggsTop_2j_Bjet.push_back(MC_BJets.at(i));
	    }
	  
          FoundTop.push_back(isGenuine);
        }//For-loop: All top-quarks                                           
      
      //BJet from Higgs-side                                                                                                      
      for (size_t i=0; i<GenChargedHiggs_BQuark.size(); i++)
        {
          double dRmin = 999.999;
          Jet mcMatched_ChargedHiggsBjet;
          for (auto& jet: jetData.getSelectedJets())
            {
              double same = false;
              for (auto& topJet: MCtrue_TopJets) if (areSameJets(jet, topJet)) same = true;
              if (same) continue;
              double dR_Hb = ROOT::Math::VectorUtil::DeltaR(jet.p4(),GenChargedHiggs_BQuark.at(i).p4());
              double dPtOverPt_Hb = std::abs(jet.pt() - GenChargedHiggs_BQuark.at(i).pt())/GenChargedHiggs_BQuark.at(i).pt();
              if (dR_Hb > dRcut || dR_Hb > dRmin) continue;
              if (dPtOverPt_Hb > twoSigmaDpt) continue;
              dRmin = dR_Hb;
              mcMatched_ChargedHiggsBjet = jet;
            }
          if (dRmin <= dRcut) HBjet.push_back(mcMatched_ChargedHiggsBjet);
        }
    } //if (doMatching)
      
  //==================================================================================================================================
  //Soti

  bool haveMatchedChargedHiggsBJet    = HBjet.size() > 0;
  bool haveMatchedTopFromChargedHiggs = HiggsTop_Bjet.size() > 0;
  bool haveMatchedAssocTop            = AssocTop_Bjet.size() > 0; 
  
  if (0) std::cout<<haveMatchedAssocTop<<std::endl;
  
  if (doMatching){
  for (size_t i=0; i< GenTops.size(); i++)
    {
      if (FoundTop.at(i))
	{
	  genParticle top = GenTops.at(i);
	  hMatched_TopQuark_Pt -> Fill(top.pt());
	}
    }
      
  double deltaRmin_qq = 999.999;
  double deltaRmin_jj = 999.999;
  genParticle quark1, quark2;
  Jet jet1, jet2;
  
  for (size_t i=0; i< MGen_Bjet.size(); i++)
    {
      genParticle ldg_quark    = MGen_LdgJet.at(i);
      genParticle subldg_quark = MGen_SubldgJet.at(i);
      genParticle bquark       = MGen_Bjet.at(i);

      double dR_q1q2 = ROOT::Math::VectorUtil::DeltaR(ldg_quark.p4(), subldg_quark.p4());
      double dR_q1b  = ROOT::Math::VectorUtil::DeltaR(ldg_quark.p4(), bquark.p4());
      double dR_q2b  = ROOT::Math::VectorUtil::DeltaR(subldg_quark.p4(), bquark.p4());
      double dR_min = min(dR_q1q2, min(dR_q1b, dR_q2b));
      
      if (deltaRmin_qq > dR_min)
	{
	  deltaRmin_qq = dR_min;
	  if (dR_q1q2 < dR_q1b && dR_q1q2 < dR_q2b)
	    {
	      quark1 = ldg_quark;
	      quark2 = subldg_quark;
	    }
	  if (dR_q1b < dR_q1q2 && dR_q1b < dR_q2b)
	    {
	      quark1 = ldg_quark;
	      quark2 = bquark;
	    }
	  if (dR_q2b < dR_q1q2 && dR_q2b < dR_q1b)
	    {
	      quark1 = subldg_quark;
	      quark2 = bquark;
	    }
	}

      hMatched_Q1Q2_Pt                     -> Fill((ldg_quark.p4() + subldg_quark.p4()).pt());
      hMatched_Q1Q2B_Pt                    -> Fill((ldg_quark.p4() + subldg_quark.p4() + bquark.p4()).pt());
      hMatched_Q1Q2_Pt_Vs_Matched_Q1Q2B_Pt -> Fill((ldg_quark.p4() + subldg_quark.p4()).pt(), (ldg_quark.p4() + subldg_quark.p4() + bquark.p4()).pt());
    }

  for (auto& j1: jetData.getSelectedJets())
    {
      for (auto& j2: jetData.getSelectedJets())
	{
	  if (areSameJets(j1, j2)) continue;
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(j1.p4(), j2.p4());
	  if (deltaRmin_jj > deltaR)
	    {
	      deltaRmin_jj = deltaR;
	      jet1 = j1;
	      jet2 = j2;
	    }
	}
    }

  //====
  bool findMin = deltaRmin_qq < 999. && deltaRmin_jj < 999.;
  
  if (findMin)
    {
      bool same1 = ROOT::Math::VectorUtil::DeltaR(quark1.p4(), jet1.p4()) <= 0.3 && ROOT::Math::VectorUtil::DeltaR(quark2.p4(), jet1.p4()) <= 0.3;
      bool same2 = ROOT::Math::VectorUtil::DeltaR(quark1.p4(), jet2.p4()) <= 0.3 && ROOT::Math::VectorUtil::DeltaR(quark2.p4(), jet2.p4()) <= 0.3;
      
      if ((same1 || same2) && 0)
	{
	  std::cout<<"DR_q1j1: "<<ROOT::Math::VectorUtil::DeltaR(quark1.p4(), jet1.p4())<<std::endl;
	  std::cout<<"DR_q2j1: "<<ROOT::Math::VectorUtil::DeltaR(quark2.p4(), jet1.p4())<<std::endl;;
	  std::cout<<"DR_q1j2: "<<ROOT::Math::VectorUtil::DeltaR(quark1.p4(), jet2.p4())<<std::endl;;
	  std::cout<<"DR_q2j2: "<<ROOT::Math::VectorUtil::DeltaR(quark2.p4(), jet2.p4())<<std::endl;;
	  std::cout<<"same1: "<<same1<<" same2: "<<same2<<std::endl;
	  std::cout<<"deltaRmin_qq: "<<deltaRmin_qq<<" deltaRmin_jj: "<<deltaRmin_jj<<std::endl;
	  std::cout<<"==="<<std::endl;
	}
      if (same1 || same2) deltaRmin_jj = -1.;

      hDeltaRqqMin_Vs_DeltaRjjMin -> Fill(deltaRmin_qq, deltaRmin_jj);
    }
  //====

  for (size_t i=0; i< MCtrue_Bjet.size(); i++)
    {
      Jet ldgJet    = MCtrue_LdgJet.at(i);
      Jet subldgJet = MCtrue_SubldgJet.at(i);
      Jet bjet      = MCtrue_Bjet.at(i);

      math::XYZTLorentzVector dijet_p4, trijet_p4;
      dijet_p4  = ldgJet.p4() + subldgJet.p4();
      trijet_p4 = ldgJet.p4() + subldgJet.p4() + bjet.p4();
	  
      double dR_j1j2 = ROOT::Math::VectorUtil::DeltaR(ldgJet.p4(), subldgJet.p4());
      double dR_j1b  = ROOT::Math::VectorUtil::DeltaR(ldgJet.p4(), bjet.p4());
      double dR_j2b  = ROOT::Math::VectorUtil::DeltaR(subldgJet.p4(), bjet.p4());
            
      bool mergedDijet            = dR_j1j2 < 0.8 && dR_j1b > 0.8 && dR_j2b > 0.8 && max(ldgJet.bjetDiscriminator(), subldgJet.bjetDiscriminator()) < 0.5426;
      bool mergedTrijet_untaggedW = max(dR_j1j2, max(dR_j1b, dR_j2b)) < 0.8 && max(ldgJet.bjetDiscriminator(), subldgJet.bjetDiscriminator()) < 0.5426;
      bool mergedTrijet           = max(dR_j1j2, max(dR_j1b, dR_j2b)) < 0.8;
      bool mergedJB               = dR_j1j2 > 0.8 && max(dR_j1b, dR_j2b) > 0.8 && min(dR_j1b, dR_j2b) < 0.8;
	  
      bool isHtop = false; 
      if (haveMatchedTopFromChargedHiggs)
	{
	  isHtop = areSameJets(HiggsTop_Bjet.at(0), bjet) && areSameJets(HiggsTop_LdgJet.at(0), ldgJet) && areSameJets(HiggsTop_SubldgJet.at(0), subldgJet);
	}
	  
      hMatched_DijetDeltaR      -> Fill(dR_j1j2);
      hMatched_DeltaR_DijetBjet -> Fill(mergedDijet, ROOT::Math::VectorUtil::DeltaR(dijet_p4, bjet.p4()));
      hMatched_DijetMass        -> Fill(mergedDijet, dijet_p4.M());
      hMatched_DijetPt          -> Fill(mergedDijet, dijet_p4.Pt());
	  
      if (isHtop)
	{
	  hHiggsTop_DijetDeltaR      -> Fill(dR_j1j2);
	  hHiggsTop_DeltaR_DijetBjet -> Fill(mergedDijet, ROOT::Math::VectorUtil::DeltaR(dijet_p4, bjet.p4()));
	  hHiggsTop_DijetMass        -> Fill(mergedDijet, dijet_p4.M());
	  hHiggsTop_DijetPt          -> Fill(mergedDijet, dijet_p4.Pt());
	}

      hCEvts_mergedDijet             -> Fill(isHtop, 0.5);
      hCEvts_mergedTrijet            -> Fill(isHtop, 0.5);
      hCEvts_mergedTrijet_untaggedW  -> Fill(isHtop, 0.5);
      hCEvts_mergedJB                -> Fill(isHtop, 0.5);
	  
      if (mergedDijet)                                hCEvts_mergedDijet -> Fill(isHtop, 1.5);
      if (mergedDijet && (dijet_p4.Pt() < 200))       hCEvts_mergedDijet -> Fill(isHtop, 2.5);
	  
      if (mergedTrijet_untaggedW)                           hCEvts_mergedTrijet_untaggedW -> Fill(isHtop, 1.5);
      if (mergedTrijet_untaggedW && (trijet_p4.Pt() < 400)) hCEvts_mergedTrijet_untaggedW -> Fill(isHtop, 2.5);
	  
      if (mergedTrijet)                           hCEvts_mergedTrijet -> Fill(isHtop, 1.5);
      if (mergedTrijet && (trijet_p4.Pt() < 400)) hCEvts_mergedTrijet -> Fill(isHtop, 2.5);	  

      if (mergedJB)                               hCEvts_mergedJB     -> Fill(isHtop, 1.5);

      if (max(dR_j1b, dR_j2b) < 0.8) hMatched_DeltaRDijet_mergedJB    -> Fill(isHtop, dR_j1j2);
      
    }
  }// if (doMatching){                              
  /*  
  if (haveMatchedTopFromChargedHiggs)
    {
      Jet bjet = HiggsTop_Bjet.at(0);
      Jet jet1 = HiggsTop_LdgJet.at(0);
      Jet jet2 = HiggsTop_SubldgJet.at(0);
      
      math::XYZTLorentzVector higgs_dijet_p4, higgs_trijet_p4;
      higgs_dijet_p4 = jet1.p4() + jet2.p4();
      higgs_trijet_p4 = jet1.p4() + jet2.p4() + bjet.p4();

      double dR_j1j2 = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
      double dR_j1b  = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), bjet);
      double dR_j2b  = ROOT::Math::VectorUtil::DeltaR(jet2.p4(), bjet);

      bool mergedDijet  = dR_j1j2 < 0.8 && dR_j1b > 0.8 && dR_j2b > 0.8 && max(jet1.bjetDiscriminator(), jet2.bjetDiscriminator()) < 0.5426;
      bool mergedTrijet_untaggedW = max(dR_j1j2, max(dR_j1b, dR_j2b)) < 0.8 && max(jet1.bjetDiscriminator(), jet2.bjetDiscriminator()) < 0.5426;
      bool mergedTrijet = max(dR_j1j2, max(dR_j1b, dR_j2b)) < 0.8;
      bool mergedJB     = dR_j1j2 > 0.8 && max(dR_j1b, dR_j2b) > 0.8 && min(dR_j1b, dR_j2b) < 0.8;

      hHiggsTop_DijetDeltaR -> Fill(dR_j1j2);
      hHiggsTop_DeltaR_DijetBjet -> Fill(mergedDijet, ROOT::Math::VectorUtil::DeltaR(higgs_dijet_p4, bjet.p4()));
      hHiggsTop_DijetMass -> Fill(mergedDijet, higgs_dijet_p4.M());
      hHiggsTop_DijetPt -> Fill(mergedDijet, higgs_dijet_p4.Pt());

      hCEvts_mergedDijet -> Fill(0.5);
      hCEvts_mergedTrijet -> Fill(0.5);
      hCEvts_mergedTrijet_untaggedW -> Fill(0.5);

      if (mergedDijet) hCEvts_mergedDijet -> Fill(1.5);
      if (mergedDijet && (higgs_dijet_p4.Pt() < 200)) hCEvts_mergedDijet -> Fill(2.5);

      if (mergedTrijet_untaggedW) hCEvts_mergedTrijet_untaggedW -> Fill(1.5);
      if (mergedTrijet_untaggedW && (higgs_trijet_p4.Pt() < 200)) hCEvts_mergedTrijet_untaggedW -> Fill(2.5);

      if (mergedTrijet) hCEvts_mergedTrijet -> Fill(1.5);
      if (mergedTrijet && (higgs_trijet_p4.Pt() < 200)) hCEvts_mergedTrijet -> Fill(2.5);
      
    }
  */
  //================================================================================================================================================//

    
  //================================================================================================================================================//

  bool isBfromH = false;
  if (haveMatchedChargedHiggsBJet) isBfromH = areSameJets(HBjet.at(0), topData.getTetrajetBJet());

  SelectedTrijet LdgTrijet, SubldgTrijet;  //Leading (subleading) in pt Selected Trijet 

  if (areSameJets(topData.getLdgTrijetBJet(), topData.getTrijet1BJet()))
    {
      LdgTrijet.Jet1 = topData.getTrijet1Jet1();
      LdgTrijet.Jet2 = topData.getTrijet1Jet2();
      LdgTrijet.BJet = topData.getLdgTrijetBJet();
      LdgTrijet.TrijetP4 = topData.getLdgTrijet();
      
      SubldgTrijet.Jet1 = topData.getTrijet2Jet1();
      SubldgTrijet.Jet2 = topData.getTrijet2Jet2();
      SubldgTrijet.BJet = topData.getSubldgTrijetBJet();
      SubldgTrijet.TrijetP4 = topData.getSubldgTrijet();
    }
  else if (areSameJets(topData.getLdgTrijetBJet(), topData.getTrijet2BJet()))
    {
      LdgTrijet.Jet1 = topData.getTrijet2Jet1();
      LdgTrijet.Jet2 = topData.getTrijet2Jet2();
      LdgTrijet.BJet = topData.getLdgTrijetBJet();
      LdgTrijet.TrijetP4 = topData.getLdgTrijet();
      
      SubldgTrijet.Jet1 = topData.getTrijet1Jet1();
      SubldgTrijet.Jet2 = topData.getTrijet1Jet2();
      SubldgTrijet.BJet = topData.getSubldgTrijetBJet();
      SubldgTrijet.TrijetP4 = topData.getSubldgTrijet();
    }
  else
    {
      std::cout<<"never reach here"<<std::endl;
    }

  //====================================================================================================================//
  // Fat jet Analysis
  //====================================================================================================================//
  //Create text bins 

  //Require HT_modif >900GeV
  if (HT_modif < 900) return;

  const double  ptcut_min = 200;
  double ptcut = ptcut_min;

  vector<double> ptcuts;
  //Find the fraction of events in a wide range of fatjet.pt values (from 200 to 600+ - step 50)
  for (size_t i=0; i< hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.size() ; i++)
    {
      std::cout<<"ptcut "<<ptcut<<std::endl;
      ptcuts.push_back(ptcut);
      ptcut += 50;
    }
  
  hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("t1b", 0);
  hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("wb", 0);
  hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("jb", 0);
  hCEvts_LdgTrijet_MergedResolved -> Fill("merged", 0);
  hCEvts_LdgTrijet_MergedResolved -> Fill("resolved", 0);
  
  hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Ldg", 0);
  hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Subldg", 0);
  hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Other", 0);
  
  for (size_t i =0; i< ptcuts.size(); i++)
    {
      hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("t1b", 0);
      hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("wb", 0);
      hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("jb", 0);
      //      hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("resolved", 0);
    }
  

  bool haveLdgFatTop = false,    haveLdgFatW = false,    haveLdgFatJB = false;
  bool haveSubldgFatTop = false, haveSubldgFatW = false, haveSubldgFatBJ = false;
  AK8Jet FatJet_ldgFatTop, FatJet_ldgFatW, FatJet_ldgFatJB, FatJet;

  bool isLdgTrijetW_untagged    = true; //max(LdgTrijet.Jet1.bjetDiscriminator(), LdgTrijet.Jet2.bjetDiscriminator()) < 0.5426;
  bool isSubldgTrijetW_untagged = true; //max(SubldgTrijet.Jet1.bjetDiscriminator(), SubldgTrijet.Jet2.bjetDiscriminator()) < 0.5426;

  for(AK8Jet fatJet: fEvent.ak8jets())
    {
      if (fatJet.pt() < 170) continue;
      
      double ldg_dR1fat =  ROOT::Math::VectorUtil::DeltaR( LdgTrijet.Jet1.p4(), fatJet.p4());
      double ldg_dR2fat =  ROOT::Math::VectorUtil::DeltaR( LdgTrijet.Jet2.p4(), fatJet.p4());
      double ldg_dRbfat =  ROOT::Math::VectorUtil::DeltaR( LdgTrijet.BJet.p4(), fatJet.p4());
      
      double sldg_dR1fat =  ROOT::Math::VectorUtil::DeltaR( SubldgTrijet.Jet1.p4(), fatJet.p4());
      double sldg_dR2fat =  ROOT::Math::VectorUtil::DeltaR( SubldgTrijet.Jet2.p4(), fatJet.p4());
      double sldg_dRbfat =  ROOT::Math::VectorUtil::DeltaR( SubldgTrijet.BJet.p4(), fatJet.p4());
      
      // bool isLdgTrijetW_untagged    = max(LdgTrijet.Jet1.bjetDiscriminator(), LdgTrijet.Jet2.bjetDiscriminator()) < 0.5426;
      // bool isSubldgTrijetW_untagged = max(SubldgTrijet.Jet1.bjetDiscriminator(), SubldgTrijet.Jet2.bjetDiscriminator()) < 0.5426;
      
      if (max(ldg_dRbfat, max(ldg_dR1fat, ldg_dR2fat)) < 0.8)
	{
	  haveLdgFatTop = true;
	  FatJet_ldgFatTop = fatJet;
	  FatJet = fatJet;
	}
      else if (max(ldg_dR1fat, ldg_dR2fat) < 0.8)
	{
	  haveLdgFatW = true;
	  FatJet_ldgFatW = fatJet;
	  FatJet = fatJet;
	}
      else if (max(ldg_dRbfat, ldg_dR1fat)< 0.8 || max(ldg_dRbfat, ldg_dR2fat)< 0.8)
	{
	  haveLdgFatJB = true;      
	  FatJet_ldgFatJB = fatJet;
	  FatJet = fatJet;
	}
      if (max(sldg_dRbfat, max(sldg_dR1fat, sldg_dR2fat)) < 0.8)                         haveSubldgFatTop = true;
      else if (max(sldg_dR1fat, sldg_dR2fat) < 0.8)                                      haveSubldgFatW = true;
      else if (max(sldg_dRbfat, sldg_dR1fat)< 0.8 || max(sldg_dRbfat, sldg_dR2fat)< 0.8) haveSubldgFatBJ = true;
    }
  // if (haveLdgFatTop+haveLdgFatW+haveLdgFatJB > 0)
  // 	{
  // 	  std::cout<<"DeltaR "<<ldg_dR1fat<<" "<<ldg_dR2fat<<" "<<ldg_dRbfat<<std::endl;
  // 	  std::cout<<haveLdgFatTop<<" "<<haveLdgFatW<<" "<<haveLdgFatJB<<std::endl;
  // 	}
  
  // if (haveLdgFatTop || haveLdgFatW || haveLdgFatJB) Fat_ldgTrijet = fatJet;
  // if (haveSubldgFatTop || haveSubldgFatW || haveSubldgFatBJ) Fat_sldgTrijet = fatJet;

      // double tau21 = fatJet.NjettinessAK8CHStau2()/fatJet.NjettinessAK8CHStau1();
      // double tau32 = fatJet.NjettinessAK8CHStau3()/fatJet.NjettinessAK8CHStau2();


  
  if (haveLdgFatTop || haveLdgFatW || haveLdgFatJB)
    {
      hCEvts_LdgTrijet_MergedResolved -> Fill("merged", 1);
      if (haveLdgFatTop)      hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("t1b", 1);
      else if (haveLdgFatW)   hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("wb", 1);
      else if (haveLdgFatJB)  hCEvts_LdgTrijetMatchedToFatJet_categories -> Fill("jb", 1);
      
      for (size_t i =0; i< ptcuts.size(); i++)
	{
	  if (FatJet.pt() < ptcuts.at(i)) continue;
	  if (haveLdgFatTop) hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("t1b", 1);
	  if (haveLdgFatW)   hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("wb", 1);
	  if (haveLdgFatJB)  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("jb", 1);
	}
    }
  else
    {
      hCEvts_LdgTrijet_MergedResolved -> Fill("resolved", 1);
      // for (size_t i =0; i< ptcuts.size(); i++)
      // 	{
      // 	  //if (FatJet.pt() < ptcuts.at(i)) continue;
      // 	  hCEvts_LdgTrijetMatchedToFatJet_Ptcuts.at(i) -> Fill("resolved", 1);
	  
      // 	}
    }
  if (haveLdgFatTop)
    {
      hFatTop_LdgTrijet_Pt -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatTop.pt());

      if (LdgFatJet.index() == FatJet_ldgFatTop.index())         hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Ldg", 1);
      else if (SubldgFatJet.index() == FatJet_ldgFatTop.index()) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Subldg", 1);
      else if ((LdgFatJet.index() != FatJet_ldgFatTop.index()) && (SubldgFatJet.index() != FatJet_ldgFatTop.index())) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Other", 1);
      
      double tau21 = FatJet_ldgFatTop.NjettinessAK8CHStau2()/FatJet_ldgFatTop.NjettinessAK8CHStau1();
      double tau32 = FatJet_ldgFatTop.NjettinessAK8CHStau3()/FatJet_ldgFatTop.NjettinessAK8CHStau2();
      

      hFatTop_LdgTrijet_tau21 -> Fill(isLdgTrijetW_untagged, tau21);
      hFatTop_LdgTrijet_tau32 -> Fill(isLdgTrijetW_untagged, tau32);
      
      if (HT_modif > 900)
	{
	  hFatTop_LdgTrijet_Pt_ht900 -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatTop.pt());
	  hFatTop_LdgTrijet_tau21_ht900 -> Fill(isLdgTrijetW_untagged, tau21);
	  hFatTop_LdgTrijet_tau32_ht900 -> Fill(isLdgTrijetW_untagged, tau32);
	}
    }
  else if (haveLdgFatW)
    {
      hFatW_LdgTrijet_Pt   -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatW.pt());
      if (LdgFatJet.index() == FatJet_ldgFatW.index())         hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Ldg", 1);
      else if (SubldgFatJet.index() == FatJet_ldgFatW.index()) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Subldg", 1);
      else if ((LdgFatJet.index() != FatJet_ldgFatW.index()) && (SubldgFatJet.index() != FatJet_ldgFatTop.index())) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Other", 1);

      double tau21 = FatJet_ldgFatW.NjettinessAK8CHStau2()/FatJet_ldgFatW.NjettinessAK8CHStau1();
      double tau32 = FatJet_ldgFatW.NjettinessAK8CHStau3()/FatJet_ldgFatW.NjettinessAK8CHStau2();
       
      hFatW_LdgTrijet_tau21  -> Fill(isLdgTrijetW_untagged, tau21);
      hFatW_LdgTrijet_tau32  -> Fill(isLdgTrijetW_untagged, tau32);
      if (HT_modif > 900)
	{
	  hFatW_LdgTrijet_Pt_ht900 -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatW.pt());
	  hFatW_LdgTrijet_tau21_ht900 -> Fill(isLdgTrijetW_untagged, tau21);
	  hFatW_LdgTrijet_tau32_ht900 -> Fill(isLdgTrijetW_untagged, tau32);
	}
    }
  else if (haveLdgFatJB)
    {
      hFatJB_LdgTrijet_Pt -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatJB.pt());

      if (LdgFatJet.index() == FatJet_ldgFatJB.index())         hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Ldg", 1);
      else if (SubldgFatJet.index() == FatJet_ldgFatJB.index()) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Subldg", 1);
      else if ((LdgFatJet.index() != FatJet_ldgFatJB.index()) && (SubldgFatJet.index() != FatJet_ldgFatTop.index())) hCEvts_LdgTrijetMatchedtoFatJet_LdgSbldgOther -> Fill("Other", 1);

      double tau21 = FatJet_ldgFatJB.NjettinessAK8CHStau2()/FatJet_ldgFatJB.NjettinessAK8CHStau1();
      double tau32 = FatJet_ldgFatJB.NjettinessAK8CHStau3()/FatJet_ldgFatJB.NjettinessAK8CHStau2();

      hFatJB_LdgTrijet_tau21 -> Fill(isLdgTrijetW_untagged, tau21);
      hFatJB_LdgTrijet_tau32 -> Fill(isLdgTrijetW_untagged, tau32);
      if (HT_modif > 900)
	{
	  hFatJB_LdgTrijet_Pt_ht900 -> Fill(isLdgTrijetW_untagged, FatJet_ldgFatJB.pt());
	  hFatJB_LdgTrijet_tau21_ht900 -> Fill(isLdgTrijetW_untagged, tau21);
	  hFatJB_LdgTrijet_tau32_ht900 -> Fill(isLdgTrijetW_untagged, tau32);
	}
    }
  
  // if (haveSubldgFatTop)
  // 	{
      // 	  hFatTop_SubldgTrijet_Pt -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	  hFatTop_SubldgTrijet_tau21 -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	  hFatTop_SubldgTrijet_tau32 -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	  if (HT_modif > 900)
      // 	    {
      // 	      hFatTop_SubldgTrijet_Pt_ht900 -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	      hFatTop_SubldgTrijet_tau21_ht900 -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	      hFatTop_SubldgTrijet_tau32_ht900 -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	    }
      // 	}
      // if (haveSubldgFatW)
      // 	{
      // 	  hFatW_SubldgTrijet_Pt   -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	  hFatW_SubldgTrijet_tau21   -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	  hFatW_SubldgTrijet_tau32   -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	  if (HT_modif > 900)
      // 	    {
      // 	      hFatW_SubldgTrijet_Pt_ht900   -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	      hFatW_SubldgTrijet_tau21_ht900   -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	      hFatW_SubldgTrijet_tau32_ht900   -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	    }
      // 	}
      // if (haveSubldgFatBJ)
      // 	{
      // 	  hFatJB_SubldgTrijet_Pt  -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	  hFatJB_SubldgTrijet_tau21  -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	  hFatJB_SubldgTrijet_tau32  -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	  if (HT_modif > 900)
      // 	    {
      // 	      hFatJB_SubldgTrijet_Pt_ht900  -> Fill(isSubldgTrijetW_untagged, FatJet.pt());
      // 	      hFatJB_SubldgTrijet_tau21_ht900  -> Fill(isSubldgTrijetW_untagged, tau21);
      // 	      hFatJB_SubldgTrijet_tau32_ht900  -> Fill(isSubldgTrijetW_untagged, tau32);
      // 	    }
      // 	}

      //NjettinessAK8CHStau1

  
  //===Definitions
  math::XYZTLorentzVector tetrajet_p4, subldgTetrajet_p4; 
  tetrajet_p4 = LdgTrijet.TrijetP4 + topData.getTetrajetBJet().p4();
  subldgTetrajet_p4 = SubldgTrijet.TrijetP4 + topData.getTetrajetBJet().p4();
  
  bool LdgTopIsTopFromH = false;
  bool SubldgTopIsTopFromH = false;
  if (haveMatchedTopFromChargedHiggs)  LdgTopIsTopFromH       = isRealMVATop(LdgTrijet.Jet1, LdgTrijet.Jet2, LdgTrijet.BJet, HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0));
  if (haveMatchedTopFromChargedHiggs)  SubldgTopIsTopFromH    = isRealMVATop(SubldgTrijet.Jet1, SubldgTrijet.Jet2, SubldgTrijet.BJet, HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0));

  double LdgTrijet_Rapidity = 0.5*log((LdgTrijet.TrijetP4.E() + LdgTrijet.TrijetP4.Pz())/(LdgTrijet.TrijetP4.E() - LdgTrijet.TrijetP4.Pz()));
  double SubldgTrijet_Rapidity = 0.5*log((SubldgTrijet.TrijetP4.E() + SubldgTrijet.TrijetP4.Pz())/(SubldgTrijet.TrijetP4.E() - SubldgTrijet.TrijetP4.Pz()));
  double TetrajetBjet_Rapidity = 0.5*log((topData.getTetrajetBJet().p4().E() + topData.getTetrajetBJet().p4().Pz())/(topData.getTetrajetBJet().p4().E() - topData.getTetrajetBJet().p4().Pz()));

  double dR12Ldg = ROOT::Math::VectorUtil::DeltaR(LdgTrijet.Jet1.p4(), LdgTrijet.Jet2.p4());
  double dR1bLdg = ROOT::Math::VectorUtil::DeltaR(LdgTrijet.Jet1.p4(), LdgTrijet.BJet.p4());
  double dR2bLdg = ROOT::Math::VectorUtil::DeltaR(LdgTrijet.Jet2.p4(), LdgTrijet.BJet.p4());

  double dRLdg_min = min(min(dR12Ldg, dR1bLdg), dR2bLdg);
  double dRLdg_max = max(max(dR12Ldg, dR1bLdg), dR2bLdg);

  double dR12Subldg = ROOT::Math::VectorUtil::DeltaR(SubldgTrijet.Jet1.p4(), SubldgTrijet.Jet2.p4());
  double dR1bSubldg = ROOT::Math::VectorUtil::DeltaR(SubldgTrijet.Jet1.p4(), SubldgTrijet.BJet.p4());
  double dR2bSubldg = ROOT::Math::VectorUtil::DeltaR(SubldgTrijet.Jet2.p4(), SubldgTrijet.BJet.p4());

  double dRSubldg_min = min(min(dR12Subldg, dR1bSubldg), dR2bSubldg);
  double dRSubldg_max = max(max(dR12Subldg, dR1bSubldg), dR2bSubldg);

  double deltaR_LdgTrijet_TetrajetBjet = ROOT::Math::VectorUtil::DeltaR(LdgTrijet.TrijetP4, topData.getTetrajetBJet().p4());
  double deltaR_SubldgTrijet_TetrajetBjet = ROOT::Math::VectorUtil::DeltaR(SubldgTrijet.TrijetP4, topData.getTetrajetBJet().p4());
  
  double deltaEta_LdgTrijet_TetrajetBjet = std::abs(LdgTrijet.TrijetP4.Eta() - topData.getTetrajetBJet().eta());
  double deltaEta_SubldgTrijet_TetrajetBjet = std::abs(SubldgTrijet.TrijetP4.Eta() - topData.getTetrajetBJet().eta());

  double deltaPhi_LdgTrijet_TetrajetBjet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(LdgTrijet.TrijetP4, topData.getTetrajetBJet().p4()));
  double deltaPhi_SubldgTrijet_TetrajetBjet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(SubldgTrijet.TrijetP4, topData.getTetrajetBJet().p4()));

  double deltaY_LdgTrijet_TetrajetBjet = std::abs(LdgTrijet_Rapidity - TetrajetBjet_Rapidity);
  double deltaY_SubldgTrijet_TetrajetBjet = std::abs(SubldgTrijet_Rapidity - TetrajetBjet_Rapidity);
  
  //Calculate the p_{T,rel}: p_{T,rel} = p_{T,b} - a*p_{T,t}, where a = p_{T,b}*p_{T,t}/(p_{T,t}*p_{T,t})

  double px_bt = LdgTrijet.TrijetP4.Px()*LdgTrijet.BJet.p4().Px();
  double py_bt = LdgTrijet.TrijetP4.Py()*LdgTrijet.BJet.p4().Py();
  double px_tt = LdgTrijet.TrijetP4.Px()*LdgTrijet.TrijetP4.Px();
  double py_tt = LdgTrijet.TrijetP4.Py()*LdgTrijet.TrijetP4.Py();
  
  double a_factor = (px_bt+py_bt)/(px_tt+py_tt);
  double px_proj = a_factor*LdgTrijet.TrijetP4.Px();
  double py_proj = a_factor*LdgTrijet.TrijetP4.Py();

  double px_rel = LdgTrijet.BJet.p4().Px() - px_proj;
  double py_rel = LdgTrijet.BJet.p4().Py() - py_proj;
  double pT_rel = sqrt(px_rel*px_rel + py_rel*py_rel);


  
  //===Definitions

  //===Fill Histograms


  hLdgTrijetPt         -> Fill(LdgTopIsTopFromH, LdgTrijet.TrijetP4.Pt());
  hLdgTrijetDijetPt    -> Fill(LdgTopIsTopFromH, topData.getLdgTrijetDijet().Pt());
  hSubldgTrijetPt      -> Fill(SubldgTopIsTopFromH, SubldgTrijet.TrijetP4.Pt());
  hSubldgTrijetDijetPt -> Fill(SubldgTopIsTopFromH, topData.getLdgTrijetDijet().Pt());



  hLdgTrijet_DeltaR_Trijet_TetrajetBjet      -> Fill(LdgTopIsTopFromH, deltaR_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet    -> Fill(LdgTopIsTopFromH, deltaEta_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet    -> Fill(LdgTopIsTopFromH, deltaPhi_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet      -> Fill(LdgTopIsTopFromH, deltaY_LdgTrijet_TetrajetBjet);
  
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet   -> Fill(SubldgTopIsTopFromH, deltaR_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet -> Fill(SubldgTopIsTopFromH, deltaEta_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet -> Fill(SubldgTopIsTopFromH, deltaPhi_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet   -> Fill(SubldgTopIsTopFromH, deltaY_SubldgTrijet_TetrajetBjet);
  
  hLdgTrijetJets_DeltaRmin     -> Fill(LdgTopIsTopFromH,    dRLdg_min);
  hSubldgTrijetJets_DeltaRmin  -> Fill(SubldgTopIsTopFromH, dRSubldg_min);
  hLdgTrijetJets_DeltaRmax     -> Fill(LdgTopIsTopFromH,    dRLdg_max);
  hSubldgTrijetJets_DeltaRmax  -> Fill(SubldgTopIsTopFromH, dRSubldg_max);
  
  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet      -> Fill(isBfromH, deltaR_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet    -> Fill(isBfromH, deltaEta_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet    -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet      -> Fill(isBfromH, deltaY_LdgTrijet_TetrajetBjet);
  
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet   -> Fill(isBfromH, deltaR_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet -> Fill(isBfromH, deltaEta_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet -> Fill(isBfromH, deltaPhi_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet   -> Fill(isBfromH, deltaY_SubldgTrijet_TetrajetBjet);

  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth      -> Fill(LdgTopIsTopFromH*isBfromH, deltaR_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth    -> Fill(LdgTopIsTopFromH*isBfromH, deltaEta_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth    -> Fill(LdgTopIsTopFromH*isBfromH, deltaPhi_LdgTrijet_TetrajetBjet);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth      -> Fill(LdgTopIsTopFromH*isBfromH, deltaY_LdgTrijet_TetrajetBjet);
  
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth   -> Fill(SubldgTopIsTopFromH*isBfromH, deltaR_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth -> Fill(SubldgTopIsTopFromH*isBfromH, deltaEta_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth -> Fill(SubldgTopIsTopFromH*isBfromH, deltaPhi_SubldgTrijet_TetrajetBjet);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth   -> Fill(SubldgTopIsTopFromH*isBfromH, deltaY_SubldgTrijet_TetrajetBjet);

  hTetrajetBjetBDisc -> Fill(isBfromH, topData.getTetrajetBJet().bjetDiscriminator());

  //Invariant Mass reconstruction
  //Boolean defines if tetrajetBjet is correctly identified
  hTetrajetMass -> Fill(isBfromH, tetrajet_p4.M());
  if (tetrajet_p4.M() < 800)  hTetrajetMass_M800            -> Fill(isBfromH, tetrajet_p4.M());
  if (LdgTopIsTopFromH)       hTetrajetMass_LdgTopIsHTop    -> Fill(isBfromH, tetrajet_p4.M());
  if (SubldgTopIsTopFromH)    hTetrajetMass_SubldgTopIsHTop -> Fill(isBfromH, subldgTetrajet_p4.M());

  bool passDeltaPhi_condition = deltaR_SubldgTrijet_TetrajetBjet >= -deltaR_LdgTrijet_TetrajetBjet + pi;
  if (passDeltaPhi_condition) hTetrajetMass_deltaPhiCond    -> Fill(tetrajet_p4.M());
  
  hTetrajetMass_isGenuineB -> Fill(bjetData.isGenuineB(), tetrajet_p4.M());
  
  hTetrajetPtDPhi -> Fill (isBfromH, tetrajet_p4.Pt()*deltaPhi_LdgTrijet_TetrajetBjet);
  if (LdgTopIsTopFromH)       hTetrajetPtDPhi_LdgTopIsHTop -> Fill(isBfromH, tetrajet_p4.Pt()*deltaPhi_LdgTrijet_TetrajetBjet);
  if (tetrajet_p4.M() < 800)  hTetrajetPtDPhi_M800         -> Fill(isBfromH, tetrajet_p4.Pt()*deltaPhi_LdgTrijet_TetrajetBjet);
  hTetrajetPtDPhi_isGenuineB                               -> Fill(bjetData.isGenuineB(), tetrajet_p4.Pt()*deltaPhi_LdgTrijet_TetrajetBjet);

  hTetrajetPtDR -> Fill (isBfromH, tetrajet_p4.Pt()*deltaR_LdgTrijet_TetrajetBjet);
  if (LdgTopIsTopFromH)       hTetrajetPtDR_LdgTopIsHTop -> Fill(isBfromH, tetrajet_p4.Pt()*deltaR_LdgTrijet_TetrajetBjet);
  if (tetrajet_p4.M() < 800)  hTetrajetPtDR_M800         -> Fill(isBfromH, tetrajet_p4.Pt()*deltaR_LdgTrijet_TetrajetBjet);
  hTetrajetPtDR_isGenuineB                               -> Fill(bjetData.isGenuineB(), tetrajet_p4.Pt()*deltaR_LdgTrijet_TetrajetBjet);

  //===Fill TH2 Histograms

  hLdgTrijetPt_Vs_TetrajetPt             -> Fill(topData.getLdgTrijet().Pt()    ,                topData.getLdgTetrajet().Pt());
  hSubldgTrijetPt_Vs_TetrajetPt          -> Fill(topData.getSubldgTrijet().Pt() ,                topData.getLdgTetrajet().Pt());

  hLdgTrijetDijetPt_Vs_TetrajetPt        -> Fill(topData.getLdgTrijetDijet().Pt()    ,           topData.getLdgTetrajet().Pt());
  hSubldgTrijetDijetPt_Vs_TetrajetPt     -> Fill(topData.getSubldgTrijetDijet().Pt() ,           topData.getLdgTetrajet().Pt());

  hLdgTrijetPt_Vs_TetrajetBjetPt         -> Fill(isBfromH, topData.getLdgTrijet().Pt()    ,      topData.getTetrajetBJet().pt());
  hSubldgTrijetPt_Vs_TetrajetBjetPt      -> Fill(isBfromH, topData.getSubldgTrijet().Pt() ,      topData.getTetrajetBJet().pt());

  hLdgTrijetDijetPt_Vs_TetrajetBjetPt    -> Fill(isBfromH, topData.getLdgTrijetDijet().Pt()    , topData.getTetrajetBJet().pt());
  hSubldgTrijetDijetPt_Vs_TetrajetBjetPt -> Fill(isBfromH, topData.getSubldgTrijetDijet().Pt() , topData.getTetrajetBJet().pt());

  hLdgTrijetJets_DeltaRmin_Vs_BDT    -> Fill(LdgTopIsTopFromH, dRLdg_min, topData.getLdgTrijetMVA());
  hLdgTrijetJets_DeltaRmin_Vs_Pt     -> Fill(LdgTopIsTopFromH, dRLdg_min, LdgTrijet.TrijetP4.Pt());
  hLdgTrijetJets_DeltaRmax_Vs_BDT    -> Fill(LdgTopIsTopFromH, dRLdg_max, topData.getLdgTrijetMVA());
  hLdgTrijetJets_DeltaRmax_Vs_Pt     -> Fill(LdgTopIsTopFromH, dRLdg_max, LdgTrijet.TrijetP4.Pt());

  hSubldgTrijetJets_DeltaRmin_Vs_BDT -> Fill(SubldgTopIsTopFromH, dRSubldg_min, topData.getSubldgTrijetMVA());
  hSubldgTrijetJets_DeltaRmin_Vs_Pt  -> Fill(SubldgTopIsTopFromH, dRSubldg_min, SubldgTrijet.TrijetP4.Pt());
  hSubldgTrijetJets_DeltaRmax_Vs_BDT -> Fill(SubldgTopIsTopFromH, dRSubldg_max, topData.getSubldgTrijetMVA());
  hSubldgTrijetJets_DeltaRmax_Vs_Pt  -> Fill(SubldgTopIsTopFromH, dRSubldg_max, SubldgTrijet.TrijetP4.Pt());

  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet    -> Fill(isBfromH, deltaR_LdgTrijet_TetrajetBjet,   deltaR_SubldgTrijet_TetrajetBjet);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet  -> Fill(isBfromH, deltaEta_LdgTrijet_TetrajetBjet, deltaEta_SubldgTrijet_TetrajetBjet);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet    -> Fill(isBfromH, deltaY_LdgTrijet_TetrajetBjet,   deltaY_SubldgTrijet_TetrajetBjet);


  hLdgTrijetBjet_PtRel -> Fill(isBfromH, pT_rel);

  // if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.01*0.01)
  //   {
  //     hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
  //   }

  //  if (deltaPhi_LdgTrijet_TetrajetBjet > 1. && deltaPhi_SubldgTrijet_TetrajetBjet < 1.)
  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 1*1)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

    //  if (deltaPhi_LdgTrijet_TetrajetBjet > 2. && deltaPhi_SubldgTrijet_TetrajetBjet < 2.)
  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 2*2)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }


  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 1.5*1.5)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_1p5  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

    //  if (deltaPhi_LdgTrijet_TetrajetBjet > 2. && deltaPhi_SubldgTrijet_TetrajetBjet < 2.)
  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 2.5*2.5)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_2p5  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }


  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.1*0.1)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p1  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

    //  if (deltaPhi_LdgTrijet_TetrajetBjet > 2. && deltaPhi_SubldgTrijet_TetrajetBjet < 2.)
  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.2*0.2)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p2  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.3*0.3)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p3  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

    //  if (deltaPhi_LdgTrijet_TetrajetBjet > 2. && deltaPhi_SubldgTrijet_TetrajetBjet < 2.)
  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.4*0.4)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p4  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }

  if ((deltaPhi_LdgTrijet_TetrajetBjet - 3.15)*(deltaPhi_LdgTrijet_TetrajetBjet - 3.15) + deltaPhi_SubldgTrijet_TetrajetBjet*deltaPhi_SubldgTrijet_TetrajetBjet >= 0.5*0.5)
    {
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_0p5  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
    }


  //  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);

  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth    -> Fill(LdgTopIsTopFromH*isBfromH, deltaR_LdgTrijet_TetrajetBjet,   deltaR_SubldgTrijet_TetrajetBjet);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth  -> Fill(LdgTopIsTopFromH*isBfromH, deltaEta_LdgTrijet_TetrajetBjet, deltaEta_SubldgTrijet_TetrajetBjet);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth  -> Fill(LdgTopIsTopFromH*isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth    -> Fill(LdgTopIsTopFromH*isBfromH, deltaY_LdgTrijet_TetrajetBjet,   deltaY_SubldgTrijet_TetrajetBjet);  
  //===Fill Histograms

  if (tetrajet_p4.M() < 800)
    {
      hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800    -> Fill(isBfromH, deltaR_LdgTrijet_TetrajetBjet,   deltaR_SubldgTrijet_TetrajetBjet);
      hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800  -> Fill(isBfromH, deltaEta_LdgTrijet_TetrajetBjet, deltaEta_SubldgTrijet_TetrajetBjet);
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800  -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
      hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_M800    -> Fill(isBfromH, deltaY_LdgTrijet_TetrajetBjet,   deltaY_SubldgTrijet_TetrajetBjet);
      
      hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800    -> Fill(LdgTopIsTopFromH*isBfromH, deltaR_LdgTrijet_TetrajetBjet,   deltaR_SubldgTrijet_TetrajetBjet);
      hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800  -> Fill(LdgTopIsTopFromH*isBfromH, deltaEta_LdgTrijet_TetrajetBjet, deltaEta_SubldgTrijet_TetrajetBjet);
      hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800  -> Fill(LdgTopIsTopFromH*isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
      hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_trueBoth_M800    -> Fill(LdgTopIsTopFromH*isBfromH, deltaY_LdgTrijet_TetrajetBjet,   deltaY_SubldgTrijet_TetrajetBjet);  
    }

  //if (bjetData.isGenuineB)
  hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB    -> Fill(bjetData.isGenuineB(), deltaR_LdgTrijet_TetrajetBjet,   deltaR_SubldgTrijet_TetrajetBjet);
  hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB  -> Fill(bjetData.isGenuineB(), deltaEta_LdgTrijet_TetrajetBjet, deltaEta_SubldgTrijet_TetrajetBjet);
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB  -> Fill(bjetData.isGenuineB(), deltaPhi_LdgTrijet_TetrajetBjet, deltaPhi_SubldgTrijet_TetrajetBjet);
  hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet_isGenuineB    -> Fill(bjetData.isGenuineB(), deltaY_LdgTrijet_TetrajetBjet,   deltaY_SubldgTrijet_TetrajetBjet);
      
  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, tetrajet_p4.Pt());
  if (tetrajet_p4.M() < 800)  hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_M800 -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, tetrajet_p4.Pt());
  if (LdgTopIsTopFromH)       hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_TetrajetPt_LdgTopIsHTop -> Fill(isBfromH, deltaPhi_LdgTrijet_TetrajetBjet, tetrajet_p4.Pt());


  hCEvts_closeJetToTetrajetBjet_isBTagged ->  Fill("untagged", 0);
  hCEvts_closeJetToTetrajetBjet_isBTagged ->  Fill("btagged", 0);
  
  bool foundJetCloseToTetrajetBjet = false;
  for (auto& jet: jetData.getSelectedJets())
    {
      if (areSameJets(jet, topData.getTetrajetBJet())) continue;
      if (areSameJets(jet, LdgTrijet.Jet1) || areSameJets(jet, LdgTrijet.Jet2) || areSameJets(jet, LdgTrijet.BJet)) continue;
      if (areSameJets(jet, SubldgTrijet.Jet1) || areSameJets(jet, SubldgTrijet.Jet2) || areSameJets(jet, SubldgTrijet.BJet)) continue;
      double deltaPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(jet.p4(), topData.getTetrajetBJet()));
      if (deltaPhi >= 0.8) continue;
      foundJetCloseToTetrajetBjet = true;
      if (jet.bjetDiscriminator() > 0.8484) hCEvts_closeJetToTetrajetBjet_isBTagged ->  Fill("btagged", 1);
      else hCEvts_closeJetToTetrajetBjet_isBTagged ->  Fill("untagged", 1);
      //      std::cout<<jet.bjetDiscriminator()<<std::endl;
      
      if (foundJetCloseToTetrajetBjet) hTetrajetMass_closeJetToTetrajetBjet -> Fill(jet.bjetDiscriminator() > 0.8484, tetrajet_p4.M());
    }

  

  
 //================================================================================================
  // Fill final plots
  //===============================================================================================
  //fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, 1);
 
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
