// -*- c++ -*-
#ifndef DataFormat_JetGenerated_h
#define DataFormat_JetGenerated_h

#include "DataFormat/interface/Particle.h"

class JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit JetGeneratedCollection(const std::string& prefix="Jets"): ParticleCollection(prefix) {}
  ~JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:
  Branch<std::vector<float>> *fSecondaryVertex;
  Branch<std::vector<float>> *fTrackCountingHighEffBJetTags;
  Branch<std::vector<float>> *fTrackCountingHighPurBJetTags;
  Branch<std::vector<short>> *fPdgId;
  Branch<std::vector<bool>> *fPUIDloose;
  Branch<std::vector<bool>> *fPUIDmedium;
  Branch<std::vector<bool>> *fPUIDtight;
};


template <typename Coll>
class JetGenerated: public Particle<Coll> {
public:
  JetGenerated() {}
  JetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~JetGenerated() {}

  float secondaryVertex() const { return this->fCollection->fSecondaryVertex->value()[this->index()]; }
  float trackCountingHighEffBJetTags() const { return this->fCollection->fTrackCountingHighEffBJetTags->value()[this->index()]; }
  float trackCountingHighPurBJetTags() const { return this->fCollection->fTrackCountingHighPurBJetTags->value()[this->index()]; }
  short pdgId() const { return this->fCollection->fPdgId->value()[this->index()]; }
  bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
};

#endif
