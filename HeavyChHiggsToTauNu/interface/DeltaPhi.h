// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhi_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhi_h

namespace reco {
  class Candidate;
  class MET;
}

namespace HPlus {
  class DeltaPhi {
  public:
    static double reconstruct(const reco::Candidate& tau, const reco::MET& met);
      };
}

#endif
