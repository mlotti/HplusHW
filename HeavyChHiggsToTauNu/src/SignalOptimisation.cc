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
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    /// Make TTree for SignalOptimisation
    myTree = fs->make<TTree>("HPlusSignalOptimisation","HPlusSignalOptimisation");
    /// Variables used for SignalOptimisation
    bTauIDStatus = new std::vector<bool>;
    myTree->Branch("bTauIDStatus", "std::vector<bool>", &bTauIDStatus);
    //
    fTauJetEt = new std::vector<float>;
    myTree->Branch("fTauJetEt", "std::vector<float>", &fTauJetEt);
    //
    fMET = new std::vector<float>;
    myTree->Branch("fMET", "std::vector<float>", &fMET);
    //
    iNHadronicJets = new std::vector<int>;
    myTree->Branch("iNHadronicJets", "std::vector<int>", &iNHadronicJets);
    //
    iNBtags = new std::vector<int>;
    myTree->Branch("iNBtags", "std::vector<int>", &iNBtags);
    //
    fGlobalMuonVetoHighestPt = new std::vector<float>;
    myTree->Branch("fGlobalMuonVetoHighestPt", "std::vector<float>", &fGlobalMuonVetoHighestPt);
    //
    fGlobalElectronVetoHighestPt = new std::vector<float>;
    myTree->Branch("fGlobalElectronVetoHighestPt", "std::vector<float>", &fGlobalElectronVetoHighestPt);
    //
    fTransverseMass = new std::vector<float>;
    myTree->Branch("fTransverseMass", "std::vector<float>", &fTransverseMass);
    //
    fDeltaPhi = new std::vector<float>;
    myTree->Branch("fDeltaPhi", "std::vector<float>", &fDeltaPhi);
    //
    fAlphaT = new std::vector<float>;
    myTree->Branch("fAlphaT", "std::vector<float>", &fAlphaT);
    
    // Book histograms filled in the analysis body
    hAlphaTInvMass = fs->make<TH1F>("alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    
  }

  SignalOptimisation::~SignalOptimisation() {}

  void SignalOptimisation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void SignalOptimisation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllCounter);
    /// Clear TTree vectors
    bTauIDStatus->clear();
    fTauJetEt->clear();
    fMET->clear();
    iNHadronicJets->clear();
    iNBtags->clear();
    fGlobalMuonVetoHighestPt->clear();
    fGlobalElectronVetoHighestPt->clear();
    fTransverseMass->clear();
    fDeltaPhi->clear();
    fAlphaT->clear();

    /// 1) Trigger
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return; /// no Trigger means no Tau => meaningless to continue.
    
    /// 2) Trigger Emulation (for MC data)
    TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup); 
    if(!triggerMETEmulationData.passedEvent()) return; /// I need to emulate the Data Trigger => to get DataSample of interest and optimise it.

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
    bool bEvtTopologyPass  = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets());
    // if(!bEvtTopologyPass) return;

    /// 8) GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup);
    if (!muonVetoData.passedEvent()) return; 

    /// 9) GlobalElectronVeto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    
    /// Create some variables
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    AlphaStruc sAlphaT = fEvtTopology.alphaT();
    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
    bool bDecision = triggerData.passedEvent() 
      * triggerMETEmulationData.passedEvent()
      * tauData.passedEvent()
      * jetData.passedEvent()
      * metData.passedEvent()
      * btagData.passedEvent()
      * bEvtTopologyPass;

    /// Fill Vectors for HPlusSignalOptimisation
    bTauIDStatus->push_back(tauData.passedEvent());
    fTauJetEt->push_back((float( (tauData.getSelectedTaus()[0])->pt())));
    fMET->push_back(metData.getSelectedMET()->et());
    iNHadronicJets->push_back(jetData.getHadronicJetCount());
    iNBtags->push_back(btagData.getBJetCount());
    fAlphaT->push_back(sAlphaT.fAlphaT);
    fGlobalMuonVetoHighestPt->push_back( muonVetoData.getSelectedMuonPt() );
    fGlobalElectronVetoHighestPt->push_back( electronVetoData.getSelectedElectronPt() );
    fTransverseMass->push_back(transverseMass);
    fDeltaPhi->push_back(deltaPhi);
    
    /// Fill TTree for HPlusSignalOptimisation
    myTree->Fill();

  }
}
