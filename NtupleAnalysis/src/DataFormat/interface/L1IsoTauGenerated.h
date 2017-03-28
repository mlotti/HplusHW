// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_L1IsoTauGenerated_h
#define DataFormat_L1IsoTauGenerated_h

#include "DataFormat/interface/Particle.h"

class L1IsoTauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit L1IsoTauGeneratedCollection(const std::string& prefix="L1IsoTau")
  : ParticleCollection(prefix)
  {

  }
  ~L1IsoTauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class L1IsoTauGenerated: public Particle<Coll> {
public:
  L1IsoTauGenerated() {}
  L1IsoTauGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~L1IsoTauGenerated() {}





protected:

};

#endif
