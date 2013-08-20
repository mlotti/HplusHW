#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusVertexReorderProducer: public edm::EDProducer {
public:
  explicit HPlusVertexReorderProducer(const edm::ParameterSet&);
  ~HPlusVertexReorderProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag fVertexSrc;
  edm::InputTag fIndexSrc;
};

HPlusVertexReorderProducer::HPlusVertexReorderProducer(const edm::ParameterSet& iConfig):
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  fIndexSrc(iConfig.getParameter<edm::InputTag>("indexSrc"))
{
  produces<std::vector<reco::Vertex> >();
}
HPlusVertexReorderProducer::~HPlusVertexReorderProducer() {}

void HPlusVertexReorderProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<std::vector<reco::Vertex> > hvertex;
  iEvent.getByLabel(fVertexSrc, hvertex);

  edm::Handle<int> hindex;
  iEvent.getByLabel(fIndexSrc, hindex);

  std::auto_ptr<std::vector<reco::Vertex> > product(new std::vector<reco::Vertex>());
  product->reserve(hvertex->size());

  if(*hindex >= static_cast<int>(hvertex->size()))
    throw cms::Exception("Assert") << "Index (" << *hindex << ") is larger than vertex collection size (" << hvertex->size() << ")!" << std::endl;

  // Pick the selected vertex to the first
  // Note that the case *hindex < 0 (no vertex selected, i.e. stick
  // with original orderr) gets handled automatically
  if(*hindex >= 0)
    product->push_back(hvertex->at(0));
  // Then copy the rest of the vertices
  for(size_t i=0; i<hvertex->size(); ++i) {
    if (static_cast<int>(i) != *hindex)
      product->push_back(hvertex->at(i));
  }

  iEvent.put(product);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexReorderProducer);
