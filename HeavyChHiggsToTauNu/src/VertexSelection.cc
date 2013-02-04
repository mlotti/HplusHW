#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"


namespace HPlus {
  VertexSelection::Data::Data():
    fPassedEvent(false) {}
  VertexSelection::Data::~Data() {}

  VertexSelection::VertexSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fEnabled(iConfig.getUntrackedParameter<bool>("enabled"))
  {}

  VertexSelection::~VertexSelection() {}

  VertexSelection::Data VertexSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  VertexSelection::Data VertexSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  VertexSelection::Data VertexSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;

    if(!fEnabled) {
      output.fPassedEvent = true;
      return output;
    }

    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fSrc, hvertex);

    if(hvertex->empty()) {
      output.fPassedEvent = false;
      return output;
    }

    output.fSelectedVertex = hvertex->ptrAt(0);
    output.fPassedEvent = true;
    return output;
  }
}
