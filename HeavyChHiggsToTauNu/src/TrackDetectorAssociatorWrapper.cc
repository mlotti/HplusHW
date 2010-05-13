#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackDetectorAssociatorWrapper.h"

TrackDetectorAssociatorWrapper::TrackDetectorAssociatorWrapper(const edm::ParameterSet& iConfig):
  event(0), setup(0) {
  trackAssociatorParameters_.loadParameters(iConfig.getParameter<edm::ParameterSet>("TrackAssociatorParameters"));
  trackAssociator_.useDefaultPropagator();
}

TrackDetectorAssociatorWrapper::~TrackDetectorAssociatorWrapper() {}

void TrackDetectorAssociatorWrapper::setEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if(event || setup) {
    throw cms::Exception("LogicError") << "TrackDetectorAssociatorWrapper has already been initialized for this event! The object should be reset after event processing." << std::endl;
  }
  event = &iEvent;
  setup = &iSetup;
}

void TrackDetectorAssociatorWrapper::reset() {
  event = 0;
  setup = 0;
}

math::XYZPoint TrackDetectorAssociatorWrapper::trackPositionAtEcal(const reco::Track& track) {
  if(!event || !setup) {
    throw cms::Exception("LogicError") << "TrackDetectorAssociatorWrapper object must be initialized for current event with setEvent()" << std::endl;
  }

  const FreeTrajectoryState fts = trackAssociator_.getFreeTrajectoryState(*setup, track);
  TrackDetMatchInfo info = trackAssociator_.associate(*event, *setup, fts, trackAssociatorParameters_);
  if(info.isGoodEcal) {
    return info.trkGlobPosAtEcal;
  }
  else {
    return math::XYZPoint(0,0,0);
  }
}
