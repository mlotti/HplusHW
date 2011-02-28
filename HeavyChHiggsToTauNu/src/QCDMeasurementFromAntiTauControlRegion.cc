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
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("TauSelection")),
    fJetSelectionCounter(eventCounter.addCounter("JetSelection")),
    fInvMassVetoOnJetsCounter(eventCounter.addCounter("InvMassVetoOnJets")),    
    fEvtTopologyCounter(eventCounter.addCounter("EvtTopology")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),
    fMETgt0AfterWholeSelectionCounter(eventCounter.addCounter("METgt0AfterWholeSelection")),
    fMETgt30AfterWholeSelectionCounter(eventCounter.addCounter("METgt30AfterWholeSelection")),
    fMETgt40AfterWholeSelectionCounter(eventCounter.addCounter("METgt40AfterWholeSelection")),
    fMETgt50AfterWholeSelectionCounter(eventCounter.addCounter("METgt50AfterWholeSelection")),
    fMETgt60AfterWholeSelectionCounter(eventCounter.addCounter("METgt60AfterWholeSelection")),
    fMETgt70AfterWholeSelectionCounter(eventCounter.addCounter("METgt70AfterWholeSelection")),
    fMETgt80AfterWholeSelectionCounter(eventCounter.addCounter("METgt80AfterWholeSelection")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    //fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight)
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),

   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms 
    hMETAfterTrigger           = fs->make<TH1F>("METAfterTrigger", "MET after Trigger;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterTrigger->Sumw2();
    hMETAfterElectronVeto      = fs->make<TH1F>("METAfterElectronVeto", "MET after Electron Veto;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterElectronVeto->Sumw2();
    hMETAfterMuonVeto          = fs->make<TH1F>("METAfterMuonVeto", "MET after Muon Veto;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterMuonVeto->Sumw2();
    hMETAfterTauSelection      = fs->make<TH1F>("METAfterTauSelection", "MET after Tau Selection;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterTauSelection->Sumw2();
    hMETAfterJetSelection      = fs->make<TH1F>("METAfterJetSelection", "MET after Jet Selection;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterJetSelection->Sumw2();
    hMETAfterInvMassVetoOnJets = fs->make<TH1F>("METAfterInvMassVetoOnJets", "MET after InvMass Veto On Jets;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterInvMassVetoOnJets->Sumw2();
    hMETAfterMET               = fs->make<TH1F>("METAfterMET", "MET after MET cut;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterMET->Sumw2();
    hMETAfterBTagging          = fs->make<TH1F>("METAfterBTagging", "MET after b-tagging;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterBTagging->Sumw2();
    hMETAfterFakeMetVeto       = fs->make<TH1F>("METAfterFakeMetVeto", "MET after fake MET Veto;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterFakeMetVeto->Sumw2();
    hMETAfterWholeSelection    = fs->make<TH1F>("METAfterWholeSelection", "MET after whole selection;MET, GeV;N/2 GeV", 250, 0, 500);
    hMETAfterWholeSelection->Sumw2();
    hRTauAfterAllSelectionsExceptMETandFakeMetVeto = fs->make<TH1F>("RTauAfterAllSelectionsExceptMETAndFakeMETVeto", "RTauAfterAllSelectionsExceptMETAndFakeMETVeto;Rtau;N_{events}/0.02", 60, 0., 1.2);
    hRTauAfterAllSelectionsExceptMETandFakeMetVeto->Sumw2();
    hRTauAfterAllSelections = fs->make<TH1F>("RTauAfterAllSelections", "RTauAfterAllSelections;Rtau;N_{events}/0.02", 60, 0., 1.2);;
    hRTauAfterAllSelections->Sumw2();
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

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);

    // Get MET for histo-plotting purposes
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    hMETAfterTrigger->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // GlobalElectronVeto 
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);
    hMETAfterElectronVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    hMETAfterMuonVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // Apply tau-Selection (available: antitautag, antiisolation, standard)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    edm::PtrVector<pat::Tau> mySelectedAntiTau;
    mySelectedAntiTau.push_back(tauData.getSelectedTaus()[0]);
    hMETAfterTauSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedAntiTau);
    if(!jetData.passedEvent()) return; // Note: jets close to tau-Jet in eta-phi space are removed from jet list.
    increment(fJetSelectionCounter);
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Run alphaT plots just for reference (will NOT affect the method in any way)
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets());     

    // InvMassVeto: Apply InvMassVeto to reject events with W->qq and t->bW. Anticipated to increase QCD Purity
    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
    if(!invMassVetoOnJetsData.passedEvent()) return; 
    increment(fInvMassVetoOnJetsCounter);
    hMETAfterInvMassVetoOnJets->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // Obtain MET, btagging, "InvMass Veto On Jets" and "fake MET veto" data objects
    //METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedAntiTau, jetData.getSelectedJets());

    
    // Fill additional counters before dropping events because of MET cut
    if ( btagData.passedEvent() && fakeMETData.passedEvent() ) {
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

    if(btagData.passedEvent())
      hRTauAfterAllSelectionsExceptMETandFakeMetVeto->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());

    // MET 
    if(!metData.passedEvent()) return;
    increment(fMETCounter);
    hMETAfterMET->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // BTagging
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);
    hMETAfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // FakeMETVeto
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    hMETAfterFakeMetVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    hRTauAfterAllSelections->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
  }
}
