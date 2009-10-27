#ifndef MYSIMTRACK_H
#define MYSIMTRACK_H

#include "TROOT.h"
#include "TLorentzVector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

class MySimTrack : public TLorentzVector {
 public:
  MySimTrack();
  ~MySimTrack();

  void print();

  // Data members
  TVector3 thePosition;
  int theGenPID; // Generator particle
  int theType; // Particle type (in case there is no gen particle)
  int theTrackID; // Track ID
  MyGlobalPoint trackEcalHitPoint; // for simtrack // LAW 11.02.08

 private:

  ClassDef(MySimTrack,1)
};



#endif
