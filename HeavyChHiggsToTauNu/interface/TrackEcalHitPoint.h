// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TrackEcalHitPoint_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TrackEcalHitPoint_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

// Forward declarations
namespace pat { class Electron; }
namespace reco { 
  class TransientTrack;
  class CaloJet;
  class Conversion;
  class GsfElectron;
  class PFCandidate; 
}

class TrackEcalHitPoint {
public:
  static MyGlobalPoint convert(const reco::TransientTrack&, const reco::CaloJet *);
  static MyGlobalPoint convert(const reco::TransientTrack&, const reco::Conversion *);
  static MyGlobalPoint convert(const reco::TransientTrack&, const reco::GsfElectron *);
  static MyGlobalPoint convert(const reco::TransientTrack&, const pat::Electron *);
  static MyGlobalPoint convert(const reco::PFCandidate *);
};

#endif
