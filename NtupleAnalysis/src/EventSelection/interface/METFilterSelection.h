// -*- c++ -*-
#ifndef EventSelection_METFilterSelection_h
#define EventSelection_METFilterSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/MET.h"
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

class METFilterSelection: public BaseSelection {
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

    const bool passedSelection() const { return bPassedSelection; }

    friend class METFilterSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit METFilterSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit METFilterSelection(const ParameterSet& config);
  virtual ~METFilterSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& iEvent);

  // Input parameters
  
  // Event counter for passing selection
  Count cSubAll;
  std::vector<Count> cSubPassedFilter;
  Count cPassedMETFilterSelection;
  // Histograms

  bool dataOnly(std::string);
  std::vector<std::string> runOnlyData;
};

#endif
