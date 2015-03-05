// -*- c++ -*-
#ifndef DataFormat_JetGenerated_h
#define DataFormat_JetGenerated_h

#include "DataFormat/interface/Particle.h"

class JetGenerated;

class JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit JetGeneratedCollection(const std::string& prefix="Jets"): ParticleCollection(prefix) {}
  ~JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  JetGenerated operator[](size_t i);

  friend class JetGenerated;
  friend class Particle<JetGeneratedCollection>;

protected:
  Branch<std::vector<float>> *fSecondaryVertex;
  Branch<std::vector<float>> *fTrackCountingHighEffBJetTags;
  Branch<std::vector<float>> *fTrackCountingHighPurBJetTags;
  Branch<std::vector<short>> *fPdgId;
  Branch<std::vector<bool>> *fPUIDloose;
  Branch<std::vector<bool>> *fPUIDmedium;
  Branch<std::vector<bool>> *fPUIDtight;
};


class JetGenerated: public Particle<JetGeneratedCollection> {
public:
  JetGenerated() {}
  JetGenerated(JetGeneratedCollection* coll, size_t index): Particle<JetGeneratedCollection>(coll, index) {}
  ~JetGenerated() {}

  float secondaryVertex() { return fCollection->fSecondaryVertex->value()[index()]; }
  float trackCountingHighEffBJetTags() { return fCollection->fTrackCountingHighEffBJetTags->value()[index()]; }
  float trackCountingHighPurBJetTags() { return fCollection->fTrackCountingHighPurBJetTags->value()[index()]; }
  short pdgId() { return fCollection->fPdgId->value()[index()]; }
  bool PUIDloose() { return fCollection->fPUIDloose->value()[index()]; }
  bool PUIDmedium() { return fCollection->fPUIDmedium->value()[index()]; }
  bool PUIDtight() { return fCollection->fPUIDtight->value()[index()]; }
};

inline
JetGenerated JetGeneratedCollection::operator[](size_t i) {
  return JetGenerated(this, i);
}

#endif
