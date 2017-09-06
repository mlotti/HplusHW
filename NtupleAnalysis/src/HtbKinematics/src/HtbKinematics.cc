// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

// User
#include "Auxiliary/interface/Table.h"
#include "Auxiliary/interface/Tools.h"
#include "Tools/interface/MCTools.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

// ROOT
#include "TDirectory.h"
#include "Math/VectorUtil.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"

struct PtComparator
{
  bool operator() (const genParticle p1, const genParticle p2) const { return ( p1.pt() > p2.pt() ); }
  bool operator() (const math::XYZTLorentzVector p1, const math::XYZTLorentzVector p2) const { return ( p1.pt() > p2.pt() ); }
};


class HtbKinematics: public BaseSelector {
public:
  explicit HtbKinematics(const ParameterSet& config, const TH1* skimCounters);
  virtual ~HtbKinematics() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
  virtual vector<genParticle> GetGenParticles(const vector<genParticle> genParticles, double ptCut, double etaCut, const int pdgId, const bool isLastCopy=true, const bool hasNoDaughters=false);
  virtual vector<GenJet> GetGenJets(const GenJetCollection& genJets, std::vector<float> ptCut, std::vector<float> etaCut);
  virtual vector<GenJet> GetGenJets(const vector<GenJet> genJets, std::vector<float> ptCut, std::vector<float> etaCut, vector<genParticle> genParticlesToMatch);
  virtual TMatrixDSym ComputeMomentumTensor(std::vector<math::XYZTLorentzVector> jets, double r = 2.0); 
  virtual TMatrixDSym ComputeMomentumTensor2D(std::vector<math::XYZTLorentzVector> jets);
  virtual vector<float> GetMomentumTensorEigenValues(std::vector<math::XYZTLorentzVector> jets,
						     float &C,
						     float &D,
						     float &H2);
  virtual vector<float> GetMomentumTensorEigenValues2D(std::vector<math::XYZTLorentzVector> jets, 
						       float &Circularity);
  virtual vector<float> GetSphericityTensorEigenValues(std::vector<math::XYZTLorentzVector> jets,
						       float &y23, float &Sphericity, float &SphericityT, float &Aplanarity, float &Planarity, float &Y);
  virtual double GetAlphaT(std::vector<math::XYZTLorentzVector> jets,
			   float &HT,
			   float &JT,
			   float &MHT,
			   float &Centrality);

   
private:
  // Input parameters
  const double cfg_Verbose;
  const ParameterSet PSet_ElectronSelection;
  const double cfg_ElectronPtCut;
  const double cfg_ElectronEtaCut;
  const ParameterSet PSet_MuonSelection;
  const double cfg_MuonPtCut;
  const double cfg_MuonEtaCut;
  const ParameterSet PSet_TauSelection;
  const double cfg_TauPtCut;
  const double cfg_TauEtaCut;
  const ParameterSet PSet_JetSelection;
  const std::vector<float> cfg_JetPtCuts;
  const std::vector<float> cfg_JetEtaCuts;
  const DirectionalCut<int> cfg_JetNumberCut;
  const ParameterSet PSet_HtSelection;
  const DirectionalCut<float> cfg_HtCut;
  const ParameterSet PSet_BJetSelection;
  const std::vector<float> cfg_BJetPtCuts;
  const std::vector<float> cfg_BJetEtaCuts;
  const DirectionalCut<int> cfg_BJetNumberCut;
  // METSelection PSet_METSelection;
  TopologySelection PSet_TopologySelection;
  const DirectionalCut<double> cfg_SphericityCut;
  const DirectionalCut<double> cfg_AplanarityCut;
  const DirectionalCut<double> cfg_PlanarityCut;
  const DirectionalCut<double> cfg_CircularityCut;
  const DirectionalCut<double> cfg_Y23Cut;
  const DirectionalCut<double> cfg_CparameterCut;
  const DirectionalCut<double> cfg_DparameterCut;
  const DirectionalCut<double> cfg_FoxWolframMomentCut;
  const DirectionalCut<double> cfg_AlphaTCut;
  const DirectionalCut<double> cfg_CentralityCut;
  // TopSelection PSet_TopSelection;
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;
  const HistogramSettings cfg_PhiBinSetting;
  const HistogramSettings cfg_MassBinSetting;
  const HistogramSettings cfg_DeltaEtaBinSetting;
  const HistogramSettings cfg_DeltaPhiBinSetting;
  const HistogramSettings cfg_DeltaRBinSetting;
  /*
  const ParameterSet PSet_JetSelection;
  const double cfg_JetPtCut;
  const double cfg_JetEtaCut;
  const DirectionalCut<int> cfg_JetNumberCut;
  const ParameterSet PSet_ElectronSelection;
  const double cfg_ElectronPtCut;
  const double cfg_ElectronEtaCut;
  const DirectionalCut<int> cfg_ElectronNumberCut;
  const ParameterSet PSet_MuonSelection;
  const double cfg_MuonPtCut;
  const double cfg_MuonEtaCut;
  const DirectionalCut<int> cfg_MuonNumberCut;
  const ParameterSet PSet_HtSelection;
  const DirectionalCut<float> cfg_HtCut;
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;
  const HistogramSettings cfg_PhiBinSetting;
  const HistogramSettings cfg_MassBinSetting;
  const HistogramSettings cfg_DeltaEtaBinSetting;
  const HistogramSettings cfg_DeltaPhiBinSetting;
  const HistogramSettings cfg_DeltaRBinSetting;
  */
  
  Tools auxTools;
  
  // Event Counters
  Count cAllEvents;  
  Count cTrigger;
  Count cElectronVeto;
  Count cMuonVeto;
  Count cTauVeto;
  Count cJetSelection;
  Count cBJetSelection;
  Count cTopologySelection;
  Count cTopSelection;
  Count cSelected;
  // BR Counters
  Count cInclusive;
  Count cHtb_HPlus;
  Count cHtb_TQuark;
  Count cHtb_BQuark;
  Count cHtb_tbW_BQuark;
  Count cHtb_tbW_WBoson;
  Count cHtb_tbW_Wqq_Quark;
  Count cHtb_tbW_Wqq_AntiQuark;
  Count cHtb_tbW_Wqq_Leptons;
  Count cgtt_TQuark;
  Count cgbb_BQuark;
  Count cgtt_tbW_Wqq_Quark;
  Count cgtt_tbW_Wqq_AntiQuark;
  Count cgtt_tbW_Wqq_Leptons;
  Count cgtt_tbW_WBoson;
  Count cgtt_tbW_BQuark;

  // Event Variables
  WrappedTH1 *h_genMET_Et;
  WrappedTH1 *h_genMET_Phi;
  WrappedTH1 *h_genHT_GenParticles;
  WrappedTH1 *h_genHT_GenJets;  
  
  // GenParticles
  WrappedTH1 *h_gtt_TQuark_Pt;
  WrappedTH1 *h_gtt_tbW_WBoson_Pt;
  WrappedTH1 *h_gtt_tbW_BQuark_Pt;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Pt;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Pt;
  WrappedTH1 *h_tbH_HPlus_Pt;
  WrappedTH1 *h_tbH_TQuark_Pt;
  WrappedTH1 *h_tbH_BQuark_Pt;
  WrappedTH1 *h_tbH_tbW_WBoson_Pt;
  WrappedTH1 *h_tbH_tbW_BQuark_Pt;
  WrappedTH1 *h_gbb_BQuark_Pt;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Pt;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Pt;
  //
  WrappedTH1 *h_gtt_TQuark_Eta;
  WrappedTH1 *h_gtt_tbW_WBoson_Eta;
  WrappedTH1 *h_gtt_tbW_BQuark_Eta;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Eta;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Eta;  
  WrappedTH1 *h_tbH_HPlus_Eta;
  WrappedTH1 *h_tbH_TQuark_Eta;
  WrappedTH1 *h_tbH_BQuark_Eta;
  WrappedTH1 *h_tbH_tbW_WBoson_Eta;
  WrappedTH1 *h_tbH_tbW_BQuark_Eta;
  WrappedTH1 *h_gbb_BQuark_Eta;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Eta;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Eta;
  //
  WrappedTH1 *h_gtt_TQuark_Rap;
  WrappedTH1 *h_gtt_tbW_WBoson_Rap;
  WrappedTH1 *h_gtt_tbW_BQuark_Rap;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Rap;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Rap;  
  WrappedTH1 *h_tbH_HPlus_Rap;
  WrappedTH1 *h_tbH_TQuark_Rap;
  WrappedTH1 *h_tbH_BQuark_Rap;
  WrappedTH1 *h_tbH_tbW_WBoson_Rap;
  WrappedTH1 *h_tbH_tbW_BQuark_Rap;
  WrappedTH1 *h_gbb_BQuark_Rap;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Rap;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Rap;
  //  
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dR;
  //
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dEta;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dEta;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dEta;
  //
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dPhi;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dPhi;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dPhi;
  //  
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dRap;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dRap;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dRap;
  //  
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  //
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_BQuark_dR;
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_tbW_WBoson_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_tbW_WBoson_gbb_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_WBoson_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_WBoson_gbb_BQuark_dR;
  //
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_BQuark_dEta;
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_tbW_BQuark_dEta;
  WrappedTH1 *h_Htb_tbW_WBoson_gtt_tbW_BQuark_dEta;
  WrappedTH1 *h_Htb_tbW_WBoson_gbb_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_tbW_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_WBoson_gtt_tbW_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_WBoson_gbb_BQuark_dEta;
  //
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_BQuark_dPhi;
  WrappedTH1 *h_Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi;
  WrappedTH1 *h_Htb_tbW_WBoson_gtt_tbW_BQuark_dPhi;
  WrappedTH1 *h_Htb_tbW_WBoson_gbb_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_WBoson_Htb_tbW_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_WBoson_gtt_tbW_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_WBoson_gbb_BQuark_dPhi;
  //
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dR;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR;
  //
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dEta;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dEta;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta;
  //
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dPhi;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dPhi;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi;
  //  
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dRap;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dRap;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dRap;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap;

  // GenParticles: BQuarks
  WrappedTH1 *h_BQuark1_Pt;
  WrappedTH1 *h_BQuark2_Pt;
  WrappedTH1 *h_BQuark3_Pt;
  WrappedTH1 *h_BQuark4_Pt;
  //
  WrappedTH1 *h_BQuark1_Eta;
  WrappedTH1 *h_BQuark2_Eta;
  WrappedTH1 *h_BQuark3_Eta;
  WrappedTH1 *h_BQuark4_Eta;
  // GenParticles: BQuarks pair closest together
  WrappedTH1 *h_BQuarkPair_dRMin_pT;
  WrappedTH1 *h_BQuarkPair_dRMin_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_Mass;
  WrappedTH2 *h_BQuarkPair_dRMin_Eta1_Vs_Eta2;
  WrappedTH2 *h_BQuarkPair_dRMin_Phi1_Vs_Phi2;
  WrappedTH2 *h_BQuarkPair_dRMin_Pt1_Vs_Pt2;
  WrappedTH2 *h_BQuarkPair_dRMin_dEta_Vs_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dPhi;

  // GenParticles: bqq trijet system (H+)
  WrappedTH1 *h_Htb_tbW_bqq_Pt;
  WrappedTH1 *h_Htb_tbW_bqq_Rap;
  WrappedTH1 *h_Htb_tbW_bqq_Mass;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dR;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dRap;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dPhi;
  WrappedTH2 *h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi;

  // GenParticles: bqq trijet system (associated top)
  WrappedTH1 *h_gtt_tbW_bqq_Pt;
  WrappedTH1 *h_gtt_tbW_bqq_Rap;
  WrappedTH1 *h_gtt_tbW_bqq_Mass;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dR;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dRap;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dPhi;
  WrappedTH2 *h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi;

  // GenJets
  WrappedTH1 *h_GenJets_N;  
  WrappedTH1 *h_GenJet1_Pt;
  WrappedTH1 *h_GenJet2_Pt;
  WrappedTH1 *h_GenJet3_Pt;
  WrappedTH1 *h_GenJet4_Pt;
  WrappedTH1 *h_GenJet5_Pt;
  WrappedTH1 *h_GenJet6_Pt;
  //
  WrappedTH1 *h_GenJet1_Eta;
  WrappedTH1 *h_GenJet2_Eta;
  WrappedTH1 *h_GenJet3_Eta;
  WrappedTH1 *h_GenJet4_Eta;
  WrappedTH1 *h_GenJet5_Eta;
  WrappedTH1 *h_GenJet6_Eta;

  // tt system
  WrappedTH1 *h_tt_Pt;
  WrappedTH1 *h_tt_Eta;
  WrappedTH1 *h_tt_Rap; 
  WrappedTH1 *h_tt_Mass;

  // GenJets: Dijet with largest mass
  WrappedTH1 *h_MaxDiJetMass_Pt;
  WrappedTH1 *h_MaxDiJetMass_Eta;
  WrappedTH1 *h_MaxDiJetMass_Rap; 
  WrappedTH1 *h_MaxDiJetMass_Mass;
  WrappedTH1 *h_MaxDiJetMass_dR;
  WrappedTH1 *h_MaxDiJetMass_dRrap;
  WrappedTH1 *h_MaxDiJetMass_dEta;
  WrappedTH1 *h_MaxDiJetMass_dPhi;
  WrappedTH1 *h_MaxDiJetMass_dRap;
  WrappedTH2 *h_MaxDiJetMass_dEta_Vs_dPhi;
  WrappedTH2 *h_MaxDiJetMass_dRap_Vs_dPhi;  

  // Correlations 
  WrappedTH2 *h_BQuark1_BQuark2_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark3_BQuark4_dEta_Vs_dPhi;

  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta;
  WrappedTH2 *h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi;  
  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass;
  WrappedTH2 *h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(HtbKinematics);

HtbKinematics::HtbKinematics(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_Verbose(config.getParameter<bool>("verbose")),
    PSet_ElectronSelection(config.getParameter<ParameterSet>("ElectronSelection")),
    cfg_ElectronPtCut(config.getParameter<float>("ElectronSelection.electronPtCut")),  
    cfg_ElectronEtaCut(config.getParameter<float>("ElectronSelection.electronEtaCut")),
    PSet_MuonSelection(config.getParameter<ParameterSet>("MuonSelection")),
    cfg_MuonPtCut(config.getParameter<float>("MuonSelection.muonPtCut")),
    cfg_MuonEtaCut(config.getParameter<float>("MuonSelection.muonEtaCut")),
    PSet_TauSelection(config.getParameter<ParameterSet>("TauSelection")),
    cfg_TauPtCut(config.getParameter<float>("TauSelection.tauPtCut")),
    cfg_TauEtaCut(config.getParameter<float>("TauSelection.tauEtaCut")),
    PSet_JetSelection(config.getParameter<ParameterSet>("JetSelection")),
    cfg_JetPtCuts(config.getParameter<std::vector<float>>("JetSelection.jetPtCuts")),
    cfg_JetEtaCuts(config.getParameter<std::vector<float>>("JetSelection.jetEtaCuts")),
    cfg_JetNumberCut(config, "JetSelection.numberOfJetsCut"),
    PSet_HtSelection(config.getParameter<ParameterSet>("JetSelection")),
    cfg_HtCut(config, "JetSelection.HTCut"),
    PSet_BJetSelection(config.getParameter<ParameterSet>("BJetSelection")),
    cfg_BJetPtCuts(config.getParameter<std::vector<float>>("BJetSelection.jetPtCuts")),
    cfg_BJetEtaCuts(config.getParameter<std::vector<float>>("BJetSelection.jetEtaCuts")),
    cfg_BJetNumberCut(config, "BJetSelection.numberOfBJetsCut"),
    // PSet_METSelection(config.getParameter<ParameterSet>("METSelection")),
    PSet_TopologySelection(config.getParameter<ParameterSet>("TopologySelection")),
    cfg_SphericityCut(config, "TopologySelection.SphericityCut"),
    cfg_AplanarityCut(config, "TopologySelection.AplanarityCut"),
    cfg_PlanarityCut(config, "TopologySelection.PlanarityCut"),
    cfg_CircularityCut(config, "TopologySelection.CircularityCut"),
    cfg_Y23Cut(config, "TopologySelection.Y23Cut"),
    cfg_CparameterCut(config, "TopologySelection.CparameterCut"),
    cfg_DparameterCut(config, "TopologySelection.DparameterCut"),
    cfg_FoxWolframMomentCut(config, "TopologySelection.FoxWolframMomentCut"),
    cfg_AlphaTCut(config, "TopologySelection.AlphaTCut"),
    cfg_CentralityCut(config, "TopologySelection.CentralityCut"),
    // PSet_TopSelection(config.getParameter<ParameterSet>("TopSelection")),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invMassBins")),
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Trigger")),
    cElectronVeto(fEventCounter.addCounter("e-veto")),
    cMuonVeto(fEventCounter.addCounter("#mu-veto")),
    cTauVeto(fEventCounter.addCounter("#tau-veto")),
    cJetSelection(fEventCounter.addCounter("Jets + H_{T}")),
    cBJetSelection(fEventCounter.addCounter("b-jets")),
    cTopologySelection(fEventCounter.addCounter("Topology")),
    cTopSelection(fEventCounter.addCounter("Top")),
    cSelected(fEventCounter.addCounter("All Selections")),
    cInclusive(fEventCounter.addSubCounter("Branching", "All events")),
    cHtb_HPlus(fEventCounter.addSubCounter("Branching", "H+")),
    cHtb_TQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t")),
    cHtb_BQuark(fEventCounter.addSubCounter("Branching", "H+->tb, b")),
    cHtb_tbW_BQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, b")),
    cHtb_tbW_WBoson(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W+")),
    cHtb_tbW_Wqq_Quark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->qq, q")),
    cHtb_tbW_Wqq_AntiQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->qq, qbar")),
    cHtb_tbW_Wqq_Leptons(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->l v")),
    cgtt_TQuark(fEventCounter.addSubCounter("Branching", "g->tt, t")),
    cgbb_BQuark(fEventCounter.addSubCounter("Branching", "g->bb, b")),
    cgtt_tbW_Wqq_Quark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->qq, q")),
    cgtt_tbW_Wqq_AntiQuark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->qq, qbar")),
    cgtt_tbW_Wqq_Leptons(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->l v")),
    cgtt_tbW_WBoson(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W")),
    cgtt_tbW_BQuark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, b"))
{ }

void HtbKinematics::book(TDirectory *dir) {

  // Fixed binning
  const int nBinsPt   = 4*cfg_PtBinSetting.bins();
  const double minPt  = cfg_PtBinSetting.min();
  const double maxPt  = 4*cfg_PtBinSetting.max();

  const int nBinsEta  = 2*cfg_EtaBinSetting.bins();
  const double minEta = cfg_EtaBinSetting.min();
  const double maxEta = 2*cfg_EtaBinSetting.max();

  const int nBinsRap  = cfg_EtaBinSetting.bins();
  const double minRap = cfg_EtaBinSetting.min();
  const double maxRap = cfg_EtaBinSetting.max();

  const int nBinsPhi  = cfg_PhiBinSetting.bins();
  const double minPhi = cfg_PhiBinSetting.min();
  const double maxPhi = cfg_PhiBinSetting.max();

  const int nBinsM  = cfg_MassBinSetting.bins();
  const double minM = cfg_MassBinSetting.min();
  const double maxM = cfg_MassBinSetting.max();
  
  const int nBinsdEta  = 2*cfg_DeltaEtaBinSetting.bins();
  const double mindEta = cfg_DeltaEtaBinSetting.min();
  const double maxdEta = 2*cfg_DeltaEtaBinSetting.max();

  const int nBinsdRap  = 2*cfg_DeltaEtaBinSetting.bins();
  const double mindRap = cfg_DeltaEtaBinSetting.min();
  const double maxdRap = 2*cfg_DeltaEtaBinSetting.max();

  const int nBinsdPhi  = cfg_DeltaPhiBinSetting.bins();
  const double mindPhi = cfg_DeltaPhiBinSetting.min();
  const double maxdPhi = cfg_DeltaPhiBinSetting.max();

  const int nBinsdR  = 2*cfg_DeltaRBinSetting.bins();
  const double mindR = cfg_DeltaRBinSetting.min();
  const double maxdR = cfg_DeltaRBinSetting.max();

  TDirectory* th1 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "TH1");
  TDirectory* th2 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "TH2");
    
  // Event Variables
  h_genMET_Et         =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "genMET_Et"         , ";E_{T}^{miss} (GeV)", 1000,  0.0,   +500.0);
  h_genMET_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, th1, "genMET_Phi"  , ";#phi (rads)"       , nBinsPhi, minPhi, maxPhi);
  h_genHT_GenParticles=  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "genHT_GenParticles", ";GenP H_{T} (GeV)"  , nBinsM, minM, maxM   );
  h_genHT_GenJets     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "genHT_GenJets"     , ";GenJ H_{T} (GeV)"  , nBinsM, minM, maxM   );

  // GenParticles  
  h_gtt_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_Quark_Pt"    , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_AntiQuark_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_HPlus_Pt             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_HPlus_Pt"            , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_TQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_BQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_WBoson_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_BQuark_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gbb_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gbb_BQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_Htb_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_Quark_Pt"    , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_Htb_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_AntiQuark_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  //
  h_gtt_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_Quark_Eta"    , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_AntiQuark_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_HPlus_Eta             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_HPlus_Eta"            , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_TQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_BQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_WBoson_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_BQuark_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gbb_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gbb_BQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_Htb_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_Quark_Eta"    , ";#eta", nBinsEta, minEta, maxEta);
  h_Htb_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_AntiQuark_Eta", ";#eta", nBinsEta, minEta, maxEta);
  //
  h_gtt_TQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_Rap"           , ";#omega", nBinsRap, minRap, maxRap);
  h_gtt_tbW_WBoson_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_BQuark_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_Wqq_Quark_Rap     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_Quark_Rap"    , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_Wqq_AntiQuark_Rap =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_Wqq_AntiQuark_Rap", ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_HPlus_Rap             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_HPlus_Rap"            , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_TQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_TQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_BQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_BQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_tbW_WBoson_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_WBoson_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_tbW_BQuark_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tbH_tbW_BQuark_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gbb_BQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gbb_BQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_Htb_tbW_Wqq_Quark_Rap     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_Quark_Rap"    , ";#omega", nBinsEta, minRap, maxRap);
  h_Htb_tbW_Wqq_AntiQuark_Rap =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_Wqq_AntiQuark_Rap", ";#omega", nBinsEta, minRap, maxRap);
  // 
  h_Htb_TQuark_Htb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_Htb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_TQuark_gtt_TQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gtt_TQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gbb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_BQuark_dR"           , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_Quark_dR"        , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gbb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gtt_tbW_BQuark_dR"           , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_WBoson_Htb_BQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_BQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_tbW_BQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gtt_tbW_BQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_WBoson_gbb_BQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gbb_BQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_WBoson_Htb_BQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_BQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_tbW_BQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gtt_tbW_BQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_WBoson_gbb_BQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gbb_BQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  // 
  h_Htb_TQuark_Htb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_Htb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_TQuark_gtt_TQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gtt_TQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_TQuark_gbb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gbb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_BQuark_dEta            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_BQuark_dEta"           , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_Quark_dEta"        , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_TQuark_gbb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gbb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_TQuark_gtt_tbW_BQuark_dEta            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gtt_tbW_BQuark_dEta"           , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);

  h_Htb_tbW_WBoson_Htb_BQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_BQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_tbW_BQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gtt_tbW_BQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_WBoson_gbb_BQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gbb_BQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_WBoson_Htb_BQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_BQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_tbW_BQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gtt_tbW_BQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_WBoson_gbb_BQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gbb_BQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //
  h_Htb_TQuark_Htb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_Htb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_TQuark_gtt_TQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gtt_TQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_TQuark_gbb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gbb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_BQuark_dPhi           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_BQuark_dPhi"           ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi"        ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi",";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_TQuark_gbb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gbb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_TQuark_gtt_tbW_BQuark_dPhi           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gtt_tbW_BQuark_dPhi"           ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi",";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_WBoson_Htb_BQuark_dPhi     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_BQuark_dPhi"    , ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gtt_tbW_BQuark_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_WBoson_gbb_BQuark_dPhi     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_WBoson_gbb_BQuark_dPhi"    , ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_WBoson_Htb_BQuark_dPhi     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_BQuark_dPhi"    , ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_Htb_tbW_BQuark_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gtt_tbW_BQuark_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_WBoson_gbb_BQuark_dPhi     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_WBoson_gbb_BQuark_dPhi"    , ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  //
  h_Htb_TQuark_Htb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_Htb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_TQuark_gtt_TQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gtt_TQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_TQuark_gbb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_TQuark_gbb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_BQuark_dRap            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_BQuark_dRap"           , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_Quark_dRap"        , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap", ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_TQuark_gbb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gbb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_TQuark_gtt_tbW_BQuark_dRap            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_TQuark_gtt_tbW_BQuark_dRap"           , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap", ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  
  // GenParticles: B-quarks
  h_BQuark1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark1_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark2_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark3_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark4_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);

  h_BQuark1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuark4_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // GenParticles: BQuarks pair closest together
  h_BQuarkPair_dRMin_pT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_pT"  , ";p_{T} (GeV/c)"     ,  nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_Mass", ";M (GeV/c^{2})"     ,  nBinsM, minM, maxM);
  //
  h_BQuarkPair_dRMin_Eta1_Vs_Eta2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuarkPair_dRMin_Eta1_Vs_Eta2", ";#eta;#eta", nBinsEta, minEta, maxEta, nBinsEta, minEta, maxEta);
  h_BQuarkPair_dRMin_Phi1_Vs_Phi2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuarkPair_dRMin_Phi1_Vs_Phi2", ";#phi;#phi", nBinsPhi, minPhi, maxPhi, nBinsPhi, minPhi, maxPhi);
  h_BQuarkPair_dRMin_Pt1_Vs_Pt2   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuarkPair_dRMin_Pt1_Vs_Pt2"  , ";p_{T} (GeV/c); p_{T} (GeV/c)", nBinsPt, minPt, maxPt, nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuarkPair_dRMin_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  //
  h_BQuarkPair_dRMin_jet1_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet1_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet1_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet1_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet1_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet1_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_jet2_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet2_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet2_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet2_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet2_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "BQuarkPair_dRMin_jet2_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);

  // GenParticles: bqq trijet system (H+)
  h_Htb_tbW_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_Pt"   , ";p_{T} (GeV/c)"    ,  nBinsPt, minPt, maxPt);
  h_Htb_tbW_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_Htb_tbW_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_Htb_tbW_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_dRMax_dPhi" , ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_dRMax_dRap" , ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "Htb_tbW_bqq_dRMax_dR"   , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);
  h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "Htb_tbW_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);

  // GenParticles: bqq trijet system (associated top)
  h_gtt_tbW_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_Pt"   , ";p_{T} (GeV/c^{2})",  nBinsPt, minPt, maxPt);
  h_gtt_tbW_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_gtt_tbW_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_gtt_tbW_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_dRMax_dPhi", ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_dRMax_dRap", ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "gtt_tbW_bqq_dRMax_dR"  , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);  
  h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "gtt_tbW_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);
  
  // Leading Jets
  h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "Jet1Jet2_dEta_Vs_Jet3Jet4_dEta", ";#Delta#eta(j_{1},j_{2});#Delta#eta(j_{3},j_{4})", nBinsdEta, mindEta, maxdEta, nBinsdEta, mindEta, maxdEta);

  h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi", ";#Delta#phi(j_{1},j_{2}) (rads);#Delta#phi(j_{3},j_{4}) (rads)", nBinsdPhi, mindPhi, maxdPhi, nBinsdPhi, mindPhi, maxdPhi);

  h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "Jet1Jet2_dEta_Vs_Jet1Jet2_Mass", ";#Delta#eta(j_{1},j_{2});M(j_{1},j_{2}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);

  h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "Jet3Jet4_dEta_Vs_Jet3Jet4_Mass", ";#Delta#eta(j_{3},j_{4});M(j_{4},j_{4}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);
  
  // GenJets
  h_GenJets_N   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJets_N" , ";genJet multiplicity", 30, 0.0, 30.0);
  h_GenJet1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet4_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet5_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet5_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet6_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet6_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  //
  h_GenJet1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet4_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet5_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet5_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet6_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "GenJet6_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // tt system
  h_tt_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tt_Pt"   , ";p_{T} (GeV/c)"    , nBinsPt , minPt , maxPt );
  h_tt_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tt_Eta"  , ";#eta"             , nBinsEta, minEta, maxEta);
  h_tt_Rap   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tt_Rap"  , ";#omega"           , nBinsRap, minRap, maxRap);
  h_tt_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "tt_Mass" , ";M (GeV/c^{2})"    , nBinsM  , minM  , maxM  );

  // GenJets: Dijet with largest mass
  h_MaxDiJetMass_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_Pt"   , ";p_{T} (GeV/c)"    , nBinsPt, minPt, maxPt);
  h_MaxDiJetMass_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_Eta"  , ";#eta"             , nBinsEta, minEta, maxEta);
  h_MaxDiJetMass_Rap   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_Rap"  , ";#omega"           , nBinsRap, minRap, maxRap);
  h_MaxDiJetMass_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_Mass" , ";M (GeV/c^{2})"    , 100,  0.0, +2000.0);  
  h_MaxDiJetMass_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_dEta" , ";#Delta#eta"       , nBinsdEta, mindEta, maxdEta);
  h_MaxDiJetMass_dRap  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_dRap" , ";#Delta#omega"     , nBinsdRap, mindRap, maxdRap);
  h_MaxDiJetMass_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_dPhi" , ";#Delta#phi"       , nBinsdPhi, mindPhi, maxdPhi);  
  h_MaxDiJetMass_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_dR"   , ";#DeltaR"          , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dRrap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, th1, "MaxDiJetMass_dRrap", ";#DeltaR_{#omega}" , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "MaxDiJetMass_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)"  , nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_MaxDiJetMass_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "MaxDiJetMass_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  // Correlations
  h_BQuark1_BQuark2_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark1_BQuark2_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark1_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark1_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark2_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark2_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark3_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, th2, "BQuark3_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  return;
}

void HtbKinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void HtbKinematics::process(Long64_t entry) {

  if ( !fEvent.isMC() ) return;
  
  // Create MCools object
  MCTools mcTools(fEvent);
  
  // Increment Counter
  cAllEvents.increment();

  //start-new
  //================================================================================================
  // 1) Apply trigger
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;
  cTrigger.increment();


  //================================================================================================
  // 2) MET filters (to remove events with spurious sources of fake MET)       
  //================================================================================================
  // nothing to do

  //================================================================================================
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================
  // nothing to do

  //================================================================================================
  // 4) Electron veto (fully hadronic + orthogonality)  
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== Electron veto" << std::endl;
  vector<genParticle> selectedElectrons = GetGenParticles(fEvent.genparticles().getGenParticles(), cfg_ElectronPtCut, cfg_ElectronEtaCut, 11, true, false);
  if (0)
    {
      std::cout << "\nnElectrons = " << selectedElectrons.size() << std::endl;
      for (auto& p: selectedElectrons) std::cout << "\tpT = " << p.pt() << " (GeV/c), eta = " << p.eta() << ", phi = " << p.phi() << " (rads)" << std::endl;
    }
  if ( selectedElectrons.size() > 0 ) return;
  cElectronVeto.increment();


  //================================================================================================
  // 5) Muon veto (fully hadronic + orthogonality)  
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== Muon veto" << std::endl;
  vector<genParticle> selectedMuons = GetGenParticles(fEvent.genparticles().getGenParticles(), cfg_MuonPtCut, cfg_MuonEtaCut, 13, true, false);
  if (cfg_Verbose)
    {
      std::cout << "\nnMuons = " << selectedMuons.size() << std::endl;
      for (auto& p: selectedMuons) std::cout << "\tpT = " << p.pt() << " (GeV/c), eta = " << p.eta() << ", phi = " << p.phi() << " (rads)" << std::endl;
    }
  if ( selectedMuons.size() > 0 ) return;
  cMuonVeto.increment();


  //================================================================================================
  // 6) Tau veto (HToTauNu orthogonality)  
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== Tau veto" << std::endl;
  vector<genParticle> selectedTaus = GetGenParticles(fEvent.genparticles().getGenParticles(), cfg_TauPtCut, cfg_TauEtaCut, 15, true, false);
  if (0)
    {
      std::cout << "\nnTaus = " << selectedTaus.size() << std::endl;
      for (auto& p: selectedTaus) std::cout << "\tpT = " << p.pt() << " (GeV/c), eta = " << p.eta() << ", phi = " << p.phi() << " (rads)" << std::endl;
      std::cout << "" << std::endl;
    }
  if ( selectedTaus.size() > 0 ) return;
  cTauVeto.increment();


  //================================================================================================
  // 7) Jet Selection
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== Jet Selection" << std::endl;
  vector<GenJet> selectedJets = GetGenJets(fEvent.genjets(), cfg_JetPtCuts, cfg_JetEtaCuts);
  // for (auto& p: selectedJets) std::cout << "\tpT = " << p.pt() << " (GeV/c), eta = " << p.eta() << ", phi = " << p.phi() << " (rads)" << std::endl;
  if (!cfg_JetNumberCut.passedCut(selectedJets.size())) return;

  // HT Selection
  double genJ_HT = 0.0;
  std::vector<math::XYZTLorentzVector> selJets_p4;
  math::XYZTLorentzVector jet_p4;
  for(auto jet: selectedJets) 
    {
        jet_p4 = jet.p4();
	genJ_HT += jet.pt();
	selJets_p4.push_back( jet_p4 );
    }

  if ( !cfg_HtCut.passedCut(genJ_HT) ) return;
  cJetSelection.increment();

  //================================================================================================
  // 8) BJet Selection
  //================================================================================================
  if (cfg_Verbose) std::cout << "=== BJet Selection" << std::endl;
  vector<genParticle> selectedBQuarks = GetGenParticles(fEvent.genparticles().getGenParticles(), 10, 3, 5, true, false);
  std::sort( selectedBQuarks.begin(), selectedBQuarks.end(), PtComparator() );
  if (0) for (auto& p: selectedBQuarks) mcTools.PrintGenParticle(p);

  // Match b-quarks with GenJets
  vector<GenJet> selectedBJets = GetGenJets(selectedJets, cfg_BJetPtCuts, cfg_BJetEtaCuts, selectedBQuarks);
  // for (auto& p: selectedBJets) std::cout << "\tpT = " << p.pt() << " (GeV/c), eta = " << p.eta() << ", phi = " << p.phi() << " (rads)" << std::endl;

  // Get selected jets excluding the matched bjets
  bool isBJet = false;
  std::vector<math::XYZTLorentzVector> selJets_NoBJets_p4;

  // For-loop: Selected jets
  for (auto& jet: selectedJets) 
    {
      isBJet = false;
	    
      // For-loop: Selected bjets
      for (auto& bjet: selectedBJets) 
	{
	  double dR = ROOT::Math::VectorUtil::DeltaR(jet.p4(), bjet.p4());
	  if (dR < 0.01) isBJet = true;
	}
      if (isBJet) continue;
      jet_p4 = jet.p4();
      selJets_NoBJets_p4.push_back(jet_p4);
    }

  if (!cfg_BJetNumberCut.passedCut(selectedBJets.size())) return;
  cBJetSelection.increment();


  //================================================================================================
  // 9) BJet SF
  //================================================================================================
  // nothing to do
  

  //================================================================================================
  // 10) MET selection 
  //================================================================================================
  // nothing to do


  //================================================================================================
  // 11) Topology selection 
  //================================================================================================
  float C, D, H2;
  float Circularity;
  float y23, Sphericity, SphericityT, Aplanarity, Planarity, Y; // functions to return values when properly implemented
  float HT, JT, MHT, Centrality;
  vector<float> a = GetMomentumTensorEigenValues(selJets_p4, C, D, H2);
  vector<float> b = GetMomentumTensorEigenValues2D(selJets_p4, Circularity);
  vector<float> c = GetSphericityTensorEigenValues(selJets_p4, y23, Sphericity, SphericityT, Aplanarity, Planarity, Y);
  double alphaT   = GetAlphaT(selJets_p4, HT, JT, MHT, Centrality);
  
  // Apply cuts
  if ( !cfg_CparameterCut.passedCut(C) ) return;
  if ( !cfg_DparameterCut.passedCut(D) ) return;
  if ( !cfg_FoxWolframMomentCut.passedCut(H2) ) return;
  if ( !cfg_CircularityCut.passedCut(Circularity) ) return;
  if ( !cfg_Y23Cut.passedCut(y23) ) return;
  if ( !cfg_SphericityCut.passedCut(Sphericity) ) return;
  if ( !cfg_AplanarityCut.passedCut(Aplanarity) ) return;
  if ( !cfg_PlanarityCut.passedCut(Planarity) ) return;
  if ( !cfg_CentralityCut.passedCut(Centrality) ) return;
  if ( !cfg_AlphaTCut.passedCut(alphaT) ) return;
  cTopologySelection.increment();


  //================================================================================================
  // 12) Top selection 
  //================================================================================================
  cTopSelection.increment();


  //================================================================================================
  // Standard Selections    
  //================================================================================================


  //================================================================================================
  // All Selections
  //================================================================================================
  cSelected.increment();

  // Fill Histograms
  h_GenJets_N->Fill(selectedJets.size());

  ///////////////////////////////////////////////////////////////////////////
  // GenParticles
  ///////////////////////////////////////////////////////////////////////////
  cInclusive.increment();
  int nWToENu  = 0;
  int nWToMuNu = 0;
  bool bSkipEvent = false;

  // Indices
  // int Htb_HPlus_index             = -1.0;
  // int Htb_TQuark_index            = -1.0;
  // int Htb_BQuark_index            = -1.0;
  // int Htb_tbW_BQuark_index        = -1.0;
  // int Htb_tbW_WBoson_index        = -1.0;
  // int Htb_tbW_Wqq_Quark_index     = -1.0;
  // int Htb_tbW_Wqq_AntiQuark_index = -1.0;
  // int gtt_TQuark_index            = -1.0;
  // int gbb_BQuark_index            = -1.0;
  // int gtt_tbW_Wqq_Quark_index     = -1.0;
  // int gtt_tbW_Wqq_AntiQuark_index = -1.0;
  // int gtt_tbW_WBoson_index        = -1.0;
  // int gtt_tbW_BQuark_index        = -1.0; 

  // 4-momenta
  math::XYZTLorentzVector Htb_HPlus_p4;
  math::XYZTLorentzVector Htb_TQuark_p4;
  math::XYZTLorentzVector Htb_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_WBoson_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector gtt_TQuark_p4;
  math::XYZTLorentzVector gbb_BQuark_p4;
  math::XYZTLorentzVector gtt_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector gtt_tbW_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector gtt_tbW_WBoson_p4;
  math::XYZTLorentzVector gtt_tbW_BQuark_p4;


  // Define the table
  Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | E | Vertex (mm) | D0 (mm) | Lxy (mm) | Mom | Daughters", "Text"); //LaTeX or Text

  int row = 0;
  // For-loop: GenParticles
  for (auto& p: fEvent.genparticles().getGenParticles()) {

    // Particle properties
    short genP_index     = p.index();
    int genP_pdgId       = p.pdgId();
    int genP_status      = p.status();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    int genP_charge      = p.charge();
    // math::XYZTLorentzVector genP_p4;
    // genP_p4 = p.p4();    

    // Associated genParticles
    std::vector<genParticle> genP_daughters;
    for (unsigned int i=0; i < p.daughters().size(); i++) genP_daughters.push_back(fEvent.genparticles().getGenParticles()[p.daughters().at(i)]);
    std::vector<genParticle> genP_mothers;
    for (unsigned int i=0; i < p.mothers().size(); i++) genP_mothers.push_back(fEvent.genparticles().getGenParticles()[p.mothers().at(i)]);
    std::vector<genParticle> genP_grandMothers;
    std::vector<unsigned int> genMoms_index;
    std::vector<unsigned int> genMoms_pdgId;
    std::vector<unsigned int> genDaus_index;
    std::vector<unsigned int> genDaus_pdgId;

    // Removed real vertex from Tree (to save size)
    ROOT::Math::XYZPoint vtxIdeal;
    vtxIdeal.SetXYZ(0, 0, 0);
    double genP_vtxX = vtxIdeal.X(); // p.vtxX()*10; // in mm
    double genP_vtxY = vtxIdeal.Y(); // p.vtxY()*10; // in mm
    double genP_vtxZ = vtxIdeal.Z(); // p.vtxZ()*10; // in mm

    // Daughter, Mom and Grand-mom properties    
    genParticle m;
    genParticle g;
    genParticle d;

    if (genP_daughters.size() > 0) d = genP_daughters.at(0);
    if (p.mothers().size() > 0)
      {
	m = genP_mothers.at(0); // fixme
	for (unsigned int i=0; i < m.mothers().size(); i++) genP_grandMothers.push_back(fEvent.genparticles().getGenParticles()[m.mothers().at(i)]);
	if (m.mothers().size() > 0) g = genP_grandMothers.at(0); // fixme
      } 

    // For convenience, save the pdgIds in vectors
    for (unsigned int i=0; i < genP_mothers.size(); i++) 
      {
	if (genP_mothers.at(i).index() < 0) continue;
	genMoms_index.push_back(genP_mothers.at(i).index());
	genMoms_pdgId.push_back(genP_mothers.at(i).pdgId());
      }
    for (unsigned int i=0; i < genP_daughters.size(); i++) 
      {
	if (genP_daughters.at(i).index() < 0) continue;
	genDaus_index.push_back(genP_daughters.at(i).index());
	genDaus_pdgId.push_back(genP_daughters.at(i).pdgId());
      }

    // Properties that need to be calculated
    double genP_Lxy = 0.0; 
    double genP_d0  = 0.0;
    if (genP_daughters.size() > 0 && genP_mothers.size() > 0)
      {
	genP_d0  = mcTools.GetD0 (p, m, d, vtxIdeal); // in mm
	genP_Lxy = mcTools.GetLxy(p, m, d, vtxIdeal); // in mm
      }
   
    
    // Print genParticle properties or decay tree ?
    if (0)
      {
    	mcTools.PrintGenParticle(p);
     	mcTools.PrintGenDaughters(p);
       }


    // Add table rows
    //if (cfg_Verbose){
    table.AddRowColumn(row, auxTools.ToString(entry)           );
    table.AddRowColumn(row, auxTools.ToString(genP_index)      );
    table.AddRowColumn(row, auxTools.ToString(genP_pdgId)      );
    table.AddRowColumn(row, auxTools.ToString(genP_status)     );
    table.AddRowColumn(row, auxTools.ToString(genP_charge)     );
    table.AddRowColumn(row, auxTools.ToString(genP_pt , 3)     );
    table.AddRowColumn(row, auxTools.ToString(genP_eta, 4)     );
    table.AddRowColumn(row, auxTools.ToString(genP_phi, 3)     );
    table.AddRowColumn(row, auxTools.ToString(genP_energy, 3)  );
    table.AddRowColumn(row, "(" + auxTools.ToString(genP_vtxX, 3) + ", " + auxTools.ToString(genP_vtxY, 3)  + ", " + auxTools.ToString(genP_vtxZ, 3) + ")" );
    table.AddRowColumn(row, auxTools.ToString(genP_d0 , 3)     );
    table.AddRowColumn(row, auxTools.ToString(genP_Lxy, 3)     );	
    if (genMoms_index.size() < 6)
      {
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genMoms_index) );
	// table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genMoms_pdgId) );
      }
    else table.AddRowColumn(row, ".. Too many .." );
    if (genDaus_index.size() < 6)
      {
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genDaus_index) );
	// table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genDaus_pdgId) );
      }
    else table.AddRowColumn(row, ".. Too many .." );
    row++;
    //  }
	       

    // Filtering
    // if (!p.isLastCopy()) continue;
    // if ( !mcTools.IsQuark(genP_pdgId) ) continue;
    // if (!p.isPrompt()) continue;
    // if (!p.isPromptDecayed()) continue;
    // if (!p.isPromptFinalState()) continue;
    // if (!p.isDecayedLeptonHadron()) continue;
    // if (!p.isTauDecayProduct()) continue;
    // if (!p.isPromptTauDecayProduct()) continue;
    // if (!p.isDirectTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProductFinalState()) continue;
    // if (!p.isDirectHadronDecayProduct()) continue;
    // if (!p.isDirectHardProcessTauDecayProductFinalState()) continue;
    //// if (!p.isHardProcess()) continue;
    // if (!p.fromHardProcess()) continue;
    // if (!p.fromHardProcessDecayed()) continue;
    // if (!p.fromHardProcessFinalState()) continue;
    // if (!p.isHardProcessTauDecayProduct()) continue;
    // if (!p.isDirectHardProcessTauDecayProduct()) continue;
    // if (!p.fromHardProcessBeforeFSR()) continue;
    // if (!p.isFirstCopy()) continue;
    // if (!p.isLastCopyBeforeFSR()) continue;

    
    // Associated top (g->tt)
    if (genP_pdgId == -6)
      {
	if (!p.isLastCopy()) continue;
	       
	cgtt_TQuark.increment();
	gtt_TQuark_p4    = p.p4();
	// gtt_TQuark_index = genP_index; 


	for (auto& d: genP_daughters) 
	  {
	    
	    if (d.pdgId() == -5)// g->tt, t->bW, b-quark
	      {
		cgtt_tbW_BQuark.increment();
		gtt_tbW_BQuark_p4 = d.p4();
		// gtt_tbW_BQuark_index = genP_index;
	      }
	    else if (d.pdgId() == -24)// g->tt, t->bW, W-boson
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cgtt_tbW_WBoson.increment();
		gtt_tbW_WBoson_p4 = d.p4();
		// gtt_tbW_WBoson_index = genP_index;
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "HtbKinematics::process() Unexpected top-quark daughter.";
		bSkipEvent = true;
	      }

	  } // for (auto& d: genP_daughters)
      }// if (genP_pdgId == -6)
  

    // W- from Associated top (g->tt, t->bW)
    if (genP_pdgId == -24)
      {
	if (!p.isLastCopy()) continue;
	
	for (auto& d: genP_daughters) 
	  {
	    
	    if ( mcTools.IsQuark(d.pdgId() ) )// g->tt, t->bWH, t->bW, W->q qbar'
	      {
		if (d.pdgId() > 0)
		  {
		    // Quarks
		    cgtt_tbW_Wqq_Quark.increment();
		    gtt_tbW_Wqq_Quark_p4 = d.p4();
		    // gtt_tbW_Wqq_Quark_index = d.index();
		  }	       
		else
		  {
		    // AntiQuarks
		    cgtt_tbW_Wqq_AntiQuark.increment();
		    gtt_tbW_Wqq_AntiQuark_p4 = d.p4();
		    // gtt_tbW_Wqq_AntiQuark_index = d.index();
		  }
	      }	  
	    else if ( mcTools.IsLepton(d.pdgId() ) )// g->tt, t->bWH, t->bW, W->l v
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cgtt_tbW_Wqq_Leptons.increment();
		
		if ( std::abs(d.pdgId()) == 11)
		  {		      
		    if ( d.p4().pt() < cfg_ElectronPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_ElectronEtaCut) continue;
		    nWToENu++;
		  }
		else if ( std::abs(d.pdgId()) == 13)
		  {
		    if ( d.p4().pt() < cfg_MuonPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_MuonEtaCut) continue;
		    nWToMuNu++;
		  }		  
		else{}
	      }
	    else
	      {
		throw hplus::Exception("Logic") << "HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		// std::cout << "*** HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this." << std::endl;
		// bSkipEvent = true;
	      }
	  }// for (auto& d: genP_daughters)
      }// if (genP_pdgId == -24)



    // H+
    if (genP_pdgId == 37)
      {
	if (!p.isLastCopy()) continue;

	cHtb_HPlus.increment();
	Htb_HPlus_p4 = p.p4();
	// Htb_HPlus_index = genP_index;

	for (auto& d: genP_daughters) 
	  {

	    if ( d.pdgId() == 6)// H->tb, t
	      {
		
		cHtb_TQuark.increment();
		Htb_TQuark_p4 = d.p4();
		// Htb_TQuark_index = genP_index;
	      }
	    else if ( d.pdgId() == -5)// H->tb, b
	      {
		cHtb_BQuark.increment();
		Htb_BQuark_p4 = d.p4();
		// Htb_BQuark_index = genP_index;
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "HtbKinematics::process() B-quark whose origins are not accounted for. Need to rethink this.";
		// std::cout << "*** HtbKinematics::process() H+ daughters whose origins are not accounted for. Need to rethink this." << std::endl;
		bSkipEvent = true;
	      }

	  }// for (auto& d: genP_daughters) 

      }// if (genP_pdgId == 37)
	    

    // Top (H->tb)
    if (genP_pdgId == 6)
      {

	if (!p.isLastCopy()) continue;	
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);

	for (auto& d: genP_daughters) 
	  {

	    if ( d.pdgId() == +24)// H->tb, t->bW+, W+
	      {
		// mcTools.PrintGenParticle(d);		

		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		cHtb_tbW_WBoson.increment();
		Htb_tbW_WBoson_p4  = d.p4();
		// Htb_tbW_WBoson_index = genP_index;
	      }
	    else if ( d.pdgId() == +5)// H->tb, t->bW+, b
	      {
		// mcTools.PrintGenParticle(d);
		
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu
		cHtb_tbW_BQuark.increment();
		Htb_tbW_BQuark_p4 = d.p4();
		// Htb_tbW_BQuark_index = genP_index;
	      }
	    else
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!

		// std::cout << "*** HtbKinematics::process() t (H->tb) daughters whose origins are not accounted for. Need to rethink this." << std::endl;
		// mcTools.PrintGenParticle(d);
		// mcTools.PrintGenDaughters(d);
	      }
	  }// for (auto& d: genP_daughters) 
      }// if (genP_pdgId == 6)


    // W+ (H->tb, t->bW+, W+)
    if (genP_pdgId == +24)
      {

	if (!p.isLastCopy()) continue;		
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);

	for (auto& d: genP_daughters) 
	  {

	    if ( mcTools.IsQuark(d.pdgId()) ) // H+->tb, t->bW+, W+->qq
	      {	
		if (d.pdgId() > 0)
		  {
		    // Quarks
		    cHtb_tbW_Wqq_Quark.increment();
		    Htb_tbW_Wqq_Quark_p4 = d.p4();
		    // Htb_tbW_Wqq_Quark_index = d.index();
		  }
		else
		  {
		    // Anti-Quarks
		    cHtb_tbW_Wqq_AntiQuark.increment();
		    Htb_tbW_Wqq_AntiQuark_p4 = d.p4();
		    // Htb_tbW_Wqq_AntiQuark_index = d.index();
		  }
	      }
	    else if ( mcTools.IsLepton(d.pdgId() ) ) // H+->tb, t->bW+, W+->l v
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cHtb_tbW_Wqq_Leptons.increment();
		
		if ( std::abs(d.pdgId()) == 11)
		  {		      
		    if ( d.p4().pt() < cfg_ElectronPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_ElectronEtaCut) continue;
		    nWToENu++;
		  }
		else if ( std::abs(d.pdgId()) == 13)
		  {
		    if ( d.p4().pt() < cfg_MuonPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_MuonEtaCut) continue;
		    nWToMuNu++;
		  }		  
		else{}		  
	      }
	    else
	      {
		throw hplus::Exception("Logic") << "HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		// std::cout << "*** HtbKinematics::process() W+ (H->tb) daughters whose origins are not accounted for. Need to rethink this." << std::endl;
	      }
	    
	  }// for (auto& d: genP_daughters) 

      }// if (genP_pdgId == +24)


    // Flavour-excited b-quark (g->bb)
    if (genP_pdgId == 5)
      {

	// Consider only status=23 (outgoing) particles
	if ( p.status() != 23 )  continue;

	// Comes from proton or gluon
	bool fromGluon  = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 21) != genMoms_pdgId.end();
	bool fromProton = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 2212) != genMoms_pdgId.end();
	bool fromDQuark = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 1) != genMoms_pdgId.end();
	bool fromUQuark = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 2) != genMoms_pdgId.end();
	bool fromSQuark = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 3) != genMoms_pdgId.end();
	bool fromCQuark = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 4) != genMoms_pdgId.end();
	if (fromGluon==false && fromProton==false && fromUQuark==false && fromDQuark==false && fromCQuark==false && fromSQuark==false) continue;
	
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);
	
	cgbb_BQuark.increment();
	gbb_BQuark_p4 = p.p4();
	// gbb_BQuark_index = genP_index;

      }// if (genP_pdgId == 5)

	    
  }// for-loop: genParticles

  
  ///////////////////////////////////////////////////////////////////////////
  // Preselection Cuts (python/parameters/hplus2tbAnalysis.py)
  ///////////////////////////////////////////////////////////////////////////
  // Skip event if various forbidden decays detected (t->Wd, t->Ws instead of dominant t->Wb)
  if ( bSkipEvent ) return;

  // Event Variables
  double genP_HT = (Htb_BQuark_p4.pt() + Htb_tbW_BQuark_p4.pt() + Htb_tbW_Wqq_Quark_p4.pt() + Htb_tbW_Wqq_AntiQuark_p4.pt()
		    + gtt_tbW_Wqq_Quark_p4.pt() + gtt_tbW_Wqq_AntiQuark_p4.pt() + gtt_tbW_BQuark_p4.pt()
		    + gbb_BQuark_p4.pt());
  
  std::vector<math::XYZTLorentzVector> v_dijet_p4;
  std::vector<double> v_dijet_masses;
  std::vector<double> v_dijet_dR;
  std::vector<double> v_dijet_dRrap;
  std::vector<double> v_dijet_dEta;
  std::vector<double> v_dijet_dPhi;
  std::vector<double> v_dijet_dRap;
  

  math::XYZTLorentzVector tt_p4 = Htb_TQuark_p4 + gtt_TQuark_p4;
  h_tt_Mass ->Fill( tt_p4.mass() );
  h_tt_Pt   ->Fill( tt_p4.pt()  );
  h_tt_Eta  ->Fill( tt_p4.eta() );
  h_tt_Rap  ->Fill( mcTools.GetRapidity(tt_p4) );

  double maxDijetMass_mass;
  math::XYZTLorentzVector maxDijetMass_p4;
  int maxDijetMass_pos;
  double maxDijetMass_dR;
  double maxDijetMass_dRrap;
  double maxDijetMass_dEta;
  double maxDijetMass_dPhi;
  double maxDijetMass_dRap;
  double maxDijetMass_rapidity;
  
  int iJet = 0;
  if (selJets_p4.size() > 1) {
    // For-loop: All selected jets 
    for (size_t i=0; i < selJets_p4.size(); i++)
      {
	iJet++;
	double genJ_Pt  = selJets_p4.at(i).pt();
	double genJ_Eta = selJets_p4.at(i).eta();
	// double genJ_Rap = mcTools.GetRapidity(selJets_p4.at(i));
	
	if (iJet==1)
	  {
	    
	    h_GenJet1_Pt -> Fill( genJ_Pt  );
	    h_GenJet1_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==2)
	  {
	    
	    h_GenJet2_Pt -> Fill( genJ_Pt  );
	    h_GenJet2_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==3)
	  {
	    
	    h_GenJet3_Pt -> Fill( genJ_Pt  );
	    h_GenJet3_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==4)
	  {

	    h_GenJet4_Pt -> Fill( genJ_Pt  );
	    h_GenJet4_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==5)
	  {

	    h_GenJet5_Pt -> Fill( genJ_Pt  );
	    h_GenJet5_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==6)
	  {

	    h_GenJet6_Pt -> Fill( genJ_Pt  );
	    h_GenJet6_Eta-> Fill( genJ_Eta );

	  }
	else{}
	
	// For-loop: All selected jets (nested)
	for (size_t j=i+1; j < selJets_p4.size(); j++)
	  {
	    math::XYZTLorentzVector p4_i = selJets_p4.at(i);
	    math::XYZTLorentzVector p4_j = selJets_p4.at(j);
	    math::XYZTLorentzVector p4   = p4_i + p4_j;
	    double rap_i = mcTools.GetRapidity(p4_i);
	    double rap_j = mcTools.GetRapidity(p4_j);
	    double dR    = ROOT::Math::VectorUtil::DeltaR(p4_i, p4_j);
	    double dRap  = std::abs(rap_i - rap_j);
	    double dEta  = std::abs(p4_i.eta() - p4_j.eta());
	    double dPhi  = std::abs(ROOT::Math::VectorUtil::DeltaPhi(p4_i, p4_j));
	    
	    v_dijet_p4.push_back( p4 );
	    v_dijet_masses.push_back( p4.mass() );
	    v_dijet_dR.push_back( dR );
	    v_dijet_dRrap.push_back( sqrt( pow(dRap, 2) + pow(dPhi, 2) ) ); 
	    v_dijet_dEta.push_back( dEta ); 
	    v_dijet_dRap.push_back( dRap );
	    v_dijet_dPhi.push_back( dPhi );

	  }
      }

    // MaxDiJet: DiJet combination with largest mass
    maxDijetMass_pos      = std::max_element(v_dijet_masses.begin(), v_dijet_masses.end()) - v_dijet_masses.begin();
    maxDijetMass_mass     = v_dijet_masses.at(maxDijetMass_pos);
    maxDijetMass_p4       = v_dijet_p4.at(maxDijetMass_pos);
    maxDijetMass_dR       = v_dijet_dR.at(maxDijetMass_pos);
    maxDijetMass_dRrap    = v_dijet_dRrap.at(maxDijetMass_pos);
    maxDijetMass_dEta     = v_dijet_dEta.at(maxDijetMass_pos);
    maxDijetMass_dPhi     = v_dijet_dPhi.at(maxDijetMass_pos);
    maxDijetMass_dRap     = v_dijet_dRap.at(maxDijetMass_pos);
    maxDijetMass_rapidity = mcTools.GetRapidity(maxDijetMass_p4);

  }// if (selJets_p4.size() > 1) {

  //  if (selJets_p4.size() > 3) {
    double jet1_Eta = selJets_p4.at(0).eta();
    double jet2_Eta = selJets_p4.at(1).eta();
    double jet3_Eta = selJets_p4.at(2).eta();
    double jet4_Eta = selJets_p4.at(3).eta();

    double jet1_Phi = selJets_p4.at(0).phi();
    double jet2_Phi = selJets_p4.at(1).phi();
    double jet3_Phi = selJets_p4.at(2).phi();
    double jet4_Phi = selJets_p4.at(3).phi();

    
    h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta ->Fill(std::abs(jet1_Eta - jet2_Eta), std::abs(jet3_Eta - jet4_Eta));
    h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi ->Fill(std::abs(jet1_Phi - jet2_Phi), std::abs(jet3_Phi - jet4_Phi));
    h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass ->Fill(std::abs(jet1_Eta - jet2_Eta), (selJets_p4.at(0) + selJets_p4.at(1)).mass() );
    h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass ->Fill(std::abs(jet3_Eta - jet4_Eta), (selJets_p4.at(2) + selJets_p4.at(3)).mass() );
    //  } alex
  
  // Event-based histograms
  h_genMET_Et  ->Fill(fEvent.genMET().et()); 
  h_genMET_Phi ->Fill(fEvent.genMET().Phi());

  
  // Trijet system (H+)
  math::XYZTLorentzVector Htb_tbW_bqq_p4 = Htb_tbW_BQuark_p4 + Htb_tbW_Wqq_Quark_p4 + Htb_tbW_Wqq_AntiQuark_p4;

  // Find max separation
  std::vector<math::XYZTLorentzVector> bqq_p4;
  bqq_p4.push_back(Htb_tbW_BQuark_p4);
  bqq_p4.push_back(Htb_tbW_Wqq_Quark_p4);
  bqq_p4.push_back(Htb_tbW_Wqq_AntiQuark_p4);
  double deltaRMax = -1.0;
  int deltaRMax_i  = -1;
  int deltaRMax_j  = -1;
  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system

  // double bqq_dEta = std::abs(bqq_p4.at(deltaRMax_i).eta() - bqq_p4.at(deltaRMax_j).eta());
  double bqq_dRap = std::abs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
  double bqq_dPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
  // Fill Histos
  h_Htb_tbW_bqq_Pt->Fill( Htb_tbW_bqq_p4.pt());
  h_Htb_tbW_bqq_Rap->Fill( mcTools.GetRapidity(Htb_tbW_bqq_p4) );
  h_Htb_tbW_bqq_Mass->Fill( Htb_tbW_bqq_p4.mass() );
  h_Htb_tbW_bqq_dRMax_dR->Fill( deltaRMax );
  h_Htb_tbW_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_Htb_tbW_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi->Fill( bqq_dRap, bqq_dPhi );

  // Trijet system (associated top)
  math::XYZTLorentzVector gtt_tbW_bqq_p4 = gtt_tbW_Wqq_Quark_p4 + gtt_tbW_Wqq_AntiQuark_p4 + gtt_tbW_BQuark_p4;

  // Fix max separation (again)
  bqq_p4.clear();
  bqq_p4.push_back(gtt_tbW_BQuark_p4);
  bqq_p4.push_back(gtt_tbW_Wqq_Quark_p4);
  bqq_p4.push_back(gtt_tbW_Wqq_AntiQuark_p4);
  deltaRMax    = -1.0;
  deltaRMax_i  = -1;
  deltaRMax_j  = -1;

  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system

  // bqq_dEta = std::abs(bqq_p4.at(deltaRMax_i).eta() - bqq_p4.at(deltaRMax_j).eta());
  bqq_dRap = std::abs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
  bqq_dPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
  // Fill Histos
  h_gtt_tbW_bqq_Pt->Fill( gtt_tbW_bqq_p4.pt() );
  h_gtt_tbW_bqq_Rap->Fill( mcTools.GetRapidity(gtt_tbW_bqq_p4) );
  h_gtt_tbW_bqq_Mass->Fill( gtt_tbW_bqq_p4.mass() );
  h_gtt_tbW_bqq_dRMax_dR->Fill( deltaRMax );
  h_gtt_tbW_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_gtt_tbW_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi ->Fill( bqq_dRap, bqq_dPhi );

  // MaxDiJet
  h_MaxDiJetMass_Mass ->Fill( maxDijetMass_mass     );
  h_MaxDiJetMass_Pt   ->Fill( maxDijetMass_p4.pt()  );
  h_MaxDiJetMass_Eta  ->Fill( maxDijetMass_p4.eta() );
  h_MaxDiJetMass_Rap  ->Fill( maxDijetMass_rapidity );
  h_MaxDiJetMass_dR   ->Fill( maxDijetMass_dR       );
  h_MaxDiJetMass_dRrap->Fill( maxDijetMass_dRrap    );
  h_MaxDiJetMass_dEta ->Fill( maxDijetMass_dEta     );
  h_MaxDiJetMass_dPhi ->Fill( maxDijetMass_dPhi     );
  h_MaxDiJetMass_dRap ->Fill( maxDijetMass_dRap     );
  h_MaxDiJetMass_dEta_Vs_dPhi->Fill( maxDijetMass_dEta, maxDijetMass_dPhi );
  h_MaxDiJetMass_dRap_Vs_dPhi->Fill( maxDijetMass_dRap, maxDijetMass_dPhi );
  
  // Calculate HT
  h_genHT_GenParticles->Fill(genP_HT);
  h_genHT_GenJets->Fill(genJ_HT);
  
  
  // Print the table with genP info
  if (cfg_Verbose) table.Print();
  
  // H+->tb, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu)
  h_tbH_tbW_BQuark_Pt ->Fill( Htb_tbW_BQuark_p4.pt()  );
  h_tbH_tbW_BQuark_Eta->Fill( Htb_tbW_BQuark_p4.eta() );
  h_tbH_tbW_BQuark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_BQuark_p4) );

  // H+->tb, b
  h_tbH_BQuark_Pt ->Fill( Htb_BQuark_p4.pt()  );
  h_tbH_BQuark_Eta->Fill( Htb_BQuark_p4.eta() );
  h_tbH_BQuark_Rap->Fill( mcTools.GetRapidity(Htb_BQuark_p4 ) );

  // g->bb, b (flavour-excited )	       
  h_gbb_BQuark_Pt ->Fill( gbb_BQuark_p4.pt()  );
  h_gbb_BQuark_Eta->Fill( gbb_BQuark_p4.eta() );
  h_gbb_BQuark_Rap->Fill( mcTools.GetRapidity(gbb_BQuark_p4) );

  // g->tt, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_BQuark_Pt ->Fill( gtt_tbW_BQuark_p4.pt()  ); 
  h_gtt_tbW_BQuark_Eta->Fill( gtt_tbW_BQuark_p4.eta() );
  h_gtt_tbW_BQuark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_BQuark_p4) );
    
  // H+->tb (From HPlus decay)
  h_tbH_TQuark_Pt ->Fill( Htb_TQuark_p4.pt()) ;
  h_tbH_TQuark_Eta->Fill( Htb_TQuark_p4.eta() );
  h_tbH_TQuark_Rap->Fill( mcTools.GetRapidity(Htb_TQuark_p4) );

  // g->tt (Associated top)
  h_gtt_TQuark_Pt ->Fill( gtt_TQuark_p4.pt()  );
  h_gtt_TQuark_Eta->Fill( gtt_TQuark_p4.eta() );
  h_gtt_TQuark_Rap->Fill( mcTools.GetRapidity(gtt_TQuark_p4) );
  
  // tb->H+, H+
  h_tbH_HPlus_Pt ->Fill( Htb_HPlus_p4.pt()  );
  h_tbH_HPlus_Eta->Fill( Htb_HPlus_p4.eta() );
  h_tbH_HPlus_Rap->Fill( mcTools.GetRapidity(Htb_HPlus_p4) );
  
  // H+->tb, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_tbH_tbW_WBoson_Pt ->Fill( Htb_tbW_WBoson_p4.pt()  );
  h_tbH_tbW_WBoson_Eta->Fill( Htb_tbW_WBoson_p4.eta() );
  h_tbH_tbW_WBoson_Rap->Fill( mcTools.GetRapidity(Htb_tbW_WBoson_p4) );

  // H+->tb, t->bW, W-boson, Quark
  h_Htb_tbW_Wqq_Quark_Pt ->Fill( Htb_tbW_Wqq_Quark_p4.pt()  );
  h_Htb_tbW_Wqq_Quark_Eta->Fill( Htb_tbW_Wqq_Quark_p4.eta() );
  h_Htb_tbW_Wqq_Quark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4) );

  // H+->tb, t->bW, W-boson, AntiQuark
  h_Htb_tbW_Wqq_AntiQuark_Pt ->Fill( Htb_tbW_Wqq_AntiQuark_p4.pt()  );
  h_Htb_tbW_Wqq_AntiQuark_Eta->Fill( Htb_tbW_Wqq_AntiQuark_p4.eta() );
  h_Htb_tbW_Wqq_AntiQuark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4) );

  // g->tt, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_WBoson_Pt ->Fill( gtt_tbW_WBoson_p4.pt()  );
  h_gtt_tbW_WBoson_Eta->Fill( gtt_tbW_WBoson_p4.eta() );
  h_gtt_tbW_WBoson_Rap->Fill( mcTools.GetRapidity(gtt_tbW_WBoson_p4) );

  // g->tt, t->bW, W->qq, Quark
  h_gtt_tbW_Wqq_Quark_Pt ->Fill( gtt_tbW_Wqq_Quark_p4.pt()  );
  h_gtt_tbW_Wqq_Quark_Eta->Fill( gtt_tbW_Wqq_Quark_p4.eta() );
  h_gtt_tbW_Wqq_Quark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_Wqq_Quark_p4) );

  // g->tt, t->bW, W->qq, AntiQuark
  h_gtt_tbW_Wqq_AntiQuark_Pt ->Fill( gtt_tbW_Wqq_AntiQuark_p4.pt()  );
  h_gtt_tbW_Wqq_AntiQuark_Eta->Fill( gtt_tbW_Wqq_AntiQuark_p4.eta() );
  h_gtt_tbW_Wqq_AntiQuark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_Wqq_AntiQuark_p4) );

 
  // H+->tb, t->bW, W->qq
  double dR_Htb_TQuark_Htb_BQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, Htb_BQuark_p4           );
  double dR_Htb_TQuark_gtt_TQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, gtt_TQuark_p4           );
  double dR_Htb_TQuark_gbb_BQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, gbb_BQuark_p4           );
  double dR_Htb_BQuark_Htb_tbW_BQuark            = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_BQuark_p4       );
  double dR_Htb_BQuark_Htb_tbW_Wqq_Quark         = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4    );
  double dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);
  double dR_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_Quark_p4);
  double dR_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);
  double dR_Htb_tbW_WBoson_Htb_BQuark            = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_WBoson_p4, Htb_BQuark_p4    );
  double dR_Htb_tbW_WBoson_Htb_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_WBoson_p4, Htb_tbW_BQuark_p4);
  double dR_Htb_tbW_WBoson_gtt_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_WBoson_p4, gtt_tbW_BQuark_p4);
  double dR_Htb_tbW_WBoson_gbb_BQuark            = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_WBoson_p4, gbb_BQuark_p4    );
  double dR_gtt_tbW_WBoson_Htb_BQuark            = ROOT::Math::VectorUtil::DeltaR( gtt_tbW_WBoson_p4, Htb_BQuark_p4    );
  double dR_gtt_tbW_WBoson_Htb_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR( gtt_tbW_WBoson_p4, Htb_tbW_BQuark_p4);
  double dR_gtt_tbW_WBoson_gtt_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR( gtt_tbW_WBoson_p4, gtt_tbW_BQuark_p4);
  double dR_gtt_tbW_WBoson_gbb_BQuark            = ROOT::Math::VectorUtil::DeltaR( gtt_tbW_WBoson_p4, gbb_BQuark_p4    );

  double dEta_Htb_TQuark_Htb_BQuark                = std::abs( Htb_TQuark_p4.eta() - Htb_BQuark_p4.eta()            );
  double dEta_Htb_TQuark_gtt_TQuark                = std::abs( Htb_TQuark_p4.eta() - gtt_TQuark_p4.eta()            );
  double dEta_Htb_TQuark_gbb_BQuark                = std::abs( Htb_TQuark_p4.eta() - gbb_BQuark_p4.eta()            );
  double dEta_Htb_BQuark_Htb_tbW_BQuark            = std::abs( Htb_BQuark_p4.eta() - Htb_tbW_BQuark_p4.eta()        );
  double dEta_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::abs( Htb_BQuark_p4.eta() - Htb_tbW_Wqq_Quark_p4.eta()     );
  double dEta_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::abs( Htb_BQuark_p4.eta() - Htb_tbW_Wqq_AntiQuark_p4.eta() );
  double dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::abs( Htb_tbW_BQuark_p4.eta() - Htb_tbW_Wqq_Quark_p4.eta() );
  double dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::abs( Htb_tbW_BQuark_p4.eta() - Htb_tbW_Wqq_AntiQuark_p4.eta() );
  double dEta_Htb_tbW_WBoson_Htb_BQuark            = std::abs( Htb_tbW_WBoson_p4.eta() - Htb_BQuark_p4.eta()     );
  double dEta_Htb_tbW_WBoson_Htb_tbW_BQuark        = std::abs( Htb_tbW_WBoson_p4.eta() - Htb_tbW_BQuark_p4.eta() );
  double dEta_Htb_tbW_WBoson_gtt_tbW_BQuark        = std::abs( Htb_tbW_WBoson_p4.eta() - gtt_tbW_BQuark_p4.eta() );
  double dEta_Htb_tbW_WBoson_gbb_BQuark            = std::abs( Htb_tbW_WBoson_p4.eta() - gbb_BQuark_p4.eta()     );
  double dEta_gtt_tbW_WBoson_Htb_BQuark            = std::abs( gtt_tbW_WBoson_p4.eta() - Htb_BQuark_p4.eta()     );
  double dEta_gtt_tbW_WBoson_Htb_tbW_BQuark        = std::abs( gtt_tbW_WBoson_p4.eta() - Htb_tbW_BQuark_p4.eta() );
  double dEta_gtt_tbW_WBoson_gtt_tbW_BQuark        = std::abs( gtt_tbW_WBoson_p4.eta() - gtt_tbW_BQuark_p4.eta() );
  double dEta_gtt_tbW_WBoson_gbb_BQuark            = std::abs( gtt_tbW_WBoson_p4.eta() - gbb_BQuark_p4.eta()     );

  double dPhi_Htb_TQuark_Htb_BQuark                = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, Htb_BQuark_p4            ));
  double dPhi_Htb_TQuark_gtt_TQuark                = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, gtt_TQuark_p4            ));
  double dPhi_Htb_TQuark_gbb_BQuark                = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, gbb_BQuark_p4            ));
  double dPhi_Htb_BQuark_Htb_tbW_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_BQuark_p4        ));
  double dPhi_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4     ));
  double dPhi_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4 ));
  double dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_Quark_p4 ));
  double dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4));
  double dPhi_Htb_tbW_WBoson_Htb_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_WBoson_p4, Htb_BQuark_p4    ) );
  double dPhi_Htb_tbW_WBoson_Htb_tbW_BQuark        = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_WBoson_p4, Htb_tbW_BQuark_p4) );
  double dPhi_Htb_tbW_WBoson_gtt_tbW_BQuark        = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_WBoson_p4, gtt_tbW_BQuark_p4) );
  double dPhi_Htb_tbW_WBoson_gbb_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_WBoson_p4, gbb_BQuark_p4    ) );
  double dPhi_gtt_tbW_WBoson_Htb_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_WBoson_p4, Htb_BQuark_p4    ) );
  double dPhi_gtt_tbW_WBoson_Htb_tbW_BQuark        = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_WBoson_p4, Htb_tbW_BQuark_p4) );
  double dPhi_gtt_tbW_WBoson_gtt_tbW_BQuark        = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_WBoson_p4, gtt_tbW_BQuark_p4) );
  double dPhi_gtt_tbW_WBoson_gbb_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_WBoson_p4, gbb_BQuark_p4    ) );

  double dRap_Htb_TQuark_Htb_BQuark                = std::abs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(Htb_BQuark_p4)            );
  double dRap_Htb_TQuark_gtt_TQuark                = std::abs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(gtt_TQuark_p4)            );
  double dRap_Htb_TQuark_gbb_BQuark                = std::abs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(gbb_BQuark_p4)            );
  double dRap_Htb_BQuark_Htb_tbW_BQuark            = std::abs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_BQuark_p4)        );
  double dRap_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::abs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4)     );
  double dRap_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::abs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4) );
  double dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::abs( mcTools.GetRapidity(Htb_tbW_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4 ));
  double dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::abs( mcTools.GetRapidity(Htb_tbW_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4));
  
  // Associated products
  double dR_gtt_TQuark_gbb_BQuark                = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4    , gbb_BQuark_p4            );
  double dR_gtt_TQuark_gtt_tbW_BQuark            = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4    , gtt_tbW_BQuark_p4        ); 
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4     );
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4 );

  double dEta_gtt_TQuark_gbb_BQuark                = std::abs( gtt_TQuark_p4.eta()     - gbb_BQuark_p4.eta()            );
  double dEta_gtt_TQuark_gtt_tbW_BQuark            = std::abs( gtt_TQuark_p4.eta()     - gtt_tbW_BQuark_p4.eta()        ); 
  double dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::abs( gtt_tbW_BQuark_p4.eta() - gtt_tbW_Wqq_Quark_p4.eta()     );
  double dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::abs( gtt_tbW_BQuark_p4.eta() - gtt_tbW_Wqq_AntiQuark_p4.eta() );
  
  double dPhi_gtt_TQuark_gbb_BQuark                = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_TQuark_p4    , gbb_BQuark_p4            ));
  double dPhi_gtt_TQuark_gtt_tbW_BQuark            = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_TQuark_p4    , gtt_tbW_BQuark_p4        )); 
  double dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4     ));
  double dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::abs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4 ));

  double dRap_gtt_TQuark_gbb_BQuark                = std::abs( mcTools.GetRapidity(gtt_TQuark_p4)     - mcTools.GetRapidity(gbb_BQuark_p4)            );
  double dRap_gtt_TQuark_gtt_tbW_BQuark            = std::abs( mcTools.GetRapidity(gtt_TQuark_p4)     - mcTools.GetRapidity(gtt_tbW_BQuark_p4)        ); 
  double dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::abs( mcTools.GetRapidity(gtt_tbW_BQuark_p4) - mcTools.GetRapidity(gtt_tbW_Wqq_Quark_p4)     );
  double dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::abs( mcTools.GetRapidity(gtt_tbW_BQuark_p4) - mcTools.GetRapidity(gtt_tbW_Wqq_AntiQuark_p4) );

  // Fill dR histos
  h_Htb_TQuark_Htb_BQuark_dR                ->Fill(dR_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dR                ->Fill(dR_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dR                ->Fill(dR_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            ->Fill(dR_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR     ->Fill(dR_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR ->Fill(dR_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dR                ->Fill(dR_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            ->Fill(dR_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);
  h_Htb_tbW_WBoson_Htb_BQuark_dR            ->Fill(dR_Htb_tbW_WBoson_Htb_BQuark); 
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dR        ->Fill(dR_Htb_tbW_WBoson_Htb_tbW_BQuark); 
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dR        ->Fill(dR_Htb_tbW_WBoson_gtt_tbW_BQuark); 
  h_Htb_tbW_WBoson_gbb_BQuark_dR            ->Fill(dR_Htb_tbW_WBoson_gbb_BQuark); 
  h_gtt_tbW_WBoson_Htb_BQuark_dR            ->Fill(dR_gtt_tbW_WBoson_Htb_BQuark); 
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dR        ->Fill(dR_gtt_tbW_WBoson_Htb_tbW_BQuark);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dR        ->Fill(dR_gtt_tbW_WBoson_gtt_tbW_BQuark);
  h_gtt_tbW_WBoson_gbb_BQuark_dR            ->Fill(dR_gtt_tbW_WBoson_gbb_BQuark);

  h_Htb_TQuark_Htb_BQuark_dEta                ->Fill(dEta_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dEta                ->Fill(dEta_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dEta                ->Fill(dEta_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dEta            ->Fill(dEta_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta         ->Fill(dEta_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta     ->Fill(dEta_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta     ->Fill(dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta ->Fill(dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dEta                ->Fill(dEta_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dEta            ->Fill(dEta_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta     ->Fill(dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta ->Fill(dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);
  h_Htb_tbW_WBoson_Htb_BQuark_dEta            ->Fill(dEta_Htb_tbW_WBoson_Htb_BQuark); 
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dEta        ->Fill(dEta_Htb_tbW_WBoson_Htb_tbW_BQuark); 
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dEta        ->Fill(dEta_Htb_tbW_WBoson_gtt_tbW_BQuark); 
  h_Htb_tbW_WBoson_gbb_BQuark_dEta            ->Fill(dEta_Htb_tbW_WBoson_gbb_BQuark); 
  h_gtt_tbW_WBoson_Htb_BQuark_dEta            ->Fill(dEta_gtt_tbW_WBoson_Htb_BQuark); 
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dEta        ->Fill(dEta_gtt_tbW_WBoson_Htb_tbW_BQuark);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dEta        ->Fill(dEta_gtt_tbW_WBoson_gtt_tbW_BQuark);
  h_gtt_tbW_WBoson_gbb_BQuark_dEta            ->Fill(dEta_gtt_tbW_WBoson_gbb_BQuark); 

  h_Htb_TQuark_Htb_BQuark_dPhi                ->Fill(dPhi_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dPhi                ->Fill(dPhi_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dPhi                ->Fill(dPhi_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dPhi            ->Fill(dPhi_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi         ->Fill(dPhi_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi     ->Fill(dPhi_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi     ->Fill(dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi ->Fill(dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dPhi                ->Fill(dPhi_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dPhi            ->Fill(dPhi_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi     ->Fill(dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi ->Fill(dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);
  h_Htb_tbW_WBoson_Htb_BQuark_dPhi            ->Fill(dPhi_Htb_tbW_WBoson_Htb_BQuark); 
  h_Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi        ->Fill(dPhi_Htb_tbW_WBoson_Htb_tbW_BQuark); 
  h_Htb_tbW_WBoson_gtt_tbW_BQuark_dPhi        ->Fill(dPhi_Htb_tbW_WBoson_gtt_tbW_BQuark); 
  h_Htb_tbW_WBoson_gbb_BQuark_dPhi            ->Fill(dPhi_Htb_tbW_WBoson_gbb_BQuark); 
  h_gtt_tbW_WBoson_Htb_BQuark_dPhi            ->Fill(dPhi_gtt_tbW_WBoson_Htb_BQuark); 
  h_gtt_tbW_WBoson_Htb_tbW_BQuark_dPhi        ->Fill(dPhi_gtt_tbW_WBoson_Htb_tbW_BQuark);
  h_gtt_tbW_WBoson_gtt_tbW_BQuark_dPhi        ->Fill(dPhi_gtt_tbW_WBoson_gtt_tbW_BQuark);
  h_gtt_tbW_WBoson_gbb_BQuark_dPhi            ->Fill(dPhi_gtt_tbW_WBoson_gbb_BQuark); 

  h_Htb_TQuark_Htb_BQuark_dRap                ->Fill(dRap_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dRap                ->Fill(dRap_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dRap                ->Fill(dRap_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dRap            ->Fill(dRap_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap         ->Fill(dRap_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap     ->Fill(dRap_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap     ->Fill(dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap ->Fill(dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dRap                ->Fill(dRap_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dRap            ->Fill(dRap_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap     ->Fill(dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap ->Fill(dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  
  // Leading B-quarks
  std::vector<math::XYZTLorentzVector> bQuarks_p4;
  bQuarks_p4.push_back(Htb_BQuark_p4);
  bQuarks_p4.push_back(Htb_tbW_BQuark_p4);
  bQuarks_p4.push_back(gbb_BQuark_p4);
  bQuarks_p4.push_back(gtt_tbW_BQuark_p4);
  /// Sort bQuarks by pT 
  std::sort( bQuarks_p4.begin(), bQuarks_p4.end(), PtComparator() );

  // Require at least 4 b-quarks for these plots
  if (bQuarks_p4.size() < 4) return;

  double deltaRMin = 999999.9;
  int deltaRMin_i  = -1;
  int deltaRMin_j  = -1;
  
  // For-loop: All (pT-sorted) b-quarks
  for (size_t i = 0; i < bQuarks_p4.size(); i++)
    {

      double dEta_1_2 = std::abs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(1).eta());
      double dEta_1_3 = std::abs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(2).eta());
      double dEta_1_4 = std::abs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(3).eta());
      double dPhi_1_2 = std::abs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(1).phi());
      double dPhi_1_3 = std::abs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(2).phi());
      double dPhi_1_4 = std::abs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(3).phi());
      //
      double dEta_2_3 = std::abs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(2).eta());
      double dEta_2_4 = std::abs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(3).eta());
      double dPhi_2_3 = std::abs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(2).phi());
      double dPhi_2_4 = std::abs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(3).phi());
      //
      double dEta_3_4 = std::abs(bQuarks_p4.at(2).eta() - bQuarks_p4.at(3).eta());
      double dPhi_3_4 = std::abs(bQuarks_p4.at(2).phi() - bQuarks_p4.at(3).phi());
           
      // Fill 2D histos
      h_BQuark1_BQuark2_dEta_Vs_dPhi->Fill( dEta_1_2 , dPhi_1_2 );
      h_BQuark1_BQuark3_dEta_Vs_dPhi->Fill( dEta_1_3 , dPhi_1_3 );
      h_BQuark1_BQuark4_dEta_Vs_dPhi->Fill( dEta_1_4 , dPhi_1_4 );
      h_BQuark2_BQuark3_dEta_Vs_dPhi->Fill( dEta_2_3 , dPhi_2_3 );
      h_BQuark2_BQuark4_dEta_Vs_dPhi->Fill( dEta_2_4 , dPhi_2_4 );
      h_BQuark3_BQuark4_dEta_Vs_dPhi->Fill( dEta_3_4 , dPhi_3_4 );

      if (i==0)
	{
	  h_BQuark1_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark1_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==1)
	{
	  h_BQuark2_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark2_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==2)
	{
	  h_BQuark3_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark3_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==3)
	{
	  h_BQuark4_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark4_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else{}

      for (size_t j = i+1; j < bQuarks_p4.size(); j++)
	{
	  
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bQuarks_p4.at(i), bQuarks_p4.at(j));

	  if (deltaR < deltaRMin)
	    {
	      deltaRMin = deltaR;
	      deltaRMin_i = i;
	      deltaRMin_j = j;
	    }	  
	}      
    } // For-loop: All (pT-sorted) b-quarks

  // std::cout << "deltaRMin = " << deltaRMin << ", i = " << deltaRMin_i << ", j = " << deltaRMin_j <<  ", nbjets = " << bQuarks_p4.size() << std::endl;  
  math::XYZTLorentzVector bQuarkPair_dRMin_p4 = bQuarks_p4.at(deltaRMin_i) + bQuarks_p4.at(deltaRMin_j);
  double bQuarkPair_dEta = std::abs(bQuarks_p4.at(deltaRMin_i).eta() - bQuarks_p4.at(deltaRMin_j).eta());
  double bQuarkPair_dPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bQuarks_p4.at(deltaRMin_i), bQuarks_p4.at(deltaRMin_j)));
  h_BQuarkPair_dRMin_pT   ->Fill( bQuarkPair_dRMin_p4.pt() );
  h_BQuarkPair_dRMin_dEta ->Fill( bQuarkPair_dEta );
  h_BQuarkPair_dRMin_dPhi ->Fill( bQuarkPair_dPhi );
  h_BQuarkPair_dRMin_dR   ->Fill( deltaRMin );
  h_BQuarkPair_dRMin_Mass ->Fill( bQuarkPair_dRMin_p4.mass() );
  h_BQuarkPair_dRMin_Eta1_Vs_Eta2->Fill( bQuarks_p4.at(deltaRMin_i).eta(), bQuarks_p4.at(deltaRMin_j).eta());
  h_BQuarkPair_dRMin_Phi1_Vs_Phi2->Fill( bQuarks_p4.at(deltaRMin_i).phi(), bQuarks_p4.at(deltaRMin_j).phi());
  h_BQuarkPair_dRMin_Pt1_Vs_Pt2  ->Fill(bQuarks_p4.at(deltaRMin_i).pt(), bQuarks_p4.at(deltaRMin_j).pt());
  h_BQuarkPair_dRMin_dEta_Vs_dPhi->Fill( bQuarkPair_dEta, bQuarkPair_dPhi);
  //
  if (selJets_p4.size() > 0)
    {
      h_BQuarkPair_dRMin_jet1_dEta ->Fill( std::abs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(0).eta()) );
      h_BQuarkPair_dRMin_jet1_dPhi ->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) ) );
      h_BQuarkPair_dRMin_jet1_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) );
    }

  if (selJets_p4.size() > 1)  
    {
      h_BQuarkPair_dRMin_jet2_dEta ->Fill( std::abs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(1).eta()) );
      h_BQuarkPair_dRMin_jet2_dPhi ->Fill( std::abs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) ) );
      h_BQuarkPair_dRMin_jet2_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) );
    }
  
  return;
}



vector<float> HtbKinematics::GetMomentumTensorEigenValues(std::vector<math::XYZTLorentzVector> jets,
						       float &C,
						       float &D,
						       float &H2){

  // Tensor required for calculation of: Sphericity, Aplanarity, Planarity
  // Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
  // Links:
  // https://cmssdt.cern.ch/SDT/doxygen/CMSSW_8_0_24/doc/html/d5/d29/EventShapeVariables_8h_source.html
  // https://cmssdt.cern.ch/SDT/doxygen/CMSSW_8_0_24/doc/html/dd/d99/classEventShapeVariables.html

  // Get the Linear Momentum Tensor
  TMatrixDSym MomentumTensor = ComputeMomentumTensor(jets, 1.0);

  // Find the Momentum-Tensor EigenValues (Q1, Q2, Q3)
  TMatrixDSymEigen eigen(MomentumTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  vector<float> eigenvalues(3);
  eigenvalues.at(0) = eigenvals(0); // Q1
  eigenvalues.at(1) = eigenvals(1); // Q2
  eigenvalues.at(2) = eigenvals(2); // Q3
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Calculate the eigenvalues sum (Requirement: Q1 + Q2 + Q3 = 1)
  float eigenSum = std::accumulate(eigenvalues.begin(), eigenvalues.end(), 0);
  if ( (eigenSum - 1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Q1+Q2+Q3=1. Found that Q1+Q2+Q3 = " << eigenSum << ", instead.";
    }

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);
  float Q3 = eigenvalues.at(2);

  // Sanity check on eigenvalues: Q1 >= Q2 >= Q3 (Q1 >= 0)
  bool bQ1Zero = (Q1 >= 0.0);
  bool bQ1Q2   = (Q1 >= Q2);
  bool bQ2Q3   = (Q2 >= Q3);
  bool bInequality = bQ1Zero * bQ1Q2 * bQ2Q3;
  
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2 >= Q3 (Q1 >= 0). Q1 = " << Q1 << ", Q2 = " << Q2 << ", Q3 = " << Q3;
    }

  // Calculate the linear combinations C and D
  C  = 3*(Q1*Q2 + Q1*Q3 + Q2*Q3); // Used to measure the 3-jet structure. Vanishes for perfece 2-jet event. Related to the 2nd Fox-Wolfram Moment (H2)
  D  = 27*Q1*Q2*Q3; // Used to measure the 4-jet structure. Vanishes for a planar event
  H2 = 1-C; // The C-measure is related to the second Fox-Wolfram moment (see below), $C = 1 - H_2$.

  // C
  if ( abs(C-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the quantity C satisfies the inequality: 0.0 <= C <= 1.0. Found that C = " << C;
    }

  // D
  if ( abs(C-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the quantity C satisfies the inequality: 0.0 <= D <= 1.0. Found that D = " << D;
    }

  // 2nd Fox-Wolfram Moment
  if ( abs(H2-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the 2nd Fox-Wolfram Moment (H2) satisfies the inequality: 0.0 <= H2 <= 1.0. Found that H2 = " << H2;
    }
  
  if (0)
    {

      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "C");
      vars.AddRowColumn(0, auxTools.ToString(C) );
      vars.AddRowColumn(0, "0.0 <= C <= 1.0");
      vars.AddRowColumn(0, "C = 3 x (Q1Q2 + Q1Q3 + Q2Q3");
      //
      vars.AddRowColumn(1, "D");
      vars.AddRowColumn(1, auxTools.ToString(D) );
      vars.AddRowColumn(1, "0.0 <= D <= 1.0");
      vars.AddRowColumn(1, "D = 27 x Q1 x Q2 x Q3");
      //
      vars.AddRowColumn(2, "2nd F-W Moment");
      vars.AddRowColumn(2, auxTools.ToString(H2) );
      vars.AddRowColumn(2, "0.0 <= H2 <= 1.0 ");
      vars.AddRowColumn(2, "H2 = 1-C");
      vars.Print();
    }

  return eigenvalues;
}


vector<float> HtbKinematics::GetMomentumTensorEigenValues2D(std::vector<math::XYZTLorentzVector> jets,
							 float &Circularity){

  // For Circularity, the momentum tensor is the 2¡Á2 submatrix of Mjk, normalized by the sum of pT instead by the sum of
  // This matrix has two eigenvalues Qi with 0 < Q1 < Q2. The following definition for the circularity C has been used:
  //  C = 2 ¡Á min (Q1,Q2) / (Q1 +Q2)
  // The circularity C is especially interesting for hadron colliders because it only uses the momentum values in x and y direction transverse
  // to the beam line. So C is a two dimensional event shape variable and is therefore independent from a boost along z. 
  // In addition, the normalization by the sum of the particle momenta makes C highly independent from energy calibration effects  (systematic uncertainty).
  // C takes small values for linear and high values for circular events. 
  
  // Find the Momentum-Tensor EigenValues (E1, E2)
  TMatrixDSym MomentumTensor = ComputeMomentumTensor2D(jets);
  TMatrixDSymEigen eigen(MomentumTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  vector<float> eigenvalues(2);
  eigenvalues.at(0) = eigenvals[0]; // Q1
  eigenvalues.at(1) = eigenvals[1]; // Q2
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);

  // Sanity check on eigenvalues: (Q1 > Q2)
  if (Q1 == 0) return eigenvalues;

  bool bInequality = (Q1 > 0 && Q1 > Q2);
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2. Found Q1 = " << Q1 << ", Q2 " << Q2;
    }
  
  // Calculate circularity
  Circularity = 2*std::min(Q1, Q2)/(Q1+Q2); // is this definition correct?

  if (0)
    {      
      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "Circularity");
      vars.AddRowColumn(0, auxTools.ToString(Circularity) );
      vars.AddRowColumn(0, "0.0 <= C <= 1.0 ");
      vars.AddRowColumn(0, "C = 2 ¡Á min (Q1,Q2)/(Q1+Q2)");
      vars.Print();
    }
  
  return eigenvalues;
}



vector<float> HtbKinematics::GetSphericityTensorEigenValues(std::vector<math::XYZTLorentzVector> jets,
							 float &y23, float &Sphericity, float &SphericityT, float &Aplanarity, 
							 float &Planarity, float &Y){

  // C, D parameters
  // Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
  // Links:
  // http://home.fnal.gov/~mrenna/lutp0613man2/node234.html

  // Sanity check: at least 3 jets (for 3rd-jet resolution)
  if( (jets.size()) < 3 )
    {
      vector<float> zeros(3, 0);
      return zeros;
    }

  // Sort the jets by pT (leading jet first)
  std::sort( jets.begin(), jets.end(), PtComparator() );  

  // Get the Sphericity Tensor
  TMatrixDSym SphericityTensor = ComputeMomentumTensor(jets, 2.0);

  // Find the Momentum-Tensor EigenValues (Q1, Q2, Q3)
  TMatrixDSymEigen eigen(SphericityTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  vector<float> eigenvalues(3);
  eigenvalues.at(0) = eigenvals(0); // Q1
  eigenvalues.at(1) = eigenvals(1); // Q2
  eigenvalues.at(2) = eigenvals(2); // Q3
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Calculate the eigenvalues sum (Requirement: Q1 + Q2 + Q3 = 1)
  float eigenSum = std::accumulate(eigenvalues.begin(), eigenvalues.end(), 0);
  if ( (eigenSum - 1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Q1+Q2+Q3=1. Found that Q1+Q2+Q3 = " << eigenSum << ", instead.";
    }

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);
  float Q3 = eigenvalues.at(2);

  // Sanity check on eigenvalues: Q1 >= Q2 >= Q3 (Q1 >= 0)
  bool bQ1Zero = (Q1 >= 0.0);
  bool bQ1Q2   = (Q1 >= Q2);
  bool bQ2Q3   = (Q2 >= Q3);
  bool bInequality = bQ1Zero * bQ1Q2 * bQ2Q3;
  
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2 >= Q3 (Q1 >= 0)";
    }


  // Calculate the event-shape variables
  float pT3Squared  = pow(jets.at(2).Pt(), 2);
  float HT2Squared  = pow(jets.at(0).Pt() + jets.at(1).Pt(), 2);
  y23         = pT3Squared/HT2Squared;
  Sphericity  = -1.0;
  SphericityT = -1.0;
  Aplanarity  = -1.0;
  Planarity   = -1.0;
  Y = (sqrt(3.0)/2.0)*(Q2-Q3); // (Since Q1>Q2, then my Q1 corresponds to Q3 when Q's are reversed-ordered). Calculate the Y (for Y-S plane)

  // Check the value of the third-jet resolution
  if (abs(y23-0.25) > 0.25 + 1e-4)
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that y23 satisfies the inequality: 0.0 <= y23 <= 0.25. Found that y23 = " << y23;
    }
  
  // Calculate the Sphericity (0 <= S <= 1). S~0 for a 2-jet event, and S~1 for an isotropic one
  Sphericity = 1.5*(Q2 + Q3); 
  if ( abs(Sphericity-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Sphericity (S) satisfies the inequality: 0.0 <= S <= 1.0. Found that S = " << Sphericity;
    }

  // Calculate the Sphericity (0 <= S <= 1). S~0 for a 2-jet event, and S~1 for an isotropic one
  SphericityT = 2.0*Q2/(Q1 + Q2); 
  if ( abs(SphericityT-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Transverse Sphericity (ST) satisfies the inequality: 0.0 <= ST <= 1.0. Found that ST = " << SphericityT;
    }

  // Calculate the Aplanarity (0 <= A <= 0.5).  It measures the transverse momentum component out of the event plane
  // A~0 for a planar event, A~0.5 for an isotropic one
  Aplanarity = 1.5*(Q3);
  if ( abs(Aplanarity-0.5) > 0.5 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Aplanarity (A) satisfies the inequality: 0.0 <= A <= 0.5";
    }

  // Calculate the Aplanarity (0 <= P <= 0.5)
  Planarity  = (2.0/3.0)*(Sphericity-2*Aplanarity);
  if ( abs(Planarity-0.5) > 0.5 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Planarity (P) satisfies the inequality: 0.0 <= P <= 0.5";
    }

  if (0)
    {

      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "y23");
      vars.AddRowColumn(0, auxTools.ToString(y23) );
      vars.AddRowColumn(0, "0.0 <= y23 <= 0.25");
      vars.AddRowColumn(0, "y23 = pow(jet3_Pt, 2) / pow(jet1_Pt + jet2_Pt, 2)" );
      //
      vars.AddRowColumn(1, "Sphericity");
      vars.AddRowColumn(1, auxTools.ToString(Sphericity) );
      vars.AddRowColumn(1, "0.0 <= S <= 1.0");
      vars.AddRowColumn(1, "S = 1.5 x (Q2 + Q3)");
      //
      vars.AddRowColumn(2, "Sphericity (T)");
      vars.AddRowColumn(2, auxTools.ToString(SphericityT) );
      vars.AddRowColumn(2, "0.0 <= S (T) <= 1.0");
      vars.AddRowColumn(2, "S (T) = (2 x Q2)/(Q1 + Q2)");
      //
      vars.AddRowColumn(3, "Aplanarity");
      vars.AddRowColumn(3, auxTools.ToString(Aplanarity) );
      vars.AddRowColumn(3, "0.0 <= A <= 0.5 ");
      vars.AddRowColumn(3, "A = 1.5 x Q3");
      //
      vars.AddRowColumn(4, "Planarity");
      vars.AddRowColumn(4, auxTools.ToString(Planarity) );
      vars.AddRowColumn(4, "0.0 <= P <= 0.5 ");
      vars.AddRowColumn(4, "P (2/3) x (S - 2A)");
      //
      vars.AddRowColumn(5, "Y");
      vars.AddRowColumn(5, auxTools.ToString(Y) );
      vars.AddRowColumn(5, "");
      vars.AddRowColumn(5, "Y = sqrt(3)/2 x (Q1 - Q2)");
      vars.Print();
    }
    
  return eigenvalues;
  
}

TMatrixDSym HtbKinematics::ComputeMomentumTensor(std::vector<math::XYZTLorentzVector> jets, double r)
{

  // r = 2: Corresponds to sphericity tensor (Get: Sphericity, Aplanarity, Planarity, ..)
  // r = 1: Corresponds to linear measures (Get: C, D, Second Fox-Wolfram moment, ...)
  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();
  
  if (r!=1.0 && r!=2.0)
    {
      throw hplus::Exception("LogicError") << "Invalid value r-value in computing the Momentum Tensor (r=" << r << ").  Supported valued are r=2.0 and r=1.0.";
    }
  
  // Sanity Check
  if ( jets.size() < 2 )
    {
      return momentumTensor;
    }
  
  // Declare the Matrix normalisation (sum of momentum magnitutes to power r). That is: sum(|p|^{r})
  double normalisation = 0.0;
  double trace = 0.0;

  // For-loop: Jets
  for (auto& jet: jets){
    
    // Get the |p|^2 of the jet
    double p2 = pow(jet.P(), 2); // jet.P(); 
    
    // For r=2, use |p|^{2}, for r=1 use |p| as the momentum weight
    double pR = ( r == 2.0 ) ? p2 : TMath::Power(p2, 0.5*r);
    
    // For r=2, use |1|, for r=1 use   (|p|^{2})^{-0.5} = |p|^{2 (-1/2)} = |p|^{-1} = 1.0/|p|
    double pRminus2 = ( r == 2.0 ) ? 1.0 : TMath::Power(p2, 0.5*r - 1.0); // 
    
    // Add pR to the matrix normalisation factor
    normalisation += pR;
       
    // Fill the momentum (r=1) or  sphericity (r=2) tensor (Must be symmetric: Mij = Mji)
    momentumTensor(0,0) += pRminus2*jet.px()*jet.px(); // xx
    momentumTensor(0,1) += pRminus2*jet.px()*jet.py(); // xy
    momentumTensor(0,2) += pRminus2*jet.px()*jet.pz(); // xz
    
    momentumTensor(1,0) += pRminus2*jet.py()*jet.px(); // yx
    momentumTensor(1,1) += pRminus2*jet.py()*jet.py(); // yy
    momentumTensor(1,2) += pRminus2*jet.py()*jet.pz(); // yz
    
    momentumTensor(2,0) += pRminus2*jet.pz()*jet.px(); // zx
    momentumTensor(2,1) += pRminus2*jet.pz()*jet.py(); // zy
    momentumTensor(2,2) += pRminus2*jet.pz()*jet.pz(); // zz
    
  }// for (auto& jet: jets){

  // Normalise the tensors to have unit trace (Mxx + Myy + Mzz = 1)
  momentumTensor *= (1.0/normalisation);
  trace = momentumTensor(0,0) + momentumTensor(1,1) + momentumTensor(2,2);
  
  // Print the tensor
  if (0)
    {
      std::cout << "\nMomentum Tensor (r = " << r << "):" << std::endl;
      Table tensor(" |  | ", "Text"); //LaTeX or Text    
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,0) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,1) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,2) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,0) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,1) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,2) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,0) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,1) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,2) ) );
      tensor.AddRowColumn(3, "");
      tensor.AddRowColumn(4, "Normalisation");
      tensor.AddRowColumn(4, auxTools.ToString(normalisation));
      tensor.AddRowColumn(5, "IsSymmetric");
      tensor.AddRowColumn(5, auxTools.ToString(momentumTensor.IsSymmetric()));
      tensor.AddRowColumn(6, "Determinant");
      tensor.AddRowColumn(6, auxTools.ToString(momentumTensor.Determinant()));
      tensor.AddRowColumn(7, "Trace");
      tensor.AddRowColumn(7, auxTools.ToString(trace));
      tensor.Print(false);
    }

  if ( abs(trace-1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the Momentum-Tensor (r = " << r << ") Trace is 1.0. Found that abs(trace-1) = " << abs(trace-1) << ", instead.";
    }

  return momentumTensor;
}



TMatrixDSym HtbKinematics::ComputeMomentumTensor2D(std::vector<math::XYZTLorentzVector> jets)
{

  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();
  
  // Sanity Check
  if ( jets.size() < 2 )
    {
      return momentumTensor;
    }
  
  // Declare the Matrix normalisation (sum of momentum magnitutes to power r). That is: sum(|p|^{r})
  double normalisation = 0.0;
  double trace = 0.0;

  // For-loop: Jets
  for (auto& jet: jets){
    
    // Get the pT
    double pT = jet.Pt();
    
    // Add pT to the matrix normalisation factor
    normalisation += pow(pT,2);
       
    // Fill the two-dimensional momentum tensor
    momentumTensor(0,0) += jet.px()*jet.px(); // xx
    momentumTensor(0,1) += jet.px()*jet.py(); // xy
    momentumTensor(1,0) += jet.py()*jet.px(); // yx
    momentumTensor(1,1) += jet.py()*jet.py(); // yy
    
  }// for (auto& jet: jets){

  // Normalise tensor to get the normalised 2-d momentum tensor
  momentumTensor *= (1.0/normalisation);
  trace = momentumTensor(0,0) + momentumTensor(1,1);
  
  // Print the tensor
  if (0)
    {
      std::cout << "\nNormalied 2-D Momentum Tensor"  << std::endl;
      Table tensor(" |  | ", "Text"); //LaTeX or Text    
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,0) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,1) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,0) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,1) ) );
      tensor.AddRowColumn(2, "");
      tensor.AddRowColumn(3, "Normalisation");
      tensor.AddRowColumn(3, auxTools.ToString(normalisation));
      tensor.AddRowColumn(4, "IsSymmetric");
      tensor.AddRowColumn(4, auxTools.ToString(momentumTensor.IsSymmetric()));
      tensor.AddRowColumn(5, "Determinant");
      tensor.AddRowColumn(5, auxTools.ToString(momentumTensor.Determinant()));
      tensor.AddRowColumn(6, "Trace");
      tensor.AddRowColumn(6, auxTools.ToString(trace));
      tensor.Print(false);
    }

  if ( abs(trace-1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the 2D Momentum-Tensor Trace is 1.0. Found that abs(trace-1) = " << abs(trace-1) << ", instead.";
    }

  return momentumTensor;
}


double HtbKinematics::GetAlphaT(std::vector<math::XYZTLorentzVector> jets,
			     float &HT,
			     float &JT,
			     float &MHT,
			     float &Centrality){

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /// AlphaT:
  /// Calculates the AlphaT variable, defined as an N-jets. This definition reproduces the kinematics of a 
  // di-jet system by constructing two pseudo-jets, which balance one another in Ht. 
  // The two pseudo-jets are formed from the combination of the N objects that minimizes the quantity
  /// DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                             
  //
  // Detailed Explanation: 
  // The method "alphaT()" of this class takes as input all jets in the event and uses them to form 
  // two Pseudo-Jets to describe the event. 
  // If there are NJets in a given event this means there are 2^{NJets-1} combinations to do this.
  // The methods does exactly that and for the combination which minimises the quantity
  // DeltaHt = Ht_PseudoJet1 - Ht_PseudoJet2,
  // it calculates the quantity alphaT.
  // The method "alphaT()" employs a double loop to recreate all the possilbe jet combinations 
  // out of NJets, by the use of an NJets-binary system. For example, if NJets=5, the loop
  // indices ("k" outside, "l" inside) run both from "k"=0 to "k"=2^{4}=16 . The upper limit of 
  // the outside loop is given by the expression:
  // 1<<(NJets-1)) = shift the number 1 by (NJets-1) positions to the left. 
  // So, for NJets=5  (i.e. 1  --> 1 0 0 0 0 ) 
  // This is now the way we will represent grouping into 2 Pseudo-Jets. The 0's represent one group and the 1's the other.
  // So, for example 1 0 0 0 0 means 1 jet forms Pseudo-Jet1 and 4 jets form Pseudo-Jet2. 
  // Also, for example, 1 0 0 1 0 means 2 jets form Pseudo-Jet1 and 3 jets form Pseudo-Jet2.
  // The inside loop performs a bitwise right shift of index "k" by "l" positions and then
  // compares the resulting bit to 1. So, for "k"=0, all the resulting comparisons in the 
  // inside loop will result to 0, except the one with "l"=4.
  // This gives the first combination: 0 0 0 0 0   ( i.e. 0 jets form Pseudo-Jet1 and 5 jets form Pseudo-Jet2 )
  // For "k"=1 (00000001 in 8bit representation), the first comparison is 1, since k is shifted by zero positions 
  // and then compared to 1. The rest comparisons yield zero, since by shifting the bit by any position and comparing to 1 gives zero. 
  // Thus, for "k"=1 we have after the second loop: 0 0 0 0 1
  // In the same manner, we get for "k"=2 (00000001 in 8bit representation) we have after the second loop: 0 0 0 1 0
  //  To summarise, for NJets=5 we have 16 combinations:
  // For "k"=0  ( 00000000 in 8bit representation) we have after the second loop: 0 0 0 0 0
  // For "k"=1  ( 00000001 in 8bit representation) we have after the second loop: 0 0 0 0 1
  // For "k"=2  ( 00000001 in 8bit representation) we have after the second loop: 0 0 0 1 0
  // For "k"=3  ( 00000011 in 8bit representation) we have after the second loop: 0 0 0 1 1
  // For "k"=4  ( 00000100 in 8bit representation) we have after the second loop: 0 0 1 0 0
  // For "k"=5  ( 00000101 in 8bit representation) we have after the second loop: 0 0 1 0 1
  // For "k"=6  ( 00000110 in 8bit representation) we have after the second loop: 0 0 1 1 0
  // For "k"=7  ( 00000111 in 8bit representation) we have after the second loop: 0 0 1 1 1
  // For "k"=8  ( 00001000 in 8bit representation) we have after the second loop: 0 1 0 0 0
  // For "k"=9  ( 00001001 in 8bit representation) we have after the second loop: 0 1 0 0 1
  // For "k"=10 ( 00010000 in 8bit representation) we have after the second loop: 0 1 0 0 0
  // For "k"=11 ( 00010001 in 8bit representation) we have after the second loop: 0 1 0 0 1
  // For "k"=12 ( 00010010 in 8bit representation) we have after the second loop: 0 1 0 1 0
  // For "k"=13 ( 00010011 in 8bit representation) we have after the second loop: 0 1 0 1 1
  // For "k"=14 ( 00010100 in 8bit representation) we have after the second loop: 0 1 1 0 0
  // For "k"=15 ( 00010101 in 8bit representation) we have after the second loop: 0 1 1 0 1
  // For "k"=16 ( 00010110 in 8bit representation) we have after the second loop: 0 1 1 1 0
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

  /// Declaration of variables 
  unsigned nJets = jets.size();

  // Sanity Check
  if ( jets.size() < 2 )
    {
      return -1.0;
    }

  std::vector<float> vE, vEt, vPx, vPy, vPz;
  std::vector<bool> vPseudo_jet1;
  const bool bList = true;

  // For-Loop: All jets
  for (auto& jet: jets){
    vE.push_back( jet.E() );
    vEt.push_back( jet.Et() );
    vPx.push_back( jet.Px() );
    vPy.push_back( jet.Py() );
    vPz.push_back( jet.Pz() );
  }

  // Calculate sums
  float fSum_e  = accumulate( vE.begin() , vE.end() , 0.0 );
  float fSum_et = accumulate( vEt.begin(), vEt.end(), 0.0 );
  float fSum_px = accumulate( vPx.begin(), vPx.end(), 0.0 );
  float fSum_py = accumulate( vPy.begin(), vPy.end(), 0.0 );

  // Minimum Delta Et for two pseudo-jets
  float fMin_delta_sum_et = -1.0;

  // Iterate through different combinations
  for ( unsigned k=0; k < unsigned(1<<(nJets-1)); k++ ) { 
    float fDelta_sum_et = 0.0;
    std::vector<bool> jet;

    // Iterate through jets
    for ( unsigned l=0; l < vEt.size(); l++ ) { 
      /// Bitwise shift of "k" by "l" positions to the right and compare to 1 (&1)
      /// i.e.: fDelta_sum_et += vEt[l] * ( 1 - 2*0 );  if comparison is un-successful
      ///  or   fDelta_sum_et += vEt[l] * ( 1 - 2*1 );  if comparison is successful
      // in this way you add up all Et from PseudoJetsGroupA (belonging to 0's group) and subtract that from PseudoJetsGroupB (1's group)
      fDelta_sum_et += vEt[l] * ( 1 - 2 * (int(k>>l)&1) ); 
      if ( bList ) { jet.push_back( (int(k>>l)&1) == 0 ); } 
    }

    // Find configuration with minimum value of DeltaHt 
    if ( ( fabs(fDelta_sum_et) < fMin_delta_sum_et || fMin_delta_sum_et < 0.0 ) ) {
      fMin_delta_sum_et = fabs(fDelta_sum_et);
      if ( bList && jet.size() == vEt.size() ){vPseudo_jet1.resize(jet.size());}
    }

  }
    
  // Sanity check
  if ( fMin_delta_sum_et < 0.0 )
    { 
      throw hplus::Exception("LogicError") << "Minimum Delta(Sum_Et) is less than zero! fMin_delta_sum_et = " << fMin_delta_sum_et;
    }
  
  // Calculate Event-Shape Variables
  float dHT = fMin_delta_sum_et;
  HT  = fSum_et;
  JT  = fSum_et - vEt.at(0); // Ht without considering the Ldg Jet of the Event
  MHT = sqrt(pow(fSum_px,2) + pow(fSum_py,2));
  Centrality = fSum_et/fSum_e;
  float AlphaT = ( 0.5 * ( HT - dHT ) / sqrt( pow(HT,2) - pow(MHT,2) ) );

  if (0)
    {

      Table vars("Variable | Value | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "HT");
      vars.AddRowColumn(0, auxTools.ToString(HT) );
      vars.AddRowColumn(0, "HT = Sum(Jet_Et)");
      //
      vars.AddRowColumn(1, "JT");
      vars.AddRowColumn(1, auxTools.ToString(JT) );
      vars.AddRowColumn(1, "JT = Ht - Jet1_Et");
      //
      vars.AddRowColumn(2, "dHT");
      vars.AddRowColumn(2, auxTools.ToString(dHT) );
      vars.AddRowColumn(2, "DeltaHT = min[Delta(Pseudojet1_Et, Pseudojet2_Et)]");
      //
      vars.AddRowColumn(3, "MHT");
      vars.AddRowColumn(3, auxTools.ToString(MHT) );
      vars.AddRowColumn(3, "MHT = sqrt( pow(Sum(px), 2) + pow(Sum(py), 2))");
      //
      vars.AddRowColumn(4, "AlphaT");
      vars.AddRowColumn(4, auxTools.ToString(AlphaT) );
      vars.AddRowColumn(4, "AlphaT = 0.5 x (HT - dHT) /sqr( pow(HT, 2) - pow(MHT, 2))");
      vars.Print();
    }

  return AlphaT;
}

vector<GenJet> HtbKinematics::GetGenJets(const vector<GenJet> genJets, std::vector<float> ptCuts, std::vector<float> etaCuts, vector<genParticle> genParticlesToMatch)
{
  /*
    Jet-Flavour Definitions (https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools)

    Algorithmic definition: (NOTE: Algorithmic definition is used by default for all b-tagging purposes)
    - Try to find the parton that most likely determines the properties of the jet and assign that flavour as the true flavour
    - Here, the ¡°final state¡± partons (after showering, radiation) are analyzed (within ¦¤R < 0.3 of the reconstructed jet axis). 
    Partons selected for the algorithmic definition are those partons that don't have other partons as daughters, 
    without any explicit requirement on their status (for Pythia6 these are status=2 partons).
    - Jets from radiation are matched with full efficiency
    -If there is a b/c within the jet cone: label as b/c
    -Otherwise: assign flavour of the hardest parton
   */

  // Definitions
  std::vector<GenJet> jets;
  unsigned int jet_index   = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;

  // For-loop: All genParticles
  for (auto& p: genParticlesToMatch) 
    {
      
      // Comparison variables
      double dR   = 1e6;
      double dPt  = 1e6;
      double dEta = 1e6;
      double dPhi = 1e6;
	  
      // For-loop: All Generated Jets
      for (auto jet: genJets) 
	{
	  
	  // Jet index (for pT and eta cuts)
	  jet_index++;
	  
	  dPt  = jet.pt() - p.pt();
	  dEta = jet.eta() - p.eta();
	  dPhi = jet.phi() - p.phi();
       	  dR   = ROOT::Math::VectorUtil::DeltaR(jet.p4(), p.p4());
      
	  // Fail to match
	  if (dR > 0.3) continue;
	  
	  // Apply cuts after the matching
	  const float ptCut  = ptCuts.at(ptCut_index);
	  const float etaCut = etaCuts.at(etaCut_index);
	  if (jet.pt() < ptCut) continue;
	  if (std::abs(jet.eta()) > etaCut) continue;
	  
	  // Save this particle
	  jets.push_back(jet);
	  if (0) std::cout << "dR = " << dR << ": dPt = " << dPt << ", dEta = " << dEta << ", dPhi = " << dPhi << std::endl;

	  // Increment cut index only. Cannot be bigger than the size of the cut list provided
	  if (ptCut_index  < ptCuts.size()-1  ) ptCut_index++;
	  if (etaCut_index < etaCuts.size()-1  ) etaCut_index++;
	  break;
	}
    }
  if (0) std::cout << "bjets.size() = " << jets.size() << std::endl;
  return jets;
}

vector<GenJet> HtbKinematics::GetGenJets(const GenJetCollection& genJets, std::vector<float> ptCuts, std::vector<float> etaCuts)
{
  std::vector<GenJet> jets;

  // Definitions
  unsigned int jet_index   = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;

  // For-loop: All Generated Jets
  for (auto jet: genJets) 
    {

      // Jet index (for pT and eta cuts)
      jet_index++;
      
      // Apply cuts
      const float ptCut  = ptCuts.at(ptCut_index);
      const float etaCut = etaCuts.at(etaCut_index);
      if (jet.pt() < ptCut) continue;
      if (std::abs(jet.eta()) > etaCut) continue;

      // Save this particle
      jets.push_back(jet);

      // Increment cut index only. Cannot be bigger than the size of the cut list provided
      if (ptCut_index  < ptCuts.size()-1  ) ptCut_index++;
      if (etaCut_index < etaCuts.size()-1  ) etaCut_index++;
    }
  return jets;
}

vector<genParticle> HtbKinematics::GetGenParticles(const vector<genParticle> genParticles, double ptCut, double etaCut, const int pdgId, const bool isLastCopy, const bool hasNoDaughters)
  {
  
  std::vector<genParticle> particles;

  // For-loop: All genParticles
  for (auto& p: genParticles) 
    {
      // Find last copy of a given particle
      if (isLastCopy) if (!p.isLastCopy()) continue;      

      // Commonly enables for parton-based jet flavour definition
      if (hasNoDaughters) if (p.daughters().size() > 0) continue;

      // Consider only particles
      if (std::abs(p.pdgId()) != pdgId) continue;
      
      // Apply cuts
      if ( p.pt() < ptCut ) continue;
      if (std::abs(p.eta()) > etaCut) continue;
      
      // Save this particle
      particles.push_back(p);
    }
  return particles;
  }

