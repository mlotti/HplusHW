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
    static std::vector<std::string> n = { std::string("pfCombinedCvsBJetTags"), std::string("pfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("pfCombinedMVAV2BJetTags"), std::string("pfCombinedSecondaryVertexV2BJetTags"), std::string("pfJetBProbabilityBJetTags"), std::string("pfJetProbabilityBJetTags"), std::string("pfSimpleInclusiveSecondaryVertexHighEffBJetTags"), std::string("pfSimpleSecondaryVertexHighEffBJetTags"), std::string("pfTrackCountingHighEffBJetTags"), std::string("softPFElectronBJetTags"), std::string("softPFMuonBJetTags"), std::string("tightpfCombinedCvsBJetTags"), std::string("tightpfCombinedInclusiveSecondaryVertexV2BJetTags"), std::string("tightpfCombinedSecondaryVertexV2BJetTags")};
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
  const Branch<std::vector<double>> *fAK4PFCHSpileupJetIdEvaluatorfullDiscriminant;
  const Branch<std::vector<double>> *fQGTaggerAK4PFCHSaxis2;
  const Branch<std::vector<double>> *fQGTaggerAK4PFCHSptD;
  const Branch<std::vector<double>> *fQGTaggerAK4PFCHSqgLikelihood;
  const Branch<std::vector<double>> *fPileupJetIdfullDiscriminant;
  const Branch<std::vector<float>> *fPfCombinedCvsBJetTags;
  const Branch<std::vector<float>> *fPfCombinedCvsLJetTags;
  const Branch<std::vector<float>> *fPfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fPfCombinedMVAV2BJetTags;
  const Branch<std::vector<float>> *fPfCombinedSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fPfJetBProbabilityBJetTags;
  const Branch<std::vector<float>> *fPfJetProbabilityBJetTags;
  const Branch<std::vector<float>> *fPfSimpleInclusiveSecondaryVertexHighEffBJetTags;
  const Branch<std::vector<float>> *fPfSimpleSecondaryVertexHighEffBJetTags;
  const Branch<std::vector<float>> *fPfTrackCountingHighEffBJetTags;
  const Branch<std::vector<float>> *fSoftPFElectronBJetTags;
  const Branch<std::vector<float>> *fSoftPFMuonBJetTags;
  const Branch<std::vector<float>> *fTightpfCombinedCvsBJetTags;
  const Branch<std::vector<float>> *fTightpfCombinedCvsLJetTags;
  const Branch<std::vector<float>> *fTightpfCombinedInclusiveSecondaryVertexV2BJetTags;
  const Branch<std::vector<float>> *fTightpfCombinedSecondaryVertexV2BJetTags;
  const Branch<std::vector<int>> *fQGTaggerAK4PFCHSmult;
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
      [&](){ return this->pfCombinedCvsBJetTags(); },
      [&](){ return this->pfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfCombinedMVAV2BJetTags(); },
      [&](){ return this->pfCombinedSecondaryVertexV2BJetTags(); },
      [&](){ return this->pfJetBProbabilityBJetTags(); },
      [&](){ return this->pfJetProbabilityBJetTags(); },
      [&](){ return this->pfSimpleInclusiveSecondaryVertexHighEffBJetTags(); },
      [&](){ return this->pfSimpleSecondaryVertexHighEffBJetTags(); },
      [&](){ return this->pfTrackCountingHighEffBJetTags(); },
      [&](){ return this->softPFElectronBJetTags(); },
      [&](){ return this->softPFMuonBJetTags(); },
      [&](){ return this->tightpfCombinedCvsBJetTags(); },
      [&](){ return this->tightpfCombinedInclusiveSecondaryVertexV2BJetTags(); },
      [&](){ return this->tightpfCombinedSecondaryVertexV2BJetTags(); }
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
  double AK4PFCHSpileupJetIdEvaluatorfullDiscriminant() const { return this->fCollection->fAK4PFCHSpileupJetIdEvaluatorfullDiscriminant->value()[this->index()]; }
  double QGTaggerAK4PFCHSaxis2() const { return this->fCollection->fQGTaggerAK4PFCHSaxis2->value()[this->index()]; }
  double QGTaggerAK4PFCHSptD() const { return this->fCollection->fQGTaggerAK4PFCHSptD->value()[this->index()]; }
  double QGTaggerAK4PFCHSqgLikelihood() const { return this->fCollection->fQGTaggerAK4PFCHSqgLikelihood->value()[this->index()]; }
  double pileupJetIdfullDiscriminant() const { return this->fCollection->fPileupJetIdfullDiscriminant->value()[this->index()]; }
  float pfCombinedCvsBJetTags() const { return this->fCollection->fPfCombinedCvsBJetTags->value()[this->index()]; }
  float pfCombinedCvsLJetTags() const { return this->fCollection->fPfCombinedCvsLJetTags->value()[this->index()]; }
  float pfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfCombinedMVAV2BJetTags() const { return this->fCollection->fPfCombinedMVAV2BJetTags->value()[this->index()]; }
  float pfCombinedSecondaryVertexV2BJetTags() const { return this->fCollection->fPfCombinedSecondaryVertexV2BJetTags->value()[this->index()]; }
  float pfJetBProbabilityBJetTags() const { return this->fCollection->fPfJetBProbabilityBJetTags->value()[this->index()]; }
  float pfJetProbabilityBJetTags() const { return this->fCollection->fPfJetProbabilityBJetTags->value()[this->index()]; }
  float pfSimpleInclusiveSecondaryVertexHighEffBJetTags() const { return this->fCollection->fPfSimpleInclusiveSecondaryVertexHighEffBJetTags->value()[this->index()]; }
  float pfSimpleSecondaryVertexHighEffBJetTags() const { return this->fCollection->fPfSimpleSecondaryVertexHighEffBJetTags->value()[this->index()]; }
  float pfTrackCountingHighEffBJetTags() const { return this->fCollection->fPfTrackCountingHighEffBJetTags->value()[this->index()]; }
  float softPFElectronBJetTags() const { return this->fCollection->fSoftPFElectronBJetTags->value()[this->index()]; }
  float softPFMuonBJetTags() const { return this->fCollection->fSoftPFMuonBJetTags->value()[this->index()]; }
  float tightpfCombinedCvsBJetTags() const { return this->fCollection->fTightpfCombinedCvsBJetTags->value()[this->index()]; }
  float tightpfCombinedCvsLJetTags() const { return this->fCollection->fTightpfCombinedCvsLJetTags->value()[this->index()]; }
  float tightpfCombinedInclusiveSecondaryVertexV2BJetTags() const { return this->fCollection->fTightpfCombinedInclusiveSecondaryVertexV2BJetTags->value()[this->index()]; }
  float tightpfCombinedSecondaryVertexV2BJetTags() const { return this->fCollection->fTightpfCombinedSecondaryVertexV2BJetTags->value()[this->index()]; }
  int QGTaggerAK4PFCHSmult() const { return this->fCollection->fQGTaggerAK4PFCHSmult->value()[this->index()]; }
  int hadronFlavour() const { return this->fCollection->fHadronFlavour->value()[this->index()]; }
  int partonFlavour() const { return this->fCollection->fPartonFlavour->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCjet;

};

#endif
