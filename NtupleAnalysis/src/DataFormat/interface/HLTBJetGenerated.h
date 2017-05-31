// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_HLTBJetGenerated_h
#define DataFormat_HLTBJetGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTBJetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTBJetGeneratedCollection(const std::string& prefix="HLTBJet"): ParticleCollection(prefix) {}
  ~HLTBJetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);


protected:

};


template <typename Coll>
class HLTBJetGenerated: public Particle<Coll> {
public:
  HLTBJetGenerated() {}
  HLTBJetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~HLTBJetGenerated() {}




};

#endif
