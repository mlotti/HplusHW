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
    fAllCounter(eventCounter.addCounter("All events")),
    fEventWeight(eventWeight),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    /// Make TTree for SignalOptimisation
    myTree = fs->make<TTree>("HPlusSignalOptimisation","HPlusSignalOptimisation");
    
    /// Variables used for SignalOptimisation
    myTree->Branch("bTauIDStatus", &bTauIDStatus);
    myTree->Branch("fTauJetEt",  &fTauJetEt);
    myTree->Branch("fTauJetEta", &fTauJetEta);
    myTree->Branch("fMET", &fMET);
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
    iNHadronicJets = -5.0;
    iNBtags = -5.0;
    fGlobalMuonVetoHighestPt = -5.0;
    fGlobalElectronVetoHighestPt = -5.0;
    fTransverseMass = -5.0;
    fDeltaPhi = -5.0;
    fAlphaT = -5.0;

    /// 1) Trigger
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return; /// no Trigger means no Tau => meaningless to continue.
        
    /// 2) Trigger Emulation (for MC data)
    TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup); 
    if(!triggerMETEmulationData.passedEvent()) return; /// I need to emulate the Data Trigger => to get DataSample of interest and optimise it

    /// 3) tauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return; /// without tau-Jet meaningless to compute Mt, deltaPhi, or alphaT.
    
    /// 4) MET 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //if(!metData.passedEvent()) return;

    /// 5) Jet Selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    //if(!jetData.passedEvent()) return; /// after tauID. Note: jets close to tau-Jet in eta-phi space are removed from jet list.
    
    /// 6) BTagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    //if(!btagData.passedEvent()) return;

    /// 7) AlphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return;

    /// 8) GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 

    /// 9) GlobalElectronVeto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    
    /// Create some variables
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
    bool bDecision = triggerData.passedEvent() 
      * triggerMETEmulationData.passedEvent()
      * tauData.passedEvent()
      * jetData.passedEvent()
      * metData.passedEvent()
      * btagData.passedEvent()
      * evtTopologyData.passedEvent();

    /// Fill Vectors for HPlusSignalOptimisation
    bTauIDStatus = tauData.passedEvent();
    fTauJetEt = static_cast<float>((tauData.getSelectedTaus()[0])->pt());
    fTauJetEt = static_cast<float>((tauData.getSelectedTaus()[0])->eta());
    fMET = metData.getSelectedMET()->et();
    iNHadronicJets = jetData.getHadronicJetCount();
    iNBtags = btagData.getBJetCount();
    fGlobalMuonVetoHighestPt = muonVetoData.getSelectedMuonPt();
    fGlobalElectronVetoHighestPt = electronVetoData.getSelectedElectronPt();
    fTransverseMass = transverseMass;
    fDeltaPhi = deltaPhi;
    fAlphaT = sAlphaT.fAlphaT;
    
    /// Fill TTree for HPlusSignalOptimisation
    myTree->Fill();
  }
}
