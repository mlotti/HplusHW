// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementFactorised_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementFactorised_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
// JetTauInvMass.h
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
// TriggerEmulationEfficiency.h
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
//#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithMHSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetDetailHistograms.h"

#include <vector>
#include <string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class QCDMeasurementFactorised {
    /// Helper class for handling the factorisation higtograms
    class QCDFactorisedHistogramHandler {
    public:
      QCDFactorisedHistogramHandler(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
      ~QCDFactorisedHistogramHandler();
      /// Reset pointer to current bin
      void initialize();
      /// Set pointer to current bin
      void setFactorisationBinForEvent(double pt, double eta, int nvtx);
      /// Create a histogram for a Nevent count in factorisation bins
      void createCountHistogram(TFileDirectory& fdir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, std::string title);
      /// Create a histogram for a shape in factorisation bins
      void createShapeHistogram(TFileDirectory& fdir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, std::string title, std::string label, int nbins, double min, double max);
      /// Fill method for a factorisation histogram containting Nevents counts
      void fillNeventHistogram(WrappedUnfoldedFactorisationHisto* h);
      /// Fill method for a factorisation histogram containting Nevents counts, with unconventional weight
      void fillNeventHistogram(WrappedUnfoldedFactorisationHisto* h, double weight);
      /// Fill method for a factorisation histogram containting a shape
      void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value);
      /// Fill method for a factorisation histogram containting a shape, with unconventional weight
      void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight);

    private:
      int getTauPtBinIndex(double pt);
      int getTauEtaBinIndex(double eta);
      int getNVerticesBinIndex(int nvtx);
      int getMtBinIndex(double mt);
      int getFullMassBinIndex(double mass);
      int getShapeBinIndex(int tauPtBin, int tauEtaBin, int nvtxBin);
      void setAxisLabelsForUnfoldedHisto(WrappedUnfoldedFactorisationHisto* h);
      void checkProperBinning();

    private:
      HistoWrapper& fHistoWrapper;
      std::vector<double> fTauPtBinLowEdges;
      std::vector<double> fTauEtaBinLowEdges;
      std::vector<int> fNVerticesBinLowEdges;
      // Are the following needed?
      std::vector<double> fTransverseMassRange; // Range from config
      std::vector<double> fFullMassRange; // Range from config
      std::vector<double> fTransverseMassBinLowEdges;
      std::vector<double> fFullMassRangeBinLowEdges;
      const int fNUnfoldedBins;
      std::string fBinningString; // string holding the info of the binning
      // Pointer to current bin
      int fCurrentBinX;
      int fCurrentBinY;
      int fCurrentBinZ;
      int fCurrentUnfoldedBin;
    };

    enum QCDFactorisedVariationType {
      kQCDFactorisedTraditional,
      kQCDFactorisedABCD,
      kQCDFactorisedDoubleABCD
    };

    class QCDFactorisedVariation {
    public:
      QCDFactorisedVariation(edm::Service< TFileService >& fs, QCDFactorisedHistogramHandler* histoHandler, EventCounter& eventCounter, CommonPlots& commonPlots, QCDFactorisedVariationType methodType, std::string prefix);
      ~QCDFactorisedVariation();

      void doSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);

    private:
      void doTraditionalSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);
      void doABCDSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);
      void doDoubleABCDSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);

    private:
      QCDFactorisedVariationType fMethodType;
      Count fAfterNjetsCounter;
      Count fAfterStandardSelectionsCounter;
      Count fAfterLeg1Counter;
      Count fAfterLeg2Counter;
      Count fAfterLeg1AndLeg2Counter;
      QCDFactorisedHistogramHandler* fHistoHandler;

      // Common plots
      CommonPlotsFilledAtEveryStep* fCommonPlotsAfterStandardSelections;
      CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMET;
      CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETAndBtag;
      CommonPlotsFilledAtEveryStep* fCommonPlotsAfterLeg1;
      CommonPlotsFilledAtEveryStep* fCommonPlotsAfterLeg2;

      // NQCD Histograms - obsolete
      WrappedUnfoldedFactorisationHisto* hNevtAfterStandardSelections;
      WrappedUnfoldedFactorisationHisto* hNevtAfterLeg1;
      WrappedUnfoldedFactorisationHisto* hNevtAfterLeg2;
      WrappedUnfoldedFactorisationHisto* hNevtAfterLeg1AndLeg2;
      // Shape histograms (some needed for closure test)
      WrappedUnfoldedFactorisationHisto* hMtShapesAfterStandardSelections;
      WrappedUnfoldedFactorisationHisto* hInvariantMassShapesAfterStandardSelections;
      WrappedUnfoldedFactorisationHisto* hMtShapesAfterLeg1;
      WrappedUnfoldedFactorisationHisto* hInvariantMassShapesAfterLeg1;
      WrappedUnfoldedFactorisationHisto* hMtShapesAfterLeg1WithoutBtag;
      WrappedUnfoldedFactorisationHisto* hMtShapesAfterLeg2;
      WrappedUnfoldedFactorisationHisto* hInvariantMassShapesAfterLeg2;
      WrappedUnfoldedFactorisationHisto* hMtShapesAfterLeg1AndLeg2;
      WrappedUnfoldedFactorisationHisto* hInvariantMassShapesAfterLeg1AndLeg2;
      // Data-driven control histograms
      WrappedUnfoldedFactorisationHisto* hCtrlRtau;
      std::vector<WrappedUnfoldedFactorisationHisto*> hCtrlQCDTailKillerCollinear;
      WrappedUnfoldedFactorisationHisto* hCtrlNjets;
      WrappedUnfoldedFactorisationHisto* hCtrlNjetsAfterCollinearCuts;
      WrappedUnfoldedFactorisationHisto* hCtrlMET;
      WrappedUnfoldedFactorisationHisto* hCtrlNbjets;
      std::vector<WrappedUnfoldedFactorisationHisto*> hCtrlQCDTailKillerBackToBack;
      // Closure test oF MET
      WrappedUnfoldedFactorisationHisto* hCtrlMETAfterLeg1;
      WrappedUnfoldedFactorisationHisto* hCtrlMETAfterLeg2;
      WrappedUnfoldedFactorisationHisto* hCtrlMETAfterBJets;
    };

    class TailTest {
    public:
      TailTest(std::string prefix, edm::Service<TFileService>& fs, HistoWrapper& histoWrapper);
      ~TailTest();

      void Fill(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const QCDTailKiller::Data& qcdTailKillerData, const JetSelection::Data& jetData, const ElectronSelection::Data& eData, const MuonSelection::Data& muData, const METSelection::Data& metData, const bool isRealData, const bool isFakeTau);

    private:
      // Tests
      JetDetailHistograms* fJetFakingTauGenuineTaus;
      JetDetailHistograms* fJetFakingTauFakeTaus;
      JetDetailHistograms* fCollinearSystemJetsFakingTauGenuineTaus;
      JetDetailHistograms* fCollinearSystemJetsFakingTauFakeTaus;
      JetDetailHistograms* fCollinearSystemJetsOppositeToTau;
      JetDetailHistograms* fBackToBackSystemJetsFakingTauGenuineTaus;
      JetDetailHistograms* fBackToBackSystemJetsFakingTauFakeTaus;
      JetDetailHistograms* fBackToBackSystemJetsOppositeToTau;

      std::vector<WrappedTH2*> hTailTestByDeltaPhi;
      std::vector<WrappedTH2*> hTailTestByDeltaRJets;
      std::vector<WrappedTH2*> hTailTestByDeltaEtaJets;
      std::vector<WrappedTH2*> hTailTestByDeltaPhiJets;
      std::vector<WrappedTH1*> hTailTestDiffByDeltaEtaBackToBack; // Difference in eta
      std::vector<WrappedTH1*> hTailTestDiffByDeltaEtaCollinear; // Difference in eta
      WrappedTH1* hTailTestMinDeltaR;
      WrappedTH2* hTailTestByDeltaPhiForMinDeltaR;
      WrappedTH2* hTailTestByDeltaPhiForMinDeltaR10;
      WrappedTH2* hTailTestByDeltaPhiForMinDeltaR05;
      WrappedTH2* hCollinearEtaPhi;
      WrappedTH2* hBackToBackEtaPhi;
      WrappedTH2* hCollinearEtaPhiForSelectedTau;
      WrappedTH2* hBackToBackEtaPhiForSelectedTau;
    };

    enum QCDSelectionOrder {
      kQCDOrderTrigger,
      kQCDOrderTauCandidateSelection,
      kQCDOrderElectronVeto,
      kQCDOrderMuonVeto,
      kQCDOrderJetSelection
    };

  public:
    explicit QCDMeasurementFactorised(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::EventWeight& eventWeight, HPlus::HistoWrapper& histoWrapper);
    ~QCDMeasurementFactorised();

    // Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void doTreeFilling(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData, const edm::Ptr<pat::Tau>& selectedTau, const ElectronSelection::Data& electronData, const MuonSelection::Data& muonData, const JetSelection::Data& jetData, const METSelection::Data& metData);

  private:
    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;
    HistoWrapper& fHistoWrapper;
    const double fDeltaPhiCutValue;
    const std::string fTopRecoName; // Name of selected top reconstruction algorithm
    const bool fApplyNprongsCutForTauCandidate;
    const bool fApplyRtauCutForTauCandidate;
    const bool fDoAnalysisVariationWithTraditionalMethod;
    const bool fDoAnalysisVariationWithABCDMethod;
    const bool fDoAnalysisVariationWithDoubleABCDMethod;

    // Counters - do not change order
    Count fAllCounter;
    Count fWJetsWeightCounter;
    Count fMETFiltersCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistAfterCandidateSelectionCounter;
    Count fTausExistAfterNprongsCutCounter;
    Count fTausExistAfterRtauCutCounter;
    Count fMultipleTausAfterTauSelection;
    Count fTausAfterScaleFactorsCounter;
    Count fVetoTauCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fMETTriggerScaleFactorCounter;
    Count fStandardSelectionsCounter;
    Count fStandardSelectionsWithMET30Counter;
    Count fStandardSelectionsWithTailKillerCounter;
    Count fStandardSelectionsWithTailKillerAndMET30Counter;

    // Do not change order
    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fTauSelection;
    VetoTauSelection fVetoTauSelection;
    ElectronSelection fElectronSelection;
    MuonSelection fMuonSelection;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    BTagging fBTagging;
    TopSelection fTopSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    TopWithWSelection fTopWithWSelection;
    BjetSelection fBjetSelection;
    FullHiggsMassCalculator fFullHiggsMassCalculator;
    GenParticleAnalysis fGenparticleAnalysis;
    //ForwardJetVeto fForwardJetVeto;
    EvtTopology fEvtTopology;
    TauTriggerEfficiencyScaleFactor fTauTriggerEfficiencyScaleFactor;
    METTriggerEfficiencyScaleFactor fMETTriggerEfficiencyScaleFactor;
    WeightReader fPrescaleWeightReader;
    WeightReader fPileupWeightReader;
    WeightReader fWJetsWeightReader;
    FakeTauIdentifier fFakeTauIdentifier;
    METFilters fMETFilters;
    QCDTailKiller fQCDTailKiller;
    SignalAnalysisTree fTree;
    CommonPlots fCommonPlots;
    //FakeMETVeto fFakeMETVeto;
    QCDFactorisedHistogramHandler fQCDFactorisedHistogramHandler;

    // Common plots
    //CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTrigger;
    //CommonPlotsFilledAtEveryStep* fCommonPlotsAfterVertexSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeight;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETScaleFactor;

    // Histograms
    WrappedTH1* hVerticesBeforeWeight;
    WrappedTH1* hVerticesAfterWeight;
    WrappedTH1* hVerticesTriggeredBeforeWeight;
    WrappedTH1* hVerticesTriggeredAfterWeight;

    WrappedTH1* hSelectionFlow;

    // Measurement variations
    QCDFactorisedVariation* fVariationTraditionalReference;
    QCDFactorisedVariation* fVariationTraditionalPlusMET30;
    QCDFactorisedVariation* fVariationTraditionalPlusTailKiller;
    QCDFactorisedVariation* fVariationTraditionalPlusMET30AndTailKiller;
    QCDFactorisedVariation* fVariationTraditionalPlusCollinearTailKiller;
    QCDFactorisedVariation* fVariationTraditionalPlusMET30AndCollinearTailKiller;
    QCDFactorisedVariation* fVariationABCDReference;
    QCDFactorisedVariation* fVariationABCDPlusMET30;
    QCDFactorisedVariation* fVariationABCDPlusTailKiller;
    QCDFactorisedVariation* fVariationABCDPlusMET30AndTailKiller;
    QCDFactorisedVariation* fVariationABCDPlusCollinearTailKiller;
    QCDFactorisedVariation* fVariationABCDPlusMET30AndCollinearTailKiller;
    QCDFactorisedVariation* fVariationDoubleABCD;

    // Tail tests
    TailTest* fTailTestAfterStdSel;
    TailTest* fTailTestAfterTauLeg;
  };

}

#endif
