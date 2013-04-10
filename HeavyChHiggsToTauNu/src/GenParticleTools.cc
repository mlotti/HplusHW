#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "FWCore/Utilities/interface/Exception.h"

namespace {
  void visibleTauHelper(const reco::Candidate *cand, math::XYZTLorentzVector& result) {
    // stable
    if(cand->status() == 1) {
      // ignore neutrinos
      int pdgid = std::abs(cand->pdgId());
      if(pdgid == 12 || pdgid == 14 || pdgid == 16)
        return;

      result += cand->p4();
      if(cand->numberOfDaughters() > 0)
        throw cms::Exception("Assert") << "Candidate has status 1, and " << cand->numberOfDaughters() << " daughters in " << __FILE__ << ":" << __LINE__;
    }
    else {
      for(size_t i=0; i<cand->numberOfDaughters(); ++i) {
        visibleTauHelper(cand->daughter(i), result);
      }
    }
  }
}

namespace HPlus {
  namespace GenParticleTools {
    const reco::GenParticle *rewindChainUp(const reco::GenParticle *particle) {
      const reco::GenParticle *tmp = particle;
      int pdgId = particle->pdgId();
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(tmp->mother())) {
        if(mother->pdgId() == pdgId) {
          tmp = mother;
          continue;
        }
        return tmp;
      }
      return 0;
    }                                                                               

    const reco::GenParticle *rewindChainDown(const reco::GenParticle *particle) {
      const reco::GenParticle *tmp = particle;
      int pdgId = particle->pdgId();
      bool daughterIsSame = true;
      while(daughterIsSame) {
        daughterIsSame = false;
        size_t n = tmp->numberOfDaughters();
        //std::cout << "Daughters " << n << std::endl;
        for(size_t i=0; i<n; ++i) {
          //std::cout << "  daughter " << i << std::endl;
          //std::cout << "    pdgId " << tmp->daughter(i)->pdgId() << std::endl;
          if(tmp->daughter(i)->pdgId() == pdgId) {
            tmp = dynamic_cast<const reco::GenParticle *>(tmp->daughter(i));
            daughterIsSame = true;
            break;
          }
        }
      }
      return tmp;
    }                                                                               

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

    const reco::GenParticle *hasMother(const reco::GenParticle *particle, unsigned pdgId) {
      const reco::GenParticle *tmp = particle;
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(tmp->mother())) {
        if(static_cast<unsigned>(std::abs(mother->pdgId())) == pdgId)
          return mother;
        tmp = mother;
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
        if(id == particle->pdgId())
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

    const math::XYZTLorentzVector calculateVisibleTau(const reco::GenParticle *tau) {
      if(std::abs(tau->pdgId()) != 15)
        throw cms::Exception("LogicError") << "GenParticleTools::calculateVisibleTau() requires a reco::GenParticle with abs(pdgId) == 15, got " << tau->pdgId() << std::endl;

      tau = rewindChainDown(tau);
      math::XYZTLorentzVector result;
      visibleTauHelper(tau, result);
      return result;
    }
  }
}
