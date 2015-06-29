// -*- c++ -*-
#ifndef EventSelection_CommonPlots_h
#define EventSelection_CommonPlots_h

#include "EventSelection/interface/EventSelections.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/HistogramSettings.h"
#include "Framework/interface/HistoSplitter.h"
#include "Framework/interface/HistoWrapper.h"

#include "TDirectory.h"

#include <vector>

class CommonPlots {
public:
  enum AnalysisType {
    kSignalAnalysis = 0,
    kEmbedding,
    kQCDMeasurement,
    kQCDNormalizationSystematicsSignalRegion, // Needed for obtaining normalization systematics to data-driven control plots
    kQCDNormalizationSystematicsControlRegion // Needed for obtaining normalization systematics to data-driven control plots
  };

  CommonPlots(const ParameterSet& config, const CommonPlots::AnalysisType type, HistoWrapper& histoWrapper);
  ~CommonPlots();
  
  void book(TDirectory *dir);
/*
  //===== unique filling methods (to be called inside the event selection routine only)
  //void fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData);
  void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  void fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data);
  void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  void fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data);
  //void fillControlPlotsAtTopSelection(const Event& event, const TopSelectionManager::Data& data);
  //void fillControlPlotsAtEvtTopology(const Event& event, const EvtTopology::Data& data);
  
  //===== unique filling methods (to be called AFTER return statement from analysis routine)
  void fillControlPlotsAfterTauTriggerScaleFactor(const Event& event);
  void fillControlPlotsAfterMETTriggerScaleFactor(const Event& event);
  void fillControlPlotsAfterTopologicalSelections(const Event& event);
  void fillControlPlotsAfterAllSelections(const Event& event, double transverseMass);
  void fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, double transverseMass);
  //void fillControlPlotsAfterAllSelectionsWithFullMass(const Event& event, FullHiggsMassCalculator::Data& data);
*/

private:
  //===== Analysis type
  const AnalysisType fAnalysisType;
  //===== Histogram splitter
  HistoSplitter fHistoSplitter;
  //===== Settings for histogram binning
  const HistogramSettings fPtBinSettings;
  const HistogramSettings fEtaBinSettings;
  const HistogramSettings fPhiBinSettings;
  const HistogramSettings fDeltaPhiBinSettings;
  const HistogramSettings fRtauBinSettings;
  const HistogramSettings fNjetsBinSettings;
  const HistogramSettings fMetBinSettings;
  const HistogramSettings fBJetDiscriminatorBinSettings;
  const HistogramSettings fAngularCuts1DSettings;
  //const HistogramSettings fTopMassBinSettings;
  //const HistogramSettings fWMassBinSettings;
  const HistogramSettings fMtBinSettings;
  //const HistogramSettings fInvmassBinSettings;
  

};

#endif
