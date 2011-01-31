// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "TTree.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class SignalOptimisation {
  public:
    explicit SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalOptimisation();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const double  ftransverseMassCut;

    // Counters
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fTriggerEmulationCounter;
    Count fClobalMuonVetoCounter;
    Count fClobalElectronVetoCounter;
    Count fOneProngTauSelectionCounter;
    Count fMETCounter;
    Count fJetSelectionCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fEvtTopologyCounter;
    //
    EventWeight& fEventWeight;

    // The order here defines the order the counters are printed at the program termination
    TriggerSelection fTriggerSelection;
    TriggerTauMETEmulation fTriggerTauMETEmulation;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    TauSelection fOneProngTauSelection;
    METSelection fMETSelection;
    JetSelection fJetSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    EvtTopology fEvtTopology;

    
    // Histograms
    TH1 *hAlphaTInvMass;
    TH1 *hAlphaTDiJetMassClosestToW;

    // for Tree
    TTree *myTree;

    bool bTauIDStatus;
    float fTauJetEt;
    float fTauJetEta;
    float fMET;
    float fFakeMETDeltaPhi;
    int iNHadronicJets;
    int iNHadronicJetsInFwdDir;
    int iNBtags;
    float fGlobalMuonVetoHighestPt;
    float fGlobalElectronVetoHighestPt;
    float fTransverseMass;
    float fDeltaPhi;
    float fAlphaT;
    float fHt;
    float fJt; // Jt = Ht - TauJetEt - LdgJetEt
    float fDiJetMassClosestToW;
  };
}

#endif
