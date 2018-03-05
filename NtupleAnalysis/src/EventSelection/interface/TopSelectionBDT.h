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
    bool isGenuineB() const { return bIsGenuineB; }
    bool hasFreeBJet() const { return bHasFreeBJet; }
    // FakeB Measurement
    // const std::vector<Jet>& getJetsUsedAsBJets() const { return fJetsUsedAsBJets;}
    // const std::vector<Jet>& getFailedBJetsUsedAsBJets() const { return fFailedBJetsUsedAsBJets;}
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
    // GenuineB = All selected b-jets are genuine, FakeB=At least one selected b-jet is not genuine
    bool bIsGenuineB;    
    // FakeB Measurement
    std::vector<Jet> fJetsUsedAsBJets;
    std::vector<Jet> fFailedBJetsUsedAsBJets;
    // A free bjet is left after the top reconstruction (for invariant mass)
    bool bHasFreeBJet;
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
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const bool doMatching);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const bool doMatching=true);
  // analyze for FakeBMeasurement
  Data silentAnalyzeWithoutBJets(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets, bool doMatching=true);
  Data analyzeWithoutBJets(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets, bool doMatching=true);
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
  Data privateAnalyze(const Event& event, const std::vector<Jet> selectedJets, const std::vector<Jet> selectedBjets, bool doMatching);
  /// Returns true if the two jets are the same
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  /// Return true if a selected jet matches a selected bjet
  bool isBJet(const Jet& jet1, const std::vector<Jet>& bjets);
  /// Determine if event is GenuineB or FakeB  and store internally
  bool _getIsGenuineB(bool bIsMC, const std::vector<Jet>& selectedBjets);  
  /// Determine if top candidate is MC matched
  bool _getIsMatchedTop(bool isMC, Jet bjet, Jet jet1, Jet jet2, TrijetSelection mcTrueTrijets);

  virtual std::vector<genParticle> GetGenParticles(const std::vector<genParticle> genParticles, const int pdgId);
  const genParticle GetLastCopy(const std::vector<genParticle> genParticles, const genParticle &p);
  Jet getLeadingSubleadingJet(const Jet& jet0, const Jet& jet1, string selectedJet);
  bool isMatchedJet(const Jet& jet, const std::vector<Jet>& jets);
  bool isWsubjet(const Jet& jet, const std::vector<Jet>& jets1, const std::vector<Jet>& jets2);
  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, const std::vector<Jet>& MCtrue_LdgJet, const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet);
  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet,const Jet& MCtrue_LdgJet, const Jet& MCtrue_SubldgJet, const Jet& MCtrue_Bjet);
  vector <int> GetWrongAssignmentTrijetIndex(int matched_index, const std::vector<Jet>& TopCandJet1, const std::vector<Jet>& TopCandJet2, const std::vector<Jet>& TopCandBjet);
  TrijetSelection SortInMVAvalue(TrijetSelection TopCand);
  bool foundFreeBjet(const Jet& trijet1Jet1, const Jet& trijet1Jet2, const Jet& trijet1BJet, const Jet& trijet2Jet1, const Jet& trijet2Jet2, const Jet& trijet2BJet , const std::vector<Jet>& bjets);
  bool HasMother(const Event& event, const genParticle &p, const int mom_pdgId);
  int getTopFromHiggs(TrijetSelection TopCand, const Jet&  MCtrueTopFromH_LdgJet, const Jet& MCtrueTopFromH_SubldgJet, const Jet& MCtrueTopFromH_Bjet);
  int GetTrijet1(TrijetSelection TopCand, const std::vector<Jet>& bjets);
  int GetTrijet2(TrijetSelection TopCand, const std::vector<Jet>& bjets, SelectedTrijets trijet1);
  SelectedTrijets getLeadingSubleadingTrijet(SelectedTrijets trijet1, SelectedTrijets trijet2, string selectedTrijet, float MVAmax1, float MVAmax2);
  SelectedTrijets GetSelectedTopCandidate(TrijetSelection TopCand, int index);
  bool TrijetPassBDT_crossCleaned(int Index, TrijetSelection TopCand, const std::vector<Jet>& bjets);
  // Input parameters
  const DirectionalCut<double> cfg_LdgMVACut;
  const DirectionalCut<double> cfg_SubldgMVACut;
  const DirectionalCut<double> cfg_MVACut;
  const DirectionalCut<double> cfg_MassCut;
  const DirectionalCut<double> cfg_CSV_bDiscCut;
  const unsigned int cfg_NjetsMax;
  const unsigned int cfg_NBjetsMax;

  // Event counter for passing selection
  Count cPassedTopSelectionBDT;

  // Sub counters
  Count cSubAll;
  Count cSubPassedFreeBjetCut;
  Count cSubPassedBDTCut;

  // Histograms (1D)
  WrappedTH1  *hBDTresponse;
  WrappedTH1  *hTopCandMass;

  WrappedTH1  *hLdgTrijetTopMassWMassRatio;
  WrappedTH1  *hSubldgTrijetTopMassWMassRatio;

  WrappedTH1  *hTetrajetBJetPt;
  WrappedTH1  *hTetrajetBJetEta;
  WrappedTH1  *hTetrajetBJetBDisc;
  WrappedTH1  *hTetrajetPt;
  WrappedTH1  *hTetrajetMass;
  WrappedTH1  *hTetrajetEta;

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

  WrappedTH1  *hLdgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1  *hLdgTrijet_DeltaY_Trijet_TetrajetBjet;

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

  WrappedTH1  *hSubldgTrijet_DeltaR_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaEta_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaPhi_Trijet_TetrajetBjet;
  WrappedTH1  *hSubldgTrijet_DeltaY_Trijet_TetrajetBjet;

  WrappedTH1 *hTopQuarkPt;
  WrappedTH1 *hTopQuarkPt_InTopDirBDT;
  WrappedTH1 *hTopQuarkPt_InTopDir;
  WrappedTH1 *hTrijetPt_BDT;
  WrappedTH1 *hAllTopQuarkPt_InTopDir;
  WrappedTH1 *hAllTopQuarkPt_InTopDirBDT;
  WrappedTH1 *hAllTopQuarkPt_Matched;
  WrappedTH1 *hAllTopQuarkPt_MatchedBDT;

  WrappedTH1 *hLdgTrijetFake;
  WrappedTH1 *hLdgTrijetFake_BDT;
  WrappedTH1 *hTopQuarkPt_BDT;

  WrappedTH1 *hBDTmultiplicity;
  WrappedTH1 *hTrijetInTopDirNonMatched_Mass;
  WrappedTH1 *hTrijetInTopDir_Mass;
  WrappedTH1 *hTrijetTopMatched_Mass;
  WrappedTH1 *hInTopDirBDTmult;
  WrappedTH1 *hMatchedBDTmult;
  WrappedTH1 *hEventTrijetPt_BDT;
  WrappedTH1 *hEventTrijetPt_InTopDirBDT;
  WrappedTH1 *hTrijetNotInTopDirPt;
  WrappedTH1 *hTrijetNotInTopDirPt_BDT;
  WrappedTH1 *hTrijetFakePt;
  WrappedTH1 *hTrijetFakePt_BDT;
  WrappedTH1 *hDeltaRMinTopTrijet;

  WrappedTH1 *hEventTrijetPt2T_BDT;
  WrappedTH1 *hEventTrijetPt2T_MatchedBDT;

  WrappedTH1 *hEventTrijetPt2T_Matched;
  WrappedTH1 *hAllTopQuarkPt_NotInTopDir;

  WrappedTH1 *hEventTrijetPt;
  WrappedTH1 *hEventTrijetPt2T;
  WrappedTH1 *hRealSelectedTopMult;
  WrappedTH1 *hTrijetMultiplicity;
  WrappedTH1 *hTrijetBDT_Mass;
  WrappedTH1 *hTrijetMatched_BDTvalue;
  WrappedTH1 *hTrijetNonMatched_BDTvalue;
  WrappedTH1 *hNjets;
  WrappedTH1 *hDeltaMVAmax_MCtruth_SameObjFakes;
  WrappedTH1 *hAbsDeltaMVAmax_MCtruth_SameObjFakes;
  WrappedTH1 *hFakeInTopDirMult;
  WrappedTH1 *hDeltaMVAmax_MCtruth_SameObjFakesPassBDT;
  WrappedTH1 *hDeltaMVAmin_MCtruth_SameObjFakes;
  WrappedTH1 *hDeltaMVAmin_MCtruth_SameObjFakesPassBDT;
  WrappedTH1 *hMatchedTrijetMult_JetsGT9;
  WrappedTH1 *hMatchedTrijetMult_JetsInc;
  WrappedTH1 *hMVAvalue_DeltaMVAgt1;
  WrappedTH1 *hMatchedPassBDTmult_SameObjFakes;

  WrappedTH1 *hAllTrijetPassBDT_pt;
  WrappedTH1 *hAllTrijetPassBDTbPassCSV_pt;
  WrappedTH1 *hTrijetPassBDT_bDisc;
  
  WrappedTH1 *hTrijetSameObjPassBDT;
  WrappedTH1 *hTrijetSameObjPassBDT_bTagged;

  WrappedTH1 *hChHiggsBjetPt_TetrajetBjetMatched;
  WrappedTH1 *hChHiggsBjetPt_foundTetrajetBjet;
  WrappedTH1 *hHiggsBjetPt;
  WrappedTH1 *hHiggsBjetPt_LdgBjetMatched;
  WrappedTH1 *hLdgBjetPt;
  WrappedTH1 *hLdgBjetPt_isLdgFreeBjet;
  WrappedTH1 *hTrijetPtMaxMVASameFakeObj_BjetPassCSV;
  WrappedTH1 *hTrijetPtMaxMVASameFakeObj;
  WrappedTH1 *hTopFromHiggsPt_isLdgMVATrijet;
  WrappedTH1 *hTopFromHiggsPt_isSubldgMVATrijet;
  WrappedTH1 *hTopFromHiggsPt_isMVATrijet;

  WrappedTH1 *hDeltaPtOverPt_TopFromH_LdgMVATrijet;
  WrappedTH1 *hDeltaEta_TopFromH_LdgMVATrijet;
  WrappedTH1 *hDeltaPhi_TopFromH_LdgMVATrijet;
  WrappedTH1 *hDeltaR_TopFromH_LdgMVATrijet;

  WrappedTH1 *hDeltaPtOverPt_TopFromH_SubldgMVATrijet;
  WrappedTH1 *hDeltaEta_TopFromH_SubldgMVATrijet;
  WrappedTH1 *hDeltaPhi_TopFromH_SubldgMVATrijet;
  WrappedTH1 *hDeltaR_TopFromH_SubldgMVATrijet;

  WrappedTH1 *hTopFromHiggsPt;

  WrappedTH1 *hSelectedTrijetsPt_BjetPassCSVdisc_afterCuts;
  WrappedTH1 *hSelectedTrijetsPt_afterCuts;
  WrappedTH1 *hTrijetPt_PassBDT_BJetPassCSV;
  WrappedTH1 *hTrijetPt_PassBDT;

  WrappedTH1 *hChHiggsBjetPt_TetrajetBjetMatched_afterCuts;
  WrappedTH1 *hChHiggsBjetPt_foundTetrajetBjet_afterCuts;
  WrappedTH1 *hHiggsBjetPt_afterCuts;
  WrappedTH1 *hHiggsBjetPt_isTrijetSubjet_afterCuts;
  WrappedTH1 *hHiggsBjetPt_LdgBjetMatched_afterCuts;
  WrappedTH1 *hLdgBjetPt_afterCuts;
  WrappedTH1 *hLdgBjetPt_isLdgFreeBjet_afterCuts;

  WrappedTH1 *hTopFromHiggsPt_isLdgMVATrijet_afterCuts;
  WrappedTH1 *hTopFromHiggsPt_isSubldgMVATrijet_afterCuts;
  WrappedTH1 *hTopFromHiggsPt_isMVATrijet_afterCuts;
  WrappedTH1 *hTopFromHiggsPt_notMVATrijet_afterCuts;

  WrappedTH1 *hDeltaPtOverPt_TopFromH_LdgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaEta_TopFromH_LdgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaPhi_TopFromH_LdgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaR_TopFromH_LdgMVATrijet_afterCuts;

  WrappedTH1 *hDeltaPtOverPt_TopFromH_SubldgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaEta_TopFromH_SubldgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaPhi_TopFromH_SubldgMVATrijet_afterCuts;
  WrappedTH1 *hDeltaR_TopFromH_SubldgMVATrijet_afterCuts;

  WrappedTH1 *hTopFromHiggsPt_afterCuts;

  WrappedTH1 *hDeltaCSV_TopFromHBJet_LdgMVATrijetBjet_afterCuts;
  WrappedTH1 *hDeltaBDT_TopFromH_LdgMVATrijet_afterCuts;

  WrappedTH1 *hDeltaCSV_TopFromHBJet_SubldgMVATrijetBjet_afterCuts;
  WrappedTH1 *hDeltaBDT_TopFromH_SubldgMVATrijet_afterCuts;

  WrappedTH1 *hDeltaPtOverPt_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  WrappedTH1 *hDeltaEta_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  WrappedTH1 *hDeltaPhi_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  WrappedTH1 *hDeltaR_HiggsBjetPt_TetrajetBjetMatched_afterCuts;
  WrappedTH1 *hDeltaCSV_HiggsBjetPt_TetrajetBjetMatched_afterCuts;

  WrappedTH1 *hChHiggdBJetPt_passCSV;
  WrappedTH1 *hChHiggdBJetPt_passCSV_LdgTopReco;
  WrappedTH1 *hChHiggdBJetPt_passCSV_SubldgTopReco;


  WrappedTH1 *hHiggsBjet_isTrijetSubjet_TetrajetMass_afterCuts;
  WrappedTH1 *hTopFromHiggs_isLdgMVATrijet_TetrajetMass_afterCuts;
  WrappedTH1 *hTopFromHiggs_notMVATrijet_TetrajetMass_afterCuts;
  WrappedTH1 *hChHiggsBjet_TetrajetBjetMatched_TetrajetMass_afterCuts;

  WrappedTH1 *hDeltaR_BDTtrijets_TetrajetBjet;
  WrappedTH1 *hTrijetJets_DeltaRmin;
  WrappedTH1 *hTrijetJets_DeltaRmin_passBDT;

  WrappedTH1 *hTrijetMultiplicityPassBDT;

  // WrappedTH1 *hChHiggdBJetPt_passCSV_LdgFreeBjet;
  // WrappedTH1 *hChHiggdBJetPt_passCSV_SubldgFreeBjet;
  //next WrappedTH1

  // Histograms (2D)                                                                                                                             
  WrappedTH2 *hNjetsVsNTrijets_beforeBDT;
  WrappedTH2 *hNjetsVsNTrijets_afterBDT;
  WrappedTH2 *hTrijetCountForBDTcuts;
  WrappedTH2 *hDeltaMVAmaxVsTrijetPassBDTvalue;
  WrappedTH2 *hDeltaMVAminVsTrijetPassBDTvalue;
  WrappedTH2 *hFakeTrijetMassVsBDTvalue;
  WrappedTH2 *hTopFromHiggsPtVSAssocTopPt;
  WrappedTH2 *DEta_Dijet1TetrajetBjet_Vs_DEta_Dijet2TetrajetBjet;
  WrappedTH2 *DPhi_Dijet1TetrajetBjet_Vs_DPhi_Dijet2TetrajetBjet;
  WrappedTH2 *DR_Dijet1TetrajetBjet_Vs_DR_Dijet2TetrajetBjet;
  WrappedTH2 *DEta_WFromHBjetFromH_Vs_DEta_WFromAssocTopBjetFromH;
  WrappedTH2 *DPhi_WFromHBjetFromH_Vs_DPhi_WFromAssocTopBjetFromH;
  WrappedTH2 *DR_WFromHBjetFromH_Vs_DR_WFromAssocTopBjetFromH;
  WrappedTH2 *hTrijetJets_DeltaRmin_Vs_BDT;
  WrappedTH2 *hTrijetJets_DeltaRmin_Vs_Pt;
  WrappedTH2 *hTrijetJets_DeltaRmin_Vs_BDT_passBDT;
  WrappedTH2 *hTrijetJets_DeltaRmin_Vs_Pt_passBDT;

  WrappedTH2 *hDeltaR_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaEta_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaPhi_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;
  WrappedTH2 *hDeltaY_LdgTrijet_TetrajetBjet_Vs_SubldgTrijet_TetrajetBjet;

  WrappedTH2 *hTrijetMult_Vs_BDTcut;  

};

#endif
