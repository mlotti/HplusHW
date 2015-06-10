// -*- c++ -*-
#ifndef EventSelection_BJetSelection_h
#define EventSelection_BJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
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

class BJetSelection: public BaseSelection {
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
    // Obtain number of selected jets
    int getNumberOfSelectedBJets() const { return fSelectedBJets.size(); }
    // Obtain collection of selected jets
    const std::vector<Jet>& getSelectedBJets() const { return fSelectedBJets; }
    /// Obtain the b-tagging event weight
    const double getBTaggingEventWeight() const { return fBTaggingEventWeight; }
   
    friend class BJetSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    /// B-jet tagging event weight
    double fBTaggingEventWeight;
    /// BJet collection after all selections
    std::vector<Jet> fSelectedBJets;
  };
  
  // Main class
  explicit BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~BJetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData);

private:
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData);
  // Input parameters
  const DirectionalCut<int> fNumberOfJetsCut;
  float fDisriminatorValue; // not a const because constructor sets it based on input string
  
  // Event counter for passing selection
  Count cPassedBJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedDiscriminator;
  Count cSubPassedNBjets;
  // Histograms
  std::vector<WrappedTH1*> hSelectedBJetPt;
  std::vector<WrappedTH1*> hSelectedBJetEta;
};

#endif
