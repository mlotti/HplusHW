// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementBasic_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedMuonVeto.h"
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
    class AnalysisVariation {
    public:
      AnalysisVariation(double METcut, double deltaPhiTauMETCut, int tauIsolation, int nTauPtBins, int nMtBins, HistoWrapper& histoWrapper);
      ~AnalysisVariation();

      void analyse(bool isRealData, const float maxElectronPt, const float maxMuonPt, const int njets, const METSelection::Data& METData, const TauSelection::Data& tauCandidateData,const BTagging::Data& btagData, int tauPtBinIndex, double weightAfterVertexReweight, TriggerEfficiencyScaleFactor::Data& trgEffData, FakeTauIdentifier::MCSelectedTauMatchType tauMatch, double mTBinIndex, const TopSelection::Data& topSelectionData, const BjetSelection::Data& bjetSelectionData, const TopChiSelection::Data& topChiSelectionData, const TopWithBSelection::Data& topWithBSelectionData);

    private:
      double fMETCut;
      double fDeltaPhiTauMETCut;
      int iTauIsolation;
      // Control plots
      std::vector<WrappedTH1*> hCtrlSelectedTauPtAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauEtaAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauPhiAfterStandardSelections;
      std::vector<WrappedTH2*> hCtrlSelectedTauEtaVsPhiAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauRtauAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauPAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlIdentifiedElectronPtAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlIdentifiedMuonPtAfterStandardSelections;
      std::vector<WrappedTH1*> hCtrlNjets; // Nbjets in bins of tau pT
      std::vector<WrappedTH1*> hCtrlMET; // Nbjets in bins of tau pT
      std::vector<WrappedTH1*> hCtrlNbjets; // Nbjets in bins of tau pT
      std::vector<WrappedTH1*> hCtrlDeltaPhi; // DeltaPhi in bins of tau pT

      // event counts in bins of tau jet pt
       WrappedTH1* hLeg1AfterDeltaPhiTauMET;
       WrappedTH1* hLeg1AfterMET;
       WrappedTH1* hLeg1AfterBTagging;
       WrappedTH1* hLeg1AfterTopSelection;
       WrappedTH1* hLeg1AfterTopChiSelection;
       WrappedTH1* hLeg1AfterTopWithBSelection;
      ScaleFactorUncertaintyManager* fSFUncertaintyAfterMetLeg;
       WrappedTH1* hLeg2AfterTauIDNoRtau;
       WrappedTH1* hLeg2AfterTauIDWithRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyAfterTauLeg;
      // event counts in bins of tau jet pt for transverse mass
       WrappedTH1* hMtLegAfterMET;
       WrappedTH1* hMtLegAfterDeltaPhiTauMET;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterMETAndDeltaPhi;
       WrappedTH1* hMtLegAfterMETAndTauIDNoRtau;
       WrappedTH1* hMtLegAfterMETAndTauIDWithRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterTauID;
       WrappedTH1* hMtLegAfterMETAndDeltaPhiAndInvertedTauIDNoRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterMETAndDeltaPhiAndInvertedTauID;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndDeltaPhi;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndBTaggingAndDeltaPhi;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndBTaggingAndDeltaPhiAndTopSelection;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndBTaggingAndDeltaPhiAndTopChiSelection;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndBTaggingAndDeltaPhiAndTopWithBSelection;
      std::vector< WrappedTH1*> hMtShapesAfterMETAndDeltaPhiAndInvertedTau;
      // event counts in bins of tau jet pt and transverse mass for transverse mass
      WrappedTH2* h2DMtLegAfterDeltaPhiTauMET;
      WrappedTH2* h2DMtLegAfterMETAndTauIDNoRtau;
      WrappedTH2* h2DMtLegAfterMETAndTauIDWithRtau;
      WrappedTH2* h2DMtLegAfterMETAndDeltaPhiAndInvertedTauIDNoRtau;

      // Fake tau histograms (type II)
       WrappedTH1* hFakeTauLeg1AfterDeltaPhiTauMET;
       WrappedTH1* hFakeTauLeg1AfterMET;
       WrappedTH1* hFakeTauLeg1AfterBTagging;
       WrappedTH1* hFakeTauLeg2AfterTauIDNoRtau;
       WrappedTH1* hFakeTauLeg2AfterTauIDWithRtau;
      // Transverse mass histograms
       WrappedTH1* hFakeTauMtLegAfterDeltaPhiTauMET;
       WrappedTH1* hFakeTauMtLegAfterMET;
       WrappedTH1* hFakeTauMtLegAfterMETAndTauIDNoRtau;
       WrappedTH1* hFakeTauMtLegAfterMETAndTauIDWithRtau;
       WrappedTH1* hFakeTauMtLegAfterMETAndInvertedTauIDNoRtau;
       WrappedTH1* hFakeTauMtLegAfterMETAndInvertedTauIDWithRtau;
      std::vector< WrappedTH1*> hFakeTauMtShapesAfterMETAndDeltaPhi;
      std::vector< WrappedTH1*> hFakeTauMtShapesAfterMETAndDeltaPhiAndInvertedTau;
      
    };
    
  enum QCDSelectionOrder {
    kQCDOrderTrigger,
    //kQCDOrderVertexSelection,
    kQCDOrderTauCandidateSelection,
    kQCDOrderElectronVeto,
    kQCDOrderMuonVeto,
    kQCDOrderJetSelection
    /*kQCDOrderDeltaPhiTauMET,
    kQCDOrderTauID,
    kQCDOrderRtau,
    kQCDOrderMETFactorized,
    kQCDOrderBTagFactorized*/
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
    int getMtBinIndex(double mt);
    

  private:
    // Different forks of analysis
    std::vector<AnalysisVariation> fAnalyses;

    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper fHistoWrapper;

    // Counters - order is important
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fPrimaryVertexCounter;
    Count fTauSelectionCounter;
    Count fOneSelectedTauCounter;
    Count fGlobalElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fJetSelectionCounter;
    Count fNonIsolatedElectronVetoCounter;
    Count fNonIsolatedMuonVetoCounter;
    Count fDeltaPhiTauMETCounter;
    Count fMETCounter;
    Count fBTaggingCounter;
    Count fOneProngTauIDWithoutRtauCounter;
    Count fOneProngTauIDWithRtauCounter;
    // Counters for propagating result into signal region from reversed rtau control region

    // The order here defines the order the subcounters are printed at the program termination
    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    NonIsolatedElectronVeto fNonIsolatedElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    NonIsolatedMuonVeto fNonIsolatedMuonVeto;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    //InvMassVetoOnJets fInvMassVetoOnJets;
    EvtTopology fEvtTopology;
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
    BjetSelection fBjetSelection;
    //
    VertexWeightReader fVertexWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;

    SignalAnalysisTree fTree;
    ScaleFactorUncertaintyManager fSFUncertaintyAfterStandardSelections;
    
    std::vector<double> fTauPtBinLowEdges;
    std::vector<double> fTransverseMassBinLowEdges;
    
    // Histograms
    WrappedTH1* hVerticesBeforeWeight;
    WrappedTH1* hVerticesAfterWeight;
    
    // event counts in bins of tau jet pt
     WrappedTH1* hAfterTauCandidateSelection;
     WrappedTH1* hAfterIsolatedElectronVeto;
     WrappedTH1* hAfterIsolatedMuonVeto;
     WrappedTH1* hAfterJetSelection;
    // Fake tau counts (type II)
     WrappedTH1* hFakeTauAfterTauCandidateSelection;
     WrappedTH1* hFakeTauAfterIsolatedElectronVeto;
     WrappedTH1* hFakeTauAfterIsolatedMuonVeto;
     WrappedTH1* hFakeTauAfterJetSelection;
    // Histograms for obtaining control plots
     WrappedTH1* hAfterTauCandidateSelectionAndTauID;
     WrappedTH1* hAfterIsolatedElectronVetoAndTauID;
     WrappedTH1* hAfterIsolatedMuonVetoAndTauID;
     WrappedTH1* hAfterJetSelectionAndTauID;

    // Other control histograms
    //WrappedTH1* hTauCandidateSelectionIsolatedPtMax;

    // event counts in bins of tau jet pt and transverse mass
    WrappedTH2* hMtAfterJetSelection;

    // Other histograms
    WrappedTH1 *hSelectionFlow;

  };
}

#endif
