// -*- c++ -*-
#include "EventSelection/interface/TransverseMass.h"

#include <DataFormat/interface/Tau.h>
#include <DataFormat/interface/Muon.h>

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



double TransverseMass::reconstruct(const math::XYVector tauptvec_1, const math::XYVector tauptvec_2, const math::XYVector muonptvec, const math::XYVectorD& met) {
  //we use scalar sums to get the transverse mass
  double metEt = met.R();
  double tau1Et = tauptvec_1.r();
  double tau2Et = tauptvec_2.r();
  double muonEt = muonptvec.r();

  double myHWTransverseMass=-999;
  double myHWTransverseMassSquared = 0;

  myHWTransverseMassSquared = (metEt+tau1Et+tau2Et+muonEt)*(metEt+tau1Et+tau2Et+muonEt)-(tauptvec_1.x()+tauptvec_2.x()+muonptvec.x())*(tauptvec_1.x()+tauptvec_2.x()+muonptvec.x())-(tauptvec_1.y()+tauptvec_2.y()+muonptvec.y())*(tauptvec_1.y()+tauptvec_2.y()+muonptvec.y());
  if (myHWTransverseMassSquared >= 0)
    myHWTransverseMass = std::sqrt(myHWTransverseMassSquared);
  return myHWTransverseMass;
}
