#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusVertexNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusVertexNtupleProducer(const edm::ParameterSet&);
  ~HPlusVertexNtupleProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef math::XYZPoint XYZPoint;

  edm::InputTag fSrc;
  edm::InputTag fGoodSrc;
  edm::InputTag fSumPtSrc;
  edm::InputTag fSumPt2Src;

  double fDeltaSq;
  bool fDoSumPt;
};

HPlusVertexNtupleProducer::HPlusVertexNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")), 
  fGoodSrc(iConfig.getParameter<edm::InputTag>("goodSrc")),
  fDeltaSq(iConfig.getParameter<double>("maxDelta")),
  fDoSumPt(false)
{
  fDeltaSq *= fDeltaSq;

  std::string prefix(iConfig.getParameter<std::string>("prefix"));
  std::string name;

  // vertex branches
  name = "position";
  produces<std::vector<XYZPoint> >(name).setBranchAlias(prefix+name);
  name = "good";
  produces<std::vector<bool> >(name).setBranchAlias(prefix+name);

  if(iConfig.exists("sumPtSrc") || iConfig.exists("sumPt2Src")) {
    fDoSumPt = true;
    fSumPtSrc = iConfig.getParameter<edm::InputTag>("sumPtSrc");
    fSumPt2Src = iConfig.getParameter<edm::InputTag>("sumPt2Src");

    name = "sumPt";
    produces<std::vector<float> >(name).setBranchAlias(prefix+name);
    name = "sumPt2";
    produces<std::vector<float> >(name).setBranchAlias(prefix+name);
  }
}
HPlusVertexNtupleProducer::~HPlusVertexNtupleProducer() {}

void HPlusVertexNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvertices;
  iEvent.getByLabel(fSrc, hvertices);

  edm::Handle<edm::View<reco::Vertex> > hgoodvertices;
  iEvent.getByLabel(fGoodSrc, hgoodvertices);

  edm::Handle<edm::ValueMap<float> > hsumpt;
  edm::Handle<edm::ValueMap<float> > hsumpt2;

  if(fDoSumPt) {
    iEvent.getByLabel(fSumPtSrc, hsumpt);
    iEvent.getByLabel(fSumPt2Src, hsumpt2);
  }

  std::auto_ptr<std::vector<XYZPoint> > vertices(new std::vector<XYZPoint>());
  std::auto_ptr<std::vector<bool> > isGood(new std::vector<bool>());
  vertices->reserve(hvertices->size());
  isGood->reserve(hvertices->size());

  std::auto_ptr<std::vector<float> > sumPt;
  std::auto_ptr<std::vector<float> > sumPt2;
  if(fDoSumPt) {
    sumPt.reset(new std::vector<float>());
    sumPt2.reset(new std::vector<float>());
    sumPt->reserve(hvertices->size());
    sumPt2->reserve(hvertices->size());
  }

  // Loop over vertices
  for(size_t i=0; i<hvertices->size(); ++i) {
    XYZPoint pos(hvertices->at(i).position());
    vertices->push_back(pos);

    short minJ = -1;
    double minDeltaSq = 2*fDeltaSq;
    for(size_t j=0; j<hgoodvertices->size(); ++j) {
      double deltaSq = (pos - hgoodvertices->at(j).position()).Mag2();
      if(deltaSq < fDeltaSq && deltaSq < minDeltaSq) {
        if(minJ >= 0)
          throw cms::Exception("LogicError") << "The assumption that there would be only one vertex pair within " << std::sqrt(fDeltaSq) << " failed. First was within " << std::sqrt(minDeltaSq) << ", second one is " << std::sqrt(deltaSq) << std::endl;
        minDeltaSq = deltaSq;
        minJ = j;
      }
    }
    isGood->push_back(minJ >= 0);

    if(fDoSumPt) {
      sumPt->push_back( (*hsumpt)[hvertices->refAt(i)] );
      sumPt2->push_back( (*hsumpt2)[hvertices->refAt(i)] );
    }
  }

  iEvent.put(vertices, "position");
  iEvent.put(isGood, "good");

  if(fDoSumPt) {
    iEvent.put(sumPt, "sumPt");
    iEvent.put(sumPt2, "sumPt2");
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexNtupleProducer);
