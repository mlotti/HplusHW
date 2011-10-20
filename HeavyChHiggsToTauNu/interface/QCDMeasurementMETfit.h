// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementMETfit_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementMETfit_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NonIsolatedMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PFTauIsolationCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"

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
  class QCDMeasurementMETfit {  
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
      TH1F* hLeg1AfterBTagging17;
      TH1F* hLeg1AfterBTagging;
      TH1F* hLeg1AfterBTagging33;
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
    //kQCDOrderVertexSelection,
    kQCDOrderTauCandidateSelection,
    kQCDOrderElectronVeto,
    kQCDOrderMuonVeto,
    kQCDOrderJetSelection,
    kQCDOrderTauID,
    //kQCDOrderFakeMETVeto,
    //kQCDOrderTopSelection,
    kQCDOrderMETFactorized,
    kQCDOrderBTagFactorized,
    kQCDOrderRtauFactorized
  };
  
  public:
    explicit QCDMeasurementMETfit(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~QCDMeasurementMETfit();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    std::vector<double> getWiderTauPtBins(void);
    const int getWiderTauPtBinsIndex(double met);
    std::vector<double> getMetBins(void);
    const int getMetIndex(double met);
    const int getJetPtIndex(double JetPt);
    std::vector<double> getJetPtBins(void);
    void createHistogramGroupByOtherVariableBins(std::string name, std::vector<TH1*>& histograms, const int nBins, double xMin, double xMax, std::vector<double> BinVariableBins, const TString BinVariableName, const TString VariableName, const TString VariableUnits);
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void AfterBigBox(double EventWeightWithBtag, double EventWeightWithoutBtag, const TauSelection::Data& tauCandidateData, JetSelection::Data& jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const TauSelection::Data& tauData); 
      
    /// Chooses the most isolated of the tau candidates and returns a vector with just that candidate
    edm::PtrVector<pat::Tau> chooseMostIsolatedTauCandidate(edm::PtrVector<pat::Tau> tauCandidates);

    // Different forks of analysis
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
    Count fNonIsolatedElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fNonIsolatedMuonVetoCounter;
    Count fJetSelectionCounter;
    Count fdeltaPhiTauMET160Counter;
    Count fdeltaPhiTauMET135Counter;
    Count fdeltaPhiJetMET10Counter;
    Count fdeltaPhiTauMETJetMETCutsCounter;
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
    VertexSelection fPrimaryVertexSelection;
    TauSelection fOneProngTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    NonIsolatedElectronVeto fNonIsolatedElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    NonIsolatedMuonVeto fNonIsolatedMuonVeto;
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
    //SelectedEventsAnalyzer fWeightedSelectedEventsAnalyzer;
    //SelectedEventsAnalyzer fNonWeightedSelectedEventsAnalyzer;
    GenParticleAnalysis fGenparticleAnalysis;   
    //
    VertexWeight fVertexWeight;
    TriggerEfficiencyScaleFactor fTriggerEfficiencyScaleFactor;

    SignalAnalysisTree fTree;
    
    // Factorization table
    FactorizationTable fFactorizationTable;
    std::vector<double> fFactorizationBinLowEdges;
    

    TH1 *hVerticesBeforeWeight;
    TH1 *hVerticesAfterWeight;

    // MET Histograms
    /*
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
    TH1 *
*/

    // Standard cut path
    TH1 *hStdAfterNjets;
    TH1 *hStdAfterMET;
    TH1 *hStdAfterBjets;
    TH1 *hStdAfterTauIDNoRtau;
    TH1 *hStdAfterRtau;
    TH1 *hStdFakeMETVeto;
    TH1 *hStdTransverseMassAfterTauID;
    TH1 *hStdTransverseMassAfterBTag;
    // Correlation of factorisation
    /*TH1 *hCorrelationMETAfterAllSelections;
    TH1 *hCorrelationBtagAfterAllSelections;
    TH1 *hCorrelationRtauAfterAllSelections;
    TH1 *hCorrelationBtagAndRtauAfterAllSelections;*/

    // Other control histograms
    TH1 *hTauCandidateSelectionIsolatedPtMax;
    
    // Other histograms
    //TH1 *hAlphaTAfterTauID;
    TH1 *hSelectionFlow;

    TH1 *hMET_AfterBigBox; // 22 Sep 2011
    TH1 *hTransverseMass_AfterBigBox; // 14 Aug 2011
    TH1 *hMET_AfterJetSelection; // 22 Sep 2011
    TH1 *hDeltaPhiTauMet;
    TH1 *hDeltaPhiJetMet;
    TH1 *hPhiTauJet135;
    TH1 *hPhiJet10;
    TH1 *hEtaTauJet135;
    TH1 *hEtaJet10;
    TH1 *hTransverseMassDeltaPhiUpperCut;
    TH1 *hTransverseMassDeltaPhiJetMet10;
    TH1 *hTransverseMassDeltaPhiCuts;
    TH1 *hMET_AfterJetsBtagging;
    TH1 *hMET_AfterJetsBtagging4050;
    TH1 *hMET_AfterJetsBtagging5060;
    TH1 *hMET_AfterJetsBtagging6070;
    TH1 *hMET_AfterJetsBtagging7080;
    TH1 *hMET_AfterJetsBtagging80100;
    TH1 *hMET_AfterJetsBtagging100120;
    TH1 *hMET_AfterJetsBtagging120150;
    TH1 *hMET_AfterJetsBtagging150;
    TH1 *hTransverseMass_AfterJetsBtagging;  
    TH1 *hTransverseMass_AfterJetsBtagMet;
    TH1 *hMET_AfterJetSelMt80; // 22 Sep 2011
    TH1 *hTransverseMass_AfterJetSelection; // 14 Aug 2011
    TH1 *hTransverseMass_AfterJetSelMetCut; // 14 Aug 2011
    TH1 *hTransverseMass_AfterBigBoxAndMet; // 14 Aug 2011
    TH1 *hTransverseMass_AfterBigBoxAndBtag; // 14 Aug 2011
    TH1 *hTransverseMass_AfterBigBoxAndTauID; // 14 Aug 2011
    TH1 *hDeltaPhiMetTauCand_AfterBigBox; // 14 Aug 2011
    TH1 *hDeltaPhiMetTauCand_AfterBigBoxAndMet; // 14 Aug 2011
    TH1 *hDeltaPhiMetFirstLdgJet_AfterBigBox; // 14 Aug 2011
    TH1 *hDeltaPhiMetSecondLdgJet_AfterBigBox; // 14 Aug 2011
    TH1 *hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet; // 14 Aug 2011
    TH1 *hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet; // 14 Aug 2011

    //    TH1 *hTransverseMass_AfterBigBox;
    //    TH1 *hTransverseMass_AfterBigBoxAndMet;
    //    TH1 *hTransverseMass_AfterBigBoxAndBtag;
    //    TH1 *hTransverseMass_AfterBigBoxAndTauID;
    //    TH1 *hDeltaPhiMetTauCand_AfterBigBox;
    //    TH1 *hDeltaPhiMetTauCand_AfterBigBoxAndMet;
    //    TH1 *hDeltaPhiMetFirstLdgJet_AfterBigBox;
    //    TH1 *hDeltaPhiMetSecondLdgJet_AfterBigBox;
    //    TH1 *hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet;
    //    TH1 *hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet;
    TH1 *hRtau_AfterBigBox;
    TH1 *hRtauEfficiency_AfterBigBoxTauID;


    // PAS Control Plots
    /*
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
*/
    // For Histogram Groups 
    /*std::vector<TH1*> fCounterAfterJetsTauIdNoRtauByTauPt;
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
    // MET-Tau Isolation Correlation check in tau pT bins
    std::vector<TH1*> fMetInTauPtBins_AfterBigBox_withIsolation;
    std::vector<TH1*> fMetInTauPtBins_AfterBigBox_withoutIsolation;
    std::vector<TH1*> fMetInWiderTauPtBins_AfterBigBox_withIsolation;
    std::vector<TH1*> fMetInWiderTauPtBins_AfterBigBox_withoutIsolation;
*/
  };
}

#endif
