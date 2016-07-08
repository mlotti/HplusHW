#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"

#include <vector>
#include <iostream>

class HPlusGenBQuarkFilter: public edm::EDFilter {
public:
  explicit HPlusGenBQuarkFilter(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
    fNumberOfBJetsCut(iConfig.getUntrackedParameter<uint32_t>("bjetNumber"), iConfig.getUntrackedParameter<std::string>("bjetNumberCutDirection")) {

  }
  ~HPlusGenBQuarkFilter() {}

private:
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Return true for data events
    if (iEvent.isRealData()) return true;

    edm::Handle<edm::View<reco::GenParticle> > hcand;
    iEvent.getByLabel(fSrc, hcand);

    size_t nBjets = 0;
    //double myPreviousPt = 0.0;
    // Loop over gen particles
    for(edm::View<reco::GenParticle>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      // Find b quark
      if (std::abs((*iCand).pdgId()) != 5) continue;
      // Apply cut on status
      if ((*iCand).status() >= 10) continue;
      // Require that offspring does not include a b jet (i.e. do not double count initial/final state radiation)
      bool myOffspringIsBjetStatus = false;
      for(size_t i=0; i < (*iCand).numberOfDaughters(); ++i) {
        if (std::abs((*iCand).daughter(i)->pdgId()) == 5)
          myOffspringIsBjetStatus = true;
      }
      if (myOffspringIsBjetStatus) continue;
      ++nBjets;
      //if (std::fabs(myPreviousPt - (*iCand).pt()) < 0.001) std::cout << "***" << std::endl;
      //myPreviousPt = (*iCand).pt();
      //std::cout << nBjets << "  " << (*iCand).status() << "  " << (*iCand).pt() << std::endl;
    }
    // Make cut
    return fNumberOfBJetsCut.passedCut(nBjets);
  }

  edm::InputTag fSrc;
  HPlus::DirectionalCut fNumberOfBJetsCut;
};

DEFINE_FWK_MODULE(HPlusGenBQuarkFilter);
