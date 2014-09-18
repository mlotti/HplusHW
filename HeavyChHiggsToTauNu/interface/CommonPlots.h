// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlots_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlots_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SplittedHistogramHandler.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlotsFilledAtEveryStep.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauFakeRateAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationDYEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationWJetsEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationTTJetsEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <string>
#include <vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  /**
   * Helper class for histogram settings
   */
  class HistogramSettings {
  public:
    HistogramSettings(const edm::ParameterSet& iConfig);
    ~HistogramSettings();
    int bins() const { return fBins; }
    double min() const { return fAxisMin; }
    double max() const { return fAxisMax; }

  private:
    int fBins;
    double fAxisMin;
    double fAxisMax;
  };

  /**
   * Class to contain plots common to all analyses (signalAnalysis, QCD, ...)
   */
  class CommonPlots {
  public:
    enum AnalysisType {
      kSignalAnalysis = 0,
      kEmbedding,
      kQCDFactorised,
      kQCDInverted,
      kQCDNormalizationSystematicsSignalRegion, // Needed for obtaining normalization systematics to data-driven control plots
      kQCDNormalizationSystematicsControlRegion // Needed for obtaining normalization systematics to data-driven control plots
    };

    CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, AnalysisType analysisType, bool isEmbeddedData = false);
    ~CommonPlots();

    void disableCommonPlotsFilledAtEveryStep() { bDisableCommonPlotsFilledAtEveryStep = true; }
    /// Initialize data objects; call for every event
    void initialize(const edm::Event& iEvent,
                    const edm::EventSetup& iSetup,
                    VertexSelection::Data& vertexData,
                    TauSelection& tauSelection,
                    FakeTauIdentifier& fakeTauIdentifier,
                    ElectronSelection& eVeto,
                    MuonSelection& muonVeto,
                    JetSelection& jetSelection,
                    METTriggerEfficiencyScaleFactor& metTrgSF,
                    METSelection& metSelection,
                    BTagging& bTagging,
                    QCDTailKiller& qcdTailKiller,
                    BjetSelection& bjetSelection,
                    TopSelectionManager& topSelection,
                    EvtTopology& evtTopology,
                    FullHiggsMassCalculator& fullHiggsMassCalculator);
    /// Initialization where TauSelection::Data is used instead of TauSelection object (use for QCD measurements)
    void initialize(const edm::Event& iEvent,
                    const edm::EventSetup& iSetup,
                    VertexSelection::Data& vertexData,
                    TauSelection::Data& tauData,
                    FakeTauIdentifier& fakeTauIdentifier,
                    ElectronSelection& eVeto,
                    MuonSelection& muonVeto,
                    JetSelection& jetSelection,
                    METTriggerEfficiencyScaleFactor& metTrgSF,
                    METSelection& metSelection,
                    BTagging& bTagging,
                    QCDTailKiller& qcdTailKiller,
                    BjetSelection& bjetSelection,
                    TopSelectionManager& topSelection,
                    EvtTopology& evtTopology,
                    FullHiggsMassCalculator& fullHiggsMassCalculator);

    /// create object containing histograms to be filled after all (or almost all) selection steps
    CommonPlotsFilledAtEveryStep* createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot = false, std::string selectionFlowPlotLabel = "");

    /// Obtain splitted histogram handler
    SplittedHistogramHandler& getSplittedHistogramHandler() { return fSplittedHistogramHandler; }

    /// unique filling methods (to be called AFTER return statement)
    void fillControlPlotsAfterVertexSelection(const edm::Event& iEvent, const VertexSelection::Data& data);
    void fillControlPlotsAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData, JetSelection& jetSelection, METSelection& metSelection, BTagging& btagging, QCDTailKiller& qcdTailKiller);
    void setSplittingOfPhaseSpaceInfoAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, METSelection& metSelection);
    void fillControlPlotsAfterTauTriggerScaleFactor(const edm::Event& iEvent);
    void fillControlPlotsAfterMETTriggerScaleFactor(const edm::Event& iEvent);
    void fillControlPlotsAfterTopologicalSelections(const edm::Event& iEvent);
    void fillControlPlotsAfterAllSelections(const edm::Event& iEvent, double transverseMass);
    void fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const edm::Event& iEvent, double transverseMass);
    void fillControlPlotsAfterAllSelectionsWithFullMass(const edm::Event& iEvent, FullHiggsMassCalculator::Data& data);
    /// unique filling methods (to be called BEFORE return statement)
    void fillControlPlotsAtTauVetoSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const VetoTauSelection::Data& tauVetoData);
    void fillControlPlotsAtElectronSelection(const edm::Event& iEvent, const ElectronSelection::Data& data);
    void fillControlPlotsAtMuonSelection(const edm::Event& iEvent, const MuonSelection::Data& data);
    void fillControlPlotsAtJetSelection(const edm::Event& iEvent, const JetSelection::Data& data);
    void fillControlPlotsAtCollinearDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data);
    void fillControlPlotsAtMETSelection(const edm::Event& iEvent, const METSelection::Data& data);
    void fillControlPlotsAtBtagging(const edm::Event& iEvent, const BTagging::Data& data);
    void fillControlPlotsAtBackToBackDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data);
    void fillControlPlotsAtTopSelection(const edm::Event& iEvent, const TopSelectionManager::Data& data);
    void fillControlPlotsAtEvtTopology(const edm::Event& iEvent, const EvtTopology::Data& data);
    /// Fill all plots at once (needed for QCD normalization systematics)
    void fillAllControlPlots(const edm::Event& iEvent, double transverseMass);
    /// Getters for histogram bin definitions
    const HistogramSettings& getPtBinSettings() const { return fPtBinSettings; }
    const HistogramSettings& getEtaBinSettings() const { return fEtaBinSettings; }
    const HistogramSettings& getPhiBinSettings() const { return fPhiBinSettings; }
    const HistogramSettings& getRtauBinSettings() const { return fRtauBinSettings; }
    const HistogramSettings& getNjetsBinSettings() const { return fNjetsBinSettings; }
    const HistogramSettings& getMetBinSettings() const { return fMetBinSettings; }
    const HistogramSettings& getTailKiller1DSettings() const { return fTailKiller1DSettings; }
    const HistogramSettings& getMtBinSettings() const { return fMtBinSettings; }
    const HistogramSettings& getInvmassBinSettings() const { return fInvmassBinSettings; }

  protected:
    /// Options
    const bool bOptionEnableTauFakeRateAnalysis;
    const bool bOptionEnableNormalisationAnalysis;
    const bool bOptionEnableMETOscillationAnalysis;
    /// Analysis type
    bool bDisableCommonPlotsFilledAtEveryStep;
    AnalysisType fAnalysisType;
    /// Creates histograms
    void createHistograms();
    /// Event counter object
    EventCounter& fEventCounter;
    /// HistoWrapper object
    HistoWrapper& fHistoWrapper;
    /// Splitted histogram handler
    SplittedHistogramHandler fSplittedHistogramHandler;
    /// Base directory in root file for every step histograms
    edm::Service<TFileService> fs;
    TFileDirectory fCommonBaseDirectory;
    TFileDirectory fEveryStepDirectory;
    /// Tau fake rate analysis object
    TauFakeRateAnalysis* fTauFakeRateAnalysis;
    /// Normalisation analysis objects
    std::vector<NormalisationAnalysis*> fNormalisationAnalysisObjects;
    /// Selection objects
    TauSelection* fTauSelection;
    FakeTauIdentifier* fFakeTauIdentifier;
    METTriggerEfficiencyScaleFactor* fMetTrgSF;
    /// Cached data objects from silent analyze
    VertexSelection::Data fVertexData;
    TauSelection::Data fTauData;
    FakeTauIdentifier::Data fFakeTauData;
    ElectronSelection::Data fElectronData;
    MuonSelection::Data fMuonData;
    JetSelection::Data fJetData;
    METSelection::Data fMETData;
    BTagging::Data fBJetData;
    QCDTailKiller::Data fQCDTailKillerData;
    TopSelectionManager::Data fTopData;
    EvtTopology::Data fEvtTopology;
    FullHiggsMassCalculator::Data fFullHiggsMassData;

    // Input parameters
    HistogramSettings fPtBinSettings;
    HistogramSettings fEtaBinSettings;
    HistogramSettings fPhiBinSettings;
    HistogramSettings fDeltaPhiBinSettings;
    HistogramSettings fRtauBinSettings;
    HistogramSettings fNjetsBinSettings;
    HistogramSettings fMetBinSettings;
    HistogramSettings fBJetDiscriminatorBinSettings;
    HistogramSettings fTailKiller1DSettings;
    HistogramSettings fTopMassBinSettings;
    HistogramSettings fWMassBinSettings;
    HistogramSettings fMtBinSettings;
    HistogramSettings fInvmassBinSettings;

    // Counters - needed or not?

    // Histograms ------------------------------------------
    // NOTE: the histograms with the prefix hCtrl are used as data driven control plots
    // NOTE: the histograms with the prefix hShape are used as shape histograms

    // vertex

    // tau selection

    // tau trigger SF
    WrappedTH2* hTauPhiOscillationX;
    WrappedTH2* hTauPhiOscillationY;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterTaus;

    // veto tau selection
    
    // electron veto

    // muon veto
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterLeptonVeto;

    // jet selection
    std::vector<WrappedTH1*> hCtrlNjets;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNjets;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterNjets;

    // MET trigger SF
    std::vector<WrappedTH1*> hCtrlNjetsAfterJetSelectionAndMETSF;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterMETSF;

    // improved delta phi collinear cuts (currently the point of the std. selections)
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearMinimum;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearJet1;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearJet2;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearJet3;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearJet4;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DCollinearMinimum;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DCollinearJet1;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DCollinearJet2;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DCollinearJet3;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DCollinearJet4;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearMinimum;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearJet1;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearJet2;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearJet3;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearJet4;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DCollinearMinimum;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DCollinearJet1;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DCollinearJet2;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DCollinearJet3;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DCollinearJet4;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterCollinearCuts;

    std::vector<WrappedTH1*> hCtrlSelectedTauPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauEtaAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hSelectedTauEtaVsPhiAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauRtauAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauPAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauDecayModeAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauDecayModeAfterStandardSelections;

    std::vector<WrappedTH1*> hCtrlNjetsAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlJetPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlJetEtaAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNjetsAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausJetPtAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausJetEtaAfterStandardSelections;

    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearMinimumAfterStandardSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearMinimumAfterStandardSelections;

    // MET selection
    std::vector<WrappedTH1*> hCtrlMET;
    std::vector<WrappedTH1*> hCtrlMETPhi;
    std::vector<WrappedTH1*> hCtrlTauPlusMETPt; // a.k.a. boost
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMET;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMETPhi;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTauPlusMETPt; // a.k.a. boost
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterMET;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionEWKFakeTausAfterMET;

    // b tagging
    std::vector<WrappedTH1*> hCtrlNbjets;
    std::vector<WrappedTH1*> hCtrlBJetPt;
    std::vector<WrappedTH1*> hCtrlBJetEta;
    std::vector<WrappedTH1*> hCtrlBDiscriminator;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNbjets;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBDiscriminator;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBJetPt;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBJetEta;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterBjets;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionEWKFakeTausAfterBjets;

    // improved delta phi back to back cuts
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackMinimum;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackJet1;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackJet2;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackJet3;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackJet4;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DBackToBackMinimum;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DBackToBackJet1;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DBackToBackJet2;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DBackToBackJet3;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DBackToBackJet4;
    std::vector<WrappedTH1*> hCtrlDeltaPhiTauMET;
    std::vector<WrappedTH1*> hCtrlMinDeltaPhiTauJet;
    std::vector<WrappedTH1*> hCtrlMaxDeltaPhiTauJet;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackMinimum;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackJet1;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackJet2;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackJet3;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackJet4;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DBackToBackMinimum;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DBackToBackJet1;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DBackToBackJet2;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DBackToBackJet3;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DBackToBackJet4;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausDeltaPhiTauMET;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMinDeltaPhiTauJet;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMaxDeltaPhiTauJet;
    
    // top selection
    std::vector<WrappedTH1*> hCtrlTopMass;
    std::vector<WrappedTH1*> hCtrlTopPt;
    std::vector<WrappedTH1*> hCtrlWMass;
    std::vector<WrappedTH1*> hCtrlWPt;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTopMass;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTopPt;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausWMass;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausWPt;

    // evt topology

    // ctrl plots after all selections
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinearMinimumAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinearMinimumAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedGenuineTauPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauPhiAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauRtauAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauPAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauLeadingTrkPAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlSelectedTauDecayModeAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPhiAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauRtauAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauPAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausSelectedTauDecayModeAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlNjetsAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlJetPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlJetEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNjetsAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausJetPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausJetEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlMETAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlMETPhiAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlTauPlusMETPtAfterMtSelections; // a.k.a. boost
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMETAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMETPhiAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTauPlusMETPtAfterMtSelections; // a.k.a. boost
    std::vector<WrappedTH1*> hCtrlNbjetsAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlBJetPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlBJetEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlBDiscriminatorAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausNbjetsAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBDiscriminatorAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBJetPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausBJetEtaAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBackMinimumAfterMtSelections;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DMinimum;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DJet1;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DJet2;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DJet3;
    std::vector<WrappedTH2*> hCtrlQCDTailKiller2DJet4;
    std::vector<WrappedTH1*> hCtrlDeltaPhiTauMETAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlMinDeltaPhiTauJetAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlMaxDeltaPhiTauJetAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBackMinimumAfterMtSelections;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DMinimum;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DJet1;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DJet2;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DJet3;
    std::vector<WrappedTH2*> hCtrlEWKFakeTausQCDTailKiller2DJet4;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausDeltaPhiTauMETAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMinDeltaPhiTauJetAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausMaxDeltaPhiTauJetAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlTopMassAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlTopPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlWMassAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlWPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTopMassAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausTopPtAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausWMassAfterMtSelections;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausWPtAfterMtSelections;

    // all selections
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterAllSelections;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionEWKControlRegion;
    std::vector<WrappedTH1*> hShapeTransverseMass;
    std::vector<WrappedTH1*> hShapeEWKFakeTausTransverseMass;
    std::vector<WrappedTH1*> hShapeEWKGenuineTausTransverseMass;
    std::vector<WrappedTH1*> hShapeEmbeddingLikeMultipleTausTransverseMass;

    std::vector<WrappedTH1*> hShapeProbabilisticBtagTransverseMass;
    std::vector<WrappedTH1*> hShapeProbabilisticBtagEWKFakeTausTransverseMass;
    std::vector<WrappedTH1*> hShapeProbabilisticBtagEmbeddingLikeMultipleTausTransverseMass;
    // NOTE: do we want to try out something like mT vs. rTau?

    // all selections with full mass
    std::vector<WrappedTH1*> hShapeFullMass;
    std::vector<WrappedTH1*> hShapeEWKFakeTausFullMass;
    std::vector<WrappedTH1*> hShapeEmbeddingLikeMultipleTausFullMass;
    // FIXME: Add unfolded histogram for mT vs. full mass

    // histograms to be filled at every step
    std::vector<CommonPlotsFilledAtEveryStep*> hEveryStepHistograms; // Owner of objects
  };
}

#endif
