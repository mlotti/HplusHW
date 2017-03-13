// -*- c++ -*-
#ifndef EventSelection_CommonPlots_h
#define EventSelection_CommonPlots_h

#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/CommonPlotsHelper.h"
#include "EventSelection/interface/CommonPlotsBase.h"
#include "EventSelection/interface/PUDependencyPlots.h"
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
    kHplus2tbAnalysis= 0,
    kEmbedding,
    kQCDMeasurement,
    kFakeBMeasurement,
    kQCDNormalizationSystematicsSignalRegion, // Needed for obtaining normalization systematics to data-driven control plots
    kQCDNormalizationSystematicsControlRegion // Needed for obtaining normalization systematics to data-driven control plots
  };

  CommonPlots(const ParameterSet& config, const CommonPlots::AnalysisType type, HistoWrapper& histoWrapper);
  ~CommonPlots();

  //Tau ID syst switches
  bool tauIDup;
  bool tauIDdown;
  
  void book(TDirectory* dir, bool isData);
  
  /// Initialize (call this at the beginning of each event; prevents double-counting of events)
  void initialize();
  /// Sets factorisation bin (call this for each event before filling the first histogram!)
  void setFactorisationBinForEvent(const std::vector<float>& values=std::vector<float>{}) { fHistoSplitter.setFactorisationBinForEvent(values); }
  
  /// Returns the histogram splitter object (usecase: QCD measurement)
  HistoSplitter& getHistoSplitter() { return fHistoSplitter; }
  /// Returns the histogram settings for pt histograms (usecase: QCD measurement)
  const HistogramSettings& getPtBinSettings() const { return fPtBinSettings; }
  /// Returns the histogram settings for MET bins (usecase: QCD measurement)
  const HistogramSettings& getMetBinSettings() const { return fMetBinSettings; }
  /// Returns the histogram settings for HT bins (usecase: Htb analysis)
  const HistogramSettings& getHtBinSettings() const { return fHtBinSettings; }
  /// Returns the histogram settings for Mt bins (usecase: QCD measurement)
  const HistogramSettings& getMtBinSettings() const { return fMtBinSettings; }

  /** Special method for setting genuine tau status 
    * (it is usually set through TauSelection via CommonPlots::fillControlPlotsAfterTauSelection)
    */
  void setGenuineTauStatus(const bool isGenuineTau) { bIsGenuineTau = isGenuineTau; };
  
  //===== unique filling methods (to be called inside the event selection routine only, i.e. (before a passing decision is done))
  void fillControlPlotsAtVertexSelection(const Event& event);
  //void fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData);
  void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  void fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  void fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data);
  void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  void fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data);
  //void fillControlPlotsAtTopSelection(const Event& event, const TopSelectionManager::Data& data);
  //void fillControlPlotsAtEvtTopology(const Event& event, const EvtTopology::Data& data);
  
  //===== unique filling methods (to be called AFTER return statement from analysis routine)
  void setNvertices(int vtx) { iVertices = vtx; fPUDependencyPlots->setNvtx(vtx); }
  void fillControlPlotsAfterTrigger(const Event& event);
  void fillControlPlotsAfterMETFilter(const Event& event);
  void fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAfterMETTriggerScaleFactor(const Event& event);
  void fillControlPlotsAfterTopologicalSelections(const Event& event, bool withoutTau=false);
  void fillControlPlotsAfterAllSelections(const Event& event, bool withoutTau=false);
  void fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight);
  //void fillControlPlotsAfterAllSelectionsWithFullMass(const Event& event, FullHiggsMassCalculator::Data& data);

  //===== Filling of control plots for determining QCD shape uncertainty
  void fillControlPlotsForQCDShapeUncertainty(const Event& event,
                                              const AngularCutsBackToBack::Data& collinearAngularCutsData,
                                              const BJetSelection::Data& bJetData,
                                              const METSelection::Data& metData,
                                              const AngularCutsCollinear::Data& backToBackAngularCutsData);
  
  /// Getter for all vertices
  int nVertices() const { return iVertices; }

private:
  /// Returns true if anti-isolated taus need to be used (QCD measurement)
  const bool usesAntiIsolatedTaus() const { return fAnalysisType == kQCDMeasurement ||
    fAnalysisType == kQCDNormalizationSystematicsControlRegion; }
  
private:
  ///===== Config params
  const bool fEnableGenuineTauHistograms;
  
  ///===== Analysis type
  const AnalysisType fAnalysisType;

  ///===== HistoWrapper;
  HistoWrapper fHistoWrapper;
  
  ///===== Histogram splitter
  HistoSplitter fHistoSplitter;

  ///===== Settings for histogram binning
  const HistogramSettings fNVerticesBinSettings;
  const HistogramSettings fPtBinSettings;
  const HistogramSettings fEtaBinSettings;
  const HistogramSettings fPhiBinSettings;
  const HistogramSettings fDeltaPhiBinSettings;
  const HistogramSettings fDeltaRBinSettings;
  const HistogramSettings fRtauBinSettings;
  const HistogramSettings fNjetsBinSettings;
  const HistogramSettings fMetBinSettings;
  const HistogramSettings fHtBinSettings;
  const HistogramSettings fBJetDiscriminatorBinSettings;
  const HistogramSettings fAngularCuts1DSettings;
  //const HistogramSettings fTopMassBinSettings;
  //const HistogramSettings fWMassBinSettings;
  const HistogramSettings fMtBinSettings;
  //const HistogramSettings fInvmassBinSettings;

  ///===== Histograms
  // NOTE: think before adding a histogram - they do slow down the analysis a lot
  // NOTE: the histograms with the prefix hCtrl are used as data driven control plots
  // NOTE: the histograms with the prefix hShape are used as shape histograms
  // NOTE: histogram triplets contain the inclusive and events with fake tau histograms
  
  // vertex

  // tau selection

  // tau trigger SF

  // veto tau selection
  
  // electron veto
  
  // muon veto

  // tau veto
 
  // jet selection
  HistoSplitter::SplittedTripletTH1s hCtrlNjets;
  
  // MET trigger SF
  HistoSplitter::SplittedTripletTH1s hCtrlNjetsAfterJetSelectionAndMETSF;
  
  // collinear angular cuts
  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsMinimum;
  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsJet1;
  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsJet2;
  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsJet3;
  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsJet4;
  
  // this is the point of "standard selections"
  HistoSplitter::SplittedTripletTH1s hCtrlNVerticesAfterStdSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauEtaAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPhiAfterStdSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlSelectedTauEtaPhiAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauLdgTrkPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauDecayModeAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauNProngsAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauRtauAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauSourceAfterStdSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlNJetsAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetPtAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetEtaAfterStdSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlJetEtaPhiAfterStdSelections;
  
  // MET
  HistoSplitter::SplittedTripletTH1s hCtrlMET;
  HistoSplitter::SplittedTripletTH1s hCtrlMETPhi;
  
  // b tagging
  HistoSplitter::SplittedTripletTH1s hCtrlNBJets;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetPt;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetEta;
  HistoSplitter::SplittedTripletTH1s hCtrlBDiscriminator;
  
  // back-to-back angular cuts
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsMinimum;
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsJet1;
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsJet2;
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsJet3;
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsJet4;

  // control plots after all selections
  HistoSplitter::SplittedTripletTH1s hCtrlNVerticesAfterAllSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauPhiAfterAllSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlSelectedTauEtaPhiAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauLdgTrkPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauDecayModeAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauNProngsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauRtauAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauSourceAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlSelectedTauIPxyAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlNJetsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlJetEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH2s hCtrlJetEtaPhiAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlHTAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMHTAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMinDeltaPhiJetMHTAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMaxDeltaPhiJetMHTAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMinDeltaRJetMHTAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMinDeltaRReversedJetMHTAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlCollinearAngularCutsMinimumAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlMETAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlMETPhiAfterAllSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlNBJetsAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetPtAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBJetEtaAfterAllSelections;
  HistoSplitter::SplittedTripletTH1s hCtrlBDiscriminatorAfterAllSelections;
  
  HistoSplitter::SplittedTripletTH1s hCtrlBackToBackAngularCutsMinimumAfterAllSelections;

  HistoSplitter::SplittedTripletTH1s hCtrlDeltaPhiTauMetAfterAllSelections;
  
  // shape plots after all selections
  HistoSplitter::SplittedTripletTH1s hShapeTransverseMass;
  HistoSplitter::SplittedTripletTH1s hShapeProbabilisticBtagTransverseMass;

  // Other plots
  WrappedTH1* hNSelectedVsRunNumber; // For data only
  
  //====== Plots from base class
  std::vector<CommonPlotsBase*> fBaseObjects;
  PUDependencyPlots* fPUDependencyPlots;
  
  //====== Data cache
  /// Cached data objects from silent analyze
  //VertexSelection::Data fVertexData;
  int iVertices;
  TauSelection::Data fTauData;
  //FakeTauIdentifier::Data fFakeTauData;
  bool bIsGenuineTau;
  ElectronSelection::Data fElectronData;
  MuonSelection::Data fMuonData;
  JetSelection::Data fJetData;
  AngularCutsBackToBack::Data fCollinearAngularCutsData;
  BJetSelection::Data fBJetData;
  METSelection::Data fMETData;
  AngularCutsCollinear::Data fBackToBackAngularCutsData;

  /// Helper
  CommonPlotsHelper fHelper;
};

#endif
