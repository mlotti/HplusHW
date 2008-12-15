#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"

ClassImp(MyMCParticle)

MyMCParticle::MyMCParticle(){}
MyMCParticle::MyMCParticle(double px,double py,double pz,double e){
        SetXYZT(px,py,pz,e);
}
MyMCParticle::~MyMCParticle(){}
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
