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
    // Trijet-1
    const std::vector<Jet>& getJetsUsedAsBJetsInFit() const { return fJetsUsedAsBJetsInFit;}
    const Jet getTrijet1Jet1() const { return fTrijet1Jet1; } 
    const Jet getTrijet1Jet2() const { return fTrijet1Jet2; } 
    const Jet getTrijet1BJet() const { return fTrijet1BJet; } 
    const math::XYZTLorentzVector getTrijet1DijetP4() const {return fTrijet1Dijet_p4; }
    const math::XYZTLorentzVector getTriJet1() const {return fTrijet1_p4; }
    // Trijet-2
    const Jet getTrijet2Jet1() const { return fTrijet2Jet1; } 
    const Jet getTrijet2Jet2() const { return fTrijet2Jet2; } 
    const Jet getTrijet2BJet() const { return fTrijet2BJet; } 
    const math::XYZTLorentzVector getTrijet2Dijet() const {return fTrijet2Dijet_p4; }
    const math::XYZTLorentzVector getTriJet2() const {return fTrijet2_p4; }
    // Leading/Subleading Trijets
    const math::XYZTLorentzVector getLdgTrijet() const 
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1_p4; 
      else return fTrijet2_p4; 
    }
    const math::XYZTLorentzVector getSubldgTrijet() const
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet2_p4;
      else return fTrijet1_p4; 
    }
    // Leading/Subleading Dijets
    const math::XYZTLorentzVector getLdgDijet() const 
    { 
      if (fTrijet1Dijet_p4.pt() > fTrijet1Dijet_p4.pt()) return fTrijet1Dijet_p4; 
      else return fTrijet2Dijet_p4; 
    }
    const math::XYZTLorentzVector getSubldgDijet() const 
    {
      if (fTrijet2Dijet_p4.pt() > fTrijet1Dijet_p4.pt()) return fTrijet2Dijet_p4; 
      else return fTrijet1Dijet_p4;
    }

    // Fit-related quantities
    const double ChiSqr() const { return fChiSqr; }
    const unsigned int getNumberOfFits() const { return fNumberOfFits;}

    friend class TopSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    /// Jets used in di-top fit
    unsigned int fNumberOfFits;
    std::vector<Jet> fJetsUsedAsBJetsInFit;
    /// Trijet-1
    Jet fTrijet1Jet1;
    Jet fTrijet1Jet2;
    Jet fTrijet1BJet;
    math::XYZTLorentzVector fTrijet1Dijet_p4;
    math::XYZTLorentzVector fTrijet1_p4;
    /// Trijet-2
    Jet fTrijet2Jet1;
    Jet fTrijet2Jet2;
    Jet fTrijet2BJet;
    math::XYZTLorentzVector fTrijet2Dijet_p4;
    math::XYZTLorentzVector fTrijet2_p4;
    // Chi-squared value of di-top fit
    double fChiSqr;

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
  // silentAnalyze for FakeBMeasurement
  Data silentAnalyzeWithoutBJets(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  // analyze for FakeBMeasurement
  Data analyzeWithoutBJets(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const std::vector<Jet> jets, const std::vector<Jet> bjets);
  // The actual selection for FakeBMeasurement
  Data privateAnalyzeWithoutBJets(const Event& event, const std::vector<Jet> jets, const std::vector<Jet> bjets);
  // Returns true if the two jets are the same
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  // Return true if a selected jet matches a selected bjet
  bool isBJet(const Jet& jet1, const std::vector<Jet>& bjets);
  // Calculates the index combinations for the di-top fit
  void GetJetIndicesForChiSqrFit(const std::vector<Jet> jets,
				 const std::vector<Jet> bjets,
				 std::vector<unsigned int>& jet1,
				 std::vector<unsigned int>& jet2,
				 std::vector<unsigned int>& jet3,
				 std::vector<unsigned int>& jet4,
				 std::vector<unsigned int>& bjet1,
				 std::vector<unsigned int>& bjet2);
  // Calculates the chi-squared of the di-top fit
  double CalculateChiSqrForTrijetSystems(const Jet& jet1, const Jet& jet2,
					 const Jet& jet3, const Jet& jet4,
					 const Jet& bjet1, const Jet& bjet2);
 
  const std::vector<Jet> GetBJetsToBeUsedInFit(const BJetSelection::Data& bjetData,
					       const unsigned int maxNumberOfBJetsToUse=3);
  // Input parameters
  // Input parameters
  int nSelectedBJets;
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
  WrappedTH1 *hChiSqr_Before;
  WrappedTH1 *hChiSqr_After;
  WrappedTH1 *hNJetsUsedAsBJetsInFit_Before;
  WrappedTH1 *hNJetsUsedAsBJetsInFit_After;
  WrappedTH1 *hNumberOfFits_Before;
  WrappedTH1 *hNumberOfFits_After;

  WrappedTH1 *hTrijet1Mass_Before;
  WrappedTH1 *hTrijet2Mass_Before;
  WrappedTH1 *hTrijet1Mass_After;
  WrappedTH1 *hTrijet2Mass_After;
  WrappedTH1 *hTrijet1Pt_Before;
  WrappedTH1 *hTrijet2Pt_Before;
  WrappedTH1 *hTrijet1Pt_After;
  WrappedTH1 *hTrijet2Pt_After;

  WrappedTH1 *hTrijet1DijetMass_Before;
  WrappedTH1 *hTrijet2DijetMass_Before;
  WrappedTH1 *hTrijet1DijetMass_After;
  WrappedTH1 *hTrijet2DijetMass_After;
  WrappedTH1 *hTrijet1DijetPt_Before;
  WrappedTH1 *hTrijet2DijetPt_Before;
  WrappedTH1 *hTrijet1DijetPt_After;
  WrappedTH1 *hTrijet2DijetPt_After;
  WrappedTH1 *hTrijet1DijetDEta_Before;
  WrappedTH1 *hTrijet2DijetDEta_Before;
  WrappedTH1 *hTrijet1DijetDEta_After;
  WrappedTH1 *hTrijet2DijetDEta_After;
  WrappedTH1 *hTrijet1DijetDPhi_Before;
  WrappedTH1 *hTrijet2DijetDPhi_Before;
  WrappedTH1 *hTrijet1DijetDPhi_After;
  WrappedTH1 *hTrijet2DijetDPhi_After;
  WrappedTH1 *hTrijet1DijetDR_Before;
  WrappedTH1 *hTrijet2DijetDR_Before;
  WrappedTH1 *hTrijet1DijetDR_After;
  WrappedTH1 *hTrijet2DijetDR_After;

  WrappedTH1 *hTrijet1DijetBJetDR_Before;
  WrappedTH1 *hTrijet2DijetBJetDR_Before;
  WrappedTH1 *hTrijet1DijetBJetDR_After;
  WrappedTH1 *hTrijet2DijetBJetDR_After;
  WrappedTH1 *hTrijet1DijetBJetDPhi_Before;
  WrappedTH1 *hTrijet2DijetBJetDPhi_Before;
  WrappedTH1 *hTrijet1DijetBJetDPhi_After;
  WrappedTH1 *hTrijet2DijetBJetDPhi_After;
  WrappedTH1 *hTrijet1DijetBJetDEta_Before;
  WrappedTH1 *hTrijet2DijetBJetDEta_Before;
  WrappedTH1 *hTrijet1DijetBJetDEta_After;
  WrappedTH1 *hTrijet2DijetBJetDEta_After;

  WrappedTH1 *hLdgTrijetPt_Before;
  WrappedTH1 *hLdgTrijetPt_After;
  WrappedTH1 *hLdgTrijetMass_Before;
  WrappedTH1 *hLdgTrijetMass_After;
  WrappedTH1 *hLdgTrijetJet1Pt_Before;
  WrappedTH1 *hLdgTrijetJet1Pt_After;
  WrappedTH1 *hLdgTrijetJet1Eta_Before;
  WrappedTH1 *hLdgTrijetJet1Eta_After;
  WrappedTH1 *hLdgTrijetJet1BDisc_Before;
  WrappedTH1 *hLdgTrijetJet1BDisc_After;
  WrappedTH1 *hLdgTrijetJet2Pt_Before;
  WrappedTH1 *hLdgTrijetJet2Pt_After;
  WrappedTH1 *hLdgTrijetJet2Eta_Before;
  WrappedTH1 *hLdgTrijetJet2Eta_After;
  WrappedTH1 *hLdgTrijetJet2BDisc_Before;
  WrappedTH1 *hLdgTrijetJet2BDisc_After;
  WrappedTH1 *hLdgTrijetBJetPt_Before;
  WrappedTH1 *hLdgTrijetBJetPt_After;
  WrappedTH1 *hLdgTrijetBJetEta_Before;
  WrappedTH1 *hLdgTrijetBJetEta_After;
  WrappedTH1 *hLdgTrijetBJetBDisc_Before;
  WrappedTH1 *hLdgTrijetBJetBDisc_After;
  WrappedTH1 *hLdgTrijetDiJetPt_Before;
  WrappedTH1 *hLdgTrijetDiJetPt_After;
  WrappedTH1 *hLdgTrijetDiJetEta_Before;
  WrappedTH1 *hLdgTrijetDiJetEta_After;
  WrappedTH1 *hLdgTrijetDiJetMass_Before;
  WrappedTH1 *hLdgTrijetDiJetMass_After;

  WrappedTH1 *hSubldgTrijetPt_Before;
  WrappedTH1 *hSubldgTrijetPt_After;
  WrappedTH1 *hSubldgTrijetMass_Before;
  WrappedTH1 *hSubldgTrijetMass_After;
  WrappedTH1 *hSubldgTrijetJet1Pt_Before;
  WrappedTH1 *hSubldgTrijetJet1Pt_After;
  WrappedTH1 *hSubldgTrijetJet1Eta_Before;
  WrappedTH1 *hSubldgTrijetJet1Eta_After;
  WrappedTH1 *hSubldgTrijetJet1BDisc_Before;
  WrappedTH1 *hSubldgTrijetJet1BDisc_After;
  WrappedTH1 *hSubldgTrijetJet2Pt_Before;
  WrappedTH1 *hSubldgTrijetJet2Pt_After;
  WrappedTH1 *hSubldgTrijetJet2Eta_Before;
  WrappedTH1 *hSubldgTrijetJet2Eta_After;
  WrappedTH1 *hSubldgTrijetJet2BDisc_Before;
  WrappedTH1 *hSubldgTrijetJet2BDisc_After;
  WrappedTH1 *hSubldgTrijetBJetPt_Before;
  WrappedTH1 *hSubldgTrijetBJetPt_After;
  WrappedTH1 *hSubldgTrijetBJetEta_Before;
  WrappedTH1 *hSubldgTrijetBJetEta_After;
  WrappedTH1 *hSubldgTrijetBJetBDisc_Before;
  WrappedTH1 *hSubldgTrijetBJetBDisc_After;
  WrappedTH1 *hSubldgTrijetDiJetPt_Before;
  WrappedTH1 *hSubldgTrijetDiJetPt_After;
  WrappedTH1 *hSubldgTrijetDiJetEta_Before;
  WrappedTH1 *hSubldgTrijetDiJetEta_After;
  WrappedTH1 *hSubldgTrijetDiJetMass_Before;
  WrappedTH1 *hSubldgTrijetDiJetMass_After;

  // Histograms (2D)
  WrappedTH2 *hTrijet1MassVsChiSqr_Before;
  WrappedTH2 *hTrijet2MassVsChiSqr_Before;
  WrappedTH2 *hTrijet1MassVsChiSqr_After;
  WrappedTH2 *hTrijet2MassVsChiSqr_After;
  WrappedTH2 *hTrijet1DijetPtVsDijetDR_Before;
  WrappedTH2 *hTrijet2DijetPtVsDijetDR_Before;
  WrappedTH2 *hTrijet1DijetPtVsDijetDR_After;
  WrappedTH2 *hTrijet2DijetPtVsDijetDR_After;

};

#endif
