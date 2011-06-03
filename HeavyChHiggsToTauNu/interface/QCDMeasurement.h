// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurement_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurement_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PFTauIsolationCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"

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
  class QCDMeasurement {  
    class AnalysisVariation {
    public:
      AnalysisVariation(double METcut, double fakeMETVetoCut, int nTauPtBins);
      ~AnalysisVariation();
      
      void analyse(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET);

    private:
      double fMETCut;
      double fFakeMETVetoCut;
      // event counts in bins of tau jet pt
      TH1F* hAfterBigBox;
      TH1F* hLeg1AfterBTagging;
      TH1F* hLeg1AfterMET;
      TH1F* hLeg1AfterFakeMETVeto;
      TH1F* hLeg1AfterTopSelection;
      TH1F* hLeg1AfterAntiTopSelection;
      TH1F* hAfterBigBoxAndTauIDNoRtau;
      TH1F* hLeg2AfterRtau;
      TH1F* hLeg3AfterFakeMETVeto;      
      
      TH1F* hLeg1FakeMetVetoDistribution;
      TH1F* hLeg3FakeMetVetoDistribution;
      TH1F* hTopMassDistribution;
    };
    
  enum QCDSelectionOrder {
    kQCDOrderTrigger,
    kQCDOrderVertexSelection,
    kQCDOrderTauCandidateSelection,
    kQCDOrderElectronVeto,
    kQCDOrderMuonVeto,
    kQCDOrderJetSelection,
    kQCDOrderTauID,
    kQCDOrderFakeMETVeto,
    kQCDOrderTopSelection,
    kQCDOrderMETFactorized,
    kQCDOrderBTagFactorized,
    kQCDOrderRtauFactorized
  };
  
  public:
    explicit QCDMeasurement(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~QCDMeasurement();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    std::vector<double> getMetBins(void);
    const int getMetIndex(double met);
    const int getJetPtIndex(double JetPt);
    std::vector<double> getJetPtBins(void);
    void createHistogramGroupByOtherVariableBins(std::string name, std::vector<TH1*>& histograms, const int nBins, double xMin, double xMax, std::vector<double> BinVariableBins, const TString BinVariableName, const TString VariableName, const TString VariableUnits);
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// Chooses the most isolated of the tau candidates and returns a vector with just that candidate
    edm::PtrVector<pat::Tau> chooseMostIsolatedTauCandidate(edm::PtrVector<pat::Tau> tauCandidates);
    
    // Different forks of analysis
    /// ABCD method between tau isolation and b-tagging (very low statistics for passing tauID)
    void analyzeABCDByTauIsolationAndBTagging(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETDat, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET);
    void analyzeCorrelation(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET);
    void analyzePurities(const TauSelection::Data& tauDataForTauID, const JetSelection::Data &jetData, const METSelection::Data& METData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const int myTauPtIndex, double EventWeight, std::vector<TH1*> fPurityBeforeAfterJets, std::vector<TH1*> fPurityBeforeAfterJetsMet, std::vector<TH1*> fPurityBeforeAfterJetsMetBtag, std::vector<TH1*> fPurityBeforeAfterJetsFakeMet, std::vector<TH1*> fPurityBeforeAfterJetsTauIdNoRtau);
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
    Count fJetSelectionCounter2;
    Count fJetSelectionCounter;
    Count fMETCounter;
    Count fOneProngTauIDWithoutRtauCounter;
    Count fOneProngTauIDWithRtauCounter;
    Count fInvMassVetoOnJetsCounter;
    Count fEvtTopologyCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fTopSelectionCounter;
    Count fForwardJetVetoCounter;
    
    // Counters for propagating result into signal region from reversed rtau control region

    // The order here defines the order the subcounters are printed at the program termination
    TriggerSelection fTriggerSelection;
    //TriggerTauMETEmulation  fTriggerTauMETEmulation;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fOneProngTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    InvMassVetoOnJets fInvMassVetoOnJets;
    EvtTopology fEvtTopology;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    DeltaPhi fDeltaPhi;
    TopSelection fTopSelection;
    ForwardJetVeto fForwardJetVeto;
    TransverseMass fTransverseMass;
    SelectedEventsAnalyzer fWeightedSelectedEventsAnalyzer;
    SelectedEventsAnalyzer fNonWeightedSelectedEventsAnalyzer;
    PFTauIsolationCalculator fPFTauIsolationCalculator;
    GenParticleAnalysis fGenparticleAnalysis;   
    //
    VertexWeight fVertexWeight;
    // TriggerEmulationEfficiency fTriggerEmulationEfficiency;
    
    // Factorization table
    FactorizationTable fFactorizationTable;
    std::vector<double> fFactorizationBinLowEdges;
    
    // MET Histograms
    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;
    TH1 *hMETAfterJetSelection;
    TH1 *hWeightedMETAfterJetSelection;
    TH1 *hWeightedMETAfterTauIDNoRtau;
    TH1 *hWeightedMETAfterTauID;
    TH1 *hWeightedMETAfterBTagging;
    TH1 *hWeightedMETAfterFakeMETVeto;
    TH1 *hWeightedMETAfterForwardJetVeto;
    // After all selections -- FIXME move to separate class
    TH1 *hWeightedTauPtAfterAllSelections;
    TH1 *hWeightedTauEtaAfterAllSelections;
    TH1 *hWeightedRTauAfterAllSelections;
    TH1 *hWeightedNJetsAfterAllSelections;
    TH1 *hWeightedBJetsAfterAllSelections;
    TH1 *hWeightedMETAfterAllSelections;
    TH1 *hWeightedFakeMETVetoAfterAllSelections;
    TH1 *hWeightedDeltaPhiAfterAllSelections;
    TH1 *hWeightedTransverseMassAfterAllSelections;

    // METFactorization details
    TH1 *hMETFactorizationNJetsBefore;
    TH1 *hMETFactorizationNJetsAfter;
    TH2 *hMETFactorizationNJets;
    TH1 *hMETFactorizationBJetsBefore;
    TH1 *hMETFactorizationBJetsAfter;
    TH2 *hMETFactorizationBJets;

    // Standard cut path
    TH1 *hStdNonWeightedTauPtAfterJetSelection;
    TH1 *hStdNonWeightedTauPtAfterTauIDNoRtau;
    TH1 *hStdNonWeightedTauPtAfterTauID;
    TH1 *hStdNonWeightedTauPtAfterBTagging;
    TH1 *hStdNonWeightedTauPtAfterFakeMETVeto;
    TH1 *hStdNonWeightedTauPtAfterForwardJetVeto;
    TH1 *hStdWeightedRtau;
    TH1 *hStdNonWeightedTauPtAfterRtauWithoutNjetsBeforeCut;
    TH1 *hStdNonWeightedTauPtAfterRtauWithoutNjetsAfterCut;
    TH1 *hStdWeightedBjets;
    TH1 *hStdWeightedFakeMETVeto;
    TH1 *hStdNonWeightedRtau;
    TH1 *hStdNonWeightedSelectedTauPt;
    TH1 *hStdNonWeightedSelectedTauEta;
    TH1 *hStdNonWeightedBjets;
    TH1 *hStdNonWeightedFakeMETVeto;

    // ABCD(tau isol. vs. b-tag) cut path - ugly duplication, but fast code
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterJetSelection[4];
    TH2 *hABCDTauIsolBNonWeightedTauPtVsMET[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterMET[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterRtau[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[4];
    TH1 *hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[4];
    TH1 *hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[4];

    // Correlation of factorisation
    TH1 *hCorrelationMETAfterAllSelections;
    TH1 *hCorrelationBtagAfterAllSelections;
    TH1 *hCorrelationRtauAfterAllSelections;
    TH1 *hCorrelationBtagAndRtauAfterAllSelections;

    // Control histograms for P(MET>70)
    TH1 *hMETPassProbabilityAfterJetSelection;
    TH1 *hMETPassProbabilityAfterTauIDNoRtau;
    TH1 *hMETPassProbabilityAfterTauID;
    TH1 *hMETPassProbabilityAfterBTagging;
    TH1 *hMETPassProbabilityAfterFakeMETVeto;
    TH1 *hMETPassProbabilityAfterForwardJetVeto;

    // Other control histograms
    TH1 *hTauCandidateSelectionIsolatedPtMax;

    // Other histograms
    TH1 *hAlphaTAfterTauID;
    TH1 *hSelectionFlow;

    // PAS Control Plots
    TH1 *hCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId;
    TH1 *hCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId;
    TH1 *hCtrlPlot_Rtau_AfterLeptonVeto_WithTauId;
    TH1 *hCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau;
    TH1 *hCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau;
    TH1 *hCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau;
    TH1 *hCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau;
    TH1 *hCtrlPlot_TransverseMass_AfterJetSelection;
    TH1 *hCtrlPlot_TransverseMass_AfterJetSelectionAndTauId;
    TH1 *hCtrlPlot_TransverseMass_AfterJetSelectionMetAndBtag;
    TH1 *hCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet;
    TH1 *hCtrlPlot_TauCandPt_AfterJetSelection;
    TH1 *hCtrlPlot_JetMultiplicity_AfterMETNoJetSelection_WithTauIdAndRtau;
    std::vector<TH1*> fCtrlPlot_MetAndBtagEff_AfterJetSelection_ByTauPt;
    std::vector<TH1*> fCtrlPlot_MetAndBtagEff_AfterJetSelectionAndFakeMet_ByTauPt;

    // For Histogram Groups 
    std::vector<TH1*> fCounterAfterJetsTauIdNoRtauByTauPt;
    std::vector<TH1*> fCounterAfterJetsTauIdNoRtauFakeMetByTauPt;
    std::vector<TH1*> fCounterAfterJetsMetBtagByTauPt;
    std::vector<TH1*> fCounterAfterJetsMetBtagFakeMetByTauPt;
    std::vector<TH1*> fMETHistogramsByTauPtAfterTauCandidateSelection;
    std::vector<TH1*> fMETHistogramsByTauPtAfterJetSelection;
    std::vector<TH1*> fMETHistogramsByTauPtAfterTauIsolation;
    std::vector<TH1*> fNBtagsHistogramsByTauPtAfterJetSelection;
    std::vector<TH1*> fNBtagsHistogramsByTauPtAfterTauIdNoRtau;
    std::vector<TH1*> fNBtagsHistogramsByTauPtAfterTauIdAndRtau;
    std::vector<TH1*> fLdgJetPtHistogramGroupByMET;
    std::vector<TH1*> fNBtagsHistogramGroupByMET;
    std::vector<TH1*> fMETHistogramGroupByLdgJetPt;
    std::vector<TH1*> fFakeMETVetoHistogramGroupByMET;
    // MC
    std::vector<TH1*> fNBquarksHistogramGroupByMET;
    std::vector<TH1*> fNBquarksStatus2HistogramGroupByMET;
    std::vector<TH1*> fNBquarksStatus3HistogramGroupByMET;
    // Purity
    std::vector<TH1*> fPurityBeforeAfterJets;
    std::vector<TH1*> fPurityBeforeAfterJetsMet;
    std::vector<TH1*> fPurityBeforeAfterJetsMetBtag;
    std::vector<TH1*> fPurityBeforeAfterJetsFakeMet;
    std::vector<TH1*> fPurityBeforeAfterJetsTauIdNoRtau;

  };
}

#endif
