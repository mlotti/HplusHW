#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventItem.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTauBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeVertexBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTriggerBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenTauBranches.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include <limits>

class HPlusTauNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusTauNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusTauNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  void endJob();

  void reset();

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  TTree *fTree;

  typedef HPlus::EventItem<XYZTLorentzVector> MetItem;
  typedef HPlus::EventItem<double> DoubleItem;

  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EventCounter eventCounter;

  edm::InputTag fGenParticleTauSrc;
  edm::InputTag fSelectedPrimaryVertexSrc;
  edm::InputTag fGoodPrimaryVertexSrc;

  HPlus::TreeEventBranches fEventBranches;
  HPlus::TreeGenBranches fGenBranches;
  HPlus::TreeVertexBranches fSelectedVertexBranches;
  HPlus::TreeVertexBranches fGoodVertexBranches;
  HPlus::TreeTriggerBranches fTriggerBranches;

  const bool fTauEnabled;
  HPlus::TreeTauBranches fTauBranches;

  HPlus::TreeJetBranches fJetBranches;

  HPlus::TreeMuonBranches fMuonBranches;

  HPlus::TreeGenTauBranches fGenTaus;

  const bool fGenTTBarEnabled;
  HPlus::TreeGenParticleBranches fGenTTBarBranches;

  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;

  HPlus::Count cAllEvents;
};

HPlusTauNtupleAnalyzer::HPlusTauNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  fGenParticleTauSrc(iConfig.getParameter<edm::InputTag>("genParticleTauSrc")),
  fGenBranches(iConfig),
  fSelectedVertexBranches(iConfig, "selectedPrimaryVertex", "selectedPrimaryVertexSrc"),
  fGoodVertexBranches(iConfig, "goodPrimaryVertex", "goodPrimaryVertexSrc"),
  fTriggerBranches(iConfig),
  fTauEnabled(iConfig.getParameter<bool>("tauEnabled")),
  fTauBranches(iConfig),
  fJetBranches(iConfig.getParameter<edm::ParameterSet>("jets"), false),
  fMuonBranches(iConfig.getParameter<edm::ParameterSet>("muons")),
  fGenTaus("gentaus"),
  fGenTTBarEnabled(iConfig.getParameter<bool>("genTTBarEnabled")),
  fGenTTBarBranches("genttbarwdecays"),
  cAllEvents(eventCounter.addCounter("All events"))
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

  edm::Service<TFileService> fs;
  // Save the module configuration to the output ROOT file as a TNamed object
  fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fGenBranches.book(fTree);
  fSelectedVertexBranches.book(fTree);
  fGoodVertexBranches.book(fTree);
  fTriggerBranches.book(fTree);

  if(fTauEnabled)
    fTauBranches.book(fTree);

  fJetBranches.book(fTree);

  fMuonBranches.book(fTree);

  fGenTaus.book(fTree);

  if(fGenTTBarEnabled)
    fGenTTBarBranches.book(fTree);

  for(size_t i=0; i<fMets.size(); ++i) {
    fTree->Branch(fMets[i].name.c_str(), &(fMets[i].value));
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fTree->Branch(fDoubles[i].name.c_str(), &(fDoubles[i].value));
  }
}

HPlusTauNtupleAnalyzer::~HPlusTauNtupleAnalyzer() {}

void HPlusTauNtupleAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}
void HPlusTauNtupleAnalyzer::endJob() {
  eventCounter.endJob();
}

void HPlusTauNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fGenBranches.reset();
  fSelectedVertexBranches.reset();
  fGoodVertexBranches.reset();
  fTriggerBranches.reset();
  fTauBranches.reset();
  fJetBranches.reset();

  fMuonBranches.reset();

  fGenTaus.reset();
  fGenTTBarBranches.reset();

  for(size_t i=0; i<fMets.size(); ++i) {
    fMets[i].value.SetXYZT(nan, nan, nan, nan);
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fDoubles[i].value = nan;
  }
}

void HPlusTauNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventWeight.beginEvent();
  increment(cAllEvents);

  fEventBranches.setValues(iEvent);
  fSelectedVertexBranches.setValues(iEvent);
  fGoodVertexBranches.setValues(iEvent);
  fTriggerBranches.setValues(iEvent);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
  edm::Handle<edm::View<reco::GenParticle> > hgenparticlestau;
  if(!iEvent.isRealData()) {
    iEvent.getByLabel(fGenBranches.getInputTag(), hgenparticles);
    iEvent.getByLabel(fGenParticleTauSrc, hgenparticlestau);
  }

  // Taus
  if(iEvent.isRealData()) {
    if(fTauEnabled)
      fTauBranches.setValues(iEvent);
  }
  else {
    fGenBranches.setValues(iEvent);
    if(fTauEnabled)
      fTauBranches.setValues(iEvent, *hgenparticlestau);

    for(edm::View<reco::GenParticle>::const_iterator iGen = hgenparticlestau->begin(); iGen != hgenparticlestau->end(); ++iGen) {
      if(std::abs(iGen->pdgId()) == 15) {
        fGenTaus.addValue(&(*iGen));
      }
    }

    if(fGenTTBarEnabled) {

      std::vector<const reco::GenParticle *> ttbarDecays = HPlus::GenParticleTools::findTTBarWdecays(hgenparticles->ptrVector());
      for(size_t i=0; i<ttbarDecays.size(); ++i) {
        fGenTTBarBranches.addValue(ttbarDecays[i]);
      }
    }
  }

  fJetBranches.setValues(iEvent);

  if(iEvent.isRealData()) {
    fMuonBranches.setValues(iEvent);
  }
  else {
    fMuonBranches.setValues(iEvent, *hgenparticles);
  }

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

DEFINE_FWK_MODULE(HPlusTauNtupleAnalyzer);
