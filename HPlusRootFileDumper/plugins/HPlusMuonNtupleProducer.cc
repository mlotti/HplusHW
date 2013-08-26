#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusMuonNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusMuonNtupleProducer(const edm::ParameterSet&);
  ~HPlusMuonNtupleProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef math::XYZTLorentzVector XYZTLorentzVector;
  typedef math::XYZPoint XYZPoint;

  edm::InputTag fSrc;

  edm::InputTag fVertexSrc;
  double fVertexDeltaSq;
  bool fDoVertices;
};

HPlusMuonNtupleProducer::HPlusMuonNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")),
  fDoVertices(false)
{
  std::string prefix(iConfig.getParameter<std::string>("prefix"));
  std::string name;

  // muon branches
  name = "p4";
  produces<std::vector<XYZTLorentzVector> >(name).setBranchAlias(prefix+name);
  name = "vertex";
  produces<std::vector<XYZPoint> >(name).setBranchAlias(prefix+name);

  if(iConfig.exists("vertexSrc")) {
    fDoVertices = true;
    fVertexSrc = iConfig.getParameter<edm::InputTag>("vertexSrc");
    fVertexDeltaSq = iConfig.getParameter<double>("vertexMaxDelta");
    fVertexDeltaSq *= fVertexDeltaSq;
    name = "vertexIndex";
    produces<std::vector<short> >(name).setBranchAlias(prefix+name);
  }
}
HPlusMuonNtupleProducer::~HPlusMuonNtupleProducer() {}

void HPlusMuonNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  edm::Handle<edm::View<reco::Vertex> > hvertices;

  if(fDoVertices) {
    iEvent.getByLabel(fVertexSrc, hvertices);
    if(hvertices->size() > static_cast<size_t>(std::numeric_limits<short>::max()))
      throw cms::Exception("AssumptionFailed") << "The assumption that short would be enough to store vertex indices just failed. Max value " << std::numeric_limits<short>::max() << ", number of vertices " << hvertices->size() << std::endl;
  }

  std::auto_ptr<std::vector<XYZTLorentzVector> > p4s(new std::vector<XYZTLorentzVector>());
  std::auto_ptr<std::vector<XYZPoint> > vertices(new std::vector<XYZPoint>());

  std::auto_ptr<std::vector<short> > vertexIndices;

  if(fDoVertices) {
    vertexIndices.reset(new std::vector<short>());
    vertexIndices->reserve(hcands->size());
  }

  p4s->reserve(hcands->size());
  vertices->reserve(hcands->size());

  // Loop over muons
  for(size_t i=0; i<hcands->size(); ++i) {
    edm::Ptr<pat::Muon> muon(hcands->ptrAt(i));
    if(muon.get() == 0) {
      throw cms::Exception("ProductNotFound") << "Object " << i << " in muon collection " << fSrc.encode() << " is not derived from pat::Muon" << std::endl;
    }

    p4s->push_back(XYZTLorentzVector(muon->p4()));
    
    // Find the matching vertex, store index
    if(fDoVertices) {
      short minJ = -1;
      double minDeltaSq = 2*fVertexDeltaSq;
      for(size_t j=0; j<hvertices->size(); ++j) {
        double deltaSq = (muon->vertex() - hvertices->at(j).position()).Mag2();
        if(deltaSq < fVertexDeltaSq && deltaSq < minDeltaSq) {
          minDeltaSq = deltaSq;
          minJ = j;
        }
      }
      vertexIndices->push_back(minJ);
    }
  }

  iEvent.put(p4s, "p4");
  iEvent.put(vertices, "vertex");

  if(fDoVertices)
    iEvent.put(vertexIndices, "vertexIndex");
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMuonNtupleProducer);
