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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithMHSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"
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
      void incrementTopSelectionCounter() { increment(fTopSelectionCounter); }
      void incrementTopChiSelectionCounter() { increment(fTopChiSelectionCounter); }
      void incrementSelectedEventsCounter() { increment(fSelectedEventsCounter); }
      void incrementSelectedEventsFullMassCounter() { increment(fSelectedEventsFullMassCounter); }

    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fNJetsCounter;
      Count fDeltaPhiCollinearCounter;
      Count fMETCounter;
      Count fBTaggingCounter;
      Count fDeltaPhiBackToBackCounter;
      Count fTopSelectionCounter;
      Count fTopChiSelectionCounter;
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
    void fillSelectionFlowAndCounterGroups(int nVertices, FakeTauIdentifier::Data& tauMatchData, SignalSelectionOrder selection, const TauSelection::Data& tauData);
    CounterGroup* getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch);
    void fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData);
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
    Count fWJetsWeightCounter;
    Count fMETFiltersCounter;
    Count fEmbeddingMuonEfficiencyCounter;
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
    Count fMETTriggerScaleFactorCounter;
    Count fQCDTailKillerCollinearCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fQCDTailKillerBackToBackCounter;
    Count fTopReconstructionCounter;
    Count fSelectedEventsCounter;
    Count fHiggsMassSelectionCounter;
    Count fFakeMETVetoCounter;

    Count fTauVetoAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiCounter;
    Count fRealTauAfterDeltaPhiTauVetoCounter;

    Count fElectronNotInTauCounter;
    Count fElectronNotInTauFromWCounter;
    Count fElectronNotInTauFromBottomCounter;
    Count fElectronNotInTauFromTauCounter;

    Count fMuonNotInTauCounter;
    Count fMuonNotInTauFromWCounter;
    Count fMuonNotInTauFromBottomCounter;
    Count fMuonNotInTauFromTauCounter;

    Count fTauNotInTauCounter;
    Count fTauNotInTauFromWCounter;
    Count fTauNotInTauFromBottomCounter;
    Count fTauNotInTauFromHplusCounter;

    Count fObservableMuonsCounter;
    Count fObservableElectronsCounter;
    Count fObservableTausCounter;

    Count fTauIsHadronFromHplusCounter;
    Count fTauIsElectronFromHplusCounter;
    Count fTauIsMuonFromHplusCounter;
    Count fTauIsQuarkFromWCounter;
    Count fTauIsQuarkFromZCounter;
    Count fTauIsElectronFromWCounter;
    Count fTauIsElectronFromZCounter;
    Count fTauIsMuonFromWCounter;
    Count fTauIsHadronFromWTauCounter;
    Count fTauIsElectronFromWTauCounter;
    Count fTauIsMuonFromWTauCounter;
    Count fTauIsMuonFromZCounter;
    Count fTauIsHadronFromZTauCounter;
    Count fTauIsElectronFromZTauCounter;
    Count fTauIsMuonFromZTauCounter;
    Count fTauIsElectronFromBottomCounter;
    Count fTauIsMuonFromBottomCounter;
    Count fTauIsHadronFromBottomCounter;
    Count fTauIsElectronFromJetCounter;
    Count fTauIsMuonFromJetCounter;
    Count fTauIsHadronFromJetCounter;

    // Counters for different top algorithms
    Count fTopSelectionCounter;
    Count fTopChiSelectionCounter;
    Count fTopWithMHSelectionCounter;
    Count fTopWithBSelectionCounter;
    Count fTopWithWSelectionCounter;

    
    
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
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    TopSelection fTopSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    TopWithWSelection fTopWithWSelection;
    //    TopWithMHSelection fTopWithMHSelection;
    BjetSelection fBjetSelection;
    //    BjetWithPtSelection fBjetWithPtSelection;
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    EmbeddingMuonEfficiency fEmbeddingMuonEfficiency;
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    WeightReader fWJetsWeightReader;
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

    // MCAnalysis histograms
    WrappedTH1 *hgenWmass;
    WrappedTH1 *hGenMET;
    WrappedTH1 *hdeltaPhiMetGenMet;
    WrappedTH1 *hdeltaEtMetGenMet;
    WrappedTH1 *htransverseMassMuonNotInTau;
    WrappedTH1 *htransverseMassElectronNotInTau;
    WrappedTH1 *htransverseMassTauNotInTau;
    WrappedTH1 *htransverseMassMetReso02;
    WrappedTH1 *htransverseMassLeptonNotInTau;
    WrappedTH1 *htransverseMassNoLeptonNotInTau;
    WrappedTH1 *htransverseMassNoLeptonGoodMet;
    WrappedTH1 *htransverseMassNoLeptonGoodMetGoodTau;
    WrappedTH1 *htransverseMassLeptonRealSignalTau;
    WrappedTH1 *htransverseMassLeptonFakeSignalTau;
    WrappedTH1 *htransverseMassNoObservableLeptons;
    WrappedTH1 *htransverseMassObservableLeptons;

    // Transverse mass histogram
    

    // Transverse mass for top algorithms
    WrappedTH1 *hTransverseMassTopSelection;
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassWmassCut;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH1 *hTransverseMassTopWithWSelection;

    WrappedTH1 *hTransverseMassMET70;
    WrappedTH1 *hTransverseMassTauVeto;
    WrappedTH1 *hTransverseMassAfterDeltaPhi;
    
    WrappedTH1 *hTransverseMassFakeMetVeto;
    WrappedTH1 *hTransverseMassAfterDeltaPhi160;
    WrappedTH1 *hTransverseMassAfterDeltaPhi130;
    WrappedTH1 *hTransverseMassAfterDeltaPhi90;
    WrappedTH2 *hDeltaPhiVsTransverseMass;
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
    WrappedTH2 *hSelectionFlowVsVerticesFakeTaus;

    // Control plots for fakes


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
    CounterGroup fAllTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fElectronFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fMuonFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fGenuineOneProngToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fJetToTausAndTauOutsideAcceptanceCounterGroup;

    WrappedTH1 *hEMFractionAll;
    WrappedTH1 *hEMFractionElectrons;

    std::string fModuleLabel;

    bool fProduce;
    bool fOnlyGenuineTaus; 
    
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
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelected;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTail;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMass;

    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeightFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTaggingFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTailFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMassFakeTaus;

  };
}

#endif
