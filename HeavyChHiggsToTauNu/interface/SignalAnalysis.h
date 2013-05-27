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
      Count fNJetsCounter;
      Count fMETCounter;
      //      Count fRtauAfterMetCounter;
      Count fBTaggingCounter;
      Count fDeltaPhiCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
      Count fTopChiSelectionCounter;
      //      Count fTopChiSelectionNarrowCounter;
      Count fTopWithMHSelectionCounter;
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
  explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~SignalAnalysis();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    CounterGroup* getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch);
    void fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData);
    void doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData);
    bool selectTailEvents(edm::Event& iEvent, const edm::EventSetup& iSetup);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper fHistoWrapper;
    const bool bBlindAnalysisStatus;
    const bool bTauEmbeddingStatus;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm
    //    const double ftransverseMassCut;

    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;


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
    //Count fElectronMatchingTauCounter;
    Count fMuonVetoCounter;
    Count fMetCutBeforeJetCutCounter;
    Count fNJetsCounter;
    Count fQCDTailKillerCollinearCounter;
    Count fMETTriggerScaleFactorCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fQCDTailKillerBackToBackCounter;
    Count fDeltaPhiTauMETCounter;
    Count fDeltaPhiVSDeltaPhiMETJet1CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet2CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet3CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet4CutCounter;
    Count fDeltaPhiAgainstTTCutCounter;
    Count fDeltaPtJetTauCounter;
    Count fBjetVetoCounter;
    Count fMetCut80Counter;
    Count fMetCut100Counter;
    Count fHiggsMassCutCounter;
    Count fTransverseMass100CutCounter;
    Count fTransverseMass120CutCounter;
    Count fTransverseMass150CutCounter;
    //    Count fTransverseMass100CutPhiLow30Counter;
    //    Count fTransverseMass100CutPhiLow60Counter;
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

    Count fTopSelectionCounter;
    Count fTopWithMHSelectionCounter;
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
    WrappedTH1 *hVerticesTriggeredBeforeWeight;
    WrappedTH1 *hVerticesTriggeredAfterWeight;

    // MCAnalysis histograms
    
    WrappedTH2 *hDeltaPhiVsDeltaPhiMETJet1;
    WrappedTH2 *hDeltaPhiVsDeltaPhiMETJet2;
    WrappedTH2 *hDeltaPhiVsDeltaPhiMETJet3;
    WrappedTH2 *hDeltaPhiVsDeltaPhiMETJet4;
    WrappedTH1 *hDeltaPhiMETJet1;
    WrappedTH1 *hgenWmass;
    WrappedTH1 *hGenMET;
    WrappedTH1 *hdeltaPhiMetGenMet;
    WrappedTH1 *hdeltaEtMetGenMet;
    WrappedTH1 *hTransverseMassAgainstTTCut;
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
    WrappedTH1 *htransverseMassElectronFromTauFound;
    WrappedTH1 *htransverseMassElectronFromWFound;
    WrappedTH1 *htransverseMassElectronFromBottomFound;
    WrappedTH1 *htransverseMassElectronFound;
    WrappedTH1 *htransverseMassMuonFromTauFound;
    WrappedTH1 *htransverseMassMuonFromWFound;
    WrappedTH1 *htransverseMassMuonFromBottomFound;
    WrappedTH1 *htransverseMassMuonFound;
    WrappedTH1 *htransverseMassTauFromWFound;
    WrappedTH1 *htransverseMassTauFound;
    WrappedTH1 *hDeltaR_TauMETJet1MET;
    WrappedTH1 *hDeltaR_TauMETJet2MET;
    WrappedTH1 *hDeltaR_TauMETJet3MET;
    WrappedTH1 *hDeltaR_TauMETJet4MET;
    WrappedTH1 *hDeltaPhiTauMET;

    // Transverse mass histograms
    WrappedTH1 *hTransverseMass;
    WrappedTH1 *hTransverseMassAfterBtagging;
    WrappedTH1 *hTransverseMassDeltaPhiJet1;
    WrappedTH1 *hTransverseMassDeltaPhiJet2;
    WrappedTH1 *hTransverseMassDeltaPhiJet3;
    WrappedTH1 *hTransverseMassDeltaPhiJet4;    
    WrappedTH1 *hTransverseMassSecondBveto;
    WrappedTH1 *hTransverseMassMet80;
    WrappedTH1 *hTransverseMassMet100;
    WrappedTH1 *hTransverseMassNoBtagging;
    WrappedTH1 *hTransverseMassTopSelection;
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassWmassCut;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH1 *hTransverseMassTopWithWSelection;
    WrappedTH1 *hTransverseMassMET70;
    WrappedTH1 *hTransverseMassTauVeto;
    WrappedTH1 *hTransverseMassAfterDeltaPhi;
    WrappedTH1 *hEWKFakeTausTransverseMass;
    WrappedTH2 *hTransverseMassVsNjets;
    WrappedTH2 *hEWKFakeTausTransverseMassVsNjets;
    WrappedTH1 *hDeltaPtJetTau;
    WrappedTH1 *hDeltaRJetTau;


    // Full mass histograms
    WrappedTH1 *hFullMass;
    WrappedTH1 *hEWKFakeTausFullMass;

    WrappedTH1 *hDeltaPhiNoBtagging;
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
    WrappedTH1 *hMet_beforeJetCut;
    WrappedTH1 *hMetWithBtagging;
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
    //    WrappedTH1* hDeltaPtJetTau;
    //    WrappedTH1* hDeltaRJetTau;
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
    WrappedTH1* hCtrlNjetsBeforeCollinearCuts;
    WrappedTH1* hCtrlMET;
    WrappedTH1* hCtrlNbjets;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBack;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinear;

    WrappedTH1* hCtrlQCDTailKillerJet1BackToBack;
    WrappedTH1* hCtrlQCDTailKillerJet2BackToBack;
    WrappedTH1* hCtrlQCDTailKillerJet3BackToBack;
    WrappedTH1* hCtrlQCDTailKillerJet4BackToBack;
    WrappedTH1* hCtrlQCDTailKillerJet1Collinear;
    WrappedTH1* hCtrlQCDTailKillerJet2Collinear;
    WrappedTH1* hCtrlQCDTailKillerJet3Collinear;
    WrappedTH1* hCtrlQCDTailKillerJet4Collinear;
    // Control plots for fakes
    WrappedTH1* hCtrlEWKFakeTausIdentifiedElectronPt;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedMuonPt;
    WrappedTH1* hCtrlEWKFakeTausNjets;
    WrappedTH1* hCtrlEWKFakeTausNjetsAfterMET;
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
    WrappedTH1* hCtrlEWKFakeTausNjetsBeforeCollinearCuts;
    WrappedTH1* hCtrlEWKFakeTausMET;
    WrappedTH1* hCtrlEWKFakeTausNbjets;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBack;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinear;

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
    
    
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode0;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode1;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode2;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode0NoNeutralHadrons;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode1NoNeutralHadrons;
    WrappedTH1 *hReferenceJetToTauDeltaPtDecayMode2NoNeutralHadrons;

    // Common plots
    CommonPlots fCommonPlots;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTrigger;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterVertexSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeight;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMET;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTagging;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelected;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTail;

    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeightFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTaggingFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTailFakeTaus;

  };
}

#endif
