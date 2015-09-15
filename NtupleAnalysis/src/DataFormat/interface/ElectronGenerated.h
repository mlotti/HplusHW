// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_ElectronGenerated_h
#define DataFormat_ElectronGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class ElectronGeneratedCollection: public ParticleCollection<double> {
public:
  explicit ElectronGeneratedCollection(const std::string& prefix="Electrons"): ParticleCollection(prefix) {}
  ~ElectronGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80"), std::string("mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90")};
    return n;
  }

protected:
  const Branch<std::vector<bool>> *fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80;
  const Branch<std::vector<bool>> *fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90;
  const Branch<std::vector<double>> *fEMCelectron;
  const Branch<std::vector<double>> *fEtaMCelectron;
  const Branch<std::vector<double>> *fPhiMCelectron;
  const Branch<std::vector<double>> *fPtMCelectron;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
};


template <typename Coll>
class ElectronGenerated: public Particle<Coll> {
public:
  ElectronGenerated() {}
  ElectronGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~ElectronGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80(); },
      [&](){ return this->mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90(); }
    };
    return values;
  }

  bool mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80() const { return this->fCollection->fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80->value()[this->index()]; }
  bool mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90() const { return this->fCollection->fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90->value()[this->index()]; }
  double eMCelectron() const { return this->fCollection->fEMCelectron->value()[this->index()]; }
  double etaMCelectron() const { return this->fCollection->fEtaMCelectron->value()[this->index()]; }
  double phiMCelectron() const { return this->fCollection->fPhiMCelectron->value()[this->index()]; }
  double ptMCelectron() const { return this->fCollection->fPtMCelectron->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }

};

#endif
