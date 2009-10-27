#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"

#include <iostream>
using namespace std;

ClassImp(MyTrack)

MyTrack::MyTrack(){}

MyTrack::MyTrack(double px,double py,double pz,double e){
	SetXYZT(px,py,pz,e);
}
MyTrack::MyTrack(const MyTrack& track) {
	SetXYZT(track.Px(),track.Py(),track.Pz(),track.E());
	trackCharge 		= track.trackCharge;
	chiSquared		= track.chiSquared;
	nHits			= track.nHits;
	nPixHits		= track.nPixHits;
	particleType		= track.particleType;
	ip			= track.ip;
	trackEcalHitPoint 	= track.trackEcalHitPoint;
//	hits			= track.hits;
}


MyTrack::~MyTrack(){;}

double MyTrack::pt()  const { return Pt(); }
double MyTrack::eta() const { return Eta(); }
double MyTrack::phi() const { return Phi(); }

double MyTrack::px()  const { return Px(); }
double MyTrack::py()  const { return Py(); }
double MyTrack::pz()  const { return Pz(); }
double MyTrack::p()  const { return P(); }

TLorentzVector MyTrack::p4() const {
        return TLorentzVector(this->Px(),this->Py(),this->Pz(),this->E());
}

void MyTrack::setP4(TLorentzVector& vector){
	SetXYZT(vector.Px(),vector.Py(),vector.Pz(),vector.E());
}


double MyTrack::charge() const { return trackCharge; }
double MyTrack::normalizedChi2() const { return chiSquared; }
double MyTrack::numberOfValidHits() const { return nHits; }
double MyTrack::pfType() const { return particleType; }

MyImpactParameter MyTrack::impactParameter() const { return ip; }

MyGlobalPoint MyTrack::ecalHitPoint() const { return trackEcalHitPoint; }

void MyTrack::print() const {
	cout << "        pt,eta,phi " << this->Pt() << " " << this->Eta() << " " << this->Phi() << endl; 
}
