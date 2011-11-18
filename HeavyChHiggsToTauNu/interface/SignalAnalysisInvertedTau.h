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
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
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
    explicit SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
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

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fTauVetoAfterTauIDCounter;
    Count fNprongsAfterTauIDCounter;
    Count fRtauAfterTauIDCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fdeltaPhiTauMET10Counter;
    Count fdeltaPhiTauMET160Counter;
    Count fFakeMETVetoCounter;
    Count fdeltaPhiTauMET160FakeMetCounter;
    Count fRtauAfterCutsCounter;
    Count fForwardJetVetoCounter;
    Count fTopRtauDeltaPhiFakeMETCounter;
    Count fRtauDeltaPhiFakeMETCounter;
    Count fBtag33RtauDeltaPhiFakeMETCounter;
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

    SignalAnalysisTree fTree;

    // Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hVerticesTriggeredBeforeWeight;
    TH1 *hVerticesTriggeredAfterWeight;
    TH1 *hTransverseMass;
    TH1 *hTransverseMassWithTopCut;
    TH1 *hTransverseMassAfterVeto;
    TH1 *hTransverseMassBeforeVeto;
    TH1 *hTransverseMassNoMet;
    TH1 *hTransverseMassNoMetBtag;
    TH1 *hTransverseMassNoMetBtagRtau;
    TH1 *hTransverseMassNoMetBtagRtauFakeMet;
    TH1 *hTransverseMassNoMetBtagRtauFakeMetPhi;
    TH1 *hTransverseMassBeforeFakeMet;
    TH1 *hTransverseMassDeltaPhiUpperCut;
    TH1 *hTransverseMassWithRtauFakeMet;
    TH1 *hTransverseMassWithRtau;
    TH1 *hTransverseMassTopRtauDeltaPhiFakeMET;
    TH1 *hTransverseMassTopDeltaPhiFakeMET;
    TH1 *hTransverseMassRtauDeltaPhiFakeMET;
    TH1 *hTransverseMassBtag33RtauDeltaPhiFakeMET;
    TH1 *hTransverseMassBtag33;
    TH1 *hDeltaPhi;
    TH1 *hDeltaPhiJetMet;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
    TH1 *hMETBeforeMETCut;
    TH1 *hMETBeforeTauId;
    TH1 *hMETBaselineTauId;
    TH1 *hMETInvertedTauId;
    TH1 *hMETBaselineTauIdJets;
    TH1 *hMETBaselineTauIdJets150;
    TH1 *hMETBaselineTauIdJets120150;
    TH1 *hMETBaselineTauIdJets100120;
    TH1 *hMETBaselineTauIdJets80100;
    TH1 *hMETBaselineTauIdJets7080;
    TH1 *hMETBaselineTauIdJets6070;
    TH1 *hMETBaselineTauIdJets5060;
    TH1 *hMETBaselineTauIdJets4050;
    TH1 *hMETInvertedTauIdJets;
    TH1 *hMETInvertedTauIdJets150;
    TH1 *hMETInvertedTauIdJets120150;
    TH1 *hMETInvertedTauIdJets100120;
    TH1 *hMETInvertedTauIdJets80100;
    TH1 *hMETInvertedTauIdJets7080;
    TH1 *hMETInvertedTauIdJets6070;
    TH1 *hMETInvertedTauIdJets5060;
    TH1 *hMETInvertedTauIdJets4050;
    TH1 *hMTBaselineTauIdJet;
    TH1 *hMTBaselineTauIdJet150;
    TH1 *hMTBaselineTauIdJet120150;
    TH1 *hMTBaselineTauIdJet100120;
    TH1 *hMTBaselineTauIdJet80100;
    TH1 *hMTBaselineTauIdJet7080;
    TH1 *hMTBaselineTauIdJet6070;
    TH1 *hMTBaselineTauIdJet5060;
    TH1 *hMTBaselineTauIdJet4050;
    TH1 *hMTInvertedTauIdJets;
    TH1 *hMTInvertedTauIdJet;
    TH1 *hMTInvertedTauIdJet150;
    TH1 *hMTInvertedTauIdJet120150;
    TH1 *hMTInvertedTauIdJet100120;
    TH1 *hMTInvertedTauIdJet80100;
    TH1 *hMTInvertedTauIdJet7080;
    TH1 *hMTInvertedTauIdJet6070;
    TH1 *hMTInvertedTauIdJet5060;
    TH1 *hMTInvertedTauIdJet4050;
    TH1 *hMTInvertedTauIdJetPhi;
    TH1 *hMTInvertedTauIdJetPhi150;
    TH1 *hMTInvertedTauIdJetPhi120150;
    TH1 *hMTInvertedTauIdJetPhi100120;
    TH1 *hMTInvertedTauIdJetPhi80100;
    TH1 *hMTInvertedTauIdJetPhi7080;
    TH1 *hMTInvertedTauIdJetPhi6070;
    TH1 *hMTInvertedTauIdJetPhi5060;
    TH1 *hMTInvertedTauIdJetPhi4050;

    TH1 *hMETInvertedTauIdLoose;
    TH1 *hMETInvertedTauIdLoose150;
    TH1 *hMETInvertedTauIdLoose4070;
    TH1 *hMETInvertedTauIdLoose70150;
    TH1 *hMETBaselineTauIdBtag;
    TH1 *hMETInvertedTauIdBtag;
    //    TH1 *hMTBaselineTauIdJets;
    TH1 *hMTInvertedTauIdLoose;

    //    TH1 *hMTInvertedTauIdJets;
    TH1 *hMTBaselineTauIdBtag;
    TH1 *hMTInvertedTauIdBtag;
    TH1 *hMETBaselineTauIdBtagDphi;
    TH1 *hMETInvertedTauIdBtagDphi;
    TH1 *hMETInvertedTauInvertedBtag;
    TH1 *hMTInvertedTauInvertedBtag;
    TH1 *hSelectedTauEt;
    TH1 *hSelectedTauEta;
    TH1 *hSelectedTauPhi;
    TH1 *hSelectedTauRtau;
    TH1 *hSelectedTauLeadingTrackPt;
    TH1 *hSelectedTauLeadingTrackPtMetCut;
    TH1 *hSelectedTauRtauAfterCuts;
    TH1 *hSelectedTauEtMetCut;
    TH1 *hSelectedTauEtaMetCut;
    TH1 *hSelectedTauPhiMetCut;
    TH1 *hSelectedTauEtAfterCuts;
    TH1 *hSelectedTauEtaAfterCuts;
    TH1 *hMetAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtAfterCuts;
    TH1 *hNonQCDTypeIISelectedTauEtaAfterCuts;
    TH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 
    TH1 *hSelectedTauRtauMetCut;

    TH1 *hSelectionFlow;

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
