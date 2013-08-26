#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include<string>
#include<limits>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. In other words, this class is suitable for *one tau
// only*. If more taus are needed, look for the CandViewNtpProducer
// first!

class HPlusTauNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusTauNtupleProducer(const edm::ParameterSet&);
  ~HPlusTauNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  struct Discriminator {
    Discriminator(const std::string& d): fDiscr(d) {}
    std::string fDiscr;
    std::vector<float> fValues;
  };

  typedef math::XYZTLorentzVector XYZTLorentzVector;
  typedef math::XYZPoint XYZPoint;

  std::vector<Discriminator> fTauDiscriminators;
  edm::InputTag fSrc;

  edm::InputTag fVertexSrc;
  double fVertexDeltaSq;
  bool fDoVertices;
};

HPlusTauNtupleProducer::HPlusTauNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")),
  fDoVertices(false)
{
  std::string prefix(iConfig.getParameter<std::string>("prefix"));
  std::string name;

  // tau branches
  name = "p4";
  produces<std::vector<XYZTLorentzVector> >(name).setBranchAlias(prefix+name);
  name = "leadingPFChargedHadrCandP4";
  produces<std::vector<XYZTLorentzVector> >(name).setBranchAlias(prefix+name);
  name = "vertex";
  produces<std::vector<XYZPoint> >(name).setBranchAlias(prefix+name);
  name = "nprong";
  produces<std::vector<short> >(name).setBranchAlias(prefix+name);

  if(iConfig.exists("tauDiscriminators")) {
    std::vector<std::string> tauParam = iConfig.getParameter<std::vector<std::string> >("tauDiscriminators");
    fTauDiscriminators.reserve(tauParam.size());
    for(size_t i=0; i<tauParam.size(); ++i) {
      name = tauParam[i];
      produces<std::vector<float> >(name).setBranchAlias(prefix+"id_"+name);
      fTauDiscriminators.push_back(Discriminator(name));
    }
  }

  if(iConfig.exists("vertexSrc")) {
    fDoVertices = true;
    fVertexSrc = iConfig.getParameter<edm::InputTag>("vertexSrc");
    fVertexDeltaSq = iConfig.getParameter<double>("vertexMaxDelta");
    fVertexDeltaSq *= fVertexDeltaSq;
    name = "vertexIndex";
    produces<std::vector<short> >(name).setBranchAlias(prefix+name);
  }
}
HPlusTauNtupleProducer::~HPlusTauNtupleProducer() {}
void HPlusTauNtupleProducer::beginJob() {}

void HPlusTauNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  edm::Handle<edm::View<reco::Vertex> > hvertices;

  if(fDoVertices) {
    iEvent.getByLabel(fVertexSrc, hvertices);
    if(hvertices->size() > static_cast<size_t>(std::numeric_limits<short>::max()))
      throw cms::Exception("AssumptionFailed") << "The assumption that short would be enough to store vertex indices just failed. Max value " << std::numeric_limits<short>::max() << ", number of vertices " << hvertices->size() << std::endl;
  }

  std::auto_ptr<std::vector<XYZTLorentzVector> > p4s(new std::vector<XYZTLorentzVector>());
  std::auto_ptr<std::vector<XYZTLorentzVector> > leadingP4s(new std::vector<XYZTLorentzVector>());
  std::auto_ptr<std::vector<XYZPoint> > vertices(new std::vector<XYZPoint>());
  std::auto_ptr<std::vector<short> > nprongs(new std::vector<short>());

  std::auto_ptr<std::vector<short> > vertexIndices;

  if(fDoVertices) {
    vertexIndices.reset(new std::vector<short>());
    vertexIndices->reserve(hcands->size());
  }

  p4s->reserve(hcands->size());
  leadingP4s->reserve(hcands->size());
  vertices->reserve(hcands->size());
  nprongs->reserve(hcands->size());
  for(size_t i=0; i<fTauDiscriminators.size(); ++i) {
    fTauDiscriminators[i].fValues.reserve(hcands->size());
  }

  // Loop over taus
  for(size_t i=0; i<hcands->size(); ++i) {
    edm::Ptr<pat::Tau> tau(hcands->ptrAt(i));
    if(tau.get() == 0) {
      throw cms::Exception("ProductNotFound") << "Object " << i << " in tau collection " << fSrc.encode() << " is not derived from pat::Tau" << std::endl;
    }

    p4s->push_back(XYZTLorentzVector(tau->p4()));
    
    size_t n = tau->signalPFChargedHadrCands().size();
    nprongs->push_back(n);
    if(n > 0) {
      leadingP4s->push_back(XYZTLorentzVector(tau->leadPFChargedHadrCand()->p4()));
    }
    else {
      leadingP4s->push_back(XYZTLorentzVector());
    }
    vertices->push_back(XYZPoint(tau->vertex()));
    for(std::vector<Discriminator>::iterator iDiscr = fTauDiscriminators.begin(); iDiscr != fTauDiscriminators.end(); ++iDiscr) {
      iDiscr->fValues.push_back(tau->tauID(iDiscr->fDiscr));
    }

    // Find the matching vertex, store index
    if(fDoVertices) {
      short minJ = -1;
      double minDeltaSq = 2*fVertexDeltaSq;
      for(size_t j=0; j<hvertices->size(); ++j) {
        double deltaSq = (tau->vertex() - hvertices->at(j).position()).Mag2();
        if(deltaSq < fVertexDeltaSq && deltaSq < minDeltaSq) {
          minDeltaSq = deltaSq;
          minJ = j;
        }
      }
      vertexIndices->push_back(minJ);
    }
  }

  iEvent.put(p4s, "p4");
  iEvent.put(leadingP4s, "leadingPFChargedHadrCandP4");
  iEvent.put(vertices, "vertex");
  iEvent.put(nprongs, "nprong");

  for(std::vector<Discriminator>::iterator iDiscr = fTauDiscriminators.begin(); iDiscr != fTauDiscriminators.end(); ++iDiscr) {
    iEvent.put(std::auto_ptr<std::vector<float> >(new std::vector<float>(iDiscr->fValues)), iDiscr->fDiscr);
    iDiscr->fValues.clear();
  }

  if(fDoVertices)
    iEvent.put(vertexIndices, "vertexIndex");
}

void HPlusTauNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauNtupleProducer);
