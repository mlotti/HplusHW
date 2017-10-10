// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/BJetSelection.h"
#include "Tools/interface/MCTools.h"
#include "Auxiliary/interface/Tools.h"
#include "Auxiliary/interface/Table.h"
#include "Tools/interface/DirectionalCut.h"

#include "EventSelection/interface/TrijetSelection.h"   //Soti


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

class TopReco: public BaseSelector {
public:
  explicit TopReco(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TopReco() {}


  std::vector<int> SortInPt(std::vector<int> Vector);
  //Vector sorting according to the pt. - Descending order
  std::vector<math::XYZTLorentzVector> SortInPt(std::vector<math::XYZTLorentzVector> Vector);
  //returns the last copy of a gen particle
  genParticle findLastCopy(int index);
  //is Bjet
  bool isBJet(const Jet& jet, const std::vector<Jet>& bjets);
  ///Are same Jets
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  bool areMatchedJets(math::XYZTLorentzVector jet1, math::XYZTLorentzVector jet2);
  /// Books histograms
  virtual void book(TDirectory *dir ) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;


  //Soti-Marina
  const genParticle GetLastCopy(const vector<genParticle> genParticles, const genParticle &p);
  vector<genParticle> GetGenParticles(const vector<genParticle> genParticles, const int pdgId);


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
  Count              cAllEvents;
  Count              cTrigger;
  METFilterSelection fMETFilterSelection;
  Count              cVertexSelection;
  ElectronSelection  fElectronSelection;
  MuonSelection      fMuonSelection;
  TauSelection       fTauSelection;
  JetSelection       fJetSelection;
  BJetSelection      fBJetSelection;
  Count              cBTaggingSFCounter;
  METSelection       fMETSelection;
  TopologySelection  fTopologySelection;
  TopSelection       fTopSelection;
  Count              cSelected;
    

  WrappedTH1Triplet *hTrijetPt;
  WrappedTH1Triplet *hTrijetEta;
  WrappedTH1Triplet *hTrijetPhi;
  WrappedTH1Triplet *hTrijetMass;
  WrappedTH1Triplet *hTrijetPtDr;
  WrappedTH1Triplet *hDijetPtDr;
  WrappedTH1Triplet *hDijetMass;
  WrappedTH1Triplet *hLdgJetBdisc;
  WrappedTH1Triplet *hSubldgJetBdisc;
  WrappedTH1Triplet *hBJetBdisc;
  WrappedTH1Triplet *hBJetMass;
  WrappedTH1Triplet *hBJetLdgJet_Mass;
  WrappedTH1Triplet *hBJetSubldgJet_Mass;
  WrappedTH1Triplet *hSoftDrop_n2;
  WrappedTH1 *hNmatchedTop;
  WrappedTH1 *hNmatchedTrijets;
  WrappedTH1Triplet *hGenTop_Pt;


  WrappedTH1Triplet *hTrijetDrMin;
  WrappedTH1Triplet *hTrijetDPtOverGenPt;
  WrappedTH1Triplet *hTrijetDEtaOverGenEta;
  WrappedTH1Triplet *hTrijetDPhiOverGenPhi;

  WrappedTH1Triplet *hTrijetDPt_matched;
  WrappedTH1Triplet *hTrijetDEta_matched;
  WrappedTH1Triplet *hTrijetDPhi_matched;
  
  //Correlations
  WrappedTH2Triplet *hTrijetPtDr_TrijetMass;
  WrappedTH2Triplet *hTrijetPtDr_BjetLdgJetMass;
  WrappedTH2Triplet *hDijetPtDr_DijetMass;
  WrappedTH2Triplet *hDijetPtDr_TrijetMass;
  WrappedTH2Triplet *hTrijetMass_BjetLdgJetMass;
  WrappedTH2Triplet *hTrijetMass_BjetSubldgJetMass;
  WrappedTH2Triplet *hTrijetMass_DijetMass;


  //next WrappedTH1Triplet

  // TTree - TBranches       
  TTree *treeS;
  TTree *treeB;
  TTree *tree;
  //TBranch
  //Variables from Analysis Note AN-16-437
  TBranch *weight_S;
  TBranch *TrijetPtDR_S;
  TBranch *TrijetDijetPtDR_S;
  TBranch *TrijetBjetMass_S;
  TBranch *TrijetLdgJetPt_S;
  TBranch *TrijetLdgJetEta_S;
  TBranch *TrijetLdgJetBDisc_S;
  TBranch *TrijetSubldgJetPt_S;
  TBranch *TrijetSubldgJetEta_S;
  TBranch *TrijetSubldgJetBDisc_S;
  TBranch *TrijetBJetLdgJetMass_S;
  TBranch *TrijetBJetSubldgJetMass_S;
  TBranch *TrijetDijetMass_S;
  TBranch *TrijetBJetBDisc_S;
  TBranch *TrijetMass_S;
  TBranch *TrijetSoftDrop_n2_S;

  TBranch *weight_B;
  TBranch *TrijetPtDR_B;
  TBranch *TrijetDijetPtDR_B;
  TBranch *TrijetBjetMass_B;
  TBranch *TrijetLdgJetPt_B;
  TBranch *TrijetLdgJetEta_B;
  TBranch *TrijetLdgJetBDisc_B;
  TBranch *TrijetSubldgJetPt_B;
  TBranch *TrijetSubldgJetEta_B;
  TBranch *TrijetSubldgJetBDisc_B;
  TBranch *TrijetBJetLdgJetMass_B;
  TBranch *TrijetBJetSubldgJetMass_B;
  TBranch *TrijetDijetMass_B;
  TBranch *TrijetBJetBDisc_B;
  TBranch *TrijetMass_B;
  TBranch *TrijetSoftDrop_n2_B;

  TBranch *weight_test;
  TBranch *TrijetPtDR_test;
  TBranch *TrijetDijetPtDR_test;
  TBranch *TrijetBjetMass_test;
  TBranch *TrijetLdgJetPt_test;
  TBranch *TrijetLdgJetEta_test;
  TBranch *TrijetLdgJetBDisc_test;
  TBranch *TrijetSubldgJetPt_test;
  TBranch *TrijetSubldgJetEta_test;
  TBranch *TrijetSubldgJetBDisc_test;
  TBranch *TrijetBJetLdgJetMass_test;
  TBranch *TrijetBJetSubldgJetMass_test;
  TBranch *TrijetDijetMass_test;
  TBranch *TrijetBJetBDisc_test;
  TBranch *TrijetMass_test;
  TBranch *TrijetSoftDrop_n2_test;

  //next TBranch

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TopReco);

TopReco::TopReco(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invMassBins")),// Problem Here!!
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kTopReco, fHistoWrapper),
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
    fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))

{ }


void TopReco::book(TDirectory *dir) {
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
  const int nBinsPt    = cfg_PtBinSetting.bins();
  const double minPt   = cfg_PtBinSetting.min();
  const double maxPt   = cfg_PtBinSetting.max();
  
  const int nBinsEta   = cfg_EtaBinSetting.bins();
  const double minEta  = cfg_EtaBinSetting.min();
  const double maxEta  = cfg_EtaBinSetting.max();
 
  const int nBinsPhi   = cfg_PhiBinSetting.bins();
  const double minPhi  = cfg_PhiBinSetting.min();
  const double maxPhi  = cfg_PhiBinSetting.max();

   
  const int nBinsM     = cfg_MassBinSetting.bins();
  const double minM    = cfg_MassBinSetting.min();
  const double maxM    = cfg_MassBinSetting.max();
  
  const int nBinsdEta  = cfg_DeltaEtaBinSetting.bins();
  const double mindEta = cfg_DeltaEtaBinSetting.min();
  const double maxdEta = cfg_DeltaEtaBinSetting.max();

  const int nBinsdPhi  = cfg_DeltaPhiBinSetting.bins();
  const double mindPhi = cfg_DeltaPhiBinSetting.min();
  const double maxdPhi = cfg_DeltaPhiBinSetting.max();

  const int nBinsdR    = cfg_DeltaRBinSetting.bins();
  const double mindR   = cfg_DeltaRBinSetting.min();
  const double maxdR   = cfg_DeltaRBinSetting.max();


    // Create directories for normalization                                                                                                                                                
    std::string myInclusiveLabel  = "TrijetCandidate";
    std::string myFakeLabel       = myInclusiveLabel+"Fake";
    std::string myGenuineLabel    = myInclusiveLabel+"Genuine";
    TDirectory* myNormDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
    TDirectory* myNormEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
    TDirectory* myNormGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
    std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeBDir, myNormGenuineBDir};


  hTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs, "TrijetPt", ";p_{T} (GeV/c)", 2*nBinsPt, minPt , 2*maxPt);
  hTrijetEta          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetEta", ";|#eta|", nBinsEta/2, minEta, maxEta);
  hTrijetPhi          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetPhi",";#phi (rads)", nBinsPhi , minPhi , maxPhi );
  hTrijetMass         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetMass", ";m_{jjb} (GeV/c^{2})",150,0.0,1500);
  hTrijetPtDr         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetPtDr",";p_{T}#Delta R",150,0.0,1500);
  hDijetPtDr          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"DijetPtDr",";p_{T}#Delta R",150,0.0,1500);
  hDijetMass          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"DijetMass",";m_{W} (GeV/c^{2})",100,0.0,1000);
  hLdgJetBdisc        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"LdgJetBdisc",";b-tag discr",100,0.0,1.0);
  hSubldgJetBdisc     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"SubldgJetBdisc",";b-tag discr",100,0.0,1.0);
  hBJetBdisc          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"BJetBdisc",";b-tag discr",40,0.8,1.0);
  hBJetMass           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"BJetMass",";m_{b} (GeV/c^{2})", 120,0,120);
  hBJetLdgJet_Mass    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"BJetLdgJet_Mass",";M (GeV/c^{2})",100,0.0,1000);
  hBJetSubldgJet_Mass = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"BJetSubldgJet_Mass",";M (GeV/c^{2})",100,0.0,1000);
  hSoftDrop_n2        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"SoftDrop_n2",";SoftDrop_n2", 50, 0, 2);

  hNmatchedTop     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myNormDir,"NmatchedTrijets","NTrijet_{matched}",4,-0.5,3.5);
  hNmatchedTrijets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myNormDir,"NmatchedTrijetCand","NTrijet_{matched}",4,-0.5,3.5);
  hGenTop_Pt       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"GenTop_Pt", ";p_{T} (GeV/c)", 2*nBinsPt, minPt , 2*maxPt);

  hTrijetDrMin          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDrMin",";#Delta R", 50,0.0,0.5);
  hTrijetDPtOverGenPt   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDPtOverGenPt","#;Delta P_{T}/P_{T,qqb}", 500,-2.5,2.5);
  hTrijetDEtaOverGenEta = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDEtaOverGenEta",";#Delta #eta/#eta_{qqb}", 200,-1.0,1.0);
  hTrijetDPhiOverGenPhi = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDPhiOverGenPhi",";#Delta #phi/#phi_{qqb}", 200,-1.0,1.0);

  hTrijetDPt_matched  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDPt_matched",";#Delta P_{T}", 2*nBinsPt, -maxPt , maxPt);
  hTrijetDEta_matched = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDEta_matched",";#Delta #eta", 80,-0.4,0.4);
  hTrijetDPhi_matched = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetDPhi_matched",";#Delta #phi", 80,-0.4,0.4);
  

  hTrijetPtDr_TrijetMass        = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetPtDr_TrijetMass", ";p_{T}#Delta R_{T};m_{jjb}",100,0.0,1000,  100,0.0,1000);
  hTrijetPtDr_BjetLdgJetMass    = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetPtDr_BjetLdgJetMass",";p_{T}#Delta R_{T};m_{b+ldgJet}",100,0.0,1000, 100,0.0,1000);
  hDijetPtDr_DijetMass          = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"DijetPtDr_DijetMass",";p_{T}#Delta R_{W};m_{W}", 100,0.0,1000, 100,0.0,1000);
  hDijetPtDr_TrijetMass         = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"DijetPtDr_TrijetMass",";p_{T}#Delta R_{W};m_{jjb}", 100,0.0,1000, 100,0.0,1000);
  hTrijetMass_BjetLdgJetMass    = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetMass_BjetLdgJetMass",";m_{jjb};m_{b+ldgJet}" ,100,0.0,1000, 100,0.0,1000);
  hTrijetMass_BjetSubldgJetMass = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetMass_BjetSubldgJetMass",";m_{jjb};m_{b+subldgJet}" ,100,0.0,1000, 100,0.0,1000);
  hTrijetMass_DijetMass         = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myNormalizationDirs,"TrijetMass_DijetMass",";m_{jjb};m_{W}", 100,0.0,1000, 100,0.0,1000);
  //  h_DPhiJ12vsDPhiJ34 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, dir, "DPhiJ12vsDPhiJ34" , ";#Delta#phi(j1,j2);#Delta#phi(j3,j4)" , 40, 0.0, 3.15,  40,  0.0, 3.15);
  //Correlations
  
  //next histoTriplet

  // Event-Shape Variables - Histograms
  //  h_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "HT"         , ";H_{T}"      , 60, 0.0, 2500.0);


  // TTree
  treeS = new TTree("treeS", "TTree");
  treeB = new TTree("treeB", "TTree");
  tree = new TTree("tree", "TTree");

  weight_S                  = treeS -> Branch ("eventWeight",             &weight_S,                 "eventWeight_S/F"             );

  TrijetPtDR_S              = treeS -> Branch ("TrijetPtDR",              &TrijetPtDR_S,             "TrijetPtDR_S/F"              );
  TrijetDijetPtDR_S         = treeS -> Branch ("TrijetDijetPtDR",         &TrijetDijetPtDR_S,        "TrijetDijetPtDR_S/F"         );
  TrijetBjetMass_S          = treeS -> Branch ("TrijetBjetMass",          &TrijetBjetMass_S,         "TrijetBjetMass_S/F"          );
  TrijetLdgJetPt_S          = treeS -> Branch ("TrijetLdgJetPt",          &TrijetLdgJetPt_S,         "TrijetLdgJetPt_S/F"          );
  TrijetLdgJetEta_S         = treeS -> Branch ("TrijetLdgJetEta",         &TrijetLdgJetEta_S,        "TrijetLdgJetEta_S/F"         );
  TrijetLdgJetBDisc_S       = treeS -> Branch ("TrijetLdgJetBDisc",       &TrijetLdgJetBDisc_S,      "TrijetLdgJetBDisc_S/F"       );
  TrijetSubldgJetPt_S       = treeS -> Branch ("TrijetSubldgJetPt",       &TrijetSubldgJetPt_S,      "TrijetSubldgJetPt_S/F"       );
  TrijetSubldgJetEta_S      = treeS -> Branch ("TrijetSubldgJetEta",      &TrijetSubldgJetEta_S,     "TrijetSubldgJetEta_S/F"      );
  TrijetSubldgJetBDisc_S    = treeS -> Branch ("TrijetSubldgJetBDisc",    &TrijetSubldgJetBDisc_S,   "TrijetSubldgJetBDisc_S/F"    );
  TrijetBJetLdgJetMass_S    = treeS -> Branch ("TrijetBJetLdgJetMass",    &TrijetBJetLdgJetMass_S,   "TrijetBJetLdgJetMass_S/F"    );
  TrijetBJetSubldgJetMass_S = treeS -> Branch ("TrijetBJetSubldgJetMass", &TrijetBJetSubldgJetMass_S,"TrijetBJetSubldgJetMass_S/F" );
  TrijetDijetMass_S         = treeS -> Branch ("TrijetDijetMass",         &TrijetDijetMass_S,        "TrijetDijetMass_S/F"         );
  TrijetBJetBDisc_S         = treeS -> Branch ("TrijetBJetBDisc",         &TrijetBJetBDisc_S,        "TrijetBJetBDisc_S/F"         );
  TrijetMass_S              = treeS -> Branch ("TrijetMass",              &TrijetMass_S,             "TrijetMass_S/F"              );
  TrijetSoftDrop_n2_S       = treeS -> Branch ("TrijetSoftDrop_n2",       &TrijetSoftDrop_n2_S,      "TrijetSoftDrop_n2_S/F"       );

  weight_B                  = treeB -> Branch ("eventWeight",             &weight_B,                 "eventWeight_B/F"             );

  TrijetPtDR_B              = treeB -> Branch ("TrijetPtDR",              &TrijetPtDR_B,             "TrijetPtDR_B/F"              );
  TrijetDijetPtDR_B         = treeB -> Branch ("TrijetDijetPtDR",         &TrijetDijetPtDR_B,        "TrijetDijetPtDR_B/F"         );
  TrijetBjetMass_B          = treeB -> Branch ("TrijetBjetMass",          &TrijetBjetMass_B,         "TrijetBjetMass_B/F"          );
  TrijetLdgJetPt_B          = treeB -> Branch ("TrijetLdgJetPt",          &TrijetLdgJetPt_B,         "TrijetLdgJetPt_B/F"          );
  TrijetLdgJetEta_B         = treeB -> Branch ("TrijetLdgJetEta",         &TrijetLdgJetEta_B,        "TrijetLdgJetEta_B/F"         );
  TrijetLdgJetBDisc_B       = treeB -> Branch ("TrijetLdgJetBDisc",       &TrijetLdgJetBDisc_B,      "TrijetLdgJetBDisc_B/F"       );
  TrijetSubldgJetPt_B       = treeB -> Branch ("TrijetSubldgJetPt",       &TrijetSubldgJetPt_B,      "TrijetSubldgJetPt_B/F"       );
  TrijetSubldgJetEta_B      = treeB -> Branch ("TrijetSubldgJetEta",      &TrijetSubldgJetEta_B,     "TrijetSubldgJetEta_B/F"      );
  TrijetSubldgJetBDisc_B    = treeB -> Branch ("TrijetSubldgJetBDisc",    &TrijetSubldgJetBDisc_B,   "TrijetSubldgJetBDisc_B/F"    );
  TrijetBJetLdgJetMass_B    = treeB -> Branch ("TrijetBJetLdgJetMass",    &TrijetBJetLdgJetMass_B,   "TrijetBJetLdgJetMass_B/F"    );
  TrijetBJetSubldgJetMass_B = treeB -> Branch ("TrijetBJetSubldgJetMass", &TrijetBJetSubldgJetMass_B,"TrijetBJetSubldgJetMass_B/F" );
  TrijetDijetMass_B         = treeB -> Branch ("TrijetDijetMass",         &TrijetDijetMass_B,        "TrijetDijetMass_B/F"         );
  TrijetBJetBDisc_B         = treeB -> Branch ("TrijetBJetBDisc",         &TrijetBJetBDisc_B,        "TrijetBJetBDisc_B/F"         );
  TrijetMass_B              = treeB -> Branch ("TrijetMass",              &TrijetMass_B,             "TrijetMass_B/F"              );
  TrijetSoftDrop_n2_B       = treeB -> Branch ("TrijetSoftDrop_n2",       &TrijetSoftDrop_n2_B,      "TrijetSoftDrop_n2_B/F"       );

  //New test tree
  weight_test                  = tree -> Branch ("eventWeight",             &weight_test,                 "eventWeight_test/F"             );

  TrijetPtDR_test              = tree -> Branch ("TrijetPtDR",              &TrijetPtDR_test,             "TrijetPtDR_test/F"              );
  TrijetDijetPtDR_test         = tree -> Branch ("TrijetDijetPtDR",         &TrijetDijetPtDR_test,        "TrijetDijetPtDR_test/F"         );
  TrijetBjetMass_test          = tree -> Branch ("TrijetBjetMass",          &TrijetBjetMass_test,         "TrijetBjetMass_test/F"          );
  TrijetLdgJetPt_test          = tree -> Branch ("TrijetLdgJetPt",          &TrijetLdgJetPt_test,         "TrijetLdgJetPt_test/F"          );
  TrijetLdgJetEta_test         = tree -> Branch ("TrijetLdgJetEta",         &TrijetLdgJetEta_test,        "TrijetLdgJetEta_test/F"         );
  TrijetLdgJetBDisc_test       = tree -> Branch ("TrijetLdgJetBDisc",       &TrijetLdgJetBDisc_test,      "TrijetLdgJetBDisc_test/F"       );
  TrijetSubldgJetPt_test       = tree -> Branch ("TrijetSubldgJetPt",       &TrijetSubldgJetPt_test,      "TrijetSubldgJetPt_test/F"       );
  TrijetSubldgJetEta_test      = tree -> Branch ("TrijetSubldgJetEta",      &TrijetSubldgJetEta_test,     "TrijetSubldgJetEta_test/F"      );
  TrijetSubldgJetBDisc_test    = tree -> Branch ("TrijetSubldgJetBDisc",    &TrijetSubldgJetBDisc_test,   "TrijetSubldgJetBDisc_test/F"    );
  TrijetBJetLdgJetMass_test    = tree -> Branch ("TrijetBJetLdgJetMass",    &TrijetBJetLdgJetMass_test,   "TrijetBJetLdgJetMass_test/F"    );
  TrijetBJetSubldgJetMass_test = tree -> Branch ("TrijetBJetSubldgJetMass", &TrijetBJetSubldgJetMass_test,"TrijetBJetSubldgJetMass_test/F" );
  TrijetDijetMass_test         = tree -> Branch ("TrijetDijetMass",         &TrijetDijetMass_test,        "TrijetDijetMass_test/F"         );
  TrijetBJetBDisc_test         = tree -> Branch ("TrijetBJetBDisc",         &TrijetBJetBDisc_test,        "TrijetBJetBDisc_test/F"         );
  TrijetMass_test              = tree -> Branch ("TrijetMass",              &TrijetMass_test,             "TrijetMass_test/F"              );
  TrijetSoftDrop_n2_test       = tree -> Branch ("TrijetSoftDrop_n2",       &TrijetSoftDrop_n2_test,      "TrijetSoftDrop_n2_test/F"       );


  //next branch

  return;
}


/*                                                                                                                                                                                                                                                                 
  Get all gen particles by pdgId                                                                                                                                                                                                                                   
*/
vector<genParticle> TopReco::GetGenParticles(const vector<genParticle> genParticles, const int pdgId)
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
const genParticle TopReco::GetLastCopy(const vector<genParticle> genParticles, const genParticle &p){

  int gen_pdgId = p.pdgId();

  for (size_t i=0; i<p.daughters().size(); i++){

    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();

    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}





std::vector<int> TopReco::SortInPt(std::vector<int> Vector)
{
  int size = Vector.size();
  for (int i=0; i<size-1; i++){
    genParticle genPart1 = fEvent.genparticles().getGenParticles()[Vector.at(i)];
    for (int j=i+1;  j<size; j++){
      genParticle genPart2 = fEvent.genparticles().getGenParticles()[Vector.at(j)];
      if (genPart1.pt() > genPart2.pt()) continue;
      int temp = Vector.at(i);
      Vector.at(i) = Vector.at(j);
      Vector.at(j) = temp;
    }
  }
  return Vector;
}
std::vector<math::XYZTLorentzVector> TopReco::SortInPt(std::vector<math::XYZTLorentzVector> Vector)
{
  int size = Vector.size();
  for (int i=0; i<size-1; i++){
    math::XYZTLorentzVector p4_i = Vector.at(i);
    for (int j=i+1;  j<size; j++){
      math::XYZTLorentzVector p4_j = Vector.at(j);
      if (p4_i.pt() > p4_j.pt()) continue;
      Vector.at(i) = p4_j;
      Vector.at(j) = p4_i;
    }
  }
  return Vector;
}


genParticle TopReco::findLastCopy(int index){
  genParticle gen_particle = fEvent.genparticles().getGenParticles()[index];
  int gen_pdgId = gen_particle.pdgId();
  for (int i=0; i<gen_particle.daughters().size(); i++){
    
    genParticle genDau = fEvent.genparticles().getGenParticles()[gen_particle.daughters().at(i)];
    int genDau_index   = genDau.index();
    int genDau_pdgId   = genDau.pdgId();
    if (gen_pdgId == genDau_pdgId) return findLastCopy(genDau_index);
  }
  return gen_particle;
}
  

bool TopReco::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool TopReco::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}


bool TopReco::areMatchedJets(math::XYZTLorentzVector jet1, math::XYZTLorentzVector  jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1, jet2);
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}

void TopReco::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void TopReco::process(Long64_t entry) {

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
  if (0){ //soti removed topSelection
    if(0) std::cout << "=== Top selection" << std::endl;
    const TopSelection::Data TopData = fTopSelection.analyze(fEvent, jetData, bjetData);
    if (!TopData.passedSelection()) return;
  }
  //================================================================================================
  // All cuts passed
  //================================================================================================
  if(0) std::cout << "=== All cuts passed" << std::endl;
  cSelected.increment();



  // Define the addresses of the variables which will be added to the TTree
  float eventWeight_S;

  float trijetPtDR_S, trijetDijetPtDR_S, trijetBjetMass_S, trijetLdgJetPt_S, trijetLdgJetEta_S, trijetLdgJetBDisc_S, trijetSubldgJetPt_S, trijetSubldgJetEta_S, trijetSubldgJetBDisc_S, trijetBJetLdgJetMass_S, trijetBJetSubldgJetMass_S, trijetDijetMass_S, trijetBJetBDisc_S, trijetMass_S,trijetSoftDrop_n2_S;

  float eventWeight_B;

  float trijetPtDR_B, trijetDijetPtDR_B, trijetBjetMass_B, trijetLdgJetPt_B, trijetLdgJetEta_B, trijetLdgJetBDisc_B, trijetSubldgJetPt_B, trijetSubldgJetEta_B, trijetSubldgJetBDisc_B, trijetBJetLdgJetMass_B, trijetBJetSubldgJetMass_B, trijetDijetMass_B, trijetBJetBDisc_B, trijetMass_B, trijetSoftDrop_n2_B;

  float eventWeight_test;
  float trijetPtDR_test, trijetDijetPtDR_test, trijetBjetMass_test, trijetLdgJetPt_test, trijetLdgJetEta_test, trijetLdgJetBDisc_test, trijetSubldgJetPt_test, trijetSubldgJetEta_test, trijetSubldgJetBDisc_test, trijetBJetLdgJetMass_test, trijetBJetSubldgJetMass_test, trijetDijetMass_test, trijetBJetBDisc_test, trijetMass_test, trijetSoftDrop_n2_test;

  //next variable 
  // TTree Variables (Event-Weight)


  weight_S                     -> SetAddress(&eventWeight_S);
  TrijetPtDR_S                 -> SetAddress(&trijetPtDR_S);
  TrijetDijetPtDR_S            -> SetAddress(&trijetDijetPtDR_S);
  TrijetBjetMass_S             -> SetAddress(&trijetBjetMass_S);
  TrijetLdgJetPt_S             -> SetAddress(&trijetLdgJetPt_S);
  TrijetLdgJetEta_S            -> SetAddress(&trijetLdgJetEta_S);
  TrijetLdgJetBDisc_S          -> SetAddress(&trijetLdgJetBDisc_S);
  TrijetSubldgJetPt_S          -> SetAddress(&trijetSubldgJetPt_S);
  TrijetSubldgJetEta_S         -> SetAddress(&trijetSubldgJetEta_S);
  TrijetSubldgJetBDisc_S       -> SetAddress(&trijetSubldgJetBDisc_S);
  TrijetBJetLdgJetMass_S       -> SetAddress(&trijetBJetLdgJetMass_S);
  TrijetBJetSubldgJetMass_S    -> SetAddress(&trijetBJetSubldgJetMass_S);
  TrijetDijetMass_S            -> SetAddress(&trijetDijetMass_S);
  TrijetBJetBDisc_S            -> SetAddress(&trijetBJetBDisc_S);
  TrijetMass_S                 -> SetAddress(&trijetMass_S);
  TrijetSoftDrop_n2_S          -> SetAddress(&trijetSoftDrop_n2_S);


  weight_B                     -> SetAddress(&eventWeight_B);
  TrijetPtDR_B                 -> SetAddress(&trijetPtDR_B);
  TrijetDijetPtDR_B            -> SetAddress(&trijetDijetPtDR_B);
  TrijetBjetMass_B             -> SetAddress(&trijetBjetMass_B);
  TrijetLdgJetPt_B             -> SetAddress(&trijetLdgJetPt_B);
  TrijetLdgJetEta_B            -> SetAddress(&trijetLdgJetEta_B);
  TrijetLdgJetBDisc_B          -> SetAddress(&trijetLdgJetBDisc_B);
  TrijetSubldgJetPt_B          -> SetAddress(&trijetSubldgJetPt_B);
  TrijetSubldgJetEta_B         -> SetAddress(&trijetSubldgJetEta_B);
  TrijetSubldgJetBDisc_B       -> SetAddress(&trijetSubldgJetBDisc_B);
  TrijetBJetLdgJetMass_B       -> SetAddress(&trijetBJetLdgJetMass_B);
  TrijetBJetSubldgJetMass_B    -> SetAddress(&trijetBJetSubldgJetMass_B);
  TrijetDijetMass_B            -> SetAddress(&trijetDijetMass_B);
  TrijetBJetBDisc_B            -> SetAddress(&trijetBJetBDisc_B);
  TrijetMass_B                 -> SetAddress(&trijetMass_B);
  TrijetSoftDrop_n2_B          -> SetAddress(&trijetSoftDrop_n2_B);




  weight_test                     -> SetAddress(&eventWeight_test);
  TrijetPtDR_test                 -> SetAddress(&trijetPtDR_test);
  TrijetDijetPtDR_test            -> SetAddress(&trijetDijetPtDR_test);
  TrijetBjetMass_test             -> SetAddress(&trijetBjetMass_test);
  TrijetLdgJetPt_test             -> SetAddress(&trijetLdgJetPt_test);
  TrijetLdgJetEta_test            -> SetAddress(&trijetLdgJetEta_test);
  TrijetLdgJetBDisc_test          -> SetAddress(&trijetLdgJetBDisc_test);
  TrijetSubldgJetPt_test          -> SetAddress(&trijetSubldgJetPt_test);
  TrijetSubldgJetEta_test         -> SetAddress(&trijetSubldgJetEta_test);
  TrijetSubldgJetBDisc_test       -> SetAddress(&trijetSubldgJetBDisc_test);
  TrijetBJetLdgJetMass_test       -> SetAddress(&trijetBJetLdgJetMass_test);
  TrijetBJetSubldgJetMass_test    -> SetAddress(&trijetBJetSubldgJetMass_test);
  TrijetDijetMass_test            -> SetAddress(&trijetDijetMass_test);
  TrijetBJetBDisc_test            -> SetAddress(&trijetBJetBDisc_test);
  TrijetMass_test                 -> SetAddress(&trijetMass_test);
  TrijetSoftDrop_n2_test          -> SetAddress(&trijetSoftDrop_n2_test);
  //next address


  //================================================================================================//
  //                            Gen Trijet subjets selection                                        //
  //================================================================================================//

  //START
  if (fEvent.isMC()){
    
    vector<genParticle> GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
    vector<genParticle> GenTops_BQuark;
    vector<genParticle> GenTops_LdgQuark;
    vector<genParticle> GenTops_SubldgQuark;
    
    for (auto& top: GenTops){
      
      vector<genParticle> quarks;
      genParticle bquark;
      
      for (size_t i=0; i<top.daughters().size(); i++){
	
        int dau_index = top.daughters().at(i);
        genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
	
        // B-Quark                                                                                                                                                                       
        if (std::abs(dau.pdgId()) ==  5) bquark = dau;
	
        // W-Boson                                                                                                                                                                       
        if (std::abs(dau.pdgId()) == 24){
          // Get the last copy                                                                                                                                                           
          genParticle W = GetLastCopy(fEvent.genparticles().getGenParticles(), dau);
	  
          // Find the decay products of W                                                                                                                                                
          for (size_t idau=0; idau<W.daughters().size(); idau++){
	    
            int Wdau_index = W.daughters().at(idau);
            genParticle Wdau = fEvent.genparticles().getGenParticles()[Wdau_index];
	    
            // Consider only quarks as decaying products                                                                                                                                 
            if (std::abs(Wdau.pdgId()) > 5) continue;
	    
            quarks.push_back(Wdau);
          }
        }
      }
      
      // Skip event if any of the tops decays leptonically (the "quarks" vector will be empty causing errors)                                                                            
      if (!(quarks.size() == 2)) return;
      // Fill vectors for b-quarks, leading and subleading quarks coming from tops                                                                                                       
      GenTops_BQuark.push_back(bquark);
      
      if (quarks.at(0).pt() > quarks.at(1).pt()) {
        GenTops_LdgQuark.push_back(quarks.at(0));
        GenTops_SubldgQuark.push_back(quarks.at(1));
      }
      else{
        GenTops_LdgQuark.push_back(quarks.at(1));
        GenTops_SubldgQuark.push_back(quarks.at(0));
      }
    }
    
    // Keep only events with at least two hadronically decaying tops                                                                                                                     
    if (GenTops_BQuark.size() < 2) return;
    
    
    
    //================================================================================================//                      
    //                                    Top Candidates                                              //
    //================================================================================================//
    TrijetSelection TopCandidates;
    
    for (auto& bjet: bjetData.getSelectedBJets())
      {
	int index1 = -1;
	for (auto& jet1: jetData.getSelectedJets())
	  {
	    index1++;
	    if (isBJet(jet1, bjetData.getSelectedBJets()))     continue;
	    if (areSameJets(jet1, bjet)) continue;
	    int index2 = -1;
	    for (auto& jet2: jetData.getSelectedJets())
	      {
		index2++;
		if (index2 < index1) continue;

		if (isBJet(jet2, bjetData.getSelectedBJets()))      continue;
		if (areSameJets(jet2,  jet1)) continue;
		if (areSameJets(jet2,  bjet)) continue;
		
		TopCandidates.BJet.push_back(bjet);
		
		if (jet1.pt() > jet2.pt())
		  {
		    TopCandidates.Jet1.push_back(jet1);
		    TopCandidates.Jet2.push_back(jet2);
		  }
		else
		  {
		    TopCandidates.Jet1.push_back(jet2);
		    TopCandidates.Jet2.push_back(jet1);
		  }
	      }
	  }
      }
    
    
    //========================================================================================================
    //                              Matching:  Minimum DeltaR and DeltaPt check
    //========================================================================================================
    
    int imatched =0;
    vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet;
    vector <genParticle> MGen_LdgJet, MGen_SubldgJet, MGen_Bjet;
    for (size_t i=0; i<GenTops.size(); i++)
      {
	genParticle BQuark      = GenTops_BQuark.at(i);
	genParticle LdgQuark    = GenTops_LdgQuark.at(i);
	genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
	
	Jet mcMatched_BJet;
	Jet mcMatched_LdgJet;
	Jet mcMatched_SubldgJet;
	
	double dRmin  = 99999.9;
	double dPtmin = 99999.9;
	
	for (auto& bjet: bjetData.getSelectedBJets())
	  {
	    double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
	    double dPt = std::abs(bjet.pt() - BQuark.pt());
	    
	    if (dR > 0.4) continue;
	    if (dR > dRmin) continue;
	    if (dPt > dPtmin) continue;
	    
	    dRmin = dR;
	    dPtmin = dPt;
	    mcMatched_BJet = bjet;
	  }
	
	
	double dR1min, dR2min, dPt1min, dPt2min;
	dR1min = dR2min = dPt1min = dPt2min = 99999.9;
	for (auto& jet: jetData.getSelectedJets())
	  {
	    if (isBJet(jet, bjetData.getSelectedBJets())) continue;
	    
	    double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
	    double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
	    
	    if (std::min(dR1, dR2) > 0.4) continue;
	    
	    double dPt1 = std::abs(jet.pt() - LdgQuark.pt());
	    double dPt2 = std::abs(jet.pt() - SubldgQuark.pt());
	    
	    if (dR1 < dR2)
	      {
		if (dR1 < dR1min && dPt1 < dPt1min)
		  {
		    dR1min = dR1;
		    dPt1min= dPt1;
		    mcMatched_LdgJet = jet;
		  }
		else if (dR2 <= 0.4 && dR2 < dR2min && dPt2 < dPt2min)
		  {
		    dR2min  = dR2;
		    dPt2min = dPt2;
		    mcMatched_SubldgJet = jet;
		  }
	      }
	    else
	      {
		if (dR2 < dR2min && dPt2 < dPt2min)
		  {
		    dR2min  = dR2;
		    dPt2min = dPt2;
		    mcMatched_SubldgJet = jet;
		  }
		else if (dR1 <= 0.4 && dR1 < dR1min && dPt1 < dPt1min)
		  {
		    dR1min  = dR1;
		    dPt1min = dPt1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	  }
	
	// If Matched (fix me)                                                                                                                                                                                                             
      	
	genParticle top = GenTops.at(i);
	
	bool genuine = (dR1min<= 0.4 && dR2min <= 0.4 && dRmin <= 0.4);
	if (genuine){
	  imatched ++;
	  hGenTop_Pt->Fill(true, top.pt());
	  
	  MCtrue_LdgJet.push_back(mcMatched_LdgJet);
	  MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
	  MCtrue_Bjet.push_back(mcMatched_BJet);
	  
	  MGen_LdgJet.push_back(GenTops_LdgQuark.at(i));
	  MGen_SubldgJet.push_back(GenTops_SubldgQuark.at(i));
	  MGen_Bjet.push_back(GenTops_BQuark.at(i));
	}
	else {
	  hGenTop_Pt->Fill(false, top.pt());
	}
      }
    hNmatchedTop ->Fill(imatched);
    
    
    
    
    //========================================================================================================
    //                       Identification of fake, genuine TopCandidates
    //========================================================================================================
    
    vector <bool> GenuineTop; 
    int jmatched = 0;
    for (int i=0; i<TopCandidates.BJet.size(); i++){
      bool genuine = false;
      for (int j=0; j<MCtrue_Bjet.size(); j++){
	bool same1 = areSameJets(TopCandidates.Jet1.at(i), MCtrue_LdgJet.at(j) )       && areSameJets(TopCandidates.Jet2.at(i), MCtrue_SubldgJet.at(j) );
	bool same2 = areSameJets(TopCandidates.Jet1.at(i), MCtrue_SubldgJet.at(j) )    && areSameJets(TopCandidates.Jet2.at(i), MCtrue_LdgJet.at(j)    );
	bool sameB = areSameJets(TopCandidates.BJet.at(i), MCtrue_Bjet.at(j) );
	if ((same1 || same2) && sameB){
	  genuine = true;
	}
      }
      if (genuine) jmatched++;
      GenuineTop.push_back(genuine);
    }
    hNmatchedTrijets ->Fill(jmatched);
   
    
    //========================================================================================================
    //                           Check Properties of matched objects //Improve me! 
    //========================================================================================================
    for (int j=0; j<MCtrue_Bjet.size(); j++){
      bool flavour_bool = false;
      int flavour = 0;
      for (int k=0; k<bjetData.getSelectedBJets().size(); k++){
	Jet bjet;
	bjet = bjetData.getSelectedBJets().at(k);
	// std::cout<<"bjet hadron flavour "<<bjet.hadronFlavour()<<std::endl;                                                                                                                                              
	// std::cout<<"bjet parton flavour "<<bjet.partonFlavour()<<std::endl;      
	float dR = ROOT::Math::VectorUtil::DeltaR(bjet.p4(), MCtrue_Bjet.at(j).p4());
	float dR_match = 0.1;
	if (dR <= dR_match) flavour = bjet.partonFlavour();
      }
      if (std::abs(flavour) ==  5) flavour_bool =true;
      
      //    std::cout<<flavour_bool<<" flavour = "<<flavour<<std::endl;
      
      hTrijetDrMin -> Fill(flavour_bool, ROOT::Math::VectorUtil::DeltaR(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4()));
      hTrijetDrMin -> Fill(false, ROOT::Math::VectorUtil::DeltaR(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4()));
      hTrijetDrMin -> Fill(false, ROOT::Math::VectorUtil::DeltaR(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4()));
      
      hTrijetDPtOverGenPt -> Fill(flavour_bool, (MCtrue_Bjet.at(j).pt() - MGen_Bjet.at(j).pt())/MGen_Bjet.at(j).pt());
      hTrijetDPtOverGenPt -> Fill(false, (MCtrue_LdgJet.at(j).pt() - MGen_LdgJet.at(j).pt())/MGen_LdgJet.at(j).pt());
      hTrijetDPtOverGenPt -> Fill(false, (MCtrue_SubldgJet.at(j).pt() - MGen_SubldgJet.at(j).pt())/MGen_SubldgJet.at(j).pt());
      
      hTrijetDPt_matched -> Fill(flavour_bool, (MCtrue_Bjet.at(j).pt() - MGen_Bjet.at(j).pt()));
      hTrijetDPt_matched -> Fill(false, (MCtrue_LdgJet.at(j).pt() - MGen_LdgJet.at(j).pt()));
      hTrijetDPt_matched -> Fill(false, (MCtrue_SubldgJet.at(j).pt() - MGen_SubldgJet.at(j).pt()));
      
      hTrijetDEtaOverGenEta -> Fill(flavour_bool, (MCtrue_Bjet.at(j).eta() - MGen_Bjet.at(j).eta())/MGen_Bjet.at(j).eta());
      hTrijetDEtaOverGenEta -> Fill(false, (MCtrue_LdgJet.at(j).eta() - MGen_LdgJet.at(j).eta())/MGen_LdgJet.at(j).eta());
      hTrijetDEtaOverGenEta -> Fill(false, (MCtrue_SubldgJet.at(j).eta() - MGen_SubldgJet.at(j).eta())/MGen_SubldgJet.at(j).eta());
      
      hTrijetDEta_matched -> Fill(flavour_bool, (MCtrue_Bjet.at(j).eta() - MGen_Bjet.at(j).eta()));
      hTrijetDEta_matched -> Fill(false, (MCtrue_LdgJet.at(j).eta() - MGen_LdgJet.at(j).eta()));
      hTrijetDEta_matched -> Fill(false, (MCtrue_SubldgJet.at(j).eta() - MGen_SubldgJet.at(j).eta()));
      
      hTrijetDPhiOverGenPhi -> Fill(flavour_bool,(ROOT::Math::VectorUtil::DeltaPhi(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4()))/MGen_Bjet.at(j).phi());
      hTrijetDPhiOverGenPhi -> Fill(false, (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4()))/MGen_LdgJet.at(j).phi());
      hTrijetDPhiOverGenPhi -> Fill(false, (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4()))/MGen_SubldgJet.at(j).phi());
      
      hTrijetDPhi_matched -> Fill(flavour_bool,(ROOT::Math::VectorUtil::DeltaPhi(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4())));
      hTrijetDPhi_matched -> Fill(false, (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4())));
      hTrijetDPhi_matched -> Fill(false, (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4())));
      
    }
    
    
    
    //========================================================================================================
    //                                 Fill Triplets and trees
    //========================================================================================================
    
    
    
    Bool_t isGenuineB = false;

    for (size_t i=0; i<TopCandidates.BJet.size(); i++){
      math::XYZTLorentzVector trijetp4, dijetp4;                                                                                                                              
      trijetp4 = TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()+TopCandidates.Jet2.at(i).p4();
      dijetp4 = TopCandidates.Jet1.at(i).p4()+TopCandidates.Jet2.at(i).p4();
      TopCandidates.TrijetP4.push_back(trijetp4);                                                                                                                                      
      TopCandidates.DijetP4.push_back(dijetp4);                                                                                                                                        

      isGenuineB = GenuineTop.at(i);
      
      hTrijetPt           -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Pt());
      hTrijetEta          -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Eta());
      hTrijetPhi          -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Phi());
      
      hTrijetMass         -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).M());
      hDijetPtDr          -> Fill(isGenuineB, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()));
      hTrijetPtDr         -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()));
      hDijetMass          -> Fill(isGenuineB, TopCandidates.DijetP4.at(i).M());
      hLdgJetBdisc        -> Fill(isGenuineB, TopCandidates.Jet1.at(i).bjetDiscriminator());
      hSubldgJetBdisc     -> Fill(isGenuineB, TopCandidates.Jet2.at(i).bjetDiscriminator());
      hBJetBdisc          -> Fill(isGenuineB, TopCandidates.BJet.at(i).bjetDiscriminator());
      hBJetMass           -> Fill(isGenuineB, TopCandidates.BJet.at(i).p4().M());
      hBJetLdgJet_Mass    -> Fill(isGenuineB, (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hBJetSubldgJet_Mass -> Fill(isGenuineB, (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M());
      
      
      hTrijetPtDr_TrijetMass -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()),TopCandidates.TrijetP4.at(i).M());
      hTrijetPtDr_BjetLdgJetMass -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()),(TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hDijetPtDr_DijetMass -> Fill(isGenuineB, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()), TopCandidates.DijetP4.at(i).M()); 
      hDijetPtDr_TrijetMass -> Fill(isGenuineB, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()), TopCandidates.TrijetP4.at(i).M()); 
      hTrijetMass_BjetLdgJetMass -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).M(), (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hTrijetMass_BjetSubldgJetMass -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).M(),(TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M());
      hTrijetMass_DijetMass -> Fill(isGenuineB, TopCandidates.TrijetP4.at(i).M(), TopCandidates.DijetP4.at(i).M());
      
      
      double dr_sd = ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
      double softDrop_n2 = min(TopCandidates.Jet2.at(i).pt(), TopCandidates.Jet1.at(i).pt())/( (TopCandidates.Jet2.at(i).pt() + TopCandidates.Jet1.at(i).pt() )*dr_sd*dr_sd);
      hSoftDrop_n2        -> Fill(isGenuineB, softDrop_n2);
      
      if (isGenuineB){
	eventWeight_S             = fEventWeight.getWeight();
	trijetMass_S              = TopCandidates.TrijetP4.at(i).M();
	trijetDijetPtDR_S         = TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
	trijetPtDR_S              = TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4());
	trijetDijetMass_S         = TopCandidates.DijetP4.at(i).M();
	trijetLdgJetBDisc_S       = TopCandidates.Jet1.at(i).bjetDiscriminator();
	if (trijetLdgJetBDisc_S < 0 ) trijetLdgJetBDisc_S =-1.;
	trijetSubldgJetBDisc_S    = TopCandidates.Jet2.at(i).bjetDiscriminator();
	if (trijetSubldgJetBDisc_S < 0 ) trijetSubldgJetBDisc_S =-1.;
	trijetBJetBDisc_S         = TopCandidates.BJet.at(i).bjetDiscriminator();
	trijetBjetMass_S          = TopCandidates.BJet.at(i).p4().M();
	trijetBJetLdgJetMass_S    = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M();
	trijetBJetSubldgJetMass_S = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M();
	trijetSoftDrop_n2_S       = softDrop_n2;
	
	treeS -> Fill();
	
      }
      else{
	eventWeight_B             = fEventWeight.getWeight();
	trijetMass_B              = TopCandidates.TrijetP4.at(i).M();
	trijetDijetPtDR_B         = TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
	trijetPtDR_B              = TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4());
	trijetDijetMass_B         = TopCandidates.DijetP4.at(i).M();
	trijetLdgJetBDisc_B       = TopCandidates.Jet1.at(i).bjetDiscriminator();
	if (trijetLdgJetBDisc_B < 0 ) trijetLdgJetBDisc_B =-1.;
	trijetSubldgJetBDisc_B    = TopCandidates.Jet2.at(i).bjetDiscriminator();
	if (trijetSubldgJetBDisc_B < 0 ) trijetSubldgJetBDisc_B =-1.;
	trijetBJetBDisc_B         = TopCandidates.BJet.at(i).bjetDiscriminator();
	trijetBjetMass_B          = TopCandidates.BJet.at(i).p4().M();
	trijetBJetLdgJetMass_B    = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M();
	trijetBJetSubldgJetMass_B = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M();
	trijetSoftDrop_n2_B       = softDrop_n2;
	
	treeB -> Fill();

	
      }
      
	eventWeight_test             = fEventWeight.getWeight();
	trijetMass_test              = TopCandidates.TrijetP4.at(i).M();
	trijetDijetPtDR_test         = TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
	trijetPtDR_test              = TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4());
	trijetDijetMass_test         = TopCandidates.DijetP4.at(i).M();
	trijetLdgJetBDisc_test       = TopCandidates.Jet1.at(i).bjetDiscriminator();
	if (trijetLdgJetBDisc_test < 0 ) trijetLdgJetBDisc_test =-1.;
	trijetSubldgJetBDisc_test    = TopCandidates.Jet2.at(i).bjetDiscriminator();
	if (trijetSubldgJetBDisc_test < 0 ) trijetSubldgJetBDisc_test =-1.;
	trijetBJetBDisc_test         = TopCandidates.BJet.at(i).bjetDiscriminator();
	trijetBjetMass_test          = TopCandidates.BJet.at(i).p4().M();
	trijetBJetLdgJetMass_test    = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M();
	trijetBJetSubldgJetMass_test = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M();
	trijetSoftDrop_n2_test       = softDrop_n2;

	tree -> Fill();
      
      
    }
    //next fill histo
    //Check number of top candidates
    if (0){
      std::cout<<"Number of bjets: "<<bjetData.getSelectedBJets().size()<<" Number of untagged jets: "<<jetData.getSelectedJets().size() - bjetData.getSelectedBJets().size()<<std::endl;
      std::cout<<"Number of top candidates = "<< TopCandidates.TrijetP4.size()<<std::endl;
      std::cout<<"======================================="<<std::endl;
      std::cout<<"======================================="<<std::endl;
    }
    
    
    //next address
    // TTree Variables
    
    //Variables from AN-16-437
    
    //next 
    
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
      //    if (cAllEvents.value() == 777 || cAllEvents.value() == 5116 || cAllEvents.value() == 6520 || cAllEvents.value() == 7047 || cAllEvents.value() == 7481){
      if (0){
	if (genP_index == 0){
	  std::cout << "\n" << std::endl;                                                                                                                                                    
	  std::cout << std::string(15*10, '=') << std::endl;                                                                                                                                      std::cout << std::setw(12) << "Index "   << std::setw(12) << "PdgId"        << std::setw(12) << "Pt"           << std::setw(12) << "Eta" << std::setw(12) << "Phi"
		    << std::setw(12) << "Energy"   << std::setw(12) << "Mass"         << std::setw(12) << "status"       <<std::setw(12)  << "1st Mom-Idx"
		    << std::setw(15) << "last Mom-Idx" << std::setw(12) << "Nmothers" << std::setw(12) << "1st Dau-Idx"  << std::setw(15) << "last Dau-Idx" 
		    << std::setw(12) << "NDaughters"<<std::endl;                                                                                                                               
	  std::cout << std::string(15*10, '=') << std::endl;
	}
	std::cout << std::setw(12) << genP_index            << std::setw(12)   << genP_pdgId  
		  << std::setw(12) << genP_pt               << std::setw(12)   << genP_eta       
		  << std::setw(12) << genP_phi              << std::setw(12)   << genP_ene      
		  << std::setw(12) << genP_p4.M()           << std::setw(12)   << genP_status   
		  << std::setw(12) << firstMom              << std::setw(12)   << lastMom 
		  << std::setw(12) << genP_mothers.size()   << std::setw(12)   << firstDau 
		  << std::setw(12) << lastDau               << std::setw(12)   << genP_daughters.size() <<  std::endl;
      }
      
      // if (std::abs(genP_pdgId) == 37 && isLastCopy  (genP_index, 37 )) Higgs = genP_p4;
      // if (std::abs(genP_pdgId) == 6  && isFirstCopy (genP_index, 6  )) FirstTop.push_back(genP_p4);
      
    }
    
    
    // =========================================================================
    //================================================================================================                 
    // Fill TTree                                                                                                                
    //================================================================================================  
    
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
}
  
