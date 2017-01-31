// -*- c++ -*-
#ifndef EventSelection_TopSelection_h
#define EventSelection_TopSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BJetSelection.h"
#include "DataFormat/interface/Jet.h"
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

class TopSelection: public BaseSelection {
public:
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    // Status of passing event selection
    bool passedSelection() const { return bPassedSelection; }

    // 4-momenta of jets involved
    const math::XYZTLorentzVector Jet1P4() const { return fJet1_p4; } 
    const math::XYZTLorentzVector Jet2P4() const { return fJet2_p4; } 
    const math::XYZTLorentzVector Jet3P4() const { return fJet3_p4; } 
    const math::XYZTLorentzVector Jet4P4() const { return fJet4_p4; } 
    const math::XYZTLorentzVector BJet1P4() const { return fBJet1_p4; } 
    const math::XYZTLorentzVector BJet2P4() const { return fBJet2_p4; } 
    // 4-momenta of dijet systems
    const math::XYZTLorentzVector DiJet1P4() const {return fDiJet1_p4; }
    const math::XYZTLorentzVector DiJet2P4() const {return fDiJet2_p4; }
    // 4-momenta of trijet systems
    const math::XYZTLorentzVector TriJet1P4() const {return fTriJet1_p4; }
    const math::XYZTLorentzVector TriJet2P4() const {return fTriJet2_p4; }

    // Fit-related quantities
    const double ChiSqr() const { return fChiSqr; }

    friend class TopSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;

    // 4-momenta of jets involved
    math::XYZTLorentzVector fJet1_p4;
    math::XYZTLorentzVector fJet2_p4;
    math::XYZTLorentzVector fJet3_p4;
    math::XYZTLorentzVector fJet4_p4;
    math::XYZTLorentzVector fBJet1_p4;
    math::XYZTLorentzVector fBJet2_p4;
    // 4-momenta of dijet systems
    math::XYZTLorentzVector fDiJet1_p4;
    math::XYZTLorentzVector fDiJet2_p4;
    // 4-momenta of trijet systems
    math::XYZTLorentzVector fTriJet1_p4;
    math::XYZTLorentzVector fTriJet2_p4;

    // Chi-squared value of "fit"
    double fChiSqr;

    // 4-momenta of 3rd bjet (if exists)
    math::XYZTLorentzVector fBJet3_p4;

  };
  
  // Main class
  /// Constructor with histogramming
  explicit TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit TopSelection(const ParameterSet& config);
  virtual ~TopSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  bool matchesToBJet(const Jet& jet, const BJetSelection::Data& bjetData) const;
  bool sameJets(const Jet& jet1, const Jet& jet2);
  double CalculateChiSqrForTriJetSystems(const Jet& jet1, const Jet& jet2,
					 const Jet& jet3, const Jet& jet4,
					 const Jet& bjet1, const Jet& bjet2);
  
    
  // Input parameters
  const double cfg_MassW;
  const double cfg_diJetSigma;
  const double cfg_triJetSigma;
  const DirectionalCut<double> cfg_ChiSqrCut;

  // Event counter for passing selection
  Count cPassedTopSelection;

  // Sub counters
  Count cSubAll;
  Count cSubPassedChiSqCut;


  // Histograms (1D)
  // pt and eta of all jets involved (exept 3rd bjet)
  WrappedTH1 *h_JetPtAll_Before;
  WrappedTH1 *h_JetPtAll_After;
  WrappedTH1 *h_JetEtaAll_Before;
  WrappedTH1 *h_JetEtaAll_After;
  // mass distributions of both tops
  WrappedTH1 *h_TriJetMass_Before;
  WrappedTH1 *h_TriJetMass_After;
  // mass distribution of leading top
  WrappedTH1 *h_LdgTriJetMass_Before;
  WrappedTH1 *h_LdgTriJetMass_After;
  // mass distribution of subleading top
  WrappedTH1 *h_SubLdgTriJetMass_Before;
  WrappedTH1 *h_SubLdgTriJetMass_After;
  // mass distribution of closest top to the 3rd bjet
  WrappedTH1 *h_ClosestTo3rdBJet_TriJetMass_Before;
  WrappedTH1 *h_ClosestTo3rdBJet_TriJetMass_After;
  // mass distribution of furthest top to the 3rd bjet
  WrappedTH1 *h_FurthestTo3rdBJet_TriJetMass_Before;
  WrappedTH1 *h_FurthestTo3rdBJet_TriJetMass_After;
  // chi-square value of top fit
  WrappedTH1 *h_ChiSqr_Before;
  // mass distributions of both W
  WrappedTH1 *h_DiJetMass_Before;
  WrappedTH1 *h_DiJetMass_After;
  // dR, dPhi, dEta of jets from same W
  WrappedTH1 *h_DiJet_DR_Before;
  WrappedTH1 *h_DiJet_DR_After;
  WrappedTH1 *h_DiJet_DPhi_Before;
  WrappedTH1 *h_DiJet_DPhi_After;
  WrappedTH1 *h_DiJet_DEta_Before;
  WrappedTH1 *h_DiJet_DEta_After;
  // dR, dPhi, dEta of dijet(W) and the corresponding bjet from top
  WrappedTH1 *h_DiJetBJet_DR_Before;
  WrappedTH1 *h_DiJetBJet_DR_After;
  WrappedTH1 *h_DiJetBJet_DPhi_Before;
  WrappedTH1 *h_DiJetBJet_DPhi_After;
  WrappedTH1 *h_DiJetBJet_DEta_Before;
  WrappedTH1 *h_DiJetBJet_DEta_After;

  // Histograms (2D)
  // mass distributions of both tops Vs chi-square
  WrappedTH2 *h_TriJetMass_Vs_ChiSqr_Before;
  // pT distributions of both W Vs DR of Jets from W 
  WrappedTH2 *h_DiJetPt_Vs_DiJetDR_Before;
  WrappedTH2 *h_DiJetPt_Vs_DiJetDR_After;

};

#endif
