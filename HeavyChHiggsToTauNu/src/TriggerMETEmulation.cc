#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  TriggerMETEmulation::Data::Data(const TriggerMETEmulation *triggerMETEmulation, bool passedEvent):
    fTriggerMETEmulation(triggerMETEmulation), fPassedEvent(passedEvent) {}
  TriggerMETEmulation::Data::~Data() {}

  TriggerMETEmulation::TriggerMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fmetEmulationCutCount(eventCounter.addCounter("met emulation cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hmetAfterTrigger = fs->make<TH1F>("metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
  }

  TriggerMETEmulation::~TriggerMETEmulation() {}

  TriggerMETEmulation::Data TriggerMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hmetAfterTrigger->Fill(met->et());
    if(met->et() > fmetEmulationCut) 
      passEvent = true;

    increment(fmetEmulationCutCount);
    fSelectedTriggerMET = met;
    return Data(this, passEvent);
  }
}
