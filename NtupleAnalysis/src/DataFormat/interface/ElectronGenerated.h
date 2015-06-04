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

protected:

};


template <typename Coll>
class ElectronGenerated: public Particle<Coll> {
public:
  ElectronGenerated() {}
  ElectronGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~ElectronGenerated() {}

  std::vector<std::string> getIDDiscriminatorNames() {
    static std::vector<std::string> n[0] = {};
    return n;
  }
  std::vector<std::function<bool()>> getIDDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
    };
    return values;
  }



};

#endif
