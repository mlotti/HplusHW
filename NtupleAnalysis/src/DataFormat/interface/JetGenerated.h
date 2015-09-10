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
    static std::vector<std::string> n = { std::string("pfCombinedInclusiveSecondaryVertexBJetTags"), std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("pfCombinedSecondaryVertexBJetTags"), std::string("pfJetBProbabilityBJetTags"), std::string("pfJetProbabilityBJetTags")};
    return n;
  }
  std::vector<std::string> getPUIDDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("PUIDloose"), std::string("PUIDmedium"), std::string("PUIDtight")};
    return n;
  }
  std::vector<std::string> getJetIDDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("")};
    return n;
  }

protected:
  const Branch<std::vector<bool>> *fIDloose;
  const Branch<std::vector<bool>> *fIDtight;
  const Branch<std::vector<bool>> *fIDtightLeptonVeto;
  const Branch<std::vector<bool>> *fPUIDloose;
  const Branch<std::vector<bool>> *fPUIDmedium;
  const Branch<std::vector<bool>> *fPUIDtight;
  const Branch<std::vector<double>> *fEJERdown;
  const Branch<std::vector<double>> *fEJERup;
  const Branch<std::vector<double>> *fEJESdown;
  const Branch<std::vector<double>> *fEJESup;
  const Branch<std::vector<double>> *fEMCjet;
  const Branch<std::vector<double>> *fEtaJERdown;
  const Branch<std::vector<double>> *fEtaJERup;
  const Branch<std::vector<double>> *fEtaJESdown;
  const Branch<std::vector<double>> *fEtaJESup;
  const Branch<std::vector<double>> *fEtaMCjet;
  const Branch<std::vector<double>> *fPhiJERdown;
  const Branch<std::vector<double>> *fPhiJERup;
  const Branch<std::vector<double>> *fPhiJESdown;
  const Branch<std::vector<double>> *fPhiJESup;
  const Branch<std::vector<double>> *fPhiMCjet;
  const Branch<std::vector<double>> *fPileupJetIdfullDiscriminant;
  const Branch<std::vector<double>> *fPtJERdown;
  const Branch<std::vector<double>> *fPtJERup;
  const Branch<std::vector<double>> *fPtJESdown;
  const Branch<std::vector<double>> *fPtJESup;
  const Branch<std::vector<double>> *fPtMCjet;
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
  JetGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~JetGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->pfCombinedInclusiveSecondaryVertexBJetTags(); },
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfCombinedSecondaryVertexBJetTags(); },
      [&](){ return this->pfJetBProbabilityBJetTags(); },
      [&](){ return this->pfJetProbabilityBJetTags(); }
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
  std::vector<std::function<bool()>> getJetIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }

  bool IDloose() const { return this->fCollection->fIDloose->value()[this->index()]; }
  bool IDtight() const { return this->fCollection->fIDtight->value()[this->index()]; }
  bool IDtightLeptonVeto() const { return this->fCollection->fIDtightLeptonVeto->value()[this->index()]; }
  bool PUIDloose() const { return this->fCollection->fPUIDloose->value()[this->index()]; }
  bool PUIDmedium() const { return this->fCollection->fPUIDmedium->value()[this->index()]; }
  bool PUIDtight() const { return this->fCollection->fPUIDtight->value()[this->index()]; }
  double eJERdown() const { return this->fCollection->fEJERdown->value()[this->index()]; }
  double eJERup() const { return this->fCollection->fEJERup->value()[this->index()]; }
  double eJESdown() const { return this->fCollection->fEJESdown->value()[this->index()]; }
  double eJESup() const { return this->fCollection->fEJESup->value()[this->index()]; }
  double eMCjet() const { return this->fCollection->fEMCjet->value()[this->index()]; }
  double etaJERdown() const { return this->fCollection->fEtaJERdown->value()[this->index()]; }
  double etaJERup() const { return this->fCollection->fEtaJERup->value()[this->index()]; }
  double etaJESdown() const { return this->fCollection->fEtaJESdown->value()[this->index()]; }
  double etaJESup() const { return this->fCollection->fEtaJESup->value()[this->index()]; }
  double etaMCjet() const { return this->fCollection->fEtaMCjet->value()[this->index()]; }
  double phiJERdown() const { return this->fCollection->fPhiJERdown->value()[this->index()]; }
  double phiJERup() const { return this->fCollection->fPhiJERup->value()[this->index()]; }
  double phiJESdown() const { return this->fCollection->fPhiJESdown->value()[this->index()]; }
  double phiJESup() const { return this->fCollection->fPhiJESup->value()[this->index()]; }
  double phiMCjet() const { return this->fCollection->fPhiMCjet->value()[this->index()]; }
  double pileupJetIdfullDiscriminant() const { return this->fCollection->fPileupJetIdfullDiscriminant->value()[this->index()]; }
  double ptJERdown() const { return this->fCollection->fPtJERdown->value()[this->index()]; }
  double ptJERup() const { return this->fCollection->fPtJERup->value()[this->index()]; }
  double ptJESdown() const { return this->fCollection->fPtJESdown->value()[this->index()]; }
  double ptJESup() const { return this->fCollection->fPtJESup->value()[this->index()]; }
  double ptMCjet() const { return this->fCollection->fPtMCjet->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexBJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexBJetTags->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedMVABJetTag() const { return this->fCollection->fPfCombinedMVABJetTag->value()[this->index()]; }
  float pfCombinedSecondaryVertexBJetTags() const { return this->fCollection->fPfCombinedSecondaryVertexBJetTags->value()[this->index()]; }
  float pfJetBProbabilityBJetTags() const { return this->fCollection->fPfJetBProbabilityBJetTags->value()[this->index()]; }
  float pfJetProbabilityBJetTags() const { return this->fCollection->fPfJetProbabilityBJetTags->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }

};

#endif
