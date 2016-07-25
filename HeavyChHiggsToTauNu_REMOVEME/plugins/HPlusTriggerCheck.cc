#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

#include<vector>
#include<string>

class HPlusTriggerCheck: public edm::EDAnalyzer {
 public:

  explicit HPlusTriggerCheck(const edm::ParameterSet&);
  ~HPlusTriggerCheck();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  edm::InputTag src_;
  std::vector<std::string> triggers_;
};

HPlusTriggerCheck::HPlusTriggerCheck(const edm::ParameterSet& iConfig):
  src_(iConfig.getUntrackedParameter<edm::InputTag>("src")),
  triggers_(iConfig.getUntrackedParameter<std::vector<std::string> >("pathNames"))
{}
HPlusTriggerCheck::~HPlusTriggerCheck() {}

void HPlusTriggerCheck::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(src_, htrigger);

  for(std::vector<std::string>::const_iterator iName = triggers_.begin(); iName != triggers_.end(); ++iName) {
    if(htrigger->path(*iName) == 0)
      throw cms::Exception("Configuration") << "The trigger path '" << *iName << "' was not found from tha pat::TriggerEvent '" << src_.encode() << "'" << std::endl;
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTriggerCheck);
