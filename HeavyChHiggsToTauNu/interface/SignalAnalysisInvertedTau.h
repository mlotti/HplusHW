// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisInvertedTau_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisInvertedTau_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins2Dim.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"



namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

namespace HPlus {
  class SignalAnalysisInvertedTau {
  public:
    explicit SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~SignalAnalysisInvertedTau();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool doInvertedAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const FakeTauIdentifier::Data& tauMatchData, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData);
    bool doBaselineAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const FakeTauIdentifier::Data& tauMatchData, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData);

    double getQCDEtaCorrectionFactor(double tauEta);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisInvertedTauProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;


    //    const double ftransverseMassCut;
    const bool bBlindAnalysisStatus;
    const bool bSelectOnlyGenuineTausForMC;
    const bool bMakeEtaCorrectionStatus;
    std::string fLowBoundForQCDInvertedIsolation;
    const double fDeltaPhiCutValue;
    // Common counters
    Count fAllCounter;
    Count fTopPtWeightCounter;
    Count fWJetsWeightCounter;
    Count fMETFiltersCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fVertexFilterCounter;
    Count fTauCandidateCounter;
    Count fNprongsAfterTauIDCounter;
    Count fRtauAfterTauIDCounter;
    // Baseline counters
    Count fBaselineTauIDCounter;
    Count fBaselineTauFakeScaleFactorCounter;
    Count fBaselineTauTriggerScaleFactorCounter;
    Count fBaselineOneTauCounter;
    Count fBaselineEvetoCounter;
    Count fBaselineMuvetoCounter;
    Count fBaselineJetsCounter;
    Count fBaselinePreMETCutCounter;
    Count fBaselineMetTriggerScaleFactorCounter;
    Count fBaselineQCDTailKillerCollinearCounter;
    Count fBaselineMetCounter;
    Count fBaselineBtagCounter;
    Count fBaselineBTaggingScaleFactorCounter;
    Count fBaselineQCDTailKillerBackToBackCounter;
    Count fBaselineTopSelectionCounter;
    Count fBaselineDeltaPhiTauMETCounter;
    Count fBaselineSelectedEventsCounter;
    Count fBaselineSelectedEventsInvariantMassCounter;
    // Inverted counters
    Count fInvertedTauIDCounter;
    Count fInvertedTauFakeScaleFactorCounter;
    Count fInvertedTauTriggerScaleFactorCounter;
    Count fInvertedOneTauCounter;
    Count fInvertedElectronVetoCounter;
    Count fInvertedMuonVetoCounter;
    Count fInvertedNJetsCounter;
    Count fInvertedPreMETCutCounter;
    Count fInvertedMetTriggerScaleFactorCounter;
    Count fInvertedQCDTailKillerCollinearCounter;
    Count fInvertedBTaggingBeforeMETCounter;
    Count fInvertedBjetVetoCounter;
    Count fInvertedMetCounter;
    Count fInvertedBvetoCounter;
    Count fInvertedBvetoDeltaPhiCounter;
    Count fInvertedBTaggingCounter;
    Count fInvertedBTaggingScaleFactorCounter;
    Count fInvertedQCDTailKillerBackToBackCounter;
    Count fInvertedTopSelectionCounter;
    Count fInvertedDeltaPhiTauMETCounter;
    Count fInvertedSelectedEventsCounter;
    Count fInvertedSelectedEventsInvariantMassCounter;
    // Other counters
//     Count fDeltaPhiVSDeltaPhiMETJet1CutCounter;
//     Count fDeltaPhiVSDeltaPhiMETJet2CutCounter;
//     Count fDeltaPhiVSDeltaPhiMETJet3CutCounter;
//     Count fDeltaPhiVSDeltaPhiMETJet4CutCounter;
//     Count fHiggsMassCutCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;

    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    ElectronSelection fElectronSelection;
    MuonSelection fMuonSelection;
    TauSelection fTauSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    BjetSelection fBjetSelection;
    TopSelectionManager fTopSelectionManager; 
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    METFilters fMETFilters;
    QCDTailKiller fQCDTailKiller;
    WeightReader fWJetsWeightReader;
    WeightReader fTopPtWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    //    CommonPlots fCommonPlots;

    // Histograms
   // Common plots                                                                                                                                                                                      
    CommonPlots fCommonPlots;
    CommonPlots fNormalizationSystematicsSignalRegion; // For normalization systematics plotting
    CommonPlots fNormalizationSystematicsControlRegion; // For normalization systematics plotting

    WrappedTH1 *hTauDiscriminator;

    WrappedTH1 *hOneProngRtauPassedInvertedTaus;
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;

//     WrappedTH1* hQCDTailKillerJet0BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet1BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet2BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet3BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet0CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet1CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet2CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet3CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet0BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet1BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet2BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet3BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet0CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet1CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet2CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet3CollinearBaseline;

    WrappedTH2 *hTransverseMassVsDphi;

    // Tau properties for inverted selection after tau ID + tau SF's
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterTauID;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtaAfterTauID;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauPhiAfterTauID;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauRtauAfterTauID;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauLeadingTrackPtAfterTauID;
    // Tau properties for inverted selection after MET cut
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterMetCut;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtaAfterMetCut;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauPhiAfterMetCut;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauRtauAfterMetCut;
    // Tau properties for inverted selection after all cuts
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterCuts;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtaAfterCuts;
    // Tau pt for inverted selection after a selection
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterTauVeto;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterJetCut;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterCollinearCuts;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterBtagging;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterBjetVeto;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterBjetVetoPhiCuts;
    std::vector<WrappedTH1*> hInvertedTauIdSelectedTauEtAfterBackToBackCuts;

    // baseline MET histos
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterJets;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterMetSF;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterMetSFPlusBtag;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterMetSFPlusBveto;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterCollinearCuts;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterCollinearCutsPlusBtag;
    std::vector<WrappedTH1*> hMETBaselineTauIdAfterCollinearCutsPlusBveto;
    // baseline MT histos
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMetSF;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCuts; // <-- used for closure test
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCutsPlusBtag;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCutsPlusBveto;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMet;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMetPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMetPlusBveto;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMetPlusBvetoPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterBtag;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterBackToBackCuts;
    std::vector<WrappedTH1*> hMTBaselineTauIdAfterTopReco;

    // baseline MT histos for closure test in control region
    std::vector<WrappedTH1*> hMTBaselineTauIdFinalReversedBtag;
    std::vector<WrappedTH1*> hMTBaselineTauIdFinalReversedBacktoBackDeltaPhi;
    // baseline invariant mass histos
    std::vector<WrappedTH1*> hInvMassBaselineTauIdAfterCollinearCuts; // <-- used for closure test
    std::vector<WrappedTH1*> hInvMassBaselineTauIdAfterCollinearCutsPlusBackToBackCuts;
    // baseline invariant mass histos for closure test in control region
    std::vector<WrappedTH1*> hInvMassBaselineTauIdFinalReversedBtag;
    std::vector<WrappedTH1*> hInvMassBaselineTauIdFinalReversedBacktoBackDeltaPhi;

    // inverted MET histos
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterJets;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterMetSF;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterMetSFPlusBtag;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterMetSFPlusBveto;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterCollinearCuts;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterCollinearCutsPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterCollinearCutsPlusBtag;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterCollinearCutsPlusBveto;
    std::vector<WrappedTH1*> hMETInvertedTauIdAfterBackToBackCuts;
    // inverted MT histos
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMetSF;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCuts; // <-- used for closure test
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCutsPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCutsPlusBtag;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCutsPlusBveto;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMet;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMetPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMetPlusBveto;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMetPlusBvetoPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterMetPlusSoftBtaggingPlusBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterBtag;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterBackToBackCuts;
    std::vector<WrappedTH1*> hMTInvertedTauIdAfterTopReco;

    // inverted MT histos for closure test in control region
    std::vector<WrappedTH1*> hMTInvertedTauIdFinalReversedBtag;
    std::vector<WrappedTH1*> hMTInvertedTauIdFinalReversedBacktoBackDeltaPhi;
    // inverted invariant mass histos
    std::vector<WrappedTH1*> hInvMassInvertedTauIdAfterCollinearCuts; // <-- used for closure test
    std::vector<WrappedTH1*> hInvMassInvertedTauIdAfterCollinearCutsPlusBackToBackCuts;
    // baseline invariant mass histos for closure test in control region
    std::vector<WrappedTH1*> hInvMassInvertedTauIdFinalReversedBtag;
    std::vector<WrappedTH1*> hInvMassInvertedTauIdFinalReversedBacktoBackDeltaPhi;

//     WrappedTH1* hQCDTailKillerJet0BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet1BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet2BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet3BackToBackInverted;
//     WrappedTH1* hQCDTailKillerJet0CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet1CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet2CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet3CollinearInverted;
//     WrappedTH1* hQCDTailKillerJet0BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet1BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet2BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet3BackToBackBaseline;
//     WrappedTH1* hQCDTailKillerJet0CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet1CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet2CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet3CollinearBaseline;

//     WrappedTH1 *hDeltaR_TauMETJet1MET;
//     WrappedTH1 *hDeltaR_TauMETJet2MET;
//     WrappedTH1 *hDeltaR_TauMETJet3MET;
//     WrappedTH1 *hDeltaR_TauMETJet4MET;

    WrappedTH1 *hNBBaselineTauIdJet;
    //WrappedTH1 *hNJetBaselineTauId;
    WrappedTH1 *hDeltaPhiBaseline;
    //WrappedTH1 *hNJetBaselineTauIdMet;
    std::vector<WrappedTH1*> hNBInvertedTauIdJet;
    std::vector<WrappedTH1*> hNBInvertedTauIdJetDphi;  
    std::vector<WrappedTH1*> hDeltaPhiInvertedNoB;
    std::vector<WrappedTH1*> hDeltaPhiInverted;  

    //std::vector<WrappedTH1*> hTopMass;

    /*HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1Btagging;   

    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2Btagging;   */

    WrappedTH1 *hMTInvertedTauIdJets; 

    WrappedTH1 *hMetAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 

    WrappedTH1 *hSelectionFlow;

    // Common plots at every step for baseline
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMetSF;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCutsPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCutsPlusBtag;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCutsPlusBtagPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCutsPlusBveto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterCollinearCutsPlusBvetoPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMet;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMetPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMetPlusBveto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMetPlusBvetoPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMetPlusSoftBtaggingPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterMETAndBtagWithSF;
    CommonPlotsFilledAtEveryStep* fCommonPlotsBaselineAfterBackToBackCuts;

    // Common plots at every step for baseline
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMetSF;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCutsPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCutsPlusBtag;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCutsPlusBtagPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCutsPlusBveto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterCollinearCutsPlusBvetoPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMet;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMetPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMetPlusBveto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMetPlusBvetoPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMetPlusSoftBtaggingPlusBackToBackCuts;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterMETAndBtagWithSF;
    CommonPlotsFilledAtEveryStep* fCommonPlotsInvertedAfterBackToBackCuts;

    bool fProduce;
    bool fOnlyGenuineTaus; 
  };
}

#endif
