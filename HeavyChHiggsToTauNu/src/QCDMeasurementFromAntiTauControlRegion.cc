#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementFromAntiTauControlRegion.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurementFromAntiTauControlRegion::QCDMeasurementFromAntiTauControlRegion(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger_and_HLT_MET_cut")),
    // fTriggerEmulationCounter(eventCounter.addCounter("TriggerMETEmulation")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("tauSelection")),
    fJetSelectionCounter(eventCounter.addCounter("jetSelection")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fInvMassVetoOnJetsCounter(eventCounter.addCounter("InvMassVetoOnJets")),
    fFakeMETVetoCounter(eventCounter.addCounter("fakeMETVeto")),
    fMETgt0AfterWholeSelectionCounter(eventCounter.addCounter("METgt0AfterWholeSelection")),
    fMETgt30AfterWholeSelectionCounter(eventCounter.addCounter("METgt30AfterWholeSelection")),
    fMETgt40AfterWholeSelectionCounter(eventCounter.addCounter("METgt40AfterWholeSelection")),
    fMETgt50AfterWholeSelectionCounter(eventCounter.addCounter("METgt50AfterWholeSelection")),
    fMETgt60AfterWholeSelectionCounter(eventCounter.addCounter("METgt60AfterWholeSelection")),
    fMETgt70AfterWholeSelectionCounter(eventCounter.addCounter("METgt70AfterWholeSelection")),
    fMETgt80AfterWholeSelectionCounter(eventCounter.addCounter("METgt80AfterWholeSelection")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight)
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),

   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms 
    hMETAfterWholeSelection = fs->make<TH1F>("METAfterWholeSelection", "MET after whole selection;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterWholeSelectionButInvMassVeto = fs->make<TH1F>("METAfterWholeSelectionButInvMassVeto", "MET after whole selection no InvMassVeto);MET, GeV;N/2 GeV", 250, 0, 500);

   }

  QCDMeasurementFromAntiTauControlRegion::~QCDMeasurementFromAntiTauControlRegion() {}

  void QCDMeasurementFromAntiTauControlRegion::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurementFromAntiTauControlRegion::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);

    increment(fAllCounter);
    // Trigger and HLT_MET cut
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);

    // Trigger Emulation (for MC & Data)
    // Not needed: HLT_MET cut is applied already in trigger step 
    //TriggerTauMETEmulation::Data triggerMETEmulationData = fTriggerTauMETEmulation.analyze(iEvent, iSetup); 
    //if(!triggerMETEmulationData.passedEvent()) return;
    //increment(fTriggerEmulationCounter);
    //Trigger emulation done in trigger

    // Apply Isolation Veto to taus
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return; // At least one tau candidate was found which was isolated.
    increment(fOneProngTauSelectionCounter);
    edm::PtrVector<pat::Tau> mySelectedAntiTau;
    mySelectedAntiTau.push_back(tauData.getSelectedTaus()[0]);

    // Clean jet collection from selected tau and apply NJets>=3 cut
    // JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus());
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedAntiTau);
    if(!jetData.passedEvent()) return; // after tauID. Note: jets close to tau-Jet in eta-phi space are removed from jet list.
    increment(fJetSelectionCounter);

    // Run alphaT plots just for reference (will not affect the method in any way)
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets());     
    
    // GlobalElectronVeto
    // GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);

    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    // fGlobalMuonVeto.debug();

    // Obtain MET, btagging, "InvMass Veto On Jets" and "fake MET veto" data objects
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedAntiTau, jetData.getSelectedJets());
    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
  
    // Fill additional counters before dropping events because of MET cut
    if ( btagData.passedEvent() && invMassVetoOnJetsData.passedEvent() && fakeMETData.passedEvent() ) {
      double myMETValue = metData.getSelectedMET()->et();
      if (myMETValue > 0)
        increment(fMETgt0AfterWholeSelectionCounter);
      if (myMETValue > 30)
        increment(fMETgt30AfterWholeSelectionCounter);
      if (myMETValue > 40)
        increment(fMETgt40AfterWholeSelectionCounter);
      if (myMETValue > 50)
        increment(fMETgt50AfterWholeSelectionCounter);
      if (myMETValue > 60)
        increment(fMETgt60AfterWholeSelectionCounter);
      if (myMETValue > 70)
        increment(fMETgt70AfterWholeSelectionCounter);
      if (myMETValue > 80)
        increment(fMETgt80AfterWholeSelectionCounter);
      // Fill histogram of MET distribution of selected events (needed for MET extrapolation)
      hMETAfterWholeSelection->Fill(myMETValue, fEventWeight.getWeight());
    }

    // Fill additional counters before dropping events because of MET cut - No InvMassVeto
    if ( btagData.passedEvent() && fakeMETData.passedEvent() ) {
      double myMETValue = metData.getSelectedMET()->et();
      hMETAfterWholeSelectionButInvMassVeto->Fill(myMETValue, fEventWeight.getWeight());
    }
    
    // MET 
    if(!metData.passedEvent()) return;
    increment(fMETCounter);
    
    // BTagging
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);

    // InvMassVeto: Apply InvMassVeto to reject events with W->qq and t->bW. Anticipated to increase QCD Purity
    if(!invMassVetoOnJetsData.passedEvent()) return; 
    increment(fInvMassVetoOnJetsCounter);

    // FakeMETVeto
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);

  }
}
