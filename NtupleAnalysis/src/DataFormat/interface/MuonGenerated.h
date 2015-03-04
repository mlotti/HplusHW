// -*- c++ -*-
#ifndef DataFormat_MuonGenerated_h
#define DataFormat_MuonGenerated_h

#include "DataFormat/interface/Particle.h"

class MuonGenerated;

class MuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonGeneratedCollection(const std::string& prefix="Muons"): ParticleCollection(prefix) {}
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  MuonGenerated operator[](size_t i);

  friend class MuonGenerated;
  friend class Particle<MuonGeneratedCollection>;

protected:
  Branch<std::vector<bool>> *fIsGlobalMuon;
};


class MuonGenerated: public Particle<MuonGeneratedCollection> {
public:
  MuonGenerated() {}
  MuonGenerated(MuonGeneratedCollection* coll, size_t index): Particle<MuonGeneratedCollection>(coll, index) {}
  ~MuonGenerated() {}

  bool isGlobalMuon() { return fCollection->fIsGlobalMuon->value()[index()]; }

};

inline
MuonGenerated MuonGeneratedCollection::operator[](size_t i) {
  return MuonGenerated(this, i);
}

#endif
