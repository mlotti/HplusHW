#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    //fTriggerEmulationCounter(eventCounter.addCounter("trigger emulation")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fOneTauCounter(eventCounter.addCounter("taus == 1")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fMETCounter(eventCounter.addCounter("MET")),
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
    //    hmetAfterTrigger = makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassWithTopCut = makeTH<TH1F>(*fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassAfterVeto = makeTH<TH1F>(*fs, "transverseMassAfterVeto", "transverseMassAfterVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassBeforeVeto = makeTH<TH1F>(*fs, "transverseMassBeforeVeto", "transverseMassBeforeVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hAlphaT = makeTH<TH1F>(*fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = makeTH<TH1F>(*fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = makeTH<TH2F>(*fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    //    hMet_AfterTauSelection = makeTH<TH1F>(*fs, "met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 400.0);
    //    hMet_BeforeTauSelection = makeTH<TH1F>(*fs, "met_BeforeTauSelection", "met_BeforeTauSelection", 100, 0.0, 400.0);
    hMet_AfterBTagging = makeTH<TH1F>(*fs, "MET_AfterBTagging", "MET_AfterBTagging;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    
    hMETBeforeMETCut = makeTH<TH1F>(*fs, "MET_BeforeMETCut", "MET_BeforeMETCut;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hSelectedTauEt = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = makeTH<TH1F>(*fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhi = makeTH<TH1F>(*fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = makeTH<TH1F>(*fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);

    hSelectedTauEtMetCut = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEtaMetCut = makeTH<TH1F>(*fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhiMetCut = makeTH<TH1F>(*fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = makeTH<TH1F>(*fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
  }

  SignalAnalysis::~SignalAnalysis() { }

  bool SignalAnalysis::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    return analyze(iEvent, iSetup);
  }

  bool SignalAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale

    // Vertex weight
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData())
      fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

  // GenParticle analysis
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    //    fTauEmbeddingAnalysis.beginEvent(iEvent, iSetup);
   

    increment(fAllCounter);
//fTriggerEmulationEfficiency.analyse(iEvent,iSetup);
    // Apply trigger and HLT_MET cut
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (iEvent.isRealData()) {
      // Trigger is applied only if the data sample is real data
      if(!triggerData.passedEvent()) return false;
    }
    increment(fTriggerCounter);
/*
    // Tau+MET trigger emulation
    // HLT_MET cut is applied at trigger step
    TriggerTauMETEmulation::Data triggerTauMETEmulationData = fTriggerTauMETEmulation.analyze(iEvent, iSetup);
    if(!triggerTauMETEmulationData.passedEvent()) return false;
    increment(fTriggerEmulationCounter);
*/ 
/*
    edm::Handle <reco::VertexCollection> goodPrimaryVertices;
    edm::InputTag myVertexInputTag("goodPrimaryVertices", "", "HChPatTuple");
    iEvent.getByLabel(myVertexInputTag, goodPrimaryVertices);
    //   if (goodPrimaryVertices->size() != 1) return false;
    */

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);

    
    // TauID (with optional factorization) 
                                                                             
    //    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);

    // Hadronic jet selection                                                                                                                                                                                                      
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus());
    //    if(!jetData.passedEvent()) return false;
    //    increment(fNJetsCounter);
    

    fTauEmbeddingAnalysis.beginEvent(iEvent, iSetup);
                                                                                                                                            
    // TauID (with optional factorization)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    increment(fTausExistCounter);
    if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
    increment(fOneTauCounter);
    
    fTauEmbeddingAnalysis.setSelectedTau(tauData.getSelectedTaus()[0]);
    fTauEmbeddingAnalysis.fillAfterTauId();
    
    
    // Get MET object 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);

    // Trigger efficiency
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(tauData.getSelectedTaus()[0]), *metData.getSelectedMET());
    if (!iEvent.isRealData() || fTauEmbeddingAnalysis.isEmbeddingInput()) {
      // Apply trigger efficiency as weight for simulated events, or if the input is from tau embedding
      fEventWeight.multiplyWeight(triggerEfficiency);
    }
    hSelectedTauEt->Fill(tauData.getSelectedTaus()[0]->pt(), fEventWeight.getWeight());
    hSelectedTauEta->Fill(tauData.getSelectedTaus()[0]->eta(), fEventWeight.getWeight());
    hSelectedTauPhi->Fill(tauData.getSelectedTaus()[0]->phi(), fEventWeight.getWeight());
    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());


  

    // MET cut
    hMETBeforeMETCut->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    // tmp    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    fTauEmbeddingAnalysis.fillAfterMetCut();
    
    hSelectedTauEtMetCut->Fill(tauData.getSelectedTaus()[0]->pt(), fEventWeight.getWeight());
    hSelectedTauEtaMetCut->Fill(tauData.getSelectedTaus()[0]->eta(), fEventWeight.getWeight());
    hSelectedTauPhiMetCut->Fill(tauData.getSelectedTaus()[0]->phi(), fEventWeight.getWeight());
    hSelectedTauRtauMetCut->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );

    // hTransverseMassBeforeVeto->Fill(transverseMass);
    // Hadronic jet selection                                                                                                                                      
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus());


    hTransverseMassBeforeVeto->Fill(transverseMass, fEventWeight.getWeight());


    //    Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);


    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);

    hTransverseMassAfterVeto->Fill(transverseMass, fEventWeight.getWeight());
  

    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
   

    // b tagging
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return false;
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    increment(fBTaggingCounter);

    
    // Fake MET veto a.k.a. further QCD suppression
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!fakeMETData.passedEvent()) return false;
    increment(fFakeMETVetoCounter);
                                                                                                                     
    
                               
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());

    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3, fEventWeight.getWeight());
    hDeltaPhi->Fill(deltaPhi);

    //    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    hTransverseMass->Fill(transverseMass, fEventWeight.getWeight());


    // Alpha T
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    //if(!evtTopologyData.passedEvent()) return false;
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    hAlphaT->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight()); // FIXME: move this histogramming to evt topology

    
    // top mass
    TopSelection::Data TopSelectionData = fTopSelection.analyze(jetData.getSelectedJets(), btagData.getSelectedJets());
    if (!TopSelectionData.passedEvent()) return false;
    increment(fTopSelectionCounter);

    hTransverseMassWithTopCut->Fill(transverseMass, fEventWeight.getWeight());

    //    if(transverseMass < ftransverseMassCut-20.0 ) return false;
    if(transverseMass < 80 ) return false;
    increment(ftransverseMassCut80Counter);

    if(transverseMass < 100 ) return false;
    increment(ftransverseMassCut100Counter);
                                           
    //Z mass veto
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!jetTauInvMassData.passedEvent()) return false;
    increment(fZmassVetoCounter);
                               
    // Forward jet veto                                                                                                                                                                                                           
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return false;
    //    increment(fForwardJetVetoCounter);
    //    fTauEmbeddingAnalysis.fillEnd();


    // The following code is not correct, because there could be more than one tau jet
    // passing the tau ID (and hence multiple values of Rtau
    // Please access the selected tau jets via  tauData.getSelectedTaus()
    //std::cout << "tauData.Rtau = " << tauData.Rtau << std::endl;
    //hAlphaTVsRtau->Fill(tauData.Rtau, sAlphaT.fAlphaT);

    int diJetSize = sAlphaT.vDiJetMassesNoTau.size();
    for(int i= 0; i < diJetSize; i++){ hAlphaTInvMass->Fill(sAlphaT.vDiJetMassesNoTau[i], fEventWeight.getWeight()); }

//    fTriggerEmulationEfficiency.analyse(iEvent,iSetup);

    return true;
  }
}
