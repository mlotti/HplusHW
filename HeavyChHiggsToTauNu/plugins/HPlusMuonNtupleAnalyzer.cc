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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventItem.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeElectronBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeVertexBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"

#include "TTree.h"

#include <limits>

class HPlusMuonNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusMuonNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusMuonNtupleAnalyzer();

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

  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EventCounter eventCounter;

  edm::InputTag fPatTriggerSrc;

  HPlus::TreeEventBranches fEventBranches;
  HPlus::TreeGenBranches fGenBranches;
  HPlus::TreeVertexBranches fSelectedVertexBranches;
  HPlus::TreeVertexBranches fGoodVertexBranches;
  HPlus::TreeMuonBranches fMuonBranches;
  //HPlus::TreeElectronBranches fElectronBranches;

  std::vector<HPlus::TreeJetBranches> fJetBranches;

  bool fGenTTBarEnabled;
  HPlus::TreeGenParticleBranches fGenTTBarBranches;

  struct MuonEff {
    MuonEff(const edm::ParameterSet& pset, const std::string& n):
      efficiency(pset), name(n) {}

    void book(TTree *tree) {
      tree->Branch(name.c_str(), &values);
      tree->Branch((name+"_unc").c_str(), &uncertainties);
    }
    void reset() {
      values.clear();
      uncertainties.clear();
    }

    HPlus::EmbeddingMuonEfficiency efficiency;
    std::string name;
    std::vector<double> values;
    std::vector<double> uncertainties;
  };
  std::vector<MuonEff> fMuonEffs;

  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;
  std::vector<BoolItem> fBools;

  HPlus::Count cAllEvents;
};

HPlusMuonNtupleAnalyzer::HPlusMuonNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
  fGenBranches(iConfig),
  fSelectedVertexBranches(iConfig, "selectedPrimaryVertex", "selectedPrimaryVertexSrc"),
  fGoodVertexBranches(iConfig, "goodPrimaryVertex", "goodPrimaryVertexSrc"),
  fMuonBranches(iConfig.getParameter<edm::ParameterSet>("muons")),
  //fElectronBranches(iConfig, fSelectedVertexBranches.getInputTag()),
  fGenTTBarEnabled(iConfig.getParameter<bool>("genTTBarEnabled")),
  fGenTTBarBranches("genttbarwdecays"),
  cAllEvents(eventCounter.addCounter("All events"))
{

  edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("muonEfficiencies");
  std::vector<std::string> names = pset.getParameterNames();
  for(size_t i=0; i<names.size(); ++i) {
    fMuonEffs.push_back(MuonEff(pset.getUntrackedParameter<edm::ParameterSet>(names[i]), fMuonBranches.getPrefix()+"efficiency_"+names[i]));
  }

  pset = iConfig.getParameter<edm::ParameterSet>("jets");
  names = pset.getParameterNames();
  fJetBranches.reserve(names.size());
  for(size_t i=0; i<names.size(); ++i) {
    fJetBranches.push_back(HPlus::TreeJetBranches(pset.getParameter<edm::ParameterSet>(names[i]), false, names[i]+"_"));
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
  fGenBranches.book(fTree);
  fSelectedVertexBranches.book(fTree);
  fGoodVertexBranches.book(fTree);
  fMuonBranches.book(fTree);
  //fElectronBranches.book(fTree);

  for(size_t i=0; i<fJetBranches.size(); ++i)
    fJetBranches[i].book(fTree);

  if(fGenTTBarEnabled)
    fGenTTBarBranches.book(fTree);

  for(size_t i=0; i<fMuonEffs.size(); ++i) {
    fMuonEffs[i].book(fTree);
  }

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

HPlusMuonNtupleAnalyzer::~HPlusMuonNtupleAnalyzer() {}

void HPlusMuonNtupleAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}
void HPlusMuonNtupleAnalyzer::endJob() {
  eventCounter.endJob();
}

void HPlusMuonNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fGenBranches.reset();
  fSelectedVertexBranches.reset();
  fGoodVertexBranches.reset();
  fMuonBranches.reset();
  //fElectronBranches.reset();
  for(size_t i=0; i<fJetBranches.size(); ++i)
    fJetBranches[i].reset();
  fGenTTBarBranches.reset();

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

void HPlusMuonNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventWeight.beginEvent();
  increment(cAllEvents);

  fEventBranches.setValues(iEvent);
  fSelectedVertexBranches.setValues(iEvent);
  fGoodVertexBranches.setValues(iEvent);

  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(fPatTriggerSrc, htrigger);


  // Muons
  if(iEvent.isRealData()) {
    fMuonBranches.setValues(iEvent);
    //fElectronBranches.setValues(iEvent);
  }
  else {
    edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
    iEvent.getByLabel(fGenBranches.getInputTag(), hgenparticles);

    fGenBranches.setValues(iEvent);
    fMuonBranches.setValues(iEvent, *hgenparticles);
    //fElectronBranches.setValues(iEvent, *hgenparticles);

    if(fGenTTBarEnabled) {
      std::vector<const reco::GenParticle *> ttbarDecays = HPlus::GenParticleTools::findTTBarWdecays(hgenparticles->ptrVector());
      for(size_t i=0; i<ttbarDecays.size(); ++i) {
        fGenTTBarBranches.addValue(ttbarDecays[i]);
      }
    }
  }

  edm::Handle<edm::View<pat::Muon> > hmuons;
  iEvent.getByLabel(fMuonBranches.getInputTag(), hmuons);

  for(size_t i=0; i<fMuonEffs.size(); ++i) {
    for(size_t j=0; j<hmuons->size(); ++j) {
      HPlus::EmbeddingMuonEfficiency::Data data = fMuonEffs[i].efficiency.getEventWeight(hmuons->ptrAt(j), iEvent.isRealData());
      fMuonEffs[i].values.push_back(data.getEventWeight());
      fMuonEffs[i].uncertainties.push_back(data.getEventWeightAbsoluteUncertainty());
    }
  }

  for(size_t i=0; i<fJetBranches.size(); ++i)
    fJetBranches[i].setValues(iEvent);

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

DEFINE_FWK_MODULE(HPlusMuonNtupleAnalyzer);
