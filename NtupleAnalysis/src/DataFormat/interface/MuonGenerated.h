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
  explicit MuonGeneratedCollection(const std::string& prefix="Muons"): ParticleCollection(prefix) {}
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("muIDLoose"), std::string("muIDMedium"), std::string("muIDTight")};
    return n;
  }

protected:
  const Branch<std::vector<bool>> *fIsGlobalMuon;
  const Branch<std::vector<bool>> *fMuIDLoose;
  const Branch<std::vector<bool>> *fMuIDMedium;
  const Branch<std::vector<bool>> *fMuIDTight;
  const Branch<std::vector<double>> *fEMCmuon;
  const Branch<std::vector<double>> *fEtaMCmuon;
  const Branch<std::vector<double>> *fPhiMCmuon;
  const Branch<std::vector<double>> *fPtMCmuon;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~MuonGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->muIDLoose(); },
      [&](){ return this->muIDMedium(); },
      [&](){ return this->muIDTight(); }
    };
    return values;
  }

  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }
  bool muIDLoose() const { return this->fCollection->fMuIDLoose->value()[this->index()]; }
  bool muIDMedium() const { return this->fCollection->fMuIDMedium->value()[this->index()]; }
  bool muIDTight() const { return this->fCollection->fMuIDTight->value()[this->index()]; }
  double eMCmuon() const { return this->fCollection->fEMCmuon->value()[this->index()]; }
  double etaMCmuon() const { return this->fCollection->fEtaMCmuon->value()[this->index()]; }
  double phiMCmuon() const { return this->fCollection->fPhiMCmuon->value()[this->index()]; }
  double ptMCmuon() const { return this->fCollection->fPtMCmuon->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }

};

#endif
