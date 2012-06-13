#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include <DataFormats/Common/interface/Handle.h>

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
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
    TFileDirectory myVertexDir = fs->mkdir("Prescales");
    hPrescaleHistoLowScale = histoWrapper->makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Trigger_Prescale_Low_part", "Trigger_Prescale_Low_part;Trigger Prescale Factor;N_{events} / 1", 100, 0., 100.);
    hPrescaleHistoMediumScale = histoWrapper->makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Trigger_Prescale_Medium_part", "Trigger_Prescale_Medium_part;Trigger Prescale Factor;N_{events} / 50", 200, 0., 10000.);
    hPrescaleHistoHighScale = histoWrapper->makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Trigger_Prescale_High_part", "Trigger_Prescale_High_part;Trigger Prescale Factor;N_{events} / 5000", 200, 0., 1000000.);
  }
  
  EventWeight::~EventWeight() {
  
  }
  
  void EventWeight::updatePrescale(const edm::Event& iEvent) {
    if (!fPrescaleAvailableStatus) {
      fWeight = 1.0;
    } else {
      edm::Handle<double> myHandle;
      iEvent.getByLabel(fPrescaleSrc, myHandle);
      fWeight = *myHandle;
    }
    hPrescaleHistoLowScale->Fill(fWeight);
    hPrescaleHistoMediumScale->Fill(fWeight);
    hPrescaleHistoHighScale->Fill(fWeight);
  }
}
