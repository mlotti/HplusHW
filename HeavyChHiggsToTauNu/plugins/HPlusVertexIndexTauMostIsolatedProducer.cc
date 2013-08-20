#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

class HPlusVertexIndexTauMostIsolatedProducer: public edm::EDProducer {
public:
  explicit HPlusVertexIndexTauMostIsolatedProducer(const edm::ParameterSet&);
  ~HPlusVertexIndexTauMostIsolatedProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag fVertexSrc;
  edm::InputTag fTauSrc;
  std::string fDiscriminator;
  double fMaxDz;
};

HPlusVertexIndexTauMostIsolatedProducer::HPlusVertexIndexTauMostIsolatedProducer(const edm::ParameterSet& iConfig):
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  fTauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  fDiscriminator(iConfig.getParameter<std::string>("tauDiscriminator")),
  fMaxDz(iConfig.getParameter<double>("dz"))
{
  produces<int>();
}
HPlusVertexIndexTauMostIsolatedProducer::~HPlusVertexIndexTauMostIsolatedProducer() {}

void HPlusVertexIndexTauMostIsolatedProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(fVertexSrc, hvertex);

  edm::Handle<edm::View<pat::Tau> > htau;
  iEvent.getByLabel(fTauSrc, htau);

  int index = -1;
  if(htau->size() > 0) {
    // First find the most isolated tau
    double discrValue = htau->at(0).tauID(fDiscriminator);
    edm::Ptr<pat::Tau> selectedTau = htau->ptrAt(0);
    for(size_t i=1; i<htau->size(); ++i) {
      double val = htau->at(i).tauID(fDiscriminator);
      if(val < discrValue) {
        selectedTau = htau->ptrAt(i);
        discrValue = val;
      }
    }

    // Then find the vertex of the tau from the list of all reco::Vertices
    size_t iVertex = 0;
    double dZ = std::abs(hvertex->at(0).z() - selectedTau->vz());
    for(size_t i=1; i<hvertex->size(); ++i) {
      double val = std::abs(hvertex->at(i).z() - selectedTau->vz());
      if(val < dZ) {
        dZ = val;
        iVertex = i;
      }
    }
    if(dZ < fMaxDz)
      index = iVertex;
  }

  iEvent.put(std::auto_ptr<int>(new int(index)));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexIndexTauMostIsolatedProducer);
