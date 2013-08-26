#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. In other words, this class is suitable for *one
// candidate only*. If more taus are needed, look for the
// CandViewNtpProducer first!

class HPlusVertexCountProducer: public edm::EDProducer {
 public:

  explicit HPlusVertexCountProducer(const edm::ParameterSet&);
  ~HPlusVertexCountProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag fSrc;
  std::string fAlias;
};

HPlusVertexCountProducer::HPlusVertexCountProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")),
  fAlias(iConfig.getParameter<std::string>("alias"))
{
  produces<int>().setBranchAlias(fAlias);
}
HPlusVertexCountProducer::~HPlusVertexCountProducer() {}
void HPlusVertexCountProducer::beginJob() {}

void HPlusVertexCountProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvertices;
  iEvent.getByLabel(fSrc, hvertices);

  iEvent.put(std::auto_ptr<int>(new int(hvertices->size())));
}

void HPlusVertexCountProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexCountProducer);
