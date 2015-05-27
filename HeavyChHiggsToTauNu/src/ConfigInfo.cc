#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConfigInfo.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TNamed.h"

namespace HPlus {
  namespace ConfigInfo {
    void writeConfigInfo(const edm::ParameterSet& iConfig, TFileDirectory& fd) {
      TFileDirectory dir = fd.mkdir("configInfo");
      dir.make<TNamed>("parameterSet", iConfig.dump().c_str());
      edm::ParameterSet info = iConfig.getParameter<edm::ParameterSet>("configInfo");
      dir.make<TNamed>("pileupReweightType", info.getParameter<std::string>("pileupReweightType"));
      dir.make<TNamed>("topPtReweightType", info.getParameter<std::string>("topPtReweightType"));
    }
  }
}
