#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include <DataFormats/Common/interface/Handle.h>

namespace HPlus {
  EventWeight::EventWeight(const edm::ParameterSet& iConfig) : fWeight(1.0) {
    if (iConfig.exists("prescaleSource")) {
      fPrescaleSrc = iConfig.getUntrackedParameter<edm::InputTag>("prescaleSource");
      fPrescaleAvailableStatus = true;
    } else {
      fPrescaleAvailableStatus = false;
    }
  }
  
  EventWeight::~EventWeight() {
  
  }
  
  void EventWeight::updatePrescale(const edm::Event& iEvent) {
    if (!fPrescaleAvailableStatus) {
      fWeight = 1.0;
      return;
    }
    edm::Handle<double> myHandle;
    iEvent.getByLabel(fPrescaleSrc, myHandle);
    fWeight = *myHandle;
  }
}
