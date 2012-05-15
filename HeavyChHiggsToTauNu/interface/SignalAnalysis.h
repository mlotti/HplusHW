// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"

#include<string>

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
      void incrementFakeMETVetoCounter() { increment(fFakeMETVetoCounter); }
      void incrementTopSelectionCounter() { increment(fTopSelectionCounter); }
      void incrementTopChiSelectionCounter() { increment(fTopChiSelectionCounter); }
      void incrementSelectedEventsCounter() { increment(fSelectedEventsCounter); }
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fDeltaPhiCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
      Count fTopChiSelectionCounter;
      //      Count fTopChiSelectionNarrowCounter;
      Count fTopWithBSelectionCounter;
      Count fTopWithWSelectionCounter;
      Count fSelectedEventsCounter;
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
    kSignalOrderDeltaPhiSelection,
    kSignalOrderFakeMETVeto,
    kSignalOrderBjetSelection,
    kSignalOrderTopSelection,
    kSignalOrderSelectedEvents
  };
  public:
    explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalAnalysis();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    CounterGroup* getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch);
    void fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    const bool bBlindAnalysisStatus;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm
    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fTriggerScaleFactorCounter;
    Count fGenuineTauCounter;
    Count fVetoTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fDeltaPhiTauMETCounter;
    Count fTauVetoAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiTauVetoCounter;

    Count fTauIsHadronFromHplusCounter;
    Count fTauIsElectronFromHplusCounter;
    Count fTauIsMuonFromHplusCounter;
    Count fTauIsQuarkFromWCounter;
    Count fTauIsElectronFromWCounter;
    Count fTauIsMuonFromWCounter;
    Count fTauIsHadronFromWTauCounter;
    Count fTauIsElectronFromWTauCounter;
    Count fTauIsMuonFromWTauCounter;
    Count fTauIsElectronFromBottomCounter;
    Count fTauIsMuonFromBottomCounter;
    Count fTauIsHadronFromBottomCounter;
    Count fTauIsElectronFromJetCounter;
    Count fTauIsMuonFromJetCounter;
    Count fTauIsHadronFromJetCounter;
   
    Count fFakeMETVetoCounter;
    Count fdeltaPhiTauMET160FakeMetCounter;
    Count fForwardJetVetoCounter;
    Count fTopSelectionCounter;
    Count fTopChiSelectionCounter;
    Count fTopChiSelection250Counter;
    Count fTopChiSelection220Counter;
    Count fTopWithBSelectionCounter;
    Count fTopWithBSelection250Counter;
    Count fTopWithBSelection220Counter;
    Count fTopWithWSelectionCounter;
    Count fTopWithWSelection250Counter;
    Count fTopWithWSelection220Counter;
    Count ftransverseMassCut70Counter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMass70TauVetoCounter;
    Count ftransverseMass80TauVetoCounter;
    Count ftransverseMass70TopChiSelCounter;
    Count ftransverseMass70TopWithBSelCounter;
    Count ftransverseMass70TopWithWSelCounter;
    Count ftransverseMass70TopSelCounter;
    Count ftransverseMass80TopChiSelCounter;
    Count ftransverseMass80TopWithBSelCounter;
    Count ftransverseMass80TopWithWSelCounter;
    Count ftransverseMass80TopSelCounter;
    Count ftransverseMassCut80NoRtauCounter;
    Count ftransverseMassCut100NoRtauCounter;
    Count fZmassVetoCounter;

    Count fSelectedEventsCounter;

    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    TauSelection fTauSelection;
    VetoTauSelection fVetoTauSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    TopSelection fTopSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    TopWithWSelection fTopWithWSelection;
    BjetSelection fBjetSelection;
    //    BjetWithPtSelection fBjetWithPtSelection;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;
    VertexWeight fVertexWeight;
    VertexAssignmentAnalysis fVertexAssignmentAnalysis;
    FakeTauIdentifier fFakeTauIdentifier;
    
    SignalAnalysisTree fTree;

    // Scale factor uncertainties
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterSelection;

    // Histograms
    
    // Vertex histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hVerticesTriggeredBeforeWeight;
    TH1 *hVerticesTriggeredAfterWeight;
    
    // Transverse mass histograms
    TH1 *hTransverseMass;
    TH1 *hTransverseMassTopSelection;
    TH1 *hTransverseMassTopChiSelection;
    TH1 *hTransverseMassTopBjetSelection;
    TH1 *hTransverseMassTopWithWSelection;
    TH1 *hTransverseMassMET70;
    TH1 *hTransverseMassTauVeto;
    TH1 *hTransverseMassAfterDeltaPhi;
    
    TH1 *hTransverseMassFakeMetVeto;
    /*
    TH1 *hTransverseMassAfterDeltaPhi160;
    TH1 *hTransverseMassAfterDeltaPhi130;
    TH1 *hTransverseMassAfterDeltaPhi90;
    TH1 *hNonQCDTypeIITransverseMass;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi130;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi160;
    TH1 *hNonQCDTypeIITransverseMassAfterDeltaPhi90;
    */
    TH1 *hEWKFakeTausTransverseMass;

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
    TH1 *hEWKFakeTausSelectedTauEtAfterCuts;
    TH1 *hEWKFakeTausSelectedTauEtaAfterCuts;
    TH1 *hTransverseMassDeltaPhiUpperCutFakeMet;

    TH1 *hSelectionFlow;
    TH2 *hSelectionFlowVsVertices;
    TH2 *hSelectionFlowVsVerticesFakeTaus;

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
    CounterGroup fEWKFakeTausGroup;
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

    std::string fModuleLabel;

    bool fProduce;
    bool fOnlyGenuineTaus;
  };
}

#endif
