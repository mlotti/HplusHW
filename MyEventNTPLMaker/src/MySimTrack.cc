#include "HiggsAnalysis/MyEventNTPLMaker/interface/MySimTrack.h"

using std::endl;

MySimTrack::MySimTrack():
  TLorentzVector(0,0,0,0),
  thePosition(0,0,0),
  theGenPID(-1),
  theType(-1),
  theTrackID(-1)
{}

MySimTrack::~MySimTrack() {

}

void MySimTrack::print(std::ostream& out) {
  out << "- SimTrack: mom=(" << X()
       << ", " << Y()
       << ", " << Z()
       << ") prod=(" << thePosition.X()
       << ", " << thePosition.Y()
       << ", " << thePosition.Z() << ")" << endl
       << "    genPID=" << theGenPID
       << " type=" << theType
       << " trackID=" << theTrackID
       << " ECAL hit=(" << trackEcalHitPoint.X()
       << ", " << trackEcalHitPoint.Y()
       << ", " << trackEcalHitPoint.Z() << ")" << endl;
}
