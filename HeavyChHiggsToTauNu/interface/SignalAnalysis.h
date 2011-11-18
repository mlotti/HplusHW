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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

class TH1;
class TH2;
class TTree;

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
      void incrementDeltaPhiCounter() { increment(fDeltaPhiCounter); }
      void incrementDeltaPhi160Counter() { increment(fDeltaPhi160Counter); }
      void incrementDeltaPhi130Counter() { increment(fDeltaPhi130Counter); }
      void incrementFakeMETVetoCounter() { increment(fFakeMETVetoCounter); }
      void incrementTopSelectionCounter() { increment(fTopSelectionCounter); }
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fDeltaPhiCounter;
      Count fDeltaPhi160Counter;
      Count fDeltaPhi130Counter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
    };
  enum SignalSelectionOrder {
    kSignalOrderTrigger,
    //kSignalOrderVertexSelection,
    kSignalOrderTauID,
    kSignalOrderElectronVeto,
    kSignalOrderMuonVeto,
    kSignalOrderJetSelection,
    kSignalOrderMETSelection,
    kSignalOrderBTagSelection,
    //kSignalOrderDeltaPhiSelection,
    kSignalOrderDeltaPhi160Selection,
    kSignalOrderDeltaPhi130Selection,
    kSignalOrderFakeMETVeto,
    kSignalOrderTopSelection
  };
  public:
    explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalAnalysis();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    CounterGroup* getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch);
    void fillNonQCDTypeIICounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fTriggerScaleFactorCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fDeltaPhiTauMETCounter;
    Count fdeltaPhiTauMET10Counter;
    Count fdeltaPhiTauMET160Counter;
    Count fdeltaPhiTauMET130Counter;
    Count fFakeMETVetoCounter;
    Count fdeltaPhiTauMET160FakeMetCounter;
    Count fForwardJetVetoCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;
    Count ftransverseMassCut80NoRtauCounter;
    Count ftransverseMassCut100NoRtauCounter;
    Count fZmassVetoCounter;
    Count fTopSelectionCounter;
    Count ftransverseMassCut100TopCounter;

    TriggerSelection fTriggerSelection;
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
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;
    VertexWeight fVertexWeight;
    FakeTauIdentifier fFakeTauIdentifier;
    
    SignalAnalysisTree fTree;

    // Scale factor uncertainties
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterBTagging;
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterDeltaPhi160;
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterDeltaPhi130;
    
    // Histograms
    
    // Vertex histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hVerticesTriggeredBeforeWeight;
    TH1 *hVerticesTriggeredAfterWeight;
    
    // Transverse mass histograms
    TH1 *hTransverseMass;
    TH1 *hTransverseMassJetMetCut;
    TH1 *hTransverseMassTopSelection;
    TH1 *hTransverseMassMET70;
    TH1 *hTransverseMassAfterDeltaPhi;
    TH1 *hTransverseMassAfterDeltaPhi160;
    TH1 *hTransverseMassAfterDeltaPhi130;
    TH1 *hNonQCDTypeIITransverseMass;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi130;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi160;
    TH1 *hDeltaPhi;
    TH1 *hDeltaPhiJetMet;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hSelectedTauEt;
    TH1 *hMet;
    TH1 *hSelectedTauEta;
    TH1 *hSelectedTauPhi;
    TH1 *hSelectedTauRtau;
    TH1 *hSelectedTauLeadingTrackPt;
    TH1 *hSelectedTauRtauAfterCuts;
    TH1 *hSelectedTauEtAfterCuts;
    TH1 *hSelectedTauEtaAfterCuts;
    TH1 *hMetAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtaAfterCuts;
    TH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 

    TH1 *hSelectionFlow;

    // Control plots
    TH1* hCtrlIdentifiedElectronPt;
    TH1* hCtrlIdentifiedMuonPt;
    TH1* hCtrlNjets;
    TH1* hCtrlSelectedTauPtAfterStandardSelections;
    TH1* hCtrlSelectedTauEtaAfterStandardSelections;
    TH1* hCtrlSelectedTauPhiAfterStandardSelections;
    TH2* hCtrlSelectedTauEtaVsPhiAfterStandardSelections;
    TH1* hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
    TH1* hCtrlSelectedTauRtauAfterStandardSelections;
    TH1* hCtrlSelectedTauPAfterStandardSelections;
    TH1* hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
    TH1* hCtrlIdentifiedElectronPtAfterStandardSelections;
    TH1* hCtrlIdentifiedMuonPtAfterStandardSelections;
    TH1* hCtrlNjetsAfterStandardSelections;
    TH1* hCtrlMET;
    TH1* hCtrlNbjets;

    // CounterGroups for EWK fake taus (aka non-QCD type 2(
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

    bool fProduce;
  };
}

#endif
