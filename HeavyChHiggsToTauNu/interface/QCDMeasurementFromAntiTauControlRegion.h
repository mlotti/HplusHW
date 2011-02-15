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
    //Count fTriggerEmulationCounter;
    Count fOneProngTauSelectionCounter;
    Count fJetSelectionCounter;
    Count fGlobalElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fBTaggingCounter;
    Count fMETCounter;
    Count fInvMassVetoOnJetsCounter;
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
    TriggerTauMETEmulation  fTriggerTauMETEmulation;
    TauSelection fOneProngTauSelection;
    JetSelection fJetSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    METSelection fMETSelection;
    BTagging fBTagging;
    InvMassVetoOnJets fInvMassVetoOnJets;
    FakeMETVeto fFakeMETVeto;
    EvtTopology fEvtTopology;
    
    // Histograms
    TH1 *hMETAfterWholeSelection;
    //aa    TH1 *hTriggerPrescales;
    //aa    TH1 *hTriggerPrescales_test;

  };
}

#endif
