#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"

namespace HPlusAnalysis {

HPlusAnalysisBase::HPlusAnalysisBase(Counter* counter)
  : fCounter(counter) {
  fOwnsCounterStatus = false;
}

HPlusAnalysisBase::HPlusAnalysisBase(std::string aModuleName) {
  fOwnsCounterStatus = true;
  fCounter = new Counter(aModuleName);
}

HPlusAnalysisBase::~HPlusAnalysisBase() {
  if (fOwnsCounterStatus) {
    fCounter->storeCountersToHistogram(fFileService);
    delete fCounter;
  }
}
/*
void HPlusAnalysisBase::setup(const edm::ParameterSet& iConfig) { 

}

bool HPlusAnalysisBase::apply(const edm::Event& iEvent) {
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'apply'-method?";
  return false;
}
*/
}
