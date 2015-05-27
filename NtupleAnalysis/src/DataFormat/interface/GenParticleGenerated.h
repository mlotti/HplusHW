// -*- c++ -*-
#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"

class GenParticleGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenParticleGeneratedCollection(const std::string& prefix="GenParticles"): 
      ParticleCollection(prefix),
      fMother(nullptr),
      fStatus(nullptr),
      fTauProng(nullptr),
      fGenIndex(nullptr),
      fTauSpinEffectsW(nullptr),
      fTauSpinEffectsHpm(nullptr),
      fAssociatedWithHpm(nullptr)
  {}
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:
  const Branch<std::vector<short>> *fMother;
  const Branch<std::vector<short>> *fStatus;
  const Branch<std::vector<short>> *fTauProng;
  const Branch<std::vector<short>> *fGenIndex;
  const Branch<std::vector<double>> *fTauSpinEffectsW;
  const Branch<std::vector<double>> *fTauSpinEffectsHpm;
  const Branch<std::vector<short>> *fAssociatedWithHpm;
};


template <typename Coll>
class GenParticleGenerated: public Particle<Coll> {
public:
  GenParticleGenerated() {}
  GenParticleGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~GenParticleGenerated() {}
};

#endif
