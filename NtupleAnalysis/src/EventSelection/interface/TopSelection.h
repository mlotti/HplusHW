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
    /// Status of GenuineB event (if false event is FakeB)
    bool isGenuineB() const { return bIsGenuineB; }
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
    // Leading/Subleading Tetrajet
    const math::XYZTLorentzVector getLdgTetrajet() const {return fLdgTetrajet_p4;}
    const math::XYZTLorentzVector getSubldgTetrajet() const {return fSubldgTetrajet_p4;}
    const Jet getTetrajetBJet() const {return fTetrajetBJet;}
    // Leading/Subleading Trijet
    const math::XYZTLorentzVector getLdgTrijet() const 
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1_p4; 
      else return fTrijet2_p4; 
    }
    const Jet getLdgTrijetBJet() const 
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1BJet;
      else return fTrijet2BJet;
    }
    const Jet getSubldgTrijetBJet() const 
    { 
      if (fTrijet1_p4.pt() < fTrijet2_p4.pt()) return fTrijet1BJet;
      else return fTrijet2BJet;
    }
    const math::XYZTLorentzVector getSubldgTrijet() const
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet2_p4;
      else return fTrijet1_p4; 
    }
    // Leading/Subleading Dijets
    const math::XYZTLorentzVector getLdgDijet() const 
    { 
      if (fTrijet1Dijet_p4.pt() > fTrijet2Dijet_p4.pt()) return fTrijet1Dijet_p4; 
      else return fTrijet2Dijet_p4; 
    }
    const math::XYZTLorentzVector getSubldgDijet() const 
    {
      if (fTrijet1Dijet_p4.pt() > fTrijet2Dijet_p4.pt()) return fTrijet2Dijet_p4; 
      else return fTrijet1Dijet_p4;
    }

    // Fit-related quantities
    const double ChiSqr() const { return fChiSqr; }
    const unsigned int getNumberOfFits() const { return fNumberOfFits;}

    friend class TopSelection;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    // GenuineB = All selected b-jets are genuine, FakeB=At least one selected b-jet is not genuine
    bool bIsGenuineB;
    /// Fit properties
    double fChiSqr;
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
    // Tetrajet
    Jet fTetrajetBJet;
    math::XYZTLorentzVector fTetrajet1_p4;
    math::XYZTLorentzVector fTetrajet2_p4;
    math::XYZTLorentzVector fLdgTetrajet_p4;
    math::XYZTLorentzVector fSubldgTetrajet_p4;
    // DijetWithMinDR
    math::XYZTLorentzVector fDijetWithMinDR_p4;
    // DijetWithMaxDR
    math::XYZTLorentzVector fDijetWithMaxDR_p4;
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
  Data silentAnalyzeWithoutBJets(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const unsigned int maxNumberOfBJetsInTopFit=3);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  // analyze for FakeBMeasurement
  Data analyzeWithoutBJets(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const unsigned int maxNumberOfBJetsInTopFit=3);

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
  
  const int GetTetrajetBjetIndex(const std::vector<Jet> bjets, 
				 const Jet& bjet1, 
				 const Jet& bjet2,
				 const Jet& jet1, 
				 const Jet& jet2,
				 const Jet& jet3, 
				 const Jet& jet4);

  /// Determine if event is GenuineB or FakeB  and store internally
  bool _getIsGenuineB(bool bIsMC, const std::vector<Jet>& selectedBjets);  

 
  const std::vector<Jet> GetBjetsToBeUsedInFit(const BJetSelection::Data& bjetData,
					       const unsigned int maxNumberOfBJets);
  // Input parameters
  // Input parameters
  int nSelectedBJets;
  const double cfg_MassW;
  const double cfg_diJetSigma;
  const double cfg_triJetSigma;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dR_min;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dR_slopeCoeff;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dR_yIntercept;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dPhi_min;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dPhi_slopeCoeff;
  const double cfg_dijetWithMaxDR_tetrajetBjet_dPhi_yIntercept;
  const DirectionalCut<double> cfg_ChiSqrCut;

  // Event counter for passing selection
  Count cPassedTopSelection;

  // Sub counters
  Count cSubAll;
  Count cSubPassedChiSqCut;

  // Histograms (1D)
  WrappedTH1 *hChiSqr;
  WrappedTH1 *hNJetsUsedAsBJetsInFit;
  WrappedTH1 *hNumberOfFits;

  WrappedTH1 *hTetrajetBJetPt;
  WrappedTH1 *hTetrajetBJetEta;
  WrappedTH1 *hTetrajetBJetBDisc;
  WrappedTH1 *hTetrajet1Pt;
  WrappedTH1 *hTetrajet1Mass;
  WrappedTH1 *hTetrajet1Eta;
  WrappedTH1 *hTetrajet2Pt;
  WrappedTH1 *hTetrajet2Mass;
  WrappedTH1 *hTetrajet2Eta;
  WrappedTH1 *hLdgTetrajetPt;
  WrappedTH1 *hLdgTetrajetMass;
  WrappedTH1 *hLdgTetrajetEta;
  WrappedTH1 *hSubldgTetrajetPt;
  WrappedTH1 *hSubldgTetrajetMass;
  WrappedTH1 *hSubldgTetrajetEta;
  
  WrappedTH1 *hTrijet1Mass;
  WrappedTH1 *hTrijet2Mass;
  WrappedTH1 *hTrijet1Pt;
  WrappedTH1 *hTrijet2Pt;

  WrappedTH1 *hTrijet1DijetMass;
  WrappedTH1 *hTrijet2DijetMass;
  WrappedTH1 *hTrijet1DijetPt;
  WrappedTH1 *hTrijet2DijetPt;
  WrappedTH1 *hTrijet1DijetDEta;
  WrappedTH1 *hTrijet2DijetDEta;
  WrappedTH1 *hTrijet1DijetDPhi;
  WrappedTH1 *hTrijet2DijetDPhi;
  WrappedTH1 *hTrijet1DijetDR;
  WrappedTH1 *hTrijet2DijetDR;

  WrappedTH1 *hTrijet1DijetBJetDR;
  WrappedTH1 *hTrijet2DijetBJetDR;
  WrappedTH1 *hTrijet1DijetBJetDPhi;
  WrappedTH1 *hTrijet2DijetBJetDPhi;
  WrappedTH1 *hTrijet1DijetBJetDEta;
  WrappedTH1 *hTrijet2DijetBJetDEta;

  WrappedTH1 *hLdgTrijetPt;
  WrappedTH1 *hLdgTrijetMass;
  WrappedTH1 *hLdgTrijetJet1Pt;
  WrappedTH1 *hLdgTrijetJet1Eta;
  WrappedTH1 *hLdgTrijetJet1BDisc;
  WrappedTH1 *hLdgTrijetJet2Pt;
  WrappedTH1 *hLdgTrijetJet2Eta;
  WrappedTH1 *hLdgTrijetJet2BDisc;
  WrappedTH1 *hLdgTrijetBJetPt;
  WrappedTH1 *hLdgTrijetBJetEta;
  WrappedTH1 *hLdgTrijetBJetBDisc;
  WrappedTH1 *hLdgTrijetDiJetPt;
  WrappedTH1 *hLdgTrijetDiJetEta;
  WrappedTH1 *hLdgTrijetDiJetMass;

  WrappedTH1 *hSubldgTrijetPt;
  WrappedTH1 *hSubldgTrijetMass;
  WrappedTH1 *hSubldgTrijetJet1Pt;
  WrappedTH1 *hSubldgTrijetJet1Eta;
  WrappedTH1 *hSubldgTrijetJet1BDisc;
  WrappedTH1 *hSubldgTrijetJet2Pt;
  WrappedTH1 *hSubldgTrijetJet2Eta;
  WrappedTH1 *hSubldgTrijetJet2BDisc;
  WrappedTH1 *hSubldgTrijetBJetPt;
  WrappedTH1 *hSubldgTrijetBJetEta;
  WrappedTH1 *hSubldgTrijetBJetBDisc;
  WrappedTH1 *hSubldgTrijetDiJetPt;
  WrappedTH1 *hSubldgTrijetDiJetEta;
  WrappedTH1 *hSubldgTrijetDiJetMass;

  // Histograms (2D)
  WrappedTH2 *hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DPhiVsDPhi;
  WrappedTH2 *hTetrajetBJetDijetWithMaxDR_TetrajetBJetDijetWithMinDR_DRVsDR;
  WrappedTH2 *hTrijet1MassVsChiSqr;
  WrappedTH2 *hTrijet2MassVsChiSqr;
  WrappedTH2 *hTrijet1DijetPtVsDijetDR;
  WrappedTH2 *hTrijet2DijetPtVsDijetDR;

};

#endif
