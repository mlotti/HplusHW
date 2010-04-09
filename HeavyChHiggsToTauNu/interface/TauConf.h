// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauConf_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauConf_h

#include "FWCore/Utilities/interface/InputTag.h"
#include<vector>
#include<string>

struct CaloTauConf {
  CaloTauConf(const edm::InputTag& l, const std::vector<edm::InputTag>& d, const std::vector<std::string>& c):
    label(l), discriminators(d), corrections(c) {}
  edm::InputTag label;
  std::vector<edm::InputTag> discriminators;
  std::vector<std::string> corrections;
};

struct PFTauConf {
  PFTauConf(const edm::InputTag& l, const std::vector<edm::InputTag>& d):
    label(l), discriminators(d) {}
  edm::InputTag label;
  std::vector<edm::InputTag> discriminators;
};

#endif
