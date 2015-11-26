// -*- c++ -*-
#ifndef EventSelection_TopSelection_h
#define EventSelection_TopSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BJetSelection.h"
#include "DataFormat/interface/Jet.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class TopSelection: public BaseSelection {
public:
  /**
    * Class to encapsulate the access to the data members of
    * TauSelection. If you want to add a new accessor, add it here
    * and keep all the data of TauSelection private.
    */
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    // Status of passing event selection
    bool passedSelection() const { return bPassedSelection; }

    friend class TopSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    
    bool bHasElectronsOrMuons;
    bool bHasOneLeptonicTopDecay;
    bool bHasTwoleptonicTopDecays;
    
  };
  
  // Main class
  /// Constructor with histogramming
  explicit TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit TopSelection(const ParameterSet& config);
  virtual ~TopSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  bool matchesToBJet(const Jet& jet, const BJetSelection::Data& bjetData) const;
  
  // Input parameters
//   const float fJetPtCut;
//   const float fJetEtaCut;
//   const float fTauMatchingDeltaR;
//   const DirectionalCut<int> fNumberOfJetsCut;
  
  // Event counter for passing selection
  //Count cPassedTopSelection;
  // Sub counters
  Count cSubAll;
//   Count cSubPassedJetID;
//   Count cSubPassedJetPUID;
//   Count cSubPassedDeltaRMatchWithTau;
//   Count cSubPassedEta;
//   Count cSubPassedPt;
//   Count cSubPassedJetCount;
  // Histograms
//  WrappedTH1 *hJetPtAll;

};

#endif
