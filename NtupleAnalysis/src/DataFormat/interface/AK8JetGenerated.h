// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_AK8JetGenerated_h
#define DataFormat_AK8JetGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class AK8JetGeneratedCollection: public ParticleCollection<double> {
public:
  explicit AK8JetGeneratedCollection(const std::string& prefix="AK8Jets")
  : ParticleCollection(prefix),
    fMCjet(prefix)
  {
    fMCjet.setEnergySystematicsVariation("_MCjet");
  }
  ~AK8JetGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getBJetTagsDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("pfCombinedCvsBJetTags"), std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("pfCombinedMVAV2BJetTags")};
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
  const Branch<std::vector<bool>> *fOriginatesFromChargedHiggs;
  const Branch<std::vector<bool>> *fOriginatesFromTop;
  const Branch<std::vector<bool>> *fOriginatesFromUnknown;
  const Branch<std::vector<bool>> *fOriginatesFromW;
  const Branch<std::vector<bool>> *fOriginatesFromZ;
  const Branch<std::vector<double>> *fNjettinessAK8CHStau1;
  const Branch<std::vector<double>> *fNjettinessAK8CHStau2;
  const Branch<std::vector<double>> *fNjettinessAK8CHStau3;
  const Branch<std::vector<double>> *fNjettinessAK8CHStau4;
  const Branch<std::vector<float>> *fPfCombinedCvsBJetTags;
  const Branch<std::vector<float>> *fPfCombinedCvsLJetTags;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fPfCombinedMVAV2BJetTags;
  const Branch<std::vector<int>> *fHadronFlavour;
  const Branch<std::vector<int>> *fPartonFlavour;
};


template <typename Coll>
class AK8JetGenerated: public Particle<Coll> {
public:
  AK8JetGenerated() {}
  AK8JetGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCjet(coll->getMCjetCollection(), index)
  {}
  ~AK8JetGenerated() {}

  std::vector<std::function<bool()>> getBJetTagsDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->pfCombinedCvsBJetTags(); },
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfCombinedMVAV2BJetTags(); }
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
  bool originatesFromChargedHiggs() const { return this->fCollection->fOriginatesFromChargedHiggs->value()[this->index()]; }
  bool originatesFromTop() const { return this->fCollection->fOriginatesFromTop->value()[this->index()]; }
  bool originatesFromUnknown() const { return this->fCollection->fOriginatesFromUnknown->value()[this->index()]; }
  bool originatesFromW() const { return this->fCollection->fOriginatesFromW->value()[this->index()]; }
  bool originatesFromZ() const { return this->fCollection->fOriginatesFromZ->value()[this->index()]; }
  double NjettinessAK8CHStau1() const { return this->fCollection->fNjettinessAK8CHStau1->value()[this->index()]; }
  double NjettinessAK8CHStau2() const { return this->fCollection->fNjettinessAK8CHStau2->value()[this->index()]; }
  double NjettinessAK8CHStau3() const { return this->fCollection->fNjettinessAK8CHStau3->value()[this->index()]; }
  double NjettinessAK8CHStau4() const { return this->fCollection->fNjettinessAK8CHStau4->value()[this->index()]; }
  float pfCombinedCvsBJetTags() const { return this->fCollection->fPfCombinedCvsBJetTags->value()[this->index()]; }
  float pfCombinedCvsLJetTags() const { return this->fCollection->fPfCombinedCvsLJetTags->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedMVAV2BJetTags() const { return this->fCollection->fPfCombinedMVAV2BJetTags->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCjet;

};

#endif
