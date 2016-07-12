#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"


namespace HPlus {
  VertexSelection::Data::Data():
    fPassedEvent(false), fNumberOfAllVertices(0) {}
  VertexSelection::Data::~Data() {}

  VertexSelection::VertexSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSelectedSrc(iConfig.getUntrackedParameter<edm::InputTag>("selectedSrc")),
    fAllSrc(iConfig.getUntrackedParameter<edm::InputTag>("allSrc")),
    fSumPtSrc(iConfig.getUntrackedParameter<edm::InputTag>("sumPtSrc")),
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

    edm::Handle<edm::View<reco::Vertex> > hvertexall;
    iEvent.getByLabel(fAllSrc, hvertexall);
    output.fNumberOfAllVertices = hvertexall->size();

    if(!fEnabled) {
      output.fPassedEvent = true;
      return output;
    }

    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fSelectedSrc, hvertex);

    if(hvertex->empty()) {
      output.fPassedEvent = false;
      return output;
    }

    output.fSelectedVertex = hvertex->ptrAt(0);
    output.fPassedEvent = true;

    edm::Handle<edm::ValueMap<float> > hSumPt;
    iEvent.getByLabel(fSumPtSrc, hSumPt);
    output.fSumPt = (*hSumPt)[hvertexall->ptrAt(0)];

    return output;
  }
}
