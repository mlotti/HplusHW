// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleTools_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleTools_h

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Common/interface/Ptr.h"

#include<vector>
//#include<iostream>

class TtGenEvent;

namespace HPlus {
  namespace GenParticleTools {
    const reco::GenParticle *rewindChainUp(const reco::GenParticle *particle);
    const reco::GenParticle *rewindChainDown(const reco::GenParticle *particle);

    template <typename I, typename R>
    const reco::GenParticle *findMatching(const I& begin, const I& end, unsigned pdgId, const R& reference, double deltaR, bool visibleTau=false) {
      const reco::GenParticle *found = 0;

      double maxDR = deltaR;
      for(I iter=begin; iter != end; ++iter) {
        if(static_cast<unsigned>(std::abs(iter->pdgId())) == pdgId) {
          if(iter->mother() && iter->mother()->pdgId() == iter->pdgId())
            continue;

          double dR;
          if(visibleTau) {
            dR = reco::deltaR(calculateVisibleTau(&(*iter)), reference);
          }
          else {
            dR = reco::deltaR(*iter, reference);
          }

          if(dR < maxDR) {
            maxDR = dR;
            found = dynamic_cast<const reco::GenParticle *>(&(*iter));
          }
        }
      }

      if(found) {
        //found = rewindChainUp(found);
        /*
        std::cout << "Closest genParticle to (pt,eta,phi) (" << reference.pt() << ", " << reference.eta() << ", " << reference.phi() 
                  << ") is (" << found->pt() << ", " << found->eta() << ", " << found->phi()
                  << " mother is " << found->mother()->pdgId()
                  << ") deltaR " << maxDR
                  << std::endl;
        */
      }

      return found;
    }

    const reco::GenParticle *findMother(const reco::GenParticle *particle);
    const reco::GenParticle *hasMother(const reco::GenParticle *particle, unsigned pdgId);
    const reco::GenParticle *findMaxNonNeutrinoDaughter(const reco::GenParticle *particle);

    const reco::GenParticle *findTauDaughter(const reco::GenParticle *tau);

    const math::XYZTLorentzVector calculateVisibleTau(const reco::GenParticle *tau);

    std::vector<const reco::GenParticle *> findTTBarWdecays(const edm::PtrVector<reco::GenParticle>& particles);

    int calculateTTBarNumberOfLeptons(const TtGenEvent& ttGenEven);
  }
}

#endif
