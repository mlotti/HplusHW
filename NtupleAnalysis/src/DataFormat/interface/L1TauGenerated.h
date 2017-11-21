// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_L1TauGenerated_h
#define DataFormat_L1TauGenerated_h

#include "DataFormat/interface/Particle.h"

class L1TauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit L1TauGeneratedCollection(const std::string& prefix="L1Taus")
  : ParticleCollection(prefix)
  {

  }
  ~L1TauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class L1TauGenerated: public Particle<Coll> {
public:
  L1TauGenerated() {}
  L1TauGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~L1TauGenerated() {}





protected:

};

#endif
