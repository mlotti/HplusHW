// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTTauGenerated_h
#define DataFormat_HLTTauGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTTauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTTauGeneratedCollection(const std::string& prefix="HLTTaus"): ParticleCollection(prefix) {}
  ~HLTTauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);


protected:

};


template <typename Coll>
class HLTTauGenerated: public Particle<Coll> {
public:
  HLTTauGenerated() {}
  HLTTauGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~HLTTauGenerated() {}




};

#endif
