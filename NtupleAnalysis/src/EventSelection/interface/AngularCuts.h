// -*- c++ -*-
#ifndef EventSelection_AngularCuts_h
#define EventSelection_AngularCuts_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/TauSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/METSelection.h"
#include "Framework/interface/EventCounter.h"

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

// Base class for angular cuts; for event selections use the derived classes
// at the bottom of this header
class AngularCutsBase: public BaseSelection {
public:
  enum AngularCutsType {
    kUndefined,
    kCollinear,
    kBackToBack
  };
  
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
    /// Status of passing event selection on nth jet
    bool passedSelectionOnJet(size_t n) const;
    /// Get angle between tau and MET
    double getDeltaPhiTauMET() const { return fDeltaPhiTauMET; }
    /// Get angle between jet_n and MET
    double getDeltaPhiJetMET(size_t n) const;
    /// Get 1D cut variable on jet_n
    double get1DCutVariable(size_t n) const;
    /// Minimum value of cut variables (ignoring negative values)
    double getMinimumCutValue() const { return fMinimumCutValue; }
    
    friend class AngularCutsBase;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    /// Angle between jet_n and MET
    std::vector<bool> fPassedCutStatus;
    /// Angle between tau and MET
    double fDeltaPhiTauMET;
    /// Angle between jet_n and MET
    std::vector<double> fDeltaPhiJetMET;
    /// 1D cut variables
    std::vector<double> f1DCutVariables;
    /// Minimum value of cut variables (ignoring negative values)
    double fMinimumCutValue;
  };
    
  // Main class
  explicit AngularCutsBase(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string prefix, const AngularCutsType type, const std::string& postfix = "");
  virtual ~AngularCutsBase();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  virtual Data silentAnalyze(const Event& event, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData);
  /// analyze does fill histograms and incrementes counters
  virtual Data analyze(const Event& event, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData);

private:
  virtual Data privateAnalyze(const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData);

  bool doCollinearCuts(const double deltaPhiTauMET, const double deltaPhiJetMET, double cutValue, std::vector<double>& results);
  bool doBackToBackCuts(const double deltaPhiTauMET, const double deltaPhiJetMET, double cutValue, std::vector<double>& results);
  
  // Input parameters
  const size_t nMaxJets;
  const size_t nConsideredJets;
  const bool bEnableOptimizationPlots;
  std::vector<double> fCutValue;
  const std::string sPrefix;
  const AngularCutsType fType;
  
  // Event counter for passing selection
  Count cPassedAngularCuts;
  Count cSubAllEvents;
  std::vector<Count> cSubPassedCuts;
  
  // Histograms
  std::vector<WrappedTH2*> hOptimizationPlots;  
};

class AngularCutsCollinear : public AngularCutsBase {
public:
  using Data = AngularCutsBase::Data;
  explicit AngularCutsCollinear(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~AngularCutsCollinear();
};

class AngularCutsBackToBack: public AngularCutsBase {
public:
  using Data = AngularCutsBase::Data;
  explicit AngularCutsBackToBack(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~AngularCutsBackToBack();
};

#endif
