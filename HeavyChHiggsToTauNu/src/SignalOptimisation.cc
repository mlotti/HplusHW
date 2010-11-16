#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalOptimisation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalOptimisation::SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    ftransverseMassCut(iConfig.getUntrackedParameter<double>("transverseMassCut")),
    bUseFactorizedTauID(iConfig.getUntrackedParameter<bool>("useFactorizedTauID")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger & HLT MET Cut")),
    fTriggerEmulationCounter(eventCounter.addCounter("Trigger Emulation")),
    fClobalMuonVetoCounter(eventCounter.addCounter("Global Muon Veto")),
    fClobalElectronVetoCounter(eventCounter.addCounter("Global Electron Veto")),
    fTauSelectionCounter(eventCounter.addCounter("Tau selection")),
    fMETCounter(eventCounter.addCounter("MET")),
    fJetSelectionCounter(eventCounter.addCounter("Jet Selection")),
    fBTaggingCounter(eventCounter.addCounter("BTagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("Fake MET Veto")),
    fEvtTopologyCounter(eventCounter.addCounter("Evt Topology")),
    fEventWeight(eventWeight),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fTauSelectionFactorized(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, fTauSelection),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Make TTree for SignalOptimisation
    myTree = fs->make<TTree>("HPlusSignalOptimisation","HPlusSignalOptimisation");
    
    // Variables used for SignalOptimisation
    myTree->Branch("bTauIDStatus", &bTauIDStatus);
    myTree->Branch("fTauJetEt",  &fTauJetEt);
    myTree->Branch("fTauJetEta", &fTauJetEta);
    myTree->Branch("fMET", &fMET);
    myTree->Branch("fFakeMETDeltaR", &fFakeMETDeltaR);
    myTree->Branch("iNHadronicJets", &iNHadronicJets);
    myTree->Branch("iNBtags", &iNBtags);
    myTree->Branch("fGlobalMuonVetoHighestPt", &fGlobalMuonVetoHighestPt);
    myTree->Branch("fGlobalElectronVetoHighestPt", &fGlobalElectronVetoHighestPt);
    myTree->Branch("fTransverseMass", &fTransverseMass);
    myTree->Branch("fDeltaPhi",  &fDeltaPhi);
    myTree->Branch("fAlphaT", &fAlphaT);
    
    // Book histograms filled in the analysis body
    hAlphaTInvMass = fs->make<TH1F>("alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    
  }

  SignalOptimisation::~SignalOptimisation() {}

  void SignalOptimisation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalOptimisation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);
    
    // Reset variables
    bTauIDStatus = -5.0;
    fTauJetEt = -5.0;
    fTauJetEta = -999.99;
    fMET = -5.0;
    fFakeMETDeltaR = -5.0;
    iNHadronicJets = -5.0;
    iNBtags = -5.0;
    fGlobalMuonVetoHighestPt = -5.0;
    fGlobalElectronVetoHighestPt = -5.0;
    fTransverseMass = -5.0;
    fDeltaPhi = -5.0;
    fAlphaT = -5.0;

    // 1) Trigger
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);
         
    // 2) Trigger Emulation (for MC data)
    TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup); 
    if(!triggerMETEmulationData.passedEvent()) return;
    increment(fTriggerEmulationCounter);
    
    // 3) GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 
    increment(fClobalMuonVetoCounter);
    
    // 4) GlobalElectronVeto
    // GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fClobalElectronVetoCounter);

    // 5) tauID
    // TauID (with optional factorization (recommended only for data and QCD))
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if (bUseFactorizedTauID) { // Returns 0 or 1 tau; see TauSelectionFactorized.cc for details
      TauSelectionFactorized::Data factorizedTauData = fTauSelectionFactorized.analyze(iEvent, iSetup);
      tauData = factorizedTauData.tauSelectionData(); // Update tau data object with tau data object from factorization
      fEventWeight.multiplyWeight(factorizedTauData.factorizationCoefficient()); // Apply event weight
    }
    if(!tauData.passedEvent()) return; // No tau found!
    increment(fTauSelectionCounter);
    
    // 6) MET 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //if(!metData.passedEvent()) return;
    increment(fMETCounter);

    // 7) Jet Selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    //if(!jetData.passedEvent()) return; // after tauID. Note: jets close to tau-Jet in eta-phi space are removed from jet list.
    increment(fJetSelectionCounter);
    
    // 8) BTagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    //if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);

    // 9) FakeMETVeto
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    // if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    
    // 10) AlphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return;
    increment(fEvtTopologyCounter);
     
    // Create some variables
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
    // bool bDecision = triggerData.passedEvent() * triggerMETEmulationData.passedEvent() * tauData.passedEvent() * jetData.passedEvent() * metData.passedEvent() * btagData.passedEvent() * evtTopologyData.passedEvent();

    // Fill Vectors for HPlusSignalOptimisation
    bTauIDStatus = tauData.passedEvent();
    fTauJetEt  = static_cast<float>( (tauData.getSelectedTaus()[0])->pt() );
    fTauJetEta = static_cast<float>( (tauData.getSelectedTaus()[0])->eta() );
    fMET = metData.getSelectedMET()->et();
    fFakeMETDeltaR = fakeMETData.closestDeltaR();
    iNHadronicJets = jetData.getHadronicJetCount();
    iNBtags = btagData.getBJetCount();
    fGlobalMuonVetoHighestPt = muonVetoData.getSelectedMuonPt();
    fGlobalElectronVetoHighestPt = electronVetoData.getSelectedElectronPt();
    fTransverseMass = transverseMass;
    fDeltaPhi = deltaPhi;
    fAlphaT = sAlphaT.fAlphaT;
    
    // Fill TTree for HPlusSignalOptimisation
    myTree->Fill();
  }
}
