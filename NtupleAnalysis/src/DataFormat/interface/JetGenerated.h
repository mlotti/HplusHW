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
};


template <typename Coll>
class JetGenerated: public Particle<Coll> {
public:
  JetGenerated() {}
  JetGenerated(Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~JetGenerated() {}

  float secondaryVertex() { return this->fCollection->fSecondaryVertex->value()[this->index()]; }
  float trackCountingHighEffBJetTags() { return this->fCollection->fTrackCountingHighEffBJetTags->value()[this->index()]; }
  float trackCountingHighPurBJetTags() { return this->fCollection->fTrackCountingHighPurBJetTags->value()[this->index()]; }
  short pdgId() { return this->fCollection->fPdgId->value()[this->index()]; }
};

#endif
