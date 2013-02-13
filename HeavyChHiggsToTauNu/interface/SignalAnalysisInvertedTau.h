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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
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
    Count fTauFakeScaleFactorCounter;
    Count fTriggerScaleFactorCounter;
    Count fBaselineTauIDCounter;
    Count fBaselineEvetoCounter;
    Count fBaselineMuvetoCounter;
    Count fBaselineJetsCounter;
    Count fBaselineMetCounter;
    Count fBaselineBtagCounter;
    Count fBTaggingScaleFactorCounter;
    Count fBaselineDeltaPhiTauMETCounter;
    Count fBaselineDphi160Counter;
    Count fOneTauCounter;  
    Count fBaselineDphi130Counter;
    Count fBaselineTopChiSelectionCounter;

  
    Count fTauVetoAfterTauIDCounter;

    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingBeforeMETCounter;
    Count fMETCounter;
    Count fRtauAfterMETCounter;
    Count fBjetVetoCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorInvertedCounter;    
    Count fDeltaPhiTauMETCounter;
    //    Count fDeltaPhiTauMET140Counter;
    Count fdeltaPhiTauMET10Counter;
    Count fHiggsMassCutCounter;
    Count fdeltaPhiTauMET160Counter;
    Count fdeltaPhiTauMET130Counter;
    Count fFakeMETVetoCounter;
    Count fdeltaPhiTauMET160FakeMetCounter;
    Count fTopRtauDeltaPhiFakeMETCounter;
    Count fRtauAfterCutsCounter;
    Count fForwardJetVetoCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;
    Count ftransverseMassCut80NoRtauCounter;
    Count ftransverseMassCut100NoRtauCounter;
    Count fZmassVetoCounter;
    Count fTopSelectionCounter;
    Count fTopChiSelectionCounter;
    Count fTopWithBSelectionCounter;
    Count ftransverseMassCut100TopCounter;

    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    //    NonIsolatedElectronVeto fNonIsolatedElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
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
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;

    VertexWeightReader fVertexWeightReader;
    METFilters fMETFilters;
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
    WrappedTH1 *hTransverseMassAfterVeto;
    WrappedTH1 *hTransverseMassBeforeVeto;
    WrappedTH1 *hTransverseMassNoMet;
    WrappedTH1 *hTransverseMassNoMetBtag;
    WrappedTH1 *hTransverseMassTopRtauDeltaPhiFakeMET;
    WrappedTH1 *hTransverseMassFakeMET;
   
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hDeltaPhiAfterVeto;
    WrappedTH1 *hDeltaPhiAfterJets;
    WrappedTH1 *hDeltaPhiBeforeVeto;
    WrappedTH1 *hDeltaPhiJetMet;


    // Histograms for validation at every Selection Cut step
    WrappedTH1 *hMet_AfterTauSelection;
    WrappedTH1 *hMet_AfterBTagging;
    WrappedTH1 *hMet_AfterEvtTopology;
    WrappedTH1 *hMETBeforeMETCut;
    WrappedTH1 *hMETBeforeTauId;
    WrappedTH1 *hMETBaselineTauId;
    WrappedTH1 *hMETInvertedTauId;
    WrappedTH1 *hMETBaselineTauIdJets;
    WrappedTH1 *hMETBaselineTauIdJets150;
    WrappedTH1 *hMETBaselineTauIdJets120;
    WrappedTH1 *hMETBaselineTauIdJets120150;
    WrappedTH1 *hMETBaselineTauIdJets100120;
    WrappedTH1 *hMETBaselineTauIdJets80100;
    WrappedTH1 *hMETBaselineTauIdJets7080;
    WrappedTH1 *hMETBaselineTauIdJets6070;
    WrappedTH1 *hMETBaselineTauIdJets5060;
    WrappedTH1 *hMETBaselineTauIdJets4050;

    WrappedTH1 *hNBBaselineTauIdJet;    
    WrappedTH1 *hNJetBaselineTauId;
    WrappedTH1 *hDeltaPhiBaseline;
    WrappedTH1 *hNJetBaselineTauIdMet;

    WrappedTH1 *hMETBaselineTauId150;
    WrappedTH1 *hMETBaselineTauId120;
    WrappedTH1 *hMETBaselineTauId120150;
    WrappedTH1 *hMETBaselineTauId100120;
    WrappedTH1 *hMETBaselineTauId80100;
    WrappedTH1 *hMETBaselineTauId7080;
    WrappedTH1 *hMETBaselineTauId6070;
    WrappedTH1 *hMETBaselineTauId5060;
    WrappedTH1 *hMETBaselineTauId4050;


    //    WrappedTH1 *hMETBaselineTauIdBtag;
    WrappedTH1 *hMETBaselineTauIdBtag150;
    WrappedTH1 *hMETBaselineTauIdBtag120;
    WrappedTH1 *hMETBaselineTauIdBtag120150;
    WrappedTH1 *hMETBaselineTauIdBtag100120;
    WrappedTH1 *hMETBaselineTauIdBtag80100;
    WrappedTH1 *hMETBaselineTauIdBtag7080;
    WrappedTH1 *hMETBaselineTauIdBtag6070;
    WrappedTH1 *hMETBaselineTauIdBtag5060;
    WrappedTH1 *hMETBaselineTauIdBtag4050;

    WrappedTH1 *hMETBaselineTauIdBveto;
    WrappedTH1 *hMETBaselineTauIdBveto150;
    WrappedTH1 *hMETBaselineTauIdBveto120;
    WrappedTH1 *hMETBaselineTauIdBveto120150;
    WrappedTH1 *hMETBaselineTauIdBveto100120;
    WrappedTH1 *hMETBaselineTauIdBveto80100;
    WrappedTH1 *hMETBaselineTauIdBveto7080;
    WrappedTH1 *hMETBaselineTauIdBveto6070;
    WrappedTH1 *hMETBaselineTauIdBveto5060;
    WrappedTH1 *hMETBaselineTauIdBveto4050;

    WrappedTH1 *hMTBaselineTauIdTopMass;
    WrappedTH1 *hMTBaselineTauIdTopMass150;
    WrappedTH1 *hMTBaselineTauIdTopMass120;
    WrappedTH1 *hMTBaselineTauIdTopMass120150;
    WrappedTH1 *hMTBaselineTauIdTopMass100120;
    WrappedTH1 *hMTBaselineTauIdTopMass80100;
    WrappedTH1 *hMTBaselineTauIdTopMass7080;
    WrappedTH1 *hMTBaselineTauIdTopMass6070;
    WrappedTH1 *hMTBaselineTauIdTopMass5060;
    WrappedTH1 *hMTBaselineTauIdTopMass4050;


    WrappedTH1 *hMETInvertedTauIdJets;
    WrappedTH1 *hMETInvertedTauIdJets150;
    WrappedTH1 *hMETInvertedTauIdJets120;
    WrappedTH1 *hMETInvertedTauIdJets120150;
    WrappedTH1 *hMETInvertedTauIdJets100120;
    WrappedTH1 *hMETInvertedTauIdJets80100;
    WrappedTH1 *hMETInvertedTauIdJets7080;
    WrappedTH1 *hMETInvertedTauIdJets6070;
    WrappedTH1 *hMETInvertedTauIdJets5060;
    WrappedTH1 *hMETInvertedTauIdJets4050;

    WrappedTH1 *hMETInvertedTauId150;
    WrappedTH1 *hMETInvertedTauId120;
    WrappedTH1 *hMETInvertedTauId120150;
    WrappedTH1 *hMETInvertedTauId100120;
    WrappedTH1 *hMETInvertedTauId80100;
    WrappedTH1 *hMETInvertedTauId7080;
    WrappedTH1 *hMETInvertedTauId6070;
    WrappedTH1 *hMETInvertedTauId5060;
    WrappedTH1 *hMETInvertedTauId4050;

    WrappedTH1 *hMETInvertedTauIdBtag;
    WrappedTH1 *hMETInvertedTauIdBtag150;
    WrappedTH1 *hMETInvertedTauIdBtag120;
    WrappedTH1 *hMETInvertedTauIdBtag120150;
    WrappedTH1 *hMETInvertedTauIdBtag100120;
    WrappedTH1 *hMETInvertedTauIdBtag80100;
    WrappedTH1 *hMETInvertedTauIdBtag7080;
    WrappedTH1 *hMETInvertedTauIdBtag6070;
    WrappedTH1 *hMETInvertedTauIdBtag5060;
    WrappedTH1 *hMETInvertedTauIdBtag4050;

    WrappedTH1 *hMETInvertedTauIdBveto;
    WrappedTH1 *hMETInvertedTauIdBveto150;
    WrappedTH1 *hMETInvertedTauIdBveto120;
    WrappedTH1 *hMETInvertedTauIdBveto120150;
    WrappedTH1 *hMETInvertedTauIdBveto100120;
    WrappedTH1 *hMETInvertedTauIdBveto80100;
    WrappedTH1 *hMETInvertedTauIdBveto7080;
    WrappedTH1 *hMETInvertedTauIdBveto6070;
    WrappedTH1 *hMETInvertedTauIdBveto5060;
    WrappedTH1 *hMETInvertedTauIdBveto4050;
 
    WrappedTH1 *hMTBaselineTauIdBtag150;
    WrappedTH1 *hMTBaselineTauIdBtag120;
    WrappedTH1 *hMTBaselineTauIdBtag120150;
    WrappedTH1 *hMTBaselineTauIdBtag100120;
    WrappedTH1 *hMTBaselineTauIdBtag80100;
    WrappedTH1 *hMTBaselineTauIdBtag7080;
    WrappedTH1 *hMTBaselineTauIdBtag6070;
    WrappedTH1 *hMTBaselineTauIdBtag5060;
    WrappedTH1 *hMTBaselineTauIdBtag4050;

    WrappedTH1 *hMTBaselineTauIdBveto;
    WrappedTH1 *hMTBaselineTauIdBveto150;
    WrappedTH1 *hMTBaselineTauIdBveto120;
    WrappedTH1 *hMTBaselineTauIdBveto120150;
    WrappedTH1 *hMTBaselineTauIdBveto100120;
    WrappedTH1 *hMTBaselineTauIdBveto80100;
    WrappedTH1 *hMTBaselineTauIdBveto7080;
    WrappedTH1 *hMTBaselineTauIdBveto6070;
    WrappedTH1 *hMTBaselineTauIdBveto5060;
    WrappedTH1 *hMTBaselineTauIdBveto4050;

    WrappedTH1 *hMTBaselineTauIdJet150;
    WrappedTH1 *hMTBaselineTauIdJet120;
    WrappedTH1 *hMTBaselineTauIdJet120150;
    WrappedTH1 *hMTBaselineTauIdJet100120;
    WrappedTH1 *hMTBaselineTauIdJet80100;
    WrappedTH1 *hMTBaselineTauIdJet7080;
    WrappedTH1 *hMTBaselineTauIdJet6070;
    WrappedTH1 *hMTBaselineTauIdJet5060;
    WrappedTH1 *hMTBaselineTauIdJet4050;

    WrappedTH1 *hMTBaselineTauIdPhi150;
    WrappedTH1 *hMTBaselineTauIdPhi120;
    WrappedTH1 *hMTBaselineTauIdPhi120150;
    WrappedTH1 *hMTBaselineTauIdPhi100120;
    WrappedTH1 *hMTBaselineTauIdPhi80100;
    WrappedTH1 *hMTBaselineTauIdPhi7080;
    WrappedTH1 *hMTBaselineTauIdPhi6070;
    WrappedTH1 *hMTBaselineTauIdPhi5060;
    WrappedTH1 *hMTBaselineTauIdPhi4050;
    WrappedTH1 *hMTBaselineTauIdPhi;

    WrappedTH1 *hMTInvertedTauIdJets;
    WrappedTH1 *hMTBaselineTauIdJet;

    WrappedTH1 *hMTInvertedTauIdPhi;
    WrappedTH1 *hMTInvertedTauIdPhi150;
    WrappedTH1 *hMTInvertedTauIdPhi120;
    WrappedTH1 *hMTInvertedTauIdPhi120150;
    WrappedTH1 *hMTInvertedTauIdPhi100120;
    WrappedTH1 *hMTInvertedTauIdPhi80100;
    WrappedTH1 *hMTInvertedTauIdPhi7080;
    WrappedTH1 *hMTInvertedTauIdPhi6070;
    WrappedTH1 *hMTInvertedTauIdPhi5060;
    WrappedTH1 *hMTInvertedTauIdPhi4050;

    WrappedTH1 *hMTInvertedTauIdJetWithRtau;
    WrappedTH1 *hMTInvertedTauIdJet;
    WrappedTH1 *hMTInvertedTauIdJet150;
    WrappedTH1 *hMTInvertedTauIdJet120;
    WrappedTH1 *hMTInvertedTauIdJet120150;
    WrappedTH1 *hMTInvertedTauIdJet100120;
    WrappedTH1 *hMTInvertedTauIdJet80100;
    WrappedTH1 *hMTInvertedTauIdJet7080;
    WrappedTH1 *hMTInvertedTauIdJet6070;
    WrappedTH1 *hMTInvertedTauIdJet5060;
    WrappedTH1 *hMTInvertedTauIdJet4050;

    WrappedTH1 *hMTInvertedTauIdBveto;
    WrappedTH1 *hMTInvertedTauIdBveto150;
    WrappedTH1 *hMTInvertedTauIdBveto120;
    WrappedTH1 *hMTInvertedTauIdBveto120150;
    WrappedTH1 *hMTInvertedTauIdBveto100120;
    WrappedTH1 *hMTInvertedTauIdBveto80100;
    WrappedTH1 *hMTInvertedTauIdBveto7080;
    WrappedTH1 *hMTInvertedTauIdBveto6070;
    WrappedTH1 *hMTInvertedTauIdBveto5060;
    WrappedTH1 *hMTInvertedTauIdBveto4050;

    WrappedTH1 *hNBInvertedTauIdJet;
    WrappedTH1 *hNBInvertedTauIdJet150;
    WrappedTH1 *hNBInvertedTauIdJet120;
    WrappedTH1 *hNBInvertedTauIdJet120150;
    WrappedTH1 *hNBInvertedTauIdJet100120;
    WrappedTH1 *hNBInvertedTauIdJet80100;
    WrappedTH1 *hNBInvertedTauIdJet7080;
    WrappedTH1 *hNBInvertedTauIdJet6070;
    WrappedTH1 *hNBInvertedTauIdJet5060;
    WrappedTH1 *hNBInvertedTauIdJet4050;

    WrappedTH1 *hNJetInvertedTauIdMet;
    WrappedTH1 *hNJetInvertedTauIdMet150;
    WrappedTH1 *hNJetInvertedTauIdMet120;
    WrappedTH1 *hNJetInvertedTauIdMet120150;
    WrappedTH1 *hNJetInvertedTauIdMet100120;
    WrappedTH1 *hNJetInvertedTauIdMet80100;
    WrappedTH1 *hNJetInvertedTauIdMet7080;
    WrappedTH1 *hNJetInvertedTauIdMet6070;
    WrappedTH1 *hNJetInvertedTauIdMet5060;
    WrappedTH1 *hNJetInvertedTauIdMet4050;

    WrappedTH1 *hNJetInvertedTauId;
    WrappedTH1 *hNJetInvertedTauId150;
    WrappedTH1 *hNJetInvertedTauId120;
    WrappedTH1 *hNJetInvertedTauId120150;
    WrappedTH1 *hNJetInvertedTauId100120;
    WrappedTH1 *hNJetInvertedTauId80100;
    WrappedTH1 *hNJetInvertedTauId7080;
    WrappedTH1 *hNJetInvertedTauId6070;
    WrappedTH1 *hNJetInvertedTauId5060;
    WrappedTH1 *hNJetInvertedTauId4050;

    WrappedTH1 *hNBInvertedTauIdJetDphi;
    WrappedTH1 *hNBInvertedTauIdJetDphi150;
    WrappedTH1 *hNBInvertedTauIdJetDphi120;
    WrappedTH1 *hNBInvertedTauIdJetDphi120150;
    WrappedTH1 *hNBInvertedTauIdJetDphi100120;
    WrappedTH1 *hNBInvertedTauIdJetDphi80100;
    WrappedTH1 *hNBInvertedTauIdJetDphi7080;
    WrappedTH1 *hNBInvertedTauIdJetDphi6070;
    WrappedTH1 *hNBInvertedTauIdJetDphi5060;
    WrappedTH1 *hNBInvertedTauIdJetDphi4050;

    WrappedTH1 *hMTInvertedTauIdJetDphi;
    WrappedTH1 *hMTInvertedTauIdJetDphi150;
    WrappedTH1 *hMTInvertedTauIdJetDphi120;
    WrappedTH1 *hMTInvertedTauIdJetDphi120150;
    WrappedTH1 *hMTInvertedTauIdJetDphi100120;
    WrappedTH1 *hMTInvertedTauIdJetDphi80100;
    WrappedTH1 *hMTInvertedTauIdJetDphi7080;
    WrappedTH1 *hMTInvertedTauIdJetDphi6070;
    WrappedTH1 *hMTInvertedTauIdJetDphi5060;
    WrappedTH1 *hMTInvertedTauIdJetDphi4050;

    WrappedTH1 *hMTInvertedTauIdBtag;
    WrappedTH1 *hMTInvertedTauIdBtag150;
    WrappedTH1 *hMTInvertedTauIdBtag120;
    WrappedTH1 *hMTInvertedTauIdBtag120150;
    WrappedTH1 *hMTInvertedTauIdBtag100120;
    WrappedTH1 *hMTInvertedTauIdBtag80100;
    WrappedTH1 *hMTInvertedTauIdBtag7080;
    WrappedTH1 *hMTInvertedTauIdBtag6070;
    WrappedTH1 *hMTInvertedTauIdBtag5060;
    WrappedTH1 *hMTInvertedTauIdBtag4050;

    WrappedTH1 *hMTInvertedTauIdMet;
    WrappedTH1 *hMTInvertedTauIdMet150;
    WrappedTH1 *hMTInvertedTauIdMet120;
    WrappedTH1 *hMTInvertedTauIdMet120150;
    WrappedTH1 *hMTInvertedTauIdMet100120;
    WrappedTH1 *hMTInvertedTauIdMet80100;
    WrappedTH1 *hMTInvertedTauIdMet7080;
    WrappedTH1 *hMTInvertedTauIdMet6070;
    WrappedTH1 *hMTInvertedTauIdMet5060;
    WrappedTH1 *hMTInvertedTauIdMet4050;

    WrappedTH1 *hMTInvertedTauIdJetPhi;
    WrappedTH1 *hMTInvertedTauIdJetPhi120;
    WrappedTH1 *hMTInvertedTauIdJetPhi150;
    WrappedTH1 *hMTInvertedTauIdJetPhi120150;
    WrappedTH1 *hMTInvertedTauIdJetPhi100120;
    WrappedTH1 *hMTInvertedTauIdJetPhi80100;
    WrappedTH1 *hMTInvertedTauIdJetPhi7080;
    WrappedTH1 *hMTInvertedTauIdJetPhi6070;
    WrappedTH1 *hMTInvertedTauIdJetPhi5060;
    WrappedTH1 *hMTInvertedTauIdJetPhi4050;

    WrappedTH1 *hDeltaPhiInverted;
    WrappedTH1 *hDeltaPhiInverted150;
    WrappedTH1 *hDeltaPhiInverted120;
    WrappedTH1 *hDeltaPhiInverted120150;
    WrappedTH1 *hDeltaPhiInverted100120;
    WrappedTH1 *hDeltaPhiInverted80100;
    WrappedTH1 *hDeltaPhiInverted7080;
    WrappedTH1 *hDeltaPhiInverted6070;
    WrappedTH1 *hDeltaPhiInverted5060;
    WrappedTH1 *hDeltaPhiInverted4050;

    WrappedTH1 *hDeltaPhiInvertedNoB;
    WrappedTH1 *hDeltaPhiInvertedNoB150;
    WrappedTH1 *hDeltaPhiInvertedNoB120;
    WrappedTH1 *hDeltaPhiInvertedNoB120150;
    WrappedTH1 *hDeltaPhiInvertedNoB100120;
    WrappedTH1 *hDeltaPhiInvertedNoB80100;
    WrappedTH1 *hDeltaPhiInvertedNoB7080;
    WrappedTH1 *hDeltaPhiInvertedNoB6070;
    WrappedTH1 *hDeltaPhiInvertedNoB5060;
    WrappedTH1 *hDeltaPhiInvertedNoB4050;

    WrappedTH1 *hTopMass;
    WrappedTH1 *hTopMass150;
    WrappedTH1 *hTopMass120;
    WrappedTH1 *hTopMass120150;
    WrappedTH1 *hTopMass100120;
    WrappedTH1 *hTopMass80100;
    WrappedTH1 *hTopMass7080;
    WrappedTH1 *hTopMass6070;
    WrappedTH1 *hTopMass5060;
    WrappedTH1 *hTopMass4050;

    WrappedTH1 *hHiggsMass;
    WrappedTH1 *hHiggsMass150;
    WrappedTH1 *hHiggsMass120;
    WrappedTH1 *hHiggsMass120150;
    WrappedTH1 *hHiggsMass100120;
    WrappedTH1 *hHiggsMass80100;
    WrappedTH1 *hHiggsMass7080;
    WrappedTH1 *hHiggsMass6070;
    WrappedTH1 *hHiggsMass5060;
    WrappedTH1 *hHiggsMass4050;

    WrappedTH1 *hHiggsMassPhi;
    WrappedTH1 *hHiggsMassPhi150;
    WrappedTH1 *hHiggsMassPhi120;
    WrappedTH1 *hHiggsMassPhi120150;
    WrappedTH1 *hHiggsMassPhi100120;
    WrappedTH1 *hHiggsMassPhi80100;
    WrappedTH1 *hHiggsMassPhi7080;
    WrappedTH1 *hHiggsMassPhi6070;
    WrappedTH1 *hHiggsMassPhi5060;
    WrappedTH1 *hHiggsMassPhi4050;

    WrappedTH1 *hMTInvertedTauIdTopMass;
    WrappedTH1 *hMTInvertedTauIdTopMass150;
    WrappedTH1 *hMTInvertedTauIdTopMass120;
    WrappedTH1 *hMTInvertedTauIdTopMass120150;
    WrappedTH1 *hMTInvertedTauIdTopMass100120;
    WrappedTH1 *hMTInvertedTauIdTopMass80100;
    WrappedTH1 *hMTInvertedTauIdTopMass7080;
    WrappedTH1 *hMTInvertedTauIdTopMass6070;
    WrappedTH1 *hMTInvertedTauIdTopMass5060;
    WrappedTH1 *hMTInvertedTauIdTopMass4050;

    WrappedTH1 *hMETInvertedTauIdLoose;
    WrappedTH1 *hMETInvertedTauIdLoose150;
    WrappedTH1 *hMETInvertedTauIdLoose4070;
    WrappedTH1 *hMETInvertedTauIdLoose70150;
    WrappedTH1 *hMETBaselineTauIdBtag;
    //    WrappedTH1 *hMTBaselineTauIdJets;
    WrappedTH1 *hMTInvertedTauIdLoose;

    //    WrappedTH1 *hMTInvertedTauIdJets;
    WrappedTH1 *hMTBaselineTauIdBtag;
   
 
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauEtaBackToBack;
    WrappedTH1 *hSelectedTauEtaNoBackToBack;
    WrappedTH1 *hSelectedTauEtaCollinear;
    WrappedTH1 *hSelectedTauPhiBackToBack;
    WrappedTH1 *hSelectedTauPhiNoBackToBack;
    WrappedTH1 *hSelectedTauPhiCollinear;
    WrappedTH2 *hPtTauVsMetBackToBack;
    WrappedTH2 *hPtTauVsMetNoBackToBack;
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
