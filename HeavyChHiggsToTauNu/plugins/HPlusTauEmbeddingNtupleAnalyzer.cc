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
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventItem.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeElectronBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTauBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeVertexBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTriggerBranches.h"

#include "TTree.h"

#include <limits>

class HPlusTauEmbeddingNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusTauEmbeddingNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusTauEmbeddingNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  TTree *fTree;

  typedef HPlus::EventItem<XYZTLorentzVector> MetItem;
  typedef HPlus::EventItem<double> DoubleItem;
  typedef HPlus::EventItem<bool> BoolItem;

  edm::InputTag fGenParticleOriginalSrc;
  edm::InputTag fGenParticleEmbeddedSrc;

  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EmbeddingMuonEfficiency fEmbeddingMuonEfficiency;

  HPlus::TreeEventBranches fEventBranches;
  HPlus::TreeVertexBranches fSelectedVertexBranches;
  HPlus::TreeVertexBranches fGoodVertexBranches;
  HPlus::TreeTriggerBranches fTriggerBranches;
  HPlus::TreeMuonBranches fMuonBranches;
  //HPlus::TreeElectronBranches fElectronBranches;
  HPlus::TreeTauBranches fTauBranches;
  //HPlus::TreeJetBranches fJetBranches;

  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;
  std::vector<BoolItem> fBools;

  double fEmbeddingMuonEfficiencyWeight;
};

HPlusTauEmbeddingNtupleAnalyzer::HPlusTauEmbeddingNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fGenParticleOriginalSrc(iConfig.getParameter<edm::InputTag>("genParticleOriginalSrc")),
  fGenParticleEmbeddedSrc(iConfig.getParameter<edm::InputTag>("genParticleEmbeddedSrc")),
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  fEmbeddingMuonEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMuonEfficiency"), fHistoWrapper),
  fSelectedVertexBranches(iConfig, "selectedPrimaryVertex", "selectedPrimaryVertexSrc"),
  fGoodVertexBranches(iConfig, "goodPrimaryVertex", "goodPrimaryVertexSrc"),
  fTriggerBranches(iConfig),
  fMuonBranches(iConfig),
  //fElectronBranches(iConfig, fSelectedVertexBranches.getInputTag()),
  fTauBranches(iConfig)
  //fJetBranches(iConfig, true)
{

  edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("mets");
  std::vector<std::string> names = pset.getParameterNames();
  for(size_t i=0; i<names.size(); ++i) {
    fMets.push_back(MetItem(names[i], pset.getParameter<edm::InputTag>(names[i])));
  }

  pset = iConfig.getParameter<edm::ParameterSet>("doubles");
  names = pset.getParameterNames();
  for(size_t i=0; i<names.size(); ++i) {
    fDoubles.push_back(DoubleItem(names[i], pset.getParameter<edm::InputTag>(names[i])));
  }

  pset = iConfig.getParameter<edm::ParameterSet>("bools");
  names = pset.getParameterNames();
  for(size_t i=0; i<names.size(); ++i) {
    fBools.push_back(BoolItem(names[i], pset.getParameter<edm::InputTag>(names[i])));
  }

  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fSelectedVertexBranches.book(fTree);
  fGoodVertexBranches.book(fTree);
  fTriggerBranches.book(fTree);
  fMuonBranches.book(fTree);
  //fElectronBranches.book(fTree);
  fTauBranches.book(fTree);
  //fJetBranches.book(fTree);

  for(size_t i=0; i<fMets.size(); ++i) {
    fTree->Branch(fMets[i].name.c_str(), &(fMets[i].value));
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fTree->Branch(fDoubles[i].name.c_str(), &(fDoubles[i].value));
  }
  for(size_t i=0; i<fBools.size(); ++i) {
    fTree->Branch(fBools[i].name.c_str(), &(fBools[i].value));
  }

  fTree->Branch("weight_embeddingMuonEfficiency", &fEmbeddingMuonEfficiencyWeight);
}

HPlusTauEmbeddingNtupleAnalyzer::~HPlusTauEmbeddingNtupleAnalyzer() {}

void HPlusTauEmbeddingNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fSelectedVertexBranches.reset();
  fGoodVertexBranches.reset();
  fTriggerBranches.reset();
  fMuonBranches.reset();
  //fElectronBranches.reset();
  fTauBranches.reset();
  //fJetBranches.reset();

  for(size_t i=0; i<fMets.size(); ++i) {
    fMets[i].value.SetXYZT(nan, nan, nan, nan);
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fDoubles[i].value = nan;
  }
  for(size_t i=0; i<fBools.size(); ++i) {
    fBools[i].value = false;
  }
  fEmbeddingMuonEfficiencyWeight = 1.0;
}

void HPlusTauEmbeddingNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);
  fSelectedVertexBranches.setValues(iEvent);
  fGoodVertexBranches.setValues(iEvent);
  fTriggerBranches.setValues(iEvent);

  HPlus::EmbeddingMuonEfficiency::Data embeddingMuonData = fEmbeddingMuonEfficiency.applyEventWeight(iEvent, fEventWeight);
  fEmbeddingMuonEfficiencyWeight = embeddingMuonData.getEventWeight();

  edm::Handle<edm::View<reco::GenParticle> > hgenparticlesOriginal;
  edm::Handle<edm::View<reco::GenParticle> > hgenparticlesEmbedded;
  if(!iEvent.isRealData())
    iEvent.getByLabel(fGenParticleOriginalSrc, hgenparticlesOriginal);
  iEvent.getByLabel(fGenParticleEmbeddedSrc, hgenparticlesEmbedded);

  // Muons
  if(iEvent.isRealData()) {
    fMuonBranches.setValues(iEvent);
    //fElectronBranches.setValues(iEvent);
  }
  else {
    fMuonBranches.setValues(iEvent, *hgenparticlesOriginal);
    //fElectronBranches.setValues(iEvent, *hgenparticlesOriginal);
  }
  fTauBranches.setValues(iEvent, *hgenparticlesEmbedded);

  //fJetBranches.setValues(iEvent);

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
  for(size_t i=0; i<fBools.size(); ++i) {
    edm::Handle<bool> hnum;
    iEvent.getByLabel(fBools[i].src, hnum);
    fBools[i].value = *hnum;
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusTauEmbeddingNtupleAnalyzer);
