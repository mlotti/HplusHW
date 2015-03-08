// -*- c++ -*-
#ifndef DataFormat_MuonGenerated_h
#define DataFormat_MuonGenerated_h

#include "DataFormat/interface/Particle.h"

class MuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonGeneratedCollection(const std::string& prefix="Muons"): ParticleCollection(prefix) {}
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:
  const Branch<std::vector<bool>> *fIsGlobalMuon;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~MuonGenerated() {}

  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }

};

#endif
