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
  }
}
