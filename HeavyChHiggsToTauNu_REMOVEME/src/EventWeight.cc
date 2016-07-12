#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

namespace HPlus {
  EventWeight::EventWeight(const edm::ParameterSet& iConfig) : 
    fWeight(1.0)
  {
    if (iConfig.exists("prescaleSource")) {
      throw cms::Exception("Configuration") << "Got prescaleSource configuration parameter. Its use is deprecated, please use the generic WeightReader instead";
    }
  }
  
  EventWeight::~EventWeight() {
  
  }
}
