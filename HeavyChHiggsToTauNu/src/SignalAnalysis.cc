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
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    ftransverseMassCut(iConfig.getUntrackedParameter<double>("transverseMassCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter),
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter),
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    //    hmetAfterTrigger = fs->make<TH1F>("metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = fs->make<TH1F>("transverseMass", "transverseMass", 50, 0., 200.);
    hDeltaPhi = fs->make<TH1F>("deltaPhi", "deltaPhi", 60, 0., 180.);
    hAlphaT = fs->make<TH1F>("alphaT", "alphaT", 500, 0.0, 5.0);
    hAlphaTInvMass = fs->make<TH1F>("alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = fs->make<TH2F>("alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    hMet_AfterMETSelection = fs->make<TH1F>("met_AfterMETSelection", "met_AfterMETSelection", 150, 0.0, 300.0);
    hMet_AfterBTagging = fs->make<TH1F>("met_AfterBTagging", "met_AfterBTagging", 150, 0.0, 300.0);

  }

  SignalAnalysis::~SignalAnalysis() {}

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);
    
    if(!fTriggerSelection.analyze(iEvent, iSetup)) return;
    
    if(!fTriggerMETEmulation.analyze(iEvent, iSetup)) return;

    if(!fTauSelection.analyze(iEvent, iSetup)) return;

    if(!fJetSelection.analyze(iEvent, iSetup, fTauSelection.getSelectedTaus())) return;

    if(!fMETSelection.analyze(iEvent, iSetup)) return;
    hMet_AfterMETSelection->Fill(fMETSelection.fMet);

    if(!fBTagging.analyze(fJetSelection.getSelectedJets())) return;
    hMet_AfterBTagging->Fill(fMETSelection.fMet);

    if(!fEvtTopology.analyze(*(fTauSelection.getSelectedTaus()[0]), fJetSelection.getSelectedJets())) return;

    double deltaPhi = DeltaPhi::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3);

    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getSelectedTaus()[0]), *(fMETSelection.getSelectedMET()) );
    hTransverseMass->Fill(transverseMass);

    //  if(transverseMass < ftransverseMassCut ) return;
    //  increment(ftransverseMassCutCount);


    AlphaStruc sAlphaT = fEvtTopology.alphaT();
    hAlphaT->Fill(sAlphaT.fAlphaT);
    //std::cout << "fTauSelection.fRtau = " << fTauSelection.fRtau << std::endl;
    hAlphaTVsRtau->Fill(fTauSelection.fRtau, sAlphaT.fAlphaT);

    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
  }
}
