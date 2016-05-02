// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_PFcandidateGenerated_h
#define DataFormat_PFcandidateGenerated_h

#include "DataFormat/interface/Particle.h"

class PFcandidateGeneratedCollection: public ParticleCollection<double> {
public:
  explicit PFcandidateGeneratedCollection(const std::string& prefix="PFcandidates")
  : ParticleCollection(prefix)
  {

  }
  ~PFcandidateGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);



protected:

};


template <typename Coll>
class PFcandidateGenerated: public Particle<Coll> {
public:
  PFcandidateGenerated() {}
  PFcandidateGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~PFcandidateGenerated() {}





protected:

};

#endif
