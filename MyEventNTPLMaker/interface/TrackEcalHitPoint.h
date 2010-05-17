// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_TrackEcalHitPoint_h
#define HiggsAnalysis_MyEventNTPLMaker_TrackEcalHitPoint_h

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/TrackDetectorAssociatorWrapper.h"

// Forward declarations
namespace edm { 
  class ParameterSet;
  class Event;
  class EventSetup;
}
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
  TrackEcalHitPoint(const edm::ParameterSet& iConfig);
  ~TrackEcalHitPoint();

  void setEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();
  
  MyGlobalPoint convert(const reco::TransientTrack&, const reco::CaloJet &);

  static MyGlobalPoint convert(const reco::TransientTrack&, const reco::Conversion &);
  static MyGlobalPoint convert(const reco::GsfElectron &);
  static MyGlobalPoint convert(const pat::Electron &);
  static MyGlobalPoint convert(const reco::PFCandidate &);

private:
  TrackDetectorAssociatorWrapper trackAssociator_;
};

#endif
