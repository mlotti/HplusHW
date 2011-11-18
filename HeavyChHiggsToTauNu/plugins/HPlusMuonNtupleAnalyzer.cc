#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventItem.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"

#include "TTree.h"

#include <limits>

class HPlusMuonNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusMuonNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusMuonNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  TTree *fTree;

  typedef HPlus::EventItem<XYZTLorentzVector> MetItem;
  typedef HPlus::EventItem<double> DoubleItem;

  edm::InputTag fPatTriggerSrc;
  edm::InputTag fGenParticleSrc;

  HPlus::TreeEventBranches fEventBranches;
  HPlus::TreeMuonBranches fMuonBranches;
  HPlus::TreeJetBranches fJetBranches;

  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;
};

HPlusMuonNtupleAnalyzer::HPlusMuonNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
  fGenParticleSrc(iConfig.getParameter<edm::InputTag>("genParticleSrc")),
  fMuonBranches(iConfig),
  fJetBranches(iConfig, false)
{

  std::vector<edm::ParameterSet> mets = iConfig.getParameter<std::vector<edm::ParameterSet> >("mets");
  for(size_t i=0; i<mets.size(); ++i) {
    fMets.push_back(MetItem(mets[i].getParameter<std::string>("name"), mets[i].getParameter<edm::InputTag>("src")));
  }

  std::vector<edm::ParameterSet> doubles = iConfig.getParameter<std::vector<edm::ParameterSet> >("doubles");
  for(size_t i=0; i<doubles.size(); ++i) {
    fDoubles.push_back(DoubleItem(doubles[i].getParameter<std::string>("name"), doubles[i].getParameter<edm::InputTag>("src")));
  }

  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fMuonBranches.book(fTree);
  fJetBranches.book(fTree);

  for(size_t i=0; i<fMets.size(); ++i) {
    fTree->Branch(fMets[i].name.c_str(), &(fMets[i].value));
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fTree->Branch(fDoubles[i].name.c_str(), &(fDoubles[i].value));
  }
}

HPlusMuonNtupleAnalyzer::~HPlusMuonNtupleAnalyzer() {}

void HPlusMuonNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fMuonBranches.reset();
  fJetBranches.reset();

  for(size_t i=0; i<fMets.size(); ++i) {
    fMets[i].value.SetXYZT(nan, nan, nan, nan);
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fDoubles[i].value = nan;
  }
}

void HPlusMuonNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);

  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(fPatTriggerSrc, htrigger);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
  if(!iEvent.isRealData())
    iEvent.getByLabel(fGenParticleSrc, hgenparticles);

  // Muons
  if(iEvent.isRealData())
    fMuonBranches.setValues(iEvent);
  else
    fMuonBranches.setValues(iEvent, *hgenparticles);

  fJetBranches.setValues(iEvent);

  for(size_t i=0; i<fMets.size(); ++i) {
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fMets[i].src, hmet);
    fMets[i].value = hmet->at(0).p4();
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    edm::Handle<double> hnum;
    iEvent.getByLabel(fDoubles[i].src, hnum);
    fDoubles[i].value = *hnum;
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusMuonNtupleAnalyzer);
