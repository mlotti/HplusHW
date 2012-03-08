#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"

class HPlusBoolFilter: public edm::EDFilter {
 public:

  explicit HPlusBoolFilter(const edm::ParameterSet&);
  ~HPlusBoolFilter();

 private:
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag fSrc;
};

HPlusBoolFilter::HPlusBoolFilter(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src"))
{}
HPlusBoolFilter::~HPlusBoolFilter() {}


bool HPlusBoolFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<bool> handle;
  iEvent.getByLabel(fSrc, handle);

  return *handle;
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusBoolFilter);
