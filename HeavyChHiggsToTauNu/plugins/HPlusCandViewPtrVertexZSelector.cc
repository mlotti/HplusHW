#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusCandViewPtrVertexZSelector: public edm::EDProducer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusCandViewPtrVertexZSelector(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusCandViewPtrVertexZSelector();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  typedef edm::PtrVector<reco::Candidate> Product;

  edm::InputTag candSrc;
  edm::InputTag vertexSrc;
  double maxZ;
};

HPlusCandViewPtrVertexZSelector::HPlusCandViewPtrVertexZSelector(const edm::ParameterSet& iConfig):
  candSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
  vertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  maxZ(iConfig.getParameter<double>("maxZ"))
{
  produces<Product>();
}

HPlusCandViewPtrVertexZSelector::~HPlusCandViewPtrVertexZSelector() {}

void HPlusCandViewPtrVertexZSelector::beginJob() {}

void HPlusCandViewPtrVertexZSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(candSrc, hcand);

  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(vertexSrc, hvertex);

  std::auto_ptr<Product> prod(new Product());

  for(edm::View<reco::Candidate>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
    for(edm::View<reco::Vertex>::const_iterator iVertex = hvertex->begin(); iVertex != hvertex->end(); ++iVertex) {
      if(std::abs(iCand->vertex().z() - iVertex->z()) < maxZ)
        prod->push_back(hcand->ptrAt(iCand-hcand->begin()));
    }
  }

  iEvent.put(prod);
}

void HPlusCandViewPtrVertexZSelector::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewPtrVertexZSelector);
