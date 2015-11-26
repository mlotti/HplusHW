// -*- c++ -*-
#ifndef EventSelection_MuonSelection_h
#define EventSelection_MuonSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Muon.h"
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

class MuonSelection: public BaseSelection {
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

    const bool hasIdentifiedMuons() const { return (fSelectedMuons.size() > 0); }
    const std::vector<Muon>& getSelectedMuons() const { return fSelectedMuons; }
    const float getHighestSelectedMuonPt() const { return fHighestSelectedMuonPt; }
    const float getHighestSelectedMuonEta() const { return fHighestSelectedMuonEta; }
    const float getHighestSelectedMuonPtBeforePtCut() const { return fHighestSelectedMuonPtBeforePtCut; }
    // FIXME: Add MC information if deemed necessary
//     const bool eventContainsMuonFromCJet() const { return fHasMuonFromCjetStatus; }
//     const bool eventContainsMuonFromBJet() const { return fHasMuonFromBjetStatus; }
//     const bool eventContainsMuonFromCorBJet() const { return eventContainsMuonFromCJet() || eventContainsMuonFromBJet(); }

    friend class MuonSelection;

  private:
    /// pt and eta of highest pt muon passing the selection
    float fHighestSelectedMuonPt;
    float fHighestSelectedMuonEta;
    float fHighestSelectedMuonPtBeforePtCut;
    /// MC info about non-isolated muons
    //bool fHasMuonFromCjetStatus;
    //bool fHasMuonFromBjetStatus;
    /// Muon collection after all selections
    std::vector<Muon> fSelectedMuons;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix);
  /// Constructor without histogramming
  explicit MuonSelection(const ParameterSet& config, const std::string& postfix);
  virtual ~MuonSelection();

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

  // Input parameters
  const double fMuonPtCut;
  const double fMuonEtaCut;
  float fRelIsoCut;
  bool fVetoMode;
  
  // Event counter for passing selection
  Count cPassedMuonSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedID;
  Count cSubPassedIsolation;
  
  // Histograms
  WrappedTH1 *hMuonPtAll;
  WrappedTH1 *hMuonEtaAll;
  WrappedTH1 *hMuonPtPassed;
  WrappedTH1 *hMuonEtaPassed;
  WrappedTH1 *hPtResolution;
  WrappedTH1 *hEtaResolution;
  WrappedTH1 *hPhiResolution;
  WrappedTH1 *hIsolPtBefore;
  WrappedTH1 *hIsolEtaBefore;
  WrappedTH1 *hIsolVtxBefore;
  WrappedTH1 *hIsolPtAfter;
  WrappedTH1 *hIsolEtaAfter;
  WrappedTH1 *hIsolVtxAfter;
};

#endif
