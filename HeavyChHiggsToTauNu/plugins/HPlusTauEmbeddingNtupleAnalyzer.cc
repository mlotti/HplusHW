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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenTauBranches.h"

#include "TTree.h"

#include <limits>

class HPlusTauEmbeddingNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusTauEmbeddingNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusTauEmbeddingNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  void endJob();

  void reset();

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  TTree *fTree;

  typedef HPlus::EventItem<XYZTLorentzVector> MetItem;
  typedef HPlus::EventItem<double> DoubleItem;
  typedef HPlus::EventItem<bool> BoolItem;

  edm::InputTag fGenParticleOriginalSrc;
  edm::InputTag fGenParticleEmbeddedSrc;
  edm::InputTag fGenTauOriginalSrc;
  edm::InputTag fGenTauEmbeddedSrc;

  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EventCounter eventCounter;

  HPlus::TreeEventBranches fEventBranches;
  HPlus::TreeVertexBranches fSelectedVertexBranches;
  HPlus::TreeVertexBranches fGoodVertexBranches;
  HPlus::TreeTriggerBranches fTriggerBranches;
  HPlus::TreeMuonBranches fMuonBranches;
  //HPlus::TreeElectronBranches fElectronBranches;
  HPlus::TreeTauBranches fTauBranches;
  HPlus::TreeJetBranches fJetBranches;

  HPlus::TreeGenTauBranches fGenTausOriginal;
  HPlus::TreeGenTauBranches fGenTausEmbedded;

  struct MuonEff {
    MuonEff(const edm::ParameterSet& pset, const std::string& n): efficiency(pset), name(n) {}

    void book(TTree *tree) { tree->Branch(name.c_str(), &values); }
    void reset() { values.clear(); }

    HPlus::EmbeddingMuonEfficiency efficiency;
    std::string name;
    std::vector<double> values;
  };
  std::vector<MuonEff> fMuonEffs;

  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;
  std::vector<BoolItem> fBools;
};

HPlusTauEmbeddingNtupleAnalyzer::HPlusTauEmbeddingNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fGenParticleOriginalSrc(iConfig.getParameter<edm::InputTag>("genParticleOriginalSrc")),
  fGenParticleEmbeddedSrc(iConfig.getParameter<edm::InputTag>("genParticleEmbeddedSrc")),
  fGenTauOriginalSrc(iConfig.getParameter<edm::InputTag>("genTauOriginalSrc")),
  fGenTauEmbeddedSrc(iConfig.getParameter<edm::InputTag>("genTauEmbeddedSrc")),
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  fSelectedVertexBranches(iConfig, "selectedPrimaryVertex", "selectedPrimaryVertexSrc"),
  fGoodVertexBranches(iConfig, "goodPrimaryVertex", "goodPrimaryVertexSrc"),
  fTriggerBranches(iConfig),
  fMuonBranches(iConfig.getParameter<edm::ParameterSet>("muons")),
  //fElectronBranches(iConfig, fSelectedVertexBranches.getInputTag()),
  fTauBranches(iConfig),
  fJetBranches(iConfig.getParameter<edm::ParameterSet>("jets"), false),
  fGenTausOriginal("gentausOriginal"),
  fGenTausEmbedded("gentausEmbedded")
{

  edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("muonEfficiencies");
  std::vector<std::string> names = pset.getParameterNames();
  for(size_t i=0; i<names.size(); ++i) {
    fMuonEffs.push_back(MuonEff(pset.getUntrackedParameter<edm::ParameterSet>(names[i]), fMuonBranches.getPrefix()+"efficiency_"+names[i]));
  }

  pset = iConfig.getParameter<edm::ParameterSet>("mets");
  names = pset.getParameterNames();
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
  // Save the module configuration to the output ROOT file as a TNamed object
  fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fSelectedVertexBranches.book(fTree);
  fGoodVertexBranches.book(fTree);
  fTriggerBranches.book(fTree);
  fMuonBranches.book(fTree);

  for(size_t i=0; i<fMuonEffs.size(); ++i) {
    fMuonEffs[i].book(fTree);
  }

  //fElectronBranches.book(fTree);
  fTauBranches.book(fTree);
  fJetBranches.book(fTree);

  fGenTausOriginal.book(fTree);
  fGenTausEmbedded.book(fTree);

  for(size_t i=0; i<fMets.size(); ++i) {
    fTree->Branch(fMets[i].name.c_str(), &(fMets[i].value));
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fTree->Branch(fDoubles[i].name.c_str(), &(fDoubles[i].value));
  }
  for(size_t i=0; i<fBools.size(); ++i) {
    fTree->Branch(fBools[i].name.c_str(), &(fBools[i].value));
  }
}

HPlusTauEmbeddingNtupleAnalyzer::~HPlusTauEmbeddingNtupleAnalyzer() {}

void HPlusTauEmbeddingNtupleAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}
void HPlusTauEmbeddingNtupleAnalyzer::endJob() {
  eventCounter.endJob();
}

void HPlusTauEmbeddingNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fSelectedVertexBranches.reset();
  fGoodVertexBranches.reset();
  fTriggerBranches.reset();
  fMuonBranches.reset();
  //fElectronBranches.reset();
  fTauBranches.reset();
  fJetBranches.reset();

  fGenTausOriginal.reset();
  fGenTausEmbedded.reset();

  for(size_t i=0; i<fMuonEffs.size(); ++i) {
    fMuonEffs[i].reset();
  }

  for(size_t i=0; i<fMets.size(); ++i) {
    fMets[i].value.SetXYZT(nan, nan, nan, nan);
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fDoubles[i].value = nan;
  }
  for(size_t i=0; i<fBools.size(); ++i) {
    fBools[i].value = false;
  }
}

void HPlusTauEmbeddingNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);
  fSelectedVertexBranches.setValues(iEvent);
  fGoodVertexBranches.setValues(iEvent);
  fTriggerBranches.setValues(iEvent);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticlesOriginal;
  edm::Handle<edm::View<reco::GenParticle> > hgenparticlesEmbedded;
  edm::Handle<edm::View<reco::GenParticle> > hgentausOriginal;
  edm::Handle<edm::View<reco::GenParticle> > hgentausEmbedded;
  if(!iEvent.isRealData()) {
    iEvent.getByLabel(fGenParticleOriginalSrc, hgenparticlesOriginal);
    iEvent.getByLabel(fGenTauOriginalSrc, hgentausOriginal);
  }
  iEvent.getByLabel(fGenParticleEmbeddedSrc, hgenparticlesEmbedded);
  iEvent.getByLabel(fGenTauEmbeddedSrc, hgentausEmbedded);

  // Muons
  if(iEvent.isRealData()) {
    fMuonBranches.setValues(iEvent);
    //fElectronBranches.setValues(iEvent);
  }
  else {
    fMuonBranches.setValues(iEvent, *hgenparticlesOriginal);
    //fElectronBranches.setValues(iEvent, *hgenparticlesOriginal);
    for(edm::View<reco::GenParticle>::const_iterator iGen = hgentausOriginal->begin(); iGen != hgentausOriginal->end(); ++iGen) {
      if(std::abs(iGen->pdgId()) == 15) {
        fGenTausOriginal.addValue(&(*iGen));
      }
    }
  }
  fTauBranches.setValues(iEvent, *hgenparticlesEmbedded);
  for(edm::View<reco::GenParticle>::const_iterator iGen = hgentausEmbedded->begin(); iGen != hgentausEmbedded->end(); ++iGen) {
    if(std::abs(iGen->pdgId()) == 15) {
      fGenTausEmbedded.addValue(&(*iGen));
    }
  }

  edm::Handle<edm::View<pat::Muon> > hmuons;
  iEvent.getByLabel(fMuonBranches.getInputTag(), hmuons);

  for(size_t i=0; i<fMuonEffs.size(); ++i) {
    for(size_t j=0; j<hmuons->size(); ++j) {
      HPlus::EmbeddingMuonEfficiency::Data data = fMuonEffs[i].efficiency.getEventWeight(hmuons->ptrAt(j), iEvent.isRealData());
      fMuonEffs[i].values.push_back(data.getEfficiency());
    }
  }

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
  for(size_t i=0; i<fBools.size(); ++i) {
    edm::Handle<bool> hnum;
    iEvent.getByLabel(fBools[i].src, hnum);
    fBools[i].value = *hnum;
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusTauEmbeddingNtupleAnalyzer);
