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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"



namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}



class TTree;

namespace HPlus {
  class SignalAnalysisInvertedTau {
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
      void incrementTopChiSelectionCounter() { increment(fTopChiSelectionCounter); }
      void incrementTopWithBSelectionCounter() { increment(fTopWithBSelectionCounter); }
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
      Count fTopChiSelectionCounter;
      Count fTopWithBSelectionCounter;
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
    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau);
    CounterGroup* getCounterGroupByTauMatch(MCSelectedTauMatchType tauMatch);
    void fillNonQCDTypeIICounters(MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData, bool passedStatus = true, double value = 0);

    bool doInvertedAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData);
    bool doBaselineAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisInvertedTauProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;


    //    const double ftransverseMassCut;
    const bool bBlindAnalysisStatus;
    const double fDeltaPhiCutValue;
    Count fAllCounter;
    Count fWJetsWeightCounter;
    Count fVertexFilterCounter;
    Count fMETFiltersCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTauCandidateCounter;
    Count fNprongsAfterTauIDCounter;
    Count fRtauAfterTauIDCounter;
    Count fTausExistCounter;
    Count fTauFakeScaleFactorBaselineCounter;
    Count fTauTriggerScaleFactorBaselineCounter;

    Count fOneTauCounter; 

    Count fBaselineTauIDCounter;
    Count fBaselineEvetoCounter;
    Count fBaselineMuvetoCounter;
    Count fBaselineJetsCounter;
    Count fBaselineMetCounter;
    Count fBaselineBtagCounter;
    Count fBTaggingScaleFactorCounter;
    Count fBaselineDeltaPhiTauMETCounter;
    //    Count fBaselineDeltaPhiMHTJet1CutCounter;
    Count fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter;

  
    Count fTauVetoAfterTauIDCounter;

    Count fTauFakeScaleFactorCounter;
    Count fTauTriggerScaleFactorCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingBeforeMETCounter;
    Count fMETCounter;
    Count fBjetVetoCounter;
    Count fBvetoCounter;
    Count fBvetoDeltaPhiCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorInvertedCounter;
    Count fQCDTailKillerCounter;
    Count fDeltaPhiTauMETCounter;
    Count fDeltaPhiVSDeltaPhiMETJet1CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet2CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet3CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet4CutCounter;
    Count fDeltaPhiAgainstTTCutCounter;
    Count fHiggsMassCutCounter;
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
    //    TauSelection fOneProngTauSelection;
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
    SignalAnalysisTree fTree;
  

    // Histograms
    WrappedTH1 *hTauDiscriminator;
    WrappedTH1 *hOneProngRtauPassedInvertedTaus;
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;
    WrappedTH1 *hVerticesTriggeredBeforeWeight;
    WrappedTH1 *hVerticesTriggeredAfterWeight;
    WrappedTH1 *hTransverseMass;
    WrappedTH1 *hTransverseMassWithTopCut;

    WrappedTH1 *hTransverseMassBeforeVeto;
    WrappedTH1 *hTransverseMassNoMet;
    WrappedTH1 *hTransverseMassNoMetBtag;
 
    WrappedTH2 *hTransverseMassVsDphi;
   
   
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    //    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hDeltaPhiAfterVeto;
    WrappedTH1 *hDeltaPhiAfterJets;
    WrappedTH1 *hDeltaPhiBeforeVeto;
    WrappedTH1 *hDeltaPhiJetMet;


    // Histograms for validation at every Selection Cut step
    WrappedTH1 *hMet_AfterTauSelection;
    WrappedTH1 *hMet_AfterEvtTopology;
    WrappedTH1 *hMETBeforeMETCut;
    WrappedTH1 *hMETBeforeTauId;

    // baseline MET histos
    HistogramsInBins *hMETBaselineTauId;
    HistogramsInBins *hMETBaselineTauIdJets;
    HistogramsInBins *hMETBaselineTauIdBtag;
    HistogramsInBins *hMETBaselineTauIdBveto;
    // baseline MT histos
    HistogramsInBins *hMTBaselineTauIdJet;
    HistogramsInBins *hMTBaselineTauIdBtag;
    HistogramsInBins *hMTBaselineTauIdBveto;
    HistogramsInBins *hMTBaselineTauIdBvetoDphi;
    HistogramsInBins *hMTBaselineTauIdPhi;
    HistogramsInBins *hMTBaselineThirdDeltaPhiCut;


    WrappedTH1 *hDeltaR_TauMETJet1MET;
    WrappedTH1 *hDeltaR_TauMETJet2MET;
    WrappedTH1 *hDeltaR_TauMETJet3MET;
    WrappedTH1 *hDeltaR_TauMETJet4MET;

    WrappedTH1 *hNBBaselineTauIdJet;    
    WrappedTH1 *hNJetBaselineTauId;
    WrappedTH1 *hDeltaPhiBaseline;
    WrappedTH1 *hNJetBaselineTauIdMet;
 


    HistogramsInBins *hMETInvertedTauId;
    HistogramsInBins *hNJetInvertedTauId;  
    HistogramsInBins *hNJetInvertedTauIdMet;
    HistogramsInBins *hMETInvertedTauIdJets;
    HistogramsInBins *hMETInvertedTauIdBtag;  
    HistogramsInBins *hMETInvertedTauIdBveto;
    HistogramsInBins *hMet_AfterBTagging;
    HistogramsInBins *hNBInvertedTauIdJet;
    HistogramsInBins *hNBInvertedTauIdJetDphi;  
    HistogramsInBins *hDeltaPhiInvertedNoB;
    HistogramsInBins *hDeltaPhiInverted;  

    //    HistogramsInBins *hDeltaPhiMHTJet1Inverted;


    HistogramsInBins *hMTInvertedTauIdJet;
    HistogramsInBins *hMTInvertedTauIdPhi; 
    HistogramsInBins *hMTInvertedNoBtaggingDphiCuts;
    HistogramsInBins *hMTInvertedTauIdBveto;
    HistogramsInBins *hMTInvertedTauIdBtag;
    HistogramsInBins *hMTInvertedTauIdBvetoDphi;
    HistogramsInBins *hMTInvertedTauIdJetDphi;
    HistogramsInBins *hMTInvertedSecondDeltaPhiCut;   
    HistogramsInBins *hMTInvertedFirstDeltaPhiCut;
    HistogramsInBins *hMTInvertedThirdDeltaPhiCut;
    HistogramsInBins *hMTInvertedAgainstTTCut;
    HistogramsInBins *hTopMass;
    HistogramsInBins *hHiggsMass;
    HistogramsInBins *hHiggsMassPhi;



    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiMETJet1Inverted; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiMETJet2Inverted;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiMETJet3Inverted; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiMETJet4Inverted;   
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiMETJet2InvertedAfterCut;



   
    WrappedTH1 *hMTInvertedTauIdJets; 
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauPhi;
    WrappedTH1 *hSelectedTauRtau;
    WrappedTH1 *hSelectedTauLeadingTrackPt;
    WrappedTH1 *hSelectedTauEtMetCut;
    WrappedTH1 *hSelectedTauEtaMetCut;
    WrappedTH1 *hSelectedTauPhiMetCut;
    WrappedTH1 *hSelectedTauEtAfterCuts;
    WrappedTH1 *hSelectedTauEtaAfterCuts;
    WrappedTH1 *hMetAfterCuts;
    WrappedTH1 *hNonQCDTypeIISelectedTauEtAfterCuts;
    WrappedTH1 *hNonQCDTypeIISelectedTauEtaAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 
    WrappedTH1 *hSelectedTauRtauMetCut;

    WrappedTH1 *hSelectionFlow;

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



    bool fProduce;
    bool fOnlyGenuineTaus; 
  };
}

#endif
