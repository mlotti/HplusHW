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

protected:
  const Branch<std::vector<bool>> *fIsGlobalMuon;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~MuonGenerated() {}

  std::vector<std::string> getIDDiscriminatorNames() {
    static std::vector<std::string> n[0] = {};
    return n;
  }
  std::vector<std::function<bool()>> getIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }

  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }

};

#endif
