#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalOptimisation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalOptimisation::SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
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
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter)
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    /// Make TTree for SignalOptimisation
    myTree = fs->make<TTree>("HPlusSignalOptimisation","HPlusSignalOptimisation");
    
    /// Variables used for SignalOptimisation
    bTauIDStatus = new std::vector<bool>;
    myTree->Branch("bTauIDStatus", "std::vector<bool>", &bTauIDStatus);
    
    fTauJetEt = new std::vector<float>;
    myTree->Branch("fTauJetEt", "std::vector<float>", &fTauJetEt);

    fTauJetEta = new std::vector<float>;
    myTree->Branch("fTauJetEta", "std::vector<float>", &fTauJetEta);
    
    fMET = new std::vector<float>;
    myTree->Branch("fMET", "std::vector<float>", &fMET);
    
    iNHadronicJets = new std::vector<int>;
    myTree->Branch("iNHadronicJets", "std::vector<int>", &iNHadronicJets);
    
    iNBtags = new std::vector<int>;
    myTree->Branch("iNBtags", "std::vector<int>", &iNBtags);
    
    fGlobalMuonVetoHighestPt = new std::vector<float>;
    myTree->Branch("fGlobalMuonVetoHighestPt", "std::vector<float>", &fGlobalMuonVetoHighestPt);
    
    fGlobalElectronVetoHighestPt = new std::vector<float>;
    myTree->Branch("fGlobalElectronVetoHighestPt", "std::vector<float>", &fGlobalElectronVetoHighestPt);
    
    fTransverseMass = new std::vector<float>;
    myTree->Branch("fTransverseMass", "std::vector<float>", &fTransverseMass);
    
    fDeltaPhi = new std::vector<float>;
    myTree->Branch("fDeltaPhi", "std::vector<float>", &fDeltaPhi);
    
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
    // Reserve size
    bTauIDStatus->reserve(1);
    fTauJetEt->reserve(1);
    fTauJetEta->reserve(1);
    fMET->reserve(1);
    iNHadronicJets->reserve(1);
    iNBtags->reserve(1);
    fGlobalMuonVetoHighestPt->reserve(1);
    fGlobalElectronVetoHighestPt->reserve(1);
    fTransverseMass->reserve(1);
    fDeltaPhi->reserve(1);
    fAlphaT->reserve(1);

    /// Trigger
    bool bTriggerSelection = fTriggerSelection.analyze(iEvent, iSetup);
    if(!bTriggerSelection) return;

    /// Trigger Emulation (for MC use to emulate the Data Trigger)
    bool bTriggerMETEmulationPass =  fTriggerMETEmulation.analyze(iEvent, iSetup);
    if(!bTriggerMETEmulationPass) return;

    /// MET: Only false if MET < MetCut. MetCut value is set to 0 => can use it.
    bool bMETSelectionPass = fMETSelection.analyze(iEvent, iSetup);
    // if(!bMETSelectionPass) return;

    /// TauID
    bool bTauSelectionPass = fTauSelection.analyze(iEvent, iSetup);
    if(!bTauSelectionPass) return;
    
    /// Jet Selection    
    bool bJetSelectionPass = fJetSelection.analyze(iEvent, iSetup, fTauSelection.getTau());
    // if(!bJetSelectionPass) return;
    
    /// BTagging
    bool bBTaggingPass = fBTagging.analyze(fJetSelection.getSelectedJets());
    // if(!bBTaggingPass) return;
   
    /// AlphaT
    bool bEvtTopologyPass  = fEvtTopology.analyze(*(fTauSelection.getSelectedTaus()[0]), fJetSelection.getSelectedJets());
    // if(!bEvtTopologyPass) return;
    
    /// GlobalMuonVeto: Returns false if an isolated Muon is found in the event.
    bool bGlobalMuonVetoPass = fGlobalMuonVeto.analyze(iEvent, iSetup);
    // if(!bGlobalMuonVetoPass) return; 

    /// GlobalElectronVeto: Returns false if an isolated Electron is found in the event.
    bool bGlobalElectronVetoPass = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // if(!bGlobalElectronVetoPass) return;

    /// Create some variables
    double deltaPhi = DeltaPhi::reconstruct(*(fTauSelection.getTau()[0]), *(fMETSelection.getSelectedMET()));
    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getTau()[0]), *(fMETSelection.getSelectedMET()) );
    AlphaStruc sAlphaT = fEvtTopology.alphaT();
    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }
    bool bDecision = bTriggerSelection*bTriggerMETEmulationPass*bTauSelectionPass*bJetSelectionPass*bMETSelectionPass*bBTaggingPass*bEvtTopologyPass;

    /// Fill Vectors for HPlusSignalOptimisation
    bTauIDStatus->push_back(bTauSelectionPass);
    fTauJetEt->push_back((float( (fTauSelection.getTau()[0])->pt())));
    fTauJetEta->push_back((float( (fTauSelection.getTau()[0])->eta())));
    fMET->push_back(fMETSelection.fMet);
    iNHadronicJets->push_back(fJetSelection.iNHadronicJets);
    iNBtags->push_back(fBTagging.iNBtags);
    fAlphaT->push_back(sAlphaT.fAlphaT);
    fGlobalMuonVetoHighestPt->push_back( fGlobalMuonVeto.getSelectedMuonsPt() );
    fGlobalElectronVetoHighestPt->push_back( fGlobalElectronVeto.getSelectedElectronsPt() );
    fTransverseMass->push_back(transverseMass);
    fDeltaPhi->push_back(deltaPhi);
    // */

    /// Fill TTree for HPlusSignalOptimisation
    myTree->Fill();

  }
}
