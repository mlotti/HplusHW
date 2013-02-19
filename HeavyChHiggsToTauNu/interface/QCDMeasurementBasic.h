// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
////#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
////#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedMuonVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

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
    kQCDOrderMET,
    kQCDOrderBTag,
    kQCDOrderDeltaPhiTauMET,
    kQCDOrderMaxDeltaPhiJetMET,
    kQCDOrderTopSelection
  };

  public:
    explicit QCDMeasurementBasic(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::EventWeight& eventWeight, HPlus::HistoWrapper& histoWrapper);
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
    int getShapeBinIndex(int tauPtBin, int tauEtaBin, int nvtxBin);
    void setAxisLabelsForTH3(WrappedTH3* h);

  private:

    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm

    std::vector<double> fTauPtBinLowEdges;
    std::vector<double> fTauEtaBinLowEdges;
    std::vector<int> fNVerticesBinLowEdges;
    std::vector<double> fTransverseMassRange; // Range from config
    std::vector<double> fFullMassRange; // Range from config
    std::vector<double> fTransverseMassBinLowEdges;
    std::vector<double> fFullMassRangeBinLowEdges;

    // Counters - order is important
    Count fAllCounter;
    Count fVertexReweighting;
    Count fWJetsWeightCounter;
    Count fMETFiltersCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fControlPlotsMultipleTausCounter;
    Count fTauTriggerScaleFactorCounter;
    Count fVetoTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fFullTauIDCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorCounter;
    Count fDeltaPhiTauMETCounter;
    Count fMaxDeltaPhiJetMETCounter;
    Count fTopSelectionCounter;
    Count fCoincidenceAfterMETCounter;
    Count fCoincidenceAfterBjetsCounter;
    Count fCoincidenceAfterDeltaPhiCounter;
    Count fCoincidenceAfterSelectionCounter;

    // Counters for propagating result into signal region from reversed rtau control region

    // The order here defines the order the subcounters are printed at the program termination
    METFilters fMETFilters;
    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fTauSelection;
    VetoTauSelection fVetoTauSelection;
    ElectronSelection fElectronSelection;
    //NonIsolatedElectronVeto fNonIsolatedElectronVeto;
    MuonSelection fMuonSelection;
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
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    WeightReader fWJetsWeightReader;

    SignalAnalysisTree fTree;
    ScaleFactorUncertaintyManager fSFUncertaintyAfterStandardSelections;

    // Histograms
    WrappedTH1* hVerticesBeforeWeight;
    WrappedTH1* hVerticesAfterWeight;
    WrappedTH1* hVerticesTriggeredBeforeWeight;
    WrappedTH1* hVerticesTriggeredAfterWeight;

    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsCollinear;
    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsCollinearOpposite;
    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsBackToBack;
    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsBackToBackOpposite;
    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsCollinearTight;
    WrappedTH2* hTauEtaVsPhiAfterBasicSelectionsBackToBackTight;
    WrappedTH2* hTauEtaVsPhiAfterMETLegCollinear;
    WrappedTH2* hTauEtaVsPhiAfterMETLegCollinearOpposite;
    WrappedTH2* hTauEtaVsPhiAfterMETLegBackToBack;
    WrappedTH2* hTauEtaVsPhiAfterMETLegBackToBackOpposite;
    WrappedTH2* hTauEtaVsPhiAfterMETLegCollinearTight;
    WrappedTH2* hTauEtaVsPhiAfterMETLegBackToBackTight;
    WrappedTH2* hTauEtaVsPhiAfterTauLegCollinear;
    WrappedTH2* hTauEtaVsPhiAfterTauLegCollinearOpposite;
    WrappedTH2* hTauEtaVsPhiAfterTauLegBackToBack;
    WrappedTH2* hTauEtaVsPhiAfterTauLegBackToBackOpposite;
    WrappedTH2* hTauEtaVsPhiAfterTauLegCollinearTight;
    WrappedTH2* hTauEtaVsPhiAfterTauLegBackToBackTight;

    WrappedTH2* hJetEtaVsPhiAfterBasicSelectionsCollinear;
    WrappedTH2* hJetEtaVsPhiAfterBasicSelectionsCollinearTight;
    WrappedTH2* hJetEtaVsPhiAfterBasicSelectionsBackToBack;
    WrappedTH2* hJetEtaVsPhiAfterBasicSelectionsBackToBackTight;
    WrappedTH2* hJetEtaVsPhiAfterMETLegCollinear;
    WrappedTH2* hJetEtaVsPhiAfterMETLegCollinearTight;
    WrappedTH2* hJetEtaVsPhiAfterMETLegBackToBack;
    WrappedTH2* hJetEtaVsPhiAfterMETLegBackToBackTight;
    WrappedTH2* hJetEtaVsPhiAfterTauLegCollinear;
    WrappedTH2* hJetEtaVsPhiAfterTauLegCollinearTight;
    WrappedTH2* hJetEtaVsPhiAfterTauLegBackToBack;
    WrappedTH2* hJetEtaVsPhiAfterTauLegBackToBackTight;

    // Other histograms
    WrappedTH1 *hSelectionFlow;

    // NQCD factorisation in bins of tau jet pt, tau jet eta, and nvertices
    WrappedTH3* hAfterJetSelection;
    WrappedTH3* hAfterJetSelectionMET20;
    WrappedTH3* hAfterJetSelectionMET30;
    WrappedTH3* hLeg1AfterMET;
    WrappedTH3* hLeg1AfterBTagging;
    WrappedTH3* hLeg1AfterDeltaPhiTauMET;
    WrappedTH3* hLeg1AfterMaxDeltaPhiJetMET;
    WrappedTH3* hLeg1AfterTopSelection;
    WrappedTH3* hLeg2AfterTauIDNoRtau;
    WrappedTH3* hLeg2AfterTauIDNoRtauMET20;
    WrappedTH3* hLeg2AfterTauIDNoRtauMET30;
    WrappedTH3* hLeg2AfterTauID;
    WrappedTH3* hLeg2AfterTauIDMET20;
    WrappedTH3* hLeg2AfterTauIDMET30;

    WrappedTH3* hABCDAfterBasicSelection;
    WrappedTH3* hABCDAfterTauLeg;
    WrappedTH3* hABCDAfterMETLeg;

    // Mt shapesstd::vector<WrappedTH1*> hFeatureMinEtaOfSelectedJetToGap;
    std::vector<WrappedTH1*> hMtShapesAfterStandardSelection;
    std::vector<WrappedTH1*> hMtShapesAfterStandardSelectionMET20;
    std::vector<WrappedTH1*> hMtShapesAfterStandardSelectionMET30;
    std::vector<WrappedTH1*> hMtShapesAfterFullMETLeg;
    std::vector<WrappedTH1*> hMtShapesAfterMet;
    std::vector<WrappedTH1*> hMtShapesAfterMetAndBTagging;
    std::vector<WrappedTH1*> hMtShapesAfterMetLegNoBtagging;
    std::vector<WrappedTH1*> hMtShapesAfterTauIDNoRtau;
    std::vector<WrappedTH1*> hMtShapesAfterTauID;
    std::vector<WrappedTH1*> hMtShapesAfterTauIDNoRtauMET20;
    std::vector<WrappedTH1*> hMtShapesAfterTauIDMET20;
    std::vector<WrappedTH1*> hMtShapesAfterTauIDNoRtauMET30;
    std::vector<WrappedTH1*> hMtShapesAfterTauIDMET30;
    //std::vector<WrappedTH1*> hFullMassShapesAfterJetSelection;
    std::vector<WrappedTH1*> hFullMassShapesAfterFullMETLeg;
    //std::vector<WrappedTH1*> hFullMassShapesAfterMetLegNoBtagging;

    std::vector<WrappedTH1*> hABCDMtShapesAfterBasicSelection;
    std::vector<WrappedTH1*> hABCDMtShapesAfterTauLeg;
    std::vector<WrappedTH1*> hABCDMtShapesAfterMETLeg;
    std::vector<WrappedTH1*> hABCDMtShapesAfterMETLegNoBtag;

    // Control plots
    std::vector<WrappedTH1*> hCtrlNjets; // Njets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlNjetsMET20; // Njets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlNjetsMET30; // Njets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlNjetsAfterMET; // Njets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterStandardSelections; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterStandardSelectionsMET20; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterStandardSelectionsMET30; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMET; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterBtagging; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterTauIDNoRtau; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterTauIDNoRtauMET20; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterTauIDNoRtauMET30; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterFullTauID; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterFullTauIDMET20; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterFullTauIDMET30; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMETAfterBtaggingAndDeltaPhi; // MET in bins of tau pT
    std::vector<WrappedTH1*> hCtrlNbjets; // Nbjets in bins of tau pT
    std::vector<WrappedTH1*> hCtrlDeltaPhiTauMET; // DeltaPhi(tau,MET) in bins of tau pT
    std::vector<WrappedTH1*> hCtrlMaxDeltaPhiJetMET; // DeltaPhi(jet/tau,MET) in bins of tau pT
    std::vector<WrappedTH1*> hCtrlTopMass; // top mass in bins of tau pT

    // Control plots for ABCD
    std::vector<WrappedTH1*> hABCDCtrlNJets;
    std::vector<WrappedTH1*> hABCDCtrlMET;
    std::vector<WrappedTH1*> hABCDCtrlNbjets;
    std::vector<WrappedTH1*> hABCDCtrlDeltaPhiTauMET;

    // Feature plots
    std::vector<WrappedTH1*> hFeatureMinEtaOfSelectedJetToGapAfterBasicSelection;
    std::vector<WrappedTH1*> hFeatureMinEtaOfSelectedJetToGapAfterMETLeg;
    std::vector<WrappedTH1*> hFeatureMinEtaOfSelectedJetToGapAfterTauLeg;
    std::vector<WrappedTH1*> hFeatureEtaSpreadOfSelectedJetsAfterBasicSelection;
    std::vector<WrappedTH1*> hFeatureEtaSpreadOfSelectedJetsAfterMETLeg;
    std::vector<WrappedTH1*> hFeatureEtaSpreadOfSelectedJetsAfterTauLeg;
    std::vector<WrappedTH1*> hFeatureAverageEtaOfSelectedJetsAfterBasicSelection;
    std::vector<WrappedTH1*> hFeatureAverageEtaOfSelectedJetsAfterMETLeg;
    std::vector<WrappedTH1*> hFeatureAverageEtaOfSelectedJetsAfterTauLeg;
    std::vector<WrappedTH1*> hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterBasicSelection; // Try to think of a longer name for sake of self documentation?
    std::vector<WrappedTH1*> hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterMETLeg;
    std::vector<WrappedTH1*> hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterTauLeg;

  };
}

#endif
