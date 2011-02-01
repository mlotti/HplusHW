#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/Math/interface/deltaR.h"

class HPlusPATTauCandViewDeltaRSelector : public edm::EDProducer {
public:
  explicit HPlusPATTauCandViewDeltaRSelector(const edm::ParameterSet&);
  ~HPlusPATTauCandViewDeltaRSelector();

private:

  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  edm::InputTag srcTau_;
  edm::InputTag srcCand_;
  const double maxDR_;
};

HPlusPATTauCandViewDeltaRSelector::HPlusPATTauCandViewDeltaRSelector(const edm::ParameterSet& iConfig):
  srcTau_(iConfig.getParameter<edm::InputTag>("tauSrc")),
  srcCand_(iConfig.getParameter<edm::InputTag>("candSrc")),
  maxDR_(iConfig.getParameter<double>("deltaR"))
{
  produces<pat::TauCollection>();
}


HPlusPATTauCandViewDeltaRSelector::~HPlusPATTauCandViewDeltaRSelector() {}

void HPlusPATTauCandViewDeltaRSelector::beginJob() {}

void HPlusPATTauCandViewDeltaRSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Tau> > hmuon;
  iEvent.getByLabel(srcTau_, hmuon);

  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(srcCand_, hcand);

  std::auto_ptr<pat::TauCollection> ret(new pat::TauCollection());

  for(edm::View<pat::Tau>::const_iterator iTau = hmuon->begin(); iTau != hmuon->end(); ++iTau) {
    for(edm::View<reco::Candidate>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      if(reco::deltaR(*iTau, *iCand) < maxDR_) {
        ret->push_back(*iTau);
        break;
      }
    }
  }
  
  iEvent.put(ret);

}

void HPlusPATTauCandViewDeltaRSelector::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);
