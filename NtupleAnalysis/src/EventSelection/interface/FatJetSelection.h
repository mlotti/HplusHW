// -*- c++ -*-
#ifndef EventSelection_FatJetSelection_h
#define EventSelection_FatJetSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/AK8Jet.h"
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

class FatJetSelection: public BaseSelection {
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

    // Obtain number of selected fat jets
    int getNumberOfSelectedFatJets() const { return fSelectedFatJets.size(); }

    // Obtain collection of selected fat jets
    const std::vector<AK8Jet>& getSelectedFatJets() const { return fSelectedFatJets; }

    // Obtain collection of all fat jets
    const std::vector<AK8Jet>& getAllFatJets() const { return fAllFatJets; }

    // Check if fat jet matching to selected tau was a success
    bool fatjetMatchedToTauFound() const { return (fFatJetMatchedToTau.size() > 0); }

    // Obtain fat jet matching to selected tau
    const AK8Jet& getFatJetMatchedToTau() const;

    // Obtain HT (scalar sum of the pt of selected fat jets)
    const double HT() const { return fHT; }
    
    // Obtain JT (HT - FatJet1_Et)
    const double JT() const { return fJT; }
    
    // Obtain MHT vector (magnitude of -ve vector sum of the pt of selected fat jets)
    const math::XYZVectorD& MHT() const { return fMHT; }
    
    // Obtain MHT value (magnitude of -ve vector sum of the pt of selected fat jets)
    double MHTvalue() const { return fMHTvalue; }
    
    // Obtain minimum phi angle between a fat jet and (MHT-fat jet)
    const double minDeltaPhiFatJetMHT() const { return fMinDeltaPhiFatJetMHT; }

    // Obtain maximum phi angle between a fat jet and (MHT-fat jet)
    const double maxDeltaPhiFatJetMHT() const { return fMaxDeltaPhiFatJetMHT; }

    // Obtain minimum Delta R between a fat jet and (MHT- fat jet)
    const double minDeltaRFatJetMHT() const { return fMinDeltaRFatJetMHT; }
    
    // Obtain minimum Delta R between a fat jet and (MHT- fat jet)
    const double minDeltaRReversedFatJetMHT() const { return fMinDeltaRReversedFatJetMHT; }
    
    friend class FatJetSelection;

  private:
    // Boolean for passing selection
    bool bPassedSelection;

    // All fat jets (needed for MET)
    std::vector<AK8Jet> fAllFatJets;
    
    // Fat Jet collection after all selections
    std::vector<AK8Jet> fSelectedFatJets;

    // Fat Jet matched to tau
    std::vector<AK8Jet> fFatJetMatchedToTau;

    // HT (scalar sum of the pt of selected fat jets)
    double fHT;
    
    // JT (HT - Fat Jet1_Et)
    double fJT;

    // MHT vector (magnitude of -ve vector sum of the pt of selected fat jets)
    math::XYZVectorD fMHT;
    
    // MHT value (magnitude of -ve vector sum of the pt of selected fat jets)
    double fMHTvalue;

    // Minimum phi angle between a fat jet and (MHT-fat jet)
    double fMinDeltaPhiFatJetMHT;
    
    // Maximum phi angle between a fat jet and (MHT-fat jet)
    double fMaxDeltaPhiFatJetMHT;

    // Minimum Delta R between a fat jet and (MHT-fat jet)
    double fMinDeltaRFatJetMHT;
    
    // Maximum Delta R between a fat jet and (MHT-fat jet)
    double fMinDeltaRReversedFatJetMHT;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit FatJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit FatJetSelection(const ParameterSet& config);
  virtual ~FatJetSelection();
  
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
  
  void findFatJetMatchingToTau(std::vector<AK8Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP);
  /// Routine for calculating the MHT related values
  void calculateMHTInformation(Data& output, const math::LorentzVectorT<double>& tauP, const double tauPt);
  
  
  // Input parameters
  const std::vector<float> fFatJetPtCuts;
  const std::vector<float> fFatJetEtaCuts;
  const float fTauMatchingDeltaR;
  const DirectionalCut<int> fNumberOfFatJetsCut;
  const DirectionalCut<double> fHTCut;
  const DirectionalCut<double> fJTCut;
  const DirectionalCut<double> fMHTCut;
  
  // Event counter for passing selection
  Count cPassedFatJetSelection;
  // Sub counters
  Count cSubAll;
  Count cSubPassedFatJetID;
  Count cSubPassedFatJetPUID;
  Count cSubPassedDeltaRMatchWithTau;
  Count cSubPassedEta;
  Count cSubPassedPt;
  Count cSubPassedFatJetCount;
  Count cSubPassedHT;
  Count cSubPassedJT;
  Count cSubPassedMHT;

  // Histograms (1D)
  
  WrappedTH1 *hFatJetPtAll;
  WrappedTH1 *hFatJetEtaAll;
  WrappedTH1 *hFatJetPtPassed;
  WrappedTH1 *hFatJetEtaPassed;
  std::vector<WrappedTH1*> hSelectedFatJetPt;
  std::vector<WrappedTH1*> hSelectedFatJetEta;
  WrappedTH1 *hFatJetMatchingToTauDeltaR;
  WrappedTH1 *hFatJetMatchingToTauPtRatio;
  WrappedTH1 *hHTAll;
  WrappedTH1 *hJTAll;
  WrappedTH1 *hMHTAll;
  WrappedTH1 *hHTPassed;
  WrappedTH1 *hJTPassed;
  WrappedTH1 *hMHTPassed;
  
  
  // Binnings
  int nPtBins;
  double fPtMin,fPtMax;
  
  int  nEtaBins;
  float fEtaMin,fEtaMax;
  
  int  nHtBins;
  float fHtMin,fHtMax;
};

#endif
