#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter),
    ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut"))
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    hTransverseMass = fs->make<TH1F>("transverseMass", "transverseMass", 100, 0., 200.);
    hDeltaPhi = fs->make<TH1F>("deltaPhi", "deltaPhi", 60, 0., 180.);
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

    if(!fMETSelection.analyze(iEvent, iSetup)) return;

    if(!fBTagging.analyze(fJetSelection.getSelectedJets())) return;


    double deltaPhi = DeltaPhi::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3);

    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()));
    hTransverseMass->Fill(transverseMass);

    if(transverseMass < 100 ) return;
    increment(ftransverseMassCutCount);
  }
}
