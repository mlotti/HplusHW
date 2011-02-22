// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementFromAntiTauControlRegion_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementFromAntiTauControlRegion_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "TTree.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class QCDMeasurementFromAntiTauControlRegion {
  public:
    explicit QCDMeasurementFromAntiTauControlRegion(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~QCDMeasurementFromAntiTauControlRegion();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    // Counters
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fPrimaryVertexCounter;
    Count fGlobalElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fJetSelectionCounter;
    Count fInvMassVetoOnJetsCounter;
    Count fEvtTopologyCounter;
    Count fOneProngTauSelectionCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fMETgt0AfterWholeSelectionCounter;
    Count fMETgt30AfterWholeSelectionCounter;
    Count fMETgt40AfterWholeSelectionCounter;
    Count fMETgt50AfterWholeSelectionCounter;
    Count fMETgt60AfterWholeSelectionCounter;
    Count fMETgt70AfterWholeSelectionCounter;
    Count fMETgt80AfterWholeSelectionCounter;

    // The order here defines the order the counters are printed at the program termination
    TriggerSelection fTriggerSelection;
    //TriggerTauMETEmulation  fTriggerTauMETEmulation;
    VertexSelection fPrimaryVertexSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    JetSelection fJetSelection;
    InvMassVetoOnJets fInvMassVetoOnJets;
    EvtTopology fEvtTopology;
    TauSelection fOneProngTauSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    
    // Histograms
    TH1 *hMETAfterTrigger;
    TH1 *hMETAfterElectronVeto;
    TH1 *hMETAfterMuonVeto;
    TH1 *hMETAfterTauSelection;
    TH1 *hMETAfterJetSelection;
    TH1 *hMETAfterInvMassVetoOnJets;
    TH1 *hMETAfterMET;
    TH1 *hMETAfterBTagging;
    TH1 *hMETAfterFakeMetVeto;
    TH1 *hMETAfterWholeSelection; // without MET Cut
  };
}

#endif
