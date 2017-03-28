// -*- c++ -*-
#ifndef EventSelection_TransverseMass_h
#define EventSelection_TransverseMass_h

#include <DataFormat/interface/Particle.h>

class Tau;

/** 
 * Class for calculating the transverse mass from tau and MET in the event
 */
class TransverseMass {
public:
  /// Obtain the transverse mass
  static double reconstruct(const Tau& tau, const math::XYVectorD& met);
  static double reconstruct(const math::XYVector tauptvec, const math::XYVectorD& met);
};
#endif
