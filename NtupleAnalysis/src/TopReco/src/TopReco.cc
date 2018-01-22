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

//#include "EventSelection/interface/TrijetSelection.h"   //Soti


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

struct TrijetSelections{
  std::vector<Jet> Jet1;
  std::vector<Jet> Jet2;
  std::vector<Jet> BJet;
  std::vector <double> MVA;
  std::vector<math::XYZTLorentzVector> TrijetP4; //temporary
  std::vector<math::XYZTLorentzVector> DijetP4;  //temporary
};


class TopReco: public BaseSelector {
public:
  explicit TopReco(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TopReco() {}

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
  /// Books histograms
  virtual void book(TDirectory *dir ) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

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
  //  TopSelection       fTopSelection;
  //  TopSelectionBDT    fTopSelectionBDT;
  Count              cSelected;
    

  //Top Reconstruction Variables
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
  //...
  WrappedTH1Triplet *hLdgJetCvsL;
  WrappedTH1Triplet *hSubldgJetCvsL;
  WrappedTH1Triplet *hLdgJetPtD;
  WrappedTH1Triplet *hSubldgJetPtD;
  WrappedTH1Triplet *hLdgJetAxis2;
  WrappedTH1Triplet *hSubldgJetAxis2;
  WrappedTH1Triplet *hLdgJetMult;
  WrappedTH1Triplet *hSubldgJetMult;

  WrappedTH1Triplet *hLdgJetQGLikelihood;
  WrappedTH1Triplet *hSubldgJetQGLikelihood;

  WrappedTH1Triplet *hBJetCvsL;
  WrappedTH1Triplet *hBJetPtD;
  WrappedTH1Triplet *hBJetAxis2;
  WrappedTH1Triplet *hBJetMult;

  WrappedTH1Triplet *hAllJetCvsL;
  WrappedTH1Triplet *hAllJetPtD;
  WrappedTH1Triplet *hAllJetAxis2;
  WrappedTH1Triplet *hAllJetMult;
  WrappedTH1Triplet *hAllJetBdisc;

  WrappedTH1Triplet *hAllJetQGLikelihood;

  WrappedTH1Triplet *hCJetCvsL;
  WrappedTH1Triplet *hCJetPtD;
  WrappedTH1Triplet *hCJetAxis2;
  WrappedTH1Triplet *hCJetMult;
  WrappedTH1Triplet *hCJetBdisc;

  //Matching check
  WrappedTH1        *hNmatchedTop;
  WrappedTH1        *hNmatchedTrijets;
  WrappedTH1Triplet *hGenTop_Pt;
  WrappedTH1        *hTrijetDrMin;
  WrappedTH1        *hTrijetDPtOverGenPt;
  WrappedTH1        *hTrijetDEtaOverGenEta;
  WrappedTH1        *hTrijetDPhiOverGenPhi;
  WrappedTH1        *hTrijetDPt_matched;
  WrappedTH1        *hTrijetDEta_matched;
  WrappedTH1        *hTrijetDPhi_matched;

  WrappedTH1        *hJetsDeltaRmin;
  WrappedTH1        *hQuarkJetMinDr03_DeltaPtOverPt;
  //Correlations
  WrappedTH2Triplet *hTrijetPtDrVsTrijetMass;
  WrappedTH2Triplet *hTrijetPtDrVsBjetLdgJetMass;
  WrappedTH2Triplet *hDijetPtDrVsDijetMass;
  WrappedTH2Triplet *hDijetPtDrVsTrijetMass;
  WrappedTH2Triplet *hTrijetMassVsBjetLdgJetMass;
  WrappedTH2Triplet *hTrijetMassVsBjetSubldgJetMass;
  WrappedTH2Triplet *hTrijetMassVsDijetMass;


  //next WrappedTH1Triplet

  // TTree - TBranches       
  TTree *treeS;
  TTree *treeB;
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
  //...
  TBranch *TrijetLdgJetCvsL_S;
  TBranch *TrijetSubldgJetCvsL_S;
  TBranch *TrijetLdgJetPtD_S;
  TBranch *TrijetSubldgJetPtD_S;
  TBranch *TrijetLdgJetAxis2_S;
  TBranch *TrijetSubldgJetAxis2_S;
  TBranch *TrijetLdgJetMult_S;
  TBranch *TrijetSubldgJetMult_S;
  TBranch *TrijetLdgJetQGLikelihood_S;
  TBranch *TrijetSubldgJetQGLikelihood_S;

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
  //...
  TBranch *TrijetLdgJetCvsL_B;
  TBranch *TrijetSubldgJetCvsL_B;
  TBranch *TrijetLdgJetPtD_B;
  TBranch *TrijetSubldgJetPtD_B;
  TBranch *TrijetLdgJetAxis2_B;
  TBranch *TrijetSubldgJetAxis2_B;
  TBranch *TrijetLdgJetMult_B;
  TBranch *TrijetSubldgJetMult_B;
  TBranch *TrijetLdgJetQGLikelihood_B;
  TBranch *TrijetSubldgJetQGLikelihood_B;



  //next TBranch

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TopReco);

TopReco::TopReco(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),

    /*cfg_PrelimTopMVACut(config, "FakeBMeasurement.prelimTopMVACut"),
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
    */
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invMassBins")),
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

    //    fTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    //    fTopSelectionBDT(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    
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
  //  fTopSelection.bookHistograms(dir);
  //  fTopSelectionBDT.bookHistograms(dir);

  
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


  /* 
   
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
  */

    // Create directories for normalization                                                                                                                                                
    std::string myInclusiveLabel  = "TrijetCandidate";
    std::string myFakeLabel       = myInclusiveLabel+"Fake";
    std::string myGenuineLabel    = myInclusiveLabel+"Genuine";
    TDirectory* myInclusiveDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
    TDirectory* myFakeDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
    TDirectory* myGenuineDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
    std::vector<TDirectory*> myDirs = {myInclusiveDir, myFakeDir, myGenuineDir};
    
    std::string myInclusiveLabel_2d  = "Scatterplots_";
    std::string myFakeLabel_2d       = myInclusiveLabel_2d+"Fake";
    std::string myGenuineLabel_2d    = myInclusiveLabel_2d+"Genuine";
    TDirectory* myInclusiveDir_2d         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel_2d);
    TDirectory* myFakeDir_2d = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel_2d);
    TDirectory* myGenuineDir_2d = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel_2d);
    std::vector<TDirectory*> myDirs_2d = {myInclusiveDir_2d, myFakeDir_2d, myGenuineDir_2d};

    //Top Reconstruction Variables
  hTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TrijetPt", ";p_{T} (GeV/c)", 2*nBinsPt, minPt , 2*maxPt);
  hTrijetEta          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"TrijetEta", ";|#eta|", nBinsEta/2, minEta, maxEta);
  hTrijetPhi          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"TrijetPhi",";#phi (rads)", nBinsPhi , minPhi , maxPhi );
  hTrijetMass         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"TrijetMass", ";m_{jjb} (GeV/c^{2})",150,0.0,1500);
  hTrijetPtDr         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"TrijetPtDr",";p_{T}#Delta R",150,0.0,1500);
  hDijetPtDr          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"DijetPtDr",";p_{T}#Delta R",150,0.0,1500);
  hDijetMass          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"DijetMass",";m_{W} (GeV/c^{2})",100,0.0,1000);
  hLdgJetBdisc        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"LdgJetBdisc",";b-tag discr",100,0.0,1.0);
  hSubldgJetBdisc     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"SubldgJetBdisc",";b-tag discr",100,0.0,1.0);
  hBJetBdisc          = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"BJetBdisc",";b-tag discr",100,0.0,1.0);
  hBJetMass           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"BJetMass",";m_{b} (GeV/c^{2})", 120,0,120);
  hBJetLdgJet_Mass    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"BJetLdgJet_Mass",";M (GeV/c^{2})",100,0.0,1000);
  hBJetSubldgJet_Mass = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"BJetSubldgJet_Mass",";M (GeV/c^{2})",100,0.0,1000);
  hSoftDrop_n2        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"SoftDrop_n2",";SoftDrop_n2", 50, 0, 2);
  //...
  hLdgJetCvsL     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgJetCvsL",";CvsL discr", 200,-1,1);
  hSubldgJetCvsL  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgJetCvsL",";CvsL discr", 200,-1,1);
  hLdgJetPtD      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgJetPtD",";p_{T}D",100,0.0,1.0);
  hSubldgJetPtD   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgJetPtD",";p_{T}D",100,0.0,1.0);
  hLdgJetAxis2    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgJetAxis2",";axis2",50,0,0.2);
  hSubldgJetAxis2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgJetAxis2",";axis2",50,0.0,0.2);
  hLdgJetMult     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgJetMult",";mult",50,0,50);
  hSubldgJetMult  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgJetMult",";mult",50,0,50);
  hLdgJetQGLikelihood  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgJetQGLikelihood",";Quark-Gluon Likelihood",100,0.0,1.0);
  hSubldgJetQGLikelihood  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgJetQGLikelihood",";Quark-Gluon Likelihood",100,0.0,1.0);


  hBJetCvsL     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "BJetCvsL",";CvsL discr", 200,-1,1);
  hBJetPtD      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "BJetPtD",";p_{T}D",100,0.0,1.0);
  hBJetAxis2    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "BJetAxis2",";axis2",50,0,0.2);
  hBJetMult     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "BJetMult",";mult",50,0,50);

  hCJetCvsL     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CJetCvsL",";CvsL discr", 200,-1,1);
  hCJetPtD      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CJetPtD",";p_{T}D",100,0.0,1.0);
  hCJetAxis2    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CJetAxis2",";axis2",50,0,0.2);
  hCJetMult     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "CJetMult",";mult",50,0,50);
  hCJetBdisc = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"CJetBdisc",";b-tag discr",100,0.0,1.0);

  hAllJetCvsL     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "AllJetCvsL",";CvsL discr", 200,-1,1);
  hAllJetPtD      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "AllJetPtD",";p_{T}D",100,0.0,1.0);
  hAllJetAxis2    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "AllJetAxis2",";axis2",50,0,0.2);
  hAllJetMult     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "AllJetMult",";mult",50,0,50);
  hAllJetBdisc    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"AllJetBdisc",";b-tag discr",100,0.0,1.0);
  hAllJetQGLikelihood  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "AllJetQGLikelihood",";Quark-Gluon Likelihood",100,0.0,1.0);
  //Matching check
  hNmatchedTop     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myInclusiveDir,"NmatchedTrijets",";NTrijet_{matched}",4,-0.5,3.5);
  hNmatchedTrijets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myInclusiveDir,"NmatchedTrijetCand",";NTrijet_{matched}",4,-0.5,3.5);
  hGenTop_Pt       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs,"GenTop_Pt", ";p_{T} (GeV/c)", 2*nBinsPt, minPt , 2*maxPt);

  hTrijetDrMin          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"TrijetDrMin",";#Delta R", 50,0.0,0.5);
  hTrijetDPtOverGenPt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"TrijetDPtOverGenPt","#;Delta P_{T}/P_{T,qqb}", 500,-2.5,2.5);
  hTrijetDEtaOverGenEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myInclusiveDir,"TrijetDEtaOverGenEta",";#Delta #eta/#eta_{qqb}", 200,-1.0,1.0);
  hTrijetDPhiOverGenPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myInclusiveDir,"TrijetDPhiOverGenPhi",";#Delta #phi/#phi_{qqb}", 200,-1.0,1.0);
  hTrijetDPt_matched    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug,myInclusiveDir,"TrijetDPt_matched",";#Delta P_{T}", 2*nBinsPt, -maxPt , maxPt);
  hTrijetDEta_matched   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"TrijetDEta_matched",";#Delta #eta", 80,-0.4,0.4);
  hTrijetDPhi_matched   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"TrijetDPhi_matched",";#Delta #phi", 80,-0.4,0.4);
  hQuarkJetMinDr03_DeltaPtOverPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"QuarkJetMinDr03_DeltaPtOverPt","#;Delta P_{T}(jet-quark)/P_{T,q}", 500,-2.5,2.5);
  //Correlation plots
  hTrijetPtDrVsTrijetMass        = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"TrijetPtDrVsTrijetMass", ";p_{T}#Delta R_{T};m_{jjb}",100,0.0,1000,  100,0.0,1000);
  hTrijetPtDrVsBjetLdgJetMass    = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"TrijetPtDrVsBjetLdgJetMass",";p_{T}#Delta R_{T};m_{b+ldgJet}",100,0.0,1000, 100,0.0,1000);
  hDijetPtDrVsDijetMass          = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"DijetPtDrVsDijetMass",";p_{T}#Delta R_{W};m_{W}", 100,0.0,1000, 100,0.0,1000);
  hDijetPtDrVsTrijetMass         = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"DijetPtDrVsTrijetMass",";p_{T}#Delta R_{W};m_{jjb}", 100,0.0,1000, 100,0.0,1000);
  hTrijetMassVsBjetLdgJetMass    = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"TrijetMassVsBjetLdgJetMass",";m_{jjb};m_{b+ldgJet}" ,100,0.0,1000, 100,0.0,1000);
  hTrijetMassVsBjetSubldgJetMass = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"TrijetMassVsBjetSubldgJetMass",";m_{jjb};m_{b+subldgJet}" ,100,0.0,1000, 100,0.0,1000);
  hTrijetMassVsDijetMass         = fHistoWrapper.makeTHTriplet<TH2F>(true, HistoLevel::kVital, myDirs_2d,"TrijetMassVsDijetMass",";m_{jjb};m_{W}", 100,0.0,1000, 100,0.0,1000);

  hJetsDeltaRmin =   fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital,myInclusiveDir,"JetsDeltaRmin",";#Delta R", 50,0.0,0.5);
  // TTree
  treeS = new TTree("treeS", "TTree");
  treeB = new TTree("treeB", "TTree");

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
  //...
  TrijetLdgJetCvsL_S       = treeS -> Branch ("TrijetLdgJetCvsL",         &TrijetLdgJetCvsL_S,       "TrijetLdgJetCvsL_S/F"        );
  TrijetSubldgJetCvsL_S    = treeS -> Branch ("TrijetSubldgJetCvsL",      &TrijetSubldgJetCvsL_S,     "TrijetSubldgJetCvsL_S/F"    );
  TrijetLdgJetPtD_S        = treeS -> Branch ("TrijetLdgJetPtD",          &TrijetLdgJetPtD_S,        "TrijetLdgJetPtD_S/F"         );
  TrijetSubldgJetPtD_S     = treeS -> Branch ("TrijetSubldgJetPtD",       &TrijetSubldgJetPtD_S,     "TrijetSubldgJetPtD_S/F"      );
  TrijetLdgJetAxis2_S      = treeS -> Branch ("TrijetLdgJetAxis2",        &TrijetLdgJetAxis2_S,      "TrijetLdgJetAxis2_S/F"       );
  TrijetSubldgJetAxis2_S   = treeS -> Branch ("TrijetSubldgJetAxis2",     &TrijetSubldgJetAxis2_S,   "TrijetSubldgJetAxis2_S/F"    );
  TrijetLdgJetMult_S       = treeS -> Branch ("TrijetLdgJetMult",         &TrijetLdgJetMult_S,       "TrijetLdgJetMult_S/I"        );
  TrijetSubldgJetMult_S    = treeS -> Branch ("TrijetSubldgJetMult",      &TrijetSubldgJetMult_S,    "TrijetSubldgJetMult_S/I"     );

  TrijetLdgJetQGLikelihood_S    = treeS -> Branch ("TrijetLdgJetQGLikelihood",&TrijetLdgJetQGLikelihood_S, "TrijetLdgJetQGLikelihood_S/F");
  TrijetSubldgJetQGLikelihood_S    = treeS -> Branch ("TrijetSubldgJetQGLikelihood",&TrijetSubldgJetQGLikelihood_S, "TrijetSubldgJetQGLikelihood_S/F");

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
  //...
  TrijetLdgJetCvsL_B       = treeB -> Branch ("TrijetLdgJetCvsL",         &TrijetLdgJetCvsL_B,       "TrijetLdgJetCvsL_B/F"        );
  TrijetSubldgJetCvsL_B    = treeB -> Branch ("TrijetSubldgJetCvsL",      &TrijetSubldgJetCvsL_B,     "TrijetSubldgJetCvsL_B/F"      );
  TrijetLdgJetPtD_B        = treeB -> Branch ("TrijetLdgJetPtD",          &TrijetLdgJetPtD_B,        "TrijetLdgJetPtD_B/F"         );
  TrijetSubldgJetPtD_B     = treeB -> Branch ("TrijetSubldgJetPtD",       &TrijetSubldgJetPtD_B,     "TrijetSubldgJetPtD_B/F"      );
  TrijetLdgJetAxis2_B      = treeB -> Branch ("TrijetLdgJetAxis2",        &TrijetLdgJetAxis2_B,      "TrijetLdgJetAxis2_B/F"       );
  TrijetSubldgJetAxis2_B   = treeB -> Branch ("TrijetSubldgJetAxis2",     &TrijetSubldgJetAxis2_B,   "TrijetSubldgJetAxis2_B/F"    );
  TrijetLdgJetMult_B       = treeB -> Branch ("TrijetLdgJetMult",         &TrijetLdgJetMult_B,       "TrijetLdgJetMult_B/I"        );
  TrijetSubldgJetMult_B    = treeB -> Branch ("TrijetSubldgJetMult",      &TrijetSubldgJetMult_B,    "TrijetSubldgJetMult_B/I"     );

  TrijetLdgJetQGLikelihood_B    = treeB -> Branch ("TrijetLdgJetQGLikelihood",&TrijetLdgJetQGLikelihood_B, "TrijetLdgJetQGLikelihood_B/F");
  TrijetSubldgJetQGLikelihood_B    = treeB -> Branch ("TrijetSubldgJetQGLikelihood",&TrijetSubldgJetQGLikelihood_B, "TrijetSubldgJetQGLikelihood_B/F");


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



Jet TopReco::getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet){
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
  for (size_t i=0; i<gen_particle.daughters().size(); i++){
    
    genParticle genDau = fEvent.genparticles().getGenParticles()[gen_particle.daughters().at(i)];
    int genDau_index   = genDau.index();
    int genDau_pdgId   = genDau.pdgId();
    if (gen_pdgId == genDau_pdgId) return findLastCopy(genDau_index);
  }
  return gen_particle;
}


bool TopReco::isWsubjet(const Jet& jet , const std::vector<Jet>& jets1 , const std::vector<Jet>& jets2){
  return  (isMatchedJet(jet,jets1)||isMatchedJet(jet,jets2));
}



  
bool TopReco::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool TopReco::isMatchedJet(const Jet& jet, const std::vector<Jet>& jets) {
  for (auto Jet: jets)
    {
      if (areSameJets(jet, Jet)) return true;
    }
  return false;
}

bool TopReco::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
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
  // if (0){ //soti removed topSelection
  //   if(0) std::cout << "=== Top selection" << std::endl;
  //  const TopSelection::Data TopData = fTopSelection.analyze(fEvent, jetData, bjetData);
  //   if (!TopData.passedSelection()) return;
  // }


  //================================================================================================                            
  // 14) Top BDT selection                                                                                                     
  //================================================================================================                                                              
  //  if (0) std::cout << "=== Top BDT selection" << std::endl;
  // const TopSelectionBDT::Data topBDTData = fTopSelectionBDT.analyze(fEvent, jetData, bjetData);


  //================================================================================================
  // All cuts passed
  //================================================================================================
  if(0) std::cout << "=== All cuts passed" << std::endl;
  cSelected.increment();



  // Define the addresses of the variables which will be added to the TTree
  float eventWeight_S;

  float trijetPtDR_S, trijetDijetPtDR_S, trijetBjetMass_S, trijetLdgJetPt_S, trijetLdgJetEta_S, trijetLdgJetBDisc_S, trijetSubldgJetPt_S, trijetSubldgJetEta_S, trijetSubldgJetBDisc_S, trijetBJetLdgJetMass_S, trijetBJetSubldgJetMass_S, trijetDijetMass_S, trijetBJetBDisc_S, trijetMass_S,trijetSoftDrop_n2_S;

  float trijetLdgJetCvsL_S, trijetSubldgJetCvsL_S, trijetLdgJetPtD_S, trijetSubldgJetPtD_S, trijetLdgJetAxis2_S, trijetSubldgJetAxis2_S;
  int trijetLdgJetMult_S, trijetSubldgJetMult_S;
  float trijetLdgJetQGLikelihood_S, trijetSubldgJetQGLikelihood_S;

  float eventWeight_B;

  float trijetPtDR_B, trijetDijetPtDR_B, trijetBjetMass_B, trijetLdgJetPt_B, trijetLdgJetEta_B, trijetLdgJetBDisc_B, trijetSubldgJetPt_B, trijetSubldgJetEta_B, trijetSubldgJetBDisc_B, trijetBJetLdgJetMass_B, trijetBJetSubldgJetMass_B, trijetDijetMass_B, trijetBJetBDisc_B, trijetMass_B, trijetSoftDrop_n2_B;

  float trijetLdgJetCvsL_B, trijetSubldgJetCvsL_B, trijetLdgJetPtD_B, trijetSubldgJetPtD_B, trijetLdgJetAxis2_B, trijetSubldgJetAxis2_B;
  int trijetLdgJetMult_B, trijetSubldgJetMult_B;
  float trijetLdgJetQGLikelihood_B, trijetSubldgJetQGLikelihood_B;

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
  //...
  TrijetLdgJetCvsL_S           -> SetAddress(&trijetLdgJetCvsL_S);
  TrijetSubldgJetCvsL_S        -> SetAddress(&trijetSubldgJetCvsL_S);
  TrijetLdgJetPtD_S            -> SetAddress(&trijetLdgJetPtD_S);
  TrijetSubldgJetPtD_S         -> SetAddress(&trijetSubldgJetPtD_S);
  TrijetLdgJetAxis2_S          -> SetAddress(&trijetLdgJetAxis2_S);
  TrijetSubldgJetAxis2_S       -> SetAddress(&trijetSubldgJetAxis2_S);
  TrijetLdgJetMult_S           -> SetAddress(&trijetLdgJetMult_S);
  TrijetSubldgJetMult_S        -> SetAddress(&trijetSubldgJetMult_S);

  TrijetLdgJetQGLikelihood_S   -> SetAddress(&trijetLdgJetQGLikelihood_S);
  TrijetSubldgJetQGLikelihood_S-> SetAddress(&trijetSubldgJetQGLikelihood_S);

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
  //...
  TrijetLdgJetCvsL_B           -> SetAddress(&trijetLdgJetCvsL_B);
  TrijetSubldgJetCvsL_B        -> SetAddress(&trijetSubldgJetCvsL_B);
  TrijetLdgJetPtD_B            -> SetAddress(&trijetLdgJetPtD_B);
  TrijetSubldgJetPtD_B         -> SetAddress(&trijetSubldgJetPtD_B);
  TrijetLdgJetAxis2_B          -> SetAddress(&trijetLdgJetAxis2_B);
  TrijetSubldgJetAxis2_B       -> SetAddress(&trijetSubldgJetAxis2_B);
  TrijetLdgJetMult_B           -> SetAddress(&trijetLdgJetMult_B);
  TrijetSubldgJetMult_B        -> SetAddress(&trijetSubldgJetMult_B);

  TrijetLdgJetQGLikelihood_B   -> SetAddress(&trijetLdgJetQGLikelihood_B);
  TrijetSubldgJetQGLikelihood_B-> SetAddress(&trijetSubldgJetQGLikelihood_B);

  //next address


  //================================================================================================//
  //                            Gen Trijet subjets selection                                        //
  //================================================================================================//

  //START
  const double twoSigma = 0.32;
  const double dRcut    = 0.3;
  if (fEvent.isMC()){

    vector<genParticle> GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
    vector<genParticle> GenTops_BQuark;
    vector<genParticle> GenTops_LdgQuark;
    vector<genParticle> GenTops_SubldgQuark;
    vector<genParticle> GenTops_Quarks;

    for (auto& top: GenTops){
      //Reject boosted top
      //      if (top.pt() > 500) return;
      vector<genParticle> quarks;
      genParticle bquark;
      bool foundB = false;      
      for (size_t i=0; i<top.daughters().size(); i++){
        int dau_index = top.daughters().at(i);
        genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
        // B-Quark                                                                                                                                                                       
        if (std::abs(dau.pdgId()) ==  5){
	  bquark = dau;
	  foundB = true;
	}
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
      if (!(quarks.size() == 2 && foundB)) return;
      // Fill vectors for b-quarks, leading and subleading quarks coming from tops                                                                                 
      GenTops_BQuark.push_back(bquark);

      GenTops_Quarks.push_back(bquark);
      GenTops_Quarks.push_back(quarks.at(0));
      GenTops_Quarks.push_back(quarks.at(1));
      
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
    
    
    //Pseudo-matching: Used to calculate the dPt/Pt cut
    for (size_t i=0; i<GenTops.size(); i++)
      {
	genParticle Quark      = GenTops_Quarks.at(i);
	Jet JetClosest;
	double dRmin  = 99999.9;
	for (auto& jet: jetData.getSelectedJets())
	  {
	    double dR  = ROOT::Math::VectorUtil::DeltaR( jet.p4(), Quark.p4());
	    if (dR > 0.3)     continue;
	    if (dR > dRmin)   continue;
	    dRmin  = dR;
	    JetClosest = jet;
	  }
	if (dRmin > 0.3) continue;
	double dPtOverPt = (JetClosest.pt() - Quark.pt())/Quark.pt();
	hQuarkJetMinDr03_DeltaPtOverPt -> Fill (dPtOverPt);   //2sigma = 2*0.16 = 0.32
      }

    //========================================================================================================
    //                              Matching:  Minimum DeltaR and DeltaPt check
    //========================================================================================================

    //Sanity chack
    double DeltaR_min = 999.999;
    for (auto& jet1: jetData.getSelectedJets())
      {
	for (auto& jet2: jetData.getSelectedJets())
	  {
	    if (areSameJets(jet1, jet2)) continue;
	    double DeltaR = ROOT::Math::VectorUtil::DeltaR( jet1.p4(), jet2.p4());
	    if (DeltaR > DeltaR_min) continue;
	    DeltaR_min = DeltaR;
	  }
      }
    
    hJetsDeltaRmin -> Fill(DeltaR_min);

      //======= B jet matching (Loop over all Jets)

    int imatched =0;
    vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet;
    vector <Jet> MC_LdgJet, MC_SubldgJet, MC_Bjet;
    vector <Jet> BJetCand, MC_Jets;
    vector <genParticle> MGen_LdgJet, MGen_SubldgJet, MGen_Bjet;
    vector <double> dRminB;
    Jet firstBjet;
    for (size_t i=0; i<GenTops.size(); i++){
      genParticle BQuark      = GenTops_BQuark.at(i);
      Jet mcMatched_BJet;
      double dRmin  = 99999.9;
      // double dPtOverPtmin = 99999.9;
      for (auto& bjet: jetData.getSelectedJets()){
	double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
	double dPtOverPt = std::abs((bjet.pt() - BQuark.pt())/BQuark.pt());
	if (dR > dRcut)     continue;
	if (dR > dRmin)   continue;
	//if (dPtOverPt > dPtOverPtmin) continue;
	if (dPtOverPt > twoSigma) continue;
	dRmin  = dR;
	// dPtOverPtmin = dPtOverPt;
	mcMatched_BJet = bjet;
      }
      dRminB.push_back(dRmin);
      BJetCand.push_back(mcMatched_BJet);
    }

    //======= Dijet matching (Loop over all Jets)

    for (size_t i=0; i<GenTops.size(); i++){
      genParticle LdgQuark    = GenTops_LdgQuark.at(i);
      genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
      
      Jet mcMatched_LdgJet;
      Jet mcMatched_SubldgJet;
      
      double dR1min, dR2min, dPtOverPt1min, dPtOverPt2min;
      dR1min = dR2min = dPtOverPt1min = dPtOverPt2min = 99999.9;

      for (auto& jet: jetData.getSelectedJets()){
	bool same = false;
	for (size_t k=0; k<GenTops.size(); k++){
	  if (dRminB.at(k) <= dRcut){
	    if( areSameJets(jet,BJetCand.at(k))) same = true; //Skip the jets that are matched with bquarks
	  }
	}
	if (same) continue;
	double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
	double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
	
	if (std::min(dR1, dR2) > dRcut) continue;
	
	double dPtOverPt1 = std::abs((jet.pt() - LdgQuark.pt())/LdgQuark.pt());
	double dPtOverPt2 = std::abs( (jet.pt() - SubldgQuark.pt())/SubldgQuark.pt());

	if (dR1 < dR2)
	  {
	    if (dR1 < dR1min)
	      {
		//if(dPtOverPt1 < dPtOverPt1min)
		if(dPtOverPt1 < twoSigma)
		  {
		    dR1min = dR1;
		    dPtOverPt1min= dPtOverPt1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	    else if (dR2 <= dRcut && dR2 < dR2min)
	      {
		//if (dPtOverPt2 < dPtOverPt2min)
		if (dPtOverPt2 < twoSigma)
		  {
		    dR2min  = dR2;
		    dPtOverPt2min = dPtOverPt2;
		    mcMatched_SubldgJet = jet;
		  }
	      }
	  }
	else
	  {
	    if (dR2 < dR2min)
	      {
		//if(dPtOverPt2 < dPtOverPt2min)
		if(dPtOverPt2 < twoSigma)
		  {
		    dR2min  = dR2;
		    dPtOverPt2min = dPtOverPt2;
		    mcMatched_SubldgJet = jet;
		  }
	      }
	    else if (dR1 <= dRcut && dR1 < dR1min)
	      {
		//if (dPtOverPt1 < dPtOverPt1min)
		if (dPtOverPt1 < twoSigma)
		  {
		    dR1min  = dR1;
		    dPtOverPt1min = dPtOverPt1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	  }   
      }
      //Genuine if all the top quarks are matched
      genParticle top = GenTops.at(i);
      bool genuine = (dR1min<= dRcut && dR2min <= dRcut && dRminB.at(i) <= dRcut);
      if (genuine){
	imatched ++;
	hGenTop_Pt->Fill(true, top.pt());
	MCtrue_LdgJet.push_back(mcMatched_LdgJet);
	MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
	MCtrue_Bjet.push_back(BJetCand.at(i));
	
	MC_Jets.push_back(mcMatched_LdgJet);
	MC_Jets.push_back(mcMatched_SubldgJet);
	MC_Jets.push_back(BJetCand.at(i));

	MGen_LdgJet.push_back(GenTops_LdgQuark.at(i));
	MGen_SubldgJet.push_back(GenTops_SubldgQuark.at(i));
	MGen_Bjet.push_back(GenTops_BQuark.at(i));
      }
      else {
	hGenTop_Pt->Fill(false, top.pt());
      }
    }
    hNmatchedTop ->Fill(imatched);
    
    
    size_t nTops = GenTops_BQuark.size();
    for (size_t i=0; i<nTops; i++)
      {
	double dR12 = ROOT::Math::VectorUtil::DeltaR(GenTops_LdgQuark.at(i).p4(), GenTops_SubldgQuark.at(i).p4());
	double dR1b = ROOT::Math::VectorUtil::DeltaR(GenTops_LdgQuark.at(i).p4(), GenTops_BQuark.at(i).p4());
	double dR2b = ROOT::Math::VectorUtil::DeltaR(GenTops_SubldgQuark.at(i).p4(), GenTops_BQuark.at(i).p4());
	//	std::cout<<dR12<<" "<<dR1b<<" "<<dR12<<std::endl;
	double dRmin = min(min(dR12, dR1b), dR2b);
	if (dRmin < 0.8) return;
	//	std::cout<<dR12<<" "<<dR1b<<" "<<dR12<<std::endl;
      }
    //================================================================================================//                      
    //                                    Top Candidates                                              //
    //================================================================================================//
    TrijetSelections TopCandidates;
    int index0 = -1;
    for (auto& jet0: jetData.getSelectedJets()){
      index0++;
      int index1 = -1;
      for (auto& jet1: jetData.getSelectedJets()){
	index1++;
	if (index1 < index0) continue;
	if (areSameJets(jet1, jet0)) continue;
	int index2 = -1;
	for (auto& jet2: jetData.getSelectedJets()){
	  index2++;
	  if (index2 < index1) continue;
	  if (areSameJets(jet2,  jet1)) continue;
	  if (areSameJets(jet2,  jet0)) continue;
	  

	  //********************************** Bjet Matched OR dijet matched*********************************//
	  //	  if ( isBJet(jet0, MCtrue_Bjet)    ||    ((isMatchedJet(jet1,MCtrue_LdgJet)||isMatchedJet(jet1,MCtrue_SubldgJet))  &&  (isMatchedJet(jet2,MCtrue_LdgJet)||isMatchedJet(jet2,MCtrue_SubldgJet)))  ){
	  if ( isBJet(jet0, MCtrue_Bjet)    ||    (isWsubjet(jet1,MCtrue_LdgJet, MCtrue_SubldgJet)  &&  isWsubjet(jet2,MCtrue_LdgJet, MCtrue_SubldgJet))){
	    TopCandidates.BJet.push_back(jet0);
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));
	  }
	  
	  else if ( isBJet(jet1, MCtrue_Bjet)    ||  (isWsubjet(jet0,MCtrue_LdgJet, MCtrue_SubldgJet)  &&  isWsubjet(jet2,MCtrue_LdgJet, MCtrue_SubldgJet))){
	    TopCandidates.BJet.push_back(jet1);
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet2,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet2,"subleading"));

	  }
	  else if ( isBJet(jet2, MCtrue_Bjet)    ||  (isWsubjet(jet0,MCtrue_LdgJet, MCtrue_SubldgJet)  &&  isWsubjet(jet1,MCtrue_LdgJet, MCtrue_SubldgJet))){
	    TopCandidates.BJet.push_back(jet2);
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet1,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet1,"subleading"));
	  }
	  
	  //********************************** One of the dijet subjets matched*********************************//
	  //	  else if (isMatchedJet(jet0,MCtrue_LdgJet)||isMatchedJet(jet0,MCtrue_SubldgJet)){  //jet0 belongs to dijet

	  else if (isWsubjet(jet0,MCtrue_LdgJet, MCtrue_SubldgJet)){

	    if (jet1.bjetDiscriminator() > jet2.bjetDiscriminator()){
	      TopCandidates.BJet.push_back(jet1);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet2,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet2,"subleading"));
	    }
	    else{
	      TopCandidates.BJet.push_back(jet2);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet1,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet1,"subleading"));
            }
	  }
	  else if (isWsubjet(jet1,MCtrue_LdgJet, MCtrue_SubldgJet)){

            if (jet0.bjetDiscriminator() > jet2.bjetDiscriminator()){
	      TopCandidates.BJet.push_back(jet0);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));
            }
            else{
	      TopCandidates.BJet.push_back(jet2);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet1,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet1,"subleading"));
            }
          }
	  else if (isWsubjet(jet2,MCtrue_LdgJet, MCtrue_SubldgJet)){

            if (jet0.bjetDiscriminator() > jet1.bjetDiscriminator()){
	      TopCandidates.BJet.push_back(jet0);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));
            }
            else{
	      TopCandidates.BJet.push_back(jet1);
	      TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet2,"leading"));
	      TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet2,"subleading"));
            }
          }

	  
	  
	  
	  //********************** Non of the three subjets is matched************************//
	  
	  else if (jet0.bjetDiscriminator() > jet1.bjetDiscriminator() && jet0.bjetDiscriminator() > jet2.bjetDiscriminator()){            
	    TopCandidates.BJet.push_back(jet0);
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet1,jet2,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet1,jet2,"subleading"));	    
	  }
	  else if (jet1.bjetDiscriminator() > jet0.bjetDiscriminator() && jet1.bjetDiscriminator() > jet2.bjetDiscriminator()){
	    TopCandidates.BJet.push_back(jet1);	    
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet2,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet2,"subleading"));
	  }
	  else if (jet2.bjetDiscriminator() > jet0.bjetDiscriminator() && jet2.bjetDiscriminator() > jet1.bjetDiscriminator()){
	    TopCandidates.BJet.push_back(jet2);
	    TopCandidates.Jet1.push_back(getLeadingSubleadingJet(jet0,jet1,"leading"));
	    TopCandidates.Jet2.push_back(getLeadingSubleadingJet(jet0,jet1,"subleading"));
	  }
	}	  	 	  
      }
    }
    
    
    
    
  
    //========================================================================================================
    //                       Identification of fake, genuine TopCandidates
    //========================================================================================================
    vector <bool> GenuineTop; 
    int jmatched = 0;
    //    std::cout<<"==="<<std::endl;
    for (size_t i=0; i<TopCandidates.BJet.size(); i++){
      bool genuine = false;
      for (size_t j=0; j<MCtrue_Bjet.size(); j++){
	bool same1 = areSameJets(TopCandidates.Jet1.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCandidates.Jet2.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCandidates.BJet.at(i),  MCtrue_Bjet.at(j));
	bool same2 = areSameJets(TopCandidates.Jet1.at(i), MCtrue_SubldgJet.at(j)) && areSameJets(TopCandidates.Jet2.at(i), MCtrue_LdgJet.at(j))    && areSameJets(TopCandidates.BJet.at(i),  MCtrue_Bjet.at(j));
	//	std::cout<<"genuine "<<genuine<<std::endl;
	if (same1 || same2){
	  genuine = true;
	  //	  std::cout<<"genuine "<<genuine<<std::endl;
	  //	  continue;
	}
      }
      if (genuine) jmatched++;
      GenuineTop.push_back(genuine);
    }
    hNmatchedTrijets ->Fill(jmatched);
    //    std::cout<<"trijet cand/Matched trijets "<<TopCandidates.BJet.size()<<" "<<MCtrue_Bjet.size()<<" jmatched "<<jmatched<<std::endl;

    //========================================================================================================
    //                           Check Properties of matched objects //Improve me! 
    //========================================================================================================
    for (size_t j=0; j<MCtrue_Bjet.size(); j++){

      hTrijetDrMin -> Fill( ROOT::Math::VectorUtil::DeltaR(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4()));
      hTrijetDrMin -> Fill( ROOT::Math::VectorUtil::DeltaR(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4()));
      hTrijetDrMin -> Fill( ROOT::Math::VectorUtil::DeltaR(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4()));
      
      hTrijetDPtOverGenPt -> Fill( (MCtrue_Bjet.at(j).pt() - MGen_Bjet.at(j).pt())/MGen_Bjet.at(j).pt());
      hTrijetDPtOverGenPt -> Fill( (MCtrue_LdgJet.at(j).pt() - MGen_LdgJet.at(j).pt())/MGen_LdgJet.at(j).pt());
      hTrijetDPtOverGenPt -> Fill( (MCtrue_SubldgJet.at(j).pt() - MGen_SubldgJet.at(j).pt())/MGen_SubldgJet.at(j).pt());
      
      hTrijetDPt_matched -> Fill( (MCtrue_Bjet.at(j).pt() - MGen_Bjet.at(j).pt()));
      hTrijetDPt_matched -> Fill( (MCtrue_LdgJet.at(j).pt() - MGen_LdgJet.at(j).pt()));
      hTrijetDPt_matched -> Fill( (MCtrue_SubldgJet.at(j).pt() - MGen_SubldgJet.at(j).pt()));
      
      hTrijetDEtaOverGenEta -> Fill( (MCtrue_Bjet.at(j).eta() - MGen_Bjet.at(j).eta())/MGen_Bjet.at(j).eta());
      hTrijetDEtaOverGenEta -> Fill( (MCtrue_LdgJet.at(j).eta() - MGen_LdgJet.at(j).eta())/MGen_LdgJet.at(j).eta());
      hTrijetDEtaOverGenEta -> Fill( (MCtrue_SubldgJet.at(j).eta() - MGen_SubldgJet.at(j).eta())/MGen_SubldgJet.at(j).eta());
      
      hTrijetDEta_matched -> Fill( (MCtrue_Bjet.at(j).eta() - MGen_Bjet.at(j).eta()));
      hTrijetDEta_matched -> Fill( (MCtrue_LdgJet.at(j).eta() - MGen_LdgJet.at(j).eta()));
      hTrijetDEta_matched -> Fill( (MCtrue_SubldgJet.at(j).eta() - MGen_SubldgJet.at(j).eta()));
      
      hTrijetDPhiOverGenPhi -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4()))/MGen_Bjet.at(j).phi());
      hTrijetDPhiOverGenPhi -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4()))/MGen_LdgJet.at(j).phi());
      hTrijetDPhiOverGenPhi -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4()))/MGen_SubldgJet.at(j).phi());
      
      hTrijetDPhi_matched -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_Bjet.at(j).p4(),MGen_Bjet.at(j).p4())));
      hTrijetDPhi_matched -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_LdgJet.at(j).p4(),MGen_LdgJet.at(j).p4())));
      hTrijetDPhi_matched -> Fill( (ROOT::Math::VectorUtil::DeltaPhi(MCtrue_SubldgJet.at(j).p4(),MGen_SubldgJet.at(j).p4())));
      
    }
    

    
    //========================================================================================================
    //                                 Fill Triplets and trees
    //========================================================================================================
    
    
    
    Bool_t isGenuineTop = false;

    for (size_t i=0; i<TopCandidates.BJet.size(); i++){
      math::XYZTLorentzVector trijetp4, dijetp4;                                                                                                                              
      trijetp4 = TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()+TopCandidates.Jet2.at(i).p4();
      dijetp4 = TopCandidates.Jet1.at(i).p4()+TopCandidates.Jet2.at(i).p4();
      TopCandidates.TrijetP4.push_back(trijetp4);                                                                                                                                      
      TopCandidates.DijetP4.push_back(dijetp4);                                                                                                                                        

      isGenuineTop = GenuineTop.at(i);
      
      hTrijetPt           -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Pt());
      hTrijetEta          -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Eta());
      hTrijetPhi          -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Phi());
      
      hTrijetMass         -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).M());
      hDijetPtDr          -> Fill(isGenuineTop, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()));
      hTrijetPtDr         -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()));
      hDijetMass          -> Fill(isGenuineTop, TopCandidates.DijetP4.at(i).M());
      hLdgJetBdisc        -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).bjetDiscriminator());
      hSubldgJetBdisc     -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).bjetDiscriminator());
      hBJetBdisc          -> Fill(isGenuineTop, TopCandidates.BJet.at(i).bjetDiscriminator());
      hBJetMass           -> Fill(isGenuineTop, TopCandidates.BJet.at(i).p4().M());
      hBJetLdgJet_Mass    -> Fill(isGenuineTop, (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hBJetSubldgJet_Mass -> Fill(isGenuineTop, (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M());

      double dr_sd       = ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
      double softDrop_n2 = min(TopCandidates.Jet2.at(i).pt(), TopCandidates.Jet1.at(i).pt())/( (TopCandidates.Jet2.at(i).pt() + TopCandidates.Jet1.at(i).pt() )*dr_sd*dr_sd);
      hSoftDrop_n2        -> Fill(isGenuineTop, softDrop_n2);
      
      hLdgJetCvsL         -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).pfCombinedCvsLJetTags());
      hSubldgJetCvsL      -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).pfCombinedCvsLJetTags());
      hLdgJetPtD          -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSptD());
      hSubldgJetPtD       -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSptD());
      hLdgJetAxis2        -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSaxis2());
      hSubldgJetAxis2     -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSaxis2());
      hLdgJetMult         -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSmult());
      hSubldgJetMult      -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSmult());

      hLdgJetQGLikelihood    -> Fill(isGenuineTop, TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSqgLikelihood());
      hSubldgJetQGLikelihood -> Fill(isGenuineTop, TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSqgLikelihood());

      hBJetCvsL           -> Fill(isGenuineTop, TopCandidates.BJet.at(i).pfCombinedCvsLJetTags());
      hBJetPtD            -> Fill(isGenuineTop, TopCandidates.BJet.at(i).QGTaggerAK4PFCHSptD());
      hBJetAxis2          -> Fill(isGenuineTop, TopCandidates.BJet.at(i).QGTaggerAK4PFCHSaxis2());
      hBJetMult           -> Fill(isGenuineTop, TopCandidates.BJet.at(i).QGTaggerAK4PFCHSmult());
      
      hTrijetPtDrVsTrijetMass        -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()),TopCandidates.TrijetP4.at(i).M());
      hTrijetPtDrVsBjetLdgJetMass    -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4()),(TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hDijetPtDrVsDijetMass          -> Fill(isGenuineTop, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()), TopCandidates.DijetP4.at(i).M()); 
      hDijetPtDrVsTrijetMass         -> Fill(isGenuineTop, TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4()), TopCandidates.TrijetP4.at(i).M()); 
      hTrijetMassVsBjetLdgJetMass    -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).M(), (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M());
      hTrijetMassVsBjetSubldgJetMass -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).M(),(TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M());
      hTrijetMassVsDijetMass         -> Fill(isGenuineTop, TopCandidates.TrijetP4.at(i).M(), TopCandidates.DijetP4.at(i).M());
      
      
      if (isGenuineTop){
	eventWeight_S             = fEventWeight.getWeight();
	trijetMass_S              = TopCandidates.TrijetP4.at(i).M();
	trijetDijetPtDR_S         = TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
	trijetPtDR_S              = TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4());
	trijetDijetMass_S         = TopCandidates.DijetP4.at(i).M();
	trijetLdgJetBDisc_S       = TopCandidates.Jet1.at(i).bjetDiscriminator();
	if (trijetLdgJetBDisc_S < 0 )    trijetLdgJetBDisc_S =-1.;
	trijetSubldgJetBDisc_S    =  TopCandidates.Jet2.at(i).bjetDiscriminator();
	if (trijetSubldgJetBDisc_S < 0 ) trijetSubldgJetBDisc_S =-1.;
	trijetBJetBDisc_S         = TopCandidates.BJet.at(i).bjetDiscriminator();
	trijetBjetMass_S          = TopCandidates.BJet.at(i).p4().M();
	trijetBJetLdgJetMass_S    = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M();
	trijetBJetSubldgJetMass_S = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M();
	trijetSoftDrop_n2_S       = softDrop_n2;

	trijetLdgJetCvsL_S        = TopCandidates.Jet1.at(i).pfCombinedCvsLJetTags();
	trijetSubldgJetCvsL_S     = TopCandidates.Jet2.at(i).pfCombinedCvsLJetTags();
	trijetLdgJetPtD_S         = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSptD();
	trijetSubldgJetPtD_S      = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSptD();
	trijetLdgJetAxis2_S       = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSaxis2();
	trijetSubldgJetAxis2_S    = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSaxis2();
	trijetLdgJetMult_S        = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSmult();
	trijetSubldgJetMult_S     = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSmult();

	trijetLdgJetQGLikelihood_S        = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSqgLikelihood();
	trijetSubldgJetQGLikelihood_S     = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSqgLikelihood();
      
      
	treeS -> Fill();
	
      }
      else{
	eventWeight_B             = fEventWeight.getWeight();
	trijetMass_B              = TopCandidates.TrijetP4.at(i).M();
	trijetDijetPtDR_B         = TopCandidates.DijetP4.at(i).Pt() * ROOT::Math::VectorUtil::DeltaR(TopCandidates.Jet1.at(i).p4(),TopCandidates.Jet2.at(i).p4());
	trijetPtDR_B              = TopCandidates.TrijetP4.at(i).Pt()* ROOT::Math::VectorUtil::DeltaR(TopCandidates.DijetP4.at(i),TopCandidates.BJet.at(i).p4());
	trijetDijetMass_B         = TopCandidates.DijetP4.at(i).M();
	trijetLdgJetBDisc_B       = TopCandidates.Jet1.at(i).bjetDiscriminator();
	if (trijetLdgJetBDisc_B < 0 )    trijetLdgJetBDisc_B =-1.;
	trijetSubldgJetBDisc_B    = TopCandidates.Jet2.at(i).bjetDiscriminator();
	if (trijetSubldgJetBDisc_B < 0 ) trijetSubldgJetBDisc_B =-1.;
	trijetBJetBDisc_B         = TopCandidates.BJet.at(i).bjetDiscriminator();
	trijetBjetMass_B          = TopCandidates.BJet.at(i).p4().M();
	trijetBJetLdgJetMass_B    = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet1.at(i).p4()).M();
	trijetBJetSubldgJetMass_B = (TopCandidates.BJet.at(i).p4()+TopCandidates.Jet2.at(i).p4()).M();
	trijetSoftDrop_n2_B       = softDrop_n2;

	trijetLdgJetCvsL_B        = TopCandidates.Jet1.at(i).pfCombinedCvsLJetTags();
	trijetSubldgJetCvsL_B     = TopCandidates.Jet2.at(i).pfCombinedCvsLJetTags();
	trijetLdgJetPtD_B         = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSptD();
	trijetSubldgJetPtD_B      = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSptD();
	trijetLdgJetAxis2_B       = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSaxis2();
	trijetSubldgJetAxis2_B    = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSaxis2();
	trijetLdgJetMult_B        = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSmult();
	trijetSubldgJetMult_B     = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSmult();

	trijetLdgJetQGLikelihood_B        = TopCandidates.Jet1.at(i).QGTaggerAK4PFCHSqgLikelihood();
	trijetSubldgJetQGLikelihood_B     = TopCandidates.Jet2.at(i).QGTaggerAK4PFCHSqgLikelihood();
	
	treeB -> Fill();
	
      }
            
    }
    //next fill histo

    //*******************************************************************************************************
    //                                   TOP SELECTION ENDS HERE
    //*******************************************************************************************************


    //========================================================================================================
    //                                    Sanity check
    //========================================================================================================
    
    for (auto& jet: jetData.getSelectedJets()){
      hAllJetCvsL         -> Fill(true, jet.pfCombinedCvsLJetTags());
      hAllJetPtD          -> Fill(true, jet.QGTaggerAK4PFCHSptD());
      hAllJetAxis2        -> Fill(true, jet.QGTaggerAK4PFCHSaxis2());
      hAllJetMult         -> Fill(true, jet.QGTaggerAK4PFCHSmult());
      hAllJetBdisc        -> Fill(true, jet.bjetDiscriminator());
      hAllJetQGLikelihood -> Fill(true, jet.QGTaggerAK4PFCHSqgLikelihood());
    }
  

    vector<genParticle> GenCharm = GetGenParticles(fEvent.genparticles().getGenParticles(), 4);
    vector<Jet> CJets;

    for (size_t i=0; i<GenCharm.size(); i++){
      double dRmin = 10000.0;
      // double dPtOverPtmin = 10000.0;
      Jet mcMatched_CJet;
      for (auto& jet: jetData.getSelectedJets()){
	double dR  = ROOT::Math::VectorUtil::DeltaR( jet.p4(), GenCharm.at(i).p4());
	double dPtOverPt = std::abs((jet.pt() - GenCharm.at(i).pt())/ GenCharm.at(i).pt());
	if (dR > dRcut) continue;
	if (dR > dRmin) continue;
	//if (dPtOverPt > dPtOverPtmin) continue;
	if (dPtOverPt > twoSigma) continue;
	dRmin = dR;
	// dPtOverPtmin = dPtOverPt;
	mcMatched_CJet = jet;
      }
      if (dRmin < dRcut){
	hCJetCvsL         -> Fill(true, mcMatched_CJet.pfCombinedCvsLJetTags());
	hCJetPtD          -> Fill(true, mcMatched_CJet.QGTaggerAK4PFCHSptD());
	hCJetAxis2        -> Fill(true, mcMatched_CJet.QGTaggerAK4PFCHSaxis2());
	hCJetMult         -> Fill(true, mcMatched_CJet.QGTaggerAK4PFCHSmult());
	hCJetBdisc        -> Fill(true, mcMatched_CJet.bjetDiscriminator());
      }
    }
    


    //========================================================================================================
    //                             Gen particles - Not of interest
    //========================================================================================================
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
      
      //      int genMom_index    = -1;
      //      double genMom_pdgId = 999.999;
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
      // if (genMom_index >= 0){
      // 	const Particle<ParticleCollection<double> > m = fEvent.genparticles().getGenParticles()[genMom_index];
      // 	genMom_pdgId  = m.pdgId();
      // }
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
	  std::cout << std::string(15*10, '=') << std::endl;            
	  std::cout << std::setw(12) << "Index "   << std::setw(12) << "PdgId"        << std::setw(12) << "Pt"           << std::setw(12) << "Eta" << std::setw(12) << "Phi"
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
  
