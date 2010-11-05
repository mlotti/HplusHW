#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    ftransverseMassCut(iConfig.getUntrackedParameter<double>("transverseMassCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight)
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
    hMet_AfterTauSelection = fs->make<TH1F>("met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 300.0);
    hMet_AfterBTagging = fs->make<TH1F>("met_AfterBTagging", "met_AfterBTagging", 100, 0.0, 300.0);
    hMetBeforeEmul = fs->make<TH1F>("MetBeforeEmul", "MetBeforeEmul", 100, 0.0, 300.0);
    hMetBeforeTrigger = fs->make<TH1F>("MetBeforeTrigger", "MetBeforeTrigger", 100, 0.0, 300.0);
    hMetAfterTrigger = fs->make<TH1F>("MetAfterTrigger", "MetAfterTrigger", 100, 0.0, 300.0);
  }

  SignalAnalysis::~SignalAnalysis() { }

  void SignalAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale
    
    increment(fAllCounter);
    
    //    if(!fTriggerSelection.analyze(iEvent, iSetup)) return;
    
    //    if(!fTriggerMETEmulation.analyze(iEvent, iSetup)) return;

    //    if(fGlobalMuonVeto.analyze(iEvent, iSetup)) return;

    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup); // just to obtain the MET value

    // If factorization is applied to tauID, apply it here
    // fEventWeight.multiplyWeight(factorizationWeight); 

    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return;

    hMet_AfterTauSelection->Fill(metData.getSelectedMET()->et());


    /////////////////////////////////////
    // test
    hMetBeforeEmul->Fill(metData.getSelectedMET()->et());
    
    TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup); 
    if(!triggerMETEmulationData.passedEvent()) return;
    
    hMetBeforeTrigger->Fill(metData.getSelectedMET()->et());
    
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    
    hMetAfterTrigger->Fill(metData.getSelectedMET()->et());
/* FIXME/5.11.2010/SL
    // Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
*/
    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 

    // MET cut
    if(!metData.passedEvent()) return;

    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return;

    // b tagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return;
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et());
 
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());

    // Alpha T
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return;

    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3);

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    hTransverseMass->Fill(transverseMass);

    //  if(transverseMass < ftransverseMassCut ) return;
    //  increment(ftransverseMassCutCount);

    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    hAlphaT->Fill(sAlphaT.fAlphaT); // FIXME: move this histogramming to evt topology

    // The following code is not correct, because there could be more than one tau jet
    // passing the tau ID (and hence multiple values of Rtau
    // Please access the selected tau jets via  tauData.getSelectedTaus()
    //std::cout << "tauData.Rtau = " << tauData.Rtau << std::endl;
    //hAlphaTVsRtau->Fill(tauData.Rtau, sAlphaT.fAlphaT);

    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
  }
}
