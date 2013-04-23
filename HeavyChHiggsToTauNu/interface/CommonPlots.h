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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationAnalysis.h"

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
                          const TopChiSelection::Data* topData);

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
    const TopChiSelection::Data* fTopData;

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
  };

  /**
   * Class to contain plots common to all analyses (signalAnalysis, QCD, ...)
   */
  class CommonPlots {
  public:
    CommonPlots(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
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
                    TopChiSelection& topChiSelection,
                    EvtTopology& evtTopology);
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
                    TopChiSelection& topChiSelection,
                    EvtTopology& evtTopology);

    /// create object containing histograms to be filled after all (or almost all) selection steps
    CommonPlotsFilledAtEveryStep* createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot = false, std::string selectionFlowPlotLabel = "");

    /// unique filling methods (to be called before return statement)
    void fillControlPlots(const TriggerSelection::Data& data);
    void fillControlPlots(const edm::Event& iEvent, const VertexSelection::Data& data);
    void fillControlPlots(const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData);
    void fillControlPlots(const ElectronSelection::Data& data);
    void fillControlPlots(const MuonSelection::Data& data);
    void fillControlPlots(const JetSelection::Data& data);
    void fillControlPlots(const METSelection::Data& data);
    void fillControlPlots(const BTagging::Data& data);
    void fillControlPlots(const TopChiSelection::Data& data);
    void fillControlPlots(const EvtTopology::Data& data);
    void fillFinalPlots();
    void fillFinalPlotsForFakeTaus();

  protected:
    
    /// Creates histograms
    void createHistograms();
    /// Status indicating wheather the data objects have been cached
    bool bDataObjectsCached;
    /// Event counter object
    EventCounter& fEventCounter;
    /// HistoWrapper object
    HistoWrapper& fHistoWrapper;
    /// Base directory in root file for every step histograms
    edm::Service<TFileService> fs;
    TFileDirectory fCommonBaseDirectory;
    TFileDirectory fEveryStepDirectory;
    /// Normalisation analysis object
    NormalisationAnalysis fNormalisationAnalysis;
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
    TopChiSelection::Data fTopData;
    EvtTopology::Data fEvtTopology;

    // Input parameters

    // Counters - needed or not?

    // Histograms ------------------------------------------
    // vertex
    
    // tau selection
    WrappedTH2* hTauPhiOscillationX;
    WrappedTH2* hTauPhiOscillationY;
    
    // electron veto
    
    // muon veto
    
    // final
    WrappedTH2* hDphiTauMetVsDphiJet1MHT;
    WrappedTH2* hDphiTauMetVsDphiJet2MHT;
    WrappedTH2* hDphiTauMetVsDphiJet3MHT;
    WrappedTH2* hDphiTauMetVsDphiJet4MHT;
    WrappedTH2* hDphiTauMetVsDphiTauMHT;

    WrappedTH2* hDphiTauMetVsDphiJet1MHTFakeTaus;
    WrappedTH2* hDphiTauMetVsDphiJet2MHTFakeTaus;
    WrappedTH2* hDphiTauMetVsDphiJet3MHTFakeTaus;
    WrappedTH2* hDphiTauMetVsDphiJet4MHTFakeTaus;
    WrappedTH2* hDphiTauMetVsDphiTauMHTFakeTaus;

    // histograms to be filled at every step
    std::vector<CommonPlotsFilledAtEveryStep*> hEveryStepHistograms; // Owner of objects
  };
}

#endif