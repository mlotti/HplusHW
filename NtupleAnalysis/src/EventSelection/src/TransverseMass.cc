// -*- c++ -*-
#include "EventSelection/interface/TransverseMass.h"

#include <DataFormat/interface/Tau.h>

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
