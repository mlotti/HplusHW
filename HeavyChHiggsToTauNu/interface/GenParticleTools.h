// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleTools_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleTools_h

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"

namespace HPlus {
  namespace GenParticleTools {
    template <typename I, typename R>
    const reco::GenParticle *findMatching(const I& begin, const I& end, unsigned pdgId, const R& reference, double deltaR) {
      const reco::GenParticle *found = 0;

      double maxDR = deltaR;
      for(I iter=begin; iter != end; ++iter) {
        if(static_cast<unsigned>(std::abs(iter->pdgId())) == pdgId) {
          double dR = reco::deltaR(*iter, reference);
          if(dR < maxDR) {
            maxDR = dR;
            found = dynamic_cast<const reco::GenParticle *>(&(*iter));
          }
        }
      }

      return found;
    }

    const reco::GenParticle *findMother(const reco::GenParticle *particle);
    const reco::GenParticle *findMaxNonNeutrinoDaughter(const reco::GenParticle *particle);
  }
}

#endif
