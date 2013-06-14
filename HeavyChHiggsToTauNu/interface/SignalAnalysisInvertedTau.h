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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins2Dim.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

namespace HPlus {
  class SignalAnalysisInvertedTau {

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
    enum QCDSelectionOrder {
      kQCDOrderVertexSelection,
      kQCDOrderTrigger,
      kQCDOrderTauCandidateSelection,
      kQCDOrderTauID,
      kQCDOrderElectronVeto,
      kQCDOrderMuonVeto,
      kQCDOrderJetSelection,
      kQCDOrderMET,
      kQCDOrderBTag,
      kQCDOrderDeltaPhiTauMET,
      kQCDOrderMaxDeltaPhiJetMET,
      kQCDOrderTopSelection
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
    explicit SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~SignalAnalysisInvertedTau();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool doInvertedAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData);
    bool doBaselineAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData, bool myFakeTauStatus);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisInvertedTauProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;


    //    const double ftransverseMassCut;
    const bool bBlindAnalysisStatus;
    const double fDeltaPhiCutValue;
    // Common counters
    Count fAllCounter;
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
    Count fBaselineMetTriggerScaleFactorCounter;
    Count fBaselineQCDTailKillerCollinearCounter;
    Count fBaselineMetCounter;
    Count fBaselineBTaggingScaleFactorCounter;
    Count fBaselineBtagCounter;
    Count fBaselineQCDTailKillerBackToBackCounter;
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
    Count fInvertedMetTriggerScaleFactorCounter;
    Count fInvertedQCDTailKillerCollinearCounter;
    Count fInvertedBTaggingBeforeMETCounter;
    Count fInvertedBjetVetoCounter;
    Count fInvertedMetCounter;
    Count fInvertedBvetoCounter;
    Count fInvertedBvetoDeltaPhiCounter;
    Count fInvertedBTaggingScaleFactorCounter;
    Count fInvertedBTaggingCounter;
    Count fInvertedQCDTailKillerBackToBackCounter;
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
    Count fTopSelectionCounter;
    Count fTopChiSelectionCounter;
    Count fTopWithBSelectionCounter;
    Count ftransverseMassCut100TopCounter;

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
    TopSelection fTopSelection;
    BjetSelection fBjetSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
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
    FakeTauIdentifier fFakeTauIdentifier;
    CommonPlots fCommonPlots;

    // Histograms
    WrappedTH1 *hOneProngRtauPassedInvertedTaus;
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;
    WrappedTH1 *hTransverseMassWithTopCut;
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH2 *hTransverseMassVsDphi;
    
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauEtAfterCuts;
    WrappedTH1 *hSelectedTauEtaAfterCuts;
    WrappedTH1 *hSelectedTauPhi;
    WrappedTH1 *hSelectedTauRtau;
    WrappedTH1 *hSelectedTauLeadingTrackPt;

    // baseline MET histos
    HistogramsInBins *hMETBaselineTauIdJetsCollinear;
    HistogramsInBins *hMETBaselineTauIdBvetoCollinear;
    //HistogramsInBins *hMETBaselineTauIdBvetoTailKiller;
    // baseline MT histos
    HistogramsInBins *hMTBaselineTauIdSoftBtaggingTK;
    HistogramsInBins *hMTBaselineTauIdBtag;
    HistogramsInBins *hMTBaselineTauIdBveto;
    HistogramsInBins *hMTBaselineTauIdBvetoTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoMetBveto;
    HistogramsInBins *hMTBaselineTauIdNoMetBvetoTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoMetNoBtagging;
    HistogramsInBins *hMTBaselineTauIdNoMetNoBtaggingTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoMetBtag;
    HistogramsInBins *hMTBaselineTauIdNoMetBtagTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoBtagging;
    HistogramsInBins *hMTBaselineTauIdNoBtaggingTailKiller;
    HistogramsInBins *hMTBaselineTauIdAllCutsTailKiller;

    // inverted MET histos
    HistogramsInBins *hMETInvertedTauIdJetsCollinear;
    HistogramsInBins *hMETInvertedTauIdBtag;
    HistogramsInBins *hMETInvertedTauIdBvetoCollinear;
    HistogramsInBins *hMETInvertedTauIdBveto;
    HistogramsInBins *hMETInvertedAllCutsTailKiller;
   
    // inverted MT histos
    HistogramsInBins *hMTInvertedTauIdSoftBtaggingTK;
    HistogramsInBins *hMTInvertedTauIdBtagNoMetCut;
    HistogramsInBins *hMTInvertedTauIdBvetoNoMetCut; 
    HistogramsInBins *hMTInvertedTauIdBvetoNoMetCutTailKiller; 
    HistogramsInBins *hMTInvertedTauIdJet;
    HistogramsInBins *hMTInvertedTauIdJetTailKiller;
    HistogramsInBins *hMTInvertedNoBtaggingTailKiller;
    HistogramsInBins *hMTInvertedTauIdNoBtagging;
    HistogramsInBins *hMTInvertedTauIdBveto;
    HistogramsInBins *hMTInvertedTauIdBtag;
    HistogramsInBins *hMTInvertedTauIdBvetoDphi;
    HistogramsInBins *hMTInvertedTauIdJetDphi;
    HistogramsInBins *hMTInvertedAllCutsTailKiller;
    

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
    //WrappedTH1* hQCDTailKillerJet0CollinearBaseline;
    //WrappedTH1* hQCDTailKillerJet1CollinearBaseline;
    //WrappedTH1* hQCDTailKillerJet2CollinearBaseline;
//     WrappedTH1* hQCDTailKillerJet3CollinearBaseline;




    WrappedTH1 *hDeltaR_TauMETJet1MET;
    WrappedTH1 *hDeltaR_TauMETJet2MET;
    WrappedTH1 *hDeltaR_TauMETJet3MET;
    WrappedTH1 *hDeltaR_TauMETJet4MET;

    WrappedTH1 *hNBBaselineTauIdJet;
    //WrappedTH1 *hNJetBaselineTauId;
    WrappedTH1 *hDeltaPhiBaseline;
    //WrappedTH1 *hNJetBaselineTauIdMet;
    HistogramsInBins *hNBInvertedTauIdJet;
    HistogramsInBins *hNBInvertedTauIdJetDphi;  
    HistogramsInBins *hDeltaPhiInvertedNoB;
    HistogramsInBins *hDeltaPhiInverted;  

    HistogramsInBins *hTopMass;

    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1Btagging;   

    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2Btagging;   

    WrappedTH1 *hSelectedTauEtTauVeto;
    HistogramsInBins *hSelectedTauEtJetCut;
    HistogramsInBins *hSelectedTauEtCollinearTailKiller;
    HistogramsInBins *hSelectedTauEtMetCut;
    HistogramsInBins *hSelectedTauEtBtagging;
    WrappedTH1 *hSelectedTauEtBjetVeto;
    WrappedTH1 *hSelectedTauEtBjetVetoPhiCuts;
    HistogramsInBins *hSelectedTauEtBackToBackTailKiller;
   
    WrappedTH1 *hMTInvertedTauIdJets; 

    WrappedTH1 *hSelectedTauEtaMetCut;
    WrappedTH1 *hSelectedTauPhiMetCut;
    WrappedTH1 *hMetAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 
    WrappedTH1 *hSelectedTauRtauMetCut;

    WrappedTH1 *hSelectionFlow;

    bool fProduce;
    bool fOnlyGenuineTaus; 
  };
}

#endif
