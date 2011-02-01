#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include <DataFormats/Common/interface/Handle.h>

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


namespace HPlus {
  EventWeight::EventWeight(const edm::ParameterSet& iConfig) : 
    fWeight(1.0)
  {
    if (iConfig.exists("prescaleSource")) {
      fPrescaleSrc = iConfig.getUntrackedParameter<edm::InputTag>("prescaleSource");
      fPrescaleAvailableStatus = true;
    } else {
      fPrescaleAvailableStatus = false;
    }
    // Histograms
    edm::Service<TFileService> fs;

    hPrescaleHisto = makeTH<TH1F>(*fs, "Trigger_Prescale", "Trigger_Prescale;Trigger Prescale Factor;N_{events} / 50", 200, 0., 10000.);
  }
  
  EventWeight::~EventWeight() {
  
  }
  
  void EventWeight::updatePrescale(const edm::Event& iEvent) {
    if (!fPrescaleAvailableStatus) {
      fWeight = 1.0;
      hPrescaleHisto->Fill(fWeight);
      return;
    }
    edm::Handle<double> myHandle;
    iEvent.getByLabel(fPrescaleSrc, myHandle);
    fWeight = *myHandle;
    hPrescaleHisto->Fill(fWeight);
  }
}
