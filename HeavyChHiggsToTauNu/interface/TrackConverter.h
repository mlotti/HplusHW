// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TrackConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TrackConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace reco {
  class TransientTrack;
  class PFCandidate;
}
namespace edm {
  class Event;
  class InputTag;
}
class Trajectory;
class MyJet;

class TrackConverter {
public:
  TrackConverter(const edm::Event&, const edm::InputTag&);
  ~TrackConverter();

  void addTracksInCone(MyJet&, double cone=0.5) const;
  std::vector<reco::Track> getTracksInCone(const math::XYZTLorentzVector& direction, double cone) const;
  std::vector<reco::Track> getTracksInCone(const math::XYZTLorentzVector& direction, double cone, const std::vector<Trajectory>&) const;

  static MyTrack convert(const reco::TransientTrack&);
  static MyTrack convert(const reco::Track&);
  static MyTrack convert(const reco::PFCandidate&);
private:
  const reco::TrackCollection& tracks;
};

#endif
