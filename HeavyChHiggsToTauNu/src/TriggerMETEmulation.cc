#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  TriggerMETEmulation::Data::Data():
    fPassedEvent(false) {}
  TriggerMETEmulation::Data::~Data() {}

  TriggerMETEmulation::TriggerMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fmetEmulationCutCount(eventCounter.addSubCounter("Trigger MET emulation","Trigger met emulation cut"))
  {
    edm::Service<TFileService> fs;
    hMetBeforeEmulation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "MetBeforeEmulation", "MetBeforeEmul", 100, 0.0, 300.0);
    hMetAfterEmulation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "MetAfterEmulation", "MetAfterEmul", 100, 0.0, 300.0);
  }

  TriggerMETEmulation::~TriggerMETEmulation() {}


  TriggerMETEmulation::Data TriggerMETEmulation::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  TriggerMETEmulation::Data TriggerMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  TriggerMETEmulation::Data TriggerMETEmulation::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;

    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hMetBeforeEmulation->Fill(met->et());
    if(met->et() > fmetEmulationCut) {
      output.fPassedEvent = true;
      hMetAfterEmulation->Fill(met->et());
      increment(fmetEmulationCutCount);
    } else {
      output.fPassedEvent = false;
    }
    output.fSelectedTriggerMET = met;
    return output;
  }
}
