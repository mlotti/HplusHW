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
    ftransverseMassCut(iConfig.getUntrackedParameter<double>("transverseMassCut")),
    fAllCounter(eventCounter.addCounter("All Events")),
    fTriggerCounter(eventCounter.addCounter("Trigger Counter")),
    fPrimaryVertexCounter(eventCounter.addCounter("Primary vertex")),
    fTausExistCounter(eventCounter.addCounter("Taus > 0")),
    fOneTauCounter(eventCounter.addCounter("Taus == 1")),
    fMETCounter(eventCounter.addCounter("MET")),
    fElectronVetoCounter(eventCounter.addCounter("Electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("Muon veto")),
    fNJetsCounter(eventCounter.addCounter("NJets")),
    fBTaggingCounter(eventCounter.addCounter("Btagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("Fake MET veto")),
    fEvtTopologyCounter(eventCounter.addCounter("Evt Topology")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    fZmassVetoCounter(eventCounter.addCounter("Z Mass Veto")),
    ftransverseMassCutCounter(eventCounter.addCounter("TransverseMass Cut")),
    fEventWeight(eventWeight),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight"))//,
    {
        
    // Analysis variations
    std::vector<double> vTauPt;
    vTauPt.push_back(40);
    vTauPt.push_back(50);
    vTauPt.push_back(60);
    vTauPt.push_back(80);
    std::vector<double> vRTau;
    vRTau.push_back(0.0);
    vRTau.push_back(0.4);
    vRTau.push_back(0.7);
    vRTau.push_back(0.8);
    std::vector<double> vMET;
    vMET.push_back(60);
    vMET.push_back(70);
    //    vMET.push_back(80);
    std::vector<double> vBTagDiscr;
    vBTagDiscr.push_back(2.0);
    vBTagDiscr.push_back(1.7);
    vBTagDiscr.push_back(3.3);
    std::vector<double> vFakeMETVeto;
    vFakeMETVeto.push_back(0);
    vFakeMETVeto.push_back(10);
    //    vFakeMETVeto.push_back(20);
    //vFakeMETVeto.push_back(30);
    size_t myCount = 0;
    for (std::vector<double>::iterator itTauPt = vTauPt.begin(); itTauPt != vTauPt.end(); ++itTauPt) {
      for (std::vector<double>::iterator itRtau = vRTau.begin(); itRtau != vRTau.end(); ++itRtau) {
        for (std::vector<double>::iterator itMET = vMET.begin(); itMET != vMET.end(); ++itMET) {
          for (std::vector<double>::iterator itBtagDiscr= vBTagDiscr.begin(); itBtagDiscr != vBTagDiscr.end(); ++itBtagDiscr) {
            for (std::vector<double>::iterator itFakeMETVeto = vFakeMETVeto.begin(); itFakeMETVeto != vFakeMETVeto.end(); ++itFakeMETVeto) {
              fAnalyses.push_back(AnalysisVariation(*itTauPt, *itRtau, *itMET, *itBtagDiscr, *itFakeMETVeto));
              fAnalysisVariationCounters.push_back(eventCounter.addCounter(fAnalyses[myCount].getLabel()));
              ++myCount;
            }
          }
        }
      }
    }

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
    return analyse(iEvent, iSetup);
  }

  // void SignalOptimisation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  bool SignalOptimisation::analyse(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
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
    

    // 2) Apply trigger and HLT_MET cut
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if(!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);


    // 3) Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    

    // 4) TauID 
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    increment(fTausExistCounter);
    if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
    bTauIDStatus = 1;
    increment(fOneTauCounter);
    // Get Tau-related variables
    fTauJetEt  = static_cast<float>( (tauData.getSelectedTaus()[0])->pt() );
    fTauJetEta = static_cast<float>( (tauData.getSelectedTaus()[0])->eta() );


    // MET
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    // if(!metData.passedEvent()) return false;
    fMET = metData.getSelectedMET()->et();
    

    // Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    fGlobalElectronVetoHighestPt = electronVetoData.getSelectedElectronPt();


    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    fGlobalMuonVetoHighestPt = muonVetoData.getSelectedMuonPt();
 

    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus()[0]); 
    // if(!jetData.passedEvent()) return false;
    // increment(fNJetsCounter);
    iNHadronicJets = jetData.getHadronicJetCount();   
    iNHadronicJetsInFwdDir = jetData.getHadronicJetCountInFwdDir();
    

    // b-tagging
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets()); 
    fEventWeight.multiplyWeight(btagData.getScaleFactor());
    // if(!btagData.passedEvent()) return false;
    // increment(fBTaggingCounter);    
    iNBtags = btagData.getBJetCount();
    
    
    // Fake MET veto a.k.a. further QCD suppression
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus()[0], jetData.getSelectedJets(), metData.getSelectedMET());
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
    TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    // if (!topSelectionData.passedEvent()) return false;
    // increment(fTopSelectionCounter);

                                           
    // Z mass veto
    JetTauInvMass::Data jetTauInvMassData = fJetTauInvMass.analyze(tauData.getSelectedTaus(), jetData.getSelectedJets());
    // if (!jetTauInvMassData.passedEvent()) return false;
    // increment(fZmassVetoCounter);
                               

    // Transverse Mass Reconstruction 
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    fTransverseMass = transverseMass;


    // Handle variations of analysis
    for (size_t i = 0; i < fAnalyses.size(); ++i) {
      if (fAnalyses[i].analyse(metData, tauData.getSelectedTaus(), tauData, jetData, btagData, fakeMETData, topSelectionData, transverseMass, fEventWeight.getWeight()))
        increment(fAnalysisVariationCounters[i]);
    }
    
    // Fill TTree before any cut
// uncomment the following to produce the ROOT tree
//myTree->Fill();
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
    //if(!evtTopologyData.passedEvent()) return false;
    increment(fEvtTopologyCounter);
    //if(!TopSelectionData.passedEvent()) return false;
    increment(fTopSelectionCounter);
    //if(!TopSelectionData.passedEvent()) return false;
    increment(fZmassVetoCounter);
    //if(!jetTauInvMassData.passedEvent()) return false;
    increment(ftransverseMassCutCounter);


    return true;
  }

  
    SignalOptimisation::AnalysisVariation::AnalysisVariation(double tauPtCut, double rtau, double METcut, double btaggingDiscriminator, double fakeMETVetoCut)
  : fTauPtCut(tauPtCut),
    fRtauCut(rtau),
    fBTaggingDiscriminator(btaggingDiscriminator),
    fMETCut(METcut),
    fFakeMETVetoCut(fakeMETVetoCut) {
    std::stringstream myName;
    myName << "QCDAnalysisVariation_tauPt" << tauPtCut << "_rtau" << rtau << "_btag" << btaggingDiscriminator << "_METcut" << METcut << "_FakeMETCut" << fakeMETVetoCut;
    fLabel = myName.str();
    // Create histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(myName.str());
    hEventCount = makeTH<TH1F>(myDir, "EventCount", "EventCount", 1, 0, 1);
    hRtauAfterAllOthers = makeTH<TH1F>(myDir, "Rtau", "Rtau", 22, 0., 1.1);
    hBTaggingDiscriminatorAfterAllOthers = makeTH<TH1F>(myDir, "BTaggingDiscriminator", "BTaggingDiscriminator", 100, 0., 50.0);
    hMETAfterAllOthers = makeTH<TH1F>(myDir, "MET", "MET", 40, 0., 200.);
    hFakeMETVetoAfterAllOthers = makeTH<TH1F>(myDir, "FakeMETVeto", "FakeMETVeto", 36, 0., 180.);
    hTopSelectionAfterAllOthers = makeTH<TH1F>(myDir, "TopSelection", "TopSelection", 161, -5., 800.);
    hTransverseMassAfterAllOthers = makeTH<TH1F>(myDir, "TransverseMass", "TransverseMass", 30., 0., 300.);
    
  }
  SignalOptimisation::AnalysisVariation::~AnalysisVariation() { }
  bool SignalOptimisation::AnalysisVariation::analyse(const METSelection::Data& METData, const edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const TopSelection::Data& topSelectionData, double transverseMass, double weight) {
    bool myPassedStatus = false;
    // All cuts
    if (selectedTau[0]->pt() > fTauPtCut &&
        tauData.getRtauOfSelectedTau() > fRtauCut &&
        jetData.passedEvent() &&
        btagData.getMaxDiscriminatorValue() > fBTaggingDiscriminator &&
        METData.getSelectedMET()->et() > fMETCut &&
        fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
      //std::cout << "top mass: " << topSelectionData.getTopMass() << std::endl;
      hTopSelectionAfterAllOthers->Fill(topSelectionData.getTopMass(), weight);
      hTransverseMassAfterAllOthers->Fill(transverseMass, weight);
      hEventCount->Fill(0., weight);
      myPassedStatus = true;
    }
    // Rtau leg
    if (selectedTau[0]->pt() > fTauPtCut &&
        jetData.passedEvent() &&
        btagData.getMaxDiscriminatorValue() > fBTaggingDiscriminator &&
        METData.getSelectedMET()->et() > fMETCut &&
        fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
      hRtauAfterAllOthers->Fill(tauData.getRtauOfSelectedTau(), weight);
    }
    // BTagging leg
    if (selectedTau[0]->pt() > fTauPtCut &&
        tauData.getRtauOfSelectedTau() > fRtauCut &&
        jetData.passedEvent() &&
        METData.getSelectedMET()->et() > fMETCut &&
        fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
      //std::cout << "btag: " << btagData.getMaxDiscriminatorValue() << std::endl;
      hBTaggingDiscriminatorAfterAllOthers->Fill(btagData.getMaxDiscriminatorValue(), weight);
    }
    // MET leg
    if (selectedTau[0]->pt() > fTauPtCut &&
        tauData.getRtauOfSelectedTau() > fRtauCut &&
        jetData.passedEvent() &&
        btagData.getMaxDiscriminatorValue() > fBTaggingDiscriminator &&
        fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
      hMETAfterAllOthers->Fill(METData.getSelectedMET()->et(), weight);
    }
    // Fake MET Veto leg
    if (selectedTau[0]->pt() > fTauPtCut &&
        tauData.getRtauOfSelectedTau() > fRtauCut &&
        jetData.passedEvent() &&
        btagData.getMaxDiscriminatorValue() > fBTaggingDiscriminator &&
        METData.getSelectedMET()->et() > fMETCut) {
      hFakeMETVetoAfterAllOthers->Fill(fakeMETData.closestDeltaPhi(), weight);
    }
    return myPassedStatus;
  }

}
