// -*- c++ -*-
#ifndef EventSelection_ElectronSelection_h
#define EventSelection_ElectronSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Electron.h"
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

class ElectronSelection: public BaseSelection {
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

    const bool hasIdentifiedElectrons() const { return (fSelectedElectrons.size() > 0); }
    const std::vector<Electron>& getSelectedElectrons() const { return fSelectedElectrons; }
    const float getHighestSelectedElectronPt() const { return fHighestSelectedElectronPt; }
    const float getHighestSelectedElectronEta() const { return fHighestSelectedElectronEta; }
    // FIXME: Add MC information if deemed necessary
    // const bool eventContainsElectronFromCJet() const { return fHasElectronFromCjetStatus; }
    // const bool eventContainsElectronFromBJet() const { return fHasElectronFromBjetStatus; }
    // const bool eventContainsElectronFromCorBJet() const { return eventContainsElectronFromCJet() || eventContainsElectronFromBJet(); }

    friend class ElectronSelection;

  private:
    /// pt and eta of highest pt electron passing the selection
    float fHighestSelectedElectronPt;
    float fHighestSelectedElectronEta;
    /// MC info about non-isolated electrons
    //bool fHasElectronFromCjetStatus;
    //bool fHasElectronFromBjetStatus;
    /// Electron collection after all selections
    std::vector<Electron> fSelectedElectrons;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit ElectronSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix);
  /// Constructor without histogramming
  explicit ElectronSelection(const ParameterSet& config, const std::string& postfix);
  virtual ~ElectronSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config, const std::string& postfix);
  /// The actual selection
  Data privateAnalyze(const Event& iEvent);
  /// Return MVA decision based on MVA Cut
  bool getMVADecision(const Electron& ele, const std::string mvaCut);
  
  // Input parameters
  const double fElectronPtCut;
  const double fElectronEtaCut;
  float fRelIsoCut;
  float fMiniIsoCut;
  bool fVetoMode;
  bool fMiniIsol;
  bool fElectronMVA;
  const std::string fElectronMVACut;
  
  // Event counter for passing selection
  Count cPassedElectronSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedID;
  Count cSubPassedIsolation;
  
  // Histograms
  WrappedTH1 *hElectronNAll;
  WrappedTH1 *hElectronPtAll;
  WrappedTH1 *hElectronEtaAll;
  WrappedTH1 *hElectronRelIsoAll;
  WrappedTH1 *hElectronMiniIsoAll;

  WrappedTH1 *hElectronNPassed;
  WrappedTH1 *hElectronPtPassed;
  WrappedTH1 *hElectronEtaPassed;
  WrappedTH1 *hElectronRelIsoPassed;
  WrappedTH1 *hElectronMiniIsoPassed;

  WrappedTH1 *hPtResolution;
  WrappedTH1 *hEtaResolution;
  WrappedTH1 *hPhiResolution;

  WrappedTH1 *hIsolPtBefore;
  WrappedTH1 *hIsolEtaBefore;
  WrappedTH1 *hIsolVtxBefore;
  WrappedTH1 *hIsolRelIsoBefore;
  WrappedTH1 *hIsolMiniIsoBefore;

  WrappedTH1 *hIsolPtAfter;
  WrappedTH1 *hIsolEtaAfter;
  WrappedTH1 *hIsolVtxAfter;
  WrappedTH1 *hIsolRelIsoAfter;
  WrappedTH1 *hIsolMiniIsoAfter;
};

#endif
