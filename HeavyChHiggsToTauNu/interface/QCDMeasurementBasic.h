// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
////#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
////#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedMuonVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeightReader.h" // PU re-weight
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "TTree.h"
#include <vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class QCDMeasurementBasic {
  enum QCDSelectionOrder {
    kQCDOrderTrigger,
    kQCDOrderVertexSelection,
    kQCDOrderTauCandidateSelection,
    kQCDOrderElectronVeto,
    kQCDOrderMuonVeto,
    kQCDOrderJetSelection,
    kQCDOrderTauID,
    kQCDOrderRtau,
    kQCDOrderMET,
    kQCDOrderBTag,
    kQCDOrderDeltaPhiTauMET,
    kQCDOrderTopSelection
  };

  public:
    explicit QCDMeasurementBasic(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::EventWeight& eventWeight);
    ~QCDMeasurementBasic();

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// Returns index to tau pT bin; 0 is underflow and size() is highest bin
    int getTauPtBinIndex(double pt);
    int getTauEtaBinIndex(double eta);
    int getNVerticesBinIndex(int nvtx);
    int getMtBinIndex(double mt);
    int getFullMassBinIndex(double mass);
    void createShapeHistograms(edm::Service< TFileService >& fs, std::vector< HPlus::WrappedTH1* >& container, string title, int nbins, double min, double max);
    int getShapeBinIndex(double tauPt, double tauEta, int nvtx);

  private:
    // Different forks of analysis
    std::vector<AnalysisVariation> fAnalyses;

    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper fHistoWrapper;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm

    // Counters - order is important
    Count fAllCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fControlPlotsMultipleTausCounter;
    Count fTriggerScaleFactorCounter;
    Count fVetoTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fDeltaPhiTauMETCounter;
    Count fMaxDeltaPhiJetMETCounter;
    Count fTopSelectionCounter;
    // Counters for propagating result into signal region from reversed rtau control region

    // The order here defines the order the subcounters are printed at the program termination
    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fTauSelection;
    VetoTauSelection fVetoTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    //NonIsolatedElectronVeto fNonIsolatedElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    //NonIsolatedMuonVeto fNonIsolatedMuonVeto;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    //FakeMETVeto fFakeMETVeto;
    DeltaPhi fDeltaPhi;
    //TopSelection fTopSelection;
    //ForwardJetVeto fForwardJetVeto;
    TransverseMass fTransverseMass;
    GenParticleAnalysis fGenparticleAnalysis;
    TopSelection fTopSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    TopWithWSelection fTopWithWSelection;
    BjetSelection fBjetSelection;
    EvtTopology fEvtTopology;

    FullHiggsMassCalculator fFullHiggsMassCalculator;
    VertexWeightReader fVertexWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;

    SignalAnalysisTree fTree;
    ScaleFactorUncertaintyManager fSFUncertaintyAfterStandardSelections;

    std::vector<double> fTauPtBinLowEdges;
    std::vector<double> fTauEtaBinLowEdges;
    std::vector<int> fNVerticesBinLowEdges;
    std::vector<double> fTransverseMassRange; // Range from config
    std::vector<double> fFullMassRange; // Range from config
    std::vector<double> fTransverseMassBinLowEdges;
    std::vector<double> fFullMassRangeBinLowEdges;

    // Histograms
    WrappedTH1* hVerticesBeforeWeight;
    WrappedTH1* hVerticesAfterWeight;
    WrappedTH1* hVerticesTriggeredBeforeWeight;
    WrappedTH1* hVerticesTriggeredAfterWeight;

    // Other histograms
    WrappedTH1 *hSelectionFlow;

    // NQCD factorisation in bins of tau jet pt, tau jet eta, and nvertices
    WrappedTH3* hAfterJetSelection;
    WrappedTH3* hLeg1AfterMET;
    WrappedTH3* hLeg1AfterBTagging;
    WrappedTH3* hLeg1AfterDeltaPhiTauMET;
    WrappedTH3* hLeg1AfterMaxDeltaPhiJetMET;
    WrappedTH3* hLeg1AfterTopSelection;
    WrappedTH3* hLeg2AfterTauID;

    // Mt shapes
    std::vector<WrappedTH1*> hMtShapesAfterJetSelection;
    std::vector<WrappedTH1*> hMtShapesAfterFullMETLeg;
    //std::vector<WrappedTH1*> hMtShapesAfterMetLegNoBtagging;
    std::vector<WrappedTH1*> hFullMassShapesAfterJetSelection;
    std::vector<WrappedTH1*> hFullMassShapesAfterFullMETLeg;
    //std::vector<WrappedTH1*> hFullMassShapesAfterMetLegNoBtagging;

    // Control plots
    std::vector<WrappedTH1*> hCtrlNjets; // Njets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMET; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlNbjets; // Nbjets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlDeltaPhiTauMET; // DeltaPhi(tau,MET) in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMaxDeltaPhiJetMET; // DeltaPhi(jet/tau,MET) in bins of tau pT
    std::vector<WrappedTH1*> hCtrlTopMass; // top mass in bins of tau pT

  };
}

#endif
