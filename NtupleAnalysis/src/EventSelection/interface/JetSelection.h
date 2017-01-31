// -*- c++ -*-
#ifndef EventSelection_JetSelection_h
#define EventSelection_JetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Jet.h"
#include "EventSelection//interface/TauSelection.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"
#include <boost/concept_check.hpp>

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

    // Obtain HT (scalar sum of the pt of selected jets)
    const double HT() const { return fHT; }

    // Obtain JT (HT - Jet1_Et)
    const double JT() const { return fJT; }
    
    // Obtain MHT vector (magnitude of -ve vector sum of the pt of selected jets)
    const math::XYZVectorD& MHT() const { return fMHT; }

    // Obtain MHT value (magnitude of -ve vector sum of the pt of selected jets)
    double MHTvalue() const { return fMHTvalue; }

    // Obtain minimum phi angle between a jet and (MHT-jet)
    const double minDeltaPhiJetMHT() const { return fMinDeltaPhiJetMHT; }

    // Obtain maximum phi angle between a jet and (MHT-jet)
    const double maxDeltaPhiJetMHT() const { return fMaxDeltaPhiJetMHT; }

    // Obtain minimum Delta R between a jet and (MHT-jet)
    const double minDeltaRJetMHT() const { return fMinDeltaRJetMHT; }

    // Obtain minimum Delta R between a jet and (MHT-jet)
    const double minDeltaRReversedJetMHT() const { return fMinDeltaRReversedJetMHT; }
    
    friend class JetSelection;

  private:
    // Boolean for passing selection
    bool bPassedSelection;

    // All jets (needed for MET)
    std::vector<Jet> fAllJets;

    // Jet collection after all selections
    std::vector<Jet> fSelectedJets;

    // Jet matched to tau
    std::vector<Jet> fJetMatchedToTau;

    // HT (scalar sum of the pt of selected jets)
    double fHT;

    // JT (HT - Jet1_Et)
    double fJT;

    // MHT vector (magnitude of -ve vector sum of the pt of selected jets)
    math::XYZVectorD fMHT;

    // MHT value (magnitude of -ve vector sum of the pt of selected jets)
    double fMHTvalue;

    // Minimum phi angle between a jet and (MHT-jet)
    double fMinDeltaPhiJetMHT;

    // Maximum phi angle between a jet and (MHT-jet)
    double fMaxDeltaPhiJetMHT;

    // Minimum Delta R between a jet and (MHT-jet)
    double fMinDeltaRJetMHT;
    
    // Maximum Delta R between a jet and (MHT-jet)
    double fMinDeltaRReversedJetMHT;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit JetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit JetSelection(const ParameterSet& config);
  virtual ~JetSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const Tau& tau);
  Data silentAnalyzeWithoutTau(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const Tau& tau);
  Data analyzeWithoutTau(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt);
  
  void findJetMatchingToTau(std::vector<Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP);
  /// Routine for calculating the MHT related values
  void calculateMHTInformation(Data& output, const math::LorentzVectorT<double>& tauP, const double tauPt);
  
  
  // Input parameters
  const float fJetPtCut;
  const float fJetEtaCut;
  const float fTauMatchingDeltaR;
  const DirectionalCut<int> fNumberOfJetsCut;
  const DirectionalCut<double> fHTCut;
  const DirectionalCut<double> fJTCut;
  const DirectionalCut<double> fMHTCut;
  
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
  Count cSubPassedHT;
  Count cSubPassedJT;
  Count cSubPassedMHT;

  // Histograms (1D)
  WrappedTH1 *hJetPtAll;
  WrappedTH1 *hJetEtaAll;
  WrappedTH1 *hJetPtPassed;
  WrappedTH1 *hJetEtaPassed;
  std::vector<WrappedTH1*> hSelectedJetPt;
  std::vector<WrappedTH1*> hSelectedJetEta;
  WrappedTH1 *hJetMatchingToTauDeltaR;
  WrappedTH1 *hJetMatchingToTauPtRatio;
  WrappedTH1 *hHTAll;
  WrappedTH1 *hJTAll;
  WrappedTH1 *hMHTAll;
  WrappedTH1 *hHTPassed;
  WrappedTH1 *hJTPassed;
  WrappedTH1 *hMHTPassed;


};

#endif
