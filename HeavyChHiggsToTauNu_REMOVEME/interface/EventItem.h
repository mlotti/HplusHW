// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventItem_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventItem_h

#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

namespace HPlus {
  template <typename T>
  struct EventItem {
    EventItem(const std::string& n, const edm::InputTag& s): name(n), src(s) {}
    ~EventItem() {}
    std::string name;
    edm::InputTag src;
    T value;
  };
}

#endif
