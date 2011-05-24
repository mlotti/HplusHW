// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_AlphatAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_AlphatAnalysis_h

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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "TTree.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class AlphatAnalysis {
  public:
    explicit AlphatAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~AlphatAnalysis();

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
    

  private:
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void FillCountersAndHistos(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusAlphatAnalysisProducer
    EventWeight& fEventWeight;

    //    const double ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fMETCounter;
    //Count fTriggerEmulationCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fZmassVetoCounter;
    Count fTopSelectionCounter;
    Count fForwardJetVetoCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;


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
    TriggerEfficiency fTriggerEfficiency;
    VertexWeight fVertexWeight;
    TriggerEmulationEfficiency fTriggerEmulationEfficiency;

    // For Tree
    TTree *myTree;
    float fEvtWeight;
    bool bTriggerPassed;
    bool bTauIdPassed;
    int  iNSelectedTaus;
    float fTauJetEt;
    float fTauJetEta;
    float fRtau;
    float fMET;
    float fFakeMETDeltaPhi;
    float fLdgJetEt;
    float fSecondLdgJetEt;
    float fThirdLdgJetEt;
    int iNHadronicJets;
    int iNHadronicJetsInFwdDir;
    int iNBtags;
    float fGlobalMuonVetoHighestPt;
    float fGlobalElectronVetoHighestPt;
    float fTransverseMass;
    float fAlphaT;
    float fHt;
    float fJt; // Jt = Ht - TauJetEt - LdgJetEt
    float fTopMass; // Jt = Ht - TauJetEt - LdgJetEt

    // Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hTransverseMass;
    TH1 *hTransverseMassWithTopCut;
    TH1 *hDeltaPhi;
    //
    TH2 *hAlphatVsMETAfterTauID;
    TH1 *hAlphatAfterTauID;
    TH1 *hAlphatAfterElectronVeto;
    TH1 *hAlphatAfterMuonVeto;
    TH1 *hAlphatAfterJetSelection;
    TH1 *hAlphatAfterBtagging;
    TH1 *hAlphatAfterFakeMetVeto;
    TH1 *hAlphatAfterTopSelection;
    //
    TH1 *hAlphatInvMass;
    TH2 *hAlphatVsRtau;
    // Histograms for validation at every Selection Cut step
    TH1 *hMet_BeforeTauSelection;
    TH1 *hMet_AfterTauSelection;
    TH1 *hMet_AfterBTagging;
    TH1 *hMet_AfterEvtTopology;
    TH1 *hSelectedTauEt;
    TH1 *hSelectedTauEta;
    TH1 *hSelectedTauPhi;
    TH1 *hSelectedTauRtau;
  };
}

#endif
