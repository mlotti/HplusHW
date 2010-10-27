#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

class HPlusSelectFirstVertex: public edm::EDProducer {
 public:

  explicit HPlusSelectFirstVertex(const edm::ParameterSet&);
  ~HPlusSelectFirstVertex();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag src;
};

HPlusSelectFirstVertex::HPlusSelectFirstVertex(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src"))
{
  produces<reco::VertexCollection>();
}

HPlusSelectFirstVertex::~HPlusSelectFirstVertex() {}

void HPlusSelectFirstVertex::beginJob() {}

void HPlusSelectFirstVertex::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(src, hvertex);

  std::auto_ptr<reco::VertexCollection> prod(new reco::VertexCollection());
  prod->push_back((*hvertex)[0]);

  iEvent.put(prod);
}

void HPlusSelectFirstVertex::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusSelectFirstVertex);
