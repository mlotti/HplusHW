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
    fAllCounter(eventCounter.addCounter("All Events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("Primary Vertex")),
    fElectronVetoCounter(eventCounter.addCounter("Electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("Muon veto")),
    fTausExistCounter(eventCounter.addCounter("Taus > 0")),
    fOneTauCounter(eventCounter.addCounter("Taus == 1")),
    fRtauCounter(eventCounter.addCounter("Rtau")),
    fMETCounter(eventCounter.addCounter("MET")),
    fNJetsCounter(eventCounter.addCounter("Jet Selection")),
    fBTaggingCounter(eventCounter.addCounter("B-tagging")),
    fAlphaTCounter(eventCounter.addCounter("AlphaT")),
    fFakeMETVetoCounter(eventCounter.addCounter("Fake MET")),
    ftransverseMassCutCounter(eventCounter.addCounter("TransverseMass")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection")),
    fZmassVetoCounter(eventCounter.addCounter("ZmassVetoCounter")),
    fForwardJetVetoCounter(eventCounter.addCounter("Forward jet veto")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1, "TauID"),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    // ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
    fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
  {

    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // TTree:: Make TTree and book variables
    myTree = fs->make<TTree>("HPlusAlphatAnalysis","HPlusAlphatAnalysis");
    myTree->Branch("bTriggerPassed", &bTriggerPassed);
    myTree->Branch("bPVPassed", &bPVPassed);
    myTree->Branch("bTauIdPassed", &bTauIdPassed);
    myTree->Branch("bRtauPassed", &bRtauPassed);
    myTree->Branch("bElectronVetoPassed", &bElectronVetoPassed);
    myTree->Branch("bMuonVetoPassed", &bMuonVetoPassed);
    myTree->Branch("fTauJetEt",  &fTauJetEt);
    myTree->Branch("fTauJetEta", &fTauJetEta);
    myTree->Branch("fRtau", &fRtau);
    myTree->Branch("fMET", &fMET);
    myTree->Branch("fFakeMETDeltaPhi", &fFakeMETDeltaPhi);
    myTree->Branch("fDeltaPhiTauMET", &fDeltaPhiTauMET);
    myTree->Branch("iNHadronicJets", &iNHadronicJets);
    myTree->Branch("iNHadronicJetsInFwdDir", &iNHadronicJetsInFwdDir);
    myTree->Branch("iNBtags", &iNBtags);
    myTree->Branch("fLdgJetEt", &fLdgJetEt);
    myTree->Branch("fSecondLdgJetEt", &fSecondLdgJetEt);
    myTree->Branch("fThirdLdgJetEt", &fThirdLdgJetEt);
    myTree->Branch("fGlobalMuonVetoHighestPt", &fGlobalMuonVetoHighestPt);
    myTree->Branch("fGlobalElectronVetoHighestPt", &fGlobalElectronVetoHighestPt);
    myTree->Branch("fTransverseMass", &fTransverseMass);
    myTree->Branch("fAlphaT", &fAlphaT);
    myTree->Branch("fHt", &fHt);
    myTree->Branch("fJt", &fJt);

    // Histograms: Book histograms filled in the analysis body
    hVerticesBeforeWeight = makeTH<TH1F>(*fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = makeTH<TH1F>(*fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassWithTopCut = makeTH<TH1F>(*fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
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
    
    /// First fill the counters to get a taste of what is going on
    FillCounters(iEvent, iSetup);
    
    // Reset TTree variable values
    bTriggerPassed = false;
    bPVPassed = false;
    bTauIdPassed = false;
    bRtauPassed = false;
    bElectronVetoPassed = false;
    bMuonVetoPassed = false;

    fEvtWeight  = -5;
    iNSelectedTaus = -5;
    fTauJetEt = -5.0;
    fTauJetEta = -9999.99;
    fRtau = -5;
    fMET = -5.0;
    fFakeMETDeltaPhi = -5.0;
    fDeltaPhiTauMET = -5.0;
    iNHadronicJets = -5.0;
    iNHadronicJetsInFwdDir = -5.0;
    iNBtags = -5.0;
    fLdgJetEt = -5.0;
    fSecondLdgJetEt = -5.0;
    fThirdLdgJetEt = -5.0;
    fGlobalMuonVetoHighestPt = -5.0;
    fGlobalElectronVetoHighestPt = -5.0;
    fTransverseMass = -5.0;
    fAlphaT = -5.0; 
    fHt = -5.0;
    fJt = -5.0; 
    fTopMass = -5.0;

    // EventWeight: Set prescale for Real Data Triggers (Data only)
    fEventWeight.updatePrescale(iEvent);
    
    // EventWeight: Vertex weight (MC only)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData()) fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

    // GenParticle analysis: Where to put this?
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    // 1) Apply Trigger and HLT_MET cut (Data only)
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if( triggerData.passedEvent() ) bTriggerPassed = true;
    else bTriggerPassed = false;
    
    // 2) Primary vertex selection
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if( pvData.passedEvent() ) bPVPassed = true;
    else bPVPassed = false;

    // 3) Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if( electronVetoData.passedEvent() ){
      fGlobalElectronVetoHighestPt = electronVetoData.getSelectedElectronPt();
      bElectronVetoPassed = true;
    }

    // 4) Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if( muonVetoData.passedEvent() ){
      fGlobalMuonVetoHighestPt = muonVetoData.getSelectedMuonPt();
      bMuonVetoPassed = true;
    }
    
    // 5) TauID
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup); 
    // TauSelection::Data tauData = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup);
    if( tauData.selectedTauPassedRtau() ) bRtauPassed = true;
    if( tauData.passedEvent() ){
      bTauIdPassed = true;
      fTauJetEt  = static_cast<float>( (tauData.getSelectedTaus()[0])->pt() );
      fTauJetEta = static_cast<float>( (tauData.getSelectedTaus()[0])->eta() );
      iNSelectedTaus = tauData.getSelectedTaus().size();
      fRtau = tauData.getRtauOfSelectedTau();
    }
    

    // 6) MET
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    fMET = metData.getSelectedMET()->et();
    
    // 7) Selected Jets
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    edm::PtrVector<pat::Jet> selectedJets = jetData.getSelectedJets();
    iNHadronicJets = selectedJets.size();
    if(iNHadronicJets > 0) fLdgJetEt = selectedJets[0]->et();
    if(iNHadronicJets > 1) fSecondLdgJetEt = selectedJets[1]->et();
    if(iNHadronicJets > 2) fThirdLdgJetEt = selectedJets[2]->et();

    // Note: If TauID and JetSelection fail return; attikis
    if(!tauData.passedEvent()) return false;
    //    if(!jetData.passedEvent()) return false;

    // 8) Btagging
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets()); 
    if(btagData.passedEvent())  iNBtags = btagData.getBJetCount();
    fEventWeight.multiplyWeight(btagData.getScaleFactor());


    // 9) AlphaT 
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    fAlphaT = sAlphaT.fAlphaT;
    fHt = sAlphaT.fHt;
    fJt = sAlphaT.fJt;

    // 10) Fake MET veto a.k.a. further QCD suppression
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    fFakeMETDeltaPhi = fakeMETData.closestDeltaPhi();
                                
    // DeltaPhi(tau,MET)
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    fDeltaPhiTauMET = deltaPhi;

    // 11) Transverse Mass
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    fTransverseMass = transverseMass;

    // 12) Top mass
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    fTopMass = TopSelectionData.getTopMass();
    
    // 13) Z mass veto
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
                               
    // 14) Forward jet veto
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    iNHadronicJetsInFwdDir = jetData.getHadronicJetCountInFwdDir();    

    // Last but NOT least: Save the event weight!
    fEvtWeight = fEventWeight.getWeight();

    // Fill TTree before any cut
    myTree->Fill();    
    
    // std::cout << "*** Event passed!" << std::endl;

    return true;
  }



  void AlphatAnalysis::FillCounters(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

    // std::cout << "*** void AlphatAnalysis::FillCounters(const edm::Event& iEvent, const edm::EventSetup& iSetup) { " << std::endl;

    // 0) Start counting events 
    increment(fAllCounter);
    
    // 1) Trigger
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if(!triggerData.passedEvent()) return;
    increment(fTriggerCounter);
    
    // 2) Primary Vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;;
    increment(fPrimaryVertexCounter);

    // 3) Electron Veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return;
    increment(fElectronVetoCounter);
    // hAlphatAfterElectronVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    // 4) Muon Veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return;
    increment(fMuonVetoCounter);
    // hAlphatAfterMuonVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    // 5) TauID 
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup); 
    // Require at least one tau (no Rtau yet)
    if(!tauData.passedEvent()) return;
    increment(fTausExistCounter);

    // Require exactly one tau
    if(tauData.getSelectedTaus().size() != 1) return;
    increment(fOneTauCounter);

    // Rtau cut
    if(!tauData.selectedTauPassedRtau() ) return;
    increment(fRtauCounter);

    // Histos after Full TauID
    hSelectedTauEt->Fill(tauData.getSelectedTaus()[0]->pt(), fEventWeight.getWeight());
    hSelectedTauEta->Fill(tauData.getSelectedTaus()[0]->eta(), fEventWeight.getWeight());
    hSelectedTauPhi->Fill(tauData.getSelectedTaus()[0]->phi(), fEventWeight.getWeight());
    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    // hAlphatVsMETAfterTauID->Fill(sAlphaT.fAlphaT, metData.getSelectedMET()->et(), fEventWeight.getWeight());
    // hAlphatAfterTauID->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    
    // 6) MET 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    hMet_AfterTauSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if(!metData.passedEvent()) return;
    increment(fMETCounter);
    hMet_BeforeTauSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // 7) Selected Jets
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()); 
    if(!jetData.passedEvent()) return;
    increment(fNJetsCounter);
    // hAlphatAfterJetSelection->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    
    // 8) B-tagging
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets()); 
    if(!btagData.passedEvent()) return;
    fEventWeight.multiplyWeight(btagData.getScaleFactor());
    increment(fBTaggingCounter);
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    // hAlphatAfterBtagging->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());

    // 9) AlphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets()); 
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    if(!evtTopologyData.passedEvent()) return;
    increment(fAlphaTCounter);

    // 10) Fake MET
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    fFakeMETDeltaPhi = fakeMETData.closestDeltaPhi();
    if(!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    // hAlphatAfterFakeMetVeto->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3, fEventWeight.getWeight());
    
    // 11) Transverse Mass
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    if(transverseMass < 100 ) return;
    increment( ftransverseMassCutCounter);
    hTransverseMass->Fill(transverseMass, fEventWeight.getWeight());   
    
    // 12) Top Selection
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if( TopSelectionData.passedEvent() ) return;
    increment(fTopSelectionCounter);
    hTransverseMassWithTopCut->Fill(transverseMass, fEventWeight.getWeight());
    // hAlphatAfterTopSelection->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    // 13) Z mass veto here
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
    if (!jetTauInvMassData.passedEvent()) return;
    increment(fZmassVetoCounter);
    
    // 14) Forward jet veto here
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    if (!forwardJetData.passedEvent()) return;
    increment(fForwardJetVetoCounter);

    return;
  }

}
