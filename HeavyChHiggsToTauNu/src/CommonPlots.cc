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

  void CommonPlotsFilledAtEveryStep::fill() {
     // Safety check
     if (!fDataObjectsCached)
       throw cms::Exception("Assert") << "CommonPlotsFilledAtEveryStep: data objects have not been cached! (did you forget to call CommonPlotsFilledAtEveryStep::cacheDataObjects from CommonPlots::initialize?)";
    hNVertices->Fill(fNVertices);
    if (!fVertexData->passedEvent()) return; // Plots do not make sense if no PV has been found
    
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(int nVertices,
                                                      const VertexSelection::Data* vertexData,
                                                      const TauSelection::Data* tauData,
                                                      const GlobalElectronVeto::Data* electronData,
                                                      const GlobalMuonVeto::Data* muonData,
                                                      const JetSelection::Data* jetData,
                                                      const METSelection::Data* metData,
                                                      const BTagging::Data* bJetData,
                                                      const TopChiSelection::Data* topData,
                                                      const EvtTopology::Data* evtTopology) {
    fNVertices = nVertices;
    fVertexData = vertexData;
    fTauData = tauData;
    fElectronData = electronData;
    fMuonData = muonData;
    fJetData = jetData;
    fMETData = metData;
    fBJetData = bJetData;
    fTopData = topData;
    fEvtTopology = evtTopology;
    fDataObjectsCached = true;
  }

  // ====================================================================================================

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    bDataObjectsCached(false),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper) {
    // Create histograms
    
  }

  CommonPlots::~CommonPlots() {
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it < hEveryStepHistograms.end(); ++it)
      delete (*it);
    hEveryStepHistograms.clear();
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               int nVertices,
                               VertexSelection& vertexSelection,
                               TauSelection& tauSelection,
                               GlobalElectronVeto& eVeto,
                               GlobalMuonVeto& muonVeto,
                               JetSelection& jetSelection,
                               METSelection& metSelection,
                               BTagging& bJetSelection,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology) {
    // Obtain data objects only, if they have not yet been cached
    if (bDataObjectsCached) return;
    bDataObjectsCached = true;
    fNVertices = nVertices;
    // Obtain data objects
    fVertexData = vertexSelection.silentAnalyze(iEvent, iSetup);
    if (!fVertexData.passedEvent()) return; // Plots do not make sense if no PV has been found
    fTauData = tauSelection.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex()->z());
    if (!fTauData.passedEvent()) return; // Need to require one tau in the event
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);
    fMuonData = muonVeto.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex());
    fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fNVertices);
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getAllJets());
    fBJetData = bJetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());
    fTopData = topChiSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets());
    fEvtTopology = evtTopology.silentAnalyze(iEvent, iSetup, *(fTauData.getSelectedTau()), fJetData.getAllIdentifiedJets());

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(fNVertices,
                              &fVertexData,
                              &fTauData,
                              &fElectronData,
                              &fMuonData,
                              &fJetData,
                              &fMETData,
                              &fBJetData,
                              &fTopData,
                              &fEvtTopology);
    }
  }

  CommonPlotsFilledAtEveryStep* CommonPlots::createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) {
    // Create and return object, but sneakily save the pointer for later use
    CommonPlotsFilledAtEveryStep* myObject = new CommonPlotsFilledAtEveryStep(fHistoWrapper, label, enterSelectionFlowPlot, selectionFlowPlotLabel);
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

  void CommonPlots::fillControlPlots(const GlobalMuonVeto::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const JetSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const METSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const BTagging::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const TopChiSelection::Data& data) {
    
  }

   void CommonPlots::fillControlPlots(const EvtTopology::Data& data) {
    
  }

  void CommonPlots::fillFinalPlots() {
    
  }
}