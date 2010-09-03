// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TransverseMass_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TransverseMass_h

namespace reco {
  class Candidate;
  class MET;
}

namespace HPlus {
  class TransverseMass {
  public:
    static double reconstruct(const reco::Candidate& tau, const reco::MET& met);
  };
}

#endif
