// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TrackConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TrackConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"

namespace reco {
  class Track;
  class TransientTrack;
  class PFCandidate;
}

class TrackConverter {
public:
  static MyTrack convert(const reco::TransientTrack&);
  static MyTrack convert(const reco::Track&);
  static MyTrack convert(const reco::PFCandidate&);
};

#endif
