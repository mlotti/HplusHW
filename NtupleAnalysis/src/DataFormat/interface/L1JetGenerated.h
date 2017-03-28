// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_L1JetGenerated_h
#define DataFormat_L1JetGenerated_h

#include "DataFormat/interface/Particle.h"

class L1JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit L1JetGeneratedCollection(const std::string& prefix="L1Jet")
  : ParticleCollection(prefix)
  {

  }
  ~L1JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class L1JetGenerated: public Particle<Coll> {
public:
  L1JetGenerated() {}
  L1JetGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~L1JetGenerated() {}





protected:

};

#endif
