#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class HPlusVertexViewSumPtComputer: public edm::EDProducer {
public:
  explicit HPlusVertexViewSumPtComputer(const edm::ParameterSet&);
  ~HPlusVertexViewSumPtComputer();

private:
  typedef edm::ValueMap<float> MapType;

  virtual void beginJob();
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob();

  edm::InputTag src;
};

HPlusVertexViewSumPtComputer::HPlusVertexViewSumPtComputer(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src"))
{
  produces<MapType>("sumPt");
  produces<MapType>("sumPt2");
}

HPlusVertexViewSumPtComputer::~HPlusVertexViewSumPtComputer() {}

void HPlusVertexViewSumPtComputer::beginJob() {}
void HPlusVertexViewSumPtComputer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(src, hvertex);

  std::vector<float> sumPt;
  std::vector<float> sumPt2;
  for(edm::View<reco::Vertex>::const_iterator iVertex = hvertex->begin(); iVertex != hvertex->end(); ++iVertex) {
    float sPt = 0.0;
    float sPt2 = 0.0;

    for(reco::Vertex::trackRef_iterator iTrack = iVertex->tracks_begin(); iTrack != iVertex->tracks_end(); ++iTrack) {
      float pt = (*iTrack)->pt();
      sPt += pt;
      sPt2 += pt*pt;
    }

    sumPt.push_back(sPt);
    sumPt2.push_back(sPt2);
  }

  // Fill the value map
  std::auto_ptr<MapType> valueMap(new MapType());
  MapType::Filler filler(*valueMap);
  filler.insert(hvertex, sumPt.begin(), sumPt.end());
  filler.fill();
  iEvent.put(valueMap, "sumPt");

  std::auto_ptr<MapType> valueMap2(new MapType());
  MapType::Filler filler2(*valueMap2);
  filler2.insert(hvertex, sumPt2.begin(), sumPt2.end());
  filler2.fill();
  iEvent.put(valueMap2, "sumPt2");
}

void HPlusVertexViewSumPtComputer::endJob() {}

DEFINE_FWK_MODULE(HPlusVertexViewSumPtComputer);
