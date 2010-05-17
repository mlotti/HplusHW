// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_TrackDetectorAssociatorWrapper_h
#define HiggsAnalysis_MyEventNTPLMaker_TrackDetectorAssociatorWrapper_h

#include "TrackingTools/TrackAssociator/interface/TrackDetectorAssociator.h"

class TrackDetectorAssociatorWrapper {
public:
  TrackDetectorAssociatorWrapper(const edm::ParameterSet& iConfig);
  ~TrackDetectorAssociatorWrapper();

  void setEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  math::XYZPoint trackPositionAtEcal(const reco::Track& track);

private:
  const edm::Event *event;
  const edm::EventSetup *setup;
  TrackDetectorAssociator trackAssociator_;
  TrackAssociatorParameters trackAssociatorParameters_;
};

#endif
