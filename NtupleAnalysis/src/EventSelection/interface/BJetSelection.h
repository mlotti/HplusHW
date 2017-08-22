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
    const std::vector<Jet>& getFailedBJetCandsDescendingDiscr() const { return  fFailedBJetCandsDescendingDiscr; }
    /// Obtain collection of failed bjet candidates (sorted by discriminator value)
    const std::vector<Jet>& getFailedBJetCandsAscendingDiscr() const { return  fFailedBJetCandsAscendingDiscr; }
    /// Obtain collection of failed bjet candidates (sorted in random 
    const std::vector<Jet>& getFailedBJetCandsShuffled() const { return  fFailedBJetCandsShuffled; }
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
    /// All jets failing all the b-tagging discr (trg-matched jets first, rest random)
    std::vector<Jet> fFailedBJetCands;
    /// All jets failing all the b-tagging discr cut (sorted by descending discriminator value)
    std::vector<Jet> fFailedBJetCandsDescendingDiscr; 
    /// All jets failing all the b-tagging discr cut (sorted by ascending discriminator value)
    std::vector<Jet> fFailedBJetCandsAscendingDiscr;
    /// All jets failing the b-tagging discr cut (sorted randomly)
    std::vector<Jet> fFailedBJetCandsShuffled;
  
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
  /// Obtain the discriminator value for a given algorithm and Working Point (WP)
  const double getDiscriminatorWP(const std::string sAlgorithm, const std::string sWorkingPoint);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual event selection
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData);
  /// determine if bjet object is trigger matched (deltaR based)
  bool passTrgMatching(const Jet& bjet, std::vector<math::LorentzVectorT<double>>& trgBJets) const;
  /// Sort the failed bjet candindates collections
  void SortFailedBJetsCands(Data &output, std::vector<math::LorentzVectorT<double>> myTriggerBJetMomenta);


  /// Calculate probability to pass b tagging
  double calculateBTagPassingProbability(const Event& iEvent, const JetSelection::Data& jetData);
  // Input parameters
  const bool bTriggerMatchingApply;
  const float fTriggerMatchingCone;
  const std::vector<float> fJetPtCuts;
  const std::vector<float> fJetEtaCuts;
  const DirectionalCut<int> fNumberOfJetsCut;
  float fDisriminatorValue; // not a const because constructor sets it based on input string

  // Event counter for passing selection
  Count cPassedBJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedEta;
  Count cSubPassedPt;
  Count cSubPassedDiscriminator;
  Count cSubPassedTrgMatching;
  Count cSubPassedNBjets;
  // Scalefactor calculator
  BTagSFCalculator fBTagSFCalculator;
  // Histograms
  WrappedTH1* hTriggerMatchDeltaR;
  WrappedTH1* hTriggerMatches;
  WrappedTH1* hTriggerBJets;
  std::vector<WrappedTH1*> hTriggerMatchedBJetPt;
  std::vector<WrappedTH1*> hTriggerMatchedBJetEta;
  std::vector<WrappedTH1*> hSelectedBJetPt;
  std::vector<WrappedTH1*> hSelectedBJetEta;
  std::vector<WrappedTH1*> hSelectedBJetBDisc;
};

#endif
