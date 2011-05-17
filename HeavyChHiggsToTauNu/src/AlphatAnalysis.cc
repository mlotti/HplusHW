#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/AlphatAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  AlphatAnalysis::AlphatAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    //fTriggerEmulationCounter(eventCounter.addCounter("trigger emulation")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fOneTauCounter(eventCounter.addCounter("taus == 1")),
    fMETCounter(eventCounter.addCounter("MET")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("fake MET veto")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    ftransverseMassCut80Counter(eventCounter.addCounter("transverseMass > 80")),
    ftransverseMassCut100Counter(eventCounter.addCounter("transverseMass > 100")),
    fZmassVetoCounter(eventCounter.addCounter("ZmassVetoCounter")),
    fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
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
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    //    ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fTauEmbeddingAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("tauEmbedding"), eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
    fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
   
  {

    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    hVerticesBeforeWeight = makeTH<TH1F>(*fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = makeTH<TH1F>(*fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassWithTopCut = makeTH<TH1F>(*fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    // 
    hAlphatAfterTauID = fs->make<TH1F>("AlphatAnalysis_AlphatAfterTauID", "AlphatAnalysis_hAlphatAfterTauID; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterTauID->Sumw2();
    hAlphatVsMETAfterTauID = fs->make<TH2F>("AlphatAnalysis_AlphatVsMetAfterTauID", "AlphatAnalysis_AlphatVsMetAfterTauID;#alpha_{T};MET [GeV]", 100, 0.0, 5.0, 60, 0., 300.);
    hAlphatVsMETAfterTauID->Sumw2();
    hAlphatAfterElectronVeto = fs->make<TH1F>("AlphatAnalysis_AlphatAfterElectronVeto", "AlphatAnalysis_hAlphatAfterElectronVeto; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterElectronVeto->Sumw2();
    hAlphatAfterMuonVeto = fs->make<TH1F>("AlphatAnalysis_AlphatAfterMuonVeto", "AlphatAnalysis_hAlphatAfterMuonVeto; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterMuonVeto->Sumw2();
    hAlphatAfterJetSelection = fs->make<TH1F>("AlphatAnalysis_AlphatAfterJetSelection", "AlphatAnalysis_hAlphatAfterJetSelection; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterJetSelection->Sumw2();
    hAlphatAfterBtagging = fs->make<TH1F>("AlphatAnalysis_AlphatAfterBtagging", "AlphatAnalysis_hAlphatAfterBtagging; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterBtagging->Sumw2();
    hAlphatAfterFakeMetVeto = fs->make<TH1F>("AlphatAnalysis_AlphatAfterFakeMetVeto", "AlphatAnalysis_hAlphatAfterFakeMetVeto; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterFakeMetVeto->Sumw2();
    hAlphatAfterTopSelection = fs->make<TH1F>("AlphatAnalysis_AlphatAfterTopSelection", "AlphatAnalysis_hAlphatTopSelection; #alpha_{T} , N_{events} / 0.1", 100, 0.0, 5.0);
    hAlphatAfterTopSelection->Sumw2();
    //
    hAlphatInvMass = makeTH<TH1F>(*fs, "AlphatAnalysis_Alphat_InvMass", "AlphatAnalysis_Alphat_InvMass", 100, 0.0, 1000.0);    
    hAlphatVsRtau = makeTH<TH2F>(*fs, "AlphatAnalysis_Alphat_Vs_Rtau", "AlphatAnalysis_Alphat_Vs_Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    hMet_AfterTauSelection = makeTH<TH1F>(*fs, "AlphatAnalysis_Met_AfterTauSelection", "AlphatAnalysis_Met_AfterTauSelection", 100, 0.0, 400.0);
    hMet_BeforeTauSelection = makeTH<TH1F>(*fs, "AlphatAnalysis_Met_BeforeTauSelection", "AlphatAnalysis_Met_BeforeTauSelection", 100, 0.0, 400.0);
    hMet_AfterBTagging = makeTH<TH1F>(*fs, "AlphatAnalysis_Met_AfterBTagging", "AlphatAnalysis_Met_AfterBTagging;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hSelectedTauEt = makeTH<TH1F>(*fs, "AlphatAnalysis_SelectedTau_pT_AfterTauID", "AlphatAnalysis_SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = makeTH<TH1F>(*fs, "AlphatAnalysis_SelectedTau_eta_AfterTauID", "AlphatAnalysis_SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhi = makeTH<TH1F>(*fs, "AlphatAnalysis_SelectedTau_phi_AfterTauID", "AlphatAnalysis_SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = makeTH<TH1F>(*fs, "AlphatAnalysis_SelectedTau_Rtau_AfterTauID", "AlphatAnalysis_SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
  }

  AlphatAnalysis::~AlphatAnalysis() { }

  bool AlphatAnalysis::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    return analyze(iEvent, iSetup);
  }

  bool AlphatAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    
    // Set prescale for Real Data Triggers 
    fEventWeight.updatePrescale(iEvent);

    
    // Vertex weight
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    // Only apply this to MC! 
    if(!iEvent.isRealData())
      fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

    
    // GenParticle analysis
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);


    // Start counting events (after PU re-weighting of MC samples)
    increment(fAllCounter);

    
    // Apply trigger and HLT_MET cut (Only if REAL Data)
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (iEvent.isRealData()) {
      // Trigger is applied only if the data sample is real data
      if(!triggerData.passedEvent()) return false;
    }
    increment(fTriggerCounter);


    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    // Tau-Embedding
    fTauEmbeddingAnalysis.beginEvent(iEvent, iSetup);


    // Get MET object (Do NOT apply cut)
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    // tmp if(!metData.passedEvent()) return false;
    // increment(fMETCounter);
    // fTauEmbeddingAnalysis.fillAfterMetCut();
    // histos
    hMet_BeforeTauSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // TauID (with optional factorization)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    // Require at least one tau
    if(!tauData.passedEvent()) return false;
    increment(fTausExistCounter);
    // Require exactly one tau
    if(tauData.getSelectedTaus().size() != 1) return false; 
    increment(fOneTauCounter);


    // Trigger efficiency (Before ANY histo-filling)
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(tauData.getSelectedTaus()[0]), *metData.getSelectedMET());
    if (!iEvent.isRealData() || fTauEmbeddingAnalysis.isEmbeddingInput()) {
      // Apply trigger efficiency as weight for MC events only!
      fEventWeight.multiplyWeight(triggerEfficiency);
    }


    // Selected Jets (Do NOT apply cut)
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    // histos


    // AlphaT -> Can start calculating the variable alphaT now (need tau and jets)
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return false;
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    // histos (TauID)
    hSelectedTauEt->Fill(tauData.getSelectedTaus()[0]->pt(), fEventWeight.getWeight());
    hSelectedTauEta->Fill(tauData.getSelectedTaus()[0]->eta(), fEventWeight.getWeight());
    hSelectedTauPhi->Fill(tauData.getSelectedTaus()[0]->phi(), fEventWeight.getWeight());
    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hMet_AfterTauSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hAlphatVsMETAfterTauID->Fill(sAlphaT.fAlphaT, metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hAlphatAfterTauID->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    
    // Tau-Embedding (After TauID)
    fTauEmbeddingAnalysis.setSelectedTau(tauData.getSelectedTaus()[0]);
    fTauEmbeddingAnalysis.fillAfterTauId();
    
    
           
    // Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    // histos
    hAlphatAfterElectronVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    

    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    // histos
    hAlphatAfterMuonVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    

    // Hadronic jet selection
    // JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    // histos
    hAlphatAfterJetSelection->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    
    // Btagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    // histos
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hAlphatAfterBtagging->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    

    // Fake MET veto a.k.a. further QCD suppression
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!fakeMETData.passedEvent()) return false;
    increment(fFakeMETVetoCounter);
    // histos
    hAlphatAfterFakeMetVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    

    /////////////////////////////////////////// End of SignalAnalysis cut-flow (without MET cut) ///////////////////////////////////////////
                               
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());


    // DeltaPhi(tau,MET)
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3, fEventWeight.getWeight());
    hDeltaPhi->Fill(deltaPhi);
    
    
    // Transverse Mass
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    // histos
    hTransverseMass->Fill(transverseMass, fEventWeight.getWeight());   


    // Top mass
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (!TopSelectionData.passedEvent()) return false;
    increment(fTopSelectionCounter);
    // histos
    hTransverseMassWithTopCut->Fill(transverseMass, fEventWeight.getWeight());
    hAlphatAfterTopSelection->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    // Transverse Mass Cut
    if(transverseMass < 80 ) return false;
    increment(ftransverseMassCut80Counter);

    if(transverseMass < 100 ) return false;
    increment(ftransverseMassCut100Counter);
                                           

    // Z mass veto
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!jetTauInvMassData.passedEvent()) return false;
    increment(fZmassVetoCounter);
                               

    // Forward jet veto
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    if (!forwardJetData.passedEvent()) return false;
    increment(fForwardJetVetoCounter);
    fTauEmbeddingAnalysis.fillEnd();

    
    // // Get MET object (Do NOT apply cut)
    //     METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);


    return true;
  }
}
