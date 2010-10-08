#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

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
    ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    hTransverseMass = fs->make<TH1F>("transverseMass", "transverseMass", 100, 0., 200.);
    hDeltaPhi = fs->make<TH1F>("deltaPhi", "deltaPhi", 60, 0., 180.);
    hAlphaT = fs->make<TH1F>("alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = fs->make<TH1F>("alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
  }

  SignalAnalysis::~SignalAnalysis() {}

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
    // std::cout << "void SignalAnalysis::produce()" << std::endl;
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);
    // std::cout << "void SignalAnalysis::analyze()" << std::endl;

    if(!fTriggerSelection.analyze(iEvent, iSetup)) return;
    // std::cout << "fTriggerSelection" << std::endl;
    if(!fTauSelection.analyze(iEvent, iSetup)) return;
    // std::cout << "fTauSelection" << std::endl;
    if(!fJetSelection.analyze(iEvent, iSetup, fTauSelection.getSelectedTaus())) return; 
    // std::cout << "fJetSelection" << std::endl;
    if(!fMETSelection.analyze(iEvent, iSetup)) return;
    // std::cout << "fMETSelection" << std::endl;
    if(!fBTagging.analyze(fJetSelection.getSelectedJets())) return;
    // std::cout << "fBTagging" << std::endl;
    if(!fEvtTopology.analyze(*(fTauSelection.getSelectedTaus()[0]), fJetSelection.getSelectedJets())) return;
    // std::cout << "fEvtTopology" << std::endl;

    double deltaPhi = DeltaPhi::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3);

    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()) );
    hTransverseMass->Fill(transverseMass);
    // if(transverseMass < 100 ) return;
    increment(ftransverseMassCutCount);

    AlphaStruc sAlphaT = fEvtTopology.alphaT();
    hAlphaT->Fill(sAlphaT.fAlphaT);
    
    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
    
  }
}
