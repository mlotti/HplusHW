#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class HPlusPileupNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusPileupNtupleProducer(const edm::ParameterSet&);
  ~HPlusPileupNtupleProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag fSrc;
};

HPlusPileupNtupleProducer::HPlusPileupNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src"))
{
  std::string alias = iConfig.getParameter<std::string>("alias");
  produces<float>("aveNvtx").setBranchAlias(alias);
}
HPlusPileupNtupleProducer::~HPlusPileupNtupleProducer() {}

void HPlusPileupNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<float> ave_nvtx(new float(-1));
  if(!iEvent.isRealData()) {
    edm::Handle<std::vector<PileupSummaryInfo> >  hpu;
    iEvent.getByLabel(fSrc, hpu);

    int npv = 0;
    for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
      npv += iPV->getPU_NumInteractions();
    }
    *ave_nvtx = npv/3.;
  }
  iEvent.put(ave_nvtx, "aveNvtx");
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPileupNtupleProducer);
