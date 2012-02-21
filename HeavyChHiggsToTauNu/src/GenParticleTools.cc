#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

namespace HPlus {
  namespace GenParticleTools {
    const reco::GenParticle *findMother(const reco::GenParticle *particle) {
      const reco::GenParticle *tmp = particle;
      int pdgId = particle->pdgId();
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(tmp->mother())) {
        if(mother->pdgId() == pdgId) {
          tmp = mother;
          continue;
        }
        return mother;
      }
      return 0;
    }

    const reco::GenParticle *findMaxNonNeutrinoDaughter(const reco::GenParticle *particle) {
      const reco::GenParticle *daughter = 0;
      int did = 0;

      size_t n = particle->numberOfDaughters();
      for(size_t i=0; i<n; ++i) {
        int id = particle->daughter(i)->pdgId();
        int ida = std::abs(id);
        if(ida == 12 || ida == 14 || ida == 16)
          continue;
        if(ida > std::abs(did)) {
          did = id;
          daughter = dynamic_cast<const reco::GenParticle *>(particle->daughter(i));
        }
      }

      return daughter;
    }

    const reco::GenParticle *findTauDaughter(const reco::GenParticle *tau) {
      const reco::GenParticle *daughter = 0;
      int did = 0;

      size_t nDaughters = tau->numberOfDaughters();
      for(size_t i=0; i<nDaughters; ++i) {
        int id = tau->daughter(i)->pdgId();
        int ida = std::abs(id);
        // ignore neutrinos
        if(ida == 12 || ida == 14 || ida == 16)
          continue;

        // if e/mu, take it
        if(ida == 11 || ida == 13)
          return dynamic_cast<const reco::GenParticle *>(tau->daughter(i));

        // if W, look for it's non-neutrino daughter
        if(ida == 24) {
          const reco::GenParticle *daugh = GenParticleTools::findMaxNonNeutrinoDaughter(dynamic_cast<const reco::GenParticle *>(tau->daughter(i)));
          if(daugh != 0)
            return daugh;
        }
          
        // else, take the one with largest id number, and continue
        if(ida > std::abs(did)) {
          did = id;
          daughter = dynamic_cast<const reco::GenParticle *>(tau->daughter(i));
        }
      }

      // If again tau, try the daughter of it
      if(std::abs(did) == 15)
        daughter = findTauDaughter(daughter);

      return daughter;
    }

  }
}
