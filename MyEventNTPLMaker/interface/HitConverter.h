// -*- C++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_HitConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_HitConverter_h

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyHit.h"

#include<vector>

class TransientTrackingRecHit;
class Trajectory;

class HitConverter {
public:
  static MyHit convert(const TransientTrackingRecHit* recHit, float estimate);
  static void addHits(std::vector<MyHit>& hits, const Trajectory& trajectory, int trackLabel);
};

#endif
