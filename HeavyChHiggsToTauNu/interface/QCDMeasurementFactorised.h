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
    enum QCDFactorisedVariationType {
      kQCDFactorisedTraditional,
      kQCDFactorisedABCD,
      kQCDFactorisedDoubleABCD
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

  public:
    explicit QCDMeasurementFactorised(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::EventWeight& eventWeight, HPlus::HistoWrapper& histoWrapper);
    ~QCDMeasurementFactorised();

    /// Interface towards the EDProducer
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    /// Same method like in paper
    void doTraditionalSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);
    /// Experimental method - not validated
    void doABCDSelection(const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const JetSelection::Data jetData, const METSelection::Data& metData, const BTagging::Data& btagData, const QCDTailKiller::Data& tailKillerData, const double mT, const double fullMass);
    /// Fill root tree after standard selections
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
    const QCDFactorisedVariationType fMethodType;

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
    Count fPreMETCutCounter;
    Count fMETTriggerScaleFactorCounter;
    Count fStandardSelectionsCounter;
    Count fStandardSelectionsWithMET30Counter;
    Count fStandardSelectionsWithTailKillerCounter;
    Count fStandardSelectionsWithTailKillerAndMET30Counter;
    Count fAfterStandardSelectionsCounter;
    Count fAfterLeg1Counter;
    Count fAfterLeg2Counter;
    Count fAfterLeg1AndLeg2Counter;

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
    //QCDFactorisedHistogramHandler fQCDFactorisedHistogramHandler;

    // Common plots
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterVertexSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterTauWeight;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterElectronVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMuonVeto;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterJetSelection;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETScaleFactor;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterStandardSelections;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMET;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterMETAndBtag;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterLeg1;
    CommonPlotsFilledAtEveryStep* fCommonPlotsAfterLeg2;

    // Histograms
    WrappedTH1* hVerticesBeforeWeight;
    WrappedTH1* hVerticesAfterWeight;

    // Shape histograms (some needed for closure test)
    std::vector<WrappedTH1*> hMtShapesAfterStandardSelections;
    std::vector<WrappedTH1*> hMtShapesAfterLeg1;
    std::vector<WrappedTH1*> hMtShapesAfterLeg1WithoutBtag;
    std::vector<WrappedTH1*> hMtShapesAfterLeg2;
    std::vector<WrappedTH1*> hMtShapesAfterLeg1AndLeg2;
    std::vector<WrappedTH1*> hInvariantMassShapesAfterStandardSelections;
    std::vector<WrappedTH1*> hInvariantMassShapesAfterLeg1;
    std::vector<WrappedTH1*> hInvariantMassShapesAfterLeg1WithoutBtag;
    std::vector<WrappedTH1*> hInvariantMassShapesAfterLeg2;
    std::vector<WrappedTH1*> hInvariantMassShapesAfterLeg1AndLeg2;
    // MET shapes (just for controlling, closure test comes from mT shapes)
    std::vector<WrappedTH1*> hMETAfterLeg1;
    std::vector<WrappedTH1*> hMETAfterLeg2;
    std::vector<WrappedTH1*> hMETAfterBJets;

    // Tail tests
    TailTest* fTailTestAfterStdSel;
    TailTest* fTailTestAfterTauLeg;
  };

}

#endif
