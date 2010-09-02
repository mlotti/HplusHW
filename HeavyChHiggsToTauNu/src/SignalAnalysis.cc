#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter) {
    edm::Service<TFileService> fs;

    count1 = eventCounter.addCounter("foo1");
    count2 = eventCounter.addSubCounter("foo1", "foo2");
  }
  SignalAnalysis::~SignalAnalysis() {}

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    count1.increment();
    count2.increment();
    count2.increment(2);
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  }
}
