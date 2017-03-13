// -*- c++ -*-
#ifndef EventSelection_BJetSelection_h
#define EventSelection_BJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BTagSFCalculator.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include <string>
#include <vector>
#include <algorithm>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

// struct DiscComparator{
//   bool operator() (const Jet a, const Jet b) const
//   {
//     return ( a.bjetDiscriminator() > b.bjetDiscriminator());
//   }
// };

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
 
    /// Status of passing event selection
    bool passedSelection() const { return bPassedSelection; }
    /// Obtain number of selected jets
    int getNumberOfSelectedBJets() const { return fSelectedBJets.size(); }
    /// Obtain collection of selected jets
    const std::vector<Jet>& getSelectedBJets() const { return fSelectedBJets; }
    /// Obtain number of failed bjet candidates
    int getNumberOfFailedBJetCands() const { return fFailedBJetCands.size(); }
    /// Obtain collection of failed bjet candidates
    const std::vector<Jet>& getFailedBJetCands() const { return fFailedBJetCands; }
    /// Obtain collection of failed bjet candidates (sorted by discriminator value)
    const std::vector<Jet>& getFailedBJetCandsSortedByDiscriminator() const { return fFailedBJetCandsSorted; }
    /// Obtain the b-tagging event weight
    const double getBTaggingScaleFactorEventWeight() const { return fBTaggingScaleFactorEventWeight; }
    /// Obtain the probability for passing b tagging without applying the selection
    const double getBTaggingPassProbability() const { return fBTaggingPassProbability; }

    friend class BJetSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    /// b tagging scale factor event weight
    double fBTaggingScaleFactorEventWeight;
    /// Probability for passing b tagging 
    double fBTaggingPassProbability;
    /// BJet collection after all selections
    std::vector<Jet> fSelectedBJets;
    /// All jets failing all the b-tagging criteria
    std::vector<Jet> fFailedBJetCands;
    /// All jets failing all the b-tagging criteria (sorted by discriminator value)
    std::vector<Jet> fFailedBJetCandsSorted;

  };
  
  // Main class
  /// Constructor with histogramming
  explicit BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit BJetSelection(const ParameterSet& config);
  virtual ~BJetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual event selection
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData);
  /// Calculate probability to pass b tagging
  double calculateBTagPassingProbability(const Event& iEvent, const JetSelection::Data& jetData);
  // Input parameters
  const float fJetPtCut;
  const float fJetEtaCut;
  const DirectionalCut<int> fNumberOfJetsCut;
  float fDisriminatorValue; // not a const because constructor sets it based on input string
  
  // Event counter for passing selection
  Count cPassedBJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedDiscriminator;
  Count cSubPassedNBjets;
  // Scalefactor calculator
  BTagSFCalculator fBTagSFCalculator;
  // Histograms
  std::vector<WrappedTH1*> hSelectedBJetPt;
  std::vector<WrappedTH1*> hSelectedBJetEta;
};

#endif
