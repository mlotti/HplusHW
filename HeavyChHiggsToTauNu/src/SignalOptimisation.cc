#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalOptimisation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalOptimisation::SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    // fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    ftransverseMassCut(iConfig.getUntrackedParameter<double>("transverseMassCut")),
    fAllCounter(eventCounter.addCounter("All Events")),
    fTriggerCounter(eventCounter.addCounter("Trigger Counter")),
    fPrimaryVertexCounter(eventCounter.addCounter("Primary vertex")),
    fTausExistCounter(eventCounter.addCounter("Taus > 0")),
    fOneTauCounter(eventCounter.addCounter("Taus == 1")),
    fElectronVetoCounter(eventCounter.addCounter("Electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("Muon veto")),
    fMETCounter(eventCounter.addCounter("MET")),
    fNJetsCounter(eventCounter.addCounter("NJets")),
    fBTaggingCounter(eventCounter.addCounter("Btagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("Fake MET veto")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    ftransverseMassCutCounter(eventCounter.addCounter("TransverseMass Cut")),
    fEvtTopologyCounter(eventCounter.addCounter("Evt Topology")),
    fZmassVetoCounter(eventCounter.addCounter("Z Mass Veto")),
    fEventWeight(eventWeight),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1, "tauID"),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight"))//,
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
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
    myTree->Branch("fFakeMETDeltaPhi", &fFakeMETDeltaPhi);
    myTree->Branch("iNHadronicJets", &iNHadronicJets);
    myTree->Branch("iNHadronicJetsInFwdDir", &iNHadronicJetsInFwdDir);
    myTree->Branch("iNBtags", &iNBtags);
    myTree->Branch("fGlobalMuonVetoHighestPt", &fGlobalMuonVetoHighestPt);
    myTree->Branch("fGlobalElectronVetoHighestPt", &fGlobalElectronVetoHighestPt);
    myTree->Branch("fTransverseMass", &fTransverseMass);
    myTree->Branch("fAlphaT", &fAlphaT);
    myTree->Branch("fHt", &fHt);
    myTree->Branch("fJt", &fJt);

    // Book histograms filled in the analysis body
    hAlphaTInvMass = makeTH<TH1F>(*fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    
  }

  SignalOptimisation::~SignalOptimisation() {}

  // void SignalOptimisation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // analyze(iEvent, iSetup);
  // }
  bool SignalOptimisation::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    return analyze(iEvent, iSetup);
  }

  // void SignalOptimisation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  bool SignalOptimisation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale for Real Data triggers

    // Reset variables
    bTauIDStatus = 0;
    fTauJetEt = -5.0;
    fTauJetEta = -999.99;
    fMET = -5.0;
    fFakeMETDeltaPhi = -5.0;
    iNHadronicJets = -5.0;
    iNHadronicJetsInFwdDir = -5.0;
    iNBtags = -5.0;
    fGlobalMuonVetoHighestPt = -5.0;
    fGlobalElectronVetoHighestPt = -5.0;
    fTransverseMass = -5.0;
    fAlphaT = -5.0;
    fHt = -5.0;
    fJt = -5.0;
    

    // 1) Vertex Re-Weight (PU spectrum correction)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData())
      fEventWeight.multiplyWeight(weightSize.first);
    
    // // GenParticle analysis
    // if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    // Start the general counter (after Vertex re-weighting)
    increment(fAllCounter);
    

    // 2) Apply trigger and HLT_MET cut (Only if REAL Data)
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (iEvent.isRealData()) {
      if(!triggerData.passedEvent()) return false;   // Trigger is applied only if the data sample is real data
    }
    increment(fTriggerCounter);


    // 3) Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    

    // 4) TauID (with optional factorization)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    increment(fTausExistCounter);
    if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
    bTauIDStatus = 1;
    increment(fOneTauCounter);
    // Get Tau-related variables
    fTauJetEt  = static_cast<float>( (tauData.getSelectedTaus()[0])->pt() );
    fTauJetEta = static_cast<float>( (tauData.getSelectedTaus()[0])->eta() );


    // 5) Get MET object and apply pre-MET cut to see if MC Normalization is better.
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    // if(metData.getSelectedMET()->et() < 30 ) return false;
	

    // 6) Trigger efficiency
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(tauData.getSelectedTaus()[0]), *metData.getSelectedMET());
    if (!iEvent.isRealData() ) {
      fEventWeight.multiplyWeight(triggerEfficiency); // Apply trigger efficiency as weight for simulated events
    }


    // SignalOptimisation will be performed from this point on. Henceforth no cut will be applied!
    // -----> No CUTS <----- (start)

    // MET
    // if(!metData.passedEvent()) return false;
    fMET = metData.getSelectedMET()->et();
    

    // Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // if (!electronVetoData.passedEvent()) return false;
    // increment(fElectronVetoCounter);
    fGlobalElectronVetoHighestPt = electronVetoData.getSelectedElectronPt();


    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    // if (!muonVetoData.passedEvent()) return false;
    // increment(fMuonVetoCounter);
    fGlobalMuonVetoHighestPt = muonVetoData.getSelectedMuonPt();
 

    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    // if(!jetData.passedEvent()) return false;
    // increment(fNJetsCounter);
    iNHadronicJets = jetData.getHadronicJetCount();   
    iNHadronicJetsInFwdDir = jetData.getHadronicJetCountInFwdDir();
    

    // b-tagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    // if(!btagData.passedEvent()) return false;
    // increment(fBTaggingCounter);    
    iNBtags = btagData.getBJetCount();
    
    
    // Fake MET veto a.k.a. further QCD suppression
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    // if (!fakeMETData.passedEvent()) return false;
    // increment(fFakeMETVetoCounter);
    fFakeMETDeltaPhi = fakeMETData.closestDeltaPhi();


    // Alpha T
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    // if(!evtTopologyData.passedEvent()) return false;
    // increment(fEvtTopologyCounter);
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    // hAlphaT->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight()); // FIXME: move this histogramming to evt topology
    fAlphaT = sAlphaT.fAlphaT;
    fHt = sAlphaT.fHt;
    fJt = sAlphaT.fJt;


    // Top mass
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    // if (!TopSelectionData.passedEvent()) return false;
    // increment(fTopSelectionCounter);

                                           
    // Z mass veto
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
    // if (!jetTauInvMassData.passedEvent()) return false;
    // increment(fZmassVetoCounter);
                               

    // Transverse Mass Reconstruction 
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    fTransverseMass = transverseMass;


    // Fill TTree before any cut
    myTree->Fill();
    // -----> No CUTS <----- (end)
    
    // Fill Counters for reference - to see that all is normal
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    if(!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    if(!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    if(!fakeMETData.passedEvent()) return false;
    increment(fFakeMETVetoCounter);
    if(!evtTopologyData.passedEvent()) return false;
    increment(fEvtTopologyCounter);
    if(!TopSelectionData.passedEvent()) return false;
    increment(fTopSelectionCounter);
    if(!TopSelectionData.passedEvent()) return false;
    increment(fZmassVetoCounter);
    if(!jetTauInvMassData.passedEvent()) return false;
    increment(ftransverseMassCutCounter);


    return true;
  }
}
