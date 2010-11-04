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
    
    /// Clear TTree vectors
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

    /// Trigger
    bool bTriggerSelection = fTriggerSelection.analyze(iEvent, iSetup);
    if(!bTriggerSelection) return;

    /// Trigger Emulation (for MC use to emulate the Data Trigger)
    bool bTriggerMETEmulationPass =  fTriggerMETEmulation.analyze(iEvent, iSetup);
    if(!bTriggerMETEmulationPass) return;

    /// MET: Only false if MET < MetCut. MetCut value is set to 0 => can use it.
    bool bMETSelectionPass = fMETSelection.analyze(iEvent, iSetup);
    if(!bMETSelectionPass) return;

    /// TauID
    bool bTauSelectionPass = fTauSelection.analyze(iEvent, iSetup);
    // if(!bTauSelectionPass) return;
    
    /// Jet Selection    
    bool bJetSelectionPass = fJetSelection.analyze(iEvent, iSetup, fTauSelection.getTau());
    // if(!bJetSelectionPass) return;
    
    /// BTagging
    bool bBTaggingPass = fBTagging.analyze(fJetSelection.getSelectedJets());
    // if(!bBTaggingPass) return;
   
    /// AlphaT
    bool bEvtTopologyPass  = fEvtTopology.analyze(*(fTauSelection.getTau()[0]), fJetSelection.getSelectedJets());
    // if(!bEvtTopologyPass) return;
    
    /// GlobalMuonVeto: Returns false if an isolated Muon is found in the event.
    bool bGlobalMuonVetoPass = fGlobalMuonVeto.analyze(iEvent, iSetup);
    // if(!bGlobalMuonVetoPass) return; 

    /// GlobalElectronVeto: Returns false if an isolated Electron is found in the event.
    bool bGlobalElectronVetoPass = fGlobalElectronVeto.analyze(iEvent, iSetup); 
    // bool bGlobalElectronVetoPass = fGlobalElectronVeto.analyzeCustomElecID(iEvent, iSetup);
    // if(!bGlobalElectronVetoPass) return;

    /// Create some variables
    double deltaPhi = DeltaPhi::reconstruct(*(fTauSelection.getTau()[0]), *(fMETSelection.getSelectedMET()));

    double transverseMass = TransverseMass::reconstruct(*(fTauSelection.getTau()[0]), *(fMETSelection.getSelectedMET()) );

    AlphaStruc sAlphaT = fEvtTopology.alphaT();

    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }

    /// Assign values to TTree variables.
    bTauIDStatus = bTauSelectionPass;
    fTauJetEt = float(fTauSelection.getTau()[0]->pt());
    fTauJetEta = (float( (fTauSelection.getTau()[0])->eta()));
    fMET = fMETSelection.fMet;
    iNHadronicJets = fJetSelection.iNHadronicJets;
    iNBtags = fBTagging.iNBtags;
    fAlphaT = sAlphaT.fAlphaT;
    fGlobalMuonVetoHighestPt = fGlobalMuonVeto.getSelectedMuonsPt();
    fGlobalElectronVetoHighestPt = fGlobalElectronVeto.getSelectedElectronsPt();
    fTransverseMass = transverseMass;
    fDeltaPhi = deltaPhi;

    /// Fill TTree for HPlusSignalOptimisation
    myTree->Fill();

  }
}
