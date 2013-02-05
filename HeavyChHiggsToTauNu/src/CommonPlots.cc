// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <sstream>

namespace HPlus {
  CommonPlotsFilledAtEveryStep::CommonPlotsFilledAtEveryStep(HistoWrapper& histoWrapper, std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) :
    fDataObjectsCached(false),
    fEnterSelectionFlowPlot(enterSelectionFlowPlot),
    fSelectionFlowPlotLabel(selectionFlowPlotLabel) {
    // Create directory for histogram
    edm::Service<TFileService> fs;
    std::stringstream myStream;
    myStream << "CommonPlots_" << label;
    TFileDirectory myDir = fs->mkdir(myStream.str().c_str());
    // Create histograms
    hNVertices = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "nVertices", "Number of vertices;N_{vertices};N_{events}", 60, 0, 60);
  }

  CommonPlotsFilledAtEveryStep::~CommonPlotsFilledAtEveryStep() {}

  void CommonPlotsFilledAtEveryStep::fill(int nVertices,
                                          VertexSelection::Data* vertexData,
                                          TauSelection::Data* tauData,
                                          GlobalElectronVeto::Data* electronData) {
     // Safety check
     if (!fDataObjectsCached)
       throw cms::Exception("Assert") << "CommonPlotsFilledAtEveryStep: data objects have not been cached! (did you forget to call CommonPlotsFilledAtEveryStep::cacheDataObjects from CommonPlots::initialize?)";
    // Select which data object to use
    VertexSelection::Data* myVertexData = fVertexData;
    if (vertexData) myVertexData = vertexData;
    TauSelection::Data* myTauData = fTauData;
    if (tauData) myTauData = tauData;
    GlobalElectronVeto::Data* myElectronData = fElectronData;
    if (electronData) myElectronData = electronData;
    // Do filling with selected data objects
    hNVertices->Fill(nVertices);
    if (!myVertexData->passedEvent()) return; // Plots do not make sense if no PV has been found
    
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(VertexSelection::Data* vertexData,
                                                      TauSelection::Data* tauData,
                                                      GlobalElectronVeto::Data* electronData) {
    fVertexData = vertexData;
    fTauData = tauData;
    fElectronData = electronData;
    fDataObjectsCached = true;
  }

  // ====================================================================================================

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    BaseSelection(eventCounter, histoWrapper),
    bDataObjectsCached(false) {
    // Create histograms
    
  }

  CommonPlots::~CommonPlots() {
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it < hEveryStepHistograms.end(); ++it)
      delete (*it);
    hEveryStepHistograms.clear();
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               VertexSelection& vertexSelection,
                               TauSelection& tauSelection,
                               GlobalElectronVeto& eVeto) {
    // Obtain data objects only, if they have not yet been cached
    if (bDataObjectsCached) return;
    bDataObjectsCached = true;

    // Obtain data objects
    fVertexData = vertexSelection.silentAnalyze(iEvent, iSetup);
    if (!fVertexData.passedEvent()) return; // Plots do not make sense if no PV has been found
    fTauData = tauSelection.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex()->z());
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(&fVertexData,
                              &fTauData,
                              &fElectronData);
    }
  }

  CommonPlotsFilledAtEveryStep* CommonPlots::createCommonPlotsFilledAtEveryStep(HistoWrapper& histoWrapper, std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) {
    // Create and return object, but sneakily save the pointer for later use
    CommonPlotsFilledAtEveryStep* myObject = new CommonPlotsFilledAtEveryStep(histoWrapper, label, enterSelectionFlowPlot, selectionFlowPlotLabel);
    hEveryStepHistograms.push_back(myObject);
    return myObject;
  }

  void CommonPlots::fillControlPlots(const TriggerSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const VertexSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const TauSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const GlobalElectronVeto::Data& data) {
    
  }


}