// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class SignalAnalysis {
  enum SignalSelectionOrder {
    kSignalOrderTrigger,
    kSignalOrderVertexSelection,
    kSignalOrderTauID,
    kSignalOrderElectronVeto,
    kSignalOrderMuonVeto,
    kSignalOrderMETSelection,
    kSignalOrderJetSelection,
    kSignalOrderBTagSelection,
    kSignalOrderFakeMETVeto,
    kSignalOrderTopSelection
  };

  public:
    explicit SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalAnalysis();

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    //Count fTriggerEmulationCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fMETCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fTopSelectionCounter;
    Count fRtauAfterCutsCounter;
    Count fForwardJetVetoCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;
    Count ftransverseMassCut100TopCounter;
    Count fZmassVetoCounter;


    TriggerSelection fTriggerSelection;
    TriggerTauMETEmulation  fTriggerTauMETEmulation;
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
    TauEmbeddingAnalysis fTauEmbeddingAnalysis;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;

    VertexWeight fVertexWeight;
    TriggerEmulationEfficiency fTriggerEmulationEfficiency;

    // Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hTransverseMass;
    TH1 *hTransverseMassWithTopCut;
    TH1 *hTransverseMassAfterVeto;
    TH1 *hTransverseMassBeforeVeto;
    TH1 *hDeltaPhi;
    TH1 *hAlphaT;
    TH1 *hAlphaTInvMass;
    TH2 *hAlphaTVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
    TH1 *hMETBeforeMETCut;
    TH1 *hSelectedTauEt;
    TH1 *hSelectedTauEta;
    TH1 *hSelectedTauPhi;
    TH1 *hSelectedTauRtau;
    TH1 *hSelectedTauRtauAfterCuts;
    TH1 *hSelectedTauEtMetCut;
    TH1 *hSelectedTauEtaMetCut;
    TH1 *hSelectedTauPhiMetCut;
    TH1 *hSelectedTauRtauMetCut;

    TH1 *hSelectionFlow;

  };
}

#endif
