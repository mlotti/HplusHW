#ifndef __MySimTrack__
#define __MySimTrack__

#include "TLorentzVector.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

#include<iostream>

/**
 * \brief Simulated track class for MyEvent dataformat
 */
class MySimTrack: public TLorentzVector {
 public:
  MySimTrack();
  ~MySimTrack();

  void print(std::ostream& out = std::cout);

  // Data members
  TVector3 thePosition;            ///< Production point of the track
  int theGenPID;                   ///< Generator particle id
  int theType;                     ///< Particle type (in case there is no gen particle)
  int theTrackID;                  ///< Track ID
  MyGlobalPoint trackEcalHitPoint; ///< Track ECAL impact point

 private:

  ClassDef(MySimTrack, MYEVENT_VERSION)
};



#endif
