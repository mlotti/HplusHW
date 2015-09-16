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
  const Branch<std::vector<float>> *fIPTSignificance;
  const Branch<std::vector<float>> *fIPTwrtPV;
  const Branch<std::vector<float>> *fIPzSignificance;
  const Branch<std::vector<float>> *fIPzwrtPV;
};


template <typename Coll>
class PFcandidateGenerated: public Particle<Coll> {
public:
  PFcandidateGenerated() {}
  PFcandidateGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index)
  {}
  ~PFcandidateGenerated() {}



  float IPTSignificance() const { return this->fCollection->fIPTSignificance->value()[this->index()]; }
  float IPTwrtPV() const { return this->fCollection->fIPTwrtPV->value()[this->index()]; }
  float IPzSignificance() const { return this->fCollection->fIPzSignificance->value()[this->index()]; }
  float IPzwrtPV() const { return this->fCollection->fIPzwrtPV->value()[this->index()]; }

protected:

};

#endif
