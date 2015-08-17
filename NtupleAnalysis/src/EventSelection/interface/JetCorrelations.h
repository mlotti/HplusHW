// -*- c++ -*-
#ifndef EventSelection_JetCorrelations_h
#define EventSelection_JetCorrelations_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/TauSelection.h"
#include "EventSelection/interface/METSelection.h"
#include "EventSelection/interface/GenJet.h"
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

class JetCorrelations: public BaseSelection {
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


  private:
    /// Boolean for passing selection
    bool bPassedSelection;

  };
  
  // Main class
  explicit JetCorrelations(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~JetCorrelations();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData);

private:
  Data privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData);
  // Input parameters
  // Event counter for passing selection
   // Sub counters
  //  Count cSubAll;
  //  const size_t nMaxJets;
  //  const size_t nConsideredJets;
  // const bool bEnableOptimizationPlots;
  //  std::vector<double> fCutValue;
  //  const std::string sPrefix;

  // Histograms   
  WrappedTH1 *hPt3Jets;
  WrappedTH1 *hM3Jets;
  WrappedTH1 *hDrTau3Jets;
  WrappedTH1 *hmaxDr3Jets;
  WrappedTH1 *hgenJetPt;
  WrappedTH1 *hgenJetEta;
  WrappedTH1 *hgenJetPhi;
  WrappedTH1 *hgenBJetEta;
  WrappedTH1 *hgenBJetPt;
  WrappedTH1 *hdrTauMaxBjet_gen;
  WrappedTH1 *hdrTauMinBjet_gen;
 

};

#endif
