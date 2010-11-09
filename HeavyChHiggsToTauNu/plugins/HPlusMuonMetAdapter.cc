#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/METReco/interface/MET.h"

class HPlusMuonMetAdapter : public edm::EDProducer {
public:
  explicit HPlusMuonMetAdapter(const edm::ParameterSet&);
  ~HPlusMuonMetAdapter();

private:

  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  edm::InputTag srcMuon_;
  edm::InputTag srcMet_;
};

HPlusMuonMetAdapter::HPlusMuonMetAdapter(const edm::ParameterSet& iConfig):
  srcMuon_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  srcMet_(iConfig.getUntrackedParameter<edm::InputTag>("metSrc"))
{
  produces< std::vector< reco::Muon >  >();
}


HPlusMuonMetAdapter::~HPlusMuonMetAdapter() {}

void HPlusMuonMetAdapter::beginJob() {}

void HPlusMuonMetAdapter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Muon> > hmuon;
  iEvent.getByLabel(srcMuon_, hmuon);

  edm::Handle<edm::View<reco::MET> > hmet;
  iEvent.getByLabel(srcMet_, hmet);

  const reco::Muon::LorentzVector& muP4 = hmuon->at(0).p4();
  reco::Muon mu(hmuon->at(0).charge(), muP4, hmuon->at(0).vertex());
  mu.setInnerTrack(hmuon->at(0).innerTrack());

  const double massW = 80.403;
  const double massW2 = massW*massW;
  reco::Muon::LorentzVector nuP4 = hmet->at(0).p4();

  /*
  const double xsum = muP4.px() + nuP4.px();
  const double ysum = muP4.py() + nuP4.py();
  const double esum = muP4.E() + nuP4.E();
  const double A = -massW2 - xsum*xsum - ysum*ysum + esum*esum;
  if(A >= 0)
    nuP4.SetPz(-muP4.pz() + // can be minus too, select randomly? Does it matter?
               std::sqrt(A));
  */

  reco::Muon nu(-hmuon->at(0).charge(), nuP4, hmuon->at(0).vertex());
  nu.setInnerTrack(hmuon->at(0).innerTrack());
  
  std::auto_ptr<std::vector< reco::Muon > > ret(new std::vector< reco::Muon  > );
  ret->push_back(mu);
  ret->push_back(nu);
  iEvent.put(ret);

}

void HPlusMuonMetAdapter::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMuonMetAdapter);
