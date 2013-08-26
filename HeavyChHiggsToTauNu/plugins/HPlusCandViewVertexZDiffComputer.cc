#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusCandViewVertexZDiffComputer: public edm::EDProducer {
public:
  explicit HPlusCandViewVertexZDiffComputer(const edm::ParameterSet&);
  ~HPlusCandViewVertexZDiffComputer();

private:
  typedef edm::ValueMap<float> MapType;

  virtual void beginJob();
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob();

  edm::InputTag candSrc;
  edm::InputTag vertexSrc;
};

HPlusCandViewVertexZDiffComputer::HPlusCandViewVertexZDiffComputer(const edm::ParameterSet& iConfig):
  candSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
  vertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc"))
{
  produces<MapType>();
}

HPlusCandViewVertexZDiffComputer::~HPlusCandViewVertexZDiffComputer() {}

void HPlusCandViewVertexZDiffComputer::beginJob() {}
void HPlusCandViewVertexZDiffComputer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(candSrc, hcand);

  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(vertexSrc, hvertex);

  if(hvertex->empty())
    throw cms::Exception("LogicError") << "Got empty vertex collection " << vertexSrc.encode() << std::endl;
  const reco::Vertex& vertex = hvertex->at(0);
  
  std::vector<float> diff;
  diff.reserve(hcand->size());
  for(size_t i=0; i<hcand->size(); ++i) {
    diff.push_back(std::abs(hcand->at(i).vertex().z() - vertex.z()));
  }

  // Fill the value map
  std::auto_ptr<MapType> valueMap(new MapType());
  MapType::Filler filler(*valueMap);
  filler.insert(hcand, diff.begin(), diff.end());
  filler.fill();

  iEvent.put(valueMap);
}

void HPlusCandViewVertexZDiffComputer::endJob() {}

DEFINE_FWK_MODULE(HPlusCandViewVertexZDiffComputer);
