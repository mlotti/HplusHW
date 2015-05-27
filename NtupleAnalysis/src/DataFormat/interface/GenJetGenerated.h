// -*- c++ -*-
#ifndef DataFormat_GenJetGenerated_h
#define DataFormat_GenJetGenerated_h

#include "DataFormat/interface/Particle.h"

class GenJetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenJetGeneratedCollection(const std::string& prefix="GenJets"): ParticleCollection(prefix) {}
  ~GenJetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);
};


template <typename Coll>
class GenJetGenerated: public Particle<Coll> {
public:
  GenJetGenerated() {}
  GenJetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~GenJetGenerated() {}

};

#endif
