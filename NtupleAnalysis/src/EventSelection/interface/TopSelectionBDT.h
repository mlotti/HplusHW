// -*- c++ -*-
#ifndef EventSelection_TopSelectionBDT_h
#define EventSelection_TopSelectionBDT_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "EventSelection/interface/BJetSelection.h"
#include "DataFormat/interface/Jet.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include "Tools/interface/MCTools.h"

#include <string>
#include <vector>

#include <TDirectory.h>
#include <TChain.h>
#include <TFile.h>
#include <TTree.h>
#include <TString.h>
#include <TObjString.h>
#include <TSystem.h>
#include <TROOT.h>

#include <TMVA/Factory.h>
#include <TMVA/Tools.h>
#include <TMVA/TMVAGui.h>
#include <TMVA/Reader.h>


class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

struct TrijetSelection{
  std::vector<Jet> Jet1;
  std::vector<Jet> Jet2;
  std::vector<Jet> BJet;
  std::vector <double> MVA;
  std::vector<math::XYZTLorentzVector> TrijetP4;
  std::vector<math::XYZTLorentzVector> DijetP4; 
};

struct SelectedTrijets{
  Jet Jet1;
  Jet Jet2;
  Jet BJet;
  math::XYZTLorentzVector TrijetP4;
  math::XYZTLorentzVector DijetP4;
  double MVA;
};


class TopSelectionBDT: public BaseSelection {
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
    bool hasFreeBJet() const { return bHasFreeBJet; }
    // Trijet-1
    const float getMVAmax1() const { return fMVAmax1; }
    const Jet getTrijet1Jet1() const { return fTrijet1Jet1; } 
    const Jet getTrijet1Jet2() const { return fTrijet1Jet2; } 
    const Jet getTrijet1BJet() const { return fTrijet1BJet; } 
    const math::XYZTLorentzVector getTrijet1DijetP4() const {return fTrijet1Dijet_p4; }
    const math::XYZTLorentzVector getTriJet1() const {return fTrijet1_p4; }
    // Trijet-2
    const float getMVAmax2() const { return fMVAmax2; }
    const Jet getTrijet2Jet1() const { return fTrijet2Jet1; } 
    const Jet getTrijet2Jet2() const { return fTrijet2Jet2; } 
    const Jet getTrijet2BJet() const { return fTrijet2BJet; } 
    const math::XYZTLorentzVector getTrijet2Dijet() const {return fTrijet2Dijet_p4; }
    const math::XYZTLorentzVector getTriJet2() const {return fTrijet2_p4; }
    // Leading/Subleading Tetrajet
    const math::XYZTLorentzVector getLdgTetrajet() const {return fLdgTetrajet_p4;} // uses ldg-trijet and tetrajetBjet (NOT the tetrajet with largest pt)
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
    const Jet getLdgTrijetJet1() const 
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1Jet1;
      else return fTrijet2Jet1;
    }
    const Jet getLdgTrijetJet2() const 
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1Jet2;
      else return fTrijet2Jet2;
    }
    const math::XYZTLorentzVector getLdgTrijetDijet() const
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet1Dijet_p4;
      else return fTrijet2Dijet_p4;
    }
    const double getLdgTrijetTopMassWMassRatio() const
    { 
      double R = -1.0;
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) R = fTrijet1_p4.mass()/fTrijet1Dijet_p4.mass();
      else R = fTrijet2_p4.mass()/fTrijet2Dijet_p4.mass();
      return R;
    }

    const math::XYZTLorentzVector getSubldgTrijet() const
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet2_p4;
      else return fTrijet1_p4; 
    }
    const Jet getSubldgTrijetBJet() const 
    { 
      if (fTrijet1_p4.pt() < fTrijet2_p4.pt()) return fTrijet1BJet;
      else return fTrijet2BJet;
    } 
    const math::XYZTLorentzVector getSubldgTrijetDijet() const
    { 
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fTrijet2Dijet_p4;
      else return fTrijet1Dijet_p4;
    }
    const double getSubldgTrijetTopMassWMassRatio() const
    { 
      double R = -1.0;
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) R = fTrijet2_p4.mass()/fTrijet2Dijet_p4.mass();
      else R = fTrijet1_p4.mass()/fTrijet1Dijet_p4.mass();
      return R;
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
    
    const float getLdgTrijetMVA() const
    {
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fMVAmax1;
      else return fMVAmax2;
    }

    const float getSubldgTrijetMVA() const
    {
      if (fTrijet1_p4.pt() > fTrijet2_p4.pt()) return fMVAmax2;
      else return fMVAmax1;
    }

    friend class TopSelectionBDT;

  private:
    /// Boolean for passing selection
    bool bPassedSelection;
    std::vector<Jet> fJetsUsedAsBJets;
    std::vector<Jet> fFailedBJetsUsedAsBJets;
    bool bHasFreeBJet; // ldg in pt (free) bjet  for invariant mass reco
    /// Trijet-1
    float fMVAmax1;
    Jet fTrijet1Jet1;
    Jet fTrijet1Jet2;
    Jet fTrijet1BJet;
    math::XYZTLorentzVector fTrijet1Dijet_p4;
    math::XYZTLorentzVector fTrijet1_p4;
    /// Trijet-2
    float fMVAmax2;
    Jet fTrijet2Jet1;
    Jet fTrijet2Jet2;
    Jet fTrijet2BJet;
    math::XYZTLorentzVector fTrijet2Dijet_p4;
    math::XYZTLorentzVector fTrijet2_p4;
    // Tetrajet
    Jet fTetrajetBJet;
    math::XYZTLorentzVector fLdgTetrajet_p4;
    math::XYZTLorentzVector fSubldgTetrajet_p4;
    // DijetWithMinDR
    math::XYZTLorentzVector fDijetWithMinDR_p4;
    // DijetWithMaxDR
    math::XYZTLorentzVector fDijetWithMaxDR_p4;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit TopSelectionBDT(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit TopSelectionBDT(const ParameterSet& config);
  virtual ~TopSelectionBDT();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData);

  TMVA::Reader *reader;
  
  Float_t TrijetPtDR;
  Float_t TrijetDijetPtDR;
  Float_t TrijetBjetMass;
  Float_t TrijetLdgJetBDisc;
  Float_t TrijetSubldgJetBDisc;
  Float_t TrijetBJetLdgJetMass;
  Float_t TrijetBJetSubldgJetMass;
  Float_t TrijetMass;
  Float_t TrijetDijetMass;
  Float_t TrijetBJetBDisc;
  Float_t TrijetSoftDrop_n2;
  Float_t TrijetLdgJetCvsL;    
  Float_t TrijetSubldgJetCvsL;
  Float_t TrijetLdgJetPtD;
  Float_t TrijetSubldgJetPtD;
  Float_t TrijetLdgJetAxis2;
  Float_t TrijetSubldgJetAxis2;
  Float_t TrijetLdgJetMult;
  Float_t TrijetSubldgJetMult;
  Float_t TrijetLdgJetQGLikelihood;
  Float_t TrijetSubldgJetQGLikelihood;

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets);
  /// Returns true if the two jets are the same
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  /// Return true if a selected jet matches a selected bjet
  bool isBJet(const Jet& jet1, const std::vector<Jet>& bjets);
  /// Determine if top candidate is MC matched
  bool _getIsMatchedTop(bool isMC, Jet bjet, Jet jet1, Jet jet2, TrijetSelection mcTrueTrijets);
  Jet getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet);
  bool isMatchedJet(const Jet& jet, const TrijetSelection& myTops, const unsigned int index);
  TrijetSelection SortInMVAvalue(TrijetSelection TopCand);
  bool foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets);
  SelectedTrijets getLdgOrSubldgTop(TrijetSelection myTops, string selectedTrijet);
  SelectedTrijets GetSelectedTopCandidate(TrijetSelection TopCand, int index);
  bool TopIsCrossCleaned(int Index, TrijetSelection TopCand, const std::vector<Jet>& bjets);
  // Input parameters
  const DirectionalCut<double> cfg_MVACut;
  const DirectionalCut<double> cfg_MassCut;
  const DirectionalCut<double> cfg_CSV_bDiscCut;

  // Event counter for passing selection
  Count cPassedTopSelectionBDT;

  // Sub counters
  Count cSubAll;
  Count cSubPassedBjetsCut;
  Count cSubPassedBDTCut;
  Count cSubPassedFreeBjetCut;
  //
  Count cTopsAll;
  Count cTopsPassMassCut;
  Count cTopsPassBDiscCut;
  Count cTopsPassBDTCut;
  Count cTopsPassCrossCleanCut;

  // Histograms (1D)
  WrappedTH1 *hTopMultiplicity_AllCandidates;
  WrappedTH1 *hTopBDT_AllCandidates;
  WrappedTH1 *hTopMass_AllCandidates;
  WrappedTH1 *hTopPt_AllCandidates;
  WrappedTH1 *hTopMultiplicity_SelectedCandidates;
  WrappedTH1 *hTopBDT_SelectedCandidates;
  WrappedTH1 *hTopMass_SelectedCandidates;
  WrappedTH1 *hTopPt_SelectedCandidates;
  WrappedTH1 *hTopMultiplicity_SelectedCleanedCandidates;
  WrappedTH1 *hTopBDT_SelectedCleanedCandidates;
  WrappedTH1 *hTopMass_SelectedCleanedCandidates;
  WrappedTH1 *hTopPt_SelectedCleanedCandidates;

  // Ldg in pt free b-jet
  WrappedTH1  *hTetrajetBJetPt;
  WrappedTH1  *hTetrajetBJetEta;
  WrappedTH1  *hTetrajetBJetBDisc;

  // Tetrajet
  WrappedTH1  *hTetrajetPt;
  WrappedTH1  *hTetrajetMass;
  WrappedTH1  *hTetrajetEta;

  // Leading in pt top
  WrappedTH1  *hLdgTrijetPt;
  WrappedTH1  *hLdgTrijetMass;
  WrappedTH1  *hLdgTrijetJet1Pt;
  WrappedTH1  *hLdgTrijetJet1Eta;
  WrappedTH1  *hLdgTrijetJet1BDisc;
  WrappedTH1  *hLdgTrijetJet2Pt;
  WrappedTH1  *hLdgTrijetJet2Eta;
  WrappedTH1  *hLdgTrijetJet2BDisc;
  WrappedTH1  *hLdgTrijetBJetPt;
  WrappedTH1  *hLdgTrijetBJetEta;
  WrappedTH1  *hLdgTrijetBJetBDisc;
  WrappedTH1  *hLdgTrijetDiJetPt;
  WrappedTH1  *hLdgTrijetDiJetEta;
  WrappedTH1  *hLdgTrijetDiJetMass;
  WrappedTH1  *hLdgTrijetDijetDeltaR;
  WrappedTH1  *hLdgTrijetTopMassWMassRatio;
  WrappedTH1  *hLdgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaY_Trijet_TetrajetBjet;
  
  // Sub-Leading in pt top
  WrappedTH1  *hSubldgTrijetPt;
  WrappedTH1  *hSubldgTrijetMass;
  WrappedTH1  *hSubldgTrijetJet1Pt;
  WrappedTH1  *hSubldgTrijetJet1Eta;
  WrappedTH1  *hSubldgTrijetJet1BDisc;
  WrappedTH1  *hSubldgTrijetJet2Pt;
  WrappedTH1  *hSubldgTrijetJet2Eta;
  WrappedTH1  *hSubldgTrijetJet2BDisc;
  WrappedTH1  *hSubldgTrijetBJetPt;
  WrappedTH1  *hSubldgTrijetBJetEta;
  WrappedTH1  *hSubldgTrijetBJetBDisc;
  WrappedTH1  *hSubldgTrijetDiJetPt;
  WrappedTH1  *hSubldgTrijetDiJetEta;
  WrappedTH1  *hSubldgTrijetDiJetMass;
  WrappedTH1  *hSubldgTrijetDijetDeltaR;
  WrappedTH1  *hSubldgTrijetTopMassWMassRatio;
  WrappedTH1  *hSubldgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaY_Trijet_TetrajetBjet;

  // Histograms (2D)
  WrappedTH2 *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;

};

#endif
