#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter)
  {
    edm::Service<TFileService> fs;
    hTransverseMass = fs->make<TH1F>("transverseMass", "transverseMass", 100, 0., 200.);

  }

  SignalAnalysis::~SignalAnalysis() {}

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);

    if(!fTriggerSelection.analyze(iEvent, iSetup)) return;

    if(!fTauSelection.analyze(iEvent, iSetup)) return;

    if(!fJetSelection.analyze(iEvent, iSetup, fTauSelection.getSelectedTaus())) return;

    if(!fBTagging.analyze(fJetSelection.getSelectedJets())) return;

    if(!fMETSelection.analyze(iEvent, iSetup)) return;

    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()));
    hTransverseMass->Fill(transverseMass);
  }
}
