// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "Tools/interface/MCTools.h"
#include "Auxiliary/interface/Tools.h"
#include "Auxiliary/interface/Table.h"
#include "Tools/interface/DirectionalCut.h"

//#include "HistoWrapper.h"
//#include "BaseSelector.h"


#include "TDirectory.h"
#include "Math/VectorUtil.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"
#include "TVectorT.h"
#include "TVectorD.h"

#include "TTree.h"
#include "TBranch.h"
#include <TLorentzVector.h>

class HplusHadronic: public BaseSelector {
public:
  explicit HplusHadronic(const ParameterSet& config, const TH1* skimCounters);
  virtual ~HplusHadronic() {}

  /// Books histograms
  virtual void book(TDirectory *dir ) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;


private:
  // Input parameters
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;
  const HistogramSettings cfg_PhiBinSetting;
  const HistogramSettings cfg_MassBinSetting;
  const HistogramSettings cfg_DeltaEtaBinSetting;
  const HistogramSettings cfg_DeltaPhiBinSetting;
  const HistogramSettings cfg_DeltaRBinSetting;


  Tools auxTools;


  // Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  // Count cFakeTauSFCounter;
  // Count cTauTriggerSFCounter;
  // Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  TopologySelection fTopologySelection;
  TopSelection fTopSelection;
  Count cSelected;
    
  // Event-Shape Variables - Histograms
  WrappedTH1 *h_HT;
  WrappedTH1 *h_MHT;
  WrappedTH1 *h_Sphericity;
  WrappedTH1 *h_Aplanarity;
  WrappedTH1 *h_Planarity;
  WrappedTH1 *h_DParameter;
  WrappedTH1 *h_H2;
  WrappedTH1 *h_Circularity;
  WrappedTH1 *h_Centrality;
  WrappedTH1 *h_AlphaT;

  //  WrappedTH1 *h_METoverSqrtHT;
  WrappedTH1 *h_R32_LdgTop;
  WrappedTH1 *h_R32_SubLdgTop;

  // Jets 
  WrappedTH1 *h_Jets_N;
  WrappedTH1 *h_recoJet1_Pt;
  WrappedTH1 *h_recoJet2_Pt;
  WrappedTH1 *h_recoJet3_Pt;
  WrappedTH1 *h_recoJet4_Pt;
  WrappedTH1 *h_recoJet5_Pt;
  WrappedTH1 *h_recoJet6_Pt;
  WrappedTH1 *h_recoJet7_Pt;
  WrappedTH1 *h_recoJet8_Pt;
  WrappedTH1 *h_recoJet1_AbsEta;
  WrappedTH1 *h_recoJet2_AbsEta;
  WrappedTH1 *h_recoJet3_AbsEta;
  WrappedTH1 *h_recoJet4_AbsEta;
  WrappedTH1 *h_recoJet5_AbsEta;
  WrappedTH1 *h_recoJet6_AbsEta;
  WrappedTH1 *h_recoJet5_BJetsFirst_Pt;
  WrappedTH1 *h_recoJet6_BJetsFirst_Pt;
  WrappedTH1 *h_recoJet7_BJetsFirst_Pt;
  vector<WrappedTH1*> vh_recoJets_Pt;
  vector<WrappedTH1*> vh_recoJets_AbsEta;
  

  // B-Tagged Jets
  WrappedTH1 *h_BJets_N;
  WrappedTH1 *h_BJet1_Pt;
  WrappedTH1 *h_BJet2_Pt;
  WrappedTH1 *h_BJet3_Pt;
  WrappedTH1 *h_BJet1_AbsEta;
  WrappedTH1 *h_BJet2_AbsEta;
  WrappedTH1 *h_BJet3_AbsEta;
  vector<WrappedTH1*> vh_BJets_Pt;
  vector<WrappedTH1*> vh_BJets_AbsEta;

  // untagged Jets
  WrappedTH1 *h_untaggedJets_N;

  // B-Jet Pair
  WrappedTH1 *h_BJetPair_dPhiAverage;
  WrappedTH1 *h_BJetPair_dRAverage;
  WrappedTH1 *h_BJetPair_dEtaAverage;
  WrappedTH1 *h_BJetPair_Rbb;
  WrappedTH1 *h_BJetPair_MaxPt_Pt;
  WrappedTH1 *h_BJetPair_MaxPt_M;
  WrappedTH1 *h_BJetPair_MaxMass_Pt;
  WrappedTH1 *h_BJetPair_MaxMass_M;
  WrappedTH1 *h_BJetPair_dRMin_Pt;
  WrappedTH1 *h_BJetPair_dRMin_dR;
  WrappedTH1 *h_BJetPair_dRMin_Mass;
  WrappedTH1 *h_BJetPair_dRMin_dEta;
  WrappedTH1 *h_BJetPair_dRMin_dPhi;
  WrappedTH1 *h_BJetPair_dRMin_Rbb;
  WrappedTH1 *h_BJetPair_dPhiMin_Pt;
  WrappedTH1 *h_BJetPair_dPhiMin_Mass;
  WrappedTH1 *h_BJetPair_dPhiMax_Pt;
  WrappedTH1 *h_BJetPair_dPhiMax_Mass;

  // dR of Ldg Jet and dRMin BJet Pair 
  WrappedTH1 *h_ldgJet_dRMinBJetPair_dR; 
  WrappedTH1 *h_ldgJet_dRMinBJetPair_dEta;
  WrappedTH1 *h_ldgJet_dRMinBJetPair_dPhi;

  // dR of untagged Ldg Jet and dRMin BJet Pair                                                                             
  WrappedTH1 *h_untaggedLdgJet_dRMinBJetPair_dR;
  WrappedTH1 *h_untaggedLdgJet_dRMinBJetPair_dEta;
  WrappedTH1 *h_untaggedLdgJet_dRMinBJetPair_dPhi;

  // Di-Jet
  WrappedTH1 *h_dRMinDiJet_noBJets_Pt;
  WrappedTH1 *h_dRMinDiJet_noBJets_M;

  // Tri-Jet
  WrappedTH1 *h_TriJet_MaxPt_Pt;
  WrappedTH1 *h_TriJet_MaxPt_Mass;


  // Minimum and Maximum phi angle between a jet and (MHT-jet)
  WrappedTH1 *h_minDeltaPhiJetMHT;
  WrappedTH1 *h_maxDeltaPhiJetMHT;

  // Minimum Delta R between a jet and (MHT-jet), -(MHT-jet)
  WrappedTH1 *h_minDeltaRJetMHT;
  WrappedTH1 *h_minDeltaRReversedJetMHT;


  // Average CSV Discriminator for all jets                                                                                               
  WrappedTH1 *h_AvgCSV;
  WrappedTH1 *h_AvgCSV_PtWeighted;
  WrappedTH1 *h_AvgCSV_PtSqrWeighted;

  // Average CSV Discriminator for non-bjets                                                                                              
  WrappedTH1 *h_AvgCSV_noBjets;
  WrappedTH1 *h_AvgCSV_PtWeighted_noBjets;
  WrappedTH1 *h_AvgCSV_PtSqrWeighted_noBjets;



  // ====== Top Reconstruction (Distances - chi^2)

  // LdgTop
  WrappedTH1 *h_LdgTop_Pt;
  WrappedTH1 *h_LdgTop_Eta;
  WrappedTH1 *h_LdgTop_Phi;
  WrappedTH1 *h_LdgTop_Mass;

  // SubLdgTop                                                                    
  WrappedTH1 *h_SubLdgTop_Pt;
  WrappedTH1 *h_SubLdgTop_Eta;
  WrappedTH1 *h_SubLdgTop_Phi;
  WrappedTH1 *h_SubLdgTop_Mass;

  // BJets Distances                                                                                                                
  WrappedTH1 *h_BJet1BJet2_dR;
  WrappedTH1 *h_BJet1BJet2_dPhi;
  WrappedTH1 *h_BJet1BJet2_dEta;
  
  // DiJet-BJet Distances
  WrappedTH1 *h_DiJet1BJet1_dR;
  WrappedTH1 *h_DiJet1BJet1_dPhi;
  WrappedTH1 *h_DiJet1BJet1_dEta;
  //
  WrappedTH1 *h_DiJet1BJet2_dR;
  WrappedTH1 *h_DiJet1BJet2_dPhi;
  WrappedTH1 *h_DiJet1BJet2_dEta;
  //
  WrappedTH1 *h_DiJet2BJet1_dR;
  WrappedTH1 *h_DiJet2BJet1_dPhi;
  WrappedTH1 *h_DiJet2BJet1_dEta;
  //
  WrappedTH1 *h_DiJet2BJet2_dR;
  WrappedTH1 *h_DiJet2BJet2_dPhi;
  WrappedTH1 *h_DiJet2BJet2_dEta;
  
  // TriJet-BJet Distances
  WrappedTH1 *h_TriJet1BJet1_dR;
  WrappedTH1 *h_TriJet1BJet1_dEta;
  WrappedTH1 *h_TriJet1BJet1_dPhi;
  //
  WrappedTH1 *h_TriJet1BJet2_dR;
  WrappedTH1 *h_TriJet1BJet2_dEta;
  WrappedTH1 *h_TriJet1BJet2_dPhi;
  //           
  WrappedTH1 *h_TriJet2BJet1_dR;
  WrappedTH1 *h_TriJet2BJet1_dEta;
  WrappedTH1 *h_TriJet2BJet1_dPhi;
  //           
  WrappedTH1 *h_TriJet2BJet2_dR;
  WrappedTH1 *h_TriJet2BJet2_dEta;
  WrappedTH1 *h_TriJet2BJet2_dPhi;


  // 3rd BJet and Top Distances 
  WrappedTH1 *h_BJet3_LdgTop_dR;
  WrappedTH1 *h_BJet3_LdgTop_dEta;
  WrappedTH1 *h_BJet3_LdgTop_dPhi;
  WrappedTH1 *h_BJet3_SubLdgTop_dR;
  WrappedTH1 *h_BJet3_SubLdgTop_dEta;
  WrappedTH1 *h_BJet3_SubLdgTop_dPhi;

  // Chi Square
  WrappedTH1 *h_top_ChiSqr;
  WrappedTH1 *h_top_RedChiSqr;
  WrappedTH2 *h_H2_Vs_ChiSqr;



  //New Variables from FP
  WrappedTH1 *h_DPhi_LdgTrijet_SubldgTrijet;  
  WrappedTH1 *h_Rapidity_LdgTrijet;
  WrappedTH1 *h_Rapidity_SubldgTrijet;
  WrappedTH1 *h_Rapidity_Tetrajet;
  WrappedTH1 *h_SumPt_LdgTrijet_SubldgTrijet;

  WrappedTH1 *h_CosTheta_Bjet1TopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_Bjet1TopCM_Zaxis;
  WrappedTH1 *h_CosTheta_Bjet2TopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_Bjet2TopCM_Zaxis;
  WrappedTH1 *h_CosTheta_Bjet3TopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_Bjet3TopCM_Zaxis;

  WrappedTH1 *h_METoverSqrtHT;

  WrappedTH1 *h_CosTheta_LdgTrijetLdgJetTopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_LdgTrijetBjetTopCM_TrijetLab;

  WrappedTH1 *h_CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab;
  WrappedTH1 *h_CosTheta_SubldgTrijetBjetTopCM_TrijetLab;

  //MVA input variables
  WrappedTH1 *h_DEta_LdgTrijetDijet_TetrajetB;

  //=== scatterplots ===//
  WrappedTH2 *h_DPhiJ12vsDPhiJ34;
  WrappedTH2 *h_DEtaJ12vsDEtaJ34;
  WrappedTH2 *h_DRJ12vsDRJ34;

  WrappedTH2 *h_DPhiJ12vsDPhiJ56;
  WrappedTH2 *h_DEtaJ12vsDEtaJ56;
  WrappedTH2 *h_DRJ12vsDRJ56;

  WrappedTH2 *h_DPhiJ34vsDPhiJ56;
  WrappedTH2 *h_DEtaJ34vsDEtaJ56;
  WrappedTH2 *h_DRJ34vsDRJ56;

  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut025;
  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut05;
  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut075;
  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut10;
  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut125;
  WrappedTH2 *h_DPhiJ34vsDPhiJ56_wCut15;
  //====================//

  WrappedTH1 *h_DPhi_LdgTrijetB_SubldgTrijetB;
  WrappedTH1 *h_DPhi_TetrajetB_SubldgTrijetB;
  WrappedTH1 *h_DPhi_TetrajetB_LdgTrijetB;
  WrappedTH1 *h_DEta_LdgTrijetB_SubldgTrijetB;
  WrappedTH1 *h_DEta_TetrajetB_SubldgTrijetB;
  WrappedTH1 *h_DEta_TetrajetB_LdgTrijetB;
  WrappedTH1 *h_DR_LdgTrijetB_SubldgTrijetB;
  WrappedTH1 *h_DR_TetrajetB_SubldgTrijetB;
  WrappedTH1 *h_DR_TetrajetB_LdgTrijetB;
  
  WrappedTH1 *h_PtAsy;

  WrappedTH1 *h_Tetrajet_Mass;
  WrappedTH1 *h_HTminusSumScPt_LdgTop_SubldgTop;
  WrappedTH1 *h_HTminusSumVecPt_LdgTop_SubldgTop;

  WrappedTH1 *h_DPhiJ34;
  WrappedTH1 *h_DPhiJ56;
  WrappedTH1 *h_DPhiDistance_J34_J56;
  WrappedTH1 *h_DPhiCircle_J34_J56;

  //next Wrapped

  // TTree - TBranches
  TTree *tree;

  TBranch *weight;
  TBranch *LdgJet_Pt;                
  TBranch *H2;                       
  TBranch *HT; 
  TBranch *TriJet_maxPt_M;           
  TBranch *Centrality;  
  TBranch *Jets_N;
  TBranch *BJets_N;

  TBranch *recoJet2_Pt;
  TBranch *recoJet3_Pt;
  TBranch *recoJet4_Pt;
  TBranch *recoJet5_Pt;
  TBranch *recoJet6_Pt;
  TBranch *recoJet7_Pt;

  TBranch *LdgTop_Pt;
  TBranch *LdgTop_Eta;
  TBranch *LdgTop_Phi;
  TBranch *LdgTop_Mass;
  TBranch *SubLdgTop_Pt;
  TBranch *SubLdgTop_Eta;
  TBranch *SubLdgTop_Phi;
  TBranch *SubLdgTop_Mass;

  //Additional branches - Soti
  TBranch *Sphericity;
  TBranch *Circularity;
  TBranch *LdgTetraJet_Pt;
  TBranch *LdgTetraJet_Mass;
  TBranch *LdgBjet_Pt;
  TBranch *TopChiSqr;

  TBranch *SubldgTetrajet_Pt;
  TBranch *SubldgTetrajet_Mass;

  TBranch *DEta_TetrajetB_LdgTrijetB;
  TBranch *DEta_Dijet_LdgTrijetB;
  TBranch *DEta_LdgTrijetDijet_TetrajetB;
  TBranch *DEta_LdgTrijet_TetrajetB;
  //New DEta from Alexandros
  TBranch *DEta_LdgTrijetB_SubldgTrijetB;
  TBranch *DEta_TetrajetB_SubldgTrijetB;

  TBranch *DPhi_TetrajetB_LdgTrijetB;
  TBranch *DPhi_Dijet_LdgTrijetB;
  TBranch *DPhi_LdgTrijetDijet_TetrajetB;
  TBranch *DPhi_LdgTrijet_TetrajetB;
  //New DPhi from Alexandros
  TBranch *DPhi_LdgTrijetB_SubldgTrijetB;
  TBranch *DPhi_TetrajetB_SubldgTrijetB;

  TBranch *DR_TetrajetB_LdgTrijetB;
  TBranch *DR_Dijet_LdgTrijetB;
  TBranch *DR_LdgTrijetDijet_TetrajetB;
  TBranch *DR_LdgTrijet_TetrajetB;
  //New DR from Alexandros
  TBranch *DR_LdgTrijetB_SubldgTrijetB;
  TBranch *DR_TetrajetB_SubldgTrijetB;

  TBranch* D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB;

  //From higgs_tb_exo
  TBranch* PtAsy; 
  TBranch* DPhi_LdgBjet_Trijet;
  TBranch* AvgCSV_PtWeighted;
  //From ATLAS NOTE
  TBranch* BJetPair_dRMin_M;
  TBranch* BJetPair_dRAvg;
  TBranch *BJetPair_maxPt_M;                                                                                        
  TBranch *BJetPair_maxMass_M;
  TBranch* DijetUntaggedSmallDR_Mass;
  TBranch* Jet5_BJetsFirst_Pt;

  //New variables from FP
  TBranch *DPhi_LdgTrijet_SubldgTrijet;
  TBranch *Rapidity_LdgTrijet;
  TBranch *Rapidity_SubldgTrijet;
  TBranch *Rapidity_Tetrajet;
  TBranch *SumPt_LdgTrijet_SubldgTrijet;

  TBranch *CosTheta_Bjet1TopCM_TrijetLab;
  TBranch *CosTheta_Bjet1TopCM_Zaxis;
  TBranch *CosTheta_Bjet2TopCM_TrijetLab;
  TBranch *CosTheta_Bjet2TopCM_Zaxis;
  TBranch *CosTheta_Bjet3TopCM_TrijetLab;
  TBranch *CosTheta_Bjet3TopCM_Zaxis;

  TBranch *CosTheta_LdgTrijetLdgJetTopCM_TrijetLab;
  TBranch *CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab;
  TBranch *CosTheta_LdgTrijetBjetTopCM_TrijetLab;

  TBranch *CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab;
  TBranch *CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab;
  TBranch *CosTheta_SubldgTrijetBjetTopCM_TrijetLab;

  TBranch *METoverSqrtHT;
  TBranch *HTminusSumScPt_LdgTop_SubldgTop;
  TBranch *HTminusSumVecPt_LdgTop_SubldgTop;
  
  TBranch *DPhiJ34;
  TBranch *DPhiJ56;
  TBranch *DPhiDistance_J34_J56;
  TBranch *DPhiCircle_J34_J56;


  //Variables from Analysis Note AN-16-437
  TBranch *LdgTrijetPtDR;
  TBranch *LdgTrijetDijetPtDR;
  TBranch *LdgTrijetBjetMass;
  TBranch *LdgTrijetLdgJetPt;
  TBranch *LdgTrijetLdgJetEta;
  TBranch *LdgTrijetLdgJetBDisc;
  TBranch *LdgTrijetSubldgJetPt;
  TBranch *LdgTrijetSubldgJetEta;
  TBranch *LdgTrijetSubldgJetBDisc;
  TBranch *LdgTrijetBJetLdgJetMass;
  TBranch *LdgTrijetBJetSubldgJetMass;

  TBranch *SubldgTrijetPtDR;
  TBranch *SubldgTrijetDijetPtDR;
  TBranch *SubldgTrijetBjetMass;
  TBranch *SubldgTrijetLdgJetPt;
  TBranch *SubldgTrijetLdgJetEta;
  TBranch *SubldgTrijetLdgJetBDisc;
  TBranch *SubldgTrijetSubldgJetPt;
  TBranch *SubldgTrijetSubldgJetEta;
  TBranch *SubldgTrijetSubldgJetBDisc;
  TBranch *SubldgTrijetBJetLdgJetMass;
  TBranch *SubldgTrijetBJetSubldgJetMass;
  
  TBranch *LdgTrijetDijetMass;
  TBranch *SubldgTrijetDijetMass;
  TBranch *LdgTrijetBJetBDisc;
  TBranch *SubldgTrijetBJetBDisc;
  
  //next TBranch

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(HplusHadronic);

HplusHadronic::HplusHadronic(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invMassBins")),// Problem Here!!
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplusHadronic, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    // cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")), cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
    // cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))
    //fDiscriminatorValue(0.5426) // for bjetDiscr = "pfCombinedInclusiveSecondaryVertexV2BJetTags", bjetDiscrWorkingPoint  = "Loose"

{ }


void HplusHadronic::book(TDirectory *dir) {

  //  TDirectory* myCtrlDir            = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, "ThisIsATest");
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
  fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  
  // Fixed-binning
  const int nBinsPt   = cfg_PtBinSetting.bins();
  const double minPt  = cfg_PtBinSetting.min();
  const double maxPt  = cfg_PtBinSetting.max();
  
  const int nBinsEta  = cfg_EtaBinSetting.bins();
  const double minEta = cfg_EtaBinSetting.min();
  const double maxEta = cfg_EtaBinSetting.max();
 
  const int nBinsPhi  = cfg_PhiBinSetting.bins();
  const double minPhi = cfg_PhiBinSetting.min();
  const double maxPhi = cfg_PhiBinSetting.max();

   
  const int nBinsM  = cfg_MassBinSetting.bins();
  const double minM = cfg_MassBinSetting.min();
  const double maxM = cfg_MassBinSetting.max();
  
  const int nBinsdEta  = cfg_DeltaEtaBinSetting.bins();
  const double mindEta = cfg_DeltaEtaBinSetting.min();
  const double maxdEta = cfg_DeltaEtaBinSetting.max();

  const int nBinsdPhi  = cfg_DeltaPhiBinSetting.bins();
  const double mindPhi = cfg_DeltaPhiBinSetting.min();
  const double maxdPhi = cfg_DeltaPhiBinSetting.max();

  const int nBinsdR  = cfg_DeltaRBinSetting.bins();
  const double mindR = cfg_DeltaRBinSetting.min();
  const double maxdR = cfg_DeltaRBinSetting.max();


  // Event-Shape Variables - Histograms
  h_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "HT"         , ";H_{T}"      , 60, 0.0, 2500.0);
  h_MHT         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MHT"        , ";MHT"        , 30, 0.0,  300.0);
  h_Sphericity  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Sphericity" , ";Sphericity" , 20, 0.0,   1.00);
  h_Aplanarity  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Aplanarity" , ";Aplanarity" , 25, 0.0, 0.5);
  h_Planarity   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Planarity"  , ";Planarity"  , 25, 0.0, 0.5);
  h_DParameter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DParameter" , ";D"          , 20, 0.0, 1.0);
  h_H2          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "H2"         , ";H_{2}"      , 40, 0.0, 1.0);
  h_Circularity = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Circularity", ";Circularity", 40, 0.0, 1.0);
  h_Centrality  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Centrality" , ";Centrality" , 20, 0.0, 1.0);
  h_AlphaT      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AlphaT"     , ";#alpha_{T}" , 20, 0.0, 1.0);

  
  //  h_METoverSqrtHT  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "METoverSqrtHT" , ";E_{T}^{miss}/#sqrt{H_{T}}"  , 25, 0.0, 0.5);
  h_R32_LdgTop     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "R32_LdgTop"    , ";R_{3/2}"      , 20, 0.0,  8.0);
  h_R32_SubLdgTop  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "R32_SubLdgTop" , ";R_{3/2}"      , 20, 0.0,  8.0);
 

  // Jets
  h_Jets_N = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Jets_N" , ";N (jets)" , 17, -0.5, +16.5);
  h_recoJet1_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet2_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet3_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet4_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet4_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet5_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet5_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet6_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet6_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet7_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet7_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet8_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet8_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet1_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet1_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_recoJet2_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet2_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_recoJet3_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet3_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_recoJet4_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet4_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_recoJet5_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet5_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_recoJet6_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet6_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta); 
  h_recoJet5_BJetsFirst_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet5_BJetsFirst_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet6_BJetsFirst_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet6_BJetsFirst_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_recoJet7_BJetsFirst_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "recoJet7_BJetsFirst_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);


  // To ease manipulation put in vector                                                                           
  vh_recoJets_Pt.push_back(h_recoJet1_Pt);
  vh_recoJets_Pt.push_back(h_recoJet2_Pt);
  vh_recoJets_Pt.push_back(h_recoJet3_Pt);
  vh_recoJets_Pt.push_back(h_recoJet4_Pt);
  vh_recoJets_Pt.push_back(h_recoJet5_Pt);
  vh_recoJets_Pt.push_back(h_recoJet6_Pt);
  //                                                                                                                           
  vh_recoJets_AbsEta.push_back(h_recoJet1_AbsEta);                                                                                    
  vh_recoJets_AbsEta.push_back(h_recoJet2_AbsEta);
  vh_recoJets_AbsEta.push_back(h_recoJet3_AbsEta);
  vh_recoJets_AbsEta.push_back(h_recoJet4_AbsEta);
  vh_recoJets_AbsEta.push_back(h_recoJet5_AbsEta);
  vh_recoJets_AbsEta.push_back(h_recoJet6_AbsEta);



  // B-Tagged Jets
  h_BJets_N      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJets_N" , ";N (b-jets)" , 10, -0.5, +9.5);
  h_BJet1_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_BJet2_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_BJet3_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_BJet1_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet1_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_BJet2_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet2_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  h_BJet3_AbsEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet3_AbsEta", ";|#eta|", nBinsEta/2, 0, maxEta);
  
  // To ease manipulation put in vector                                                                                                   
  vh_BJets_Pt.push_back(h_BJet1_Pt);
  vh_BJets_Pt.push_back(h_BJet2_Pt);
  vh_BJets_Pt.push_back(h_BJet3_Pt);
  //
  vh_BJets_AbsEta.push_back(h_BJet1_AbsEta);
  vh_BJets_AbsEta.push_back(h_BJet2_AbsEta);
  vh_BJets_AbsEta.push_back(h_BJet3_AbsEta);


  // Untagged Jets
  h_untaggedJets_N = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "untaggedJets_N" , ";N (untagged-jets)" , 10, -0.5, +9.5);


  // B-Jet Pair 
  h_BJetPair_dPhiAverage   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiAvg" , ";#Delta#phi (rads)" , 40 , 0.5, 4);
  h_BJetPair_dRAverage     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRAverage" , ";#DeltaR"   , 40 , 0.5   , 4);
  h_BJetPair_dEtaAverage   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dEtaAverage" , ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_BJetPair_Rbb           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_Rbb"         , ";R_{bb}"        , nBinsdR, mindR, maxdR);
  h_BJetPair_MaxPt_Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxPt_Pt"  , ";p_{T} (GeV/c)"       , nBinsPt   , minPt  , maxPt  );
  h_BJetPair_MaxPt_M       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxPt_M"   , ";M (GeV/c^{2})"       , 100       , 0.0 , 1000.0 );
  h_BJetPair_MaxMass_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxMass_Pt"  , ";p_{T} (GeV/c)"     , nBinsPt , minPt  , maxPt  );
  h_BJetPair_MaxMass_M     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxMass_M"   , ";M (GeV/c^{2})"     , 40     ,    0.0 , 1200.0 );
  h_BJetPair_dRMin_Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Pt"       , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dRMin_dR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dR"       , ";#DeltaR"          , nBinsdR  , mindR  , maxdR  );
  h_BJetPair_dRMin_Mass    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Mass"     , ";M (GeV/c^{2})"     , 40   , 0   , 600   );
  h_BJetPair_dRMin_dEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dEta" ,  ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_BJetPair_dRMin_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dPhi" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);
  h_BJetPair_dRMin_Rbb     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Rbb"   , ";R_{bb}"        , nBinsdR, mindR, maxdR);
  h_BJetPair_dPhiMin_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMin_Pt"      , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dPhiMin_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMin_Mass"     , ";M (GeV/c^{2})"     , nBinsM   , minM   , maxM   );
  h_BJetPair_dPhiMax_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMax_Pt"      , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dPhiMax_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMax_Mass"     , ";M (GeV/c^{2})"     , nBinsM   , minM   , maxM   );


  // dR of Ldg Jet and dRMin BJet Pair
  h_ldgJet_dRMinBJetPair_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dR" , ";#DeltaR"          , nBinsdR  ,  mindR  , maxdR  );
  h_ldgJet_dRMinBJetPair_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dEta" ,  ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_ldgJet_dRMinBJetPair_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dPhi" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);
							 
  // dR of untagged Ldg Jet and dRMin BJet Pair                                                           
  h_untaggedLdgJet_dRMinBJetPair_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "untaggedLdgJet_dRMinBJetPair_dR" , ";#DeltaR"  , nBinsdR  ,  mindR  , maxdR  );
  h_untaggedLdgJet_dRMinBJetPair_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "untaggedLdgJet_dRMinBJetPair_dEta" ,  ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_untaggedLdgJet_dRMinBJetPair_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "untaggedLdgJet_dRMinBJetPair_dPhi" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);


  // Di-Jet (no BJets)
  h_dRMinDiJet_noBJets_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "dRMinDiJet_NoBJets_Pt"   , ";p_{T} (GeV/c)" , nBinsPt*2, minPt, maxPt*2);
  h_dRMinDiJet_noBJets_M  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "dRMinDiJet_NoBJets_Mass" , ";M (GeV/c^{2})"  , 50, 0.0, +500.0);

  // Tri-Jet
  h_TriJet_MaxPt_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "MaxTriJetPt_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt , maxPt);
  h_TriJet_MaxPt_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "MaxTriJetPt_Mass" , ";M (GeV/c^{2})", 50,  0.0, +1000.0);

  
  // Minimum and Maximum phi angle between a jet and (MHT-jet)                                                                            
  h_minDeltaPhiJetMHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "minDeltaPhiJetMHT", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_maxDeltaPhiJetMHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "maxDeltaPhiJetMHT", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);

  // Minimum Delta R between a jet and (MHT-jet), -(MHT-jet)                                                                             
  h_minDeltaRJetMHT         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "minDeltaRJetMHT"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_minDeltaRReversedJetMHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "minDeltaRReversedJetMHT"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);


  // Average CSV Discriminator for all jets                                                                                               
  h_AvgCSV               =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV"  , ";Average CSV"  , 100  , 0  , 1);    
  h_AvgCSV_PtWeighted    =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtWeighted"  , ";Average CSV (p_{T} weighted)"  , 100  , 0, 1);    
  h_AvgCSV_PtSqrWeighted =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtSqrWeighted"  , ";Average CSV (p_{T}^{2} weighted)"  , 100  , 0, 1);   

  // Average CSV Discriminator for non-bjets                                                                                              
  h_AvgCSV_noBjets               =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_noBjets"  , ";Average CSV"  , 100  , 0  , 1);
  h_AvgCSV_PtWeighted_noBjets    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtWeighted_noBjets"  , ";Average CSV (p_{T} weighted)" , 100  , 0, 1);
  h_AvgCSV_PtSqrWeighted_noBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtSqrWeighted_noBjets"  , ";Average CSV (p_{T}^{2} weighted)"  , 100  , 0, 1);




  
  // ======== Top Reconstruction (Distances)

  // Ldg Top 
  h_LdgTop_Pt       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "LdgTop_Pt",  ";p_{T} (GeV/c)", nBinsPt, minPt , maxPt);
  h_LdgTop_Eta      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "LdgTop_Eta", ";|#eta|", nBinsEta, minEta, maxEta);
  h_LdgTop_Phi      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "LdgTop_Phi", ";#phi (rads)", nBinsPhi , minPhi , maxPhi );
  h_LdgTop_Mass     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "LdgTop_Mass" , ";M (GeV/c^{2})", 100,  0, 1000.0);

  // SubLdg Top                                                                                                                         
  h_SubLdgTop_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SubLdgTop_Pt",  ";p_{T} (GeV/c)", nBinsPt, minPt , maxPt);
  h_SubLdgTop_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SubLdgTop_Eta", ";|#eta|", nBinsEta, minEta, maxEta);
  h_SubLdgTop_Phi   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SubLdgTop_Phi", ";#phi (rads)", nBinsPhi, minPhi ,maxPhi );
  h_SubLdgTop_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SubLdgTop_Mass" , ";M (GeV/c^{2})", 100,  0, 1000.0);

  // BJets Distances
  h_BJet1BJet2_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet1BJet2_dR", ";#DeltaR", nBinsdR, mindR, 5);
  h_BJet1BJet2_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet1BJet2_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_BJet1BJet2_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet1BJet2_dEta", ";#Delta#eta", nBinsdEta, mindEta, 5);

  // DiJet-BJet Distances
  h_DiJet1BJet1_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet1_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_DiJet1BJet1_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet1_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet1BJet1_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet1_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //
  h_DiJet1BJet2_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet2_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_DiJet1BJet2_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet2_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet1BJet2_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet1BJet2_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //                                                                                                                                                                                                            
  h_DiJet2BJet1_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet1_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_DiJet2BJet1_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet1_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet2BJet1_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet1_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //                                                                                                                                                          
  h_DiJet2BJet2_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet2_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_DiJet2BJet2_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet2_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet2BJet2_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DiJet2BJet2_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  // TriJet-BJet Distances
  h_TriJet1BJet1_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet1_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_TriJet1BJet1_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet1_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_TriJet1BJet1_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet1_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //                                                                                                                 
  h_TriJet1BJet2_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet2_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_TriJet1BJet2_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet2_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_TriJet1BJet2_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet1BJet2_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //                                                                                                                     
  h_TriJet2BJet1_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet1_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_TriJet2BJet1_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet1_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_TriJet2BJet1_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet1_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //                                                                                                                                             
  h_TriJet2BJet2_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet2_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_TriJet2BJet2_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet2_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi, maxdPhi);
  h_TriJet2BJet2_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "TriJet2BJet2_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);



  h_BJet3_LdgTop_dR      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_LdgTop_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_BJet3_LdgTop_dEta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_LdgTop_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_BJet3_LdgTop_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_LdgTop_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi,maxdPhi);
  h_BJet3_SubLdgTop_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_SubLdgTop_dR"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_BJet3_SubLdgTop_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_SubLdgTop_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_BJet3_SubLdgTop_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "BJet3_SubLdgTop_dPhi", ";#Delta#phi", nBinsdPhi, mindPhi,maxdPhi);
  
  // Chi Square
  h_top_ChiSqr         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "ChiSqr"   , ";#chi^{2}"     ,    40,  0.0, 100.0);
  h_top_RedChiSqr      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "RedChiSqr"   , ";#chi^{2}"     ,    100,  0.0, 100.0);

  h_H2_Vs_ChiSqr = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "H2_Vs_ChiSqr" , ";H_{2};#chi^{2}" , 20, 0.0, 1.0,  100,  0.0, 100.0);


  h_DPhi_LdgTrijet_SubldgTrijet  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhi_LdgTrijet_SubldgTrijet"  , ";#Delta#phi", nBinsdPhi, mindPhi,maxdPhi);
  h_Rapidity_LdgTrijet           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "Rapidity_LdgTrijet"  , ";y",45,-2,2);
  h_Rapidity_SubldgTrijet        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "Rapidity_SubldgTrijet"  , ";y",45,-2,2);
  h_Rapidity_Tetrajet            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "Rapidity_Tetrajet"  , ";y",45,-2,2);
  h_SumPt_LdgTrijet_SubldgTrijet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "SumPt_LdgTrijet_SubldgTrijet"  , ";p_{T} (GeV/c)"     , 40   , 0  , 1000  );

  h_CosTheta_Bjet1TopCM_TrijetLab = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet1TopCM_TrijetLab",";cos#theta(Bjet1_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_Bjet2TopCM_TrijetLab = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet2TopCM_TrijetLab",";cos#theta(Bjet2_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_Bjet3TopCM_TrijetLab = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet3TopCM_TrijetLab",";cos#theta(Bjet3_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_Bjet1TopCM_Zaxis     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet1TopCM_Zaxis",";cos#theta(Bjet1_{TopCM},zaxis)",40, -1., 1.);
  h_CosTheta_Bjet2TopCM_Zaxis     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet2TopCM_Zaxis",";cos#theta(Bjet2_{TopCM},zaxis)",40, -1., 1.);
  h_CosTheta_Bjet3TopCM_Zaxis     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_Bjet3TopCM_Zaxis",";cos#theta(Bjet3_{TopCM},zaxis)",40, -1., 1.);

  h_METoverSqrtHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "METoverSqrtH",";E_{T}^{miss}/#sqrt{H_{T}}",40,0,0.3);

  h_CosTheta_LdgTrijetLdgJetTopCM_TrijetLab    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_LdgTrijetLdgJetTopCM_TrijetLab",";cos#theta(LdgTrijetLdgJet_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab",";cos#theta(LdgTrijetSubldgJet_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_LdgTrijetBjetTopCM_TrijetLab      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_LdgTrijetBjetTopCM_TrijetLab",";cos#theta(LdgTrijetBjet_{TopCM},Trijet_{Lab})",40, -1., 1.);

  h_CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab",";cos#theta(SubldgTrijetLdgJet_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab",";cos#theta(SubldgTrijetSubldgJet_{TopCM},Trijet_{Lab})",40, -1., 1.);
  h_CosTheta_SubldgTrijetBjetTopCM_TrijetLab      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "CosTheta_SubldgTrijetBjetTopCM_TrijetLab",";cos#theta(SubldgTrijetBjet_{TopCM},Trijet_{Lab})",40, -1., 1.);

  h_DEta_LdgTrijetDijet_TetrajetB =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DEta_LdgTrijetDijet_TetrajetB",";#Delta#eta",40,0,4);
  h_DPhi_TetrajetB_LdgTrijetB     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhi_TetrajetB_LdgTrijetB",";#Delta#phi",45,0,3.15);
  h_DEta_TetrajetB_LdgTrijetB     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DEta_TetrajetB_LdgTrijetB",";#Delta#eta",40,0,4);

  h_Tetrajet_Mass    =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "Tetrajet_Mass","mass (GeV/c^{2})",40,0,1400);
  
  h_DPhiJ12vsDPhiJ34 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ12vsDPhiJ34" , ";#Delta#phi(j1,j2);#Delta#phi(j3,j4)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DEtaJ12vsDEtaJ34 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DEtaJ12vsDEtaJ34" , ";#Delta#eta(j1,j2);#Delta#eta(j3,j4)" , 40, 0.0, 4,     40,  0.0, 4);
  h_DRJ12vsDRJ34     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DRJ12vsDRJ34"     , ";#Delta R(j1,j2);#Delta R(j3,j4)"     , 40, 0.0, 5,     40  ,0.0, 5);

  h_DPhiJ12vsDPhiJ56 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ12vsDPhiJ56" , ";#Delta#phi(j1,j2);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DEtaJ12vsDEtaJ56 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DEtaJ12vsDEtaJ56" , ";#Delta#eta(j1,j2);#Delta#eta(j5,j6)" , 40, 0.0, 4,     40,  0.0, 4);
  h_DRJ12vsDRJ56     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DRJ12vsDRJ56"     , ";#Delta R(j1,j2);#Delta R(j5,j6)" , 40, 0.0, 5,     40  ,0.0, 5);

  h_DPhiJ34vsDPhiJ56 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DEtaJ34vsDEtaJ56 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DEtaJ34vsDEtaJ56" , ";#Delta#eta(j3,j4);#Delta#eta(j5,j6)" , 40, 0.0, 4,  40,  0.0, 4);
  h_DRJ34vsDRJ56     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DRJ34vsDRJ56"     , ";#Delta R(j3,j4);#Delta R(j5,j6)" , 40, 0.0, 5,     40  ,0.0, 5);

  h_DPhi_LdgTrijetB_SubldgTrijetB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhi_LdgTrijetB_SubldgTrijetB",";#Delta#phi",40,0,3.15);
  h_DPhi_TetrajetB_SubldgTrijetB  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhi_TetrajetB_SubldgTrijetB",";#Delta#phi",40,0,3.15);
  h_DEta_LdgTrijetB_SubldgTrijetB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DEta_LdgTrijetB_SubldgTrijetB",";#Delta#eta", 40,  0.0, 4);
  h_DEta_TetrajetB_SubldgTrijetB  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DEta_TetrajetB_SubldgTrijetB",";#Delta#eta", 40,  0.0, 4);
  h_DR_LdgTrijetB_SubldgTrijetB   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DR_LdgTrijetB_SubldgTrijetB",";#Delta R", 40, 0.0, 5);
  h_DR_TetrajetB_SubldgTrijetB    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DR_TetrajetB_SubldgTrijetB",";#Delta R", 40, 0.0, 5);
  h_DR_TetrajetB_LdgTrijetB       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DR_TetrajetB_LdgTrijetB",";#Delta R",  40, 0.0, 5);
 
  h_PtAsy = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "PtAsy",";P_{TAsy}", 40,-0.8,0.8);
  h_HTminusSumScPt_LdgTop_SubldgTop  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "HTminusSumScPt_LdgTop_SubldgTop",";H_{T}-(LdgTop.P_{T}+SubLdgTop.P_{T})",40,0.0,1300.);
  h_HTminusSumVecPt_LdgTop_SubldgTop = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "HTminusSumVecPt_LdgTop_SubldgTop",";H_{T}-(LdgTop+SubLdgTop).P_{T}",40,0.0,1300.);

  h_DPhiJ34     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhiJ34",";#Delta#phi",40,0,3.15);
  h_DPhiJ56     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhiJ56",";#Delta#phi",40,0,3.15);

  h_DPhiJ34vsDPhiJ56_wCut025 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut025" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiJ34vsDPhiJ56_wCut05 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut05" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiJ34vsDPhiJ56_wCut075 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut075" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiJ34vsDPhiJ56_wCut10 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut10" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiJ34vsDPhiJ56_wCut125 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut125" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiJ34vsDPhiJ56_wCut15 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ34vsDPhiJ56_wCut15" , ";#Delta#phi(j3,j4);#Delta#phi(j5,j6)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  h_DPhiDistance_J34_J56 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhiDistance_J34_J56",";#Delta#phi",40,0,5.0);
  h_DPhiCircle_J34_J56 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "DPhiCircle_J34_J56",";#Delta#phi",40,0,5.0);
  //next histo

  // TTree
  tree = new TTree("tree", "TTree");


  //Additional branches
  weight                    = tree -> Branch("eventWeight", &weight   , "eventWeight/F");
  LdgJet_Pt                 = tree -> Branch("recoJet1_Pt", &LdgJet_Pt, "recoJet1_Pt/F");
  H2                        = tree -> Branch("H2", &H2, "H2/F");
  HT                        = tree -> Branch("HT", &HT, "HT/F");
  TriJet_maxPt_M            = tree -> Branch("MaxTriJetPt_Mass", &TriJet_maxPt_M, "MaxTriJetPt_Mass/F");
  Centrality                = tree -> Branch("Centrality", &Centrality, "Centrality/F");
  Jets_N                    = tree -> Branch("Jets_N", &Jets_N, "Jets_N/I");
  BJets_N                   = tree -> Branch("BJets_N", &BJets_N, "BJets_N/I");
  recoJet2_Pt               = tree -> Branch("recoJet2_Pt", &recoJet2_Pt, "recoJet2_Pt/F");
  recoJet3_Pt               = tree -> Branch("recoJet3_Pt", &recoJet3_Pt, "recoJet3_Pt/F");
  recoJet4_Pt               = tree -> Branch("recoJet4_Pt", &recoJet4_Pt, "recoJet4_Pt/F");
  recoJet5_Pt               = tree -> Branch("recoJet5_Pt", &recoJet5_Pt, "recoJet5_Pt/F");
  recoJet6_Pt               = tree -> Branch("recoJet6_Pt", &recoJet6_Pt, "recoJet6_Pt/F");
  recoJet7_Pt               = tree -> Branch("recoJet7_Pt", &recoJet7_Pt, "recoJet7_Pt/F");

  LdgTop_Pt          = tree -> Branch("LdgTop_Pt", &LdgTop_Pt, "LdgTop_Pt/F");
  LdgTop_Eta         = tree -> Branch("LdgTop_Eta", &LdgTop_Eta, "LdgTop_Eta/F");
  LdgTop_Phi         = tree -> Branch("LdgTop_Phi", &LdgTop_Phi, "LdgTop_Phi/F");
  LdgTop_Mass        = tree -> Branch("LdgTop_Mass", &LdgTop_Mass, "LdgTop_Mass/F");

  SubLdgTop_Pt       = tree -> Branch("SubLdgTop_Pt", &SubLdgTop_Pt, "SubLdgTop_Pt/F");
  SubLdgTop_Eta      = tree -> Branch("SubLdgTop_Eta", &SubLdgTop_Eta, "SubLdgTop_Eta/F");
  SubLdgTop_Phi      = tree -> Branch("SubLdgTop_Phi", &SubLdgTop_Phi, "SubLdgTop_Phi/F");
  SubLdgTop_Mass     = tree -> Branch("SubLdgTop_Mass", &SubLdgTop_Mass, "SubLdgTop_Mass/F");

  Sphericity       = tree -> Branch("Sphericity", &Sphericity, "Sphericity/F");
  Circularity      = tree -> Branch("Circularity", &Circularity, "Circularity/F");
  LdgTetraJet_Mass = tree -> Branch("LdgTetraJet_Mass", &LdgTetraJet_Mass, "LdgTetraJet_Mass/F");
  LdgTetraJet_Pt   = tree -> Branch("LdgTetraJet_Pt", &LdgTetraJet_Pt, "LdgTetraJet_Pt/F");
  LdgBjet_Pt       = tree -> Branch("LdgBjet_Pt", &LdgBjet_Pt, "LdgBjet_Pt/F");
  TopChiSqr        = tree -> Branch("TopChiSqr", &TopChiSqr, "TopChiSqr/F");

  SubldgTetrajet_Pt   = tree -> Branch("SubldgTetrajet_Pt", &SubldgTetrajet_Pt, "SubldgTetrajet_Pt/F");
  SubldgTetrajet_Mass = tree -> Branch("SubldgTetrajet_Mass", &SubldgTetrajet_Mass, "SubldgTetrajet_Mass/F");
  
  DEta_TetrajetB_LdgTrijetB     = tree -> Branch("DEta_TetrajetB_LdgTrijetB",&DEta_TetrajetB_LdgTrijetB, "DEta_TetrajetB_LdgTrijetB/F");
  DEta_Dijet_LdgTrijetB         = tree -> Branch("DEta_Dijet_LdgTrijetB",&DEta_Dijet_LdgTrijetB, "DEta_Dijet_LdgTrijetB/F");
  DEta_LdgTrijetDijet_TetrajetB = tree -> Branch("DEta_LdgTrijetDijet_TetrajetB",&DEta_LdgTrijetDijet_TetrajetB, "DEta_LdgTrijetDijet_TetrajetB/F");
  DEta_LdgTrijet_TetrajetB      = tree -> Branch("DEta_LdgTrijet_TetrajetB",&DEta_LdgTrijet_TetrajetB, "DEta_LdgTrijet_TetrajetB/F");
  DEta_LdgTrijetB_SubldgTrijetB = tree -> Branch("DEta_LdgTrijetB_SubldgTrijetB",&DEta_LdgTrijetB_SubldgTrijetB, "DEta_LdgTrijetB_SubldgTrijetB/F");
  DEta_TetrajetB_SubldgTrijetB  = tree -> Branch("DEta_TetrajetB_SubldgTrijetB",&DEta_TetrajetB_SubldgTrijetB, "DEta_TetrajetB_SubldgTrijetB/F");



  DPhi_TetrajetB_LdgTrijetB     = tree -> Branch("DPhi_TetrajetB_LdgTrijetB",&DPhi_TetrajetB_LdgTrijetB, "DPhi_TetrajetB_LdgTrijetB/F");
  DPhi_Dijet_LdgTrijetB         = tree -> Branch("DPhi_Dijet_LdgTrijetB",&DPhi_Dijet_LdgTrijetB, "DPhi_Dijet_LdgTrijetB/F");
  DPhi_LdgTrijetDijet_TetrajetB = tree -> Branch("DPhi_LdgTrijetDijet_TetrajetB",&DPhi_LdgTrijetDijet_TetrajetB, "DPhi_LdgTrijetDijet_TetrajetB/F");
  DPhi_LdgTrijet_TetrajetB      = tree -> Branch("DPhi_LdgTrijet_TetrajetB",&DPhi_LdgTrijet_TetrajetB, "DPhi_LdgTrijet_TetrajetB/F");
  DPhi_LdgTrijetB_SubldgTrijetB = tree -> Branch("DPhi_LdgTrijetB_SubldgTrijetB",&DPhi_LdgTrijetB_SubldgTrijetB, "DPhi_LdgTrijetB_SubldgTrijetB/F");
  DPhi_TetrajetB_SubldgTrijetB  = tree -> Branch("DPhi_TetrajetB_SubldgTrijetB",&DPhi_TetrajetB_SubldgTrijetB, "DPhi_TetrajetB_SubldgTrijetB/F");

  DR_TetrajetB_LdgTrijetB     = tree -> Branch("DR_TetrajetB_LdgTrijetB",&DR_TetrajetB_LdgTrijetB, "DR_TetrajetB_LdgTrijetB/F");
  DR_Dijet_LdgTrijetB         = tree -> Branch("DR_Dijet_LdgTrijetB",&DR_Dijet_LdgTrijetB, "DR_Dijet_LdgTrijetB/F");
  DR_LdgTrijetDijet_TetrajetB = tree -> Branch("DR_LdgTrijetDijet_TetrajetB",&DR_LdgTrijetDijet_TetrajetB, "DR_LdgTrijetDijet_TetrajetB/F");
  DR_LdgTrijet_TetrajetB      = tree -> Branch("DR_LdgTrijet_TetrajetB",&DR_LdgTrijet_TetrajetB, "DR_LdgTrijet_TetrajetB/F");
  DR_LdgTrijetB_SubldgTrijetB = tree -> Branch("DR_LdgTrijetB_SubldgTrijetB",&DR_LdgTrijetB_SubldgTrijetB, "DR_LdgTrijetB_SubldgTrijetB/F");
  DR_TetrajetB_SubldgTrijetB  = tree -> Branch("DR_TetrajetB_SubldgTrijetB",&DR_TetrajetB_SubldgTrijetB, "DR_TetrajetB_SubldgTrijetB/F");

  D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB=tree -> Branch("D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB", &D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB, "D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB/F");

  AvgCSV_PtWeighted        = tree -> Branch("AvgCSV_PtWeighted" , &AvgCSV_PtWeighted, "AvgCSV_PtWeighted/F"); 
  PtAsy = tree -> Branch("PtAsy", &PtAsy,"PtAsy/F");
  BJetPair_dRMin_M          = tree -> Branch("BJetPair_dRMin_Mass", &BJetPair_dRMin_M, "BJetPair_dRMin_Mass/F");
  BJetPair_dRAvg            = tree -> Branch("BJetPair_dRAverage", &BJetPair_dRAvg, "BJetPair_dRAverage/F");
  BJetPair_maxPt_M          = tree -> Branch("BJetPair_MaxPt_M", &BJetPair_maxPt_M, "BJetPair_MaxPt_M/F");
  BJetPair_maxMass_M        = tree -> Branch("BJetPair_MaxMass_M ", &BJetPair_maxMass_M , "BJetPair_MaxMass_M/F");
  Jet5_BJetsFirst_Pt        = tree -> Branch("recoJet5_BJetsFirst_Pt", &Jet5_BJetsFirst_Pt, "recoJet5_BJetsFirst_Pt/F");
  DPhi_LdgBjet_Trijet       = tree -> Branch("DPhi_LdgBjet_Trijet",&DPhi_LdgBjet_Trijet,"DPhi_LdgBjet_Trijet/F");
  DijetUntaggedSmallDR_Mass = tree -> Branch("DijetUntaggedSmallDR_Mass",&DijetUntaggedSmallDR_Mass,"DijetUntaggedSmallDR_Mass/F"); 

  DPhi_LdgTrijet_SubldgTrijet  = tree -> Branch("DPhi_LdgTrijet_SubldgTrijet",&DPhi_LdgTrijet_SubldgTrijet,"DPhi_LdgTrijet_SubldgTrijet/F");
  Rapidity_LdgTrijet           = tree -> Branch("Rapidity_LdgTrijet",&Rapidity_LdgTrijet,"Rapidity_LdgTrijet/F");
  Rapidity_SubldgTrijet        = tree -> Branch("Rapidity_SubldgTrijet",&Rapidity_SubldgTrijet,"Rapidity_SubldgTrijet/F");
  Rapidity_Tetrajet            = tree -> Branch("Rapidity_Tetrajet",&Rapidity_Tetrajet,"Rapidity_Tetrajet/F");
  SumPt_LdgTrijet_SubldgTrijet = tree -> Branch("SumPt_LdgTrijet_SubldgTrijet",&SumPt_LdgTrijet_SubldgTrijet,"SumPt_LdgTrijet_SubldgTrijet/F");

  CosTheta_Bjet1TopCM_TrijetLab = tree -> Branch("CosTheta_Bjet1TopCM_TrijetLab",&CosTheta_Bjet1TopCM_TrijetLab,"CosTheta_Bjet1TopCM_TrijetLab/F");
  CosTheta_Bjet1TopCM_Zaxis     = tree -> Branch("CosTheta_Bjet1TopCM_Zaxis",&CosTheta_Bjet1TopCM_Zaxis,"CosTheta_Bjet1TopCM_Zaxis/F");
  CosTheta_Bjet2TopCM_TrijetLab = tree -> Branch("CosTheta_Bjet2TopCM_TrijetLab",&CosTheta_Bjet2TopCM_TrijetLab,"CosTheta_Bjet2TopCM_TrijetLab/F");
  CosTheta_Bjet2TopCM_Zaxis     = tree -> Branch("CosTheta_Bjet2TopCM_Zaxis",&CosTheta_Bjet2TopCM_Zaxis,"CosTheta_Bjet2TopCM_Zaxis/F");
  CosTheta_Bjet3TopCM_TrijetLab = tree -> Branch("CosTheta_Bjet3TopCM_TrijetLab",&CosTheta_Bjet3TopCM_TrijetLab,"CosTheta_Bjet3TopCM_TrijetLab/F");
  CosTheta_Bjet3TopCM_Zaxis     = tree -> Branch("CosTheta_Bjet3TopCM_Zaxis",&CosTheta_Bjet3TopCM_Zaxis,"CosTheta_Bjet3TopCM_Zaxis/F");

  METoverSqrtHT = tree -> Branch("METoverSqrtHT",&METoverSqrtHT,"METoverSqrtHT/F");

  CosTheta_LdgTrijetLdgJetTopCM_TrijetLab    = tree -> Branch("CosTheta_LdgTrijetLdgJetTopCM_TrijetLab",&CosTheta_LdgTrijetLdgJetTopCM_TrijetLab,"CosTheta_LdgTrijetLdgJetTopCM_TrijetLab/F");
  CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab = tree -> Branch("CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab",&CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab,"CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab/F");
  CosTheta_LdgTrijetBjetTopCM_TrijetLab      = tree -> Branch("CosTheta_LdgTrijetBjetTopCM_TrijetLab",&CosTheta_LdgTrijetBjetTopCM_TrijetLab,"CosTheta_LdgTrijetBjetTopCM_TrijetLab/F");

  CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab    = tree -> Branch("CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab",&CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab,"CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab/F");
  CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab = tree -> Branch("CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab",&CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab,"CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab/F");
  CosTheta_SubldgTrijetBjetTopCM_TrijetLab      = tree -> Branch("CosTheta_SubldgTrijetBjetTopCM_TrijetLab",&CosTheta_SubldgTrijetBjetTopCM_TrijetLab,"CosTheta_SubldgTrijetBjetTopCM_TrijetLab/F");

  HTminusSumScPt_LdgTop_SubldgTop  = tree -> Branch("HTminusSumScPt_LdgTop_SubldgTop",&HTminusSumScPt_LdgTop_SubldgTop, "HTminusSumScPt_LdgTop_SubldgTop/F");
  HTminusSumVecPt_LdgTop_SubldgTop = tree -> Branch("HTminusSumVecPt_LdgTop_SubldgTop",&HTminusSumVecPt_LdgTop_SubldgTop, "HTminusSumVecPt_LdgTop_SubldgTop/F");

  DPhiJ34 = tree -> Branch ("DPhiJ34",&DPhiJ34,"DPhiJ34/F");
  DPhiJ56 = tree -> Branch ("DPhiJ56",&DPhiJ56,"DPhiJ56/F");

  DPhiDistance_J34_J56 = tree ->Branch("DPhiDistance_J34_J56",&DPhiDistance_J34_J56,"DPhiDistance_J34_J56/F");
  DPhiCircle_J34_J56   = tree ->Branch("DPhiCircle_J34_J56",&DPhiCircle_J34_J56,"DPhiCircle_J34_J56/F");


  LdgTrijetPtDR              = tree -> Branch ("LdgTrijetPtDR",              &LdgTrijetPtDR,             "LdgTrijetPtDR/F"              );
  LdgTrijetDijetPtDR         = tree -> Branch ("LdgTrijetDijetPtDR",         &LdgTrijetDijetPtDR,        "LdgTrijetDijetPtDR/F"         );
  LdgTrijetBjetMass          = tree -> Branch ("LdgTrijetBjetMass",          &LdgTrijetBjetMass,         "LdgTrijetBjetMass/F"          );
  LdgTrijetLdgJetPt          = tree -> Branch ("LdgTrijetLdgJetPt",          &LdgTrijetLdgJetPt,         "LdgTrijetLdgJetPt/F"          );
  LdgTrijetLdgJetEta         = tree -> Branch ("LdgTrijetLdgJetEta",         &LdgTrijetLdgJetEta,        "LdgTrijetLdgJetEta/F"         );
  LdgTrijetLdgJetBDisc       = tree -> Branch ("LdgTrijetLdgJetBDisc",       &LdgTrijetLdgJetBDisc,      "LdgTrijetLdgJetBDisc/F"       );
  LdgTrijetSubldgJetPt       = tree -> Branch ("LdgTrijetSubldgJetPt",       &LdgTrijetSubldgJetPt,      "LdgTrijetSubldgJetPt/F"       );
  LdgTrijetSubldgJetEta      = tree -> Branch ("LdgTrijetSubldgJetEta",      &LdgTrijetSubldgJetEta,     "LdgTrijetSubldgJetEta/F"      );
  LdgTrijetSubldgJetBDisc    = tree -> Branch ("LdgTrijetSubldgJetBDisc",    &LdgTrijetSubldgJetBDisc,   "LdgTrijetSubldgJetBDisc/F"    );
  LdgTrijetBJetLdgJetMass    = tree -> Branch ("LdgTrijetBJetLdgJetMass",    &LdgTrijetBJetLdgJetMass,   "LdgTrijetBJetLdgJetMass/F"    );
  LdgTrijetBJetSubldgJetMass = tree -> Branch ("LdgTrijetBJetSubldgJetMass", &LdgTrijetBJetSubldgJetMass,"LdgTrijetBJetSubldgJetMass/F" );


  SubldgTrijetPtDR              = tree -> Branch ("SubldgTrijetPtDR",              &SubldgTrijetPtDR,             "SubldgTrijetPtDR/F"              );
  SubldgTrijetDijetPtDR         = tree -> Branch ("SubldgTrijetDijetPtDR",         &SubldgTrijetDijetPtDR,        "SubldgTrijetDijetPtDR/F"         );
  SubldgTrijetBjetMass          = tree -> Branch ("SubldgTrijetBjetMass",          &SubldgTrijetBjetMass,         "SubldgTrijetBjetMass/F"          );
  SubldgTrijetLdgJetPt          = tree -> Branch ("SubldgTrijetLdgJetPt",          &SubldgTrijetLdgJetPt,         "SubldgTrijetLdgJetPt/F"          );
  SubldgTrijetLdgJetEta         = tree -> Branch ("SubldgTrijetLdgJetEta",         &SubldgTrijetLdgJetEta,        "SubldgTrijetLdgJetEta/F"         );
  SubldgTrijetLdgJetBDisc       = tree -> Branch ("SubldgTrijetLdgJetBDisc",       &SubldgTrijetLdgJetBDisc,      "SubldgTrijetLdgJetBDisc/F"       );
  SubldgTrijetSubldgJetPt       = tree -> Branch ("SubldgTrijetSubldgJetPt",       &SubldgTrijetSubldgJetPt,      "SubldgTrijetSubldgJetPt/F"       );
  SubldgTrijetSubldgJetEta      = tree -> Branch ("SubldgTrijetSubldgJetEta",      &SubldgTrijetSubldgJetEta,     "SubldgTrijetSubldgJetEta/F"      );
  SubldgTrijetSubldgJetBDisc    = tree -> Branch ("SubldgTrijetSubldgJetBDisc",    &SubldgTrijetSubldgJetBDisc,   "SubldgTrijetSubldgJetBDisc/F"    );
  SubldgTrijetBJetLdgJetMass    = tree -> Branch ("SubldgTrijetBJetLdgJetMass",    &SubldgTrijetBJetLdgJetMass,   "SubldgTrijetBJetLdgJetMass/F"    );
  SubldgTrijetBJetSubldgJetMass = tree -> Branch ("SubldgTrijetBJetSubldgJetMass", &SubldgTrijetBJetSubldgJetMass,"SubldgTrijetBJetSubldgJetMass/F" );

  LdgTrijetDijetMass              = tree -> Branch ("LdgTrijetDijetMass", &LdgTrijetDijetMass, "LdgTrijetDijetMass/F");
  SubldgTrijetDijetMass           = tree -> Branch ("SubldgTrijetDijetMass", &SubldgTrijetDijetMass, "SubldgTrijetDijetMass/F");

  LdgTrijetBJetBDisc    = tree -> Branch ("LdgTrijetBJetBDisc",&LdgTrijetBJetBDisc,"LdgTrijetBJetBDisc/F");
  SubldgTrijetBJetBDisc = tree -> Branch ("SubldgTrijetBJetBDisc",&SubldgTrijetBJetBDisc,"SubldgTrijetBJetBDisc/F");



  //next branch

  return;
}


void HplusHadronic::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void HplusHadronic::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

  
  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if(0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;
  
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);
  

  //================================================================================================   
  // 2) MET filters (to remove events with spurious sources of fake MET)
  //================================================================================================   
  if(0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  
  
  
  //================================================================================================   
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================   
  if(0) std::cout << "=== Vertices" << std::endl;
  if (nVertices < 1) return;

  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  
  //================================================================================================   
  // 4) Trigger SF
  //================================================================================================   
  // if(0) std::cout << "=== MET Trigger SF" << std::endl;
  // const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  // if (fEvent.isMC()) {
  //   fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  // }
  // cMetTriggerSFCounter.increment();
  // fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  

  //================================================================================================   
  // 5) Electron veto (Orthogonality)
  //================================================================================================   
  if(0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;


  //================================================================================================
  // 6) Muon veto (Orthogonality)
  //================================================================================================
  if(0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;


  //================================================================================================   
  // 7) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if(0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  // Fake-Tau SF
  if (fEvent.isMC()) 
    {      
      // Not needed unless a tau is used!
      // fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
      // cFakeTauSFCounter.increment();
    }
  

  // Tau-Trigger SF
  if (fEvent.isMC())
    {
      // Not needed unless a tau is used!
      // fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
      // cTauTriggerSFCounter.increment();
    }

  
  //================================================================================================
  // 8) Jet selection
  //================================================================================================
  if(0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;

  
  //================================================================================================
  // Standard Selections
  //================================================================================================
  if(0) std::cout << "=== Standard selection" << std::endl;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  

  //================================================================================================  
  // 9) BJet selection
  //================================================================================================
  if(0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
  
  
  //================================================================================================  
  // 10) BJet SF  
  //================================================================================================
  if(0) std::cout << "=== BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
   }
  cBTaggingSFCounter.increment();


  //================================================================================================
  // 11) MET selection
  //================================================================================================
  if(0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;
  

  //================================================================================================
  // 12) Topology selection
  //================================================================================================
  if(0) std::cout << "=== Topology selection" << std::endl;
  const TopologySelection::Data TopologyData = fTopologySelection.analyze(fEvent, jetData);
  if (!TopologyData.passedSelection()) return;

  //================================================================================================
  // 13) Top selection
  //================================================================================================
  if(0) std::cout << "=== Top selection" << std::endl;
  const TopSelection::Data TopData = fTopSelection.analyze(fEvent, jetData, bjetData);
  if (!TopData.passedSelection()) return;

  //================================================================================================
  // All cuts passed
  //================================================================================================
  if(0) std::cout << "=== All cuts passed" << std::endl;
  cSelected.increment();

  

  //================================================================================================                      
  // CUTS OPTIMISATION                                                                                             
  //================================================================================================ 

  // Define the addresses of the variables which will be added to the TTree
  float eventWeight;
  float ldgJet_Pt, bJetPair_dRMin_M, jet5_bJetsFirst_Pt, h2, bJetPair_dRAvg;
  float  ht, bJetPair_maxPt_M, bJetPair_maxMass_M, triJet_maxPt_M, centrality ;
  float recoJet2_pt,recoJet3_pt,recoJet4_pt,recoJet5_pt,recoJet6_pt, recoJet7_pt;
  int jets_N, bjets_N;
  float avgCSV_PtWeighted;
  float ldgTop_Pt, ldgTop_Eta, ldgTop_Phi, ldgTop_Mass, subldgTop_Pt, subldgTop_Eta, subldgTop_Phi, subldgTop_Mass;
  
  //Additional brancher
  float sphericity, circularity, ldgTetraJet_Mass,ldgTetraJet_Pt, ldgBjet_Pt, topChiSqr, subldgTetrajet_Pt, subldgTetrajet_Mass;
  float dEta_TetrajetB_LdgTrijetB, dEta_Dijet_LdgTrijetB, dEta_LdgTrijetDijet_TetrajetB, dEta_LdgTrijet_TetrajetB;
  float dPhi_TetrajetB_LdgTrijetB, dPhi_Dijet_LdgTrijetB, dPhi_LdgTrijetDijet_TetrajetB, dPhi_LdgTrijet_TetrajetB;
  float dR_TetrajetB_LdgTrijetB, dR_Dijet_LdgTrijetB, dR_LdgTrijetDijet_TetrajetB, dR_LdgTrijet_TetrajetB;
  float d_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB;
  float ptAsy, dPhi_LdgBjet_Trijet, dijetUntaggedSmallDR_Mass;

  float dPhi_LdgTrijet_SubldgTrijet,rapidity_LdgTrijet,rapidity_SubldgTrijet,rapidity_Tetrajet,sumPt_LdgTrijet_SubldgTrijet;
  float cosTheta_Bjet1TopCM_TrijetLab=100, cosTheta_Bjet1TopCM_Zaxis=100,cosTheta_Bjet2TopCM_TrijetLab=100, cosTheta_Bjet2TopCM_Zaxis=100,cosTheta_Bjet3TopCM_TrijetLab=100, cosTheta_Bjet3TopCM_Zaxis=100;
  float cosTheta_LdgTrijetLdgJetTopCM_TrijetLab=100, cosTheta_LdgTrijetSubldgJetTopCM_TrijetLab=100, cosTheta_LdgTrijetBjetTopCM_TrijetLab=100;
  float cosTheta_SubldgTrijetLdgJetTopCM_TrijetLab=100, cosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab=100, cosTheta_SubldgTrijetBjetTopCM_TrijetLab=100;
  float dPhi_LdgTrijetB_SubldgTrijetB, dPhi_TetrajetB_SubldgTrijetB,dEta_LdgTrijetB_SubldgTrijetB, dEta_TetrajetB_SubldgTrijetB, dR_LdgTrijetB_SubldgTrijetB, dR_TetrajetB_SubldgTrijetB;
  float metOverSqrtHT;
  float hTminusSumScPt_LdgTop_SubldgTop, hTminusSumVecPt_LdgTop_SubldgTop;

  float dPhiJ34, dPhiJ56, dPhiDistance, dPhiCircle;

  float ldgTrijetPtDR,ldgTrijetDijetPtDR,ldgTrijetBjetMass,ldgTrijetLdgJetPt,ldgTrijetLdgJetEta, ldgTrijetLdgJetBDisc,ldgTrijetSubldgJetPt, ldgTrijetSubldgJetEta, ldgTrijetSubldgJetBDisc, ldgTrijetBJetLdgJetMass, ldgTrijetBJetSubldgJetMass;

  float subldgTrijetPtDR, subldgTrijetDijetPtDR, subldgTrijetBjetMass, subldgTrijetLdgJetPt, subldgTrijetLdgJetEta, subldgTrijetLdgJetBDisc, subldgTrijetSubldgJetPt, subldgTrijetSubldgJetEta, subldgTrijetSubldgJetBDisc, subldgTrijetBJetLdgJetMass, subldgTrijetBJetSubldgJetMass;

  float ldgTrijetDijetMass, subldgTrijetDijetMass, ldgTrijetBJetBDisc, subldgTrijetBJetBDisc;
  
  //next variable 

  // ATLAS BDT
  weight                    -> SetAddress(&eventWeight);
  LdgJet_Pt                 -> SetAddress(&ldgJet_Pt);
  H2                        -> SetAddress(&h2);
  HT                        -> SetAddress(&ht);
  TriJet_maxPt_M            -> SetAddress(&triJet_maxPt_M);
  Centrality                -> SetAddress(&centrality);
  Jets_N                    -> SetAddress(&jets_N);
  BJets_N                   -> SetAddress(&bjets_N);
  recoJet2_Pt               -> SetAddress(&recoJet2_pt);
  recoJet3_Pt               -> SetAddress(&recoJet3_pt);
  recoJet4_Pt               -> SetAddress(&recoJet4_pt);
  recoJet5_Pt               -> SetAddress(&recoJet5_pt);
  recoJet6_Pt               -> SetAddress(&recoJet6_pt);
  recoJet7_Pt               -> SetAddress(&recoJet7_pt);
  
  // Top Reconstruction
  LdgTop_Pt          -> SetAddress(&ldgTop_Pt);
  LdgTop_Eta         -> SetAddress(&ldgTop_Eta);
  LdgTop_Phi         -> SetAddress(&ldgTop_Phi);
  LdgTop_Mass        -> SetAddress(&ldgTop_Mass);

  SubLdgTop_Pt       -> SetAddress(&subldgTop_Pt);
  SubLdgTop_Eta      -> SetAddress(&subldgTop_Eta);
  SubLdgTop_Phi      -> SetAddress(&subldgTop_Phi);
  SubLdgTop_Mass     -> SetAddress(&subldgTop_Mass);
  //Additional branches 
  Sphericity          -> SetAddress(&sphericity);
  Circularity         -> SetAddress(&circularity);
  LdgTetraJet_Mass    -> SetAddress(&ldgTetraJet_Mass);
  LdgTetraJet_Pt      -> SetAddress(&ldgTetraJet_Pt);
  LdgBjet_Pt          -> SetAddress(&ldgBjet_Pt);
  TopChiSqr           -> SetAddress(&topChiSqr);

  SubldgTetrajet_Pt   -> SetAddress(&subldgTetrajet_Pt);
  SubldgTetrajet_Mass -> SetAddress(&subldgTetrajet_Mass);

  DEta_TetrajetB_LdgTrijetB      -> SetAddress(&dEta_TetrajetB_LdgTrijetB);
  DEta_Dijet_LdgTrijetB          -> SetAddress(&dEta_Dijet_LdgTrijetB);
  DEta_LdgTrijetDijet_TetrajetB  -> SetAddress(&dEta_LdgTrijetDijet_TetrajetB);
  DEta_LdgTrijet_TetrajetB       -> SetAddress(&dEta_LdgTrijet_TetrajetB);
  DEta_LdgTrijetB_SubldgTrijetB  -> SetAddress(&dEta_LdgTrijetB_SubldgTrijetB);
  DEta_TetrajetB_SubldgTrijetB   -> SetAddress(&dEta_TetrajetB_SubldgTrijetB);

  DPhi_TetrajetB_LdgTrijetB      -> SetAddress(&dPhi_TetrajetB_LdgTrijetB);
  DPhi_Dijet_LdgTrijetB          -> SetAddress(&dPhi_Dijet_LdgTrijetB);
  DPhi_LdgTrijetDijet_TetrajetB  -> SetAddress(&dPhi_LdgTrijetDijet_TetrajetB);
  DPhi_LdgTrijet_TetrajetB       -> SetAddress(&dPhi_LdgTrijet_TetrajetB);
  DPhi_LdgTrijetB_SubldgTrijetB  -> SetAddress(&dPhi_LdgTrijetB_SubldgTrijetB);
  DPhi_TetrajetB_SubldgTrijetB   -> SetAddress(&dPhi_TetrajetB_SubldgTrijetB);

  DR_TetrajetB_LdgTrijetB        -> SetAddress(&dR_TetrajetB_LdgTrijetB);
  DR_Dijet_LdgTrijetB            -> SetAddress(&dR_Dijet_LdgTrijetB);
  DR_LdgTrijetDijet_TetrajetB    -> SetAddress(&dR_LdgTrijetDijet_TetrajetB);
  DR_LdgTrijet_TetrajetB         -> SetAddress(&dR_LdgTrijet_TetrajetB);
  DR_LdgTrijetB_SubldgTrijetB    -> SetAddress(&dR_LdgTrijetB_SubldgTrijetB);
  DR_TetrajetB_SubldgTrijetB     -> SetAddress(&dR_TetrajetB_SubldgTrijetB);

  D_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB -> SetAddress(&d_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB);

  BJetPair_dRMin_M          -> SetAddress(&bJetPair_dRMin_M);
  BJetPair_dRAvg            -> SetAddress(&bJetPair_dRAvg);
  BJetPair_maxPt_M          -> SetAddress(&bJetPair_maxPt_M);
  BJetPair_maxMass_M        -> SetAddress(&bJetPair_maxMass_M);
  AvgCSV_PtWeighted         -> SetAddress(&avgCSV_PtWeighted);
  Jet5_BJetsFirst_Pt        -> SetAddress(&jet5_bJetsFirst_Pt);
  PtAsy                     -> SetAddress(&ptAsy);
  DPhi_LdgBjet_Trijet       -> SetAddress(&dPhi_LdgBjet_Trijet);
  DijetUntaggedSmallDR_Mass -> SetAddress(&dijetUntaggedSmallDR_Mass);

  // TTree Variables (Event-Weight)
  eventWeight = fEventWeight.getWeight();


  DPhi_LdgTrijet_SubldgTrijet    -> SetAddress(&dPhi_LdgTrijet_SubldgTrijet);
  Rapidity_LdgTrijet             -> SetAddress(&rapidity_LdgTrijet);
  Rapidity_SubldgTrijet          -> SetAddress(&rapidity_SubldgTrijet);
  Rapidity_Tetrajet              -> SetAddress(&rapidity_Tetrajet);
  SumPt_LdgTrijet_SubldgTrijet   -> SetAddress(&sumPt_LdgTrijet_SubldgTrijet);

  CosTheta_Bjet1TopCM_TrijetLab  -> SetAddress(&cosTheta_Bjet1TopCM_TrijetLab);
  CosTheta_Bjet1TopCM_Zaxis      -> SetAddress(&cosTheta_Bjet1TopCM_Zaxis);
  CosTheta_Bjet2TopCM_TrijetLab  -> SetAddress(&cosTheta_Bjet2TopCM_TrijetLab);
  CosTheta_Bjet2TopCM_Zaxis      -> SetAddress(&cosTheta_Bjet2TopCM_Zaxis);
  CosTheta_Bjet3TopCM_TrijetLab  -> SetAddress(&cosTheta_Bjet3TopCM_TrijetLab);
  CosTheta_Bjet3TopCM_Zaxis      -> SetAddress(&cosTheta_Bjet3TopCM_Zaxis);

  CosTheta_LdgTrijetLdgJetTopCM_TrijetLab       ->SetAddress(&cosTheta_LdgTrijetLdgJetTopCM_TrijetLab);
  CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab    ->SetAddress(&cosTheta_LdgTrijetSubldgJetTopCM_TrijetLab);
  CosTheta_LdgTrijetBjetTopCM_TrijetLab         ->SetAddress(&cosTheta_LdgTrijetBjetTopCM_TrijetLab);
  CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab    ->SetAddress(&cosTheta_SubldgTrijetLdgJetTopCM_TrijetLab);
  CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab ->SetAddress(&cosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab);
  CosTheta_SubldgTrijetBjetTopCM_TrijetLab      ->SetAddress(&cosTheta_SubldgTrijetBjetTopCM_TrijetLab);


  METoverSqrtHT                    -> SetAddress(&metOverSqrtHT);
  HTminusSumScPt_LdgTop_SubldgTop  -> SetAddress(&hTminusSumScPt_LdgTop_SubldgTop);
  HTminusSumVecPt_LdgTop_SubldgTop -> SetAddress(&hTminusSumVecPt_LdgTop_SubldgTop);

  DPhi_LdgTrijet_SubldgTrijet   -> SetAddress(&dPhi_LdgTrijet_SubldgTrijet);
  Rapidity_LdgTrijet            -> SetAddress(&rapidity_LdgTrijet);
  Rapidity_SubldgTrijet         -> SetAddress(&rapidity_SubldgTrijet);
  Rapidity_Tetrajet             -> SetAddress(&rapidity_Tetrajet);
  SumPt_LdgTrijet_SubldgTrijet  -> SetAddress(&sumPt_LdgTrijet_SubldgTrijet);

  DPhiJ34  -> SetAddress(&dPhiJ34);
  DPhiJ56  -> SetAddress(&dPhiJ56);
  DPhiDistance_J34_J56 -> SetAddress(&dPhiDistance);
  DPhiCircle_J34_J56   -> SetAddress(&dPhiCircle);


  LdgTrijetPtDR              -> SetAddress(&ldgTrijetPtDR);
  LdgTrijetDijetPtDR         -> SetAddress(&ldgTrijetDijetPtDR);
  LdgTrijetBjetMass          -> SetAddress(&ldgTrijetBjetMass);
  LdgTrijetLdgJetPt          -> SetAddress(&ldgTrijetLdgJetPt);
  LdgTrijetLdgJetEta         -> SetAddress(&ldgTrijetLdgJetEta);
  LdgTrijetLdgJetBDisc       -> SetAddress(&ldgTrijetLdgJetBDisc);
  LdgTrijetSubldgJetPt       -> SetAddress(&ldgTrijetSubldgJetPt);
  LdgTrijetSubldgJetEta      -> SetAddress(&ldgTrijetSubldgJetEta);
  LdgTrijetSubldgJetBDisc    -> SetAddress(&ldgTrijetSubldgJetBDisc);
  LdgTrijetBJetLdgJetMass    -> SetAddress(&ldgTrijetBJetLdgJetMass);
  LdgTrijetBJetSubldgJetMass -> SetAddress(&ldgTrijetBJetSubldgJetMass);

  SubldgTrijetPtDR              -> SetAddress(&subldgTrijetPtDR);
  SubldgTrijetDijetPtDR         -> SetAddress(&subldgTrijetDijetPtDR);
  SubldgTrijetBjetMass          -> SetAddress(&subldgTrijetBjetMass);
  SubldgTrijetLdgJetPt          -> SetAddress(&subldgTrijetLdgJetPt);
  SubldgTrijetLdgJetEta         -> SetAddress(&subldgTrijetLdgJetEta);
  SubldgTrijetLdgJetBDisc       -> SetAddress(&subldgTrijetLdgJetBDisc);
  SubldgTrijetSubldgJetPt       -> SetAddress(&subldgTrijetSubldgJetPt);
  SubldgTrijetSubldgJetEta      -> SetAddress(&subldgTrijetSubldgJetEta);
  SubldgTrijetSubldgJetBDisc    -> SetAddress(&subldgTrijetSubldgJetBDisc);
  SubldgTrijetBJetLdgJetMass    -> SetAddress(&subldgTrijetBJetLdgJetMass);
  SubldgTrijetBJetSubldgJetMass -> SetAddress(&subldgTrijetBJetSubldgJetMass);

  LdgTrijetDijetMass    ->SetAddress(&ldgTrijetDijetMass);
  SubldgTrijetDijetMass ->SetAddress(&subldgTrijetDijetMass);
  LdgTrijetBJetBDisc    ->SetAddress(&ldgTrijetBJetBDisc);
  SubldgTrijetBJetBDisc ->SetAddress(&subldgTrijetBJetBDisc);
  

  //next address
  //======================================================= 
  // Event-Shape Variables
  //======================================================= 

  h_HT         -> Fill ( TopologyData.HT()               );
  h_MHT        -> Fill ( TopologyData.MHT()              );
  h_Sphericity -> Fill ( TopologyData.Sphericity()       );
  h_Aplanarity -> Fill ( TopologyData.Aplanarity()       );
  h_Planarity  -> Fill ( TopologyData.Planarity()        );
  h_DParameter -> Fill ( TopologyData.Dparameter()       );
  h_H2         -> Fill ( TopologyData.FoxWolframMoment() );
  h_Circularity-> Fill ( TopologyData.Circularity()      );
  h_Centrality -> Fill ( TopologyData.Centrality()       );
  h_AlphaT     -> Fill ( TopologyData.AlphaT()           );
  

  h_METoverSqrtHT -> Fill ( METData.getMET().R() / (TopologyData.HT()));
  h_R32_LdgTop    -> Fill ( TopData.getLdgTrijet().M() / TopData.getLdgDijet().M());
  h_R32_SubLdgTop -> Fill ( TopData.getSubldgTrijet().M() / TopData.getSubldgDijet().M());

  // TTree Variables
  //additional branches
  ht = TopologyData.HT();
  h2 = TopologyData.FoxWolframMoment();  
  centrality = TopologyData.Centrality();
  sphericity          = TopologyData.Sphericity();
  circularity         = TopologyData.Circularity();
  topChiSqr           = TopData.ChiSqr();
  ldgTetraJet_Pt      = TopData.getLdgTetrajet().Pt();
  ldgTetraJet_Mass    = TopData.getLdgTetrajet().M();
  
  subldgTetrajet_Pt   = TopData.getSubldgTetrajet().Pt();
  subldgTetrajet_Mass = TopData.getSubldgTetrajet().M();

  math::XYZTLorentzVector ldgBjet_p4(0,0,0,0), tetrajetB_p4(0,0,0,0), ldgTrijetB_p4(0,0,0,0), subldgTrijetB_p4(0,0,0,0);

  ldgBjet_p4       = bjetData.getSelectedBJets().at(0).p4();
  ldgBjet_Pt       = ldgBjet_p4.pt();
  ldgTrijetB_p4    = TopData.getLdgTrijetBJet().p4();  //Not working
  tetrajetB_p4     = TopData.getTetrajetBJet().p4();
  subldgTrijetB_p4 = TopData.getSubldgTrijetBJet().p4();

 
  dEta_TetrajetB_LdgTrijetB     = std::abs(tetrajetB_p4.eta() - ldgTrijetB_p4.eta());
  dEta_Dijet_LdgTrijetB         = std::abs(TopData.getLdgDijet().Eta() - ldgTrijetB_p4.eta());
  dEta_LdgTrijetDijet_TetrajetB = std::abs(TopData.getLdgDijet().Eta() - tetrajetB_p4.eta());
  dEta_LdgTrijet_TetrajetB      = std::abs(TopData.getLdgTrijet().Eta() - tetrajetB_p4.eta());
  dEta_LdgTrijetB_SubldgTrijetB = std::abs(ldgTrijetB_p4.eta() - subldgTrijetB_p4.eta()); //fix
  dEta_TetrajetB_SubldgTrijetB  = std::abs(tetrajetB_p4.eta() - subldgTrijetB_p4.eta()); 

  dR_TetrajetB_LdgTrijetB       = ROOT::Math::VectorUtil::DeltaR(tetrajetB_p4,ldgTrijetB_p4);
  dR_Dijet_LdgTrijetB           = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgDijet(),ldgTrijetB_p4);
  dR_LdgTrijetDijet_TetrajetB   = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgDijet(),tetrajetB_p4);
  dR_LdgTrijet_TetrajetB        = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgTrijet(),tetrajetB_p4);
  dR_LdgTrijetB_SubldgTrijetB   = ROOT::Math::VectorUtil::DeltaR(ldgTrijetB_p4,subldgTrijetB_p4);
  dR_TetrajetB_SubldgTrijetB    = ROOT::Math::VectorUtil::DeltaR(tetrajetB_p4, subldgTrijetB_p4);

  dPhi_TetrajetB_LdgTrijetB     = std::abs(ROOT::Math::VectorUtil::DeltaPhi(tetrajetB_p4,ldgTrijetB_p4));
  dPhi_Dijet_LdgTrijetB         = std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgDijet(),ldgTrijetB_p4));
  dPhi_LdgTrijetDijet_TetrajetB = std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgDijet(),tetrajetB_p4));
  dPhi_LdgTrijet_TetrajetB      = std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(),tetrajetB_p4));
  dPhi_LdgTrijetB_SubldgTrijetB = std::abs(ROOT::Math::VectorUtil::DeltaPhi(ldgTrijetB_p4,subldgTrijetB_p4));
  dPhi_TetrajetB_SubldgTrijetB  = std::abs(ROOT::Math::VectorUtil::DeltaPhi(tetrajetB_p4, subldgTrijetB_p4));
  
   float jdr1 = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgDijet(),tetrajetB_p4);
   float jdr2 = ROOT::Math::VectorUtil::DeltaR(TopData.getSubldgDijet(),tetrajetB_p4);
   d_Dr_LdgTrDijet_TetrajB__Dr_SldgTrDijet_TetrajB = std::abs(jdr1 - jdr2);
  /////

  ldgTop_Pt      = TopData.getLdgTrijet().Pt();
  ldgTop_Mass    = TopData.getLdgTrijet().M();
  subldgTop_Pt   = TopData.getSubldgTrijet().Pt();
  subldgTop_Mass = TopData.getSubldgTrijet().M();

  h_H2_Vs_ChiSqr -> Fill ( TopologyData.FoxWolframMoment(), TopData.ChiSqr() );


  dPhi_LdgBjet_Trijet =  std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(),ldgBjet_p4));
  ptAsy = (ldgBjet_Pt - ldgTop_Pt)/(ldgBjet_Pt + ldgTop_Pt);



  dPhi_LdgTrijet_SubldgTrijet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(),TopData.getSubldgTrijet()));

  rapidity_LdgTrijet    = 0.5*log((TopData.getLdgTrijet().E()+TopData.getLdgTrijet().Pz())       / (TopData.getLdgTrijet().E()-TopData.getLdgTrijet().Pz()));
  rapidity_SubldgTrijet = 0.5*log((TopData.getSubldgTrijet().E()+TopData.getSubldgTrijet().Pz()) / (TopData.getSubldgTrijet().E()-TopData.getSubldgTrijet().Pz()));
  rapidity_Tetrajet     = 0.5*log((TopData.getLdgTetrajet().E()+TopData.getLdgTetrajet().Pz())   / (TopData.getLdgTetrajet().E()-TopData.getLdgTetrajet().Pz()));

  math::XYZTLorentzVector sum_LdgTrijet_SubldgTrijet_P4;
  sum_LdgTrijet_SubldgTrijet_P4 = TopData.getLdgTrijet()+TopData.getSubldgTrijet();
  sumPt_LdgTrijet_SubldgTrijet  = sum_LdgTrijet_SubldgTrijet_P4.Pt();

  //FIXME!
  TLorentzVector TrijetLorentz;
  TrijetLorentz.SetPtEtaPhiE(TopData.getLdgTrijet().Pt(),TopData.getLdgTrijet().Eta(),TopData.getLdgTrijet().Phi(),TopData.getLdgTrijet().E());
  TLorentzVector trijet_check;
  trijet_check = TrijetLorentz;

  trijet_check.Boost(-TrijetLorentz.BoostVector()); //Check that trijet is at rest at its center of mass
  //  std::cout<<"px = "<<trijet_check.Px()<<" py = "<<trijet_check.Py()<<" pz = "<<trijet_check.Pz()<<" E = "<<trijet_check.E()<<" M = "<<trijet_check.M()<<std::endl;

  for (size_t i=0; i < bjetData.getSelectedBJets().size(); i++ ){
    TLorentzVector bjetP4;
    bjetP4.SetPtEtaPhiE(jetData.getAllJets().at(i).pt(),jetData.getAllJets().at(i).eta(),jetData.getAllJets().at(i).phi(),jetData.getAllJets().at(i).e());
    bjetP4.Boost(-TrijetLorentz.BoostVector());

    float b_theta = 2*atan(exp(-bjetP4.Eta()));
    float t_theta = 2*atan(exp(-TrijetLorentz.Eta() ));

    if (i==0) {
      cosTheta_Bjet1TopCM_TrijetLab = std::cos(std::abs(b_theta-t_theta));
      cosTheta_Bjet1TopCM_Zaxis     = std::cos(b_theta);
    }
    if (i==1){
      cosTheta_Bjet2TopCM_TrijetLab = std::cos(std::abs(b_theta-t_theta));
      cosTheta_Bjet2TopCM_Zaxis     = std::cos(b_theta);
    }
    if (i==2){
      cosTheta_Bjet3TopCM_TrijetLab = std::cos(std::abs(b_theta-t_theta));
      cosTheta_Bjet3TopCM_Zaxis     = std::cos(b_theta);
    }
  }
  
  metOverSqrtHT = METData.getMET().R() / TopologyData.HT();

  TLorentzVector ldgtrijetJet1, ldgtrijetJet2, ldgtrijetB;
  TLorentzVector subldgtrijetJet1, subldgtrijetJet2, subldgtrijetB;

  if (TopData.getTriJet1().Pt() > TopData.getTriJet2().Pt()){

    ldgtrijetJet1.SetPtEtaPhiE(TopData.getTrijet1Jet1().pt(),TopData.getTrijet1Jet1().eta(),TopData.getTrijet1Jet1().phi(),TopData.getTrijet1Jet1().e());
    ldgtrijetJet2.SetPtEtaPhiE(TopData.getTrijet1Jet2().pt(),TopData.getTrijet1Jet2().eta(),TopData.getTrijet1Jet2().phi(),TopData.getTrijet1Jet2().e());
    ldgtrijetB.SetPtEtaPhiE(TopData.getTrijet1BJet().pt(),TopData.getTrijet1BJet().eta(),TopData.getTrijet1BJet().phi(),TopData.getTrijet1BJet().e());

    subldgtrijetJet1.SetPtEtaPhiE(TopData.getTrijet2Jet1().pt(),TopData.getTrijet2Jet1().eta(),TopData.getTrijet2Jet1().phi(),TopData.getTrijet2Jet1().e());
    subldgtrijetJet2.SetPtEtaPhiE(TopData.getTrijet2Jet2().pt(),TopData.getTrijet2Jet2().eta(),TopData.getTrijet2Jet2().phi(),TopData.getTrijet2Jet2().e());
    subldgtrijetB.SetPtEtaPhiE(TopData.getTrijet2BJet().pt(),TopData.getTrijet2BJet().eta(),TopData.getTrijet2BJet().phi(),TopData.getTrijet2BJet().e());
    
    ldgTrijetLdgJetBDisc    = TopData.getTrijet1Jet1().bjetDiscriminator();
    ldgTrijetSubldgJetBDisc = TopData.getTrijet1Jet2().bjetDiscriminator();

    subldgTrijetLdgJetBDisc    = TopData.getTrijet2Jet1().bjetDiscriminator();
    subldgTrijetSubldgJetBDisc = TopData.getTrijet2Jet2().bjetDiscriminator();
    
  }
  else{
    ldgtrijetJet1.SetPtEtaPhiE(TopData.getTrijet2Jet1().pt(),TopData.getTrijet2Jet1().eta(),TopData.getTrijet2Jet1().phi(),TopData.getTrijet2Jet1().e());
    ldgtrijetJet2.SetPtEtaPhiE(TopData.getTrijet2Jet2().pt(),TopData.getTrijet2Jet2().eta(),TopData.getTrijet2Jet2().phi(),TopData.getTrijet2Jet2().e());
    ldgtrijetB.SetPtEtaPhiE(TopData.getTrijet2BJet().pt(),TopData.getTrijet2BJet().eta(),TopData.getTrijet2BJet().phi(),TopData.getTrijet2BJet().e());

    subldgtrijetJet1.SetPtEtaPhiE(TopData.getTrijet1Jet1().pt(),TopData.getTrijet1Jet1().eta(),TopData.getTrijet1Jet1().phi(),TopData.getTrijet1Jet1().e());
    subldgtrijetJet2.SetPtEtaPhiE(TopData.getTrijet1Jet2().pt(),TopData.getTrijet1Jet2().eta(),TopData.getTrijet1Jet2().phi(),TopData.getTrijet1Jet2().e());
    subldgtrijetB.SetPtEtaPhiE(TopData.getTrijet1BJet().pt(),TopData.getTrijet1BJet().eta(),TopData.getTrijet1BJet().phi(),TopData.getTrijet1BJet().e());

    ldgTrijetLdgJetBDisc    = TopData.getTrijet1Jet2().bjetDiscriminator();
    ldgTrijetSubldgJetBDisc = TopData.getTrijet1Jet1().bjetDiscriminator();

    subldgTrijetLdgJetBDisc    = TopData.getTrijet2Jet2().bjetDiscriminator();
    subldgTrijetSubldgJetBDisc = TopData.getTrijet2Jet1().bjetDiscriminator();


  }

  trijet_check.Boost(-TrijetLorentz.BoostVector());
  
  ldgtrijetJet1.Boost(-TrijetLorentz.BoostVector());
  ldgtrijetJet2.Boost(-TrijetLorentz.BoostVector());
  ldgtrijetB.Boost(-TrijetLorentz.BoostVector());

  subldgtrijetJet1.Boost(-TrijetLorentz.BoostVector());
  subldgtrijetJet2.Boost(-TrijetLorentz.BoostVector());
  subldgtrijetB.Boost(-TrijetLorentz.BoostVector());

  float ldgtrijetJet1_theta    = 2*atan(exp(-ldgtrijetJet1.Eta()));
  float ldgtrijetJet2_theta    = 2*atan(exp(-ldgtrijetJet2.Eta()));
  float ldgtrijetB_theta       = 2*atan(exp(-ldgtrijetB.Eta()));
  float subldgtrijetJet1_theta = 2*atan(exp(-subldgtrijetJet1.Eta()));
  float subldgtrijetJet2_theta = 2*atan(exp(-subldgtrijetJet2.Eta()));
  float subldgtrijetB_theta    = 2*atan(exp(-subldgtrijetB.Eta()));
  
  float t_theta                = 2*atan(exp(-TrijetLorentz.Eta() ));

  cosTheta_LdgTrijetLdgJetTopCM_TrijetLab       =  std::cos(std::abs(ldgtrijetJet1_theta-t_theta));
  cosTheta_LdgTrijetSubldgJetTopCM_TrijetLab    =  std::cos(std::abs(ldgtrijetJet2_theta-t_theta));
  cosTheta_LdgTrijetBjetTopCM_TrijetLab         =  std::cos(std::abs(ldgtrijetB_theta-t_theta));
  cosTheta_SubldgTrijetLdgJetTopCM_TrijetLab    =  std::cos(std::abs(subldgtrijetJet1_theta-t_theta));
  cosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab =  std::cos(std::abs(subldgtrijetJet2_theta-t_theta));
  cosTheta_SubldgTrijetBjetTopCM_TrijetLab      =  std::cos(std::abs(subldgtrijetB_theta-t_theta));
  
  hTminusSumScPt_LdgTop_SubldgTop  = ht - TopData.getLdgTrijet().Pt() - TopData.getSubldgTrijet().Pt();
  hTminusSumVecPt_LdgTop_SubldgTop = ht - (TopData.getLdgTrijet()+TopData.getSubldgTrijet()).Pt();


  //Variables from AN-16-437
  ldgTrijetPtDR         = TopData.getLdgTrijet().Pt()*std::abs(ROOT::Math::VectorUtil::DeltaPhi(ldgtrijetJet1,TopData.getLdgTrijetBJet().p4()));
  ldgTrijetDijetPtDR    = TopData.getLdgTrijetDijet().Pt()*std::abs(ROOT::Math::VectorUtil::DeltaPhi(ldgtrijetJet1,ldgtrijetJet2));
  ldgTrijetBjetMass     = TopData.getLdgTrijetBJet().p4().M();
  ldgTrijetLdgJetPt     = ldgtrijetJet1.Pt();
  ldgTrijetLdgJetEta    = ldgtrijetJet1.Eta();
  ldgTrijetSubldgJetPt  = ldgtrijetJet2.Pt();
  ldgTrijetSubldgJetEta = ldgtrijetJet2.Eta();

  ldgTrijetBJetLdgJetMass    = (ldgtrijetB+ldgtrijetJet1).M();
  ldgTrijetBJetSubldgJetMass = (ldgtrijetB+ldgtrijetJet2).M();


  subldgTrijetPtDR         = TopData.getSubldgTrijet().Pt()*std::abs(ROOT::Math::VectorUtil::DeltaPhi(subldgtrijetJet1,TopData.getSubldgTrijetBJet().p4()));
  subldgTrijetDijetPtDR    = TopData.getSubldgTrijetDijet().Pt()*std::abs(ROOT::Math::VectorUtil::DeltaPhi(subldgtrijetJet1,subldgtrijetJet2));
  subldgTrijetBjetMass     = TopData.getSubldgTrijetBJet().p4().M();
  subldgTrijetLdgJetPt     = subldgtrijetJet1.Pt();
  subldgTrijetLdgJetEta    = subldgtrijetJet1.Eta();
  subldgTrijetSubldgJetPt  = subldgtrijetJet2.Pt();
  subldgTrijetSubldgJetEta = subldgtrijetJet2.Eta();

  subldgTrijetBJetLdgJetMass    = (subldgtrijetB+subldgtrijetJet1).M();
  subldgTrijetBJetSubldgJetMass = (subldgtrijetB+subldgtrijetJet2).M();
  
  ldgTrijetDijetMass    = TopData.getLdgTrijetDijet().M();
  subldgTrijetDijetMass = TopData.getSubldgTrijetDijet().M();
  
  ldgTrijetBJetBDisc    = TopData.getLdgTrijetBJet().bjetDiscriminator();
  subldgTrijetBJetBDisc = TopData.getSubldgTrijetBJet().bjetDiscriminator();

  //next 



  //FILL HISTOS
  h_DPhi_LdgTrijet_SubldgTrijet  -> Fill(dPhi_LdgTrijet_SubldgTrijet);
  h_Rapidity_LdgTrijet           -> Fill(rapidity_LdgTrijet);
  h_Rapidity_SubldgTrijet        -> Fill(rapidity_SubldgTrijet);
  h_Rapidity_Tetrajet            -> Fill(rapidity_Tetrajet);
  h_SumPt_LdgTrijet_SubldgTrijet -> Fill(sumPt_LdgTrijet_SubldgTrijet);

  h_CosTheta_Bjet1TopCM_TrijetLab -> Fill(cosTheta_Bjet1TopCM_TrijetLab);
  h_CosTheta_Bjet1TopCM_Zaxis     -> Fill(cosTheta_Bjet1TopCM_Zaxis);
  h_CosTheta_Bjet2TopCM_TrijetLab -> Fill(cosTheta_Bjet2TopCM_TrijetLab);
  h_CosTheta_Bjet2TopCM_Zaxis     -> Fill(cosTheta_Bjet2TopCM_Zaxis);
  h_CosTheta_Bjet3TopCM_TrijetLab -> Fill(cosTheta_Bjet3TopCM_TrijetLab);
  h_CosTheta_Bjet3TopCM_Zaxis     -> Fill(cosTheta_Bjet3TopCM_Zaxis);


  h_CosTheta_LdgTrijetLdgJetTopCM_TrijetLab       -> Fill(cosTheta_LdgTrijetLdgJetTopCM_TrijetLab);
  h_CosTheta_LdgTrijetSubldgJetTopCM_TrijetLab    -> Fill(cosTheta_LdgTrijetSubldgJetTopCM_TrijetLab);
  h_CosTheta_LdgTrijetBjetTopCM_TrijetLab         -> Fill(cosTheta_LdgTrijetBjetTopCM_TrijetLab);

  h_CosTheta_SubldgTrijetLdgJetTopCM_TrijetLab    -> Fill(cosTheta_SubldgTrijetLdgJetTopCM_TrijetLab);
  h_CosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab -> Fill(cosTheta_SubldgTrijetSubldgJetTopCM_TrijetLab);
  h_CosTheta_SubldgTrijetBjetTopCM_TrijetLab      -> Fill(cosTheta_SubldgTrijetBjetTopCM_TrijetLab);
  
  h_DEta_LdgTrijetDijet_TetrajetB -> Fill(dEta_LdgTrijetDijet_TetrajetB);
  h_DPhi_TetrajetB_LdgTrijetB     -> Fill(dPhi_TetrajetB_LdgTrijetB);
  h_DEta_TetrajetB_LdgTrijetB     -> Fill(dEta_TetrajetB_LdgTrijetB);

  h_DPhi_LdgTrijetB_SubldgTrijetB -> Fill(dPhi_LdgTrijetB_SubldgTrijetB);
  h_DPhi_TetrajetB_SubldgTrijetB  -> Fill(dPhi_TetrajetB_SubldgTrijetB);
  h_DPhi_TetrajetB_LdgTrijetB     -> Fill(dPhi_TetrajetB_LdgTrijetB);
  h_DEta_LdgTrijetB_SubldgTrijetB -> Fill(dEta_LdgTrijetB_SubldgTrijetB);
  h_DEta_TetrajetB_SubldgTrijetB  -> Fill(dEta_TetrajetB_SubldgTrijetB);
  h_DEta_TetrajetB_LdgTrijetB     -> Fill(dEta_TetrajetB_LdgTrijetB);
  h_DR_LdgTrijetB_SubldgTrijetB   -> Fill(dR_LdgTrijetB_SubldgTrijetB);
  h_DR_TetrajetB_SubldgTrijetB    -> Fill(dR_TetrajetB_SubldgTrijetB);
  h_DR_TetrajetB_LdgTrijetB       -> Fill(dR_TetrajetB_LdgTrijetB);

  h_PtAsy -> Fill(ptAsy);


  h_Tetrajet_Mass -> Fill(ldgTetraJet_Mass);

  h_HTminusSumScPt_LdgTop_SubldgTop  -> Fill(hTminusSumScPt_LdgTop_SubldgTop);
  h_HTminusSumVecPt_LdgTop_SubldgTop -> Fill(hTminusSumVecPt_LdgTop_SubldgTop);

  //next fill histo
  //=======================================================                                                 
  // All Jets                                                           
  //=======================================================
  
  float CSV_sum, CSV_PtWeighted_sum, CSV_PtSqrWeighted_sum, Pt_sum, PtSqr_sum;
  int N_jets;

  CSV_sum = 0;
  CSV_PtWeighted_sum = 0;
  CSV_PtSqrWeighted_sum = 0;
  N_jets = 0;
  Pt_sum = 0;
  PtSqr_sum = 0;
  
  // For-Loop: All jets                                                                                                                  
  for (size_t i=0; i != jetData.getAllJets() .size(); i++ ) {
    
    Jet jet;
    jet = jetData.getAllJets().at(i);
    
    // Count for maximum 10 jets                                                                                                        
    if (i<10) {
      CSV_sum                 += jet.bjetDiscriminator();
      CSV_PtWeighted_sum      += jet.bjetDiscriminator() * jet.pt() ;
      CSV_PtSqrWeighted_sum   += jet.bjetDiscriminator() * jet.pt() * jet.pt();
      
      N_jets  ++;
      Pt_sum    += jet.pt();
      PtSqr_sum += jet.pt() * jet.pt();
    }
    else {
      continue;
    }

  }// For-Loop: All jets 

  // Fill Histos 
  h_AvgCSV               -> Fill( CSV_sum / N_jets );
  h_AvgCSV_PtWeighted    -> Fill( CSV_PtWeighted_sum / Pt_sum );
  h_AvgCSV_PtSqrWeighted -> Fill( CSV_PtSqrWeighted_sum /  PtSqr_sum );



  //=======================================================
  // Selected Jets
  //=======================================================

  //=== Pt & Abs(Eta) of the first 6 Jets

  double jet_Pt;
  math::XYZTLorentzVector ldgJet_p4(0,0,0,0), temp_p4(0,0,0,0);
  std::vector<math::XYZTLorentzVector> Jets_p4;
  Jets_p4.clear();
  // For-Loop: Selected Jets
  for (size_t i=0; i < jetData.getSelectedJets().size(); i++ )
    {
      // Get the Pt and Eta of the Selected Jets
      jet_Pt  = jetData.getSelectedJets().at(i).pt();

      // Get the p4 of the leading jet
      if (i == 0) {
	ldgJet_p4 = jetData.getSelectedJets().at(i).p4();
      }

      temp_p4 = jetData.getSelectedJets().at(i).p4();
      Jets_p4.push_back(temp_p4);

      if (i==1) recoJet2_pt     =jet_Pt;
      if (i==2) recoJet3_pt     =jet_Pt;
      if (i==3) recoJet4_pt     =jet_Pt;
      if (i==4) recoJet5_pt     =jet_Pt;
      if (i==5) recoJet6_pt     =jet_Pt;
      if (i==6) recoJet7_pt     =jet_Pt;
      
    } // For-loop: Selected Jets

  float dPhi_j1j2 = std::abs(ROOT::Math::VectorUtil::DeltaPhi(Jets_p4.at(0),Jets_p4.at(1)));
  float dEta_j1j2 = std::abs(Jets_p4.at(0).Eta() - Jets_p4.at(1).Eta() );
  float dR_j1j2   = ROOT::Math::VectorUtil::DeltaR(Jets_p4.at(0),Jets_p4.at(1));

  float dPhi_j3j4 = std::abs(ROOT::Math::VectorUtil::DeltaPhi(Jets_p4.at(2),Jets_p4.at(3)));
  float dEta_j3j4 = std::abs(Jets_p4.at(2).Eta() - Jets_p4.at(3).Eta() );
  float dR_j3j4   = ROOT::Math::VectorUtil::DeltaR(Jets_p4.at(2),Jets_p4.at(3));

  float dPhi_j5j6 = std::abs(ROOT::Math::VectorUtil::DeltaPhi(Jets_p4.at(4),Jets_p4.at(5)));
  float dEta_j5j6 = std::abs(Jets_p4.at(4).Eta() - Jets_p4.at(5).Eta() );
  float dR_j5j6   = ROOT::Math::VectorUtil::DeltaR(Jets_p4.at(4),Jets_p4.at(5));

  dPhiJ34 = dPhi_j3j4;
  dPhiJ56 = dPhi_j5j6;


  h_DPhiJ12vsDPhiJ34 -> Fill(dPhi_j1j2,dPhi_j3j4);
  h_DEtaJ12vsDEtaJ34 -> Fill(dEta_j1j2,dEta_j3j4);
  h_DRJ12vsDRJ34     -> Fill(dR_j1j2,dR_j3j4);

  h_DPhiJ12vsDPhiJ56 -> Fill(dPhi_j1j2,dPhi_j5j6);
  h_DEtaJ12vsDEtaJ56 -> Fill(dEta_j1j2,dEta_j5j6);
  h_DRJ12vsDRJ56     -> Fill(dR_j1j2,dR_j5j6);

  h_DPhiJ34vsDPhiJ56 -> Fill(dPhi_j3j4,dPhi_j5j6);
  h_DEtaJ34vsDEtaJ56 -> Fill(dEta_j3j4,dEta_j5j6);
  h_DRJ34vsDRJ56     -> Fill(dR_j3j4,dR_j5j6);


  h_DPhiJ34 -> Fill(dPhi_j3j4);
  h_DPhiJ56 -> Fill(dPhi_j5j6);

  dPhiDistance = sqrt((dPhi_j3j4-3.14)*(dPhi_j3j4-3.14)+(dPhi_j5j6-3.14)*(dPhi_j5j6-3.14));
  double dPhi_distance = sqrt((dPhi_j3j4-3.14)*(dPhi_j3j4-3.14)+(dPhi_j5j6-3.14)*(dPhi_j5j6-3.14));
  
  dPhiCircle = sqrt(dPhi_j3j4*dPhi_j3j4+dPhi_j5j6*dPhi_j5j6);

  h_DPhiDistance_J34_J56 -> Fill(dPhi_distance);
  h_DPhiCircle_J34_J56   -> Fill(dPhiCircle);

  //h_DPhiJ34vsDPhiJ56_wCut05
  if (dPhi_distance > 0.25*0.25) h_DPhiJ34vsDPhiJ56_wCut025 -> Fill(dPhi_j3j4,dPhi_j5j6);
  if (dPhi_distance > 0.5*0.5)   h_DPhiJ34vsDPhiJ56_wCut05  -> Fill(dPhi_j3j4,dPhi_j5j6);
  if (dPhi_distance > 0.75*0.75) h_DPhiJ34vsDPhiJ56_wCut075 -> Fill(dPhi_j3j4,dPhi_j5j6);
  if (dPhi_distance > 1.0)       h_DPhiJ34vsDPhiJ56_wCut10  -> Fill(dPhi_j3j4,dPhi_j5j6);
  if (dPhi_distance > 1.25*1.25) h_DPhiJ34vsDPhiJ56_wCut125 -> Fill(dPhi_j3j4,dPhi_j5j6);
  if (dPhi_distance > 1.5*1.5)   h_DPhiJ34vsDPhiJ56_wCut15  -> Fill(dPhi_j3j4,dPhi_j5j6);
  

  //next fill histograms
  vector <math::XYZTLorentzVector> GenJets_vector;
  GenJets_vector.clear();
  //Matching for jets 3,4,5,6
  for (size_t i=0; i < jetData.getSelectedJets().size(); i++ ){
    if (i<3) continue;
    math::XYZTLorentzVector recoJet_p4;
    recoJet_p4 = jetData.getSelectedJets().at(i).p4();
    double dRmin = 1000.0;
    math::XYZTLorentzVector genJmin_p4(0,0,0,0);

    //For-loop: GenJets
    for(GenJet j: fEvent.genjets()) {
      math::XYZTLorentzVector genJ_p4;
      genJ_p4 = j.p4();
      double dR_ij = ROOT::Math::VectorUtil::DeltaR(recoJet_p4, genJ_p4);
      if (dRmin < dR_ij || dR_ij >0.4) continue;
      dRmin = dR_ij;
      genJmin_p4 = j.p4();   
    }
    
  }

  //For-loop: GenParticles
  for (auto& p: fEvent.genparticles().getGenParticles()) {
    // Particle properties                                                                                                                                                               
    short genP_index     = p.index();
    int genP_pdgId       = p.pdgId();
    int genP_status      = p.status();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_ene      = p.e();
    //    int genP_charge      = p.charge();
    
    int genMom_index    = -1;
    double genMom_pdgId = 999.999;
    
    math::XYZTLorentzVector genP_p4;                                                                                                                                                  
    genP_p4 = p.p4(); 
    
    // Associated genParticles                                                                                                                                                           
    std::vector<genParticle> genP_daughters;
    std::vector<int> genP_daughtersIndex;
    for (unsigned int i=0; i < p.daughters().size(); i++){
      genP_daughters.push_back(fEvent.genparticles().getGenParticles()[p.daughters().at(i)]);
      genParticle dau = fEvent.genparticles().getGenParticles()[p.daughters().at(i)];
      genP_daughtersIndex.push_back(dau.index());
    }
    std::vector<genParticle> genP_mothers;
    std::vector<int> genP_mothersIndex;
    for (unsigned int i=0; i < p.mothers().size(); i++){
      genP_mothers.push_back(fEvent.genparticles().getGenParticles()[p.mothers().at(i)]);
      genParticle mom = fEvent.genparticles().getGenParticles()[p.mothers().at(i)];
      genP_mothersIndex.push_back(mom.index());
    }
    
    if (genMom_index >= 0){
      const Particle<ParticleCollection<double> > m = fEvent.genparticles().getGenParticles()[genMom_index];
      genMom_pdgId  = m.pdgId();
    }
    int firstMom = -1, lastMom = -1, firstDau = -1, lastDau = -1;
    if (genP_mothers.size() > 0){
      firstMom = genP_mothersIndex.at(0);
      //      std::cout<<genP_mothersIndex.at(genP_mothers.size()-1)<<std::endl;
      lastMom  = genP_mothersIndex.at(genP_mothers.size()-1);
    }
    if (genP_daughters.size() >0){
      firstDau = genP_daughtersIndex.at(0);
      lastDau  = genP_daughtersIndex.at(genP_daughters.size()-1);
    }
    if (0){
      if (genP_index == 0){
      std::cout << "\n" << std::endl;                                                                                                                                                    
      std::cout << std::string(15*10, '=') << std::endl;                                                                                                                                      std::cout << std::setw(12) << "Index "  << std::setw(12) << "PdgId"                                                                                                                               << std::setw(12) << "Pt"      << std::setw(12) << "Eta"   << std::setw(12) << "Phi"                                                                                         
		<< std::setw(12) << "Energy"  << std::setw(12) << "Mass"  << std::setw(12) << "status"<<std::setw(12) << "1st Mom-Idx"                                                                                   
		<< std::setw(15) << "last Mom-Idx" << std::setw(12) << "Nmothers" \
		<< std::setw(12) << "1st Dau-Idx"  << std::setw(15) << "last Dau-Idx" << std::setw(12) << "NDaughters"<<std::endl;                                                                                                                               
      std::cout << std::string(15*10, '=') << std::endl;
      }
      std::cout << std::setw(12) << genP_index            << std::setw(12)   << genP_pdgId  
		<< std::setw(12) << genP_pt               << std::setw(12)   << genP_eta       
		<< std::setw(12) << genP_phi              << std::setw(12)   << genP_ene      
		<< std::setw(12) << genP_p4.M()           << std::setw(12)   << genP_status               <<std::setw(12)   << firstMom  
		<< std::setw(12) << lastMom               << std::setw(12)   << genP_mothers.size()  
		<< std::setw(12) << firstDau              << std::setw(12)   << lastDau 
		<< std::setw(12) << genP_daughters.size() <<  std::endl;
    }
    
    // if (std::abs(genP_pdgId) == 37 && isLastCopy  (genP_index, 37 )) Higgs = genP_p4;
    // if (std::abs(genP_pdgId) == 6  && isFirstCopy (genP_index, 6  )) FirstTop.push_back(genP_p4);
    
  }

  
  //  std::cout<<"=========="std::endl;
  //=== Number of Jets
  h_Jets_N   -> Fill ( jetData.getNumberOfSelectedJets() );

  //=== B-Tagged Jets                                                                                                     
  h_BJets_N  -> Fill ( bjetData.getNumberOfSelectedBJets() );

  //=== untagged Jets 
  h_untaggedJets_N -> Fill (jetData.getNumberOfSelectedJets()- bjetData.getNumberOfSelectedBJets() );

  // Minimum and Maximum phi angle between a jet and (MHT-jet)
  h_minDeltaPhiJetMHT -> Fill ( jetData.minDeltaPhiJetMHT() );
  h_maxDeltaPhiJetMHT -> Fill ( jetData.maxDeltaPhiJetMHT() );

  // Minimum Delta R between a jet and (MHT-jet), -(MHT-jet)
  h_minDeltaRJetMHT         -> Fill ( jetData.minDeltaRJetMHT());
  h_minDeltaRReversedJetMHT -> Fill ( jetData.minDeltaRReversedJetMHT());

  // TTree Variables 
  ldgJet_Pt = ldgJet_p4.pt(); 
  jets_N    = jetData.getNumberOfSelectedJets();
  bjets_N   = bjetData.getNumberOfSelectedBJets();

  //=======================================================                                                        
  // Di-Jet                                                                                                            
  //=======================================================  

  //=== B-Tagged Di-Jet  (Average dR, dPhi, dEta, MaxMass Di-Jet, MaxPt Di-Jet, dRMin Di-Jet)

  // Initialize values                                                                                                           
  int nBPairs        = 0;
  double dR          = 0.0;
  double dEta        = 0.0;
  double dPhi        = 0.0;
  double dRSum       = 0.0;
  double dEtaSum     = 0.0;
  double dPhiSum     = 0.0;
  double deltaRMin   = 999999.9;
  double deltaPhiMin = 999999.9;
  double deltaPhiMax = 0 ;
  int deltaRMin_i    = -1;
  int deltaRMin_j    = -1;
  
  math::XYZTLorentzVector maxPt_p4(0,0,0,0);
  math::XYZTLorentzVector maxMass_p4(0,0,0,0);

  math::XYZTLorentzVector i_p4;
  math::XYZTLorentzVector j_p4;
  double bjet_Pt,bjet_Eta;
  math::XYZTLorentzVector bJetPair_dRMin_p4;
  math::XYZTLorentzVector bJetPair_dPhiMin_p4(0,0,0,0);
  math::XYZTLorentzVector bJetPair_dPhiMax_p4(0,0,0,0);
  
  // For-loop: All b-jets
  for (size_t i=0; i != bjetData.getSelectedBJets().size()-1; i++ ){

    // Get the Pt and Eta of the Selected Jets                                               
    bjet_Pt  = bjetData.getSelectedBJets().at(i).pt();
    bjet_Eta = bjetData.getSelectedBJets().at(i).eta();

    // Fill histos with Pt and abs(Eta) for the first 6 jets                                             
    if ( i<3 )
      {
	vh_BJets_Pt.at(i)     -> Fill ( bjet_Pt        );
	vh_BJets_AbsEta.at(i) -> Fill ( std::abs(bjet_Eta) );
      }

    // Initialise values                                                                                                                 
    dR      = 0.0;
    dEta    = 0.0;
    dPhi    = 0.0;
    // Get the p4 of the i-jet 
    i_p4= bjetData.getSelectedBJets().at(i).p4();
  
    // For-loop: All b-Jets                                                                                                    
    for (size_t j=i+1; j != bjetData.getSelectedBJets().size(); j++ ){

      // Get the p4 of the j-jet
      j_p4= bjetData.getSelectedBJets().at(j).p4();
      
      // Calculate dR, dEta, dPhi
      dR   = ROOT::Math::VectorUtil::DeltaR(i_p4, j_p4); 
      dEta = std::abs(i_p4.Eta() - j_p4.Eta() );
      dPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(i_p4, j_p4)); 

      // Increase the counter for BJetPairs
      nBPairs++;

      // Get the total p4 of the BJetPair
      math::XYZTLorentzVector pair_p4;
      pair_p4 = i_p4 + j_p4;
 
      //Find the maxPt BJetPair
      if ( pair_p4.Pt() > maxPt_p4.Pt() ) maxPt_p4   = pair_p4;
      // Find the maxMass BJetPair
      if ( pair_p4.M() > maxMass_p4.M() )  maxMass_p4   = pair_p4;
      // Find the dPhiMin BJetPair
      if (dPhi < deltaPhiMin)  bJetPair_dPhiMin_p4 = pair_p4;
      // Find the dPhiMax BJetPair                                                                                                        
      if (dPhi > deltaPhiMax) bJetPair_dPhiMax_p4 =pair_p4;

      //Find the Jets with the minimum dR and their dRMin                                                                                 
      if (dR < deltaRMin)
	{
	  deltaRMin = dR;
	  deltaRMin_i = i;
	  deltaRMin_j = j;
	}

      // Calculate the Total dR, dEta, dPhi                                                                                         
      dRSum   += dR;
      dEtaSum += dEta;
      dPhiSum += dPhi;
    }
  }

  // Fill Histos                                                                                                                         
  h_BJetPair_dRAverage    -> Fill ( dRSum/nBPairs   );
  h_BJetPair_dEtaAverage  -> Fill ( dEtaSum/nBPairs );
  h_BJetPair_dPhiAverage  -> Fill ( dPhiSum/nBPairs );
  //
  h_BJetPair_Rbb   -> Fill ( std::sqrt( ((3.14159265359-(dPhiSum/nBPairs))*(3.14159265359-(dPhiSum/nBPairs))) + ((dEtaSum/nBPairs)*(dEtaSum/nBPairs))));
  //                                                       
  h_BJetPair_MaxPt_Pt     -> Fill ( maxPt_p4.Pt()   );
  h_BJetPair_MaxPt_M      -> Fill ( maxPt_p4.M()    );
  //
  h_BJetPair_MaxMass_Pt   -> Fill ( maxMass_p4.Pt() );
  h_BJetPair_MaxMass_M    -> Fill ( maxMass_p4.M()  );
  //
  h_BJetPair_dPhiMin_Pt   -> Fill( bJetPair_dPhiMin_p4.pt() );
  h_BJetPair_dPhiMin_Mass -> Fill( bJetPair_dPhiMin_p4.mass() );
  //
  h_BJetPair_dPhiMax_Pt   -> Fill( bJetPair_dPhiMax_p4.pt() );
  h_BJetPair_dPhiMax_Mass -> Fill( bJetPair_dPhiMax_p4.mass() );


  if (deltaRMin_i>= 0  && deltaRMin_j >= 0)
    {
      // Get the total p4 of the b-jet pair with the dRMin                                                        
      bJetPair_dRMin_p4 = bjetData.getSelectedBJets().at(deltaRMin_i).p4() + bjetData.getSelectedBJets().at(deltaRMin_j).p4();
      double dRMinBJetPair_dEta = std::abs(bjetData.getSelectedBJets().at(deltaRMin_i).eta() - bjetData.getSelectedBJets().at(deltaRMin_j).eta());
      double dRMinBJetPair_dPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(bjetData.getSelectedBJets().at(deltaRMin_i).p4(), bjetData.getSelectedBJets().at(deltaRMin_j).p4()));

      double  dRMinBJetPair_Rbb = std::sqrt( ((3.14159265359-(dRMinBJetPair_dPhi))*(3.14159265359-(dRMinBJetPair_dPhi))) + ((dRMinBJetPair_dEta)*(dRMinBJetPair_dEta)));
 

      // Fill Histos                                                                                                                    
      h_BJetPair_dRMin_Pt   -> Fill( bJetPair_dRMin_p4.pt() );
      h_BJetPair_dRMin_dR   -> Fill( deltaRMin );
      h_BJetPair_dRMin_Mass -> Fill( bJetPair_dRMin_p4.mass() );
      h_BJetPair_dRMin_dEta -> Fill( dRMinBJetPair_dEta );
      h_BJetPair_dRMin_dPhi -> Fill( dRMinBJetPair_dPhi );
      h_BJetPair_dRMin_Rbb  -> Fill( dRMinBJetPair_Rbb);

      // Get the dR, dEta, dPhi of ldg jet and b-jet pair with the dRMin
      h_ldgJet_dRMinBJetPair_dR    -> Fill ( ROOT::Math::VectorUtil::DeltaR( ldgJet_p4, bJetPair_dRMin_p4) );
      h_ldgJet_dRMinBJetPair_dPhi  -> Fill ( ROOT::Math::VectorUtil::DeltaPhi( ldgJet_p4, bJetPair_dRMin_p4) );
      h_ldgJet_dRMinBJetPair_dEta  -> Fill ( std::abs(ldgJet_p4.eta() - bJetPair_dRMin_p4.eta()) );

      bJetPair_dRMin_M          = bJetPair_dRMin_p4.mass();

    }


  // =========================================================================
   
  //=== Jet5,6,7-BJetsFirst
  
  // Define the Discriminator Value
  double fDiscriminatorValue = 0.5426;
  
  // Find the Non-Selected B-Jets
  std::vector<math::XYZTLorentzVector> selNoBJets_p4;
  
  // For-Loop: All Selected Jets
  for (size_t i=0; i != jetData.getSelectedJets().size(); i++ )
    {
      Jet jet;
      jet = jetData.getSelectedJets().at(i);
      
      //=== Check if is B-Jet and if not, keep it  
      if (!(jet.bjetDiscriminator() > fDiscriminatorValue)) {
	math::XYZTLorentzVector jet_p4;
	jet_p4 = jet.p4();
	selNoBJets_p4.push_back(jet_p4);
      }
    }
  

  // Create vectors for the Selected BJets and the Selected Jets(BJetsFirst)
  std::vector<math::XYZTLorentzVector> selBJets_p4;
  std::vector<math::XYZTLorentzVector> selJets_BJetsFirst_p4;

  // Insert all Selected BJets
  for (size_t i=0; i != bjetData.getSelectedBJets().size(); i++ )
    {
      Jet jet;
      jet = bjetData.getSelectedBJets().at(i);

      math::XYZTLorentzVector jet_p4;
      jet_p4 = jet.p4();
      selBJets_p4.push_back(jet_p4);
    }
  
  // =========================================================================
  
  //=== Non BJets

  math::XYZTLorentzVector untaggedLdgJet_p4(0,0,0,0);


  if (selNoBJets_p4.size()>1)
    {

      //======= Di-Jet (drMin) - No BJets

      double _deltaRMin = 999999.9;
      int _deltaRMin_i  = -1;
      int _deltaRMin_j  = -1;
      int _i=-1;
      int _j=-1;
      
      for (auto& i: selNoBJets_p4)
        {
 	  _i++;
          _j=-1;

	  // Get the P4 of the untagged leading jet
	  if (_i==0) untaggedLdgJet_p4 = selNoBJets_p4.at(_i);


	  for (auto& j: selNoBJets_p4)
	    {
              _j++;
              if (_i==_j) continue;
              double deltaR = ROOT::Math::VectorUtil::DeltaR(i, j);
              if (deltaR < _deltaRMin)
		{
                  _deltaRMin = deltaR;
                  _deltaRMin_i = _i;
                  _deltaRMin_j = _j;
                }
	    }
	}

      if (_deltaRMin_i > -1  && _deltaRMin_j > -1)
	{
	  // GenJets: Untagged jet pair with min dR                                                                                      
	  math::XYZTLorentzVector dRMinDiJet_NoBJets_p4 = selNoBJets_p4.at(_deltaRMin_i) + selNoBJets_p4.at(_deltaRMin_j);
	  h_dRMinDiJet_noBJets_Pt   ->Fill( dRMinDiJet_NoBJets_p4.Pt() );
	  h_dRMinDiJet_noBJets_M    ->Fill( dRMinDiJet_NoBJets_p4.M() );
	  
	  // TTree Variables
	  //	  dRMinDiJet_noBJets_M =dRMinDiJet_NoBJets_p4.M();
	  dijetUntaggedSmallDR_Mass = dRMinDiJet_NoBJets_p4.M();
	}

      
      if (deltaRMin_i>= 0  && deltaRMin_j >= 0)
	{
	  // Get the dR, dEta, dPhi of untaggedLdg jet and b-jet pair with the dRMin                                     
	  h_untaggedLdgJet_dRMinBJetPair_dR    -> Fill ( ROOT::Math::VectorUtil::DeltaR( untaggedLdgJet_p4, bJetPair_dRMin_p4) );
	  h_untaggedLdgJet_dRMinBJetPair_dPhi  -> Fill ( ROOT::Math::VectorUtil::DeltaPhi( untaggedLdgJet_p4, bJetPair_dRMin_p4) );
	  h_untaggedLdgJet_dRMinBJetPair_dEta  -> Fill ( std::abs(untaggedLdgJet_p4.eta() - bJetPair_dRMin_p4.eta()) );
	}
    }

  //========== Average CSV Discriminant (non bjets)
  
  CSV_sum = 0;
  CSV_PtWeighted_sum = 0;
  CSV_PtSqrWeighted_sum = 0;
  N_jets = 0;
  Pt_sum = 0;
  PtSqr_sum = 0;
  
  // For-Loop: Non-bjets
  for (size_t i=0; i != bjetData.getFailedBJetCands().size(); i++ )
    {
      Jet jet;
      jet = bjetData.getFailedBJetCands().at(i);
      
      // Count for maximum 10 jets
      if (i<10) {
	CSV_sum                 += jet.bjetDiscriminator();
	CSV_PtWeighted_sum      += jet.bjetDiscriminator() * jet.pt() ;
	CSV_PtSqrWeighted_sum   += jet.bjetDiscriminator() * jet.pt() * jet.pt();
	
	N_jets  ++;
	Pt_sum    += jet.pt();
	PtSqr_sum += jet.pt() * jet.pt();
      }
      else {
	continue;
      }
      
    } // For-Loop: Non-bjets
  
  
  
  // Fill Histos 
  h_AvgCSV_noBjets               -> Fill( CSV_sum / N_jets );
  h_AvgCSV_PtWeighted_noBjets    -> Fill( CSV_PtWeighted_sum / Pt_sum );
  h_AvgCSV_PtSqrWeighted_noBjets -> Fill( CSV_PtSqrWeighted_sum /  PtSqr_sum );
  
  
  // ============================================================================
  
  //=== Tri-Jet (MaxPt)
  math::XYZTLorentzVector TriJetMaxPt_p4(0,0,0,0);
  
  // For-loop: All Selected Jets                                                                                                         
  for (size_t i=0; i != jetData.getSelectedJets().size()-2; i++ )
    {
      // For-loop: All Selected Jets (nested)                                                   
      for (size_t j=i+1; j != jetData.getSelectedJets().size()-1; j++ )
	{
	  // For-loop: All Selected Jets (doubly-nested)                                                                                
	  for (size_t k=j+1; k != jetData.getSelectedJets().size(); k++ )  
	    {
	      //std::cout<<"i=  "<<i<<" j=   "<<j<<" k=  "<<k<<std::endl;
	      math::XYZTLorentzVector SelJet_p4(0,0,0,0);
	      SelJet_p4= jetData.getSelectedJets().at(i).p4()+jetData.getSelectedJets().at(j).p4()+jetData.getSelectedJets().at(k).p4();
	      if ( SelJet_p4.Pt() > TriJetMaxPt_p4.Pt() )  TriJetMaxPt_p4 = SelJet_p4;
	    }
	}
    }
  
  // Fill Histos                                                                                                                         
  h_TriJet_MaxPt_Pt   -> Fill( TriJetMaxPt_p4.Pt()  );
  h_TriJet_MaxPt_Mass -> Fill( TriJetMaxPt_p4.M() );

  // TTree Variables
  triJet_maxPt_M  = TriJetMaxPt_p4.M();



  //=== Top Reconstruction - chi^2
  h_top_ChiSqr            ->    Fill(TopData.ChiSqr());

  //================================================================================================                 
  // Fill TTree                                                                                                                
  //================================================================================================  
  tree -> Fill();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  //  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, true);
  //  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, 1);
  
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();
  }
  
  
  
