#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {

  TriggerMETEmulation::TriggerMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fmetEmulationCutCount(eventCounter.addCounter("met emulation cut"))
  {
    edm::Service<TFileService> fs;
    hmetAfterTrigger = fs->make<TH1F>("metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
  }

  TriggerMETEmulation::~TriggerMETEmulation() {}

  bool TriggerMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hmetAfterTrigger->Fill(met->et());
    if(!(met->et() > fmetEmulationCut)) return false;

    increment(fmetEmulationCutCount);
    fSelectedTriggerMET = met;
    return true;
  }
}
