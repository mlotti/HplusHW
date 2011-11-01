// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhiJets_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhiJets_h
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

namespace reco {
  class Candidate;
  class JetSelection;

}

namespace HPlus {
  class DeltaPhiJets {
  public:
    static double reconstruct(const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
  };
}

#endif
