// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/Registry.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/PtrVector.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/TauReco/interface/L2TauInfoAssociation.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/L1Trigger/interface/L1EtMissParticle.h"
#include "DataFormats/L1Trigger/interface/L1EtMissParticleFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetupFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMap.h"
//#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMaps.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"

#include "HiggsAnalysis/TriggerEfficiency/interface/MuonAnalyzer.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/LorentzVectorFwd.h"

#include "CMGTools/External/interface/PileupJetIdentifier.h"

#include "TH1F.h"
#include "TTree.h"
#include "TFile.h"

class TTEffAnalyzer2: public edm::EDAnalyzer {
public:
  explicit TTEffAnalyzer2(const edm::ParameterSet&);
  ~TTEffAnalyzer2();

private:
  typedef math::XYZTLorentzVector LorentzVector;

  void analyze(const edm::Event&, const edm::EventSetup&);
  void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);
  void endJob() ;

  void reset();
  int MCMatch(const edm::Event&,const reco::Candidate&);
  double L1EtmCorrection(double,const edm::Event&);
  double L1EtmCorrectionAlgo(double, double, double);

  // Input stuff
  edm::InputTag hltResultsSrc_;
  edm::InputTag hltEventSrc_;
  edm::InputTag hltFilterSrc_;
  edm::InputTag pfTauSrc_;
  edm::InputTag pileupSummaryInfoSrc_;
  edm::InputTag pfJetSrc_;
  edm::InputTag pfJetPUIDFlagSrc_;

  edm::InputTag lheSrc;
  edm::InputTag visibleTauSrc;
  edm::InputTag genParticleSrc;
  double MCMatchingCone;

  edm::InputTag offlinePrimaryVertexSrc_;

  edm::InputTag l1TauSrc_;
  edm::InputTag l1CenSrc_;
  edm::InputTag l1MetSrc_;
  edm::InputTag l1MhtSrc_;
//  edm::InputTag l1GtReadoutRecordSrc_;
  edm::InputTag l1GtObjectMapRecordSrc_;
  double l1JetMatchingCone_;
  bool l1SelectNearest_;

  edm::InputTag l2TauInfoAssocSrc_;
  double l2JetMatchingCone_;

  edm::InputTag primaryVertexSrc_;
  edm::InputTag l25TauSrc_;
  double l25TauMatchingCone_;
  double l25FilterMinTrackPt_;
  unsigned l25FilterMinPixelHits_;
  unsigned l25FilterMinTrackerHits_;
  double l25FilterMaxIP_;
  double l25FilterMaxChi2_;
  double l25FilterMaxDeltaZ_;
  double l25FilterMinGammaEt_;

  edm::InputTag patTriggerEventSrc;

  std::string rootFile_;
  std::vector<edm::InputTag> counters_;

  edm::InputTag topPtWeightSrc_;

  struct TriggerBit {
    TriggerBit(const std::string& n): name(n), value(false) {}
    void book(TTree *tree) {
      tree->Branch(name.c_str(), &value);
    }
    void reset() { value=false; }
    std::string name;
    bool value;
  };

  struct TriggerFilter {
    TriggerFilter(const edm::InputTag& f): filter(f) {}
    void book(TTree *tree, const std::string& prefix) {
      tree->Branch((prefix+filter.label()).c_str(), &values);
    }
    void reset() {
      objects.clear();
      values.clear();
    }
    edm::InputTag filter;
    std::vector<trigger::TriggerObject> objects;
    std::vector<bool> values;
  };

  struct MET {
    MET(const edm::InputTag& s, const std::string& n): src(s), name(n) {}
    void book(TTree *tree) {
      tree->Branch((name+"_ET").c_str(), &et);
      tree->Branch((name+"_phi").c_str(), &phi);
    }
    void fill(const edm::Event& iEvent) {
      edm::Handle<edm::View<reco::MET> > hmet;
//      edm::Handle<edm::View<pat::MET> > hmet;
      if(iEvent.getByLabel(src, hmet)){
        et = hmet->front().pt();
        phi = hmet->front().phi();
      }
    }
    void reset() { et=0; phi=0;}
    edm::InputTag src;
    std::string name;
    float et;
    float phi;
  };

  struct Selection {
    Selection(const std::string& n): name(n) {}
    void book(TTree *tree) {
      tree->Branch((name).c_str(), &value);
    }
    void fill(const edm::Event& iEvent) {
      edm::Handle<bool> hsele;
      if(iEvent.getByLabel(edm::InputTag(name,""), hsele)){
	value = *hsele;
      }
    }
    void reset() { value = -1;}

    std::string name;
    int value;
  };

  struct Discriminator {
    Discriminator(const std::string& n): name(n) {}
    std::string name;
    std::vector<float> values;
  };

  struct L25Discriminator {
    L25Discriminator(const edm::InputTag& s, const std::string& n): src(s), name(n) {}
    edm::InputTag src;
    edm::Handle<reco::PFTauDiscriminator> handle;
    std::string name;
    std::vector<float> values;
  };

  struct OtherTau {
    OtherTau(const edm::InputTag& s, const std::string& n): src(s), name(n) {}
    edm::InputTag src;
    edm::Handle<edm::View<reco::PFTau> > handle;
    std::string name;
    std::vector<bool> values;
  };

  // Branches
  uint32_t event_, run_, lumi_;
  float nPU_;
  int NUP;
  bool primaryVertexIsValid_;
  unsigned nGoodOfflinePV_;
  float topPtWeight_;
  std::vector<TriggerBit> l1Bits_;
  std::vector<TriggerBit> hltBits_;
  std::vector<MET> METs_;

  std::vector<float> PFTauPt_;
  std::vector<float> PFTauEt_;
  std::vector<float> PFTauEta_;
  std::vector<float> PFTauPhi_;
  std::vector<float> PFTauLeadChargedHadrCandPt_;
  std::vector<float> PFTauProng_;
  std::vector<Discriminator> PFTauDiscriminators_;
  std::vector<float> PFTauJetMinDR_;
  std::vector<int> PFTauMCMatch_;

  std::vector<float> PFJetPt_;
  std::vector<float> PFJetEta_;
  std::vector<float> PFJetPhi_;
  std::vector<int> PFJetMCMatch_;
  std::vector<bool> PFJet_JetPUIDloose_;
  std::vector<bool> PFJet_JetPUIDmedium_;
  std::vector<bool> PFJet_JetPUIDtight_;

  // L1 per-event
  float L1MET_;
  float L1METcorr_;
  float L1MHT_;

  std::vector<bool> l1JetIsTau_;
  std::vector<float> l1JetPt_;
  std::vector<float> l1JetEt_;
  std::vector<unsigned> l1JetRank_;
  std::vector<float> l1JetEta_;
  std::vector<float> l1JetPhi_;

  std::vector<int> PFTau_matchedL1_;
  std::vector<unsigned> PFTau_l1JetsInMatchingCone_;
  std::vector<float> PFTau_l1JetMatchDR_;

  std::vector<int> PFJet_matchedL1_;
  std::vector<unsigned> PFJet_l1JetsInMatchingCone_;
  std::vector<float> PFJet_l1JetMatchDR_;

  std::vector<int> PFTau_matchedHLTObject_;
  std::vector<TriggerFilter> PFTau_matchedHLTObjectFilters_;


  // L2 per-tau
  std::vector<bool> l2HasMatchedL2Jet_;
  std::vector<float> l2JetPt_;
  std::vector<float> l2JetEt_;
  std::vector<float> l2JetEta_;
  std::vector<float> l2JetPhi_;

  // L25 per-tau
  std::vector<bool> l25HasMatchedL25Tau_;
  std::vector<float> l25TauPt_;
  std::vector<float> l25TauEt_;
  std::vector<float> l25TauEta_;
  std::vector<float> l25TauPhi_;
  std::vector<bool> l25TauLeadChargedHadrCandExists_;
  std::vector<float> l25TauLeadChargedHadrCandPt_;
  std::vector<float> l25TauIsoChargedHadrCandPtMax_;
  std::vector<float> l25TauIsoGammaCandEtMax_;
  std::vector<unsigned> l25TauProng_;
  std::vector<L25Discriminator> l25TauDiscriminators_;
  std::vector<OtherTau> l25TauSelectedTaus_;
  std::vector<Selection> selections;

  bool triggerBitsOnly;

  MuonAnalyzer* muonAnalyzer;
  TTree *tree_;
  TFile *file_;

  TH1F *h_counters_;
};

TTEffAnalyzer2::TTEffAnalyzer2(const edm::ParameterSet& iConfig):
  hltResultsSrc_(iConfig.getParameter<edm::InputTag>("HltResults")),
  hltEventSrc_(iConfig.getParameter<edm::InputTag>("TriggerEvent")),
  hltFilterSrc_(iConfig.getParameter<edm::InputTag>("HltObjectLastFilter")),
  pfTauSrc_(iConfig.getParameter<edm::InputTag>("LoopingOver")),
  pileupSummaryInfoSrc_(iConfig.getParameter<edm::InputTag>("PileupSummaryInfoSource")),
  pfJetSrc_(iConfig.getParameter<edm::InputTag>("Jets")),
  pfJetPUIDFlagSrc_(iConfig.getParameter<edm::InputTag>("JetPUIDsrc")),
  lheSrc(iConfig.getParameter<edm::InputTag>("lheSrc")),
  visibleTauSrc(iConfig.getParameter<edm::InputTag>("VisibleTauSrc")),
  genParticleSrc(iConfig.getParameter<edm::InputTag>("GenParticleCollection")),
  MCMatchingCone(iConfig.getParameter<double>("MCMatchingCone")),
  offlinePrimaryVertexSrc_(iConfig.getParameter<edm::InputTag>("offlineVertexSrc")),
  l1TauSrc_(iConfig.getParameter<edm::InputTag>("L1extraTauJetSource")),
  l1CenSrc_(iConfig.getParameter<edm::InputTag>("L1extraCentralJetSource")),
  l1MetSrc_(iConfig.getParameter<edm::InputTag>("L1extraMETSource")),
  l1MhtSrc_(iConfig.getParameter<edm::InputTag>("L1extraMHTSource")),
//  l1GtReadoutRecordSrc_(iConfig.getParameter<edm::InputTag>("L1GtReadoutRecord")),
  l1GtObjectMapRecordSrc_(iConfig.getParameter<edm::InputTag>("L1GtObjectMapRecord")),
  l1JetMatchingCone_(iConfig.getParameter<double>("L1JetMatchingCone")),
  l2TauInfoAssocSrc_(iConfig.getParameter<edm::InputTag>("L2AssociationCollection")),
  l2JetMatchingCone_(iConfig.getParameter<double>("L2matchingDeltaR")),
  primaryVertexSrc_(iConfig.getParameter<edm::InputTag>("hltVertexSrc")),
  l25TauSrc_(iConfig.getParameter<edm::InputTag>("L25TauSource")),
  l25TauMatchingCone_(iConfig.getParameter<double>("L25MatchingCone")),
  patTriggerEventSrc(iConfig.getParameter<edm::InputTag>("PatTriggerEvent")),
  rootFile_(iConfig.getParameter<std::string>("outputFileName")),
  counters_(iConfig.getParameter<std::vector<edm::InputTag> >("Counters")),
  topPtWeightSrc_(iConfig.getParameter<edm::InputTag>("TopPtWeight")),
  triggerBitsOnly(iConfig.getParameter<bool>("triggerBitsOnly"))
{
  std::string l1MatchMode = iConfig.getParameter<std::string>("L1JetMatchingMode");
  if(l1MatchMode == "nearestDR")
    l1SelectNearest_ = true;
  else if(l1MatchMode == "highestEt")
    l1SelectNearest_ = false;
  else
    throw cms::Exception("Configuration") << "L1JetMatchingMode should be 'nearestDR' or 'highestEt', was '" << l1MatchMode << "'" << std::endl;

  std::vector<edm::InputTag> hltFilters = iConfig.getParameter<std::vector<edm::InputTag> >("HltObjectFilters");
  for(size_t i=0; i<hltFilters.size(); ++i) {
    PFTau_matchedHLTObjectFilters_.push_back(TriggerFilter(hltFilters[i]));
  }

  edm::ParameterSet qualityCuts = iConfig.getParameter<edm::ParameterSet>("L3IsoQualityCuts");
  l25FilterMinTrackPt_ = qualityCuts.getParameter<double>("minTrackPt");
  l25FilterMinPixelHits_ = qualityCuts.getParameter<unsigned>("minTrackPixelHits");
  l25FilterMinTrackerHits_ = qualityCuts.getParameter<unsigned>("minTrackHits");
  l25FilterMaxIP_ = qualityCuts.getParameter<double>("maxTransverseImpactParameter");
  l25FilterMaxChi2_ = qualityCuts.getParameter<double>("maxTrackChi2");
  l25FilterMaxDeltaZ_ = qualityCuts.getParameter<double>("maxDeltaZ");
  l25FilterMinGammaEt_ = qualityCuts.getParameter<double>("minGammaEt");


  std::vector<std::string> l1Names = iConfig.getParameter<std::vector<std::string> >("L1Paths");
  l1Bits_.reserve(l1Names.size());
  for(size_t i=0; i<l1Names.size(); ++i)
    l1Bits_.push_back(TriggerBit(l1Names[i]));

  std::vector<std::string> hltNames = iConfig.getParameter<std::vector<std::string> >("HltPaths");
  hltBits_.reserve(hltNames.size());
  for(size_t i=0; i<hltNames.size(); ++i)
    hltBits_.push_back(TriggerBit(hltNames[i]));


  std::vector<std::string> dNames = iConfig.getParameter<std::vector<std::string> >("PFTauDiscriminators");
  PFTauDiscriminators_.reserve(dNames.size());
  for(size_t i=0; i<dNames.size(); ++i)
    PFTauDiscriminators_.push_back(Discriminator(dNames[i]));

  edm::ParameterSet mets = iConfig.getParameter<edm::ParameterSet>("METs");
  std::vector<std::string> metNames = mets.getParameterNames();
  METs_.reserve(metNames.size());
  for(size_t i=0; i<metNames.size(); ++i){
    METs_.push_back(MET(mets.getParameter<edm::InputTag>(metNames[i]), metNames[i]));
  }

  edm::ParameterSet l25Discs = iConfig.getParameter<edm::ParameterSet>("L25Discriminators");
  std::vector<std::string> l25Names = l25Discs.getParameterNames();
  l25TauDiscriminators_.reserve(l25Names.size());
  for(size_t i=0; i<l25Names.size(); ++i)
    l25TauDiscriminators_.push_back(L25Discriminator(l25Discs.getParameter<edm::InputTag>(l25Names[i]), l25Names[i]));

  edm::ParameterSet l25Selections = iConfig.getParameter<edm::ParameterSet>("L25Selections");
  l25Names = l25Selections.getParameterNames();
  l25TauSelectedTaus_.reserve(l25Names.size());
  for(size_t i=0; i<l25Names.size(); ++i)
    l25TauSelectedTaus_.push_back(OtherTau(l25Selections.getParameter<edm::InputTag>(l25Names[i]), l25Names[i]));

  std::vector<std::string> seleNames = iConfig.getParameter<std::vector<std::string> >("Selections");
  selections.reserve(seleNames.size());
  for(size_t i=0; i<seleNames.size(); ++i)
    selections.push_back(Selection(seleNames[i]));

  // File setup
  file_ = TFile::Open(rootFile_.c_str(), "RECREATE");
  //_TTEffFile = TFile::Open("test.root", "RECREATE");
  // Tree setup
  tree_ = new TTree("TTEffTree", "Tau Trigger Efficiency Tree");

  tree_->Branch("event", &event_);
  tree_->Branch("run", &run_);
  tree_->Branch("lumi", &lumi_);

  tree_->Branch("MCNPU", &nPU_);
  tree_->Branch("MCNUP", &NUP);
  tree_->Branch("numGoodOfflinePV", &nGoodOfflinePV_);
  tree_->Branch("topPtWeight", &topPtWeight_);
  tree_->Branch("primaryVertexIsValid", &primaryVertexIsValid_);

  for(size_t i=0; i<l1Bits_.size(); ++i)
    l1Bits_[i].book(tree_);
  for(size_t i=0; i<hltBits_.size(); ++i)
    hltBits_[i].book(tree_);
  for(size_t i=0; i<METs_.size(); ++i)
    METs_[i].book(tree_);

  tree_->Branch("L1MET", &L1MET_);
  tree_->Branch("L1MHT", &L1MHT_);
  tree_->Branch("L1METcorr", &L1METcorr_);

  tree_->Branch("PFTauPt", &PFTauPt_);
  tree_->Branch("PFTauEt", &PFTauEt_);
  tree_->Branch("PFTauEta", &PFTauEta_);
  tree_->Branch("PFTauPhi", &PFTauPhi_);
  tree_->Branch("PFTauLeadChargedHadrCandPt", &PFTauLeadChargedHadrCandPt_);
  tree_->Branch("PFTauProng", &PFTauProng_);

  for(size_t i = 0; i < PFTauDiscriminators_.size(); ++i)
    tree_->Branch(("PFTau_"+PFTauDiscriminators_[i].name).c_str(), &(PFTauDiscriminators_[i].values));

  tree_->Branch("PFTauJetMinDR", &PFTauJetMinDR_);
  tree_->Branch("PFTauMCMatch", &PFTauMCMatch_);

  tree_->Branch("PFJetPt", &PFJetPt_);
  tree_->Branch("PFJetEta", &PFJetEta_);
  tree_->Branch("PFJetPhi", &PFJetPhi_);
  tree_->Branch("PFJetMCMatch", &PFJetMCMatch_);
  tree_->Branch("PFJetPUIDloose", &PFJet_JetPUIDloose_);
  tree_->Branch("PFJetPUIDmedium", &PFJet_JetPUIDmedium_);
  tree_->Branch("PFJetPUIDtight", &PFJet_JetPUIDtight_);

  tree_->Branch("L1JetIsTau", &l1JetIsTau_);
  tree_->Branch("L1JetPt", &l1JetPt_);
  tree_->Branch("L1JetEt", &l1JetEt_);
  tree_->Branch("L1JetRank", &l1JetRank_);
  tree_->Branch("L1JetEta", &l1JetEta_);
  tree_->Branch("L1JetPhi", &l1JetPhi_);

  tree_->Branch("PFTau_matchedL1", &PFTau_matchedL1_);
  tree_->Branch("PFTau_l1JetsInMatchingCone_", &PFTau_l1JetsInMatchingCone_);
  tree_->Branch("PFTau_l1JetMatchDR", &PFTau_l1JetMatchDR_);

  tree_->Branch("PFJet_matchedL1", &PFJet_matchedL1_);
  tree_->Branch("PFJet_l1JetsInMatchingCone_", &PFJet_l1JetsInMatchingCone_);
  tree_->Branch("PFJet_l1JetMatchDR", &PFJet_l1JetMatchDR_);

  tree_->Branch("PFTau_matchedHLTObject", &PFTau_matchedHLTObject_);
  for(size_t i=0; i<PFTau_matchedHLTObjectFilters_.size(); ++i) {
    PFTau_matchedHLTObjectFilters_[i].book(tree_, "PFTau_matchedHLTObject_");
  }

  tree_->Branch("hasMatchedL2Jet", &l2HasMatchedL2Jet_);
  tree_->Branch("L2JetPt", &l2JetPt_);
  tree_->Branch("L2JetEt", &l2JetEt_);
  tree_->Branch("L2JetEta", &l2JetEta_);
  tree_->Branch("L2JetPhi", &l2JetPhi_);

  tree_->Branch("hasMatchedL25Tau", &l25HasMatchedL25Tau_);
  tree_->Branch("L25TauPt", &l25TauPt_);
  tree_->Branch("L25TauEt", &l25TauEt_);
  tree_->Branch("L25TauEta", &l25TauEta_);
  tree_->Branch("L25TauPhi", &l25TauPhi_);
  tree_->Branch("L25TauLeadChargedHadrCandExists", &l25TauLeadChargedHadrCandExists_);
  tree_->Branch("L25TauLeadChargedHadrCandPt", &l25TauLeadChargedHadrCandPt_);
  tree_->Branch("L25TauIsoChargedHadrCandPtMax", &l25TauIsoChargedHadrCandPtMax_);
  tree_->Branch("L25TauIsoGammaCandEtMax", &l25TauIsoGammaCandEtMax_);
  tree_->Branch("L25TauProng", &l25TauProng_);

  for(size_t i=0; i<l25TauDiscriminators_.size(); ++i)
    tree_->Branch(("L25Tau_"+l25TauDiscriminators_[i].name).c_str(), &l25TauDiscriminators_[i].values);

  for(size_t i=0; i<l25TauSelectedTaus_.size(); ++i)
    tree_->Branch(("L25Tau_"+l25TauSelectedTaus_[i].name).c_str(), &l25TauSelectedTaus_[i].values);

  for(size_t i = 0; i < selections.size(); ++i)
    tree_->Branch((selections[i].name).c_str(), &(selections[i].value));

  h_counters_ = new TH1F("Counters","",counters_.size(),0,counters_.size());
  h_counters_->SetDirectory(file_);

  muonAnalyzer = new MuonAnalyzer();
  muonAnalyzer->Setup(iConfig,tree_);

  reset();
}

TTEffAnalyzer2::~TTEffAnalyzer2() {}

void TTEffAnalyzer2::reset() {
  event_ = 0;
  run_ = 0;
  lumi_ = 0;

  nPU_ = 0;
  NUP = 0;
  primaryVertexIsValid_ = false;
  nGoodOfflinePV_ = 0;
  topPtWeight_ = 1;

  for(size_t i=0; i<l1Bits_.size(); ++i)
    l1Bits_[i].reset();
  for(size_t i=0; i<hltBits_.size(); ++i)
    hltBits_[i].reset();

  for(size_t i=0; i<METs_.size(); ++i) {
    METs_[i].reset();
  }
  L1MET_ = 0;
  L1METcorr_ = 0;
  L1MHT_ = 0;

  PFTauPt_.clear();
  PFTauEt_.clear();
  PFTauEta_.clear();
  PFTauPhi_.clear();
  PFTauLeadChargedHadrCandPt_.clear();
  PFTauProng_.clear();
  for(size_t i=0; i<PFTauDiscriminators_.size(); ++i)
    PFTauDiscriminators_[i].values.clear();
  PFTauJetMinDR_.clear();
  PFTauMCMatch_.clear();

  PFJetPt_.clear();
  PFJetEta_.clear();
  PFJetPhi_.clear();
  PFJetMCMatch_.clear();
  PFJet_JetPUIDloose_.clear();
  PFJet_JetPUIDmedium_.clear();
  PFJet_JetPUIDtight_.clear();

  l1JetIsTau_.clear();
  l1JetPt_.clear();
  l1JetEt_.clear();
  l1JetRank_.clear();
  l1JetEta_.clear();
  l1JetPhi_.clear();
  l1JetPhi_.clear();

  PFTau_matchedL1_.clear();
  PFTau_l1JetsInMatchingCone_.clear();
  PFTau_l1JetMatchDR_.clear();
  PFTau_matchedHLTObject_.clear();
  for(size_t i=0; i<PFTau_matchedHLTObjectFilters_.size(); ++i) {
    PFTau_matchedHLTObjectFilters_[i].reset();
  }

  PFJet_matchedL1_.clear();
  PFJet_l1JetsInMatchingCone_.clear();
  PFJet_l1JetMatchDR_.clear();

  l2HasMatchedL2Jet_.clear();
  l2JetPt_.clear();
  l2JetEt_.clear();
  l2JetEta_.clear();
  l2JetPhi_.clear();

  l25HasMatchedL25Tau_.clear();
  l25TauPt_.clear();
  l25TauEt_.clear();
  l25TauEta_.clear();
  l25TauPhi_.clear();
  l25TauLeadChargedHadrCandExists_.clear();
  l25TauLeadChargedHadrCandPt_.clear();
  l25TauIsoChargedHadrCandPtMax_.clear();
  l25TauIsoGammaCandEtMax_.clear();
  l25TauProng_.clear();
  for(size_t i=0; i<l25TauDiscriminators_.size(); ++i)
    l25TauDiscriminators_[i].values.clear();
  for(size_t i=0; i<l25TauSelectedTaus_.size(); ++i)
    l25TauSelectedTaus_[i].values.clear();
  for(size_t i=0; i<selections.size(); ++i)
    selections[i].reset();
}

int TTEffAnalyzer2::MCMatch(const edm::Event& iEvent,const reco::Candidate& direction){

  std::vector<std::pair<int,double> > foundInCone;

  edm::Handle<std::vector<math::XYZTLorentzVectorD> > mcTaus;
  if(iEvent.getByLabel(visibleTauSrc,mcTaus)){
    for(size_t i = 0; i < mcTaus->size(); ++i){
	double DR = ROOT::Math::VectorUtil::DeltaR(direction.p4(),mcTaus->at(i));
	if( DR < MCMatchingCone ){
	    foundInCone.push_back(std::pair<int,double>(15,DR));
	    break;
	}
    }
  }

  edm::Handle <reco::GenParticleCollection> genParticles;
  if(iEvent.getByLabel(genParticleSrc, genParticles)){
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if(abs(id) == 22) continue; // not interested in photons..
      double DR = ROOT::Math::VectorUtil::DeltaR(direction.p4(),p.p4());
      if( DR < MCMatchingCone ){
        foundInCone.push_back(std::pair<int,double>(id,DR));
      }
    }
  }
  bool tauFound = false;
  bool eFound   = false;
  bool muFound  = false;
  bool bFound   = false;
  bool cFound   = false;
  for(size_t i = 0; i < foundInCone.size();++i){
    if(abs(foundInCone[i].first) == 15) tauFound = true;
    if(abs(foundInCone[i].first) == 11) eFound   = true;
    if(abs(foundInCone[i].first) == 13) muFound  = true;
    if(abs(foundInCone[i].first) == 5)  bFound   = true;
    if(abs(foundInCone[i].first) == 4)  cFound   = true;

    //std::cout << "check foundInCone " << foundInCone[i].first << " " << foundInCone[i].second << std::endl;
  }
  int mcMatch = 0;
  if(tauFound) mcMatch = 15;
  if(eFound)   mcMatch = 11;
  if(muFound)  mcMatch = 13;
  if(cFound)   mcMatch = 4;
  if(bFound)   mcMatch = 5;

  //std::cout << "check mcMatch " << mcMatch << std::endl;
  return mcMatch;
}

double TTEffAnalyzer2::L1EtmCorrection(double L1ETM,const edm::Event& iEvent){

    edm::InputTag caloMETnoHFsrc = edm::InputTag("patCaloMETnoHF");
    edm::InputTag caloMETnoHFsrcResidualCorrected = edm::InputTag("patResidualCorrectedCaloMETnoHF");

    edm::Handle<edm::View<pat::MET> > hCaloMETnoHF;
    edm::Handle<edm::View<pat::MET> > hCaloMETnoHFresidualCorrected;

    if(iEvent.getByLabel(caloMETnoHFsrc, hCaloMETnoHF) && iEvent.getByLabel(caloMETnoHFsrcResidualCorrected, hCaloMETnoHFresidualCorrected)){
	double caloMETnoHF = hCaloMETnoHF->front().et();
	double caloMETnoHFresidualCorrected = hCaloMETnoHFresidualCorrected->front().et();

	return L1EtmCorrectionAlgo(L1ETM,caloMETnoHF,caloMETnoHFresidualCorrected);
    }else{
	return L1ETM;
    }
}

double TTEffAnalyzer2::L1EtmCorrectionAlgo(double L1ETM, double caloMETnoHF, double caloMETnoHFresidualCorrected){

    double R = 0.9322;
    double H = -0.1172+0.0499*log(caloMETnoHF);
    double K = 0.6693;

    double L1etmScaleCorr = L1ETM*caloMETnoHFresidualCorrected/caloMETnoHF*R;
    double correctedL1ETM = L1etmScaleCorr + H*(L1etmScaleCorr - K*caloMETnoHF);

    return correctedL1ETM;
}

void TTEffAnalyzer2::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  event_ = iEvent.id().event();
  run_ = iEvent.run();
  lumi_ = iEvent.luminosityBlock();

  // Amount of PU
  edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
  iEvent.getByLabel(pileupSummaryInfoSrc_, hpileup);
  if(hpileup.isValid()) { // protection for data
    for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV) {
      if(iPV->getBunchCrossing() == 0) {
        nPU_ = iPV->getTrueNumInteractions();
        break;
      }
    }
  }

  // number of jets for combining WJets inclusive with exclusive
  edm::Handle<LHEEventProduct> hlhe;
  if(iEvent.getByLabel(lheSrc, hlhe)){
    NUP = hlhe->hepeup().NUP;
  }

  // PV
  nGoodOfflinePV_ = 0;
  edm::Handle<edm::View<reco::Vertex> > hoffvertex;
  if(iEvent.getByLabel(offlinePrimaryVertexSrc_, hoffvertex)){
    nGoodOfflinePV_ = hoffvertex->size();  
  }

  // Top pt weight
  edm::Handle<double> hTopPtWeight;
  if(iEvent.getByLabel(topPtWeightSrc_, hTopPtWeight)){
    topPtWeight_ = *hTopPtWeight;
  }

  // Selections
  for(size_t i=0; i<selections.size(); ++i) {
    selections[i].fill(iEvent);
  }

  // HLT bits
  edm::Handle<edm::TriggerResults> hltresults;
  iEvent.getByLabel(hltResultsSrc_, hltresults);
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*hltresults);
  for(size_t i=0; i<hltBits_.size(); ++i) {
    size_t itrig = triggerNames.triggerIndex(hltBits_[i].name);
    if(itrig == triggerNames.size()) {
      hltBits_[i].value = false;
      continue;
    }
    hltBits_[i].value = hltresults->accept(itrig);
  }

  // HLT objects.,.
  std::vector<trigger::TriggerObject> hltObjects;
  edm::Handle<trigger::TriggerEvent> triggerObjs;
  if(iEvent.getByLabel(hltEventSrc_,triggerObjs)){
	const trigger::TriggerObjectCollection objs(triggerObjs->getObjects());
	/* uncomment to get a list of available trigger objects
        for(size_t i = 0; i < objs.size(); ++i){
                std::cout << "    trigger objs pt,eta,phi: " << i << " "
                          << objs[i].pt() << " " << objs[i].eta() << " " << objs[i].phi() << std::endl;
        }
	*/
	size_t index = triggerObjs->filterIndex(hltFilterSrc_);
	//std::cout << "Filter index " << hltFilterSrc_.label() << " " << index << std::endl;
	if(index < triggerObjs->sizeFilters()){
            const trigger::Keys& KEYS(triggerObjs->filterKeys(index));
            //std::cout << "KEYS size " << KEYS.size() << std::endl;
            for(size_t i = 0;i<KEYS.size();++i){
                //std::cout << "KEYS " << KEYS[i] << " " << objs.size() << std::endl;
                const trigger::TriggerObject& TO(objs[KEYS[i]]);
                //std::cout << "TriggerObject pt,eta,phi: " << TO.pt() << " "
                //          << TO.eta() << " " << TO.phi() << std::endl;
		hltObjects.push_back(TO);
            }
	}
        for(size_t m=0; m<PFTau_matchedHLTObjectFilters_.size(); ++m) {
          index = triggerObjs->filterIndex(PFTau_matchedHLTObjectFilters_[m].filter);
          if(index < triggerObjs->sizeFilters()) {
            const trigger::Keys& KEYS(triggerObjs->filterKeys(index));
            for(size_t i=0; i<KEYS.size(); ++i) {
              PFTau_matchedHLTObjectFilters_[m].objects.push_back(objs[KEYS[i]]);
            }
          }
        }
  }else{
    edm::Handle<pat::TriggerEvent> patTrigger;
    if(iEvent.getByLabel(patTriggerEventSrc, patTrigger)){
        const pat::TriggerObjectRefVector objects = patTrigger->objectRefs();
	std::string filterName(hltFilterSrc_.label());
        for(unsigned int k=0; k < objects.size(); k++){
          if(patTrigger->objectInFilter(objects[k], filterName)){
            hltObjects.push_back(*objects[k]);
          }
          for(size_t m=0; m<PFTau_matchedHLTObjectFilters_.size(); ++m) {
            if(patTrigger->objectInFilter(objects[k], PFTau_matchedHLTObjectFilters_[m].filter.label())) {
              PFTau_matchedHLTObjectFilters_[m].objects.push_back(*objects[k]);
            }
          }
          //std::cout << " hltObjects.size: " << hltObjects.size() << std::endl;
        }
    }	
  }

  // MET stuff
  for(size_t i=0; i<METs_.size(); ++i) {
    METs_[i].fill(iEvent);
  }


  // L1 event level stuff
//  edm::Handle<l1extra::L1EtMissParticleCollection> hl1met;
//  if(iEvent.getByLabel(l1MetSrc_, hl1met)) {
//    L1MET_ = hl1met->front().et();
//  }else{
    edm::Handle<pat::TriggerEvent> htrigger;
    iEvent.getByLabel(patTriggerEventSrc, htrigger);
    pat::TriggerObjectRefVector l1mets = htrigger->objects(trigger::TriggerL1ETM);
    if(!l1mets.empty()) {
        if(l1mets.size() == 1) {
            L1MET_ = l1mets[0]->et();
	    L1METcorr_ = L1EtmCorrection(L1MET_,iEvent);
        }else{
            bool found = false; 
            for(size_t i=0; i<l1mets.size(); ++i) {
                if(l1mets[i]->coll("l1extraParticles:MET")) {
                    L1MET_ = l1mets[i]->et();
		    L1METcorr_ = L1EtmCorrection(L1MET_,iEvent);
                    found = true;
                    break;
                }
            }
            if(!found) {
              std::stringstream ss;
              for(size_t i=0; i<l1mets.size(); ++i) {
                ss << l1mets[i]->collection() << " " << l1mets[i]->et() << " ";
              }
              throw cms::Exception("Assert") << "No L1 MET from collection " << l1MetSrc_.label()
                                             << ", have " << l1mets.size() << " L1 MET objects: " << ss.str()
                                             << " at " << __FILE__ << ":" << __LINE__ << std::endl;
            }
        }
    }
    pat::TriggerObjectRefVector l1taus = htrigger->objects(trigger::TriggerL1TauJet);
    for(size_t i=0; i<l1taus.size(); ++i) {
	if(!l1taus[i]->coll("l1extraParticles:Tau")) continue;
	l1JetIsTau_.push_back(true);
	l1JetPt_.push_back(l1taus[i]->pt());
	l1JetEt_.push_back(l1taus[i]->et());
	l1JetEta_.push_back(l1taus[i]->eta());
	l1JetPhi_.push_back(l1taus[i]->phi());
    }
    pat::TriggerObjectRefVector l1cenjets = htrigger->objects(trigger::TriggerL1CenJet);
    for(size_t i=0; i<l1cenjets.size(); ++i) {
        if(!l1cenjets[i]->coll("l1extraParticles:Central")) continue;
        l1JetIsTau_.push_back(false);
        l1JetPt_.push_back(l1cenjets[i]->pt());
        l1JetEt_.push_back(l1cenjets[i]->et());
        l1JetEta_.push_back(l1cenjets[i]->eta());
        l1JetPhi_.push_back(l1cenjets[i]->phi());
    }
//  }

//  if(iEvent.getByLabel(l1MhtSrc_, hl1met)) L1MHT_ = hl1met->front().et();

  if(!triggerBitsOnly) {

/*
  edm::Handle<L1GlobalTriggerReadoutRecord>      l1GTRR;
  iEvent.getByLabel(l1GtReadoutRecordSrc_, l1GTRR);   
  const DecisionWord& gtDecisionWord = l1GTRR->decisionWord();

  edm::Handle<L1GlobalTriggerObjectMapRecord>    l1GTOMRec;
  iEvent.getByLabel(l1GtObjectMapRecordSrc_, l1GTOMRec);
  const std::vector<L1GlobalTriggerObjectMap>& objMapVec = l1GTOMRec->gtObjectMap();
  for(size_t i=0; i<l1Bits_.size(); ++i) {
    for (std::vector<L1GlobalTriggerObjectMap>::const_iterator itMap = objMapVec.begin();  itMap != objMapVec.end(); ++itMap) {
      if(itMap->algoName() == l1Bits_[i].name) {
        l1Bits_[i].value = gtDecisionWord[itMap->algoBitNumber()];
        break;
      }
    }
  }
*/
/*
  // In the new format the names are not in the event data,
  // They are in the ParameterSet registry                 
  edm::Handle<L1GlobalTriggerObjectMaps> gtObjectMaps;
  iEvent.getByLabel(l1GtObjectMapRecordSrc_, gtObjectMaps);
  edm::pset::Registry* psetRegistry = edm::pset::Registry::instance();
  edm::ParameterSet const* pset = psetRegistry->getMapped(gtObjectMaps->namesParameterSetID());
  if (pset == 0) {
    cms::Exception ex("L1GlobalTrigger");
    ex << "Could not find L1 trigger names ParameterSet in the registry";
    ex.addContext("Calling TTEffAnalyzer2::analyze");
    throw ex;
  }
  std::vector<std::string> algoNames = pset->getParameter<std::vector<std::string> >("@algorithmNames");
  std::vector<int> algoBitNumbers;
  gtObjectMaps->getAlgorithmBitNumbers(algoBitNumbers);
  for(size_t i=0; i<l1Bits_.size(); ++i) {
    for (std::vector<int>::const_iterator iBit = algoBitNumbers.begin(); iBit != algoBitNumbers.end(); ++iBit) {
      if(algoNames.at(*iBit) == l1Bits_[i].name) {
	l1Bits_[i].value = gtObjectMaps->algorithmResult(*iBit);
	break;
      }
    }
  }
*/
  }
/*
  edm::Handle<l1extra::L1JetParticleCollection> hl1taus;
  edm::Handle<l1extra::L1JetParticleCollection> hl1cenjets;

  if(!triggerBitsOnly) {
//  iEvent.getByLabel(l1TauSrc_, hl1taus);
//  iEvent.getByLabel(l1CenSrc_, hl1cenjets);
  edm::Handle<L1GctJetCandCollection> l1digis;
  iEvent.getByLabel("cenJets",l1digis);

  if(iEvent.getByLabel(l1TauSrc_, hl1taus)){
    l1extra::L1JetParticleCollection::const_iterator iJet;
    for(iJet = hl1taus->begin(); iJet != hl1taus->end(); ++iJet) {
      l1JetIsTau_.push_back(true);
      l1JetPt_.push_back(iJet->pt());
      l1JetEt_.push_back(iJet->et());
      if(l1digis.isValid())
        l1JetRank_.push_back(iJet->gctJetCand()->rank());
      l1JetEta_.push_back(iJet->eta());
      l1JetPhi_.push_back(iJet->phi());
    }
  }

  if(iEvent.getByLabel(l1CenSrc_, hl1cenjets)){
    l1extra::L1JetParticleCollection::const_iterator iJet;
    for(iJet = hl1cenjets->begin(); iJet != hl1cenjets->end(); ++iJet) {
      l1JetIsTau_.push_back(false);
      l1JetPt_.push_back(iJet->pt());
      l1JetEt_.push_back(iJet->et());
      if(l1digis.isValid())
        l1JetRank_.push_back(iJet->gctJetCand()->rank());
      l1JetEta_.push_back(iJet->eta());
      l1JetPhi_.push_back(iJet->phi());
    }
  }
  }
*/

  // L2 stuff
  edm::Handle<reco::L2TauInfoAssociation> hl2TauAssoc; // association from L2 calo jets to tau info
  iEvent.getByLabel(l2TauInfoAssocSrc_, hl2TauAssoc);

  // L25 stuff
  edm::Handle<reco::PFTauCollection> hl25taus;
  iEvent.getByLabel(l25TauSrc_, hl25taus);

  primaryVertexIsValid_ = false;
  edm::Handle<edm::View<reco::Vertex> > hvertices;
  if(iEvent.getByLabel(primaryVertexSrc_, hvertices)){
    primaryVertexIsValid_ = hvertices->size() > 0;
  }

  for(size_t i=0; i<l25TauDiscriminators_.size(); ++i) {
    iEvent.getByLabel(l25TauDiscriminators_[i].src, l25TauDiscriminators_[i].handle);
  }

  for(size_t i=0; i<l25TauSelectedTaus_.size(); ++i) {
    iEvent.getByLabel(l25TauSelectedTaus_[i].src, l25TauSelectedTaus_[i].handle);
  }

  // Jets
  edm::PtrVector<pat::Jet> selectedPFJets;
  edm::Handle<edm::View<pat::Jet> > hjets;
  edm::Handle<edm::ValueMap<int> > hflag;
  iEvent.getByLabel(pfJetPUIDFlagSrc_, hflag);
  if(iEvent.getByLabel(pfJetSrc_, hjets)){
  for(size_t i=0; i<hjets->size(); ++i) {
    edm::Ptr<pat::Jet> jet = hjets->ptrAt(i);
    if(jet->pt() > 20 && // kinematics
       std::abs(jet->eta()) < 2.4 && 
       jet->numberOfDaughters() > 1 && jet->chargedEmEnergyFraction() < 0.99 &&
       jet->neutralHadronEnergyFraction() < 0.99 && jet->neutralEmEnergyFraction() < 0.99 &&
       jet->chargedHadronEnergyFraction() > 0 && jet->chargedMultiplicity() > 0) { // loose id
      PFJetPt_.push_back(jet->pt());
      PFJetEta_.push_back(jet->eta());
      PFJetPhi_.push_back(jet->phi());

      // Matching to MC truth
      int mcMatch = MCMatch(iEvent,*jet);
      PFJetMCMatch_.push_back(mcMatch);

      // Jet PU ID
      bool puidLoose  = true;
      bool puidMedium = true;
      bool puidTight  = true;

      if(hflag.isValid()){
	int flag = (*hflag)[jet];

	puidLoose =  PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kLoose);
	puidMedium = PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kMedium);
	puidTight  = PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kTight);
      }

      PFJet_JetPUIDloose_.push_back(puidLoose);
      PFJet_JetPUIDmedium_.push_back(puidMedium);
      PFJet_JetPUIDtight_.push_back(puidTight);


      selectedPFJets.push_back(jet);

      if(!triggerBitsOnly) {
      // Matching to L1 jets
      int l1JetIndex = 0;
      int foundL1 = -1;
      float jetMinDR = 99999999.;
      double jetMaxEt = 0;
      unsigned jetsInMatchingCone = 0;

      for(size_t i=0; i<l1taus.size(); ++i) {
	double DR = deltaR(*l1taus[i], *jet);
        if(DR < l1JetMatchingCone_) {
          ++jetsInMatchingCone;
          if((l1SelectNearest_ && DR < jetMinDR) ||
             (!l1SelectNearest_ && l1taus[i]->et() > jetMaxEt)) {
            foundL1 = l1JetIndex;
            jetMinDR = DR;
            jetMaxEt = l1taus[i]->et();
          }
        }
      }
      for(size_t i=0; i<l1cenjets.size(); ++i) {
        double DR = deltaR(*l1cenjets[i], *jet);
        if(DR < l1JetMatchingCone_) {
          ++jetsInMatchingCone;
          if((l1SelectNearest_ && DR < jetMinDR) ||
             (!l1SelectNearest_ && l1cenjets[i]->et() > jetMaxEt)) {
            foundL1 = l1JetIndex;
            jetMinDR = DR;
            jetMaxEt = l1cenjets[i]->et();
          }
        }
      }
/*
      l1extra::L1JetParticleCollection::const_iterator iJet;
      for(iJet = hl1taus->begin(); iJet != hl1taus->end(); ++iJet, ++l1JetIndex) {
        double DR = deltaR(*iJet, *jet);
        if(DR < l1JetMatchingCone_) {
          ++jetsInMatchingCone;
          if((l1SelectNearest_ && DR < jetMinDR) ||
             (!l1SelectNearest_ && iJet->et() > jetMaxEt)) {
            foundL1 = l1JetIndex;
            jetMinDR = DR;
            jetMaxEt = iJet->et();
          }
        }
      }
      for(iJet = hl1cenjets->begin(); iJet != hl1cenjets->end(); ++iJet, ++l1JetIndex) {
        double DR = deltaR(*iJet, *jet);
        if(DR < l1JetMatchingCone_) {
          ++jetsInMatchingCone;
          if((l1SelectNearest_ && DR < jetMinDR) ||
             (!l1SelectNearest_ && iJet->et() > jetMaxEt)) {
            foundL1 = l1JetIndex;
            jetMinDR = DR;
            jetMaxEt = iJet->et();
          }
        }
      }
*/
      PFJet_matchedL1_.push_back(foundL1);
      PFJet_l1JetsInMatchingCone_.push_back(jetsInMatchingCone);
      PFJet_l1JetMatchDR_.push_back(jetMinDR);
      }
    }
  }
  }
  // Reference taus
  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(pfTauSrc_, htaus);

  for(size_t iTau=0; iTau<htaus->size(); ++iTau) {
    const pat::Tau& tau = htaus->at(iTau);
    PFTauPt_.push_back(tau.pt());
    PFTauEt_.push_back(tau.et());
    PFTauEta_.push_back(tau.eta());
    PFTauPhi_.push_back(tau.phi());
    if(tau.leadPFChargedHadrCand().isNonnull()){
      PFTauLeadChargedHadrCandPt_.push_back(tau.leadPFChargedHadrCand()->pt());
      PFTauProng_.push_back(tau.signalPFChargedHadrCands().size());
    }
    for(size_t iDiscr=0; iDiscr<PFTauDiscriminators_.size(); ++iDiscr) {
      PFTauDiscriminators_[iDiscr].values.push_back(tau.tauID(PFTauDiscriminators_[iDiscr].name));
    }

    // Matching to offline jets
    double jetMinDR = 99999999.;
    for(size_t i=0; i<selectedPFJets.size(); ++i) {
      jetMinDR = std::min(deltaR(*(selectedPFJets[i]), tau), jetMinDR);
    }
    PFTauJetMinDR_.push_back(jetMinDR);

    // Matching to MC truth
    int mcMatch = MCMatch(iEvent,tau);
    PFTauMCMatch_.push_back(mcMatch);
    
    // Matching to HLT objects
    int foundMatch = 0;
    for(size_t i = 0; i < hltObjects.size(); ++i){
        double DR = deltaR(hltObjects[i], tau);
	if(DR < jetMinDR) foundMatch = 1;

    }
    PFTau_matchedHLTObject_.push_back(foundMatch);
    for(size_t iFilter=0; iFilter<PFTau_matchedHLTObjectFilters_.size(); ++iFilter) {
      TriggerFilter& tf = PFTau_matchedHLTObjectFilters_[iFilter];
      bool found = false;
      for(size_t iObj=0; iObj<tf.objects.size(); ++iObj) {
        if(deltaR(tf.objects[iObj], tau) < jetMinDR) {
          found = true;
          break;
        }
      }
      tf.values.push_back(found);
    }


    if(!triggerBitsOnly) {

    // Matching to L1
    int l1JetIndex = 0;
    int foundL1 = -1;
    jetMinDR = 99999999.;
    double jetMaxEt = 0;
    unsigned jetsInMatchingCone = 0;
    for(size_t i=0; i<l1taus.size(); ++i) {
      double DR = deltaR(*l1taus[i], tau);
      if(DR < l1JetMatchingCone_) {
	++jetsInMatchingCone;
	if((l1SelectNearest_ && DR < jetMinDR) ||
	   (!l1SelectNearest_ && l1taus[i]->et() > jetMaxEt)) {
	  foundL1 = l1JetIndex;
	  jetMinDR = DR;
	  jetMaxEt = l1taus[i]->et();
	}
      }
    }
    for(size_t i=0; i<l1cenjets.size(); ++i) {
      double DR = deltaR(*l1cenjets[i], tau);
      if(DR < l1JetMatchingCone_) {
	++jetsInMatchingCone;
	if((l1SelectNearest_ && DR < jetMinDR) ||
	   (!l1SelectNearest_ && l1cenjets[i]->et() > jetMaxEt)) {
	  foundL1 = l1JetIndex;
	  jetMinDR = DR;
	  jetMaxEt = l1cenjets[i]->et();
	}
      }
    }
    /*
    l1extra::L1JetParticleCollection::const_iterator iJet;
    for(iJet = hl1taus->begin(); iJet != hl1taus->end(); ++iJet, ++l1JetIndex) {
      double DR = deltaR(*iJet, tau);
      if(DR < l1JetMatchingCone_) {
        ++jetsInMatchingCone;
        if((l1SelectNearest_ && DR < jetMinDR) ||
           (!l1SelectNearest_ && iJet->et() > jetMaxEt)) {
          foundL1 = l1JetIndex;
          jetMinDR = DR;
          jetMaxEt = iJet->et();
        }
      }
    }
    for(iJet = hl1cenjets->begin(); iJet != hl1cenjets->end(); ++iJet, ++l1JetIndex) {
      double DR = deltaR(*iJet, tau);
      if(DR < l1JetMatchingCone_) {
        ++jetsInMatchingCone;
        if((l1SelectNearest_ && DR < jetMinDR) ||
           (!l1SelectNearest_ && iJet->et() > jetMaxEt)) {
          foundL1 = l1JetIndex;
          jetMinDR = DR;
          jetMaxEt = iJet->et();
        }
      }
    }
    */
    PFTau_matchedL1_.push_back(foundL1);
    PFTau_l1JetsInMatchingCone_.push_back(jetsInMatchingCone);
    PFTau_l1JetMatchDR_.push_back(jetMinDR);

    // Matching to L2
    const reco::CaloJet *foundL2 = 0;
    jetMinDR = 99999999.;
    if(hl2TauAssoc.isValid()){
    for(reco::L2TauInfoAssociation::const_iterator it = hl2TauAssoc->begin(); it != hl2TauAssoc->end(); ++it) {
      const reco::CaloJet& l2Jet = *(it->key);
      double DR = deltaR(l2Jet, tau);
      if(DR < l2JetMatchingCone_ && DR < jetMinDR) {
        jetMinDR = DR;
        foundL2 = &l2Jet;
      }
    }
    }

    bool hasMatchedL2Jet = false;
    float jetPt = 0;
    float jetEt = 0;
    float jetEta = 0;
    float jetPhi = 0;
    if(foundL2) {
      hasMatchedL2Jet = true;
      jetPt = foundL2->pt();
      jetEt = foundL2->et();
      jetEta = foundL2->eta();
      jetPhi = foundL2->phi();
    }
    l2HasMatchedL2Jet_.push_back(hasMatchedL2Jet);
    l2JetPt_.push_back(jetPt);
    l2JetEt_.push_back(jetEt);
    l2JetEta_.push_back(jetEta);
    l2JetPhi_.push_back(jetPhi);


    // Matching to L25
    const reco::PFTau *foundL25 = 0;
    size_t l25Index = 0;
    if(hl25taus.isValid()){
    jetMinDR = 999999.;
    for(reco::PFTauCollection::const_iterator it = hl25taus->begin(); it != hl25taus->end(); ++it) {
      const reco::PFTau& l25tau = *it;
      double DR = deltaR(l25tau, tau);
      if(DR < l25TauMatchingCone_ && DR < jetMinDR) {
        jetMinDR = DR;
        foundL25 = &l25tau;
        l25Index = (it-hl25taus->begin());
      }
    }
    }

    bool hasMatchedL25Tau = false;
    jetPt = 0;
    jetEt = 0;
    jetEta = 0;
    jetPhi = 0;
    bool leadTrackExists = false;
    float leadTrackPt = 0;
    float isoTrackPtMax = 0;
    float isoGammaEtMax = 0;
    unsigned prongs = 0;
    if(foundL25) {
      hasMatchedL25Tau = true;
      jetPt = foundL25->pt();
      jetEt = foundL25->et();
      jetEta = foundL25->eta();
      jetPhi = foundL25->phi();
      const reco::PFCandidateRef leadChargedHadr = foundL25->leadPFChargedHadrCand();
      if(leadChargedHadr.isNonnull()) {
        leadTrackExists = true;
        leadTrackPt = leadChargedHadr->pt();
        prongs = foundL25->signalPFChargedHadrCands().size();

        if(primaryVertexIsValid_) {
          const reco::Vertex& hltPrimaryVertex = *(hvertices->begin());

          reco::PFCandidateRefVector cands;
          // Maximum pt/et of candidates after quality filtering
          cands = TauTagTools::filteredPFChargedHadrCands(foundL25->isolationPFChargedHadrCands(),
                                                          0,
                                                          l25FilterMinPixelHits_,
                                                          l25FilterMinTrackerHits_,
                                                          l25FilterMaxIP_,
                                                          l25FilterMaxChi2_,
                                                          l25FilterMaxDeltaZ_,
                                                          hltPrimaryVertex,
                                                          hltPrimaryVertex.position().z());
          for(size_t i=0; i<cands.size(); ++i) {
            isoTrackPtMax = std::max(isoTrackPtMax, static_cast<float>(cands[i]->pt()));
          }

          cands = TauTagTools::filteredPFGammaCands(foundL25->isolationPFGammaCands(), 0);
          for(size_t i=0; i<cands.size(); ++i) {
            isoGammaEtMax = std::max(isoGammaEtMax, static_cast<float>(cands[i]->pt()));
          }
        }
      }
    }
    l25HasMatchedL25Tau_.push_back(hasMatchedL25Tau);
    l25TauPt_.push_back(jetPt);
    l25TauEt_.push_back(jetEt);
    l25TauEta_.push_back(jetEta);
    l25TauPhi_.push_back(jetPhi);
    l25TauLeadChargedHadrCandExists_.push_back(leadTrackExists);
    l25TauLeadChargedHadrCandPt_.push_back(leadTrackPt);
    l25TauIsoChargedHadrCandPtMax_.push_back(isoTrackPtMax);
    l25TauIsoGammaCandEtMax_.push_back(isoGammaEtMax);
    l25TauProng_.push_back(prongs);
    for(size_t i=0; i<l25TauDiscriminators_.size(); ++i) {
      float value = -1;
      if(l25TauDiscriminators_[i].handle.isValid()){
        if(foundL25) {
          reco::PFTauRef ref(hl25taus, l25Index);
          value = (*(l25TauDiscriminators_[i].handle))[ref];
        }
        l25TauDiscriminators_[i].values.push_back(value);
      }
    }
    for(size_t i=0; i<l25TauSelectedTaus_.size(); ++i) {
      bool value = false;
      if(l25TauSelectedTaus_[i].handle.isValid()){
	   if(foundL25) {
	     for(size_t j=0; j<l25TauSelectedTaus_[i].handle->size(); ++j) {
	       if(reco::deltaR(*foundL25, l25TauSelectedTaus_[i].handle->at(j)) < 0.1) {
		 value = true;
		 break;
	       }
	     }
	   }
           l25TauSelectedTaus_[i].values.push_back(value);
      }
    }
    }
    muonAnalyzer->fill(iEvent,iSetup,tau);
  }

  tree_->Fill();
  reset();
}

void TTEffAnalyzer2::endJob() {
  file_->Write();
  file_->Close();
}

void TTEffAnalyzer2::endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup) {
  // Counters
  edm::Handle<edm::MergeableCounter> count;

  for(size_t i = 0; i < counters_.size(); ++i){
    lumi.getByLabel(counters_[i], count);
    int value = count->value;
    if(h_counters_->GetEntries()) value += h_counters_->GetBinContent(i+1);
    h_counters_->SetBinContent(i+1,value);
    h_counters_->GetXaxis()->SetBinLabel(i+1,(counters_[i].label()).c_str());
  }
}

DEFINE_FWK_MODULE(TTEffAnalyzer2);
