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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingMuonIsolationQuantifier.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

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
    void doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper fHistoWrapper;
    const bool bBlindAnalysisStatus;
    const bool bTauEmbeddingStatus;
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
    Count fHiggsMassCutCounter;
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
    Count fTopChiSelectionNarrowCounter;
    Count fFakeMETVetoCounter;
    Count fSelectedEventsCounter;
    Count fSelectedEventsCounterWithGenuineBjets;

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
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;
    VertexWeightReader fVertexWeightReader;
    VertexAssignmentAnalysis fVertexAssignmentAnalysis;
    FakeTauIdentifier fFakeTauIdentifier;
    TauEmbeddingMuonIsolationQuantifier fTauEmbeddingMuonIsolationQuantifier;

    SignalAnalysisTree fTree;

    // Scale factor uncertainties
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterSelection;
    ScaleFactorUncertaintyManager fEWKFakeTausSFUncertaintiesAfterSelection;

    // Histograms
    
    // Vertex histograms
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;
    WrappedTH1 *hVerticesTriggeredBeforeWeight;
    WrappedTH1 *hVerticesTriggeredAfterWeight;
    
    // Transverse mass histograms
    WrappedTH1 *hTransverseMass;
    WrappedTH1 *hTransverseMassTopSelection;
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH1 *hTransverseMassTopWithWSelection;
    WrappedTH1 *hTransverseMassMET70;
    WrappedTH1 *hTransverseMassTauVeto;
    WrappedTH1 *hTransverseMassAfterDeltaPhi;
    WrappedTH1 *hEWKFakeTausTransverseMass;
    WrappedTH1 *hTransverseMassFakeMetVeto;
    WrappedTH1 *hTransverseMassAfterDeltaPhi160;
    WrappedTH1 *hTransverseMassAfterDeltaPhi130;
    WrappedTH1 *hTransverseMassAfterDeltaPhi90;
    WrappedTH2 *hTransverseMassVsNjets;
    WrappedTH2 *hEWKFakeTausTransverseMassVsNjets;

    // Full mass histograms
    WrappedTH1 *hFullMass;
    WrappedTH1 *hEWKFakeTausFullMass;


    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hEWKFakeTausDeltaPhi;
    WrappedTH1 *hDeltaPhiJetMet;
    WrappedTH1 *hMaxDeltaPhiJetMet;
    WrappedTH1 *hAlphaT;
    WrappedTH1 *hAlphaTInvMass;
    WrappedTH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hMet;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauPhi;
    WrappedTH1 *hSelectedTauRtau;
    WrappedTH1 *hSelectedTauLeadingTrackPt;
    WrappedTH1 *hSelectedTauRtauAfterCuts;
    WrappedTH1 *hSelectedTauEtAfterCuts;
    WrappedTH1 *hSelectedTauEtaAfterCuts;
    WrappedTH1 *hMetAfterCuts;
    WrappedTH1 *hEWKFakeTausSelectedTauEtAfterCuts;
    WrappedTH1 *hEWKFakeTausSelectedTauEtaAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet;

    WrappedTH1 *hSelectionFlow;
    WrappedTH2 *hSelectionFlowVsVertices;
    WrappedTH2 *hSelectionFlowVsVerticesFakeTaus;

    // Control plots
    WrappedTH1* hCtrlIdentifiedElectronPt;
    WrappedTH1* hCtrlIdentifiedMuonPt;
    WrappedTH1* hCtrlNjets;
    WrappedTH1* hCtrlNjetsAfterMET;
    WrappedTH1* hCtrlSelectedTauPtAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauEtaAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hCtrlSelectedTauEtaVsPhiAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauRtauAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauPAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
    WrappedTH1* hCtrlIdentifiedElectronPtAfterStandardSelections;
    WrappedTH1* hCtrlIdentifiedMuonPtAfterStandardSelections;
    WrappedTH1* hCtrlNjetsAfterStandardSelections;
    WrappedTH1* hCtrlMET;
    WrappedTH1* hCtrlNbjets;
    // Control plots for fakes
    WrappedTH1* hCtrlEWKFakeTausIdentifiedElectronPt;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedMuonPt;
    WrappedTH1* hCtrlEWKFakeTausNjets;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedElectronPtAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedMuonPtAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausNjetsAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausMET;
    WrappedTH1* hCtrlEWKFakeTausNbjets;

    WrappedTH2* hCtrlJetMatrixAfterJetSelection;
    WrappedTH2* hCtrlJetMatrixAfterMET;
    WrappedTH2* hCtrlJetMatrixAfterMET100;

    // CounterGroups for EWK fake taus (aka non-QCD type 2)
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

    WrappedTH1 *hEMFractionAll;
    WrappedTH1 *hEMFractionElectrons;

    std::string fModuleLabel;

    bool fProduce;
    bool fOnlyGenuineTaus;
  };
}

#endif
