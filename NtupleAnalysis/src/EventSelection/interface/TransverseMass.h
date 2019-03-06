// -*- c++ -*-
#ifndef EventSelection_TransverseMass_h
#define EventSelection_TransverseMass_h

#include <DataFormat/interface/Particle.h>

class Tau;
class Muon;
//class genParticle;

/** 
 * Class for calculating the transverse mass from tau and MET in the event
 */
/**
 *Added possibility of calculating transverse mas for HW decay
 */
class TransverseMass {
public:
  /// Obtain the transverse mass
  static double reconstruct(const Tau& tau, const math::XYVectorD& met);
  static double reconstruct(const math::XYVector tauptvec, const math::XYVectorD& met);

  static double reconstruct(const Tau& tau_1,const Tau& tau_2,const Muon& muon, const math::XYVectorD& met);
  static double reconstruct(const math::XYVector tauptvec_1, const math::XYVector tauptvec_2, const math::XYVector muonptvec, const math::XYVectorD& met);

  static double reconstruct(const Muon& muon_1,const Muon& muon_2,const Muon& muon_3,const Muon& muon_4,const Muon& muon_5, const math::XYVectorD& met);
  static double reconstruct(const math::XYVector muonptvec_1, const math::XYVector muonptvec_2, const math::XYVector muonptvec_3, const math::XYVector muonptvec_4, const math::XYVector muonptvec_5, const math::XYVectorD& met);

//  static double reconstruct(const genParticle& gamma_1,const genParticle& gamma_2,const Muon& muon, const math::XYVectorD& met);

};
#endif
