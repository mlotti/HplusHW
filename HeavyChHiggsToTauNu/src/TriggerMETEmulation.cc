#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

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

  TriggerMETEmulation::TriggerMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fmetEmulationCutCount(eventCounter.addSubCounter("Trigger MET emulation","Trigger met emulation cut"))
  {
    edm::Service<TFileService> fs;
    hMetBeforeEmulation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "MetBeforeEmulation", "MetBeforeEmul", 100, 0.0, 300.0);
    hMetAfterEmulation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "MetAfterEmulation", "MetAfterEmul", 100, 0.0, 300.0);
  }

  TriggerMETEmulation::~TriggerMETEmulation() {}

  TriggerMETEmulation::Data TriggerMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hMetBeforeEmulation->Fill(met->et());
    if(met->et() > fmetEmulationCut) {
      passEvent = true;
      hMetAfterEmulation->Fill(met->et());
      increment(fmetEmulationCutCount);
    }
    fSelectedTriggerMET = met;
    return Data(this, passEvent);
  }
}
