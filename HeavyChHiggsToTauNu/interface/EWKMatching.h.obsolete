// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EWKMatching_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EWKMatching_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}

namespace HPlus {
  class EWKMatching {
  public:
    explicit EWKMatching(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~EWKMatching();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;
    const double fDeltaPhiCutValue;

    Count fAllCounter;
    Count fPrimaryVertexCounter;
    Count fOneTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fDeltaPhiTauMETCounter;
    Count fSelectedEventsCounter;
    Count fSelectedEventsCounterWithGenuineBjets;

//    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    ElectronSelection fElectronSelection;
    MuonSelection fMuonSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;

    // Histograms
    
    // Vertex histograms
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;
    WrappedTH1 *hVerticesTriggeredBeforeWeight;
    WrappedTH1 *hVerticesTriggeredAfterWeight;
    
    // Transverse mass histograms
    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hTransverseMass;
    WrappedTH1 *hWjetsNormalisationAfterJets;
    WrappedTH1 *hWjetsNormalisationAfterMET20;
    WrappedTH1 *hWjetsNormalisationAfterMET30;
    WrappedTH1 *hWjetsNormalisationAfterMET;

    // Control plots
    WrappedTH1* hCtrlNjets;
    WrappedTH1* hCtrlNjetsAfterStandardSelections;
    WrappedTH1* hCtrlMET;
    WrappedTH1* hCtrlNbjets;
    WrappedTH2* hCtrlJetMatrixAfterJetSelection;
    WrappedTH2* hCtrlJetMatrixAfterMET;
    WrappedTH2* hCtrlJetMatrixAfterMET100;

    std::string fModuleLabel;
  };
}

#endif
