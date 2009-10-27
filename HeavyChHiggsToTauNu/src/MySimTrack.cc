#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MySimTrack.h"

#include <iostream>

using namespace std;

MySimTrack::MySimTrack() {
  // Initialize values
  theGenPID = -1;
  theType = -1;
  theTrackID = -1;
  thePosition.SetXYZ(0,0,0);
}

MySimTrack::~MySimTrack() {

}

void MySimTrack::print() {
  cout << "- SimTrack: mom=(" << X()
       << ", " << Y()
       << ", " << Z()
       << ") prod=(" << thePosition.X()
       << ", " << thePosition.Y()
       << ", " << thePosition.Z() << ")" << endl;
  cout << "    genPID=" << theGenPID
       << " type=" << theType
       << " trackID=" << theTrackID
       << " ECAL hit=(" << trackEcalHitPoint.x
       << ", " << trackEcalHitPoint.y
       << ", " << trackEcalHitPoint.z << ")" << endl;
}
