// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MuonGenerated_h
#define DataFormat_MuonGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class MuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonGeneratedCollection(const std::string& prefix="Muons")
  : ParticleCollection(prefix),
    fMCmuon(prefix)
  {
    fMCmuon.setEnergySystematicsVariation("_MCmuon");
  }
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("muIDLoose"), std::string("muIDMedium"), std::string("muIDTight")};
    return n;
  }

  const ParticleCollection<double>* getMCmuonCollection() const { return &fMCmuon; }
protected:
  ParticleCollection<double> fMCmuon;

protected:
  const Branch<std::vector<bool>> *fIsGlobalMuon;
  const Branch<std::vector<bool>> *fMuIDLoose;
  const Branch<std::vector<bool>> *fMuIDMedium;
  const Branch<std::vector<bool>> *fMuIDTight;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCmuon(coll->getMCmuonCollection(), index)
  {}
  ~MuonGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->muIDLoose(); },
      [&](){ return this->muIDMedium(); },
      [&](){ return this->muIDTight(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCmuon() const { return &fMCmuon; }

  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }
  bool muIDLoose() const { return this->fCollection->fMuIDLoose->value()[this->index()]; }
  bool muIDMedium() const { return this->fCollection->fMuIDMedium->value()[this->index()]; }
  bool muIDTight() const { return this->fCollection->fMuIDTight->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCmuon;

};

#endif
