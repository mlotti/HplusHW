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

#include "TTree.h"
#include "TH2F.h"

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
      AnalysisVariation(double METcut, double deltaPhiTauMETCut, int tauIsolation, int nTauPtBins);
      ~AnalysisVariation();
      
      void analyse(const METSelection::Data& METData, const TauSelection::Data& tauCandidateData,const BTagging::Data& btagData, int tauPtBinIndex, double weightAfterVertexReweight, double triggerSF, FakeTauIdentifier::MCSelectedTauMatchType tauMatch);

    private:
      double fMETCut;
      double fDeltaPhiTauMETCut;
      int iTauIsolation;
      // event counts in bins of tau jet pt
      TH1F* hLeg1AfterDeltaPhiTauMET;
      TH1F* hLeg1AfterMET;
      TH1F* hLeg1AfterBTagging;
      TH1F* hLeg2AfterTauIDNoRtau;
      TH1F* hLeg2AfterTauIDWithRtau;
      // Transverse mass histograms
      TH1F* hMtLegAfterDeltaPhiTauMET;
      TH1F* hMtLegAfterMET;
      TH1F* hMtLegAfterMETAndTauIDNoRtau;
      TH1F* hMtLegAfterMETAndTauIDWithRtau;
      std::vector<TH1F*> hMtShapesAfterMET;

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
      std::vector<TH1F*> hFakeTauMtShapesAfterMET;
      
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

    std::vector<double> fTauPtBinLowEdges;
    
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

    // Other control histograms
    //TH1 *hTauCandidateSelectionIsolatedPtMax;
    
    // Other histograms
    TH1 *hSelectionFlow;

    // FIXME add TTree's for trigger and btag scalefactor uncertainties
  };
}

#endif
