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
  explicit ElectronGeneratedCollection(const std::string& prefix="Electrons")
  : ParticleCollection(prefix),
    fMCelectron(prefix)
  {
    fMCelectron.setEnergySystematicsVariation("_MCelectron");
  }
  ~ElectronGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("cutBasedElectronID_Spring15_25ns_V1_standalone_loose"), std::string("cutBasedElectronID_Spring15_25ns_V1_standalone_medium"), std::string("cutBasedElectronID_Spring15_25ns_V1_standalone_tight"), std::string("cutBasedElectronID_Spring15_25ns_V1_standalone_veto")};
    return n;
  }

  const ParticleCollection<double>* getMCelectronCollection() const { return &fMCelectron; }
protected:
  ParticleCollection<double> fMCelectron;

protected:
  const Branch<std::vector<bool>> *fCutBasedElectronID_Spring15_25ns_V1_standalone_loose;
  const Branch<std::vector<bool>> *fCutBasedElectronID_Spring15_25ns_V1_standalone_medium;
  const Branch<std::vector<bool>> *fCutBasedElectronID_Spring15_25ns_V1_standalone_tight;
  const Branch<std::vector<bool>> *fCutBasedElectronID_Spring15_25ns_V1_standalone_veto;
  const Branch<std::vector<float>> *fEffAreaIsoDeltaBeta;
  const Branch<std::vector<float>> *fEffAreaMiniIso;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
  const Branch<std::vector<float>> *fRelMiniIso;
};


template <typename Coll>
class ElectronGenerated: public Particle<Coll> {
public:
  ElectronGenerated() {}
  ElectronGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCelectron(coll->getMCelectronCollection(), index)
  {}
  ~ElectronGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->cutBasedElectronID_Spring15_25ns_V1_standalone_loose(); },
      [&](){ return this->cutBasedElectronID_Spring15_25ns_V1_standalone_medium(); },
      [&](){ return this->cutBasedElectronID_Spring15_25ns_V1_standalone_tight(); },
      [&](){ return this->cutBasedElectronID_Spring15_25ns_V1_standalone_veto(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCelectron() const { return &fMCelectron; }

  bool cutBasedElectronID_Spring15_25ns_V1_standalone_loose() const { return this->fCollection->fCutBasedElectronID_Spring15_25ns_V1_standalone_loose->value()[this->index()]; }
  bool cutBasedElectronID_Spring15_25ns_V1_standalone_medium() const { return this->fCollection->fCutBasedElectronID_Spring15_25ns_V1_standalone_medium->value()[this->index()]; }
  bool cutBasedElectronID_Spring15_25ns_V1_standalone_tight() const { return this->fCollection->fCutBasedElectronID_Spring15_25ns_V1_standalone_tight->value()[this->index()]; }
  bool cutBasedElectronID_Spring15_25ns_V1_standalone_veto() const { return this->fCollection->fCutBasedElectronID_Spring15_25ns_V1_standalone_veto->value()[this->index()]; }
  float effAreaIsoDeltaBeta() const { return this->fCollection->fEffAreaIsoDeltaBeta->value()[this->index()]; }
  float effAreaMiniIso() const { return this->fCollection->fEffAreaMiniIso->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }
  float relMiniIso() const { return this->fCollection->fRelMiniIso->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCelectron;

};

#endif
