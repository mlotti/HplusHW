#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"

ClassImp(MyMCParticle)

MyMCParticle::MyMCParticle(): TLorentzVector(0,0,0,0) {}
MyMCParticle::MyMCParticle(double px, double py, double pz, double E): TLorentzVector(px, py, pz, E) {}
MyMCParticle::~MyMCParticle(){}

double MyMCParticle::pt()  const { return Pt(); }
double MyMCParticle::eta() const { return Eta(); }
double MyMCParticle::phi() const { return Phi(); }

double MyMCParticle::px()  const { return Px(); }
double MyMCParticle::py()  const { return Py(); }
double MyMCParticle::pz()  const { return Pz(); }
double MyMCParticle::p()  const { return P(); }

TLorentzVector MyMCParticle::p4() const {
        return TLorentzVector(Px(), Py(), Pz(), E());
}

void MyMCParticle::setP4(const TLorentzVector& vector) {
	SetXYZT(vector.Px(), vector.Py(), vector.Pz(), vector.E());
}

int MyMCParticle::charge() const { return pCharge; }
MyImpactParameter MyMCParticle::impactParameter() const { return ip; }

/*
MyGlobalPoint MyMCParticle::GetMCVertex() const { return impactParameter; }

MyGlobalPoint MyMCParticle::GetImpactParameter() const {

    // transfering MC vertex (saved as MyGlobalPoint impactParameter) to ip
    MyGlobalPoint ip;

    ip.x = 0;
    ip.y = 0;
    ip.z = impactParameter.GetZ();

    ip.dxx = 0;
    ip.dxy = 0;
    ip.dxz = 0;
    ip.dyy = 0;
    ip.dyz = 0;
    ip.dzz = 0;

    if(Pt() > 0){
      // ip(vec) = vertex(vec) - [vertex(vec)-dotproduct-p(unitvec)]p(unitvec)
      double unit_px = Px()/Pt();
      double unit_py = Py()/Pt();
      double vertex_x = impactParameter.GetX();
      double vertex_y = impactParameter.GetY();

      ip.x = vertex_x - vertex_x*unit_px*unit_px - vertex_y*unit_px*unit_py;
      ip.y = vertex_y - vertex_x*unit_px*unit_py - vertex_y*unit_py*unit_py;
    }
    return ip;
}
*/
