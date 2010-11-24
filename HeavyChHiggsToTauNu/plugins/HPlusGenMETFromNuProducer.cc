#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include<vector>

class HPlusGenMETFromNuProducer: public edm::EDProducer {
 public:

  explicit HPlusGenMETFromNuProducer(const edm::ParameterSet&);
  ~HPlusGenMETFromNuProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag src;
  edm::InputTag embeddedSrc;
};

HPlusGenMETFromNuProducer::HPlusGenMETFromNuProducer(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  embeddedSrc(iConfig.exists("embeddedSrc") ? iConfig.getParameter<edm::InputTag>("embeddedSrc") : edm::InputTag("dummy"))
{
  produces<std::vector<reco::GenMET> >();
}
HPlusGenMETFromNuProducer::~HPlusGenMETFromNuProducer() {}

void HPlusGenMETFromNuProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::GenParticle> > hgen;
  iEvent.getByLabel(src, hgen);

  double met_x = 0;
  double met_y = 0;
  double met_z = 0;

  for(edm::View<reco::GenParticle>::const_iterator iGen = hgen->begin(); iGen != hgen->end(); ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
      met_x += iGen->px();
      met_y += iGen->py();
      met_z += iGen->pz();
    }
  }

  if(iEvent.getByLabel(embeddedSrc, hgen)) {
    for(edm::View<reco::GenParticle>::const_iterator iGen = hgen->begin(); iGen != hgen->end(); ++iGen) {
      int pdgId = std::abs(iGen->pdgId());
      if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
        const reco::GenParticle *particle = &(*(iGen));
        bool isFromTau = false;
        while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(particle->mother())) {
          if(std::abs(mother->pdgId()) == 15) {
            isFromTau = true;
            break;
          }
          else {
            particle = mother;
          }
        }
        if(isFromTau) {
          met_x += iGen->px();
          met_y += iGen->py();
          met_z += iGen->pz();
        }
      }
    }
  }

  reco::GenMET::LorentzVector metP4(met_x, met_y, met_z, std::sqrt(met_x*met_x + met_y+met_y));
  reco::GenMET::Point vertex(0, 0, 0);

  SpecificGenMETData specific;
  specific.NeutralEMEtFraction = 0.0;
  specific.NeutralEMEtFraction = 0.0;
  specific.NeutralHadEtFraction = 0.0;
  specific.ChargedEMEtFraction = 0.0;
  specific.ChargedHadEtFraction = 0.0;
  specific.MuonEtFraction = 0.0;
  specific.InvisibleEtFraction = 0.0;

  std::auto_ptr<std::vector<reco::GenMET> > ret(new std::vector<reco::GenMET>());
  ret->push_back(reco::GenMET(specific, 0.0, metP4, vertex));

  iEvent.put(ret);
}

DEFINE_FWK_MODULE(HPlusGenMETFromNuProducer);
