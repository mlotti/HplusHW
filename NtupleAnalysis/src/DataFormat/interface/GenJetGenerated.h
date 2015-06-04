// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenJetGenerated_h
#define DataFormat_GenJetGenerated_h

#include "DataFormat/interface/Particle.h"

class GenJetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenJetGeneratedCollection(const std::string& prefix="GenJets"): ParticleCollection(prefix) {}
  ~GenJetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:

};


template <typename Coll>
class GenJetGenerated: public Particle<Coll> {
public:
  GenJetGenerated() {}
  GenJetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~GenJetGenerated() {}




};

#endif
