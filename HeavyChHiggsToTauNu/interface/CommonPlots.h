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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationAnalysis.h"
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
   * Helper class to contain the plots to be plotted after each selection
   */
  class CommonPlotsFilledAtEveryStep {
  public:
    CommonPlotsFilledAtEveryStep(HistoWrapper& histoWrapper, TFileDirectory& dir, std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel);
    ~CommonPlotsFilledAtEveryStep();
    /// Fills histograms; supply pointer to data object from analyse() call, if it exists
    void fill();
    /// Returns status of wheather the item will be used for creating the selection flow plot
    const bool enterSelectionFlowPlotStatus() const { return fEnterSelectionFlowPlot; }
    /// 
    const std::string getSelectionFlowPlotLabel() const { return fSelectionFlowPlotLabel; }
    /// Cache data objects, to be called from CommonPlots::initialize()
    void cacheDataObjects(const VertexSelection::Data* vertexData,
                          const TauSelection::Data* tauData,
                          const FakeTauIdentifier::Data* fakeTauData,
                          const ElectronSelection::Data* electronData,
                          const MuonSelection::Data* muonData,
                          const JetSelection::Data* jetData,
                          const METSelection::Data* metData,
                          const BTagging::Data* bJetData,
                          const QCDTailKiller::Data* qcdTailKillerData,
                          const TopChiSelection::Data* topData,
                          const FullHiggsMassCalculator::Data* fullHiggsMassData);

  private:
    /// Status indicating wheather the data objects have been cached
    bool fDataObjectsCached;
    /// Status indicating if the step is included in the selection flow plot
    bool fEnterSelectionFlowPlot;
    std::string fSelectionFlowPlotLabel;

    /// Cached data objects from silent analyze
    const VertexSelection::Data* fVertexData;
    const TauSelection::Data* fTauData;
    const FakeTauIdentifier::Data* fFakeTauData;
    const ElectronSelection::Data* fElectronData;
    const MuonSelection::Data* fMuonData;
    const JetSelection::Data* fJetData;
    const METSelection::Data* fMETData;
    const BTagging::Data* fBJetData;
    const QCDTailKiller::Data* fQCDTailKillerData;
    const TopChiSelection::Data* fTopData;
    const FullHiggsMassCalculator::Data* fFullHiggsMassData;

    /// Histograms to be plotted after every step
    WrappedTH1* hNVertices;
    WrappedTH1* hFakeTauStatus;
    WrappedTH1* hTauPt;
    WrappedTH1* hTauEta;
    WrappedTH1* hTauPhi;
    WrappedTH1* hRtau;
    WrappedTH1* hSelectedElectrons;
    WrappedTH1* hSelectedMuons;
    WrappedTH1* hNjets;
    WrappedTH1* hNjetsAllIdentified;
    WrappedTH1* hMETRaw;
    WrappedTH1* hMET;
    WrappedTH1* hMETphi;
    WrappedTH1* hNbjets;
    WrappedTH1* hDeltaPhiTauMET;
    WrappedTH1* hDeltaR_TauMETJet1MET;
    WrappedTH1* hDeltaR_TauMETJet2MET;
    WrappedTH1* hDeltaR_TauMETJet3MET;
    WrappedTH1* hDeltaR_TauMETJet4MET;
    WrappedTH1* hTransverseMass;
    WrappedTH1* hFullMass;
  };

  /**
   * Class to contain plots common to all analyses (signalAnalysis, QCD, ...)
   */
  class CommonPlots {
  public:
    CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, bool plotSeparatelyFakeTaus);
    ~CommonPlots();

    /// Initialize data objects; call for every event
    void initialize(const edm::Event& iEvent,
                    const edm::EventSetup& iSetup,
                    VertexSelection::Data& vertexData,
                    TauSelection& tauSelection,
                    FakeTauIdentifier& fakeTauIdentifier,
                    ElectronSelection& eVeto,
                    MuonSelection& muonVeto,
                    JetSelection& jetSelection,
                    METSelection& metSelection,
                    BTagging& bJetSelection,
                    QCDTailKiller& qcdTailKiller,
                    TopChiSelection& topChiSelection,
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
                    METSelection& metSelection,
                    BTagging& bJetSelection,
                    QCDTailKiller& qcdTailKiller,
                    TopChiSelection& topChiSelection,
                    EvtTopology& evtTopology,
                    FullHiggsMassCalculator& fullHiggsMassCalculator);

    /// create object containing histograms to be filled after all (or almost all) selection steps
    CommonPlotsFilledAtEveryStep* createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot = false, std::string selectionFlowPlotLabel = "");

    /// unique filling methods (to be called AFTER return statement)
    void fillControlPlotsAfterVertexSelection(const edm::Event& iEvent, const VertexSelection::Data& data);
    void fillControlPlotsAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData, METSelection& metSelection);
    void fillControlPlotsAfterTauTriggerScaleFactor(const edm::Event& iEvent);
    void fillControlPlotsAfterMETTriggerScaleFactor(const edm::Event& iEvent);
    void fillControlPlotsAfterAllSelections(const edm::Event& iEvent, double transverseMass);
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
    void fillControlPlotsAtTopSelection(const edm::Event& iEvent, const TopChiSelection::Data& data);
    void fillControlPlotsAtEvtTopology(const edm::Event& iEvent, const EvtTopology::Data& data);
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
    const bool bOptionEnableNormalisationAnalysis;
    const bool bOptionEnableMETOscillationAnalysis;
    /// Indicator wheather fake taus should be handled separately
    bool fPlotSeparatelyFakeTaus;
    /// Creates histograms
    void createHistograms();
    /// Event counter object
    EventCounter& fEventCounter;
    /// HistoWrapper object
    HistoWrapper& fHistoWrapper;
    /// Base directory in root file for every step histograms
    edm::Service<TFileService> fs;
    TFileDirectory fCommonBaseDirectory;
    TFileDirectory fEveryStepDirectory;
    /// Normalisation analysis object
    NormalisationAnalysis* fNormalisationAnalysis;
    /// Selection objects
    TauSelection* fTauSelection;
    FakeTauIdentifier* fFakeTauIdentifier;
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
    TopChiSelection::Data fTopData;
    EvtTopology::Data fEvtTopology;
    FullHiggsMassCalculator::Data fFullHiggsMassData;

    // Input parameters
    HistogramSettings fPtBinSettings;
    HistogramSettings fEtaBinSettings;
    HistogramSettings fPhiBinSettings;
    HistogramSettings fRtauBinSettings;
    HistogramSettings fNjetsBinSettings;
    HistogramSettings fMetBinSettings;
    HistogramSettings fTailKiller1DSettings;
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
    WrappedTH1* hCtrlIdentifiedElectronPt;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedElectronPt;

    // muon veto
    WrappedTH1* hCtrlIdentifiedMuonPt;
    WrappedTH1* hCtrlEWKFakeTausIdentifiedMuonPt;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterLeptonVeto;

    // jet selection
    WrappedTH1* hCtrlNjets;
    WrappedTH1* hCtrlEWKFakeTausNjets;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterNjets;

    // MET trigger SF
    WrappedTH1* hCtrlNjetsAfterJetSelectionAndMETSF;
    WrappedTH1* hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF;

    // improved delta phi collinear cuts (currently the point of the std. selections)
    std::vector<WrappedTH1*> hCtrlQCDTailKillerCollinear;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerCollinear;

    WrappedTH1* hCtrlSelectedTauPtAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauEtaAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hCtrlSelectedTauEtaVsPhiAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauLeadingTrkPtAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauRtauAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauPAfterStandardSelections;
    WrappedTH1* hCtrlSelectedTauLeadingTrkPAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections;
    WrappedTH2* hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauPAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections;

    WrappedTH1* hCtrlNjetsAfterStandardSelections;
    WrappedTH1* hCtrlEWKFakeTausNjetsAfterStandardSelections;

    // MET selection
    WrappedTH1* hCtrlMET;
    WrappedTH1* hCtrlEWKFakeTausMET;
    
    // b tagging
    WrappedTH1* hCtrlNbjets;
    WrappedTH1* hCtrlEWKFakeTausNbjets;
    
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterBjets;

    // improved delta phi back to back cuts
    std::vector<WrappedTH1*> hCtrlQCDTailKillerBackToBack;
    std::vector<WrappedTH1*> hCtrlEWKFakeTausQCDTailKillerBackToBack;
    
    // top selection
    
    // evt topology
    
    // all selections
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionAfterAllSelections;
    METPhiOscillationCorrection* fMETPhiOscillationCorrectionEWKControlRegion;
    WrappedTH1 *hShapeTransverseMass;
    WrappedTH1 *hShapeEWKFakeTausTransverseMass;
    // NOTE: do we want to try out something like mT vs. rTau?

    // all selections with full mass
    WrappedTH1 *hShapeFullMass;
    WrappedTH1 *hShapeEWKFakeTausFullMass;
    // FIXME: Add unfolded histogram for mT vs. full mass

    // histograms to be filled at every step
    std::vector<CommonPlotsFilledAtEveryStep*> hEveryStepHistograms; // Owner of objects
  };
}

#endif
