// -*- c++ -*-
#ifndef EventSelection_LightJetSelection_h
#define EventSelection_LightJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BJetSelection.h"
#include "DataFormat/interface/Jet.h"
#include "EventSelection//interface/TauSelection.h"
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

class LightJetSelection: public BaseSelection {
public:
    /**
    * Class to encapsulate the access to the data members of
    * LightJetSelection.
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

    // Obtain number of selected jets
    int getNumberOfSelectedLJets() const { return fSelectedLJets.size(); }

    // Obtain collection of selected light-jets
    const std::vector<Jet>& getSelectedLJets() const { return fSelectedLJets; }

    friend class LightJetSelection;

  private:
    // Boolean for passing selection
    bool bPassedSelection;

    // Jet collection after all selections
    std::vector<Jet> fSelectedLJets;

  };
  
  // Main class
  /// Constructor with histogramming
  explicit LightJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit LightJetSelection(const ParameterSet& config);
  virtual ~LightJetSelection();

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
  /// Routine for checking if a jet is a bjet (dR-based)
  bool isBJet(const Jet& jet, const std::vector<Jet>& bjets, const float dR_match);
  
  
  // Input parameters
  const float fJetPtCut;
  const float fJetEtaCut;
  const float fBjetMatchingDeltaR;
  const DirectionalCut<int> fNumberOfJetsCut;
  
  // Event counter for passing selection
  Count cPassedLightJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedEta;
  Count cSubPassedPt;
  Count cSubPassedJetCount;

  // Histograms (1D)
  WrappedTH1 *hJetPtAll;
  WrappedTH1 *hJetEtaAll;
  WrappedTH1 *hJetPtPassed;
  WrappedTH1 *hJetEtaPassed;
  std::vector<WrappedTH1*> hSelectedJetPt;
  std::vector<WrappedTH1*> hSelectedJetEta;

};

#endif
