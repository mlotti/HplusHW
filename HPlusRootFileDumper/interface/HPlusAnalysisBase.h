#ifndef HPLUSANALYSISHPLUSANALYSISBASE_H
#define HPLUSANALYSISHPLUSANALYSISBASE_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/Counter.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/Event.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <string>

namespace HPlusAnalysis {

/**
Base class for H+ analysis

	@author Lauri Wendland
*/
class HPlusAnalysisBase {
 public:
  HPlusAnalysisBase(Counter* counter);
  HPlusAnalysisBase(std::string aModuleName);
  ~HPlusAnalysisBase();
  
  //virtual void setup(const edm::ParameterSet& iConfig);
  
  //virtual bool apply(const edm::Event& iEvent);
  
 protected:
  edm::Service<TFileService> fFileService;
  /// Pointer to event counter object
  HPlusAnalysis::Counter* fCounter;
  
 private:
  /// True if class owns the Counter object
  bool fOwnsCounterStatus;
};

}

#endif
