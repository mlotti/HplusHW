// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlotsFilledAtEveryStep_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CommonPlotsFilledAtEveryStep_h

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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <string>

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
                          const QCDTailKiller::Data* qcdTailKillerData,
                          const TopSelectionManager::Data* topData,
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
    const TopSelectionManager::Data* fTopData;
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
    WrappedTH1* hMETCalo;
    WrappedTH1* hMETRaw;
    WrappedTH1* hMET;
    WrappedTH1* hMETphi;
    WrappedTH1* hMETSignificance;
    WrappedTH1* hMETOverTrackPtSum;
    WrappedTH1* hMETOverMHT;
    WrappedTH1* hMETOverTauPt;
    WrappedTH1* hNbjets;
    WrappedTH1* hDeltaPhiTauMET;
    WrappedTH1* hDeltaR_TauMETJet1MET;
    WrappedTH1* hDeltaR_TauMETJet2MET;
    WrappedTH1* hDeltaR_TauMETJet3MET;
    WrappedTH1* hDeltaR_TauMETJet4MET;
    WrappedTH1* hTopMass;
    WrappedTH1* hTopPt;
    WrappedTH1* hWMass;
    WrappedTH1* hWPt;
    WrappedTH1* hChargedHiggsPt; // Boost variable
    WrappedTH1* hTransverseMass;
    WrappedTH1* hFullMass;
  };

}
#endif
