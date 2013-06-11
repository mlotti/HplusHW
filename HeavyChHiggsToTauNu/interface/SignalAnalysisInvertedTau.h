// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisInvertedTau_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisInvertedTau_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins2Dim.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class EDFilter;
}



class TTree;

namespace HPlus {
  class SignalAnalysisInvertedTau {
    class CounterGroup {
    public:
      /// Constructor for subcounters
      CounterGroup(EventCounter& eventCounter, std::string prefix);
      /// Constructor for main counters
      CounterGroup(EventCounter& eventCounter);
      ~CounterGroup();

      void incrementOneTauCounter() { increment(fOneTauCounter); }
      void incrementElectronVetoCounter() { increment(fElectronVetoCounter); }
      void incrementMuonVetoCounter() { increment(fMuonVetoCounter); }
      void incrementMETCounter() { increment(fMETCounter); }
      void incrementNJetsCounter() { increment(fNJetsCounter); }
      void incrementBTaggingCounter() { increment(fBTaggingCounter); }
      void incrementFakeMETVetoCounter() { increment(fFakeMETVetoCounter); }
      void incrementTopSelectionCounter() { increment(fTopSelectionCounter); }
      void incrementTopChiSelectionCounter() { increment(fTopChiSelectionCounter); }
      void incrementTopWithBSelectionCounter() { increment(fTopWithBSelectionCounter); }
    private:
      Count fOneTauCounter;
      Count fElectronVetoCounter;
      Count fMuonVetoCounter;
      Count fMETCounter;
      Count fNJetsCounter;
      Count fBTaggingCounter;
      Count fFakeMETVetoCounter;
      Count fTopSelectionCounter;
      Count fTopChiSelectionCounter;
      Count fTopWithBSelectionCounter;
    };
    enum SignalSelectionOrder {
      kSignalOrderTrigger,
      //kSignalOrderVertexSelection,
      kSignalOrderTauID,
      kSignalOrderMETSelection,
      kSignalOrderElectronVeto,
      kSignalOrderMuonVeto,
      kSignalOrderJetSelection,
      kSignalOrderBTagSelection,
      kSignalOrderFakeMETVeto,
      kSignalOrderTopSelection
    };
    enum QCDSelectionOrder {
      kQCDOrderVertexSelection,
      kQCDOrderTrigger,
      kQCDOrderTauCandidateSelection,
      kQCDOrderTauID,
      kQCDOrderElectronVeto,
      kQCDOrderMuonVeto,
      kQCDOrderJetSelection,
      kQCDOrderMET,
      kQCDOrderBTag,
      kQCDOrderDeltaPhiTauMET,
      kQCDOrderMaxDeltaPhiJetMET,
      kQCDOrderTopSelection
    };
  enum MCSelectedTauMatchType {
    kkElectronToTau,
    kkMuonToTau,
    kkTauToTau,
    kkJetToTau,
    kkNoMC,
    kkElectronToTauAndTauOutsideAcceptance,
    kkMuonToTauAndTauOutsideAcceptance,
    kkTauToTauAndTauOutsideAcceptance,
    kkJetToTauAndTauOutsideAcceptance
  };
  public:
    explicit SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper);
    ~SignalAnalysisInvertedTau();

    void produces(edm::EDFilter *producer) const;

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau);
    CounterGroup* getCounterGroupByTauMatch(MCSelectedTauMatchType tauMatch);
    void fillNonQCDTypeIICounters(MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData, bool passedStatus = true, double value = 0);

    bool doInvertedAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData, const GenParticleAnalysis::Data genData);
    bool doBaselineAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau, const VertexSelection::Data& pvData, bool myFakeTauStatus);

    // We need a reference in order to use the same object (and not a
    // copied one) given in HPlusSignalAnalysisInvertedTauProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;


    //    const double ftransverseMassCut;
    const bool bBlindAnalysisStatus;
    const double fDeltaPhiCutValue;
    Count fAllCounter;
    Count fWJetsWeightCounter;
    Count fVertexFilterCounter;
    Count fMETFiltersCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTauCandidateCounter;
    Count fNprongsAfterTauIDCounter;
    Count fRtauAfterTauIDCounter;
    Count fTausExistCounter;
    Count fTauFakeScaleFactorBaselineCounter;
    Count fTauTriggerScaleFactorBaselineCounter;

    Count fOneTauCounter; 

    Count fBaselineTauIDCounter;
    Count fBaselineEvetoCounter;
    Count fBaselineMuvetoCounter;
    Count fBaselineJetsCounter;

    Count fBaselineQCDTailKillerCollinearCounter;
    Count fBaselineMetCounter;
    Count fBaselineBtagCounter;
    Count fBTaggingScaleFactorCounter;
    Count fBaselineDeltaPhiTauMETCounter;
    Count fBaselineQCDTailKillerBackToBackCounter;

    //    Count fBaselineDeltaPhiMHTJet1CutCounter;
    Count fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter;

  
    Count fTauVetoAfterTauIDCounter;

    Count fTauFakeScaleFactorCounter;
    Count fTauTriggerScaleFactorCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fQCDTailKillerCollinearCounter;
    Count fBTaggingBeforeMETCounter;
    Count fMETCounter;
    Count fBjetVetoCounter;
    Count fBvetoCounter;
    Count fBvetoDeltaPhiCounter;
    Count fBTaggingCounter;
    Count fBTaggingScaleFactorInvertedCounter;
    Count fQCDTailKillerCounter;
    Count fDeltaPhiTauMETCounter;
    Count fQCDTailKillerBackToBackCounter;
    Count fDeltaPhiVSDeltaPhiMETJet1CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet2CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet3CutCounter;
    Count fDeltaPhiVSDeltaPhiMETJet4CutCounter;
    Count fDeltaPhiAgainstTTCutCounter;
    Count fHiggsMassCutCounter;
    Count ftransverseMassCut80Counter;
    Count ftransverseMassCut100Counter;
    Count fTopSelectionCounter;
    Count fTopChiSelectionCounter;
    Count fTopWithBSelectionCounter;
    Count ftransverseMassCut100TopCounter;

    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    ElectronSelection fElectronSelection;
    MuonSelection fMuonSelection;
    //    TauSelection fOneProngTauSelection;
    TauSelection fTauSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    TopSelection fTopSelection;
    BjetSelection fBjetSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    CorrelationAnalysis fCorrelationAnalysis;
    EvtTopology fEvtTopology;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    VertexAssignmentAnalysis fVertexAssignmentAnalysis;
    METPhiOscillationCorrection fMETPhiOscillationCorrection;

    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    METFilters fMETFilters;
    QCDTailKiller fQCDTailKiller;
    WeightReader fWJetsWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    SignalAnalysisTree fTree;
  

    // Histograms

   // Common plots                                                                                                                                                                                      
    CommonPlots fCommonPlots;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterVertexSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeight;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMET;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETWithPhiOscillationCorrection; // temporary                                                                                                         
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTagging;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelected;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTail;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMass;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeightFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVetoFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelectionFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterBTaggingFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedMtTailFakeTaus;
    CommonPlotsFilledAtEveryStep* fCommonPlotsSelectedFullMassFakeTaus;




    WrappedTH1 *hTauDiscriminator;
    WrappedTH1 *hOneProngRtauPassedInvertedTaus;
    WrappedTH1 *hVerticesBeforeWeight;
    WrappedTH1 *hVerticesAfterWeight;
    WrappedTH1 *hVerticesTriggeredBeforeWeight;
    WrappedTH1 *hVerticesTriggeredAfterWeight;
    WrappedTH1 *hTransverseMass;
    WrappedTH1 *hTransverseMassWithTopCut;

    WrappedTH1 *hTransverseMassBeforeVeto;
    WrappedTH1 *hTransverseMassNoMet;
    WrappedTH1 *hTransverseMassNoMetBtag;
    WrappedTH1 *hTransverseMassTailKiller;
 
    WrappedTH2 *hTransverseMassVsDphi;
   
   
    WrappedTH1 *hTransverseMassTopChiSelection;
    WrappedTH1 *hTransverseMassTopBjetSelection;
    //    WrappedTH1 *hDeltaPhi;
    WrappedTH1 *hDeltaPhiAfterVeto;
    WrappedTH1 *hDeltaPhiAfterJets;
    WrappedTH1 *hDeltaPhiBeforeVeto;
    WrappedTH1 *hDeltaPhiJetMet;


    // Histograms for validation at every Selection Cut step
    WrappedTH1 *hMet_AfterTauSelection;
    WrappedTH1 *hMet_AfterEvtTopology;
    WrappedTH1 *hMETBeforeMETCut;
    WrappedTH1 *hMETBeforeTauId;

    // std::vector<WrappedTH1*> hQCDTailKillerBackToBackInverted;
    // std::vector<WrappedTH1*> hQCDTailKillerCollinearInverted;
    //std::vector<WrappedTH1*> hQCDTailKillerBackToBackBaseline;
    //std::vector<WrappedTH1*> hQCDTailKillerCollinearBaseline;
    std::vector<WrappedTH1*> hEWKFakeTausQCDTailKillerBackToBack_Baseline;
    std::vector<WrappedTH1*> hEWKFakeTausQCDTailKillerCollinear_Baseline;

    WrappedTH1* hQCDTailKillerJet0BackToBackInverted;
    WrappedTH1* hQCDTailKillerJet1BackToBackInverted;
    WrappedTH1* hQCDTailKillerJet2BackToBackInverted;
    WrappedTH1* hQCDTailKillerJet3BackToBackInverted;
    WrappedTH1* hQCDTailKillerJet0CollinearInverted;
    WrappedTH1* hQCDTailKillerJet1CollinearInverted;
    WrappedTH1* hQCDTailKillerJet2CollinearInverted;
    WrappedTH1* hQCDTailKillerJet3CollinearInverted;
    WrappedTH1* hQCDTailKillerJet0BackToBackBaseline;
    WrappedTH1* hQCDTailKillerJet1BackToBackBaseline;
    WrappedTH1* hQCDTailKillerJet2BackToBackBaseline;
    WrappedTH1* hQCDTailKillerJet3BackToBackBaseline;
    WrappedTH1* hQCDTailKillerJet0CollinearBaseline;
    WrappedTH1* hQCDTailKillerJet1CollinearBaseline;
    WrappedTH1* hQCDTailKillerJet2CollinearBaseline;
    WrappedTH1* hQCDTailKillerJet3CollinearBaseline;

    //    WrappedTH1* hCtrlNjets;
    HistogramsInBins *hCtrlNjets;

    HistogramsInBins *hMETBaselineTauId;
    HistogramsInBins *hMETBaselineTauIdJets;
    HistogramsInBins *hMETBaselineTauIdBtag;
    HistogramsInBins *hMETBaselineTauIdBveto;
    HistogramsInBins *hMETBaselineTauIdJetsCollinear;
    HistogramsInBins *hMETBaselineTauIdBvetoCollinear;
    HistogramsInBins *hMETBaselineTauIdBvetoTailKiller;
    // baseline MT histos
    HistogramsInBins *hMTInvertedTauIdSoftBtaggingTK;
    HistogramsInBins *hMTBaselineTauIdSoftBtaggingTK;
    HistogramsInBins *hMTBaselineTauIdJet;
    HistogramsInBins *hMTBaselineTauIdBtag;
    HistogramsInBins *hMTBaselineTauIdBveto;
    HistogramsInBins *hMTBaselineTauIdBvetoTailKiller;
    HistogramsInBins *hMTBaselineTauIdBvetoDphi;
    HistogramsInBins *hMTBaselineTauIdNoMetBveto;
    HistogramsInBins *hMTBaselineTauIdNoMetBvetoTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoMetNoBtagging;
    HistogramsInBins *hMTBaselineTauIdNoMetNoBtaggingTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoMetBtag;
    HistogramsInBins *hMTBaselineTauIdNoMetBtagTailKiller;
    HistogramsInBins *hMTBaselineTauIdNoBtagging;
    HistogramsInBins *hMTBaselineTauIdNoBtaggingTailKiller;
    HistogramsInBins *hMTBaselineTauIdPhi;
    HistogramsInBins *hMTBaselineTauIdAllCutsTailKiller;


    WrappedTH1 *hDeltaR_TauMETJet1MET;
    WrappedTH1 *hDeltaR_TauMETJet2MET;
    WrappedTH1 *hDeltaR_TauMETJet3MET;
    WrappedTH1 *hDeltaR_TauMETJet4MET;

    WrappedTH1 *hNBBaselineTauIdJet;    
    WrappedTH1 *hNJetBaselineTauId;
    WrappedTH1 *hDeltaPhiBaseline;
    WrappedTH1 *hNJetBaselineTauIdMet;
 


    HistogramsInBins *hMETInvertedTauId;
    HistogramsInBins *hNJetInvertedTauId;  
    HistogramsInBins *hNJetInvertedTauIdMet;
    HistogramsInBins *hMETInvertedTauIdJets;
    HistogramsInBins *hMETInvertedTauIdBtag;  
    HistogramsInBins *hMETInvertedTauIdBveto;
    HistogramsInBins *hMETInvertedTauIdJetsCollinear;
    HistogramsInBins *hMETInvertedTauIdBvetoCollinear;
    HistogramsInBins *hMETInvertedAllCutsTailKiller;
    HistogramsInBins *hMet_AfterBTagging;
    HistogramsInBins *hNBInvertedTauIdJet;
    HistogramsInBins *hNBInvertedTauIdJetDphi;  
    HistogramsInBins *hDeltaPhiInvertedNoB;
    HistogramsInBins *hDeltaPhiInverted;  

    //    HistogramsInBins *hDeltaPhiMHTJet1Inverted;

    HistogramsInBins *hMTInvertedTauIdBtagNoMetCut;
    HistogramsInBins *hMTInvertedTauIdBvetoNoMetCut; 
    HistogramsInBins *hMTInvertedTauIdBtagNoMetCutTailKiller;
    HistogramsInBins *hMTInvertedTauIdBvetoNoMetCutTailKiller; 
    HistogramsInBins *hMTInvertedTauIdJet;
    HistogramsInBins *hMTInvertedTauIdJetTailKiller;
    HistogramsInBins *hMTInvertedTauIdPhi; 
    HistogramsInBins *hMTInvertedNoBtaggingTailKiller;
    HistogramsInBins *hMTInvertedTauIdNoBtagging;
    HistogramsInBins *hMTInvertedTauIdBveto;
    HistogramsInBins *hMTInvertedTauIdBtag;
    HistogramsInBins *hMTInvertedTauIdBvetoDphi;
    HistogramsInBins *hMTInvertedTauIdJetDphi;
    HistogramsInBins *hMTInvertedNoBtagging;
    HistogramsInBins *hMTInvertedAllCutsTailKiller;
    HistogramsInBins *hTopMass;
    HistogramsInBins *hHiggsMass;

    WrappedTH2 *hDeltaPhiJet1TauSel;
    WrappedTH2 *hDeltaPhiJet1LeptonVeto;
    WrappedTH2 *hDeltaPhiJet1MetCut;
    WrappedTH2 *hDeltaPhiJet1Btagging;
    WrappedTH2 *hDeltaPhiJet2TauSel;
    WrappedTH2 *hDeltaPhiJet2LeptonVeto;
    WrappedTH2 *hDeltaPhiJet2MetCut;
    WrappedTH2 *hDeltaPhiJet2Btagging;
    WrappedTH2 *hDeltaPhiJet3TauSel;
    WrappedTH2 *hDeltaPhiJet3LeptonVeto;
    WrappedTH2 *hDeltaPhiJet3MetCut;
    WrappedTH2 *hDeltaPhiJet3Btagging;
    WrappedTH2 *hDeltaPhiJet4TauSel;
    WrappedTH2 *hDeltaPhiJet4LeptonVeto;
    WrappedTH2 *hDeltaPhiJet4MetCut;
    WrappedTH2 *hDeltaPhiJet4Btagging;

    WrappedTH2 *hDeltaPhiJet1TauSelBaseline;
    WrappedTH2 *hDeltaPhiJet1BtaggingBaseline;
    WrappedTH2 *hDeltaPhiJet2TauSelBaseline;
    WrappedTH2 *hDeltaPhiJet2BtaggingBaseline;
    WrappedTH2 *hDeltaPhiJet3TauSelBaseline;
    WrappedTH2 *hDeltaPhiJet3BtaggingBaseline;
    WrappedTH2 *hDeltaPhiJet4TauSelBaseline;
    WrappedTH2 *hDeltaPhiJet4BtaggingBaseline;


    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet1Btagging;   
   

    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2TauSel; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2LeptonVeto;
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2MetCut; 
    HistogramsInBins2Dim *hDeltaPhiVsDeltaPhiJet2Btagging;   
   



    WrappedTH1 *hSelectedTauEtTauVeto;
    HistogramsInBins *hSelectedTauEtJetCut;
    HistogramsInBins *hSelectedTauEtCollinearTailKiller;
    HistogramsInBins *hSelectedTauEtMetCut;
    HistogramsInBins *hSelectedTauEtBtagging;
    WrappedTH1 *hSelectedTauEtBjetVeto;
    WrappedTH1 *hSelectedTauEtBjetVetoPhiCuts;
    HistogramsInBins *hSelectedTauEtBackToBackTailKiller;


   
    WrappedTH1 *hMTInvertedTauIdJets; 
    WrappedTH1 *hSelectedTauEt;
    WrappedTH1 *hSelectedTauEta;
    WrappedTH1 *hSelectedTauPhi;
    WrappedTH1 *hSelectedTauRtau;
    WrappedTH1 *hSelectedTauLeadingTrackPt;

    WrappedTH1 *hSelectedTauEtaMetCut;
    WrappedTH1 *hSelectedTauPhiMetCut;
    WrappedTH1 *hSelectedTauEtAfterCuts;
    WrappedTH1 *hSelectedTauEtaAfterCuts;
    WrappedTH1 *hMetAfterCuts;
    WrappedTH1 *hNonQCDTypeIISelectedTauEtAfterCuts;
    WrappedTH1 *hNonQCDTypeIISelectedTauEtaAfterCuts;
    WrappedTH1 *hTransverseMassDeltaPhiUpperCutFakeMet; 
    WrappedTH1 *hSelectedTauRtauMetCut;

    WrappedTH1 *hSelectionFlow;

    CounterGroup fNonQCDTypeIIGroup;
    CounterGroup fAllTausCounterGroup;
    CounterGroup fElectronToTausCounterGroup;
    CounterGroup fMuonToTausCounterGroup;
    CounterGroup fGenuineToTausCounterGroup;
    CounterGroup fJetToTausCounterGroup;
    CounterGroup fAllTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    CounterGroup fJetToTausAndTauOutsideAcceptanceCounterGroup;



    bool fProduce;
    bool fOnlyGenuineTaus; 
  };
}

#endif
