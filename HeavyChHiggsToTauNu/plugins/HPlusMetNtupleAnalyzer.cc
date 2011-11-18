#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/METReco/interface/MET.h"

#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventItem.h"

#include "TTree.h"

#include <limits>

class HPlusMetNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusMetNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusMetNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  TTree *fTree;

  typedef HPlus::EventItem<XYZTLorentzVector> MetItem;
  typedef HPlus::EventItem<double> DoubleItem;

  edm::InputTag fPatTriggerSrc;
  std::string fL1MetCollection;
  XYZTLorentzVector fL1Met;
  std::vector<MetItem> fMets;
  std::vector<DoubleItem> fDoubles;

  HPlus::TreeEventBranches fEventBranches;
};

HPlusMetNtupleAnalyzer::HPlusMetNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
  fL1MetCollection("l1extraParticles:MET")
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

  fTree->Branch("l1Met", &fL1Met);

  for(size_t i=0; i<fMets.size(); ++i) {
    fTree->Branch(fMets[i].name.c_str(), &(fMets[i].value));
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fTree->Branch(fDoubles[i].name.c_str(), &(fDoubles[i].value));
  }
}

HPlusMetNtupleAnalyzer::~HPlusMetNtupleAnalyzer() {}

void HPlusMetNtupleAnalyzer::reset() {
  double nan = std::numeric_limits<double>::quiet_NaN();
 
  fEventBranches.reset();
  fL1Met.SetXYZT(nan, nan, nan, nan);
  for(size_t i=0; i<fMets.size(); ++i) {
    fMets[i].value.SetXYZT(nan, nan, nan, nan);
  }
  for(size_t i=0; i<fDoubles.size(); ++i) {
    fDoubles[i].value = nan;
  }
}

void HPlusMetNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);

  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(fPatTriggerSrc, htrigger);

  // L1 MET
  pat::TriggerObjectRefVector l1mets = htrigger->objects(trigger::TriggerL1ETM);
  if(!l1mets.empty()) {
    if(l1mets.size() != 1) {
      bool found = false;
      for(size_t i=0; i<l1mets.size(); ++i) {
        if(l1mets[i]->coll(fL1MetCollection)) {
          fL1Met = l1mets[i]->p4();
          found = true;
          break;
        }
      }
      if(!found) {
        std::stringstream ss;
        for(size_t i=0; i<l1mets.size(); ++i) {
          ss << l1mets[i]->collection() << " " << l1mets[i]->et() << " ";
        }
        throw cms::Exception("Assert") << "No L1 MET from collection " << fL1MetCollection 
                                       << ", have " << l1mets.size() << " L1 MET objects: " << ss.str()
                                       << " at " << __FILE__ << ":" << __LINE__ << std::endl;
      }
    }
    fL1Met = l1mets[0]->p4();
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

DEFINE_FWK_MODULE(HPlusMetNtupleAnalyzer);
