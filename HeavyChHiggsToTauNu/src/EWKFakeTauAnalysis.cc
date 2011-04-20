#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EWKFakeTauAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  EWKFakeTauAnalysis::CounterGroup::CounterGroup(EventCounter& eventCounter, std::string prefix) :
    fOneTauCounter(eventCounter.addCounter(prefix+":taus == 1")),
    fElectronVetoCounter(eventCounter.addCounter(prefix+":electron veto")),
    fMuonVetoCounter(eventCounter.addCounter(prefix+":muon veto")),
    fMETCounter(eventCounter.addCounter(prefix+":MET")),
    fNJetsCounter(eventCounter.addCounter(prefix+":njets")),
    fBTaggingCounter(eventCounter.addCounter(prefix+":btagging")),
    fFakeMETVetoCounter(eventCounter.addCounter(prefix+":fake MET veto")) { }
  EWKFakeTauAnalysis::CounterGroup::~CounterGroup() { }

  EWKFakeTauAnalysis::EWKFakeTauAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    //fTriggerEmulationCounter(eventCounter.addCounter("trigger emulation")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fAllTausCounterGroup(eventCounter, "All"),
    fElectronToTausCounterGroup(eventCounter, "e->tau"),
    fMuonToTausCounterGroup(eventCounter, "mu->tau"),
    fGenuineToTausCounterGroup(eventCounter, "tau->tau"),
    fJetToTausCounterGroup(eventCounter, "jet->tau"),
    //    ftransverseMassCutCounter(eventCounter.addCounter("transverseMass cut")),
    //fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    //fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    //    ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("ftransverseMassCut"), eventCounter, eventWeight),
    fGenparticleAnalysis(eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fTauEmbeddingAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("tauEmbedding"), eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
   
  {

    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    //    hmetAfterTrigger = makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass", 400, 0., 400.);
    hTransverseMassWithTopCut = makeTH<TH1F>(*fs, "transverseMassWithTopCut", "transverseMassWithTopCut", 400, 0., 400.);
    hTransverseMassAfterVeto = makeTH<TH1F>(*fs, "transverseMassAfterVeto", "transverseMassAfterVeto", 400, 0., 400.);
    hTransverseMassBeforeVeto = makeTH<TH1F>(*fs, "transverseMassBeforeVeto", "transverseMassBeforeVeto", 400, 0., 400.);
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi", 400, 0., 3.2);
    hAlphaT = makeTH<TH1F>(*fs, "alphaT", "alphaT", 500, 0.0, 5.0);
    hAlphaTInvMass = makeTH<TH1F>(*fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = makeTH<TH2F>(*fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    //    hMet_AfterTauSelection = makeTH<TH1F>(*fs, "met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 400.0);
    //    hMet_BeforeTauSelection = makeTH<TH1F>(*fs, "met_BeforeTauSelection", "met_BeforeTauSelection", 100, 0.0, 400.0);
    hMet_AfterBTagging = makeTH<TH1F>(*fs, "met_AfterBTagging", "met_AfterBTagging", 100, 0.0, 300.0);
  }

  EWKFakeTauAnalysis::~EWKFakeTauAnalysis() { }

  void EWKFakeTauAnalysis::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void EWKFakeTauAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale
    

  // GenParticle analysis
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    //    fTauEmbeddingAnalysis.beginEvent(iEvent, iSetup);
   

    increment(fAllCounter);
//fTriggerEmulationEfficiency.analyse(iEvent,iSetup);
    // Apply trigger and HLT_MET cut
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if(!triggerData.passedEvent()) return;
    increment(fTriggerCounter);
/*
    // Tau+MET trigger emulation
    // HLT_MET cut is applied at trigger step
    TriggerTauMETEmulation::Data triggerTauMETEmulationData = fTriggerTauMETEmulation.analyze(iEvent, iSetup);
    if(!triggerTauMETEmulationData.passedEvent()) return;
    increment(fTriggerEmulationCounter);
*/ 
/*
    edm::Handle <reco::VertexCollection> goodPrimaryVertices;
    edm::InputTag myVertexInputTag("goodPrimaryVertices", "", "HChPatTuple");
    iEvent.getByLabel(myVertexInputTag, goodPrimaryVertices);
    //   if (goodPrimaryVertices->size() != 1) return;
    */

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);

    
    // TauID (with optional factorization) 
                                                                             
    //    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);

    // Hadronic jet selection                                                                                                                                                                                                      
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus());
    //    if(!jetData.passedEvent()) return;
    //    increment(fNJetsCounter);
    

     fTauEmbeddingAnalysis.beginEvent(iEvent, iSetup);
                                                                                                                                            
    // TauID (with optional factorization)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return; // Require at least one tau
    increment(fTausExistCounter);
    if(tauData.getSelectedTaus().size() != 1) return; // Require exactly one tau
    
    // Obtain MC matching
    MCTauMatchType myTauMatch = matchTauToMC(iEvent, tauData.getSelectedTaus()[0]);
    fAllTausCounterGroup.incrementOneTauCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementOneTauCounter();
    
    fTauEmbeddingAnalysis.setSelectedTau(tauData.getSelectedTaus()[0]);
    fTauEmbeddingAnalysis.fillAfterTauId();

    // MET 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    hTransverseMassBeforeVeto->Fill(transverseMass);
 
    //    Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return;
    fAllTausCounterGroup.incrementElectronVetoCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementElectronVetoCounter();

    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return;
    fAllTausCounterGroup.incrementMuonVetoCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementMuonVetoCounter();
    hTransverseMassAfterVeto->Fill(transverseMass);

    // MET cut
    if(!metData.passedEvent()) return;
    fAllTausCounterGroup.incrementMETCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementMETCounter();
    fTauEmbeddingAnalysis.fillAfterMetCut();
   
    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return;
    fAllTausCounterGroup.incrementNJetsCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementNJetsCounter();

    // b tagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return;
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et());
    fAllTausCounterGroup.incrementBTaggingCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementBTaggingCounter();

    // Fake MET veto
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!fakeMETData.passedEvent()) return;
    fAllTausCounterGroup.incrementFakeMETVetoCounter();
    if (myTauMatch != kNoMC) getCounterGroupByTauMatch(myTauMatch)->incrementFakeMETVetoCounter();
    
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());

    // Alpha T
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return;

    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3);
    //    hDeltaPhi->Fill(deltaPhi);

    //    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    hTransverseMass->Fill(transverseMass);

    //    if(transverseMass < 100 ) return;
    //   increment(ftransverseMassCutCounter);

    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    hAlphaT->Fill(sAlphaT.fAlphaT); // FIXME: move this histogramming to evt topology
    /*
    // top mass
    TopSelection::Data TopSelectionData = fTopSelection.analyze(jetData.getSelectedJets(), btagData.getSelectedJets());
    if (!TopSelectionData.passedEvent()) return;
    increment(fTopSelectionCounter);

    hTransverseMassWithTopCut->Fill(transverseMass);
    */
                                           
    // Forward jet veto                                                                                                                                                                                                                
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return;
    //    increment(fForwardJetVetoCounter);
    //    fTauEmbeddingAnalysis.fillEnd();


    // The following code is not correct, because there could be more than one tau jet
    // passing the tau ID (and hence multiple values of Rtau
    // Please access the selected tau jets via  tauData.getSelectedTaus()
    //std::cout << "tauData.Rtau = " << tauData.Rtau << std::endl;
    //hAlphaTVsRtau->Fill(tauData.Rtau, sAlphaT.fAlphaT);

    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i]); }

//    fTriggerEmulationEfficiency.analyse(iEvent,iSetup);

  }

  EWKFakeTauAnalysis::MCTauMatchType EWKFakeTauAnalysis::matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau) {
    if (iEvent.isRealData()) return kNoMC;
    bool isMCTau = false;
    bool isMCElectron = false;
    bool isMCMuon = false;
    
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {  
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13 || std::abs(p.pdgId()) == 15) {
        // Check match with tau
        if (reco::deltaR(p, tau->p4()) < 0.1) {
          if (p.pt() > 10.) {
            //std::cout << "  match found, pid=" << p.pdgId() << " eta=" << std::abs(p.eta()) << " pt=" << p.pt() << std::endl;
            if (std::abs(p.pdgId()) == 11) isMCElectron = true;
            if (std::abs(p.pdgId()) == 13) isMCMuon = true;
            if (std::abs(p.pdgId()) == 15) isMCTau = true;
          }
        }
      }
    }
    if (isMCElectron) return kElectronToTau;
    if (isMCMuon) return kMuonToTau;
    if (isMCTau) return kTauToTau;
    return kJetToTau;
  }

  EWKFakeTauAnalysis::CounterGroup* EWKFakeTauAnalysis::getCounterGroupByTauMatch(MCTauMatchType tauMatch) {
    if (tauMatch == kElectronToTau) return &fElectronToTausCounterGroup;
    else if (tauMatch == kMuonToTau) return &fMuonToTausCounterGroup;
    else if (tauMatch == kTauToTau) return &fGenuineToTausCounterGroup;
    else if (tauMatch == kJetToTau) return &fJetToTausCounterGroup;
    return 0;
  }
}
