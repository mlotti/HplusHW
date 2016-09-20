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
    static std::vector<std::string> n = { std::string("Flag_CSCTightHaloFilter"), std::string("Flag_EcalDeadCellTriggerPrimitiveFilter"), std::string("Flag_HBHENoiseFilter"), std::string("Flag_HBHENoiseIsoFilter"), std::string("Flag_eeBadScFilter"), std::string("Flag_globalTightHalo2016Filter"), std::string("Flag_goodVertices"), std::string("badChargedCandidateFilter"), std::string("badPFMuonFilter"), std::string("hbheIsoNoiseToken"), std::string("hbheNoiseTokenRun2Loose"), std::string("hbheNoiseTokenRun2Tight") };
    return n;
  }

  std::vector<std::function<bool()>> getDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->passFlag_CSCTightHalo2015Filter(); },
      [&](){ return this->passFlag_CSCTightHaloFilter(); },
      [&](){ return this->passFlag_EcalDeadCellTriggerPrimitiveFilter(); },
      [&](){ return this->passFlag_HBHENoiseFilter(); },
      [&](){ return this->passFlag_HBHENoiseIsoFilter(); },
      [&](){ return this->passFlag_eeBadScFilter(); },
      [&](){ return this->passFlag_globalTightHalo2016Filter(); },
      [&](){ return this->passFlag_goodVertices(); },
      [&](){ return this->passBadChargedCandidateFilter(); },
      [&](){ return this->passBadPFMuonFilter(); },
      [&](){ return this->passHbheIsoNoiseToken(); },
      [&](){ return this->passHbheNoiseTokenRun2Loose(); },
      [&](){ return this->passHbheNoiseTokenRun2Tight(); }
    };
    return values;
  }

  bool passFlag_CSCTightHalo2015Filter() const { return fFlag_CSCTightHalo2015Filter->value(); }
  bool passFlag_CSCTightHaloFilter() const { return fFlag_CSCTightHaloFilter->value(); }
  bool passFlag_EcalDeadCellTriggerPrimitiveFilter() const { return fFlag_EcalDeadCellTriggerPrimitiveFilter->value(); }
  bool passFlag_HBHENoiseFilter() const { return fFlag_HBHENoiseFilter->value(); }
  bool passFlag_HBHENoiseIsoFilter() const { return fFlag_HBHENoiseIsoFilter->value(); }
  bool passFlag_eeBadScFilter() const { return fFlag_eeBadScFilter->value(); }
  bool passFlag_globalTightHalo2016Filter() const { return fFlag_globalTightHalo2016Filter->value(); }
  bool passFlag_goodVertices() const { return fFlag_goodVertices->value(); }
  bool passBadChargedCandidateFilter() const { return fBadChargedCandidateFilter->value(); }
  bool passBadPFMuonFilter() const { return fBadPFMuonFilter->value(); }
  bool passHbheIsoNoiseToken() const { return fHbheIsoNoiseToken->value(); }
  bool passHbheNoiseTokenRun2Loose() const { return fHbheNoiseTokenRun2Loose->value(); }
  bool passHbheNoiseTokenRun2Tight() const { return fHbheNoiseTokenRun2Tight->value(); }

protected:
  const Branch<bool> *fFlag_CSCTightHalo2015Filter;
  const Branch<bool> *fFlag_CSCTightHaloFilter;
  const Branch<bool> *fFlag_EcalDeadCellTriggerPrimitiveFilter;
  const Branch<bool> *fFlag_HBHENoiseFilter;
  const Branch<bool> *fFlag_HBHENoiseIsoFilter;
  const Branch<bool> *fFlag_eeBadScFilter;
  const Branch<bool> *fFlag_globalTightHalo2016Filter;
  const Branch<bool> *fFlag_goodVertices;
  const Branch<bool> *fBadChargedCandidateFilter;
  const Branch<bool> *fBadPFMuonFilter;
  const Branch<bool> *fHbheIsoNoiseToken;
  const Branch<bool> *fHbheNoiseTokenRun2Loose;
  const Branch<bool> *fHbheNoiseTokenRun2Tight;

};

#endif
