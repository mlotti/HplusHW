// -*- c++ -*-
#include "EventSelection/interface/TransverseMass.h"

#include <DataFormat/interface/Tau.h>
#include <DataFormat/interface/Muon.h>
//#include <DataFormat/interface/GenParticle.h>

#include <cmath>

double TransverseMass::reconstruct(const Tau& tau, const math::XYVectorD& met) {
  math::XYVector tauptvec = tau.p2();
  return TransverseMass::reconstruct(tauptvec,met);
}


double TransverseMass::reconstruct(const math::XYVector tauptvec, const math::XYVectorD& met) {
  // Calculate cosine of angle between jet and met direction
  //  math::XYVector tauptvec = tau.p2();
  double metEt = met.R();
  double myCosPhi = 100;
  if (metEt > 0.0 && tauptvec.r() > 0.0)
    myCosPhi = (tauptvec.x()*met.x() + tauptvec.y()*met.y()) / (tauptvec.r()*metEt);
  // Calculate transverse mass
  double myTransverseMass = -999;
  double myTransverseMassSquared = 0;
  if (myCosPhi < 10)
    myTransverseMassSquared = 2 * tauptvec.r() * metEt * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    myTransverseMass = std::sqrt(myTransverseMassSquared);
  return myTransverseMass;
}


double TransverseMass::reconstruct(const Tau& tau_1,const Tau& tau_2,const Muon& muon, const math::XYVectorD& met) {
  math::XYVector tauptvec_1 = tau_1.p2();
  math::XYVector tauptvec_2 = tau_2.p2();
  math::XYVector muonptvec = muon.p2();

  return TransverseMass::reconstruct(tauptvec_1,tauptvec_2,muonptvec,met);
}


//double TransverseMass::reconstruct(const genParticle& gamma_1,const genParticle& gamma_2,const Muon& muon, const math::XYVectorD& met) {
//  math::XYVector gammaptvec_1 = gamma_1.p2();
//  math::XYVector gammaptvec_2 = gamma_2.p2();
//  math::XYVector muonptvec = muon.p2();

//  return TransverseMass::reconstruct(gammaptvec_1,gammaptvec_2,muonptvec,met);
//}


double TransverseMass::reconstruct(const math::XYVector tauptvec_1, const math::XYVector tauptvec_2, const math::XYVector muonptvec, const math::XYVectorD& met) {
  //we use scalar sums to get the transverse mass
  double metEt = met.R();
  double tau1Et = tauptvec_1.r();
  double tau2Et = tauptvec_2.r();
  double muonEt = muonptvec.r();

  double myHWTransverseMass=-999;
  double myHWTransverseMassSquared = 0;

  myHWTransverseMassSquared = (metEt+tau1Et+tau2Et+muonEt)*(metEt+tau1Et+tau2Et+muonEt)-(tauptvec_1.x()+tauptvec_2.x()+muonptvec.x()+met.x())*(tauptvec_1.x()+tauptvec_2.x()+muonptvec.x()+met.x())-(tauptvec_1.y()+tauptvec_2.y()+muonptvec.y()+met.y())*(tauptvec_1.y()+tauptvec_2.y()+muonptvec.y()+met.y());
  if (myHWTransverseMassSquared >= 0)
    myHWTransverseMass = std::sqrt(myHWTransverseMassSquared);
  return myHWTransverseMass;
}


double TransverseMass::reconstruct(const Muon& muon_1,const Muon& muon_2,const Muon& muon_3,const Muon& muon_4,const Muon& muon_5, const math::XYVectorD& met) {
  math::XYVector muonptvec_1 = muon_1.p2();
  math::XYVector muonptvec_2 = muon_2.p2();
  math::XYVector muonptvec_3 = muon_3.p2();
  math::XYVector muonptvec_4 = muon_4.p2();
  math::XYVector muonptvec_5 = muon_5.p2();

  return TransverseMass::reconstruct(muonptvec_1,muonptvec_2,muonptvec_3,muonptvec_4,muonptvec_5,met);
}



double TransverseMass::reconstruct(const math::XYVector muonptvec_1, const math::XYVector muonptvec_2, const math::XYVector muonptvec_3,const math::XYVector muonptvec_4, const math::XYVector muonptvec_5, const math::XYVectorD& met) {
  //we use scalar sums to get the transverse mass
  double metEt = met.R();
  double muon1Et = muonptvec_1.r();
  double muon2Et = muonptvec_2.r();
  double muon3Et = muonptvec_3.r();
  double muon4Et = muonptvec_4.r();
  double muon5Et = muonptvec_5.r();

  double myHWTransverseMass=-999;
  double myHWTransverseMassSquared = 0;

  double Esum = metEt+muon1Et+muon2Et+muon3Et + muon4Et + muon5Et;
  double xsum = muonptvec_1.x()+muonptvec_2.x()+muonptvec_3.x()+muonptvec_4.x()+muonptvec_5.x()+met.x();
  double ysum = muonptvec_1.y()+muonptvec_2.y()+muonptvec_3.y()+muonptvec_4.y()+muonptvec_5.y()+met.y();

  myHWTransverseMassSquared = (Esum*Esum)-(xsum*xsum)-(ysum*ysum);
  if (myHWTransverseMassSquared >= 0)
    myHWTransverseMass = std::sqrt(myHWTransverseMassSquared);
  return myHWTransverseMass;
}
