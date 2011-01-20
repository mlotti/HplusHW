#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementSignalSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurementSignalSelection::QCDMeasurementSignalSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    // fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger & HLT MET cut")),
    fTriggerEmulationCounter(eventCounter.addCounter("Trigger Emulation cut")),
    fTauSelectionCounter(eventCounter.addCounter("Tau selection")),
    fJetSelectionCounter(eventCounter.addCounter("Jet selection")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("Global electron veto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("Global muon veto")),
    fMETCounter(eventCounter.addCounter("MET cut")),
    fBTaggingCounter(eventCounter.addCounter("B-tagging cut")),
    fFakeMETVetoCounter(eventCounter.addCounter("fakeMET veto")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter, eventWeight),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    // fTauSelectionFactorized(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, fTauSelection),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight)//,
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    // fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight)

   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  }

  QCDMeasurementSignalSelection::~QCDMeasurementSignalSelection() {}

  void QCDMeasurementSignalSelection::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurementSignalSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);

    increment(fAllCounter);

    // Trigger
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);
         
    // Trigger Emulation (for MC data)
    TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup); 
    if(!triggerMETEmulationData.passedEvent()) return;
    increment(fTriggerEmulationCounter);

    // Apply Isolation Veto to taus
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return; // No tau found!
    increment(fTauSelectionCounter);
    
    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return; // after tauID. Note: jets close to tau-Jet in eta-phi space are removed from jet list.
    increment(fJetSelectionCounter);
   
    // GlobalElectronVeto
    // GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);

    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    
    // MET 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    if(!metData.passedEvent()) return;
    increment(fMETCounter);
    
    // BTagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);

    // FakeMETVeto
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    
  }
}
