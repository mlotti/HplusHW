#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementFromAntiTauControlRegion.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurementFromAntiTauControlRegion::QCDMeasurementFromAntiTauControlRegion(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    //fTriggerEmulationCounter(eventCounter.addCounter("TriggerMETEmulation")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("tauSelection")),
    fJetSelectionCounter(eventCounter.addCounter("jetSelection")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
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
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight)//,
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    // fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight)

   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms 
    hMETAfterWholeSelection = fs->make<TH1F>("METAfterWholeSelection", "MET after whole selection;MET, GeV;N/2 GeV", 250, 0, 500);
    //aa    hTriggerPrescales = fs->make<TH1F>("TriggerPrescales", "TriggerPrescales", 4000, -0.5, 3999.5);    
    //aa    hTriggerPrescales_test = fs->make<TH1F>("TriggerPrescales", "TriggerPrescales", 4000, -0.5, 3999.5);    
   }

  QCDMeasurementFromAntiTauControlRegion::~QCDMeasurementFromAntiTauControlRegion() {}

  void QCDMeasurementFromAntiTauControlRegion::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurementFromAntiTauControlRegion::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    //aa    double TriggerPrescale = fEventWeight.getWeight();
    
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
    
    // GlobalElectronVeto
    // GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);

    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    
    // Obtain MET, btagging and fake MET veto data objects
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedAntiTau, jetData.getSelectedJets());
    
    // Fill additional counters before dropping events because of MET cut
    if (btagData.passedEvent() && fakeMETData.passedEvent()) {
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

    // MET 
    if(!metData.passedEvent()) return;
    increment(fMETCounter);
    
    // BTagging
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);

    // FakeMETVeto
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
   
    // Fill a histogram with the Trigger Prescales used
    // aa   hTriggerPrescales->Fill(TriggerPrescale);
    // aa   hTriggerPrescales_test->Fill(TriggerPrescale, TriggerPrescale);
    // aa   std::cout << "TriggerPrescale = " << TriggerPrescale << std::endl;
  }
}
