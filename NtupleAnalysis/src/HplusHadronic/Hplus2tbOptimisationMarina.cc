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

class HplusHadronic: public BaseSelector {
public:
  explicit HplusHadronic(const ParameterSet& config, const TH1* skimCounters);
  virtual ~HplusHadronic() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
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

  WrappedTH1 *h_METoverSqrtHT;
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
  
  // TTree - TBranches
  TTree *tree;
  TBranch *weight;
  TBranch *LdgJet_Pt;                
  TBranch *BJetPair_dRMin_M;
  TBranch *Jet5_BJetsFirst_Pt;       
  TBranch *H2;                       
  TBranch *BJetPair_dRAvg;           
  TBranch *LdgJet_closestBJetPair_dR;
  TBranch *DiJet_noBJets_M;          
  TBranch *HT; 
  TBranch *BJetPair_maxPt_M;         
  TBranch *BJetPair_maxMass_M;       
  TBranch *TriJet_maxPt_M;           
  TBranch *Centrality;  

  TBranch *Jets_N;
  TBranch *BJets_N;
  TBranch *untaggedJets_N;

  TBranch *recoJet6_Pt;
  TBranch *recoJet7_Pt;
  TBranch *recoJet8_Pt;

  TBranch *Jet6_BJetsFirst_Pt;
  TBranch *Jet7_BJetsFirst_Pt;
  
  TBranch *BJetPair_dPhiMin_Pt;
  TBranch *BJetPair_dPhiMin_M;
  TBranch *BJetPair_dPhiMax_Pt;
  TBranch *BJetPair_dPhiMax_M;

  // Minimum and Maximum phi angle between a jet and (MHT-jet)                                                                            
 TBranch *minDeltaPhiJetMHT;
 TBranch *maxDeltaPhiJetMHT;

  // Minimum Delta R between a jet and (MHT-jet), -(MHT-jet)                                                                              
 TBranch *minDeltaRJetMHT;
 TBranch *minDeltaRReversedJetMHT;

  // Average CSV Discriminator for all jets                                                                                               
 TBranch *AvgCSV;
 TBranch *AvgCSV_PtWeighted;
 TBranch *AvgCSV_PtSqrWeighted;

  // Average CSV Discriminator for non-bjets                                                                                              
 TBranch *AvgCSV_noBjets;
 TBranch *AvgCSV_PtWeighted_noBjets;
 TBranch *AvgCSV_PtSqrWeighted_noBjets;



  TBranch *LdgTop_Pt;
  TBranch *LdgTop_Eta;
  TBranch *LdgTop_Phi;
  TBranch *LdgTop_Mass;
  TBranch *SubLdgTop_Pt;
  TBranch *SubLdgTop_Eta;
  TBranch *SubLdgTop_Phi;
  TBranch *SubLdgTop_Mass;
  TBranch *ChiSqr;
  TBranch *RedChiSqr;
  TBranch *BJet1BJet2_dR;
  TBranch *BJet1BJet2_dPhi;
  TBranch *BJet1BJet2_dEta;
  TBranch *DiJet1BJet1_dR;
  TBranch *DiJet1BJet1_dPhi;
  TBranch *DiJet1BJet1_dEta;
  TBranch *DiJet1BJet2_dR;
  TBranch *DiJet1BJet2_dPhi;
  TBranch *DiJet1BJet2_dEta;
  TBranch *DiJet2BJet1_dR;
  TBranch *DiJet2BJet1_dPhi;
  TBranch *DiJet2BJet1_dEta;
  TBranch *DiJet2BJet2_dR;
  TBranch *DiJet2BJet2_dPhi;
  TBranch *DiJet2BJet2_dEta;
  TBranch *TriJet1BJet1_dR;
  TBranch *TriJet1BJet1_dEta;
  TBranch *TriJet1BJet1_dPhi;
  TBranch *TriJet1BJet2_dR;
  TBranch *TriJet1BJet2_dEta;
  TBranch *TriJet1BJet2_dPhi;
  TBranch *TriJet2BJet1_dR;
  TBranch *TriJet2BJet1_dEta;
  TBranch *TriJet2BJet1_dPhi;
  TBranch *TriJet2BJet2_dR;
  TBranch *TriJet2BJet2_dEta;
  TBranch *TriJet2BJet2_dPhi;
  TBranch *BJet3_LdgTop_dR;
  TBranch *BJet3_LdgTop_dEta;
  TBranch *BJet3_LdgTop_dPhi;
  TBranch *BJet3_SubLdgTop_dR;
  TBranch *BJet3_SubLdgTop_dEta;
  TBranch *BJet3_SubLdgTop_dPhi;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(HplusHadronic);

HplusHadronic::HplusHadronic(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invmassBins")),
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
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
  h_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "HT"         , ";H_{T}"      , 30, 0.0, 1500.0);
  h_MHT         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MHT"        , ";MHT"        , 30, 0.0,  300.0);
  h_Sphericity  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Sphericity" , ";Sphericity" , 20, 0.0,   1.00);
  h_Aplanarity  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Aplanarity" , ";Aplanarity" , 25, 0.0, 0.5);
  h_Planarity   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Planarity"  , ";Planarity"  , 25, 0.0, 0.5);
  h_DParameter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DParameter" , ";D"          , 20, 0.0, 1.0);
  h_H2          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "H2"         , ";H_{2}"      , 20, 0.0, 1.0);
  h_Circularity = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Circularity", ";Circularity", 20, 0.0, 1.0);
  h_Centrality  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Centrality" , ";Centrality" , 20, 0.0, 1.0);
  h_AlphaT      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AlphaT"     , ";#alpha_{T}" , 20, 0.0, 1.0);

  
  h_METoverSqrtHT  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "METoverSqrtHT" , ";E_{T}^{miss}/#sqrt{H_{T}}"  , 25, 0.0, 0.5);
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
  h_BJets_N = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJets_N" , ";N (b-jets)" , 10, -0.5, +9.5);
  h_BJet1_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_BJet2_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_BJet3_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
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
  h_BJetPair_dPhiAverage = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiAverage" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);
  h_BJetPair_dRAverage   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRAverage" , ";#DeltaR"   , nBinsdR , mindR   , maxdR);
  h_BJetPair_dEtaAverage = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dEtaAverage" , ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_BJetPair_Rbb         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_Rbb"         , ";R_{bb}"        , nBinsdR, mindR, maxdR);
  h_BJetPair_MaxPt_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxPt_Pt"  , ";p_{T} (GeV/c)"       , nBinsPt   , minPt  , maxPt  );
  h_BJetPair_MaxPt_M     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxPt_M"   , ";M (GeV/c^{2})"       , 100       , 0.0 , 1000.0 );
  h_BJetPair_MaxMass_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxMass_Pt"  , ";p_{T} (GeV/c)"     , nBinsPt , minPt  , maxPt  );
  h_BJetPair_MaxMass_M   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_MaxMass_M"   , ";M (GeV/c^{2})"     , 100     ,    0.0 , 1000.0 );
  h_BJetPair_dRMin_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Pt"       , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dRMin_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dR"       , ";#DeltaR"          , nBinsdR  , mindR  , maxdR  );
  h_BJetPair_dRMin_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Mass"     , ";M (GeV/c^{2})"     , nBinsM   , minM   , maxM   );
  h_BJetPair_dRMin_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dEta" ,  ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_BJetPair_dRMin_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_dPhi" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);
  h_BJetPair_dRMin_Rbb  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dRMin_Rbb"   , ";R_{bb}"        , nBinsdR, mindR, maxdR);
  h_BJetPair_dPhiMin_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMin_Pt"      , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dPhiMin_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMin_Mass"     , ";M (GeV/c^{2})"     , nBinsM   , minM   , maxM   );
  h_BJetPair_dPhiMax_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMax_Pt"      , ";p_{T} (GeV/c)"    , nBinsPt  , minPt  , maxPt  );
  h_BJetPair_dPhiMax_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BJetPair_dPhiMax_Mass"     , ";M (GeV/c^{2})"     , nBinsM   , minM   , maxM   );


  // dR of Ldg Jet and dRMin BJet Pair
  h_ldgJet_dRMinBJetPair_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dR" , ";#DeltaR"          , nBinsdR  ,  mindR  , maxdR  );
  h_ldgJet_dRMinBJetPair_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dEta" ,  ";#Delta#eta"        , nBinsdEta, mindEta, maxdEta);
  h_ldgJet_dRMinBJetPair_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "ldgJet_dRMinBJetPair_dPhi" , ";#Delta#phi (rads)" , nBinsdPhi , mindPhi, maxdPhi);
							 
  // dR of untagged Ldg Jet and dRMin BJet Pair                                                           
  h_untaggedLdgJet_dRMinBJetPair_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "untaggedLdgJet_dRMinBJetPair_dR" , ";#DeltaR"  , nBinsdR  ,  mindR  , maxdR  );
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
  h_minDeltaRJetMHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "minDeltaRJetMHT"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);
  h_minDeltaRReversedJetMHT = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "minDeltaRReversedJetMHT"  , ";#DeltaR"  , nBinsdR  , mindR  , maxdR);


  // Average CSV Discriminator for all jets                                                                                               
  h_AvgCSV               =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV"  , ";Average CSV"  , 100  , 0  , 1);    
  h_AvgCSV_PtWeighted    =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtWeighted"  , ";Average CSV (p_{T} weighted)"  , 100  , 0, 1);    
  h_AvgCSV_PtSqrWeighted =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtSqrWeighted"  , ";Average CSV (p_{T}^{2} weighted)"  , 100  , 0, 1);   

  // Average CSV Discriminator for non-bjets                                                                                              
  h_AvgCSV_noBjets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_noBjets"  , ";Average CSV"  , 100  , 0  , 1);
  h_AvgCSV_PtWeighted_noBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "AvgCSV_PtWeighted_noBjets"  , ";Average CSV (p_{T} weighted)" , 100  , 0, 1);
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
  h_top_ChiSqr      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "ChiSqr"   , ";#chi^{2}"     ,    100,  0.0, 100.0);
  h_top_RedChiSqr      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, dir, "RedChiSqr"   , ";#chi^{2}"     ,    100,  0.0, 100.0);

  h_H2_Vs_ChiSqr = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "H2_Vs_ChiSqr" , ";H_{2};#chi^{2}" , 20, 0.0, 1.0,  100,  0.0, 100.0);

  
  // TTree
  tree = new TTree("tree", "TTree");
  weight                    = tree -> Branch("eventWeight", &weight   , "eventWeight/F");
  LdgJet_Pt                 = tree -> Branch("recoJet1_Pt", &LdgJet_Pt, "recoJet1_Pt/F");
  BJetPair_dRMin_M          = tree -> Branch("BJetPair_dRMin_Mass", &BJetPair_dRMin_M, "BJetPair_dRMin_Mass/F");
  Jet5_BJetsFirst_Pt        = tree -> Branch("recoJet5_BJetsFirst_Pt", &Jet5_BJetsFirst_Pt, "recoJet5_BJetsFirst_Pt/F");
  H2                        = tree -> Branch("H2", &H2, "H2/F");
  BJetPair_dRAvg            = tree -> Branch("BJetPair_dRAverage", &BJetPair_dRAvg, "BJetPair_dRAverage/F");
  LdgJet_closestBJetPair_dR = tree -> Branch("ldgJet_dRMinBJetPair_dR", &LdgJet_closestBJetPair_dR, "ldgJet_dRMinBJetPair_dR/F");
  DiJet_noBJets_M           = tree -> Branch("dRMinDiJet_NoBJets_Mass", &DiJet_noBJets_M, "dRMinDiJet_NoBJets_Mass/F");
  HT                        = tree -> Branch("HT", &HT, "HT/F");
  BJetPair_maxPt_M          = tree -> Branch("BJetPair_MaxPt_M", &BJetPair_maxPt_M, "BJetPair_MaxPt_M/F");
  BJetPair_maxMass_M        = tree -> Branch("BJetPair_MaxMass_M ", &BJetPair_maxMass_M , "BJetPair_MaxMass_M/F");
  TriJet_maxPt_M            = tree -> Branch("MaxTriJetPt_Mass", &TriJet_maxPt_M, "MaxTriJetPt_Mass/F");
  Centrality                = tree -> Branch("Centrality", &Centrality, "Centrality/F");

  Jets_N                    = tree -> Branch("Jets_N", &Jets_N, "Jets_N/I");
  BJets_N                   = tree -> Branch("BJets_N", &BJets_N, "BJets_N/I");
  untaggedJets_N            = tree -> Branch("untaggedJets_N", &untaggedJets_N, "untaggedJets_N/I");

  recoJet6_Pt               = tree -> Branch("recoJet6_Pt", &recoJet7_Pt, "recoJet6_Pt/F");
  recoJet7_Pt               = tree -> Branch("recoJet7_Pt", &recoJet7_Pt, "recoJet7_Pt/F");
  recoJet8_Pt               = tree -> Branch("recoJet8_Pt", &recoJet8_Pt, "recoJet8_Pt/F");
 

  Jet6_BJetsFirst_Pt        = tree -> Branch("recoJet6_BJetsFirst_Pt", &Jet6_BJetsFirst_Pt, "recoJet6_BJetsFirst_Pt/F");
  Jet7_BJetsFirst_Pt        = tree -> Branch("recoJet7_BJetsFirst_Pt", &Jet7_BJetsFirst_Pt, "recoJet7_BJetsFirst_Pt/F");

  BJetPair_dPhiMin_Pt       = tree -> Branch("BJetPair_dPhiMin_Pt", &BJetPair_dPhiMin_Pt, "BJetPair_dPhiMin_Pt/F");
  BJetPair_dPhiMin_M        = tree -> Branch("BJetPair_dPhiMin_Mass", &BJetPair_dPhiMin_M, "BJetPair_dPhiMin_Mass/F");
  BJetPair_dPhiMax_Pt       = tree -> Branch("BJetPair_dPhiMax_Pt", &BJetPair_dPhiMax_Pt, "BJetPair_dPhiMax_Pt/F");
  BJetPair_dPhiMax_M        = tree -> Branch("BJetPair_dPhiMax_Mass", &BJetPair_dPhiMax_M, "BJetPair_dPhiMax_Mass/F");


  // Minimum and Maximum phi angle between a jet and (MHT-jet)                                                                            
  minDeltaPhiJetMHT = tree -> Branch("minDeltaPhiJetMHT", &minDeltaPhiJetMHT, "minDeltaPhiJetMHT/F");			
  maxDeltaPhiJetMHT = tree -> Branch("maxDeltaPhiJetMHT", &maxDeltaPhiJetMHT, "maxDeltaPhiJetMHT/F");

  // Minimum Delta R between a jet and (MHT-jet), -(MHT-jet)                                         
  minDeltaRJetMHT         = tree -> Branch("minDeltaRJetMHT", &minDeltaRJetMHT, "minDeltaRJetMHT/F");
  minDeltaRReversedJetMHT = tree -> Branch("minDeltaRReversedJetMHT", &minDeltaRReversedJetMHT, "minDeltaRReversedJetMHT/F"); 

  // Average CSV Discriminator for all jets 
  AvgCSV                   = tree -> Branch("AvgCSV" , &AvgCSV, "AvgCSV/F");
  AvgCSV_PtWeighted        = tree -> Branch("AvgCSV_PtWeighted" , &AvgCSV_PtWeighted, "AvgCSV_PtWeighted/F");
  AvgCSV_PtSqrWeighted     = tree -> Branch("AvgCSV_PtSqrWeighted" , &AvgCSV_PtSqrWeighted, "AvgCSV_PtSqrWeighted/F");

  // Average CSV Discriminator for non-bjets
  AvgCSV_noBjets                = tree -> Branch("AvgCSV_noBjets" , &AvgCSV_noBjets, "AvgCSV_noBjets/F");
  AvgCSV_PtWeighted_noBjets     = tree -> Branch("AvgCSV_PtWeighted_noBjets" , &AvgCSV_PtWeighted_noBjets, "AvgCSV_PtWeighted_noBjets/F");
  AvgCSV_PtSqrWeighted_noBjets  = tree -> Branch("AvgCSV_PtSqrWeighted_noBjets" , &AvgCSV_PtSqrWeighted_noBjets, "AvgCSV_PtSqrWeighted_noBjets/F");


  // Top Reconstruction
  LdgTop_Pt          = tree -> Branch("LdgTop_Pt", &LdgTop_Pt, "LdgTop_Pt/F");
  LdgTop_Eta         = tree -> Branch("LdgTop_Eta", &LdgTop_Eta, "LdgTop_Eta/F");
  LdgTop_Phi         = tree -> Branch("LdgTop_Phi", &LdgTop_Phi, "LdgTop_Phi/F");
  LdgTop_Mass        = tree -> Branch("LdgTop_Mass", &LdgTop_Mass, "LdgTop_Mass/F");

  SubLdgTop_Pt       = tree -> Branch("SubLdgTop_Pt", &SubLdgTop_Pt, "SubLdgTop_Pt/F");
  SubLdgTop_Eta      = tree -> Branch("SubLdgTop_Eta", &SubLdgTop_Eta, "SubLdgTop_Eta/F");
  SubLdgTop_Phi      = tree -> Branch("SubLdgTop_Phi", &SubLdgTop_Phi, "SubLdgTop_Phi/F");
  SubLdgTop_Mass     = tree -> Branch("SubLdgTop_Mass", &SubLdgTop_Mass, "SubLdgTop_Mass/F");

  ChiSqr             = tree -> Branch("ChiSqr", &ChiSqr, "ChiSqr/F");
  RedChiSqr             = tree -> Branch("RedChiSqr", &RedChiSqr, "RedChiSqr/F");

  BJet1BJet2_dR      = tree -> Branch("BJet1BJet2_dR"   , &BJet1BJet2_dR   , "BJet1BJet2_dR/F");
  BJet1BJet2_dPhi    = tree -> Branch("BJet1BJet2_dPhi" , &BJet1BJet2_dPhi , "BJet1BJet2_dPhi/F");
  BJet1BJet2_dEta    = tree -> Branch("BJet1BJet2_dEta" , &BJet1BJet2_dEta , "BJet1BJet2_dEta/F");
  DiJet1BJet1_dR     = tree -> Branch("DiJet1BJet1_dR"  , &DiJet1BJet1_dR  , "DiJet1BJet1_dR/F");
  DiJet1BJet1_dPhi   = tree -> Branch("DiJet1BJet1_dPhi", &DiJet1BJet1_dPhi, "DiJet1BJet1_dPhi/F");
  DiJet1BJet1_dEta   = tree -> Branch("DiJet1BJet1_dEta", &DiJet1BJet1_dEta, "DiJet1BJet1_dEta/F");
  DiJet1BJet2_dR     = tree -> Branch("DiJet1BJet2_dR"  , &DiJet1BJet2_dR  , "DiJet1BJet2_dR/F");
  DiJet1BJet2_dPhi   = tree -> Branch("DiJet1BJet2_dPhi", &DiJet1BJet2_dPhi, "DiJet1BJet2_dPhi/F");
  DiJet1BJet2_dEta   = tree -> Branch("DiJet1BJet2_dEta", &DiJet1BJet2_dEta, "DiJet1BJet2_dEta/F");
  DiJet2BJet1_dR     = tree -> Branch("DiJet2BJet1_dR"  , &DiJet2BJet1_dR  , "DiJet2BJet1_dR/F");
  DiJet2BJet1_dPhi   = tree -> Branch("DiJet2BJet1_dPhi", &DiJet2BJet1_dPhi, "DiJet2BJet1_dPhi/F");
  DiJet2BJet1_dEta   = tree -> Branch("DiJet2BJet1_dEta", &DiJet2BJet1_dEta, "DiJet2BJet1_dEta/F");
  DiJet2BJet2_dR     = tree -> Branch("DiJet2BJet2_dR"  , &DiJet2BJet2_dR  , "DiJet2BJet2_dR/F");
  DiJet2BJet2_dPhi   = tree -> Branch("DiJet2BJet2_dPhi", &DiJet2BJet2_dPhi, "DiJet2BJet2_dPhi/F");
  DiJet2BJet2_dEta   = tree -> Branch("DiJet2BJet2_dEta", &DiJet2BJet2_dEta, "DiJet2BJet2_dEta/F");

  TriJet1BJet1_dR     = tree -> Branch("TriJet1BJet1_dR"   , &TriJet1BJet1_dR   , "TriJet1BJet1_dR/F");
  TriJet1BJet1_dPhi   = tree -> Branch("TriJet1BJet1_dPhi" , &TriJet1BJet1_dPhi , "TriJet1BJet1_dPhi/F");
  TriJet1BJet1_dEta   = tree -> Branch("TriJet1BJet1_dEta" , &TriJet1BJet1_dEta , "TriJet1BJet1_dEta/F");
  TriJet1BJet2_dR     = tree -> Branch("TriJet1BJet2_dR"   , &TriJet1BJet2_dR   , "TriJet1BJet2_dR/F");
  TriJet1BJet2_dPhi   = tree -> Branch("TriJet1BJet2_dPhi" , &TriJet1BJet2_dPhi , "TriJet1BJet2_dPhi/F");
  TriJet1BJet2_dEta   = tree -> Branch("TriJet1BJet2_dEta" , &TriJet1BJet2_dEta , "TriJet1BJet2_dEta/F");
  TriJet2BJet1_dR     = tree -> Branch("TriJet2BJet1_dR"   , &TriJet2BJet1_dR   , "TriJet2BJet1_dR/F");
  TriJet2BJet1_dPhi   = tree -> Branch("TriJet2BJet1_dPhi" , &TriJet2BJet1_dPhi , "TriJet2BJet1_dPhi/F");
  TriJet2BJet1_dEta   = tree -> Branch("TriJet2BJet1_dEta" , &TriJet2BJet1_dEta , "TriJet2BJet1_dEta/F");
  TriJet2BJet2_dR     = tree -> Branch("TriJet2BJet2_dR"   , &TriJet2BJet2_dR   , "TriJet2BJet2_dR/F");
  TriJet2BJet2_dPhi   = tree -> Branch("TriJet2BJet2_dPhi" , &TriJet2BJet2_dPhi , "TriJet2BJet2_dPhi/F");
  TriJet2BJet2_dEta   = tree -> Branch("TriJet2BJet2_dEta" , &TriJet2BJet2_dEta , "TriJet2BJet2_dEta/F");
  BJet3_LdgTop_dR     = tree -> Branch("BJet3_LdgTop_dR"   , &BJet3_LdgTop_dR   , "BJet3_LdgTop_dR/F");
  BJet3_LdgTop_dEta   = tree -> Branch("BJet3_LdgTop_dEta" , &BJet3_LdgTop_dEta , "BJet3_LdgTop_dEta/F");
  BJet3_LdgTop_dPhi   = tree -> Branch("BJet3_LdgTop_dPhi" , &BJet3_LdgTop_dPhi , "BJet3_LdgTop_dPhi/F");
  BJet3_SubLdgTop_dR  = tree -> Branch("BJet3_SubLdgTop_dR"  , &BJet3_SubLdgTop_dR  , "BJet3_SubLdgTop_dR/F");
  BJet3_SubLdgTop_dEta= tree -> Branch("BJet3_SubLdgTop_dEta", &BJet3_SubLdgTop_dEta, "BJet3_SubLdgTop_dEta/F");
  BJet3_SubLdgTop_dPhi= tree -> Branch("BJet3_SubLdgTop_dPhi", &BJet3_SubLdgTop_dPhi, "BJet3_SubLdgTop_dPhi/F");

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
  float ldgJet_Pt, bJetPair_dRMin_M, jet5_bJetsFirst_Pt, h2, bJetPair_dRAvg, ldgJet_closestBJetPair_dR;
  float jet7_bJetsFirst_Pt,jet6_bJetsFirst_Pt, bJetPair_dPhiMin_M, bJetPair_dPhiMin_Pt,bJetPair_dPhiMax_M, bJetPair_dPhiMax_Pt;
  float dRMinDiJet_noBJets_M, ht, bJetPair_maxPt_M, bJetPair_maxMass_M, triJet_maxPt_M, centrality ;
  float recoJet6_pt, recoJet7_pt, recoJet8_pt;
  int jets_N, bjets_N, untaggedjets_N;
  float MinDeltaPhiJetMHT, MaxDeltaPhiJetMHT,MinDeltaRJetMHT, MinDeltaRReversedJetMHT;
  float avgCSV, avgCSV_PtWeighted, avgCSV_PtSqrWeighted, avgCSV_noBjets, avgCSV_PtWeighted_noBjets, avgCSV_PtSqrWeighted_noBjets;
  float ldgTop_Pt, ldgTop_Eta, ldgTop_Phi, ldgTop_Mass, subldgTop_Pt, subldgTop_Eta, subldgTop_Phi, subldgTop_Mass;
  float chiSqr, redChiSqr, bJet1bJet2_dR,bJet1bJet2_dPhi, bJet1bJet2_dEta;
  float diJet1bJet1_dR, diJet1bJet1_dEta, diJet1bJet1_dPhi, diJet1bJet2_dR, diJet1bJet2_dEta, diJet1bJet2_dPhi;
  float diJet2bJet1_dR, diJet2bJet1_dEta, diJet2bJet1_dPhi, diJet2bJet2_dR, diJet2bJet2_dEta, diJet2bJet2_dPhi;
  float triJet1bJet1_dR, triJet1bJet1_dEta, triJet1bJet1_dPhi, triJet1bJet2_dR, triJet1bJet2_dEta, triJet1bJet2_dPhi;
  float triJet2bJet1_dR, triJet2bJet1_dEta, triJet2bJet1_dPhi, triJet2bJet2_dR, triJet2bJet2_dEta, triJet2bJet2_dPhi;
  float bJet3_ldgTop_dR, bJet3_ldgTop_dEta, bJet3_ldgTop_dPhi, bJet3_subldgTop_dR, bJet3_subldgTop_dEta, bJet3_subldgTop_dPhi;
  
  // ATLAS BDT
  weight                    -> SetAddress(&eventWeight);
  LdgJet_Pt                 -> SetAddress(&ldgJet_Pt);
  BJetPair_dRMin_M          -> SetAddress(&bJetPair_dRMin_M);
  Jet5_BJetsFirst_Pt        -> SetAddress(&jet5_bJetsFirst_Pt);
  H2                        -> SetAddress(&h2);
  BJetPair_dRAvg            -> SetAddress(&bJetPair_dRAvg);
  LdgJet_closestBJetPair_dR -> SetAddress(&ldgJet_closestBJetPair_dR);
  DiJet_noBJets_M           -> SetAddress(&dRMinDiJet_noBJets_M);
  HT                        -> SetAddress(&ht);
  BJetPair_maxPt_M          -> SetAddress(&bJetPair_maxPt_M);
  BJetPair_maxMass_M        -> SetAddress(&bJetPair_maxMass_M);
  TriJet_maxPt_M            -> SetAddress(&triJet_maxPt_M);
  Centrality                -> SetAddress(&centrality);

  Jets_N                    -> SetAddress(&jets_N);
  BJets_N                   -> SetAddress(&bjets_N);
  untaggedJets_N            -> SetAddress(&untaggedjets_N);

  recoJet6_Pt               -> SetAddress(&recoJet6_pt);
  recoJet7_Pt               -> SetAddress(&recoJet7_pt);
  recoJet8_Pt               -> SetAddress(&recoJet8_pt);

  Jet6_BJetsFirst_Pt        -> SetAddress(&jet6_bJetsFirst_Pt);
  Jet7_BJetsFirst_Pt        -> SetAddress(&jet7_bJetsFirst_Pt);

  BJetPair_dPhiMin_Pt       -> SetAddress(&bJetPair_dPhiMin_Pt);
  BJetPair_dPhiMin_M        -> SetAddress(&bJetPair_dPhiMin_M);
  BJetPair_dPhiMax_Pt       -> SetAddress(&bJetPair_dPhiMax_Pt);
  BJetPair_dPhiMax_M        -> SetAddress(&bJetPair_dPhiMax_M);


  minDeltaPhiJetMHT -> SetAddress(&MinDeltaPhiJetMHT);
  maxDeltaPhiJetMHT -> SetAddress(&MaxDeltaPhiJetMHT);

  minDeltaRJetMHT         -> SetAddress(&MinDeltaRJetMHT);
  minDeltaRReversedJetMHT -> SetAddress(&MinDeltaRReversedJetMHT);

  AvgCSV                  -> SetAddress(&avgCSV);
  AvgCSV_PtWeighted       -> SetAddress(&avgCSV_PtWeighted);
  AvgCSV_PtSqrWeighted    -> SetAddress(&avgCSV_PtSqrWeighted);

  AvgCSV_noBjets                -> SetAddress(&avgCSV_noBjets);
  AvgCSV_PtWeighted_noBjets     -> SetAddress(&avgCSV_PtWeighted_noBjets);
  AvgCSV_PtSqrWeighted_noBjets  -> SetAddress(&avgCSV_PtSqrWeighted_noBjets);

  
  // Top Reconstruction
  LdgTop_Pt          -> SetAddress(&ldgTop_Pt);
  LdgTop_Eta         -> SetAddress(&ldgTop_Eta);
  LdgTop_Phi         -> SetAddress(&ldgTop_Phi);
  LdgTop_Mass        -> SetAddress(&ldgTop_Mass);

  SubLdgTop_Pt          -> SetAddress(&subldgTop_Pt);
  SubLdgTop_Eta         -> SetAddress(&subldgTop_Eta);
  SubLdgTop_Phi         -> SetAddress(&subldgTop_Phi);
  SubLdgTop_Mass        -> SetAddress(&subldgTop_Mass);

  ChiSqr             -> SetAddress(&chiSqr);
  RedChiSqr             -> SetAddress(&redChiSqr);

  BJet1BJet2_dR      -> SetAddress(&bJet1bJet2_dR);
  BJet1BJet2_dPhi    -> SetAddress(&bJet1bJet2_dPhi);
  BJet1BJet2_dEta    -> SetAddress(&bJet1bJet2_dEta);
  DiJet1BJet1_dR     -> SetAddress(&diJet1bJet1_dR);
  DiJet1BJet1_dPhi   -> SetAddress(&diJet1bJet1_dPhi);
  DiJet1BJet1_dEta   -> SetAddress(&diJet1bJet1_dEta);
  DiJet1BJet2_dR     -> SetAddress(&diJet1bJet2_dR);
  DiJet1BJet2_dPhi   -> SetAddress(&diJet1bJet2_dPhi);
  DiJet1BJet2_dEta   -> SetAddress(&diJet1bJet2_dEta);
  DiJet2BJet1_dR     -> SetAddress(&diJet2bJet1_dR);
  DiJet2BJet1_dPhi   -> SetAddress(&diJet2bJet1_dPhi);
  DiJet2BJet1_dEta   -> SetAddress(&diJet2bJet1_dEta);
  DiJet2BJet2_dR     -> SetAddress(&diJet2bJet2_dR);
  DiJet2BJet2_dPhi   -> SetAddress(&diJet2bJet2_dPhi);
  DiJet2BJet2_dEta   -> SetAddress(&diJet2bJet2_dEta);

  TriJet1BJet1_dR    -> SetAddress(&triJet1bJet1_dR);
  TriJet1BJet1_dPhi  -> SetAddress(&triJet1bJet1_dPhi);
  TriJet1BJet1_dEta  -> SetAddress(&triJet1bJet1_dEta);
  TriJet1BJet2_dR    -> SetAddress(&triJet1bJet2_dR);
  TriJet1BJet2_dPhi  -> SetAddress(&triJet1bJet2_dPhi);
  TriJet1BJet2_dEta  -> SetAddress(&triJet1bJet2_dEta);
  TriJet2BJet1_dR    -> SetAddress(&triJet2bJet1_dR);
  TriJet2BJet1_dPhi  -> SetAddress(&triJet2bJet1_dPhi);
  TriJet2BJet1_dEta  -> SetAddress(&triJet2bJet1_dEta);
  TriJet2BJet2_dR    -> SetAddress(&triJet2bJet2_dR);
  TriJet2BJet2_dPhi  -> SetAddress(&triJet2bJet2_dPhi);
  TriJet2BJet2_dEta  -> SetAddress(&triJet2bJet2_dEta);

  BJet3_LdgTop_dR      -> SetAddress(&bJet3_ldgTop_dR);
  BJet3_LdgTop_dEta    -> SetAddress(&bJet3_ldgTop_dEta);
  BJet3_LdgTop_dPhi    -> SetAddress(&bJet3_ldgTop_dPhi);
  BJet3_SubLdgTop_dR   -> SetAddress(&bJet3_subldgTop_dR);
  BJet3_SubLdgTop_dEta -> SetAddress(&bJet3_subldgTop_dEta);
  BJet3_SubLdgTop_dPhi -> SetAddress(&bJet3_subldgTop_dPhi);


  // TTree Variables (Event-Weight)
  eventWeight = fEventWeight.getWeight();


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
  ht = TopologyData.HT();
  h2 = TopologyData.FoxWolframMoment();
  centrality = TopologyData.Centrality();


  h_H2_Vs_ChiSqr -> Fill ( TopologyData.FoxWolframMoment(), TopData.ChiSqr() );

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

  // TTree variables
  avgCSV               = CSV_sum / N_jets;
  avgCSV_PtWeighted    = CSV_PtWeighted_sum / Pt_sum ;
  avgCSV_PtSqrWeighted = CSV_PtSqrWeighted_sum /  PtSqr_sum ;


  //=======================================================
  // Selected Jets
  //=======================================================


  //=== Pt & Abs(Eta) of the first 6 Jets

  double jet_Pt, jet_Eta;
  math::XYZTLorentzVector ldgJet_p4(0,0,0,0);
  
  // For-Loop: Selected Jets
  for (size_t i=0; i < jetData.getSelectedJets().size(); i++ )
    {
      // Get the Pt and Eta of the Selected Jets
      jet_Pt  = jetData.getSelectedJets().at(i).pt();
      jet_Eta = jetData.getSelectedJets().at(i).eta();

      // Get the p4 of the leading jet
      if (i == 0) {
	ldgJet_p4 = jetData.getSelectedJets().at(i).p4();
      }

      // Fill histos with Pt and abs(Eta) for the first 6 jets
      if ( i<6 ) {
	  vh_recoJets_Pt.at(i)     -> Fill ( jet_Pt        );
	  vh_recoJets_AbsEta.at(i) -> Fill ( std::abs(jet_Eta) );
	  
	  //TTree variable
	  if (i==5) recoJet6_pt     =jet_Pt;
      }
      
      // 7th, 8th jet Pt
      else if (i==6) {
	// Fill histo
	h_recoJet7_Pt    -> Fill(jet_Pt);
	// TTree variable
	recoJet7_pt     =jet_Pt;
      }
      else if (i==7) {
        // Fill histo                                                         
        h_recoJet8_Pt    -> Fill(jet_Pt);
        // TTree variable                                                                   
        recoJet8_pt    =jet_Pt;
      }

      
    } // For-loop: Selected Jets

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
  h_minDeltaRJetMHT -> Fill ( jetData.minDeltaRJetMHT());
  h_minDeltaRReversedJetMHT -> Fill ( jetData.minDeltaRReversedJetMHT());

  // TTree Variables 
  ldgJet_Pt = ldgJet_p4.pt(); 
  jets_N    = jetData.getNumberOfSelectedJets();
  bjets_N   = bjetData.getNumberOfSelectedBJets();
  untaggedjets_N = jets_N - bjets_N;
  //
  MinDeltaPhiJetMHT = jetData.minDeltaPhiJetMHT();
  MaxDeltaPhiJetMHT = jetData.maxDeltaPhiJetMHT();
  //
  MinDeltaRJetMHT = jetData.minDeltaRJetMHT();
  MinDeltaRReversedJetMHT = jetData.minDeltaRReversedJetMHT();

  //=======================================================                                                        
  // Di-Jet                                                                                                            
  //=======================================================  

  //=== B-Tagged Di-Jet  (Average dR, dPhi, dEta, MaxMass Di-Jet, MaxPt Di-Jet, dRMin Di-Jet)

  // Initialize values                                                                                                           
  int nBPairs = 0;
  double dR   = 0.0;
  double dEta = 0.0;
  double dPhi = 0.0;
  double dRSum   = 0.0;
  double dEtaSum = 0.0;
  double dPhiSum = 0.0;
  double deltaRMin = 999999.9;
  double deltaPhiMin = 999999.9;
  double deltaPhiMax = 0 ;
  int deltaRMin_i  = -1;
  int deltaRMin_j  = -1;
  
  math::XYZTLorentzVector maxPt_p4(0,0,0,0);
  math::XYZTLorentzVector maxMass_p4(0,0,0,0);
  //double maxPt_dEta = 0.0;
  //double maxPt_dPhi = 0.0;
  //double maxPt_dR   = 0.0;
  //double maxMass_dEta = 0.0;
  //double maxMass_dPhi = 0.0;
  //double maxMass_dR   = 0.0;

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
      if ( pair_p4.Pt() > maxPt_p4.Pt() )
	{
	  maxPt_p4   = pair_p4;
	  //maxPt_dEta = dEta;
	  //maxPt_dPhi = dPhi;
	  //maxPt_dR   = dR;
	}
      
      // Find the maxMass BJetPair
      if ( pair_p4.M() > maxMass_p4.M() )
	{
	  maxMass_p4   = pair_p4;
	  //maxMass_dEta = dEta;
	  //maxMass_dPhi = dPhi;
	  //maxMass_dR   = dR;
	}
      
      // Find the dPhiMin BJetPair
      if (dPhi < deltaPhiMin)
	{
	  bJetPair_dPhiMin_p4 = pair_p4;
	}

      // Find the dPhiMax BJetPair                                                                                                        
      if (dPhi > deltaPhiMax)
        {
          bJetPair_dPhiMax_p4 =pair_p4;
        }

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
  h_BJetPair_dRAverage   -> Fill ( dRSum/nBPairs   );
  h_BJetPair_dEtaAverage -> Fill ( dEtaSum/nBPairs );
  h_BJetPair_dPhiAverage -> Fill ( dPhiSum/nBPairs );
  //
  h_BJetPair_Rbb   -> Fill ( std::sqrt( ((3.14159265359-(dPhiSum/nBPairs))*(3.14159265359-(dPhiSum/nBPairs))) + ((dEtaSum/nBPairs)*(dEtaSum/nBPairs))));
  //                                                       
  h_BJetPair_MaxPt_Pt    -> Fill ( maxPt_p4.Pt()   );
  h_BJetPair_MaxPt_M     -> Fill ( maxPt_p4.M()    );
  //
  h_BJetPair_MaxMass_Pt  -> Fill ( maxMass_p4.Pt() );
  h_BJetPair_MaxMass_M   -> Fill ( maxMass_p4.M()  );
  //
  h_BJetPair_dPhiMin_Pt   -> Fill( bJetPair_dPhiMin_p4.pt() );
  h_BJetPair_dPhiMin_Mass -> Fill( bJetPair_dPhiMin_p4.mass() );
  //
  h_BJetPair_dPhiMax_Pt   -> Fill( bJetPair_dPhiMax_p4.pt() );
  h_BJetPair_dPhiMax_Mass -> Fill( bJetPair_dPhiMax_p4.mass() );


  // TTree Variables 
  bJetPair_dRAvg     = dRSum/nBPairs;
  bJetPair_maxPt_M   = maxPt_p4.M();
  bJetPair_maxMass_M = maxMass_p4.M();
  bJetPair_dPhiMin_Pt   = bJetPair_dPhiMin_p4.pt();
  bJetPair_dPhiMin_M   = bJetPair_dPhiMin_p4.mass();
  bJetPair_dPhiMax_Pt   = bJetPair_dPhiMax_p4.pt();
  bJetPair_dPhiMax_M   = bJetPair_dPhiMax_p4.mass();


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
      h_ldgJet_dRMinBJetPair_dR  -> Fill ( ROOT::Math::VectorUtil::DeltaR( ldgJet_p4, bJetPair_dRMin_p4) );
      h_ldgJet_dRMinBJetPair_dPhi  -> Fill ( ROOT::Math::VectorUtil::DeltaPhi( ldgJet_p4, bJetPair_dRMin_p4) );
      h_ldgJet_dRMinBJetPair_dEta  -> Fill ( std::abs(ldgJet_p4.eta() - bJetPair_dRMin_p4.eta()) );

      // TTree Variables
      //ldgJet_Pt                 = ldgJet_p4.pt();
      ldgJet_closestBJetPair_dR = ROOT::Math::VectorUtil::DeltaR( ldgJet_p4, bJetPair_dRMin_p4);
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
  
  
  if ( (selBJets_p4.size()>0) && (selNoBJets_p4.size()>0)){
      // Insert all: Selected BJets (pT ordered) in the begining (ATLAS style)                                                  
      selJets_BJetsFirst_p4 = selBJets_p4;
      selJets_BJetsFirst_p4.insert(selJets_BJetsFirst_p4.end(), selNoBJets_p4.begin(), selNoBJets_p4.end());
      
      if (selJets_BJetsFirst_p4.size()>=5){
	// Fill histo 
	h_recoJet5_BJetsFirst_Pt -> Fill ( selJets_BJetsFirst_p4.at(4).Pt()  );
	// TTree Variables                                                                                         
        jet5_bJetsFirst_Pt = selJets_BJetsFirst_p4.at(4).Pt();
      }
      if (selJets_BJetsFirst_p4.size()>=6){
	// Fill histo 
	h_recoJet6_BJetsFirst_Pt -> Fill ( selJets_BJetsFirst_p4.at(5).Pt()  );
	// TTree Variables                                                                                                               
	jet6_bJetsFirst_Pt = selJets_BJetsFirst_p4.at(5).Pt();
      }
      if (selJets_BJetsFirst_p4.size()>=7){
	// Fill histo 
	h_recoJet7_BJetsFirst_Pt -> Fill ( selJets_BJetsFirst_p4.at(6).Pt()  );
	// TTree Variables
	jet7_bJetsFirst_Pt = selJets_BJetsFirst_p4.at(6).Pt();
      }
      

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
	  dRMinDiJet_noBJets_M =dRMinDiJet_NoBJets_p4.M();
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
  
  // TTree variables
  avgCSV_noBjets               = CSV_sum / N_jets;
  avgCSV_PtWeighted_noBjets    = CSV_PtWeighted_sum / Pt_sum ;
  avgCSV_PtSqrWeighted_noBjets = CSV_PtSqrWeighted_sum /  PtSqr_sum ;
  
  
  
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

  /*
  // ============================================================================                                                      

  //=== Top Reconstruction - Ldg & SubLdg Top 
  h_LdgTop_Pt        ->    Fill(TopData.getLdgTrijet().Pt());
  h_LdgTop_Eta       ->    Fill(TopData.getLdgTrijet().Eta());
  h_LdgTop_Phi       ->    Fill(TopData.getLdgTrijet().Phi());
  h_LdgTop_Mass      ->    Fill(TopData.getLdgTrijet().M());

  h_SubLdgTop_Pt     ->    Fill(TopData.getSubldgTrijet().Pt());
  h_SubLdgTop_Eta    ->    Fill(TopData.getSubldgTrijet().Eta());
  h_SubLdgTop_Phi    ->    Fill(TopData.getSubldgTrijet().Phi());
  h_SubLdgTop_Mass   ->    Fill(TopData.getSubldgTrijet().M());


  //=== Top Reconstruction - (BJet1 - Bjet2) Distances                                                                
  h_BJet1BJet2_dR    ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1BJet().p4(), TopData.getTrijet2BJet().p4()));
  h_BJet1BJet2_dPhi  ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1BJet().p4(), TopData.getTrijet2BJet().p4()));
  h_BJet1BJet2_dEta  ->    Fill(std::abs(TopData.getTrijet1BJet().p4().eta() - TopData.getTrijet2BJet().p4().eta()));


  //=== Top Reconstruction - (Di-Jet - Bjet) Distances
  h_DiJet1BJet1_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1DijetP4(), TopData.getTrijet1BJet().p4()));
  h_DiJet1BJet2_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1DijetP4(), TopData.getTrijet2BJet().p4()));
  h_DiJet2BJet1_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet2DijetP4(), TopData.getTrijet1BJet().p4()));
  h_DiJet2BJet2_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet2DijetP4(), TopData.getTrijet2BJet().p4()));
  h_DiJet1BJet1_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1DijetP4(), TopData.getTrijet1BJet().p4()));   
  h_DiJet1BJet2_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1DijetP4(), TopData.getTrijet2BJet().p4()));
  h_DiJet2BJet1_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet2DijetP4(), TopData.getTrijet1BJet().p4()));
  h_DiJet2BJet2_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet2DijetP4(), TopData.getTrijet2BJet().p4()));
  h_DiJet1BJet1_dEta   ->    Fill(std::abs(TopData.getTrijet1DijetP4().eta() - TopData.getTrijet1BJet().p4().eta()));
  h_DiJet1BJet2_dEta   ->    Fill(std::abs(TopData.getTrijet1DijetP4().eta() - TopData.getTrijet2BJet().p4().eta()));
  h_DiJet2BJet1_dEta   ->    Fill(std::abs(TopData.getTrijet2DijetP4().eta() - TopData.getTrijet1BJet().p4().eta()));
  h_DiJet2BJet2_dEta   ->    Fill(std::abs(TopData.getTrijet2DijetP4().eta() - TopData.getTrijet2BJet().p4().eta()));

  //=== Top Reconstruction - (Tri-Jet - Bjet) Distances                                                               
  h_TriJet1BJet1_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getLdgTrijet(), TopData.getTrijet1BJet().p4()));
  h_TriJet1BJet2_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getLdgTrijet(), TopData.getTrijet2BJet().p4()));
  h_TriJet2BJet1_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getSubldgTrijet(), TopData.getTrijet1BJet().p4()));
  h_TriJet2BJet2_dR     ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.getSubldgTrijet(), TopData.getTrijet2BJet().p4()));
  h_TriJet1BJet1_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(), TopData.getTrijet1BJet().p4()));
  h_TriJet1BJet2_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(), TopData.getTrijet2BJet().p4()));
  h_TriJet2BJet1_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getSubldgTrijet(), TopData.getTrijet1BJet().p4()));
  h_TriJet2BJet2_dPhi   ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.getSubldgTrijet(), TopData.getTrijet2BJet().p4()));
  h_TriJet1BJet1_dEta   ->    Fill(std::abs(TopData.getLdgTrijet().eta() - TopData.getTrijet1BJet().p4().eta()));
  h_TriJet1BJet2_dEta   ->    Fill(std::abs(TopData.getLdgTrijet().eta() - TopData.getTrijet2BJet().p4().eta()));
  h_TriJet2BJet1_dEta   ->    Fill(std::abs(TopData.getSubldgTrijet().eta() - TopData.getTrijet1BJet().p4().eta()));
  h_TriJet2BJet2_dEta   ->    Fill(std::abs(TopData.getSubldgTrijet().eta() - TopData.getTrijet2BJet().p4().eta()));
  *///marina
  /*
  //=== Top Reconstruction - (BJet3 - Top) Distances
  h_BJet3_LdgTop_dR       ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.BJet3P4(), TopData.getLdgTrijet() ));
  h_BJet3_LdgTop_dEta     ->    Fill(std::abs(TopData.BJet3P4().eta() - TopData.getLdgTrijet().eta()));
  h_BJet3_LdgTop_dPhi     ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.BJet3P4(), TopData.getLdgTrijet() ));
  h_BJet3_SubLdgTop_dR    ->    Fill(ROOT::Math::VectorUtil::DeltaR(TopData.BJet3P4(), TopData.getSubldgTrijet() ));
  h_BJet3_SubLdgTop_dEta  ->    Fill(std::abs(TopData.BJet3P4().eta() - TopData.getSubldgTrijet().eta()));
  h_BJet3_SubLdgTop_dPhi  ->    Fill(ROOT::Math::VectorUtil::DeltaPhi(TopData.BJet3P4(), TopData.getSubldgTrijet() ));
  */

 
  //=== Top Reconstruction - chi^2
  h_top_ChiSqr            ->    Fill(TopData.ChiSqr());
  //h_top_RedChiSqr         ->    Fill((TopData.ChiSqr())/3);  

  /* marina 
  // TTree Variables
  ldgTop_Pt        =    TopData.getLdgTrijet().Pt();
  ldgTop_Eta       =    TopData.getLdgTrijet().Eta();
  ldgTop_Phi       =    TopData.getLdgTrijet().Phi();
  ldgTop_Mass      =    TopData.getLdgTrijet().M();

  subldgTop_Pt     =    TopData.getSubldgTrijet().Pt();
  subldgTop_Eta    =    TopData.getSubldgTrijet().Eta();
  subldgTop_Phi    =    TopData.getSubldgTrijet().Phi();
  subldgTop_Mass   =    TopData.getSubldgTrijet().M();


  chiSqr    = TopData.ChiSqr();
  redChiSqr = chiSqr/3;

  bJet1bJet2_dR         = ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1BJet().p4(), TopData.getTrijet2BJet().p4());
  bJet1bJet2_dPhi       = ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1BJet().p4(), TopData.getTrijet2BJet().p4());
  bJet1bJet2_dEta       = std::abs(TopData.getTrijet1BJet().p4().eta() - TopData.getTrijet2BJet().p4().eta());

  diJet1bJet1_dR        = ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1DijetP4(), TopData.getTrijet1BJet().p4());
  diJet1bJet1_dEta      = std::abs(TopData.getTrijet1DijetP4().eta() - TopData.getTrijet1BJet().p4().eta());
  diJet1bJet1_dPhi      = ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1DijetP4(), TopData.getTrijet1BJet().p4());
  diJet1bJet2_dR        = ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet1DijetP4(), TopData.getTrijet2BJet().p4());
  diJet1bJet2_dEta      = std::abs(TopData.getTrijet1DijetP4().eta() - TopData.getTrijet2BJet().p4().eta());
  diJet1bJet2_dPhi      = ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet1DijetP4(), TopData.getTrijet2BJet().p4());
  diJet2bJet1_dR        = ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet2DijetP4(), TopData.getTrijet1BJet().p4());
  diJet2bJet1_dEta      = std::abs(TopData.getTrijet2DijetP4().eta() - TopData.getTrijet1BJet().p4().eta());
  diJet2bJet1_dPhi      = ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet2DijetP4(), TopData.getTrijet1BJet().p4());
  diJet2bJet2_dR        = ROOT::Math::VectorUtil::DeltaR(TopData.getTrijet2DijetP4(), TopData.getTrijet2BJet().p4());
  diJet2bJet2_dEta      = std::abs(TopData.getTrijet2DijetP4().eta() - TopData.getTrijet2BJet().p4().eta());
  diJet2bJet2_dPhi      = ROOT::Math::VectorUtil::DeltaPhi(TopData.getTrijet2DijetP4(), TopData.getTrijet2BJet().p4());

  triJet1bJet1_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgTrijet(), TopData.getTrijet1BJet().p4());
  triJet1bJet1_dEta     = std::abs(TopData.getLdgTrijet().eta() - TopData.getTrijet1BJet().p4().eta());
  triJet1bJet1_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(), TopData.getTrijet1BJet().p4());
  triJet1bJet2_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.getLdgTrijet(), TopData.getTrijet2BJet().p4());
  triJet1bJet2_dEta     = std::abs(TopData.getLdgTrijet().eta() - TopData.getTrijet2BJet().p4().eta());
  triJet1bJet2_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.getLdgTrijet(), TopData.getTrijet2BJet().p4());
  triJet2bJet1_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.getSubldgTrijet(), TopData.getTrijet1BJet().p4());
  triJet2bJet1_dEta     = std::abs(TopData.getSubldgTrijet().eta() - TopData.getTrijet1BJet().p4().eta());
  triJet2bJet1_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.getSubldgTrijet(), TopData.getTrijet1BJet().p4());
  triJet2bJet2_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.getSubldgTrijet(), TopData.getTrijet2BJet().p4());
  triJet2bJet2_dEta     = std::abs(TopData.getSubldgTrijet().eta() - TopData.getTrijet2BJet().p4().eta());
  triJet2bJet2_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.getSubldgTrijet(), TopData.getTrijet2BJet().p4());
  */ //marina
  /*
  bJet3_ldgTop_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.BJet3P4(), TopData.getLdgTrijet());
  bJet3_ldgTop_dEta     = std::abs(TopData.BJet3P4().eta() - TopData.getLdgTrijet().eta());
  bJet3_ldgTop_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.BJet3P4(), TopData.getLdgTrijet());
  bJet3_subldgTop_dR       = ROOT::Math::VectorUtil::DeltaR(TopData.BJet3P4(), TopData.getSubldgTrijet());
  bJet3_subldgTop_dEta     = std::abs(TopData.BJet3P4().eta() - TopData.getSubldgTrijet().eta());
  bJet3_subldgTop_dPhi     = ROOT::Math::VectorUtil::DeltaPhi(TopData.BJet3P4(), TopData.getSubldgTrijet());
  */
  
  //================================================================================================                 
  // Fill TTree                                                                                                                
  //================================================================================================  
  tree -> Fill();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, true);
  
  
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();
  }
  
  
  
