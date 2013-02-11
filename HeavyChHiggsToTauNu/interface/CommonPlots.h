// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlots_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlots_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

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
    CommonPlotsFilledAtEveryStep(HistoWrapper& histoWrapper, std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel);
    ~CommonPlotsFilledAtEveryStep();
    /// Fills histograms; supply pointer to data object from analyse() call, if it exists
    void fill();
    /// Returns status of wheather the item will be used for creating the selection flow plot
    const bool enterSelectionFlowPlotStatus() const { return fEnterSelectionFlowPlot; }
    /// 
    const std::string getSelectionFlowPlotLabel() const { return fSelectionFlowPlotLabel; }
    /// Cache data objects, to be called from CommonPlots::initialize()
    void cacheDataObjects(int nVertices,
                          const VertexSelection::Data* vertexData,
                          const TauSelection::Data* tauData,
                          const GlobalElectronVeto::Data* electronData);

  private:
    /// Status indicating wheather the data objects have been cached
    bool fDataObjectsCached;
    /// Status indicating if the step is included in the selection flow plot
    bool fEnterSelectionFlowPlot;
    std::string fSelectionFlowPlotLabel;

    /// Cached data objects from silent analyze
    int fNVertices;
    const VertexSelection::Data* fVertexData;
    const TauSelection::Data* fTauData;
    const GlobalElectronVeto::Data* fElectronData;

    /// Histograms to be plotted after every step
    WrappedTH1* hNVertices;
    WrappedTH1* hTauPt;
    WrappedTH1* hTauEta;
    WrappedTH1* hTauPhi;
    WrappedTH1* hRtau;
    WrappedTH1* hFakeTauCategory;
    WrappedTH1* hElectronSelectedPt;
    WrappedTH1* hMuonSelectedPt;
    WrappedTH1* hNjets;
    WrappedTH1* hMET;
    WrappedTH1* hMETphi;
    WrappedTH1* hNbjets;
    WrappedTH1* hDeltaPhiTauMET;
    WrappedTH1* hDeltaPhiJetMET;
    WrappedTH1* hTransverseMass;
  };

  /**
   * Class to contain plots common to all analyses (signalAnalysis, QCD, ...)
   */
  class CommonPlots {
  public:
    CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~CommonPlots();

    /// Initialize data objects
    void initialize(const edm::Event& iEvent,
                    const edm::EventSetup& iSetup,
                    int nVertices,
                    VertexSelection& vertexSelection,
                    TauSelection& tauSelection,
                    GlobalElectronVeto& eVeto); // FIXME add more data objects

    /// create object containing histograms to be filled after all (or almost all) selection steps
    CommonPlotsFilledAtEveryStep* createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot = false, std::string selectionFlowPlotLabel = "");

    /// unique filling methods (to be called before return statement)
    void fillControlPlots(const TriggerSelection::Data& data);
    void fillControlPlots(const VertexSelection::Data& data);
    void fillControlPlots(const TauSelection::Data& data);
    void fillControlPlots(const GlobalElectronVeto::Data& data);
    /*void fillControlPlots(const GlobalMuonVeto::Data& data);
    void fillControlPlots(const JetSelection::Data& data);
    void fillControlPlots(const METSelection::Data& data);
    void fillControlPlots(const BTagging::Data& data);*/

  private:
    /// Status indicating wheather the data objects have been cached
    bool bDataObjectsCached;
    /// Event counter object
    EventCounter& fEventCounter;
    /// HistoWrapper object
    HistoWrapper& fHistoWrapper;
    /// Cached data objects from silent analyze
    int fNVertices;
    VertexSelection::Data fVertexData;
    TauSelection::Data fTauData;
    GlobalElectronVeto::Data fElectronData;
    // FIXME add more ...

    // Input parameters

    // Counters - needed or not?

    // Histograms ------------------------------------------
    // vertex
    
    // tau selection
    
    // electron veto
    
    // muon veto
    
    
    
    // histograms to be filled at every step
    std::vector<CommonPlotsFilledAtEveryStep*> hEveryStepHistograms; // Owner of objects
  };
}

#endif