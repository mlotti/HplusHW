// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EWKFakeTauAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EWKFakeTauAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class EWKFakeTauAnalysis {
    class CounterGroup {
    public:
      CounterGroup(EventCounter& eventCounter, std::string prefix);
      ~CounterGroup();
  
      void incrementOneTauCounter() { increment(fOneTauCounter); }
      void incrementElectronVetoCounter() { increment(fElectronVetoCounter); }
      void incrementMuonVetoCounter() { increment(fMuonVetoCounter); }
      void incrementMETCounter() { increment(fMETCounter); }
      void incrementNJetsCounter() { increment(fNJetsCounter); }
      void incrementBTaggingCounter() { increment(fBTaggingCounter); }
      void incrementFakeMETVetoCounter() { increment(fFakeMETVetoCounter); }
      void incrementTopSelectionCounter() { increment(fTopSelectionCounter); }
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
    };

  enum MCTauMatchType {
    kElectronToTau,
    kMuonToTau,
    kTauToTau,
    kJetToTau,
    kNoMC,
    kElectronToTauAndTauOutsideAcceptance,
    kMuonToTauAndTauOutsideAcceptance,
    kTauToTauAndTauOutsideAcceptance,
    kJetToTauAndTauOutsideAcceptance
  };
  public:
    explicit EWKFakeTauAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~EWKFakeTauAnalysis();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    MCTauMatchType matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau);
    CounterGroup* getCounterGroupByTauMatch(MCTauMatchType tauMatch);
    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusEWKFakeTauAnalysisProducer
    EventWeight& fEventWeight;

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    //Count fTriggerEmulationCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;

    CounterGroup fAllTausCounterGroup;
    CounterGroup fElectronToTausCounterGroup;
    CounterGroup fMuonToTausCounterGroup;
    CounterGroup fGenuineToTausCounterGroup;
    CounterGroup fJetToTausCounterGroup;
    CounterGroup fAllTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fJetToTausAndTauOutsideAcceptanceCounterGroup;

    //Count fForwardJetVetoCounter;
    //    Count ftransverseMassCutCounter;

    TriggerSelection fTriggerSelection;
    TriggerTauMETEmulation  fTriggerTauMETEmulation;
    VertexSelection fPrimaryVertexSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    TauSelection fOneProngTauSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    TopSelection fTopSelection;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    TauEmbeddingAnalysis fTauEmbeddingAnalysis;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;

    //
    TriggerEmulationEfficiency fTriggerEmulationEfficiency;

    // Histograms
    TH1 *hTransverseMass;
    TH1 *hTransverseMassWithTopCut;
    TH1 *hTransverseMassAfterVeto;
    TH1 *hTransverseMassBeforeVeto;
    TH1 *hDeltaPhi;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;

    TH1 *hEMFractionAll;
    TH1 *hEMFractionElectrons;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
  };
}

#endif
