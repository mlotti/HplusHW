#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

class HPlusCandViewSumPtComputer: public edm::EDProducer {
public:
  explicit HPlusCandViewSumPtComputer(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src")) {
    produces<double>();
  }
  ~HPlusCandViewSumPtComputer() {}

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<reco::Candidate> > hcand;
    iEvent.getByLabel(fSrc, hcand);

    double sum = 0;
    for(edm::View<reco::Candidate>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      sum += iCand->pt();
    }

    std::auto_ptr<double> prod(new double(sum));
    iEvent.put(prod);
  }

  edm::InputTag fSrc;
};

DEFINE_FWK_MODULE(HPlusCandViewSumPtComputer);
