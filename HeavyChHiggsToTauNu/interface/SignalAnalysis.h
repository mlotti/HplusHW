// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelectionFactorized.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class SignalAnalysis {
  public:
    explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalAnalysis();

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    const double ftransverseMassCut;
    const bool fUseFactorizedTauID;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fTriggerEmulationCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fMETCounter;
    Count fNJetsCounter;
    Count fBTaggingCounter;

    TriggerSelection fTriggerSelection;
    TriggerMETEmulation  fTriggerMETEmulation;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    TauSelection fTauSelection;
    TauSelectionFactorized fTauSelectionFactorized;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    
    // Count ftransverseMassCutCount;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;

    // Histograms
    TH1 *hTransverseMass;
    TH1 *hDeltaPhi;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
    TH1 *hMetBeforeEmul;
    TH1 *hMetBeforeTrigger;
    TH1 *hMetAfterTrigger;
  };
}

#endif
