// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_PFCandsGenerated_h
#define DataFormat_PFCandsGenerated_h

#include "DataFormat/interface/Particle.h"

class PFCandsGeneratedCollection: public ParticleCollection<double> {
public:
  explicit PFCandsGeneratedCollection(const std::string& prefix="PFCandss"): ParticleCollection(prefix) {}
  ~PFCandsGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);


protected:

};


template <typename Coll>
class PFCandsGenerated: public Particle<Coll> {
public:
  PFCandsGenerated() {}
  PFCandsGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~PFCandsGenerated() {}




};

#endif
