// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhi_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_DeltaPhi_h

namespace reco {
  class Candidate;
  class MET;
  
}

namespace pat {
  class Jet;
}

namespace HPlus {
  class DeltaPhi {
  public:
    static double reconstruct(const reco::Candidate& tau, const reco::MET& met);
    static double reconstruct(const reco::Candidate& tau, const pat::Jet& jet);
  };
}

#endif
