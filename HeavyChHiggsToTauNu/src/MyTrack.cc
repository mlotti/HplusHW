#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"

#include <iostream>

//ClassImp(MyTrack)

MyTrack::MyTrack(){}

MyTrack::MyTrack(double px,double py,double pz,double e){
	SetXYZT(px,py,pz,e);
}


MyTrack::~MyTrack(){}

double MyTrack::pt()  const { return Pt(); }
double MyTrack::eta() const { return Eta(); }
double MyTrack::phi() const { return Phi(); }

double MyTrack::px()  const { return Px(); }
double MyTrack::py()  const { return Py(); }
double MyTrack::pz()  const { return Pz(); }
double MyTrack::p()  const { return P(); }

TLorentzVector MyTrack::p4() const {
        return TLorentzVector(Px(), Py(), Pz(), E());
}

void MyTrack::setP4(const TLorentzVector& vector){
	SetXYZT(vector.Px(), vector.Py(), vector.Pz(), vector.E());
}


double MyTrack::charge() const { return trackCharge; }
double MyTrack::normalizedChi2() const { return normChiSquared; }
unsigned int MyTrack::numberOfValidHits() const { return nHits; }
int MyTrack::pfType() const { return particleType; }

MyImpactParameter MyTrack::impactParameter() const { return ip; }

MyGlobalPoint MyTrack::ecalHitPoint() const { return trackEcalHitPoint; }

void MyTrack::print(std::ostream& out) const {
        out << "        " << *this << std::endl;
}

std::ostream& operator<<(std::ostream& out, const MyTrack& track) {
        out << "pt,eta,phi" << track.Pt() << " " << track.Eta() << " " << track.Phi();
        return out;
}
