//TopTaggerEfficiency
// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

struct SelectedTrijet{
  Jet Jet1;
  Jet Jet2;
  Jet BJet;
  double MVA;
  math::XYZTLorentzVector TrijetP4;
  math::XYZTLorentzVector DijetP4;
};

class TopTaggerEfficiency: public BaseSelector {
public:
  explicit TopTaggerEfficiency(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TopTaggerEfficiency() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;

  bool HasMother(const Event& event, const genParticle &p, const int mom_pdgId);
  bool HasRecursivelyMother(const Event& event, const genParticle &p, const int mom_pdgId);
  genParticle findLastCopy(int index);
  //is Bjet                       
  bool isBJet(const Jet& jet, const std::vector<Jet>& bjets);
  bool isMatchedJet(const Jet& jet, const std::vector<Jet>& jets);
  ///Are same Jets
  bool areSameJets(const Jet& jet1, const Jet& jet2);

  const genParticle GetLastCopy(const vector<genParticle> genParticles, const genParticle &p);
  vector<genParticle> GetGenParticles(const vector<genParticle> genParticles, const int pdgId);

  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet);
  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet,
		    const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet);



  int GetTrijet1(const TopSelectionBDT::Data& topData,  const std::vector<Jet>& bjets);
  int GetTrijet2(const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets, const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet);
  bool foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets);

  bool Trijet_crossCleaned(int Index, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets);
  bool TrijetPassBDT_crossCleaned(int Index, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets); //Really needed?
  bool IsCrossCleaned(int index_j, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets, std::vector<int> TopIndex);
  int GetLdgOrSubldgTopIndex(std::vector<int>TopIndex, const TopSelectionBDT::Data& topData, string type);

  std::vector<int>SortPt(const TopSelectionBDT::Data& topData);

  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
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
  TauSelection  fTauSelection;
  JetSelection  fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  // QuarkGluonLikelihoodRatio fQGLRSelection;
  TopSelectionBDT fTopSelection;
  // FatJetSelection fFatJetSelection;
  Count cSelected;
    
  //For Efficiency plots
  WrappedTH1 *hAllTopQuarkPt_Matched;
  WrappedTH1 *hTopQuarkPt;
  WrappedTH1 *hAllTopQuarkPt_MatchedBDT;
  WrappedTH1 *hEventTrijetPt2T_Matched;
  WrappedTH1 *hEventTrijetPt2T;
  WrappedTH1 *hEventTrijetPt2T_BDT;
  WrappedTH1 *hEventTrijetPt2T_MatchedBDT;
  WrappedTH1 *hTrijetFakePt_BDT;
  WrappedTH1 *hTrijetFakePt;
  
  WrappedTH1 *hAssocTopQuarkPt;
  WrappedTH1 *hAssocTopQuarkPt_Matched;
  WrappedTH1 *hAssocTopQuarkPt_MatchedBDT;

  WrappedTH1 *hHiggsTopQuarkPt;           
  WrappedTH1 *hHiggsTopQuarkPt_Matched;   
  WrappedTH1 *hHiggsTopQuarkPt_MatchedBDT;

  //Debug
  WrappedTH1 *hBothTopQuarkPt;           
  WrappedTH1 *hBothTopQuarkPt_Matched;   
  WrappedTH1 *hBothTopQuarkPt_MatchedBDT;

  //Top candidates multiplicity
  WrappedTH1 *h_TopMultiplicity_AllTops;
  WrappedTH1 *h_TopMultiplicity_SelectedTops;
  WrappedTH1 *h_TopMultiplicity_AllTops_cleaned;
  WrappedTH1 *h_TopMultiplicity_SelectedTops_cleaned;

  //More Efficiency plots
  WrappedTH1 *hTrijetPt_LdgOrSldg;
  WrappedTH1 *hTrijetPt_Ldg;
  WrappedTH1 *hTrijetPt_Subldg;

  WrappedTH1 *hTrijetPt_LdgOrSldg_Unmatched;
  WrappedTH1 *hTrijetPt_LdgOrSldg_UnmatchedBDT;
  WrappedTH1 *hTrijetPt_LdgOrSldg_Matched;
  WrappedTH1 *hTrijetPt_LdgOrSldg_MatchedBDT;

  WrappedTH1 *hTrijetPt_Ldg_Unmatched;
  WrappedTH1 *hTrijetPt_Ldg_UnmatchedBDT;
  WrappedTH1 *hTrijetPt_Ldg_Matched;
  WrappedTH1 *hTrijetPt_Ldg_MatchedBDT;
   
  WrappedTH1 *hTrijetPt_Sldg_Unmatched;
  WrappedTH1 *hTrijetPt_Sldg_UnmatchedBDT;
  WrappedTH1 *hTrijetPt_Sldg_Matched;
  WrappedTH1 *hTrijetPt_Sldg_MatchedBDT;


  // Non-common histograms
  WrappedTH1Triplet* hTetrajetMass;
  WrappedTH1Triplet* hLdgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaY_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaY_Trijet_TetrajetBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth;
  WrappedTH1Triplet* hLdgTrijetJets_DeltaRmin;
  WrappedTH1Triplet* hSubldgTrijetJets_DeltaRmin;
  WrappedTH1Triplet* hLdgTrijetJets_DeltaRmax;
  WrappedTH1Triplet* hSubldgTrijetJets_DeltaRmax;

  WrappedTH1Triplet* hTetrajetMass_LdgTopIsHTop;
  WrappedTH1Triplet* hTetrajetMass_SubldgTopIsHTop;
  WrappedTH1Triplet* hTetrajetMass_LdgWIsWfromH;
  WrappedTH1Triplet* hTetrajetMass_TopUnmatched;

  WrappedTH1Triplet* hTetrajetBjetBDisc;
  WrappedTH1Triplet* hLdgTrijetPt;
  WrappedTH1Triplet* hLdgTrijetDijetPt;
  WrappedTH1Triplet* hSubldgTrijetPt;
  WrappedTH1Triplet* hSubldgTrijetDijetPt;
  WrappedTH1Triplet* hLdgTrijetBjetPt;
  WrappedTH1Triplet* hTetrajetBjetPt;
  WrappedTH1Triplet* hTetrajetPt_LdgTopIsHTop;
  WrappedTH1Triplet* hTetrajetPt;
  WrappedTH1Triplet* hLdgTrijet_DeltaR_Dijet_TrijetBjet;
  WrappedTH1Triplet* hLdgTrijet_DeltaR_Dijet;

  WrappedTH1Triplet* hTopBDT_AllCandidates;

  WrappedTH1* hLdgInPtTrijetBDT;
  WrappedTH1* hSubldgInPtTrijetBDT;
  WrappedTH1* hLdgInBDTTrijetBDT;
  WrappedTH1* hSubldgInBDTTrijetBDT;

  WrappedTH1* hTopBDT_AllCleanedCandidates;
  WrappedTH1* hTrijet1_BDT;
  WrappedTH1* hTrijet2_BDT;
  WrappedTH1* hLdgTrijet_BDT;
  WrappedTH1* hSubldgTrijet_BDT;
  WrappedTH1* hBothTopCandidates_BDT;

  WrappedTH2* hTopBDT_Vs_TopMass;
  WrappedTH2* hTopBDT_Vs_WMass;
  WrappedTH2* hTopBDT_Vs_TopMass_AllCandidates;
  WrappedTH2* hTopBDT_Vs_WMass_AllCandidates;
  WrappedTH2* hTopBDT_Vs_TopMass_AllCleanedCandidates;
  WrappedTH2* hTopBDT_Vs_WMass_AllCleanedCandidates;
  WrappedTH2* hTrijet1_BDT_Vs_TopMass;
  WrappedTH2* hTrijet2_BDT_Vs_TopMass;
  WrappedTH2* hLdgTrijet_BDT_Vs_TopMass;
  WrappedTH2* hSubldgTrijet_BDT_Vs_TopMass;
  WrappedTH2* hTrijet1_BDT_Vs_WMass;
  WrappedTH2* hTrijet2_BDT_Vs_WMass;
  WrappedTH2* hLdgTrijet_BDT_Vs_WMass;
  WrappedTH2* hSubldgTrijet_BDT_Vs_WMass;
  WrappedTH2* hBothTopCandidates_BDT_Vs_TopMass;
  WrappedTH2* hBothTopCandidates_BDT_Vs_WMass;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TopTaggerEfficiency);

TopTaggerEfficiency::TopTaggerEfficiency(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PrelimTopMVACut(config, "TopSelectionBDT.TopMVACut"),
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
    fMETSelection(config.getParameter<ParameterSet>("METSelection")), // no subcounter in main counter
    // fQGLRSelection(config.getParameter<ParameterSet>("QGLRSelection")),// fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    // fFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void TopTaggerEfficiency::book(TDirectory *dir) {

  if (0) std::cout << "=== TopTaggerEfficiency::book()" << std::endl;
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
  // fQGLRSelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  // fFatJetSelection.bookHistograms(dir);


  // const int nPtBins       = 2*fCommonPlots.getPtBinSettings().bins();
  // const double fPtMin     = 2 *fCommonPlots.getPtBinSettings().min();
  // const double fPtMax     = 2* fCommonPlots.getPtBinSettings().max();

  const int nWMassBins    = fCommonPlots.getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots.getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots.getWMassBinSettings().max();

  const int nTopMassBins  = fCommonPlots.getTopMassBinSettings().bins();
  const float fTopMassMin = fCommonPlots.getTopMassBinSettings().min();
  const float fTopMassMax = fCommonPlots.getTopMassBinSettings().max();

  const int nPtBins       = 2*fCommonPlots.getPtBinSettings().bins();
  const double fPtMin     = 2 *fCommonPlots.getPtBinSettings().min();
  const double fPtMax     = 2* fCommonPlots.getPtBinSettings().max();


  // const int nEtaBins       = fCommonPlots.getEtaBinSettings().bins();
  // const double fEtaMin     = fCommonPlots.getEtaBinSettings().min();
  // const double fEtaMax     = fCommonPlots.getEtaBinSettings().max();

  // const int nPhiBins       = fCommonPlots.getPhiBinSettings().bins();
  // const double fPhiMin     = fCommonPlots.getPhiBinSettings().min();
  // const double fPhiMax     = fCommonPlots.getPhiBinSettings().max();

  const int nDRBins       = fCommonPlots.getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots.getDeltaRBinSettings().min();
  //const double fDRMax     = 3/5.*fCommonPlots.getDeltaRBinSettings().max();

  const int nDPhiBins     = fCommonPlots.getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots.getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots.getDeltaPhiBinSettings().max();

  const int nDEtaBins     = fCommonPlots.getDeltaEtaBinSettings().bins();
  const double fDEtaMin   = fCommonPlots.getDeltaEtaBinSettings().min();
  const double fDEtaMax   = fCommonPlots.getDeltaEtaBinSettings().max();

  const int  nBDiscBins   = fCommonPlots.getBJetDiscBinSettings().bins();
  //  const float fBDiscMin   = fCommonPlots.getBJetDiscBinSettings().min(); 
  const float fBDiscMax   = fCommonPlots.getBJetDiscBinSettings().max();


  TDirectory* subdirTH1 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topbdtSelection_");
  TDirectory* subdirTH2 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "topbdtSelectionTH2_");

  std::string myInclusiveLabel  = "AnalysisTriplets";
  std::string myFakeLabel       = myInclusiveLabel+"False";
  std::string myGenuineLabel    = myInclusiveLabel+"True";
  TDirectory* myInclusiveDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myGenuineDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs = {myInclusiveDir, myFakeDir, myGenuineDir};

  // Book non-common histograms
  //For Efficiency plots
  hTopQuarkPt                   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopQuarkPt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_Matched        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "AllTopQuarkPt_Matched"       , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAllTopQuarkPt_MatchedBDT     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "AllTopQuarkPt_MatchedBDT"    , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hEventTrijetPt2T_Matched      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "EventTrijetPt2T_Matched"     , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hEventTrijetPt2T              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "EventTrijetPt2T"             ,";p_{T} (GeV/c)" , nPtBins, fPtMin, fPtMax);
  hEventTrijetPt2T_BDT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "EventTrijetPt2T_BDT"         , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hEventTrijetPt2T_MatchedBDT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "EventTrijetPt2T_MatchedBDT"  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetFakePt                 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetFakePt"                ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetFakePt_BDT             = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetFakePt_BDT"            ,";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hAssocTopQuarkPt              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "AssocTopQuarkPt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAssocTopQuarkPt_Matched      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "AssocTopQuarkPt_Matched"       , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hAssocTopQuarkPt_MatchedBDT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "AssocTopQuarkPt_MatchedBDT"    , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hHiggsTopQuarkPt              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "HiggsTopQuarkPt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hHiggsTopQuarkPt_Matched      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "HiggsTopQuarkPt_Matched"       , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hHiggsTopQuarkPt_MatchedBDT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "HiggsTopQuarkPt_MatchedBDT"    , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  //Debug
  hBothTopQuarkPt              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "BothTopQuarkPt"                  , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hBothTopQuarkPt_Matched      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "BothTopQuarkPt_Matched"       , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hBothTopQuarkPt_MatchedBDT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "BothTopQuarkPt_MatchedBDT"    , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  //More Efficiency plots
  hTrijetPt_LdgOrSldg          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_LdgOrSldg", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Ldg                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Ldg",       ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Subldg             = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Subldg",    ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hTrijetPt_LdgOrSldg_Unmatched     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_LdgOrSldg_Unmatched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_LdgOrSldg_UnmatchedBDT  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_LdgOrSldg_UnmatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_LdgOrSldg_Matched       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_LdgOrSldg_Matched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_LdgOrSldg_MatchedBDT    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_LdgOrSldg_MatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  hTrijetPt_Ldg_Unmatched      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Ldg_Unmatched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Ldg_UnmatchedBDT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Ldg_UnmatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Ldg_Matched        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Ldg_Matched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Ldg_MatchedBDT     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Ldg_MatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
   
  hTrijetPt_Sldg_Unmatched     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Sldg_Unmatched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Sldg_UnmatchedBDT  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Sldg_UnmatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Sldg_Matched       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Sldg_Matched", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hTrijetPt_Sldg_MatchedBDT     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TrijetPt_Sldg_MatchedBDT", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);


  //Distances
  hLdgTrijet_DeltaR_Trijet_TetrajetBjet      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet"  , 
										 ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet"  , 
										 ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet"  , 
										 ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet"  , 
										 ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet"  , 
										 ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet"  , 
										 ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet"  , 
										 ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet"  , 
										 ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);

  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBjet"  , 
											  ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hLdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hLdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hLdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);
  hSubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaR_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta R(Trijet,b_{free})"  , nDRBins     , fDRMin     , 6.);
  hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaEta_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Eta(Trijet,b_{free})", nDEtaBins, fDEtaMin, fDEtaMax/2.);
  hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaPhi_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Phi(Trijet,b_{free})", nDPhiBins, fDPhiMin, fDPhiMax);
  hSubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijet_DeltaY_Trijet_TetrajetBjet_trueBoth"  , 
											  ";#Delta Y(Trijet,b_{free})"  , nDRBins     , fDRMin     , 5.);

  hLdgTrijetJets_DeltaRmin       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetJets_DeltaRmin",    ";#Delta R"  , 60      , fDRMin     , 3.);
  hSubldgTrijetJets_DeltaRmin    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetJets_DeltaRmin", ";#Delta R"  , 60      , fDRMin     , 3.);
  hLdgTrijetJets_DeltaRmax       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetJets_DeltaRmax",    ";#Delta R"  , 120     , fDRMin     , 6.);
  hSubldgTrijetJets_DeltaRmax    = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetJets_DeltaRmax", ";#Delta R"  , 120     , fDRMin     , 6.);

  hTetrajetMass                      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass"             , ";m_{jjbb} (GeV/c^{2})",    300,  0, 3000);
  hTetrajetMass_LdgTopIsHTop         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_LdgTopIsHTop", ";m_{jjbb} (GeV/c^{2})",    300,  0, 3000);
  hTetrajetMass_SubldgTopIsHTop      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_SubldgTopIsHTop", ";m_{jjbb} (GeV/c^{2})", 300,  0, 3000);
  hTetrajetMass_LdgWIsWfromH         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_LdgWIsWfromH", ";m_{jjbb} (GeV/c^{2})",    300,  0, 3000);
  hTetrajetMass_TopUnmatched         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetMass_TopUnmatched", ";m_{jjbb} (GeV/c^{2})",    300,  0, 3000);

  hTetrajetBjetBDisc     = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetBJetBDisc",";b-tag discriminator", nBDiscBins  , 0.8 , fBDiscMax);
  hLdgTrijetPt           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetPt", ";p_{T}", 100, 0, 1000);
  hLdgTrijetDijetPt      = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetDijetPt", ";p_{T}",100, 0,1000);
  hSubldgTrijetPt        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetPt", ";p_{T}", 100, 0, 1000);
  hSubldgTrijetDijetPt   = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "SubldgTrijetDijetPt", ";p_{T}",100, 0,1000);
  hLdgTrijetBjetPt       = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijetBjetPt", ";p_{T}", 100, 0, 1000);
  hTetrajetBjetPt        = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetBjetPt", ";p_{T}", 100, 0, 1000);
  hTetrajetPt_LdgTopIsHTop            = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPt_LdgTopIsHTop", ";p_{T}", 100, 0, 1000);
  hTetrajetPt                         = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TetrajetPt", ";p_{T}", 100, 0, 1000);
  hLdgTrijet_DeltaR_Dijet_TrijetBjet  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Dijet_TrijetBjet", ";",
                                                                          nDRBins     , fDRMin     , 6);
  hLdgTrijet_DeltaR_Dijet = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "LdgTrijet_DeltaR_Dijet", ";",
							      nDRBins     , fDRMin     , 6);

  hTopBDT_AllCandidates           = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "TopBDT_AllCandidates",";top candidate BDT", 40, -1.0, 1.0);
  hLdgInPtTrijetBDT               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgInPtTrijetBDT",    ";top candidate BDT", 40, -1.0, 1.0);
  hSubldgInPtTrijetBDT            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgInPtTrijetBDT", ";top candidate BDT", 40, -1.0, 1.0);
  hLdgInBDTTrijetBDT              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgInBDTTrijetBDT",   ";top candidate BDT", 40, -1.0, 1.0);
  hSubldgInBDTTrijetBDT           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgInBDTTrijetBDT",";top candidate BDT", 40, -1.0, 1.0);

  //Top candidates multiplicity
  h_TopMultiplicity_AllTops              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopMultiplicity_AllTops",             ";top multiplicity", 20, 0, 20);
  h_TopMultiplicity_SelectedTops         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopMultiplicity_SelectedTops",        ";top multiplicity", 20, 0, 20);
  h_TopMultiplicity_AllTops_cleaned      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopMultiplicity_AllTops_cleaned",     ";top multiplicity", 10, 0, 10);
  h_TopMultiplicity_SelectedTops_cleaned = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopMultiplicity_SelectedTops_cleaned",";top multiplicity", 10, 0, 10);

  hTopBDT_AllCleanedCandidates  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "TopBDT_AllCleanedCandidates",";top candidate BDT", 40, -1.0, 1.0);
  hTrijet1_BDT                  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "Trijet1_BDT", ";top candidate BDT", 40, -1.0, 1.0);
  hTrijet2_BDT                  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "Trijet2_BDT", ";top candidate BDT", 40, -1.0, 1.0);
  hLdgTrijet_BDT                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "LdgTrijet_BDT", ";top candidate BDT", 40, -1.0, 1.0);
  hSubldgTrijet_BDT             = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "SubldgTrijet_BDT", ";top candidate BDT", 40, -1.0, 1.0);
  hBothTopCandidates_BDT        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdirTH1, "BothTopCandidates_BDT", ";top candidate BDT", 40, -1.0, 1.0);

  // Histograms (2D)

  hTopBDT_Vs_TopMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
						  40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hTopBDT_Vs_WMass   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
						  40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);

  hTopBDT_Vs_TopMass_AllCandidates = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_TopMass_AllCandidates", ";top candidate BDT;m_{top} GeV/c^{2}",
								40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hTopBDT_Vs_WMass_AllCandidates   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_WMass_AllCandidates", ";top candidate BDT;m_{W} GeV/c^{2}",                         
								40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);                                                           

  hTopBDT_Vs_TopMass_AllCleanedCandidates = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_TopMass_AllCleanedCandidates", ";top candidate BDT;m_{top} GeV/c^{2}",
								       40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hTopBDT_Vs_WMass_AllCleanedCandidates   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "TopBDT_Vs_WMass_AllCleanedCandidates", ";top candidate BDT;m_{W} GeV/c^{2}",
								       40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);

  hTrijet1_BDT_Vs_TopMass   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "Trijet1_BDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
							 40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hTrijet2_BDT_Vs_TopMass  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "Trijet2_BDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
							40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hLdgTrijet_BDT_Vs_TopMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijet_BDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
							 40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hSubldgTrijet_BDT_Vs_TopMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "SubldgTrijet_BDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
							    40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);
  
  hTrijet1_BDT_Vs_WMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "Trijet1_BDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
						     40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);

  hTrijet2_BDT_Vs_WMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "Trijet2_BDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
						     40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);

  hLdgTrijet_BDT_Vs_WMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "LdgTrijet_BDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
						       40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);

  hSubldgTrijet_BDT_Vs_WMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "SubldgTrijet_BDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
							  40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);
  
  hBothTopCandidates_BDT_Vs_TopMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "BothTopCandidates_BDT_Vs_TopMass", ";top candidate BDT;m_{top} GeV/c^{2}",
								 40, -1.0, 1.0, nTopMassBins, fTopMassMin, fTopMassMax);

  hBothTopCandidates_BDT_Vs_WMass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdirTH2, "BothTopCandidates_BDT_Vs_WMass", ";top candidate BDT;m_{W} GeV/c^{2}",
							       40, -1.0, 1.0, nWMassBins, fWMassMin, fWMassMax);


  return;
}

bool TopTaggerEfficiency::HasMother(const Event& event, const genParticle &p, const int mom_pdgId){
  //  Description:                                                                                         //  Returns true if the particle has a mother with pdgId equal to mom_pdgId.                           

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
    }

  return false;
}


bool TopTaggerEfficiency::HasRecursivelyMother(const Event& event, const genParticle &p, const int mom_pdgId){
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
      if (std::abs(motherID) == mom_pdgId) return true;
      else{
	return HasRecursivelyMother(event, m, mom_pdgId);
      }
    }

  return false;
}

//Get all gen particles by pdgId                   
vector<genParticle> TopTaggerEfficiency::GetGenParticles(const vector<genParticle> genParticles, const int pdgId)
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

//  Get the last copy of a particle.                                              
const genParticle TopTaggerEfficiency::GetLastCopy(const vector<genParticle> genParticles, const genParticle &p){

  int gen_pdgId = p.pdgId();
  for (size_t i=0; i<p.daughters().size(); i++){
    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();

    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}


bool TopTaggerEfficiency::isMatchedJet(const Jet& jet, const std::vector<Jet>& jets) {
  for (auto iJet: jets)
    {
      if (areSameJets(jet, iJet)) return true;
    }
  return false;
}

bool TopTaggerEfficiency::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}

bool TopTaggerEfficiency::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, 
				       const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet){

  bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet)       && areSameJets(trijetJet2, MCtrue_SubldgJet) && areSameJets(trijetBJet,  MCtrue_Bjet);
  bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet)    && areSameJets(trijetJet2, MCtrue_LdgJet)    && areSameJets(trijetBJet,  MCtrue_Bjet);
  if (same1 || same2) return true;
  return false;

}

bool TopTaggerEfficiency::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, 
				       const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet){

  for (size_t k=0; k<MCtrue_Bjet.size(); k++){
    bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet.at(k))       && areSameJets(trijetJet2, MCtrue_SubldgJet.at(k)) && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet.at(k))    && areSameJets(trijetJet2, MCtrue_LdgJet.at(k))    && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    if (same1 || same2) return true;
  }
  return false;
}


int TopTaggerEfficiency::GetTrijet1(const TopSelectionBDT::Data& topData,  const std::vector<Jet>& bjets){
  //  Description:
  //  Returns the leading in BDT trijet
  int trijet1_index = -1;

  for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){
    Jet jet1 = topData.getAllTopsJet1().at(i);
    Jet jet2 = topData.getAllTopsJet2().at(i);
    Jet bjet = topData.getAllTopsBJet().at(i);
    
    //Skip Trijet combination if no free bjets left in the event
      if ( (size_t)( isBJet(jet1,bjets) + isBJet(jet2,bjets) + isBJet(bjet,bjets)) ==  bjets.size()) continue;
      trijet1_index = i;
      return trijet1_index;
    }
  return trijet1_index;
}


int TopTaggerEfficiency::GetTrijet2(const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets, const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet){
  //  Description:
  //  Returns the subleading in BDT trijet
  double MVAmax2 = -999.999;
  std::vector<Jet> Trijet1;
  Trijet1.push_back(trijetJet1); Trijet1.push_back(trijetJet2); Trijet1.push_back(trijetBJet);
  int trijet2_index = -1;

  for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){
    Jet jet1 = topData.getAllTopsJet1().at(i);
    Jet jet2 = topData.getAllTopsJet2().at(i);
    Jet bjet = topData.getAllTopsBJet().at(i);
    
    // Skip top candidates with same jets as Leading in BDT trijet
    if (isMatchedJet(bjet, Trijet1) || isMatchedJet(jet1, Trijet1) || isMatchedJet(jet2, Trijet1)) continue;
    //Skip if there are no free bjets left
    if (!foundFreeBjet(trijetJet1, trijetJet2, trijetBJet, jet1, jet2, bjet, bjets)) continue;
    
    double mvaValue = topData.getAllTopsMVA().at(i);
    // Find subleading in BDT value trijet
    if (mvaValue < MVAmax2) continue;
    
    trijet2_index = i;
    return trijet2_index;
  }
  return trijet2_index;
}

bool TopTaggerEfficiency::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool TopTaggerEfficiency::foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets){
  //Description:
  //Returns false if two trijet combinations use all the bjets of the event
  //Used to select the best two top candidates which are not formed by all the bjets off the event
  //One free bjet is required for the tetrajet reconstruction
  int SumTrijet1 = isBJet(trijet1Jet1, bjets) + isBJet(trijet1Jet2, bjets) + isBJet(trijet1BJet, bjets);
  int SumTrijet2 = isBJet(trijet2Jet1, bjets) + isBJet(trijet2Jet2, bjets) + isBJet(trijet2BJet, bjets);
  if ((size_t)(SumTrijet1 + SumTrijet2) != bjets.size()) return true;
  return false;
}



bool TopTaggerEfficiency::Trijet_crossCleaned(int Index, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets){
  //Descriptions: Used to find the cross-cleaned trijet multiplicity. The function takes as input the index of a trijet and the total trijet collection and returns
  //False: (a) If the trijet uses all the bjets of the event
  //       (b) If at least one of the subjets of the trijets are used by the trijets with Higher BDT value (Higher BDT value -> smaller index: Trijets sorted in BDT value)
  //True: If cross-cleaned trijet                                                                                                                                                                                                                                     
  if ( (size_t)( isBJet(topData.getAllTopsJet1().at(Index),bjets) + isBJet(topData.getAllTopsJet2().at(Index),bjets) + isBJet(topData.getAllTopsBJet().at(Index),bjets)) ==  bjets.size()) return false;
  if (Index > 0)
    {
      for (size_t i=0; i<(size_t)Index; i++)
        {
          if ( (size_t)( isBJet(topData.getAllTopsJet1().at(i),bjets) + isBJet(topData.getAllTopsJet2().at(i),bjets) + isBJet(topData.getAllTopsBJet().at(i),bjets)) ==  bjets.size()) continue;
          //Vector includes the 3 subjets of a trijet                                                                                                                                                                                                                 
	  std::vector<Jet> Trijet;
          Trijet.push_back(topData.getAllTopsJet1().at(i)); Trijet.push_back(topData.getAllTopsJet2().at(i)); Trijet.push_back(topData.getAllTopsBJet().at(i));
          // Skip top candidates with same jets as Trijets with higher BDDT value                                                                                                                                                                                     

          bool sharedJets = isMatchedJet(topData.getAllTopsBJet().at(Index), Trijet) || isMatchedJet(topData.getAllTopsJet1().at(Index), Trijet) || isMatchedJet(topData.getAllTopsJet2().at(Index), Trijet);
	  //if (sharedJets) return false;
	  if (Trijet_crossCleaned(i, topData, bjets) && sharedJets ){
            return false;
          }
        }
    }

  return true;
}


bool TopTaggerEfficiency::TrijetPassBDT_crossCleaned(int Index, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets){
  //Descriptions: Used to find the cross-cleaned trijet multiplicity. The function takes as input the index of a trijet and the total trijet collection and returns
  //False: (a) If the trijet uses all the bjets of the event
  //       (b) If at least one of the subjets of the trijets are used by the trijets with Higher BDT value (Higher BDT value -> smaller index: Trijets sorted in BDT value)
  //True: If cross-cleaned trijet                                                                                                                                                                                                                                     
  if ( (size_t)( isBJet(topData.getSelectedTopsJet1().at(Index),bjets) + isBJet(topData.getSelectedTopsJet2().at(Index),bjets) + isBJet(topData.getSelectedTopsBJet().at(Index),bjets)) ==  bjets.size()) return false;
  if (Index > 0)
    {
      for (size_t i=0; i<(size_t)Index; i++)
        {
          if ( (size_t)( isBJet(topData.getSelectedTopsJet1().at(i),bjets) + isBJet(topData.getSelectedTopsJet2().at(i),bjets) + isBJet(topData.getSelectedTopsBJet().at(i),bjets)) ==  bjets.size()) continue;
          //Vector includes the 3 subjets of a trijet                                                                                                                                                                                                                 
	  std::vector<Jet> Trijet;
          Trijet.push_back(topData.getSelectedTopsJet1().at(i)); Trijet.push_back(topData.getSelectedTopsJet2().at(i)); Trijet.push_back(topData.getSelectedTopsBJet().at(i));
          // Skip top candidates with same jets as Trijets with higher BDDT value                                                                                                                                                                                     

          bool sharedJets = isMatchedJet(topData.getSelectedTopsBJet().at(Index), Trijet) || isMatchedJet(topData.getSelectedTopsJet1().at(Index), Trijet) || isMatchedJet(topData.getSelectedTopsJet2().at(Index), Trijet);
	  //if (sharedJets) return false;
	  if (TrijetPassBDT_crossCleaned(i, topData, bjets) && sharedJets ){
            return false;
          }
        }
    }

  return true;
}

bool TopTaggerEfficiency::IsCrossCleaned(int index_j, const TopSelectionBDT::Data& topData, const std::vector<Jet>& bjets, std::vector<int> TopIndex){
  //Descriptions: Used to find the cross-cleaned trijet multiplicity. The function takes as input the index of a trijet and the total trijet collection and returns
  //False: (a) If the trijet uses all the bjets of the event
  //       (b) If at least one of the subjets of the trijets are used by the trijets with Higher BDT value (Higher BDT value -> smaller index: Trijets sorted in BDT value)
  //True: If cross-cleaned trijet                                                                                                                                                                                                                                     
  int Index = TopIndex.at(index_j);
  if ( (size_t)( isBJet(topData.getAllTopsJet1().at(Index),bjets) + isBJet(topData.getAllTopsJet2().at(Index),bjets) + isBJet(topData.getAllTopsBJet().at(Index),bjets)) ==  bjets.size()) return false;
  //std::cout<<"3"<<std::endl;
  if (index_j > 0)
    {
      for (size_t i=0; i<(size_t)index_j; i++)
	{
	  int Index_i = TopIndex.at(i);
          if ( (size_t)( isBJet(topData.getAllTopsJet1().at(Index_i),bjets) + isBJet(topData.getAllTopsJet2().at(Index_i),bjets) + isBJet(topData.getAllTopsBJet().at(Index_i),bjets)) ==  bjets.size()) continue;
          //Vector includes the 3 subjets of a trijet
	  std::vector<Jet> Trijet;
          Trijet.push_back(topData.getAllTopsJet1().at(Index_i)); Trijet.push_back(topData.getAllTopsJet2().at(Index_i)); Trijet.push_back(topData.getAllTopsBJet().at(Index_i));
          // Skip top candidates with same jets as Trijets with higher BDDT value                                                                                                                                                                                    
                                                                                                                                                                                                                   
          bool sharedJets = isMatchedJet(topData.getAllTopsBJet().at(Index), Trijet) || isMatchedJet(topData.getAllTopsJet1().at(Index), Trijet) || isMatchedJet(topData.getAllTopsJet2().at(Index), Trijet);

	  // std::cout<<"trijet1: "<<topData.getAllTopsJet1().at(Index_i).index()<<" "<<topData.getAllTopsJet2().at(Index_i).index()<<" "<<topData.getAllTopsBJet().at(Index_i).index()<<std::endl;
	  // std::cout<<"trijet2: "<<topData.getAllTopsBJet().at(Index).index()<<" "<<topData.getAllTopsJet1().at(Index).index()<<" "<<topData.getAllTopsJet2().at(Index).index()<<std::endl;
	  // std::cout<<"have shared objects "<<sharedJets<<std::endl;
	  //bool myBoolean = IsCrossCleaned(i, topData, bjets, TopIndex) && sharedJets;
	  //std::cout<<"IsCrossCleaned(i, topData, bjets, TopIndex) && sharedJets "<<myBoolean<<std::endl;
	  if (IsCrossCleaned(i, topData, bjets, TopIndex) && sharedJets ){
	    return false;
	  }
	  //return (!(IsCrossCleaned(i, topData, bjets, TopIndex) && sharedJets ));
        }
    }

  return true;
}




int TopTaggerEfficiency::GetLdgOrSubldgTopIndex(std::vector<int>TopIndex, const TopSelectionBDT::Data& topData, string type){
  double maxPt1 = -999.999, maxPt2 = -999.999;
  int maxIndex1 = -1, maxIndex2 = -1;
  
  for (size_t i=0; i< TopIndex.size(); i++){
    int index = TopIndex.at(i);
    math::XYZTLorentzVector TopP4;
    TopP4 = topData.getAllTopsJet1().at(index).p4() + topData.getAllTopsJet2().at(index).p4() + topData.getAllTopsBJet().at(index).p4() ;
    //std::cout<<"pt "<<TopP4.Pt()<<std::endl;
    if (maxPt2 > TopP4.Pt()) continue;
    if (maxPt1 < TopP4.Pt()){
      maxPt2 = maxPt1;
      maxIndex2 = maxIndex1;
      maxPt1 = TopP4.Pt();
      maxIndex1 = index;
    }
    else{
      maxPt2 = TopP4.Pt();
      maxIndex2 = index;
    }
  }
  //std::cout<<"leading "<<maxPt1<<" subleading "<<maxPt2<<std::endl;
  if (type == "leading") return maxIndex1;
  if (type == "subleading") return maxIndex2;
  std::cout<<"GetLdgOrSubldgTopIndex: returning leading top index"<<std::endl;
  return maxIndex1;
}
      

// AllTopCandIndexSortPt_cleaned = SortPt(AllTopCandIndex_cleaned, topData);
std::vector<int>TopTaggerEfficiency::SortPt(const TopSelectionBDT::Data& topData){
  
  vector<int> TopSortPt;
  size_t size = topData.getAllTopsBJet().size();
  
  //Fill TopSortPt with initial vector's values
  for (size_t i=0; i<size; i++){
    TopSortPt.push_back(i);
  }
    
  if (size < 1) return TopSortPt;

  for (size_t i=0; i<size-1; i++)
    {
      for  (size_t j=i+1; j<size; j++)
        {
	  int index_i = TopSortPt.at(i);
	  math::XYZTLorentzVector TopP4_i;
	  TopP4_i = topData.getAllTopsJet1().at(index_i).p4() + topData.getAllTopsJet2().at(index_i).p4() + topData.getAllTopsBJet().at(index_i).p4() ;

	  int index_j = TopSortPt.at(j);
	  math::XYZTLorentzVector TopP4_j;
	  TopP4_j = topData.getAllTopsJet1().at(index_j).p4() + topData.getAllTopsJet2().at(index_j).p4() + topData.getAllTopsBJet().at(index_j).p4() ;
	  if (TopP4_i.Pt() >= TopP4_j.Pt()) continue;
	  int keepIndex = TopSortPt.at(i);
	  TopSortPt.at(i) = TopSortPt.at(j);
	  TopSortPt.at(j) = keepIndex;
	}
    }
  return TopSortPt;
}

/*
int TopTaggerEfficiency::SortInPt(vector <int> TopIndex){
  //  Description
  //  Takes as input a collection of Top Candidates and returns the collection sorted in pt value

  size_t size = TopIndex.size();
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

*/
void TopTaggerEfficiency::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void TopTaggerEfficiency::process(Long64_t entry) {

  // Sanity check
  //if (cfg_LdgTopDefinition != "MVA" &&  cfg_LdgTopDefinition != "Pt")
  //  {
  //    throw hplus::Exception("config") << "Unsupported method of defining the leading top (=" << cfg_LdgTopDefinition << "). Please select from \"MVA\" and \"Pt\".";
  //  }

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

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
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
 
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
  // - MET selection
  //================================================================================================
  if (0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 10) Top selection
  //================================================================================================
  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);

  //================================================================================================                             
  // Gen Particle Selection                            
  //================================================================================================           
  if (!fEvent.isMC()) return;

  std::vector<genParticle> GenTops;  
  GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
  
  std::vector<genParticle> GenChargedHiggs;
  std::vector<genParticle> GenChargedHiggs_BQuark;
  genParticle              GenHTop, GenATop;
  std::vector<genParticle> GenTops_BQuark;
  std::vector<genParticle> GenTops_SubldgQuark;
  std::vector<genParticle> GenTops_LdgQuark;
  
  vector <Jet> MCtrue_LdgJet,   MCtrue_SubldgJet,   MCtrue_Bjet,   MC_BJets;
  vector <Jet> HiggsTop_LdgJet, HiggsTop_SubldgJet, HiggsTop_Bjet, HBjet, MCtrue_TopJets;
  vector <Jet> HiggsTop_2j_LdgJet, HiggsTop_2j_SubldgJet, HiggsTop_2j_Bjet;   //At least 2 jets matched to Higgs's side top decay products
  vector <Jet> AssocTop_LdgJet, AssocTop_SubldgJet, AssocTop_Bjet;
  std::vector<genParticle> GenH_LdgQuark, GenH_SubldgQuark, GenH_BQuark;
  std::vector<genParticle> GenA_LdgQuark, GenA_SubldgQuark, GenA_BQuark;
  std::vector<bool> FoundTop;

  bool haveGenHTop = false, haveGenATop = false;
  //Find Assoc Top, Top from Higgs
  for (auto& top: GenTops){
    if (HasMother(fEvent, top, 37)){
      haveGenHTop = true;
      GenHTop = top;
    }
    else {
      haveGenATop = true;
      GenATop = top;
    }
  }

  

  const double twoSigmaDpt = 0.32;
  const double dRcut    = 0.4;
  
  int nGenuineTops = 0;
  
  genParticle Gen_Wh, Gen_Wa;
  bool have_Wh = false, have_Wa = false;
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
	    if (HasRecursivelyMother(fEvent, W, 37)){
	      Gen_Wh = W;
	      have_Wh = true;
	    }
	    else{
	      Gen_Wa = W;
	      have_Wa = true;
	    }
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
  if (doMatching){
    for (size_t i=0; i<GenTops.size(); i++)
      {	
	genParticle top = GenTops.at(i);
	genParticle LdgQuark    = GenTops_LdgQuark.at(i);
	genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
	genParticle BQuark      = GenTops_BQuark.at(i);
	if (HasMother(fEvent, top, 37)){
	  GenH_LdgQuark.push_back(GenTops_LdgQuark.at(i));
	  GenH_SubldgQuark.push_back(GenTops_SubldgQuark.at(i));
	  GenH_BQuark.push_back(GenTops_BQuark.at(i));
	}
	else{
	  GenA_LdgQuark.push_back(GenTops_LdgQuark.at(i));
	  GenA_SubldgQuark.push_back(GenTops_SubldgQuark.at(i));
	  GenA_BQuark.push_back(GenTops_BQuark.at(i));
	}
      }
  }
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
	  FoundTop.push_back(isGenuine);
	}

      // Top quark matched with a trijet                                                             
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
              if (dPtOverPt_Hb > twoSigmaDpt)     continue;
              dRmin = dR_Hb;
              mcMatched_ChargedHiggsBjet = jet;
            }
          if (dRmin <= dRcut) HBjet.push_back(mcMatched_ChargedHiggsBjet);
        }
    } //if (doMatching)
  
  if (0){
    std::cout<<GenHTop.pt()<<have_Wa<<have_Wh<<std::endl;
  }

  vector <int> AllTopCandIndex_cleaned, SelectedTopCandIndex_cleaned, AllTopCandIndexSortPt, AllTopCandIndexSortPt_cleaned;
  bool haveMatchedHiggsTop = HiggsTop_Bjet.size() > 0;
  bool haveMatchedAssocTop = AssocTop_Bjet.size() > 0;
  int ncleaned = 0;//, ncleaned_selected = 0;

  AllTopCandIndexSortPt = SortPt(topData);

  //Find cross-cleaned Tops
  for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){
    int index = i;
    if (Trijet_crossCleaned(index, topData, bjetData.getSelectedBJets())){
      ncleaned++;
      AllTopCandIndex_cleaned.push_back(index);
    }
  }

  //Find cross-cleaned Selected Tops 
  for (size_t i = 0; i < topData.getSelectedTopsBJet().size(); i++){
    int index = i;
    if (TrijetPassBDT_crossCleaned(index, topData, bjetData.getSelectedBJets())){
      SelectedTopCandIndex_cleaned.push_back(index);
    }
  }


  //Find cross-cleaned Top candidates !Starting from leading in pt top
  for (size_t i = 0; i < AllTopCandIndexSortPt.size(); i++){    
    int index = i;
    Jet jet1 = topData.getAllTopsJet1().at(AllTopCandIndexSortPt.at(i));
    Jet jet2 = topData.getAllTopsJet2().at(AllTopCandIndexSortPt.at(i));
    Jet bjet = topData.getAllTopsBJet().at(AllTopCandIndexSortPt.at(i));
    math::XYZTLorentzVector TopP4;
    TopP4 = jet1.p4() + jet2.p4() + bjet.p4();
	  
    if (IsCrossCleaned(index, topData, bjetData.getSelectedBJets(), AllTopCandIndexSortPt)){  //Soti:FIXME - Write ONE function for cleaned tops
      AllTopCandIndexSortPt_cleaned.push_back(AllTopCandIndexSortPt.at(i));      
      //std::cout<<jet1.index()<<" "<<jet2.index()<<" "<<bjet.index()<<std::endl;
    }
  }

  
  for (size_t i = 0; i < AllTopCandIndexSortPt_cleaned.size(); i++){    
    Jet jet1 = topData.getAllTopsJet1().at(AllTopCandIndexSortPt_cleaned.at(i));
    Jet jet2 = topData.getAllTopsJet2().at(AllTopCandIndexSortPt_cleaned.at(i));
    Jet bjet = topData.getAllTopsBJet().at(AllTopCandIndexSortPt_cleaned.at(i));
    // std::cout<<jet1.index()<<" "<<jet2.index()<<" "<<bjet.index()<<std::endl;
    // std::cout<<"Pt "<<(jet1.p4() + jet2.p4() + bjet.p4()).Pt()<<std::endl;
  }
  
  //std::cout<<"==="<<std::endl;
    
  //Top candidates multiplicity
  h_TopMultiplicity_AllTops              -> Fill(topData.getAllTopsBJet().size());
  h_TopMultiplicity_SelectedTops         -> Fill(topData.getSelectedTopsBJet().size());
  h_TopMultiplicity_AllTops_cleaned      -> Fill(AllTopCandIndex_cleaned.size());
  h_TopMultiplicity_SelectedTops_cleaned -> Fill(SelectedTopCandIndex_cleaned.size());

  
  for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){      	
    Jet jet1 = topData.getAllTopsJet1().at(i);
    Jet jet2 = topData.getAllTopsJet2().at(i);
    Jet bjet = topData.getAllTopsBJet().at(i);
    
    //double mva = topData.getAllTopsMVA().at(i);

    bool realTrijet = isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
    hTopBDT_AllCandidates -> Fill(realTrijet, topData.getAllTopsMVA().at(i));

  }

  
  //============================================================
  //============================================================
  //Return if less than two top candidates found in the event!!!
  if (ncleaned < 2) return;
  //============================================================
  //============================================================


  for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){      	
    Jet jet1 = topData.getAllTopsJet1().at(i);
    Jet jet2 = topData.getAllTopsJet2().at(i);
    Jet bjet = topData.getAllTopsBJet().at(i);
    
    double mva = topData.getAllTopsMVA().at(i);

    math::XYZTLorentzVector trijetP4, dijetP4;
    trijetP4 = jet1.p4() + jet2.p4() + bjet.p4();
    dijetP4  = jet1.p4() + jet2.p4();

    hTopBDT_Vs_TopMass_AllCandidates -> Fill(mva, trijetP4.M());
    hTopBDT_Vs_WMass_AllCandidates   -> Fill(mva, dijetP4.M());   

  }

  for (size_t i = 0; i < AllTopCandIndex_cleaned.size(); i++){
    int index = AllTopCandIndex_cleaned.at(i);

    Jet jet1 = topData.getAllTopsJet1().at(index);
    Jet jet2 = topData.getAllTopsJet2().at(index);
    Jet bjet = topData.getAllTopsBJet().at(index);
    
    double mva = topData.getAllTopsMVA().at(index);
    hTopBDT_AllCleanedCandidates -> Fill(mva);
    
    math::XYZTLorentzVector trijetP4, dijetP4;
    trijetP4 = jet1.p4() + jet2.p4() + bjet.p4();
    dijetP4  = jet1.p4() + jet2.p4();

    hTopBDT_Vs_TopMass_AllCleanedCandidates -> Fill(mva, trijetP4.M());
    hTopBDT_Vs_WMass_AllCleanedCandidates   -> Fill(mva, dijetP4.M());   
  }


  //Leading / Subleading top: Before cuts
  math::XYZTLorentzVector Trijet1_beforeCuts, Trijet2_beforeCuts;
  int ldg_index = -1, sldg_index = -1;

  int index1 = AllTopCandIndex_cleaned.at(0);
  Jet Trijet1Jet1_beforeCut  = topData.getAllTopsJet1().at(index1);
  Jet Trijet1Jet2_beforeCut  = topData.getAllTopsJet2().at(index1);
  Jet Trijet1BJet_beforeCut  = topData.getAllTopsBJet().at(index1);
  float Trijet1MVA_beforeCut = topData.getAllTopsMVA().at(index1);
  Trijet1_beforeCuts = Trijet1Jet1_beforeCut.p4() + Trijet1Jet2_beforeCut.p4() + Trijet1BJet_beforeCut.p4();

  int index2 = AllTopCandIndex_cleaned.at(1);
  Jet Trijet2Jet1_beforeCut  = topData.getAllTopsJet1().at(index2);
  Jet Trijet2Jet2_beforeCut  = topData.getAllTopsJet2().at(index2);
  Jet Trijet2BJet_beforeCut  = topData.getAllTopsBJet().at(index2);
  float Trijet2MVA_beforeCut = topData.getAllTopsMVA().at(index2);
  Trijet2_beforeCuts = Trijet2Jet1_beforeCut.p4() + Trijet2Jet2_beforeCut.p4() + Trijet2BJet_beforeCut.p4();
  
  if (Trijet1_beforeCuts.Pt() >= Trijet2_beforeCuts.Pt()){
    ldg_index = index1;
    sldg_index = index2;
  }
  else{
    ldg_index = index2;
    sldg_index = index1;
  }
    
  Jet LdgTrijetJet1_beforeCut     = topData.getAllTopsJet1().at(ldg_index);
  Jet LdgTrijetJet2_beforeCut     = topData.getAllTopsJet2().at(ldg_index);
  Jet LdgTrijetBJet_beforeCut     = topData.getAllTopsBJet().at(ldg_index);
  float LdgTrijetMVA_beforeCut    = topData.getAllTopsMVA().at(ldg_index);

  Jet SubldgTrijetJet1_beforeCut  = topData.getAllTopsJet1().at(sldg_index);
  Jet SubldgTrijetJet2_beforeCut  = topData.getAllTopsJet2().at(sldg_index);
  Jet SubldgTrijetBJet_beforeCut  = topData.getAllTopsBJet().at(sldg_index);
  float SubldgTrijetMVA_beforeCut = topData.getAllTopsMVA().at(sldg_index);


  //Fill Histograms
  hTrijet1_BDT      -> Fill(Trijet1MVA_beforeCut);
  hTrijet2_BDT      -> Fill(Trijet2MVA_beforeCut);
  hLdgTrijet_BDT    -> Fill(LdgTrijetMVA_beforeCut);
  hSubldgTrijet_BDT -> Fill(SubldgTrijetMVA_beforeCut);
  
  hTrijet1_BDT_Vs_TopMass   -> Fill(Trijet1MVA_beforeCut, (Trijet1Jet1_beforeCut.p4() + Trijet1Jet2_beforeCut.p4() + Trijet1BJet_beforeCut.p4()).M());
  hTrijet2_BDT_Vs_TopMass   -> Fill(Trijet2MVA_beforeCut, (Trijet2Jet1_beforeCut.p4() + Trijet2Jet2_beforeCut.p4() + Trijet2BJet_beforeCut.p4()).M());
  hLdgTrijet_BDT_Vs_TopMass -> Fill(LdgTrijetMVA_beforeCut, (LdgTrijetJet1_beforeCut.p4() + LdgTrijetJet2_beforeCut.p4() + LdgTrijetBJet_beforeCut.p4()).M());
  hSubldgTrijet_BDT_Vs_TopMass -> Fill(SubldgTrijetMVA_beforeCut, (SubldgTrijetJet1_beforeCut.p4() + SubldgTrijetJet2_beforeCut.p4() + SubldgTrijetBJet_beforeCut.p4()).M());

  hTrijet1_BDT_Vs_WMass   -> Fill(Trijet1MVA_beforeCut, (Trijet1Jet1_beforeCut.p4() + Trijet1Jet2_beforeCut.p4()).M());
  hTrijet2_BDT_Vs_WMass   -> Fill(Trijet2MVA_beforeCut, (Trijet2Jet1_beforeCut.p4() + Trijet2Jet2_beforeCut.p4()).M());
  hLdgTrijet_BDT_Vs_WMass -> Fill(LdgTrijetMVA_beforeCut, (LdgTrijetJet1_beforeCut.p4() + LdgTrijetJet2_beforeCut.p4()).M());
  hSubldgTrijet_BDT_Vs_WMass -> Fill(SubldgTrijetMVA_beforeCut, (SubldgTrijetJet1_beforeCut.p4() + SubldgTrijetJet2_beforeCut.p4()).M());

  hBothTopCandidates_BDT -> Fill(Trijet1MVA_beforeCut);
  hBothTopCandidates_BDT -> Fill(Trijet2MVA_beforeCut);

  hBothTopCandidates_BDT_Vs_TopMass -> Fill(Trijet1MVA_beforeCut, (Trijet1Jet1_beforeCut.p4() + Trijet1Jet2_beforeCut.p4() + Trijet1BJet_beforeCut.p4()).M());
  hBothTopCandidates_BDT_Vs_TopMass -> Fill(Trijet2MVA_beforeCut, (Trijet2Jet1_beforeCut.p4() + Trijet2Jet2_beforeCut.p4() + Trijet2BJet_beforeCut.p4()).M());

  hBothTopCandidates_BDT_Vs_WMass -> Fill(Trijet1MVA_beforeCut, (Trijet1Jet1_beforeCut.p4() + Trijet1Jet2_beforeCut.p4()).M());
  hBothTopCandidates_BDT_Vs_WMass -> Fill(Trijet2MVA_beforeCut, (Trijet2Jet1_beforeCut.p4() + Trijet2Jet2_beforeCut.p4()).M());


  
  if (doMatching){
    bool TopPassBDT_h = false;
    bool TopPassBDT_a = false;
    bool TopMatched_h = false;
    bool TopMatched_a = false;
    //Top from Higgs pt
    if (haveGenHTop){
      hHiggsTopQuarkPt -> Fill(GenHTop.pt());
      hBothTopQuarkPt -> Fill(GenHTop.pt());
    }
    //Associated Top pt
    if (haveGenATop){
      hAssocTopQuarkPt -> Fill(GenATop.pt());
      hBothTopQuarkPt -> Fill(GenATop.pt());
    }

    if (haveMatchedHiggsTop) TopMatched_h = isRealMVATop(HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0),
							 topData.getAllTopsJet1(), topData.getAllTopsJet2(), topData.getAllTopsBJet());
    if (haveMatchedAssocTop) TopMatched_a = isRealMVATop(AssocTop_LdgJet.at(0), AssocTop_SubldgJet.at(0), AssocTop_Bjet.at(0),
							 topData.getAllTopsJet1(), topData.getAllTopsJet2(), topData.getAllTopsBJet());
    
    //Matched top from Higgs
    if (TopMatched_h){
      hHiggsTopQuarkPt_Matched -> Fill(GenHTop.pt());
      hBothTopQuarkPt_Matched -> Fill(GenHTop.pt());
    }
    //Matched assiciated top
    if (TopMatched_a){
      hAssocTopQuarkPt_Matched -> Fill(GenATop.pt());
      hBothTopQuarkPt_Matched -> Fill(GenATop.pt());
    }

    if (haveMatchedHiggsTop) TopPassBDT_h = isRealMVATop(HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0),
						      topData.getSelectedTopsJet1(), topData.getSelectedTopsJet2(), topData.getSelectedTopsBJet());
    if (haveMatchedAssocTop) TopPassBDT_a = isRealMVATop(AssocTop_LdgJet.at(0), AssocTop_SubldgJet.at(0), AssocTop_Bjet.at(0),
						      topData.getSelectedTopsJet1(), topData.getSelectedTopsJet2(), topData.getSelectedTopsBJet());

    //Top from Higgs passes BDT
    if (TopPassBDT_h){
      hHiggsTopQuarkPt_MatchedBDT -> Fill(GenHTop.pt());
      hBothTopQuarkPt_MatchedBDT -> Fill(GenHTop.pt());
    }
    //Associated Top passes BDT
    if (TopPassBDT_a){
      hAssocTopQuarkPt_MatchedBDT -> Fill(GenATop.pt());
      hBothTopQuarkPt_MatchedBDT -> Fill(GenATop.pt());
    }

    
    //======================================
    //Denominator: Tagging Efficidency
    //======================================
    for (size_t j=0; j<GenTops.size(); j++){    
      // Get the genParicle
      genParticle top;
      top = GenTops.at(j);  
      hTopQuarkPt ->Fill(top.pt());
      // Find index of matched trijets
      bool isMatched      = FoundTop.at(j);
      bool isOnlyMatched  = (MCtrue_Bjet.size() == 1);
      bool sizesAgree     = (MCtrue_Bjet.size() == GenTops.size());
      bool genuineTop     = false;
      bool genuineTopPass = false;
      //bool genuineTop_passBDT = false;
      //bool fakeTop       = true;    
      for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){      	
	Jet jet1 = topData.getAllTopsJet1().at(i);
	Jet jet2 = topData.getAllTopsJet2().at(i);
	Jet bjet = topData.getAllTopsBJet().at(i);
	
	//bool realTrijet = isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
	//Fill only once
	// if (j == 0){	  
	//   hTopBDT_AllCandidates -> Fill(realTrijet, topData.getAllTopsMVA().at(i));
	// }
	if ( isMatched*isOnlyMatched )
	  {	    
	    if (isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet.at(0), MCtrue_SubldgJet.at(0), MCtrue_Bjet.at(0))) genuineTop = true;
	  }// if ( isMatched*isOnlyMatched )
	if ( isMatched*sizesAgree )
	  {
	    if (isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet.at(j), MCtrue_SubldgJet.at(j), MCtrue_Bjet.at(j))) genuineTop = true;
	  }//if ( isMatched*sizesAgree )  
	//if (genuineTop) continue;
      } //for (int i = 0; i < topData.getAllTopsBJet().size(); i++)

      if (genuineTop) hAllTopQuarkPt_Matched -> Fill(top.pt());
    
      //======================================
      //Numerator: Tagging Efficiency
      //======================================
      for (size_t i = 0; i < topData.getSelectedTopsBJet().size(); i++){
	Jet jet1 = topData.getSelectedTopsJet1().at(i);
	Jet jet2 = topData.getSelectedTopsJet2().at(i);
	Jet bjet = topData.getSelectedTopsBJet().at(i);
        if ( isMatched*isOnlyMatched )
          {
            if (isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet.at(0), MCtrue_SubldgJet.at(0), MCtrue_Bjet.at(0))) genuineTopPass = true;
          }// if ( isMatched*isOnlyMatched )
        if ( isMatched*sizesAgree )
          {
            if (isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet.at(j), MCtrue_SubldgJet.at(j), MCtrue_Bjet.at(j))) genuineTopPass = true;
          }//if ( isMatched*sizesAgree )
	//if (genuineTopPass) continue;
      }//for (int i = 0; i < topData.getSelectedTopsBJet().size(); i++) 
      if (genuineTopPass){
	hAllTopQuarkPt_MatchedBDT -> Fill(top.pt());
      }
    }//for (size_t j=0; j<GenTops.size(); j++)
  
    //======================================
    //Fake trijets: Unmatched
    //======================================
    for (size_t i = 0; i < topData.getAllTopsBJet().size(); i++){
      Jet jet1 = topData.getAllTopsJet1().at(i);
      Jet jet2 = topData.getAllTopsJet2().at(i);
      Jet bjet = topData.getAllTopsBJet().at(i);
	bool isFakeTop = (!isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet));
      math::XYZTLorentzVector trijetP4;
      trijetP4 = jet1.p4() + jet2.p4() + bjet.p4();
      if (isFakeTop){
	hTrijetFakePt                 -> Fill (trijetP4.Pt());
	if (cfg_PrelimTopMVACut.passedCut(topData.getAllTopsMVA().at(i))) hTrijetFakePt_BDT -> Fill (trijetP4.Pt());
      }
    }

    //======================================
    //Check only leading - subleading trijet
    //======================================    

    //Ldg in BDT top candidate
    int index1 = AllTopCandIndexSortPt_cleaned.at(0);
    Jet LdgTijetJet1_afterSS = topData.getAllTopsJet1().at(index1);
    Jet LdgTijetJet2_afterSS = topData.getAllTopsJet2().at(index1);
    Jet LdgTijetBJet_afterSS = topData.getAllTopsBJet().at(index1);
    float LdgTrijetMVA_afterSS = topData.getAllTopsMVA().at(index1);

    math::XYZTLorentzVector LdgTrijetP4_afterSS;
    LdgTrijetP4_afterSS = LdgTijetJet1_afterSS.p4() + LdgTijetJet2_afterSS.p4() + LdgTijetBJet_afterSS.p4();

    bool isreal_ldgTop  = (isRealMVATop(LdgTijetJet1_afterSS, LdgTijetJet2_afterSS, LdgTijetBJet_afterSS, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet));    
    hTrijetPt_Ldg    -> Fill(LdgTrijetP4_afterSS.Pt());
    hTrijetPt_LdgOrSldg -> Fill(LdgTrijetP4_afterSS.Pt());

    if (isreal_ldgTop){
      hTrijetPt_LdgOrSldg_Matched -> Fill(LdgTrijetP4_afterSS.Pt());
      hTrijetPt_Ldg_Matched       -> Fill(LdgTrijetP4_afterSS.Pt());
      if (cfg_PrelimTopMVACut.passedCut(LdgTrijetMVA_afterSS)){
      hTrijetPt_LdgOrSldg_MatchedBDT -> Fill(LdgTrijetP4_afterSS.Pt());
      hTrijetPt_Ldg_MatchedBDT       -> Fill(LdgTrijetP4_afterSS.Pt());
      }	
    }
    else{
      hTrijetPt_LdgOrSldg_Unmatched -> Fill(LdgTrijetP4_afterSS.Pt());
      hTrijetPt_Ldg_Unmatched       -> Fill(LdgTrijetP4_afterSS.Pt());      
      if (cfg_PrelimTopMVACut.passedCut(LdgTrijetMVA_afterSS)){
      hTrijetPt_LdgOrSldg_UnmatchedBDT -> Fill(LdgTrijetP4_afterSS.Pt());
      hTrijetPt_Ldg_UnmatchedBDT       -> Fill(LdgTrijetP4_afterSS.Pt());      
      }
    }
    

    if (AllTopCandIndexSortPt_cleaned.size() > 1){
      //Subldg in BDT top candidate
      int index2 = AllTopCandIndexSortPt_cleaned.at(1);
      Jet SubldgTijetJet1_afterSS = topData.getAllTopsJet1().at(index2);
      Jet SubldgTijetJet2_afterSS = topData.getAllTopsJet2().at(index2);
      Jet SubldgTijetBJet_afterSS = topData.getAllTopsBJet().at(index2);
      float SubldgTrijetMVA_afterSS = topData.getAllTopsMVA().at(index2);
      
      math::XYZTLorentzVector SubldgTrijetP4_afterSS;
      SubldgTrijetP4_afterSS = SubldgTijetJet1_afterSS.p4() + SubldgTijetJet2_afterSS.p4() + SubldgTijetBJet_afterSS.p4();
      
      if (0){
	std::cout<<"LdgTop "<<LdgTijetJet1_afterSS.index()<<" "<<LdgTijetJet2_afterSS.index()<<" "<<LdgTijetBJet_afterSS.index()<<" "<<LdgTrijetMVA_afterSS<<" "<<LdgTrijetP4_afterSS.Pt()<<std::endl;
	std::cout<<"SubldgTop "<<SubldgTijetJet1_afterSS.index()<<" "<<SubldgTijetJet2_afterSS.index()<<" "<<SubldgTijetBJet_afterSS.index()<<" "<<SubldgTrijetMVA_afterSS<<" "<<SubldgTrijetP4_afterSS.Pt()<<std::endl;
	std::cout<<"==="<<std::endl;
      }
      
      bool isreal_sldgTop = (isRealMVATop(SubldgTijetJet1_afterSS, SubldgTijetJet2_afterSS, SubldgTijetBJet_afterSS, MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet));
      hTrijetPt_Subldg -> Fill(SubldgTrijetP4_afterSS.Pt());
      hTrijetPt_LdgOrSldg -> Fill(SubldgTrijetP4_afterSS.Pt());
      
      if (isreal_sldgTop){
	hTrijetPt_LdgOrSldg_Matched -> Fill(SubldgTrijetP4_afterSS.Pt());
	hTrijetPt_Sldg_Matched      -> Fill(SubldgTrijetP4_afterSS.Pt());
	if (cfg_PrelimTopMVACut.passedCut(SubldgTrijetMVA_afterSS)){
	  hTrijetPt_LdgOrSldg_MatchedBDT -> Fill(SubldgTrijetP4_afterSS.Pt());
	  hTrijetPt_Sldg_MatchedBDT      -> Fill(SubldgTrijetP4_afterSS.Pt());
	}
      }
      else{
	hTrijetPt_LdgOrSldg_Unmatched -> Fill(SubldgTrijetP4_afterSS.Pt());
	hTrijetPt_Sldg_Unmatched      -> Fill(SubldgTrijetP4_afterSS.Pt());
	if (cfg_PrelimTopMVACut.passedCut(SubldgTrijetMVA_afterSS)){
	  hTrijetPt_LdgOrSldg_UnmatchedBDT -> Fill(SubldgTrijetP4_afterSS.Pt());
	  hTrijetPt_Sldg_UnmatchedBDT      -> Fill(SubldgTrijetP4_afterSS.Pt());
	}
      }      
    }

    //======================================
    //======================================
    //Efficiency per Event: Tag both real tops 
    //======================================
    //======================================
    if (topData.getSelectedCleanedTopsBJet().size() < 2) return;
    if (!topData.hasFreeBJet()) return;

    
    if (0){
      std::cout<<"Pass LdgTop "<<topData.getLdgTrijetJet1().index()<<" "<<topData.getLdgTrijetJet2().index()<<" "<<topData.getLdgTrijetBJet().index()<<" "<<topData.getMVALdgInPt()<<std::endl;
      std::cout<<"Pass SubldgTop "<<topData.getSubldgTrijetJet1().index()<<" "<<topData.getSubldgTrijetJet2().index()<<" "<<topData.getSubldgTrijetBJet().index()<<" "<<topData.getMVASubldgInPt()<<std::endl;
      std::cout<<"==="<<std::endl;
    }

    bool realtop1    = isRealMVATop(topData.getTrijet1Jet1(), topData.getTrijet1Jet2(), topData.getTrijet1BJet(), MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);
    bool realtop2    = isRealMVATop(topData.getTrijet2Jet1(), topData.getTrijet2Jet2(), topData.getTrijet2BJet(), MCtrue_LdgJet,  MCtrue_SubldgJet, MCtrue_Bjet);
    bool realtopBoth = realtop1*realtop2;
    bool passBDTboth = cfg_PrelimTopMVACut.passedCut(topData.getMVAmax2());
    // All the top quarks have been matched                                                                                                                 
    if (MCtrue_Bjet.size() == GenTops.size())
      {
	//Efficiency: Both Trijets Matched && Pass BDT
	hEventTrijetPt2T -> Fill(topData.getLdgTrijet().Pt());
	if (realtopBoth){
	  hEventTrijetPt2T_Matched -> Fill(topData.getLdgTrijet().Pt());
	}
	if (passBDTboth){
	  hEventTrijetPt2T_BDT -> Fill(topData.getLdgTrijet().Pt());
	  if (realtopBoth){
	    hEventTrijetPt2T_MatchedBDT -> Fill(topData.getLdgTrijet().Pt());
	  }
	}
      }
  }// if (doMatching)
  
  //================================================================================================
  // 12) Top selection                                                     
  //================================================================================================ 
  if (!topData.passedSelection()) return;
  if (0) std::cout << "=== All Selections" << std::endl;
  cSelected.increment();
    
  //Definitions
  bool haveMatchedChargedHiggsBJet    = HBjet.size() > 0;
  bool haveMatchedTopFromChargedHiggs = HiggsTop_Bjet.size() > 0;
  
  math::XYZTLorentzVector tetrajet_p4, subldgTetrajet_p4;
  
  tetrajet_p4       = topData.getLdgTrijet()    + topData.getTetrajetBJet().p4();
  subldgTetrajet_p4 = topData.getSubldgTetrajet() + topData.getTetrajetBJet().p4();
  
  bool LdgTopIsTopFromH    = false;
  bool SubldgTopIsTopFromH = false;
  bool LdgWIsWFromH        = false;  //LdgW = W from leading Top
  
  bool isBfromH = false;
  if (haveMatchedChargedHiggsBJet) isBfromH = areSameJets(HBjet.at(0), topData.getTetrajetBJet());
  
  
  SelectedTrijet LdgTop, SubldgTop;

  LdgTop.Jet1 = topData.getLdgTrijetJet1();
  LdgTop.Jet2 = topData.getLdgTrijetJet2();
  LdgTop.BJet = topData.getLdgTrijetBJet();
  //topData.getLdgTrijet;
  //LdgTop.TrijetP4;
  if (areSameJets(LdgTop.BJet, topData.getTrijet1BJet())){
    SubldgTop.Jet1 = topData.getTrijet2Jet1();
    SubldgTop.Jet2 = topData.getTrijet2Jet2();
    SubldgTop.BJet = topData.getSubldgTrijetBJet();
  }
  else if (areSameJets(LdgTop.BJet, topData.getTrijet2BJet())){
    SubldgTop.Jet1 = topData.getTrijet1Jet1();
    SubldgTop.Jet2 = topData.getTrijet1Jet2();
    SubldgTop.BJet = topData.getSubldgTrijetBJet();
  }
  else
    {
      std::cout<<"never reach here"<<std::endl;
    }
  if (haveMatchedTopFromChargedHiggs){
    //Leading Top is Top from Higga
    LdgTopIsTopFromH       = isRealMVATop(LdgTop.Jet1, LdgTop.Jet2, LdgTop.BJet, HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0));
    //Subleading Top is Top from Higga
    SubldgTopIsTopFromH    = isRealMVATop(SubldgTop.Jet1, SubldgTop.Jet2, SubldgTop.BJet, HiggsTop_LdgJet.at(0), HiggsTop_SubldgJet.at(0), HiggsTop_Bjet.at(0));
  }

  if (haveMatchedTopFromChargedHiggs){
    bool same1 = areSameJets(LdgTop.Jet1, HiggsTop_LdgJet.at(0)) && areSameJets(LdgTop.Jet2, HiggsTop_SubldgJet.at(0));
    bool same2 = areSameJets(LdgTop.Jet2, HiggsTop_LdgJet.at(0)) && areSameJets(LdgTop.Jet1, HiggsTop_SubldgJet.at(0));
    if (!LdgTopIsTopFromH) LdgWIsWFromH = (same1 || same2);  //If Ldg top not matched: check if W is matched with the W from Higgs                                                     

    // bool sameJ1 = areSameJets(LdgTop.Jet1, HiggsTop_LdgJet.at(0)) || areSameJets(LdgTop.Jet1, HiggsTop_SubldgJet.at(0));
    // bool sameJ2 = areSameJets(LdgTop.Jet2, HiggsTop_LdgJet.at(0)) || areSameJets(LdgTop.Jet2, HiggsTop_SubldgJet.at(0));
    // bool sameB  = areSameJets(LdgTop.BJet, HiggsTop_Bjet.at(0));
    // bool sameJ1B = sameJ1 && sameB;
    // bool sameJ2B = sameJ2 && sameB;
    //if (!LdgTopIsTopFromH && !LdgWIsWFromH) LdgJBIsJBFromH = (sameJ1B || sameJ2B);  //If Ldg top not matched: check if W is matched with the W from Higgs                              
  }

  double LdgTrijet_Rapidity = 0.5*log((topData.getLdgTrijet().E() + topData.getLdgTrijet().Pz())/(topData.getLdgTrijet().E() - topData.getLdgTrijet().Pz()));
  double SubldgTrijet_Rapidity = 0.5*log((topData.getSubldgTrijet().E() + topData.getSubldgTrijet().Pz())/(topData.getSubldgTrijet().E() - topData.getSubldgTrijet().Pz()));
  double TetrajetBjet_Rapidity = 0.5*log((topData.getTetrajetBJet().p4().E() + topData.getTetrajetBJet().p4().Pz())/
					 (topData.getTetrajetBJet().p4().E() - topData.getTetrajetBJet().p4().Pz()));

  double dR12Ldg = ROOT::Math::VectorUtil::DeltaR(LdgTop.Jet1.p4(), LdgTop.Jet2.p4());
  double dR1bLdg = ROOT::Math::VectorUtil::DeltaR(LdgTop.Jet1.p4(), LdgTop.BJet.p4());
  double dR2bLdg = ROOT::Math::VectorUtil::DeltaR(LdgTop.Jet2.p4(), LdgTop.BJet.p4());

  double dRLdg_min = min(min(dR12Ldg, dR1bLdg), dR2bLdg);
  double dRLdg_max = max(max(dR12Ldg, dR1bLdg), dR2bLdg);

  double dR12Subldg = ROOT::Math::VectorUtil::DeltaR(SubldgTop.Jet1.p4(), SubldgTop.Jet2.p4());
  double dR1bSubldg = ROOT::Math::VectorUtil::DeltaR(SubldgTop.Jet1.p4(), SubldgTop.BJet.p4());
  double dR2bSubldg = ROOT::Math::VectorUtil::DeltaR(SubldgTop.Jet2.p4(), SubldgTop.BJet.p4());

  double dRSubldg_min = min(min(dR12Subldg, dR1bSubldg), dR2bSubldg);
  double dRSubldg_max = max(max(dR12Subldg, dR1bSubldg), dR2bSubldg);

  double deltaR_LdgTrijet_TetrajetBjet = ROOT::Math::VectorUtil::DeltaR(topData.getLdgTrijet(), topData.getTetrajetBJet().p4());
  double deltaR_SubldgTrijet_TetrajetBjet = ROOT::Math::VectorUtil::DeltaR(topData.getSubldgTrijet(), topData.getTetrajetBJet().p4());

  double deltaR_LdgTrijetDijet_LdgTrijetBjet = ROOT::Math::VectorUtil::DeltaR(topData.getLdgTrijetDijet(), LdgTop.BJet.p4());
  double deltaR_LdgTrijetDijet               = ROOT::Math::VectorUtil::DeltaR(LdgTop.Jet1.p4(), LdgTop.Jet2.p4());

  double deltaEta_LdgTrijet_TetrajetBjet = std::abs(topData.getLdgTrijet().Eta() - topData.getTetrajetBJet().eta());
  double deltaEta_SubldgTrijet_TetrajetBjet = std::abs(topData.getSubldgTrijet().Eta() - topData.getTetrajetBJet().eta());

  double deltaPhi_LdgTrijet_TetrajetBjet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(topData.getLdgTrijet(), topData.getTetrajetBJet().p4()));
  double deltaPhi_SubldgTrijet_TetrajetBjet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(topData.getSubldgTrijet(), topData.getTetrajetBJet().p4()));

  double deltaY_LdgTrijet_TetrajetBjet = std::abs(LdgTrijet_Rapidity - TetrajetBjet_Rapidity);
  double deltaY_SubldgTrijet_TetrajetBjet = std::abs(SubldgTrijet_Rapidity - TetrajetBjet_Rapidity);

  //Fill Histograms
  //Pt
  hLdgTrijetPt         -> Fill(LdgTopIsTopFromH, topData.getLdgTrijet().Pt());
  hLdgTrijetDijetPt    -> Fill(LdgTopIsTopFromH, topData.getLdgTrijetDijet().Pt());
  hLdgTrijetBjetPt     -> Fill(LdgTopIsTopFromH, LdgTop.BJet.pt());
  hTetrajetBjetPt      -> Fill(LdgTopIsTopFromH, topData.getTetrajetBJet().pt());
  hLdgTrijet_DeltaR_Dijet_TrijetBjet      -> Fill(LdgTopIsTopFromH, deltaR_LdgTrijetDijet_LdgTrijetBjet);
  hLdgTrijet_DeltaR_Dijet                 -> Fill(LdgTopIsTopFromH, deltaR_LdgTrijetDijet);
  hSubldgTrijetPt      -> Fill(SubldgTopIsTopFromH, topData.getSubldgTrijet().Pt());
  hSubldgTrijetDijetPt -> Fill(SubldgTopIsTopFromH, topData.getSubldgTrijetDijet().Pt());

  //DeltaEta, DeltaPhi, DeltaR, DeltaY
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

  //Invariant Mass reconstruction
  //Boolean defines if tetrajetBjet is correctly identified
  hTetrajetMass -> Fill(isBfromH, tetrajet_p4.M());
  hTetrajetBjetBDisc -> Fill(isBfromH, topData.getTetrajetBJet().bjetDiscriminator());
  hTetrajetPt -> Fill(isBfromH, tetrajet_p4.Pt());

  if (LdgTopIsTopFromH){
    hTetrajetMass_LdgTopIsHTop    -> Fill(isBfromH, tetrajet_p4.M());
    hTetrajetPt_LdgTopIsHTop      -> Fill(isBfromH, tetrajet_p4.Pt());
  }
  else{
    hTetrajetMass_TopUnmatched    -> Fill(isBfromH, tetrajet_p4.M());
  }
  if (SubldgTopIsTopFromH)    hTetrajetMass_SubldgTopIsHTop -> Fill(isBfromH, subldgTetrajet_p4.M());
  if (LdgWIsWFromH)           hTetrajetMass_LdgWIsWfromH    -> Fill(isBfromH, tetrajet_p4.M());

  hLdgInPtTrijetBDT     -> Fill(topData.getMVALdgInPt());
  hSubldgInPtTrijetBDT  -> Fill(topData.getMVASubldgInPt());
  hLdgInBDTTrijetBDT    -> Fill(topData.getMVAmax1());
  hSubldgInBDTTrijetBDT -> Fill(topData.getMVAmax2());

  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
