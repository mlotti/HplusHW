// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ConfigInfo_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ConfigInfo_h

#include "CommonTools/Utils/interface/TFileDirectory.h"

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  namespace ConfigInfo {
    void writeConfigInfo(const edm::ParameterSet& iConfig, TFileDirectory& fd);
  }
}

#endif
