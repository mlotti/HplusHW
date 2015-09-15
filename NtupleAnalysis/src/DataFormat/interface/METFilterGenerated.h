// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_METFilterGenerated_h
#define DataFormat_METFilterGenerated_h

#include <string>
#include <vector>
#include <functional>
#include "Framework/interface/BranchManager.h"

class METFilterGenerated {
public:
  explicit METFilterGenerated() {}
  ~METFilterGenerated() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("CSCTightHaloFilter"), std::string("EeBadScFilter"), std::string("GoodVertices") };
    return n;
  }

  std::vector<std::function<bool()>> getDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->passCSCTightHaloFilter(); },
      [&](){ return this->passEeBadScFilter(); },
      [&](){ return this->passGoodVertices(); }
    };
    return values;
  }

  bool passCSCTightHaloFilter() const { return fCSCTightHaloFilter->value(); }
  bool passEeBadScFilter() const { return fEeBadScFilter->value(); }
  bool passGoodVertices() const { return fGoodVertices->value(); }

protected:
  const Branch<bool> *fCSCTightHaloFilter;
  const Branch<bool> *fEeBadScFilter;
  const Branch<bool> *fGoodVertices;

};

#endif
