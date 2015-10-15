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

  std::vector<std::string> getDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("Flag_CSCTightHaloFilter"), std::string("Flag_eeBadScFilter"), std::string("Flag_goodVertices"), std::string("hbheIsoNoiseToken"), std::string("hbheNoiseTokenRun2Loose"), std::string("hbheNoiseTokenRun2Tight") };
    return n;
  }

  std::vector<std::function<bool()>> getDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->passFlag_CSCTightHaloFilter(); },
      [&](){ return this->passFlag_eeBadScFilter(); },
      [&](){ return this->passFlag_goodVertices(); },
      [&](){ return this->passHbheIsoNoiseToken(); },
      [&](){ return this->passHbheNoiseTokenRun2Loose(); },
      [&](){ return this->passHbheNoiseTokenRun2Tight(); }
    };
    return values;
  }

  bool passFlag_CSCTightHaloFilter() const { return fFlag_CSCTightHaloFilter->value(); }
  bool passFlag_eeBadScFilter() const { return fFlag_eeBadScFilter->value(); }
  bool passFlag_goodVertices() const { return fFlag_goodVertices->value(); }
  bool passHbheIsoNoiseToken() const { return fHbheIsoNoiseToken->value(); }
  bool passHbheNoiseTokenRun2Loose() const { return fHbheNoiseTokenRun2Loose->value(); }
  bool passHbheNoiseTokenRun2Tight() const { return fHbheNoiseTokenRun2Tight->value(); }

protected:
  const Branch<bool> *fFlag_CSCTightHaloFilter;
  const Branch<bool> *fFlag_eeBadScFilter;
  const Branch<bool> *fFlag_goodVertices;
  const Branch<bool> *fHbheIsoNoiseToken;
  const Branch<bool> *fHbheNoiseTokenRun2Loose;
  const Branch<bool> *fHbheNoiseTokenRun2Tight;

};

#endif
