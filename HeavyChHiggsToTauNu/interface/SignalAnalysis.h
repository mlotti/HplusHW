// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h

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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

class TH1;
class TH2;

namespace HPlus {
  class SignalAnalysis {
    class CounterGroup {
    public:
      /// Constructor for subcounters
      CounterGroup(EventCounter& eventCounter, std::string prefix);
      /// Constructor for main counters
      CounterGroup(EventCounter& eventCounter);
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
  enum SignalSelectionOrder {
    kSignalOrderTrigger,
    //kSignalOrderVertexSelection,
    kSignalOrderTauID,
    kSignalOrderMETSelection,
    kSignalOrderElectronVeto,
    kSignalOrderMuonVeto,
    kSignalOrderJetSelection,
    kSignalOrderBTagSelection,
    kSignalOrderFakeMETVeto,
    kSignalOrderTopSelection
  };
  enum MCSelectedTauMatchType {
    kkElectronToTau,
    kkMuonToTau,
    kkTauToTau,
    kkJetToTau,
    kkNoMC,
    kkElectronToTauAndTauOutsideAcceptance,
    kkMuonToTauAndTauOutsideAcceptance,
    kkTauToTauAndTauOutsideAcceptance,
    kkJetToTauAndTauOutsideAcceptance
  };
  public:
    explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalAnalysis();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau);
    CounterGroup* getCounterGroupByTauMatch(MCSelectedTauMatchType tauMatch);
    void fillNonQCDTypeIICounters(MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData, bool passedStatus = true, double value = 0);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    //Count fTriggerEmulationCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fRtauAfterTauIDCounter;    
    Count fMETCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingCounter;
    Count fdeltaPhiTauMET10Counter;
    Count fdeltaPhiTauMET160Counter;
    Count fFakeMETVetoCounter;
    Count fRtauAfterCutsCounter;
    Count fForwardJetVetoCounter;
    Count fdeltaPhiTauMET160FakeMetCounter;
    Count fTopRtauDeltaPhiFakeMETCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;
    Count ftransverseMassCut80NoRtauCounter;
    Count ftransverseMassCut100NoRtauCounter;
    Count fZmassVetoCounter;
    Count fTopSelectionCounter;
    Count ftransverseMassCut100TopCounter;

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
    JetTauInvMass fJetTauInvMass;
    TopSelection fTopSelection;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    TauEmbeddingAnalysis fTauEmbeddingAnalysis;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;

    VertexWeight fVertexWeight;
    TriggerEmulationEfficiency fTriggerEmulationEfficiency;

    // Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hVerticesTriggeredBeforeWeight;
    TH1 *hVerticesTriggeredAfterWeight;
    TH1 *hTransverseMass;
    TH1 *hTransverseMassWithTopCut;
    TH1 *hTransverseMassAfterVeto;
    TH1 *hTransverseMassBeforeVeto;
    TH1 *hTransverseMassBeforeFakeMet;
    TH1 *hTransverseMassDeltaPhiUpperCut;
    TH1 *hTransverseMassWithRtauFakeMet;
    TH1 *hTransverseMassWithRtau;
    TH1 *hTransverseMassTopRtauDeltaPhiFakeMET;
    TH1 *hDeltaPhi;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
    TH1 *hMETBeforeMETCut;
    TH1 *hMETBeforeTauId;
    TH1 *hSelectedTauEt;
    TH1 *hSelectedTauEta;
    TH1 *hSelectedTauPhi;
    TH1 *hSelectedTauRtau;
    TH1 *hSelectedTauLeadingTrackPt;
    TH1 *hSelectedTauLeadingTrackPtMetCut;
    TH1 *hSelectedTauRtauAfterCuts;
    TH1 *hSelectedTauEtMetCut;
    TH1 *hSelectedTauEtaMetCut;
    TH1 *hSelectedTauPhiMetCut;
    TH1 *hSelectedTauEtAfterCuts;
    TH1 *hSelectedTauEtaAfterCuts;
    TH1 *hMetAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtaAfterCuts;
    TH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 
    TH1 *hSelectedTauRtauMetCut;

    TH1 *hSelectionFlow;

    CounterGroup fNonQCDTypeIIGroup;
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

    TH1 *hEMFractionAll;
    TH1 *hEMFractionElectrons;

  };
}

#endif
