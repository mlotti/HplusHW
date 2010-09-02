#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter)
  {}

  SignalAnalysis::~SignalAnalysis() {}

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);

    if(!fTriggerSelection.analyze(iEvent, iSetup)) return;

    if(!fTauSelection.analyze(iEvent, iSetup)) return;
  }
}
