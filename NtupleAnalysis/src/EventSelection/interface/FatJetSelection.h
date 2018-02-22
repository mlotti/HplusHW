// -*- c++ -*-
#ifndef EventSelection_FatJetSelection_h
#define EventSelection_FatJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/EventSelections.h"
#include "DataFormat/interface/AK8Jet.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"
#include <boost/concept_check.hpp>

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class FatJetSelection: public BaseSelection {
public:
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    // Status of passing event selection
    bool passedSelection() const { return bPassedSelection; }

    // Obtain number of selected fat jets
    int getNumberOfSelectedFatJets() const { return fSelectedFatJets.size(); }

    // Obtain collection of selected fat jets
    const std::vector<AK8Jet>& getSelectedFatJets() const { return fSelectedFatJets; }

    // Obtain collection of all fat jets
    const std::vector<AK8Jet>& getAllFatJets() const { return fAllFatJets; }

    // Check if fat jet matching to the leading top was a success
    bool fatjetMatchedToTopFound() const { return (fFatJetMatchedToTop.size() > 0); }

    // Obtain fat jet matching to leading trijet system
    const AK8Jet& getFatJetMatchedToTop()  const; // { return 
    // const math::XYZTLorentzVector&  // alex
    // const AK8Jet& getFatJetMatchedToTau() const;

    friend class FatJetSelection;

  private:
    // Boolean for passing selection
    bool bPassedSelection;

    // All fat jets (needed for MET)
    std::vector<AK8Jet> fAllFatJets;
    
    // Fat Jet collection after all selections
    std::vector<AK8Jet> fSelectedFatJets;

    // Fat Jet matched to leading trijet system
    std::vector<AK8Jet> fFatJetMatchedToTop;

  };
  
  // Main class
  /// Constructor with histogramming
  explicit FatJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit FatJetSelection(const ParameterSet& config);
  virtual ~FatJetSelection();
  
  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const TopSelectionBDT::Data& topData);
  Data silentAnalyzeWithoutTop(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const TopSelectionBDT::Data& topData);
  Data analyzeWithoutTop(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const TopSelectionBDT::Data& topData);
  
  void findFatJetMatchingToTop(std::vector<AK8Jet>& collection, const Event& event,   const math::XYZTLorentzVector& topP);
  //const math::LorentzVectorT<double>& topP);
  
  // Input parameters
  const std::vector<float> fFatJetPtCuts;
  const std::vector<float> fFatJetEtaCuts;
  const float fTopMatchingDeltaR;
  const DirectionalCut<int> fNumberOfFatJetsCut;
  
  // Event counter for passing selection
  Count cPassedFatJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedFatJetID;
  Count cSubPassedFatJetPUID;
  Count cSubPassedDeltaRMatchWithTop;
  Count cSubPassedEta;
  Count cSubPassedPt;
  Count cSubPassedFatJetCount;

  // Histograms (1D)
  WrappedTH1 *hFatJetPtAll;
  WrappedTH1 *hFatJetEtaAll;
  WrappedTH1 *hFatJetPhiAll;
  WrappedTH1 *hFatJetCSVAll;
  WrappedTH1 *hFatJettau1All;
  WrappedTH1 *hFatJettau2All;
  WrappedTH1 *hFatJettau3All;
  WrappedTH1 *hFatJettau4All;
  WrappedTH1 *hFatJettau21All;
  WrappedTH1 *hFatJettau32All;  
  
  WrappedTH1 *hFatJetPtPassed;
  WrappedTH1 *hFatJetEtaPassed;
  WrappedTH1 *hFatJetPhiPassed;
  WrappedTH1 *hFatJetCSVPassed;
  WrappedTH1 *hFatJettau1Passed;
  WrappedTH1 *hFatJettau2Passed;
  WrappedTH1 *hFatJettau3Passed;
  WrappedTH1 *hFatJettau4Passed;
  WrappedTH1 *hFatJettau21Passed;
  WrappedTH1 *hFatJettau32Passed;  
  
  std::vector<WrappedTH1*> hSelectedFatJetPt;
  std::vector<WrappedTH1*> hSelectedFatJetEta;
  std::vector<WrappedTH1*> hSelectedFatJetPhi;
  std::vector<WrappedTH1*> hSelectedFatJetCSV;
  std::vector<WrappedTH1*> hSelectedFatJettau1;
  std::vector<WrappedTH1*> hSelectedFatJettau2;
  std::vector<WrappedTH1*> hSelectedFatJettau3;
  std::vector<WrappedTH1*> hSelectedFatJettau4;
  std::vector<WrappedTH1*> hSelectedFatJettau21;
  std::vector<WrappedTH1*> hSelectedFatJettau32;
  
  WrappedTH1 *hFatJetMatchingToTopDeltaR;
  WrappedTH1 *hFatJetMatchingToTopPtRatio;
  
  // Binnings
  int nPtBins;
  double fPtMin,fPtMax;
  int  nEtaBins;
  float fEtaMin,fEtaMax;
  int nCSVBins;
  float fCSVMin, fCSVMax;
  // int ntauBins;
  // float ftauMin, ftauMax;
};

#endif
