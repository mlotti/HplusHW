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
  }
}
