// -*- c++ -*-
#ifndef EventSelection_QuarkGluonLikelihoodRatio_h
#define EventSelection_QuarkGluonLikelihoodRatio_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BJetSelection.h"
#include "EventSelection/interface/BTagSFCalculator.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include <string>
#include <vector>
#include <algorithm>
#include "boost/optional.hpp"

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

// ------------------------------------------------------------------------------
class QGLInputItem {
public:
  
  QGLInputItem(float minQGL, float maxQGL, float minPt, float maxPt, float prob, float probErr);
  ~QGLInputItem();
  
  /// Returns the minimum QGL value
  const float getMinQGL() const {return fminQGL; };
  /// Returns the maximum QGL value
  const float getMaxQGL() const {return fmaxQGL; };
  /// Returns whether the QGL is within the range
  const bool isWithinQGLRange(float qgl) const {return (qgl >= fminQGL && qgl < fmaxQGL); }; 
  /// Returns whether the pT is within the range
  const bool isWithinPtRange(float pt) const {return (pt >= fminPt && pt < fmaxPt); };
  
  /// Returns the probability
  const float getProb() const {return fProb; };
  /// Returns the probability error
  const float getProbError() const {return fProbErr; }
  
private:
  float fminQGL;
  float fmaxQGL;
  float fminPt;
  float fmaxPt;
  float fProb;
  float fProbErr;
};
// ------------------------------------------------------------------------------


// ------------------------------------------------------------------------------
class QGLInputStash {
public:
  QGLInputStash();
  ~QGLInputStash();
  
  /// Add input 
  void addInput(std::string jetType, float minQGL, float maxQGL, float minPt, float maxPt, float Prob, float ProbErr);
  /// Returns value
  const float getInputValue(std::string jetType, float qgl, float pt);
  
private:
  
  std::vector<QGLInputItem*>& getCollection(std::string JetType);
  
  std::vector<QGLInputItem*> fLight;
  std::vector<QGLInputItem*> fGluon;
};
// -------------------------------------------------------------------------------


class QuarkGluonLikelihoodRatio: public BaseSelection {
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
    /// Obtain number of light and gluon jets
    int getNumberOfJetsForQGLR() const { return fJetsForQGLR.size(); }
    /// Obtain number of light jets
    int getNumberOfLightJets() const { return fLightJets.size(); }
    /// Obtain number of gluon jets
    int getNumberOfGluonJets() const { return fGluonJets.size(); }
    /// Obtain collection of light and gluon jets
    const std::vector<Jet>& getLightAndGluonJetCands() const { return fJetsForQGLR; }
    /// Obtain collection of light jet candidates
    const std::vector<Jet>& getLightJetCands() const { return fLightJets; }
    /// Obtain collection of gluon jet candidates
    const std::vector<Jet>& getGluonJetCands() const { return fGluonJets; }
    /// Obtain QGLR
    double getQGLR() const { return fQGLR; }
    
    friend class QuarkGluonLikelihoodRatio;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    // Jets to consider in QGLR calculation
    std::vector<Jet> fJetsForQGLR;
    // Light Jets
    std::vector<Jet> fLightJets;
    // Gluon Jets
    std::vector<Jet> fGluonJets;
    // Quark-Gluon Likelihood Ratio
    double fQGLR;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit QuarkGluonLikelihoodRatio(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit QuarkGluonLikelihoodRatio(const ParameterSet& config);
  virtual ~QuarkGluonLikelihoodRatio();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
 
private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual event selection
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// Get the factorial of a number
  double factorial(const int N);
  /// Calculate QGLR
  double calculateQGLR(const Event& iEvent, const std::vector<Jet> Jets);
  /// Calculate L(Nq, Ng)
  double calculateL(const Event& iEvent, const std::vector<Jet> Jets, const int Nq, const int Ng);
  /// Get permutations
  std::vector<std::vector<int> > getPermutations(std::vector<int> v, const int Nq, const int Ng);
  /// Check if permutation already exists
  bool PermutationFound(std::vector<std::vector<int> > p, std::vector<int> v, const int Nq, const int Ng);
  /// Get Jet Indices
  std::vector<int> getJetIndices(const std::vector<Jet> Jets);
  /// Method for handling the QGL input
  void handleQGLInput(const ParameterSet& config, std::string jetType);
  /// Returns true if the two jets are the same
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  /// Return true if a selected jet matches a selected bjet
  bool isBJet(const Jet& jet1, const std::vector<Jet>& bjets);
  
  // Input parameters
  const DirectionalCut<double> fQGLRCut;
  const DirectionalCut<int> fnumberOfJetsCut;

  // Event counter for passing selection
  Count cPassedQuarkGluonLikelihoodRatio;
  // Sub counters
  Count cSubAll;
  
  QGLInputStash fProb;
  
  // Histograms
  WrappedTH1* hAllJetsQGL;
  WrappedTH1* hAllJetsNonBJetsQGL;
  WrappedTH1* hGluonJetQGL;
  WrappedTH1* hLightJetQGL;
  
  WrappedTH1* hQGLR;
  WrappedTH2* hQGLR_vs_HT;
  WrappedTH2* hQGLR_vs_NJets;

};

#endif
