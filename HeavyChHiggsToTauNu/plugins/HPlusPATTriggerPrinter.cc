#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

#include<set>
#include<string>

class HPlusPATTriggerPrinter: public edm::EDAnalyzer {
public:
  explicit HPlusPATTriggerPrinter(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src"))
  {}
  ~HPlusPATTriggerPrinter() {}

  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<pat::TriggerEvent> htrigger;
    iEvent.getByLabel(fSrc, htrigger);

    pat::TriggerObjectRefVector objects = htrigger->objectRefs();
    for(size_t i=0; i<objects.size(); ++i) {
      fCollections.insert(objects[i]->collection());
    }
    
  }

  void endJob() {
    std::cout << "TriggerObject collections" << std::endl;
    for(std::set<std::string>::const_iterator iName = fCollections.begin(); iName != fCollections.end(); ++iName) {
      std::cout << *iName << std::endl;
    }
  }

private:
  edm::InputTag fSrc;
  std::set<std::string> fCollections;
};

DEFINE_FWK_MODULE( HPlusPATTriggerPrinter );
