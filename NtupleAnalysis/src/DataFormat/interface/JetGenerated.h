// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_JetGenerated_h
#define DataFormat_JetGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit JetGeneratedCollection(const std::string& prefix="Jets"): ParticleCollection(prefix) {}
  ~JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getBJetTagsDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("combinedInclusiveSecondaryVertexBJetTags"), std::string("combinedInclusiveSecondaryVertexV2BJetTags"), std::string("combinedSecondaryVertexBJetTags"), std::string("jetBProbabilityBJetTags"), std::string("jetProbabilityBJetTags"), std::string("simpleSecondaryVertexHighEffBJetTags"), std::string("simpleSecondaryVertexHighPurBJetTags"), std::string("trackCountingHighEffBJetTags"), std::string("trackCountingHighPurBJetTags")};
    return n;
  }
  std::vector<std::string> getPUIDDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("PUIDloose"), std::string("PUIDmedium"), std::string("PUIDtight")};
    return n;
  }

protected:
  const Branch<std::vector<bool>> *fPUIDloose;
  const Branch<std::vector<bool>> *fPUIDmedium;
  const Branch<std::vector<bool>> *fPUIDtight;
  const Branch<std::vector<double>> *fPileupJetIdfullDiscriminant;
  const Branch<std::vector<float>> *fCombinedInclusiveSecondaryVertexBJetTags;
  const Branch<std::vector<float>> *fCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fCombinedSecondaryVertexBJetTags;
  const Branch<std::vector<float>> *fJetBProbabilityBJetTags;
  const Branch<std::vector<float>> *fJetProbabilityBJetTags;
  const Branch<std::vector<float>> *fSimpleSecondaryVertexHighEffBJetTags;
  const Branch<std::vector<float>> *fSimpleSecondaryVertexHighPurBJetTags;
  const Branch<std::vector<float>> *fTrackCountingHighEffBJetTags;
  const Branch<std::vector<float>> *fTrackCountingHighPurBJetTags;
};


template <typename Coll>
class JetGenerated: public Particle<Coll> {
public:
  JetGenerated() {}
  JetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~JetGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->combinedInclusiveSecondaryVertexBJetTags(); },
      [&](){ return this->combinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->combinedSecondaryVertexBJetTags(); },
      [&](){ return this->jetBProbabilityBJetTags(); },
      [&](){ return this->jetProbabilityBJetTags(); },
      [&](){ return this->simpleSecondaryVertexHighEffBJetTags(); },
      [&](){ return this->simpleSecondaryVertexHighPurBJetTags(); },
      [&](){ return this->trackCountingHighEffBJetTags(); },
      [&](){ return this->trackCountingHighPurBJetTags(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getPUIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->PUIDloose(); },
      [&](){ return this->PUIDmedium(); },
      [&](){ return this->PUIDtight(); }
    };
    return values;
  }

  bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
  double pileupJetIdfullDiscriminant() const { return this->fCollection->fPileupJetIdfullDiscriminant->value()[this->index()]; }
  float combinedInclusiveSecondaryVertexBJetTags() const { return this->fCollection->fCombinedInclusiveSecondaryVertexBJetTags->value()[this->index()]; }
  float combinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float combinedSecondaryVertexBJetTags() const { return this->fCollection->fCombinedSecondaryVertexBJetTags->value()[this->index()]; }
  float jetBProbabilityBJetTags() const { return this->fCollection->fJetBProbabilityBJetTags->value()[this->index()]; }
  float jetProbabilityBJetTags() const { return this->fCollection->fJetProbabilityBJetTags->value()[this->index()]; }
  float simpleSecondaryVertexHighEffBJetTags() const { return this->fCollection->fSimpleSecondaryVertexHighEffBJetTags->value()[this->index()]; }
  float simpleSecondaryVertexHighPurBJetTags() const { return this->fCollection->fSimpleSecondaryVertexHighPurBJetTags->value()[this->index()]; }
  float trackCountingHighEffBJetTags() const { return this->fCollection->fTrackCountingHighEffBJetTags->value()[this->index()]; }
  float trackCountingHighPurBJetTags() const { return this->fCollection->fTrackCountingHighPurBJetTags->value()[this->index()]; }

};

#endif
