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
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h" // PU re-weight
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"

#include "TTree.h"
#include "TH2F.h"
#include <vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus { 
  class QCDMeasurementBasic {  
    class AnalysisVariation {
    public:
      AnalysisVariation(double METcut, double deltaPhiTauMETCut, int tauIsolation, int nTauPtBins, int nMtBins);
      ~AnalysisVariation();
      
      void analyse(bool isRealData, const float maxElectronPt, const float maxMuonPt, const int njets, const METSelection::Data& METData, const TauSelection::Data& tauCandidateData,const BTagging::Data& btagData, int tauPtBinIndex, double weightAfterVertexReweight, TriggerEfficiencyScaleFactor::Data& trgEffData, FakeTauIdentifier::MCSelectedTauMatchType tauMatch, double mTBinIndex);

    private:
      double fMETCut;
      double fDeltaPhiTauMETCut;
      int iTauIsolation;
      // Control plots
      TH1* hCtrlSelectedTauPtAfterStandardSelections;
      TH1* hCtrlSelectedTauEtaAfterStandardSelections;
      TH1* hCtrlSelectedTauPhiAfterStandardSelections;
      TH2* hCtrlSelectedTauEtaVsPhiAfterStandardSelections;
      TH1* hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
      TH1* hCtrlSelectedTauRtauAfterStandardSelections;
      TH1* hCtrlSelectedTauPAfterStandardSelections;
      TH1* hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
      TH1* hCtrlIdentifiedElectronPtAfterStandardSelections;
      TH1* hCtrlIdentifiedMuonPtAfterStandardSelections;
      TH1* hCtrlNjetsAfterStandardSelections;
      TH1* hCtrlMET; // MET distribution
      std::vector<TH1*> hCtrlNbjets; // Nbjets in bins of tau pT
      std::vector<TH1*> hCtrlDeltaPhi; // DeltaPhi in bins of tau pT

      // event counts in bins of tau jet pt
      TH1F* hLeg1AfterDeltaPhiTauMET;
      TH1F* hLeg1AfterMET;
      TH1F* hLeg1AfterBTagging;
      ScaleFactorUncertaintyManager* fSFUncertaintyAfterMetLeg;
      TH1F* hLeg2AfterTauIDNoRtau;
      TH1F* hLeg2AfterTauIDWithRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyAfterTauLeg;
      // event counts in bins of tau jet pt for transverse mass
      TH1F* hMtLegAfterMET;
      TH1F* hMtLegAfterDeltaPhiTauMET;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterMETAndDeltaPhi;
      TH1F* hMtLegAfterMETAndTauIDNoRtau;
      TH1F* hMtLegAfterMETAndTauIDWithRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterTauID;
      TH1F* hMtLegAfterMETAndDeltaPhiAndInvertedTauIDNoRtau;
      ScaleFactorUncertaintyManager* fSFUncertaintyMtAfterMETAndDeltaPhiAndInvertedTauID;
      std::vector<TH1F*> hMtShapesAfterMETAndDeltaPhi;
      std::vector<TH1F*> hMtShapesAfterMETAndDeltaPhiAndInvertedTau;
      // event counts in bins of tau jet pt and transverse mass for transverse mass
      TH2F* h2DMtLegAfterDeltaPhiTauMET;
      TH2F* h2DMtLegAfterMETAndTauIDNoRtau;
      TH2F* h2DMtLegAfterMETAndTauIDWithRtau;
      TH2F* h2DMtLegAfterMETAndDeltaPhiAndInvertedTauIDNoRtau;

      // Fake tau histograms (type II)
      TH1F* hFakeTauLeg1AfterDeltaPhiTauMET;
      TH1F* hFakeTauLeg1AfterMET;
      TH1F* hFakeTauLeg1AfterBTagging;
      TH1F* hFakeTauLeg2AfterTauIDNoRtau;
      TH1F* hFakeTauLeg2AfterTauIDWithRtau;
      // Transverse mass histograms
      TH1F* hFakeTauMtLegAfterDeltaPhiTauMET;
      TH1F* hFakeTauMtLegAfterMET;
      TH1F* hFakeTauMtLegAfterMETAndTauIDNoRtau;
      TH1F* hFakeTauMtLegAfterMETAndTauIDWithRtau;
      TH1F* hFakeTauMtLegAfterMETAndInvertedTauIDNoRtau;
      TH1F* hFakeTauMtLegAfterMETAndInvertedTauIDWithRtau;
      std::vector<TH1F*> hFakeTauMtShapesAfterMETAndDeltaPhi;
      std::vector<TH1F*> hFakeTauMtShapesAfterMETAndDeltaPhiAndInvertedTau;
      
      // FIXME add TTree's for trigger and btag scalefactor uncertainties
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
    explicit QCDMeasurementBasic(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
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

    // Counters - order is important
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fPrimaryVertexCounter;
    Count fOneProngTauSelectionCounter;
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
    TauSelection fOneProngTauSelection;
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
    //
    VertexWeight fVertexWeight;
    FakeTauIdentifier fFakeTauIdentifier;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;

    SignalAnalysisTree fTree;
    ScaleFactorUncertaintyManager fSFUncertaintyAfterStandardSelections;
    
    std::vector<double> fTauPtBinLowEdges;
    std::vector<double> fTransverseMassBinLowEdges;
    
    // Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    
    // event counts in bins of tau jet pt
    TH1F* hAfterTauCandidateSelection;
    TH1F* hAfterIsolatedElectronVeto;
    TH1F* hAfterIsolatedMuonVeto;
    TH1F* hAfterJetSelection;
    // Fake tau counts (type II)
    TH1F* hFakeTauAfterTauCandidateSelection;
    TH1F* hFakeTauAfterIsolatedElectronVeto;
    TH1F* hFakeTauAfterIsolatedMuonVeto;
    TH1F* hFakeTauAfterJetSelection;
    // Histograms for obtaining control plots
    TH1F* hAfterTauCandidateSelectionAndTauID;
    TH1F* hAfterIsolatedElectronVetoAndTauID;
    TH1F* hAfterIsolatedMuonVetoAndTauID;
    TH1F* hAfterJetSelectionAndTauID;

    // Other control histograms
    //TH1 *hTauCandidateSelectionIsolatedPtMax;

    // event counts in bins of tau jet pt and transverse mass
    TH2* hMtAfterJetSelection;

    // Other histograms
    TH1 *hSelectionFlow;

    // FIXME add TTree's for trigger and btag scalefactor uncertainties
  };
}

#endif
