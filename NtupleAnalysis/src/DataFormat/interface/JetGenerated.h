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
  explicit JetGeneratedCollection(const std::string& prefix="Jets")
  : ParticleCollection(prefix),
    fMCjet(prefix)
  {
    fMCjet.setEnergySystematicsVariation("_MCjet");
  }
  ~JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getBJetTagsDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("pfCombinedInclusiveSecondaryVertexBJetTags"), std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("pfCombinedSecondaryVertexBJetTags"), std::string("pfJetBProbabilityBJetTags"), std::string("pfJetProbabilityBJetTags")};
    return n;
  }
  std::vector<std::string> getPUIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("PUIDloose"), std::string("PUIDmedium"), std::string("PUIDtight")};
    return n;
  }
  std::vector<std::string> getJetIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("IDloose"), std::string("IDtight"), std::string("IDtightLeptonVeto")};
    return n;
  }

  const ParticleCollection<double>* getMCjetCollection() const { return &fMCjet; }
protected:
  ParticleCollection<double> fMCjet;

protected:
  const Branch<std::vector<bool>> *fIDloose;
  const Branch<std::vector<bool>> *fIDtight;
  const Branch<std::vector<bool>> *fIDtightLeptonVeto;
  const Branch<std::vector<bool>> *fPUIDloose;
  const Branch<std::vector<bool>> *fPUIDmedium;
  const Branch<std::vector<bool>> *fPUIDtight;
  const Branch<std::vector<double>> *fPileupJetIdfullDiscriminant;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexBJetTags;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fPfCombinedMVABJetTag;
  const Branch<std::vector<float>> *fPfCombinedSecondaryVertexBJetTags;
  const Branch<std::vector<float>> *fPfJetBProbabilityBJetTags;
  const Branch<std::vector<float>> *fPfJetProbabilityBJetTags;
  const Branch<std::vector<int>> *fHadronFlavour;
  const Branch<std::vector<int>> *fPartonFlavour;
};


template <typename Coll>
class JetGenerated: public Particle<Coll> {
public:
  JetGenerated() {}
  JetGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCjet(coll->getMCjetCollection(), index)
  {}
  ~JetGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->pfCombinedInclusiveSecondaryVertexBJetTags(); },
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfCombinedSecondaryVertexBJetTags(); },
      [&](){ return this->pfJetBProbabilityBJetTags(); },
      [&](){ return this->pfJetProbabilityBJetTags(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getPUIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->PUIDloose(); },
      [&](){ return this->PUIDmedium(); },
      [&](){ return this->PUIDtight(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getJetIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->IDloose(); },
      [&](){ return this->IDtight(); },
      [&](){ return this->IDtightLeptonVeto(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCjet() const { return &fMCjet; }

  bool IDloose() const { return this->fCollection->fIDloose->value()[this->index()]; }
  bool IDtight() const { return this->fCollection->fIDtight->value()[this->index()]; }
  bool IDtightLeptonVeto() const { return this->fCollection->fIDtightLeptonVeto->value()[this->index()]; }
  bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
  double pileupJetIdfullDiscriminant() const { return this->fCollection->fPileupJetIdfullDiscriminant->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexBJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexBJetTags->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedMVABJetTag() const { return this->fCollection->fPfCombinedMVABJetTag->value()[this->index()]; }
  float pfCombinedSecondaryVertexBJetTags() const { return this->fCollection->fPfCombinedSecondaryVertexBJetTags->value()[this->index()]; }
  float pfJetBProbabilityBJetTags() const { return this->fCollection->fPfJetBProbabilityBJetTags->value()[this->index()]; }
  float pfJetProbabilityBJetTags() const { return this->fCollection->fPfJetProbabilityBJetTags->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCjet;

};

#endif
