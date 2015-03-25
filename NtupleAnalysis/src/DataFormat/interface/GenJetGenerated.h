// -*- c++ -*-
#ifndef DataFormat_GenJetGenerated_h
#define DataFormat_GenJetGenerated_h

#include "DataFormat/interface/Particle.h"

class GenJetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenJetGeneratedCollection(const std::string& prefix="GenJets"): ParticleCollection(prefix) {}
  ~GenJetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:
  //const Branch<std::vector<float>> *fSecondaryVertex;
  //const Branch<std::vector<float>> *fTrackCountingHighEffBGenJetTags;
  //const Branch<std::vector<float>> *fTrackCountingHighPurBGenJetTags;
  const Branch<std::vector<short>> *fPdgId;
  //const Branch<std::vector<bool>> *fPUIDloose;
  //const Branch<std::vector<bool>> *fPUIDmedium;
  //const Branch<std::vector<bool>> *fPUIDtight;
};


template <typename Coll>
class GenJetGenerated: public Particle<Coll> {
public:
  GenJetGenerated() {}
  GenJetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~GenJetGenerated() {}

  //float secondaryVertex() const { return this->fCollection->fSecondaryVertex->value()[this->index()]; }
  //float trackCountingHighEffBGenJetTags() const { return this->fCollection->fTrackCountingHighEffBGenJetTags->value()[this->index()]; }
  //float trackCountingHighPurBGenJetTags() const { return this->fCollection->fTrackCountingHighPurBGenJetTags->value()[this->index()]; }
  short pdgId() const { return this->fCollection->fPdgId->value()[this->index()]; }
  //bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  //bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  //bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
};

#endif
