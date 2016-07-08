#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingEfficiencyInMC.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCAnalysisOfSelectedEvents.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMTWeightFit.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingMuonIsolationQuantifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"

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
      void incrementNJetsCounter() { increment(fNJetsCounter); }
      void incrementDeltaPhiCollinearCounter() { increment(fDeltaPhiCollinearCounter); }
      void incrementMETCounter() { increment(fMETCounter); }
      void incrementBTaggingCounter() { increment(fBTaggingCounter); }
      void incrementDeltaPhiBackToBackCounter() { increment(fDeltaPhiBackToBackCounter); }
      void incrementFakeMETVetoCounter() { increment(fFakeMETVetoCounter); }
      void incrementSelectedEventsCounter() { increment(fSelectedEventsCounter); }
      void incrementSelectedEventsFullMassCounter() { increment(fSelectedEventsFullMassCounter);}



    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fNJetsCounter;
      Count fDeltaPhiCollinearCounter;
      Count fMETCounter;
      Count fBTaggingCounter;
      Count fDeltaPhiBackToBackCounter;
      Count fSelectedEventsCounter;
      Count fSelectedEventsFullMassCounter;
      Count fFakeMETVetoCounter;

    };
  enum SignalSelectionOrder {
    kSignalOrderTrigger,
    kSignalOrderVertexSelection,
    kSignalOrderTauID,
    kSignalOrderElectronVeto,
    kSignalOrderMuonVeto,
    kSignalOrderJetSelection,
    kSignalOrderDeltaPhiCollinearSelection,
    kSignalOrderMETSelection,
    kSignalOrderBTagSelection,
    kSignalOrderDeltaPhiBackToBackSelection,
    kSignalOrderTopSelection,
    kSignalOrderSelectedEvents,
    kSignalOrderSelectedEventsFullMass,
    kSignalOrderFakeMETVeto,
    kSignalOrderBjetSelection
  };
  public:
  explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~SignalAnalysis();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    /// Fill TTree (after delta phi collinear cuts)
    void doTreeFilling(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData, const edm::Ptr<pat::Tau>& selectedTau, const ElectronSelection::Data& electronVetoData, const MuonSelection::Data& muonVetoData, const JetSelection::Data& jetData);
    void fillSelectionFlowAndCounterGroups(int nVertices, FakeTauIdentifier::Data& tauMatchData, bool selectedToEWKFakeTauBackgroundStatus, SignalSelectionOrder selection, const TauSelection::Data& tauData);
    CounterGroup* getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch);
    void fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, bool selectedToEWKFakeTauBackgroundStatus, SignalSelectionOrder selection, const TauSelection::Data& tauData);
    void doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData);
    bool selectTailEvents(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper fHistoWrapper;
    const bool bBlindAnalysisStatus; // FIXME: obsolete
    const bool bTauEmbeddingStatus;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm

    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;

    // Main counters
    Count fAllCounter;
    Count fTopPtWeightCounter;
    Count fWJetsWeightCounter;
    Count fEmbeddingGeneratorWeightCounter;
    Count fEmbeddingWTauMuWeightCounter;
    Count fMETFiltersCounter;
    Count fEmbeddingMuonTriggerEfficiencyCounter;
    Count fEmbeddingMuonIdEfficiencyCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fTauFakeScaleFactorCounter;
    Count fOneTauCounter;
    Count fTauTriggerScaleFactorCounter;
    Count fGenuineTauCounter;
    Count fVetoTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fPreMETCutCounter;
    Count fMETTriggerScaleFactorCounter;
    Count fQCDTailKillerCollinearCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fEmbeddingMTWeightCounter;
    Count fQCDTailKillerBackToBackCounter;
    Count fTopReconstructionCounter;
    Count fSelectedEventsCounter;
    Count fHiggsMassSelectionCounter;
    Count fFakeMETVetoCounter;

    Count fTauVetoAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiTauVetoCounter;


    Count fSelectedEventsCounterWithGenuineBjets;

    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    ElectronSelection fElectronSelection;
    MuonSelection fMuonSelection;
    TauSelection fTauSelection;
    VetoTauSelection fVetoTauSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    BTaggingEfficiencyInMC fBTaggingEfficiencyInMC;
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    BjetSelection fBjetSelection;
    MCAnalysisOfSelectedEvents fMCAnalysisOfSelectedEvents;
    //    BjetWithPtSelection fBjetWithPtSelection;
    TopSelectionManager fTopSelectionManager;
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    EmbeddingMuonEfficiency fEmbeddingMuonTriggerEfficiency;
    EmbeddingMuonEfficiency fEmbeddingMuonIdEfficiency;
    EmbeddingMTWeightFit fEmbeddingMTWeight;
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    WeightReader fWJetsWeightReader;
    WeightReader fTopPtWeightReader;
    WeightReader fEmbeddingGeneratorWeightReader;
    WeightReader fEmbeddingWTauMuWeightReader;
    VertexAssignmentAnalysis fVertexAssignmentAnalysis;
    FakeTauIdentifier fFakeTauIdentifier;
    METFilters fMETFilters;
    QCDTailKiller fQCDTailKiller;
    TauEmbeddingMuonIsolationQuantifier fTauEmbeddingMuonIsolationQuantifier;

    SignalAnalysisTree fTree;

    // Scale factor uncertainties
    ScaleFactorUncertaintyManager fSFUncertaintiesAfterSelection;
    ScaleFactorUncertaintyManager fEWKFakeTausSFUncertaintiesAfterSelection;



    // Histograms
    
    // Vertex histograms
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;

    // Transverse mass for top algorithms
    WrappedTH1 *hTransverseMassTopSelection;
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH1 *hTransverseMassTopWithWSelection;
    WrappedTH1 *hTransverseMassTauVeto;
    WrappedTH1 *hTransverseMassFakeMetVeto;

    WrappedTH2 *hTransverseMassVsNjets;
    WrappedTH2 *hEWKFakeTausTransverseMassVsNjets;

    // Full mass histograms
    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hEWKFakeTausDeltaPhi;
    WrappedTH1 *hAlphaT;
    WrappedTH1 *hAlphaTInvMass;
    WrappedTH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauPhi;
    WrappedTH1 *hSelectedTauRtau;
    WrappedTH1 *hSelectedTauLeadingTrackPt;
    WrappedTH1 *hSelectedTauRtauAfterCuts;
    WrappedTH1 *hSelectedTauEtAfterCuts;
    WrappedTH1 *hSelectedTauEtaAfterCuts;
    WrappedTH1 *hEWKFakeTausSelectedTauEtAfterCuts;
    WrappedTH1 *hEWKFakeTausSelectedTauEtaAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet;

    WrappedTH1 *hSelectionFlow;
    WrappedTH2 *hSelectionFlowVsVertices;
    WrappedTH2 *hSelectionFlowVsVerticesEWKFakeTausBkg;

    // Histograms for jet flavour tagging efficiency calculation in MC
    // Pseudorapidity (eta)
    WrappedTH1 *hGenuineBJetEta;   
    WrappedTH1 *hGenuineBJetWithBTagEta;
    WrappedTH1 *hGenuineGJetEta;
    WrappedTH1 *hGenuineGJetWithBTagEta;
    WrappedTH1 *hGenuineUDSJetEta;
    WrappedTH1 *hGenuineUDSJetWithBTagEta;
    WrappedTH1 *hGenuineCJetEta;
    WrappedTH1 *hGenuineCJetWithBTagEta;
    WrappedTH1 *hGenuineLJetEta;
    WrappedTH1 *hGenuineLJetWithBTagEta;
    // Transverse momentum (pT)
    WrappedTH1 *hGenuineBJetPt;   
    WrappedTH1 *hGenuineBJetWithBTagPt;
    WrappedTH1 *hGenuineGJetPt;
    WrappedTH1 *hGenuineGJetWithBTagPt;
    WrappedTH1 *hGenuineUDSJetPt;
    WrappedTH1 *hGenuineUDSJetWithBTagPt;
    WrappedTH1 *hGenuineCJetPt;
    WrappedTH1 *hGenuineCJetWithBTagPt;
    WrappedTH1 *hGenuineLJetPt;
    WrappedTH1 *hGenuineLJetWithBTagPt;
    // Two-dimensional histograms of pT vs. eta to investigate possible correlations
    WrappedTH2 *hGenuineBJetPtAndEta;
    WrappedTH2 *hGenuineBJetWithBTagPtAndEta;
    WrappedTH2 *hGenuineGJetPtAndEta;
    WrappedTH2 *hGenuineGJetWithBTagPtAndEta;
    WrappedTH2 *hGenuineUDSJetPtAndEta;
    WrappedTH2 *hGenuineUDSJetWithBTagPtAndEta;
    WrappedTH2 *hGenuineCJetPtAndEta;
    WrappedTH2 *hGenuineCJetWithBTagPtAndEta;
    WrappedTH2 *hGenuineLJetPtAndEta;
    WrappedTH2 *hGenuineLJetWithBTagPtAndEta;


    // Control plots for fakes

    // TTBar decay mode
    WrappedTH1 *hTTBarDecayModeAfterVertexSelection;
    WrappedTH1 *hTTBarDecayModeAfterVertexSelectionUnweighted;
    WrappedTH1 *hTTBarDecayModeAfterStandardSelections;
    WrappedTH1 *hTTBarDecayModeAfterStandardSelectionsUnweighted;
    WrappedTH1 *hTTBarDecayModeAfterMtSelections;
    WrappedTH1 *hTTBarDecayModeAfterMtSelectionsUnweighted;

    // FIXME move these to common plots
    WrappedTH2* hCtrlJetMatrixAfterJetSelection;
    WrappedTH2* hCtrlJetMatrixAfterMET;
    WrappedTH2* hCtrlJetMatrixAfterMET100;

    // CounterGroups for EWK fake taus (aka non-QCD type 2)
    CounterGroup fEWKFakeTausGroup;
    CounterGroup fAllTausCounterGroup;
    CounterGroup fElectronToTausCounterGroup;
    CounterGroup fElectronFromTauDecayToTausCounterGroup;
    CounterGroup fMuonToTausCounterGroup;
    CounterGroup fMuonFromTauDecayToTausCounterGroup;
    CounterGroup fGenuineToTausCounterGroup;
    CounterGroup fGenuineOneProngToTausCounterGroup;
    CounterGroup fJetToTausCounterGroup;
    CounterGroup fAllTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fElectronToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fElectronFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fMuonToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fMuonFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fGenuineToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fGenuineOneProngToTausAndTauJetInsideAcceptanceCounterGroup;
    CounterGroup fJetToTausAndTauJetInsideAcceptanceCounterGroup;

    WrappedTH1 *hEMFractionAll;
    WrappedTH1 *hEMFractionElectrons;

    std::string fModuleLabel;

    bool fProduce;
    bool fOnlyEmbeddingGenuineTaus;
    
    // FIXME move these to common plots
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode0;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode1;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode2;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode0NoNeutralHadrons;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode1NoNeutralHadrons;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode2NoNeutralHadrons;

    // Common plots
    CommonPlots fCommonPlots;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterVertexSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeight;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMET;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETWithPhiOscillationCorrection; // temporary
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTagging;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBackToBackDeltaPhi;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelected;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTail;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMass;
    // Probabilistic b tag as event weight (note: for invariant mass, b tag is needed!)
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagAfterBTagging;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhi;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagSelected;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagSelectedMtTail;

    // EWK fake taus background
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelectionEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeightEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVetoEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVetoEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelectionEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTaggingEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBackToBackDeltaPhiEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTailEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMassEWKFakeTausBkg;
    // Probabilistic b tag as event weight (note: for invariant mass, b tag is needed!)
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagAfterBTaggingEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhiEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagSelectedEWKFakeTausBkg;
    CommonPlotsFilledAtEveryStep* fCommonPlotsProbabilisticBTagSelectedMtTailEWKFakeTausBkg;
  };
}

#endif
