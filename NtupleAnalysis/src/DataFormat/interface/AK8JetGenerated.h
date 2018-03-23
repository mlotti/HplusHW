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
    static std::vector<std::string> n = { std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags")};
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
  const Branch<std::vector<double>> *fNjettinessAK8tau1;
  const Branch<std::vector<double>> *fNjettinessAK8tau2;
  const Branch<std::vector<double>> *fNjettinessAK8tau3;
  const Branch<std::vector<double>> *fAk8PFJetsCHSPrunedMass;
  const Branch<std::vector<double>> *fAk8PFJetsCHSSoftDropMass;
  const Branch<std::vector<double>> *fCorrPrunedMass;
  const Branch<std::vector<double>> *fSdsubjet1_csv;
  const Branch<std::vector<double>> *fSdsubjet1_eta;
  const Branch<std::vector<double>> *fSdsubjet1_mass;
  const Branch<std::vector<double>> *fSdsubjet1_phi;
  const Branch<std::vector<double>> *fSdsubjet1_pt;
  const Branch<std::vector<double>> *fSdsubjet2_csv;
  const Branch<std::vector<double>> *fSdsubjet2_eta;
  const Branch<std::vector<double>> *fSdsubjet2_mass;
  const Branch<std::vector<double>> *fSdsubjet2_phi;
  const Branch<std::vector<double>> *fSdsubjet2_pt;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<int>> *fHadronFlavour;
  const Branch<std::vector<int>> *fNsoftdropSubjets;
  const Branch<std::vector<int>> *fNumberOfDaughters;
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
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); }
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
  double NjettinessAK8tau1() const { return this->fCollection->fNjettinessAK8tau1->value()[this->index()]; }
  double NjettinessAK8tau2() const { return this->fCollection->fNjettinessAK8tau2->value()[this->index()]; }
  double NjettinessAK8tau3() const { return this->fCollection->fNjettinessAK8tau3->value()[this->index()]; }
  double ak8PFJetsCHSPrunedMass() const { return this->fCollection->fAk8PFJetsCHSPrunedMass->value()[this->index()]; }
  double ak8PFJetsCHSSoftDropMass() const { return this->fCollection->fAk8PFJetsCHSSoftDropMass->value()[this->index()]; }
  double corrPrunedMass() const { return this->fCollection->fCorrPrunedMass->value()[this->index()]; }
  double sdsubjet1_csv() const { return this->fCollection->fSdsubjet1_csv->value()[this->index()]; }
  double sdsubjet1_eta() const { return this->fCollection->fSdsubjet1_eta->value()[this->index()]; }
  double sdsubjet1_mass() const { return this->fCollection->fSdsubjet1_mass->value()[this->index()]; }
  double sdsubjet1_phi() const { return this->fCollection->fSdsubjet1_phi->value()[this->index()]; }
  double sdsubjet1_pt() const { return this->fCollection->fSdsubjet1_pt->value()[this->index()]; }
  double sdsubjet2_csv() const { return this->fCollection->fSdsubjet2_csv->value()[this->index()]; }
  double sdsubjet2_eta() const { return this->fCollection->fSdsubjet2_eta->value()[this->index()]; }
  double sdsubjet2_mass() const { return this->fCollection->fSdsubjet2_mass->value()[this->index()]; }
  double sdsubjet2_phi() const { return this->fCollection->fSdsubjet2_phi->value()[this->index()]; }
  double sdsubjet2_pt() const { return this->fCollection->fSdsubjet2_pt->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int nsoftdropSubjets() const { return this->fCollection->fNsoftdropSubjets->value()[this->index()]; }
  int numberOfDaughters() const { return this->fCollection->fNumberOfDaughters->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCjet;

};

#endif
