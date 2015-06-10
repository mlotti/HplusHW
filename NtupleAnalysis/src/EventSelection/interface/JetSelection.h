// -*- c++ -*-
#ifndef EventSelection_JetSelection_h
#define EventSelection_JetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/Tau.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"
#include <../external/boost_1_57_0/boost/concept_check.hpp>

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class JetSelection: public BaseSelection {
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
    int getNumberOfSelectedJets() const { return fSelectedJets.size(); }
    // Obtain collection of selected jets
    const std::vector<Jet>& getSelectedJets() const { return fSelectedJets; }
    // Obtain collection of all jets
    const std::vector<Jet>& getAllJets() const { return fAllJets; }
    // Check if jet matching to selected tau was a success
    bool jetMatchedToTauFound() const { return (fJetMatchedToTau.size() > 0); }
    // Obtain jet matching to selected tau
    const Jet& getJetMatchedToTau() const;
    // Obtain HT
    const double HT() const { return fHT; }

    friend class JetSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    /// All jets (needed for MET)
    std::vector<Jet> fAllJets;
    /// Jet collection after all selections
    std::vector<Jet> fSelectedJets;
    /// Jet matched to tau
    std::vector<Jet> fJetMatchedToTau;
    /// HT (scalar sum of jets)
    double fHT;
  };
  
  // Main class
  explicit JetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~JetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const Tau& selectedTau);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const Tau& selectedTau);

private:
  Data privateAnalyze(const Event& event, const Tau& selectedTau);
  void findJetMatchingToTau(std::vector<Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP);
  
  
  // Input parameters
  const float fJetPtCut;
  const float fJetEtaCut;
  const float fTauMatchingDeltaR;
  const DirectionalCut<int> fNumberOfJetsCut;
  
  // Event counter for passing selection
  Count cPassedJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedJetID;
  Count cSubPassedJetPUID;
  Count cSubPassedDeltaRMatchWithTau;
  Count cSubPassedEta;
  Count cSubPassedPt;
  Count cSubPassedJetCount;
  // Histograms
  WrappedTH1 *hJetPtAll;
  WrappedTH1 *hJetEtaAll;
  WrappedTH1 *hJetPtPassed;
  WrappedTH1 *hJetEtaPassed;
  std::vector<WrappedTH1*> hSelectedJetPt;
  std::vector<WrappedTH1*> hSelectedJetEta;
  WrappedTH1 *hJetMatchingToTauDeltaR;
  WrappedTH1 *hJetMatchingToTauPtRatio;
};

#endif
