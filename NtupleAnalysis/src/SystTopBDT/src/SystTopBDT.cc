// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/Event.h"
#include "TDirectory.h"

class SystTopBDT: public BaseSelector {
public:
  explicit SystTopBDT(const ParameterSet& config, const TH1* skimCounters);
  virtual ~SystTopBDT() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

  double DeltaEta(double eta1, double eta2);
  double DeltaPhi(double phi1, double phi2);

  double DeltaR(double eta1, double eta2,
                double phi1, double phi2);

  bool areSameJets(const Jet& jet1, const Jet& jet2);
  void DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData,  Muon mu, const METSelection::Data& METData, 
			  const TopSelectionBDT::Data& topData, Jet BJet_LeptonicBr, bool searchForLeptonicTop);
  void DoInvertedAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, Muon mu, const METSelection::Data& METData, 
			  const TopSelectionBDT::Data& topData, Jet BJet_LeptonicBr, bool searchForLeptonicTop);
  int  getLeadingTopIndex(const TopSelectionBDT::Data& topData, string topType, Muon mu, Jet BJet_LeptonicBr, bool searchForLeptonicTop);
  //int  TopCandMultiplicity( const TopSelectionBDT::Data& topData, string topType, Jet BJet_LeptonicBr, Muon mu, bool searchForLeptonicTop, bool askTopFarFromMu);
  vector<genParticle> GetGenParticles(const vector<genParticle> genParticles, const int pdgId);
  const genParticle GetLastCopy(const vector<genParticle> genParticles, const genParticle &p);
  bool isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, 
		    const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet);
  bool IsGenuineTop(const TopSelectionBDT::Data& topData, string topType, Muon mu, Jet BJet_LeptonicBr, bool searchForLeptonicTop,
		    const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet);
  vector <int> GetTopsIndex( const TopSelectionBDT::Data& topData, string topType, Jet BJet_LeptonicBr, Muon mu, bool searchForLeptonicTop, bool askTopFarFromMu);

private:
  // Input parameters
  const DirectionalCut<double> cfg_PrelimTopMVACut;
  const std::string cfg_LdgTopDefinition;
  const DirectionalCut<double> cfg_MiniIsoCut;
  const DirectionalCut<double> cfg_MiniIsoInvCut;
  const DirectionalCut<double> cfg_METCut;
  
  const float cfg_MuonPtCut;
  const float cfg_MuonEtaCut;
  
  
  // Common plots
  CommonPlots fCommonPlots;

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  QuarkGluonLikelihoodRatio fQGLRSelection;
  TopSelectionBDT fTopSelection;
  FatJetSelection fFatJetSelection;
  Count cSelected;
    
  //====================================================================
  //Signal Region
  //====================================================================
  // Non-common histograms
  WrappedTH1Triplet* h_AfterStandardSelections_MET_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_HT_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_NJets_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Eta_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Phi_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_NBJets_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Eta_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Phi_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_CSV_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Eta_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Phi_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_BJetMinDR_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_LeadingTrijetDR_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Eta_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Phi_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_CSV_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_WMass_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BDT_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_DeltaPhi_MuMET_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Pt_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Eta_SR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Phi_SR;
  //
  WrappedTH1Triplet* h_AfterAllSelections_MET_SR;
  WrappedTH1Triplet* h_AfterAllSelections_HT_SR;
  WrappedTH1Triplet* h_AfterAllSelections_NJets_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Eta_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Phi_SR;
  WrappedTH1Triplet* h_AfterAllSelections_NBJets_SR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Eta_SR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Phi_SR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_CSV_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Eta_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Phi_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_BJetMinDR_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_LeadingTrijetDR_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Eta_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Phi_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_CSV_SR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BDT_SR;
  WrappedTH1Triplet* h_AfterAllSelections_WMass_SR;
  WrappedTH1Triplet* h_AfterAllSelections_DeltaPhi_MuMET_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Pt_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Eta_SR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Phi_SR;
    
  WrappedTH1 *hCEvts_TopPassBDT_SR;
  WrappedTH1 *hCEvts_PassSelections_SR;


  //====================================================================
  //Control Region 1
  //====================================================================
  // Non-common histograms
  WrappedTH1Triplet* h_AfterStandardSelections_MET_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_HT_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_NJets_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Eta_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Phi_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_NBJets_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Eta_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Phi_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_CSV_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Eta_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Phi_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_BJetMinDR_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_LeadingTrijetDR_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Eta_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Phi_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_WMass_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BDT_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_DeltaPhi_MuMET_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Pt_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Eta_CR1;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Phi_CR1;
  //
  WrappedTH1Triplet* h_AfterAllSelections_MET_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_HT_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_NJets_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Eta_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Phi_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_NBJets_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Eta_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Phi_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_CSV_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Eta_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Phi_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_BJetMinDR_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_LeadingTrijetDR_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Eta_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Phi_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BDT_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_WMass_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_DeltaPhi_MuMET_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Pt_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Eta_CR1;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Phi_CR1;
  
    
  //====================================================================
  //Control Region 2
  //====================================================================
  // Non-common histograms
  WrappedTH1Triplet* h_AfterStandardSelections_MET_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_HT_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_NJets_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Eta_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Phi_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_NBJets_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Eta_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Phi_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_CSV_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Eta_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Phi_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_BJetMinDR_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_LeadingTrijetDR_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Eta_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Phi_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_WMass_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BDT_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_DeltaPhi_MuMET_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Pt_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Eta_CR2;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Phi_CR2;

  //
  WrappedTH1Triplet* h_AfterAllSelections_MET_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_HT_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_NJets_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Eta_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Phi_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_NBJets_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Eta_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Phi_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_CSV_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Eta_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Phi_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_BJetMinDR_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_LeadingTrijetDR_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Eta_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Phi_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BDT_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_WMass_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_DeltaPhi_MuMET_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Pt_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Eta_CR2;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Phi_CR2;
      
  //====================================================================
  //Verification Region
  //====================================================================
  // Non-common histograms
  WrappedTH1Triplet* h_AfterStandardSelections_MET_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_HT_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_NJets_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Eta_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Jets_Phi_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_NBJets_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Eta_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_Phi_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_BJets_CSV_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Eta_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_Phi_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_BJetMinDR_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Muon_LeadingTrijetDR_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Eta_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_Phi_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BJet_CSV_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_WMass_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_LeadingTrijet_BDT_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_DeltaPhi_MuMET_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Pt_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Eta_VR;
  WrappedTH1Triplet* h_AfterStandardSelections_Trijets_Phi_VR;

  //
  WrappedTH1Triplet* h_AfterAllSelections_MET_VR;
  WrappedTH1Triplet* h_AfterAllSelections_HT_VR;
  WrappedTH1Triplet* h_AfterAllSelections_NJets_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Eta_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Jets_Phi_VR;
  WrappedTH1Triplet* h_AfterAllSelections_NBJets_VR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Eta_VR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_Phi_VR;
  WrappedTH1Triplet* h_AfterAllSelections_BJets_CSV_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Eta_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_Phi_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_BJetMinDR_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Muon_LeadingTrijetDR_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Eta_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_Phi_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BJet_CSV_VR;
  WrappedTH1Triplet* h_AfterAllSelections_LeadingTrijet_BDT_VR;
  WrappedTH1Triplet* h_AfterAllSelections_WMass_VR;
  WrappedTH1Triplet* h_AfterAllSelections_DeltaPhi_MuMET_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Pt_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Eta_VR;
  WrappedTH1Triplet* h_AfterAllSelections_Trijets_Phi_VR;
  

  WrappedTH2* hMET_vs_MuonMiniIso;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SystTopBDT);

SystTopBDT::SystTopBDT(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PrelimTopMVACut(config, "SystTopBDTSelection.MVACut"),
    cfg_LdgTopDefinition(config.getParameter<std::string>("FakeBTopSelectionBDT.LdgTopDefinition")),
    cfg_MiniIsoCut(config, "SystTopBDTSelection.MiniIsoCut"),
    cfg_MiniIsoInvCut(config, "SystTopBDTSelection.MiniIsoInvCut"),
    cfg_METCut(config, "SystTopBDTSelection.METCut"),
    
    // Muon Selection Cuts
    cfg_MuonPtCut(config.getParameter<float>("MuonSelection.muonPtCut")),
    cfg_MuonEtaCut(config.getParameter<float>("MuonSelection.muonEtaCut")),
    
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection")), // no subcounter in main counter
    fQGLRSelection(config.getParameter<ParameterSet>("QGLRSelection")),// fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void SystTopBDT::book(TDirectory *dir) {

  if (0) std::cout << "=== SystTopBDT::book()" << std::endl;
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fQGLRSelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  fFatJetSelection.bookHistograms(dir);

  // const int nTopMassBins  = fCommonPlots.getTopMassBinSettings().bins();
  // const float fTopMassMin = fCommonPlots.getTopMassBinSettings().min();
  // const float fTopMassMax = fCommonPlots.getTopMassBinSettings().max();

  const int nNBins        = fCommonPlots.getNjetsBinSettings().bins();
  const float fNMin       = fCommonPlots.getNjetsBinSettings().min();
  const float fNMax       = fCommonPlots.getNjetsBinSettings().max();

  // const int nBtagBins     = fCommonPlots.getBJetDiscBinSettings().bins();
  // const float fBtagMin    = fCommonPlots.getBJetDiscBinSettings().min();
  // const float fBtagMax    = fCommonPlots.getBJetDiscBinSettings().max();

  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = 2*fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = 2*fCommonPlots.getPtBinSettings().max();

  const int  nEtaBins     = fCommonPlots.getEtaBinSettings().bins();
  const float fEtaMin     = fCommonPlots.getEtaBinSettings().min();
  const float fEtaMax     = fCommonPlots.getEtaBinSettings().max();

  const int  nPhiBins     = fCommonPlots.getPhiBinSettings().bins();
  const float fPhiMin     = fCommonPlots.getPhiBinSettings().min();
  const float fPhiMax     = fCommonPlots.getPhiBinSettings().max();
  
  const int  nBDiscBins   = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBDiscMin   = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBDiscMax   = fCommonPlots.getBJetDiscBinSettings().max();
  
  const int nWMassBins    = fCommonPlots.getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots.getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots.getWMassBinSettings().max();
  
  const int nMetBins  = fCommonPlots.getMetBinSettings().bins();
  const float fMetMin = fCommonPlots.getMetBinSettings().min();
  const float fMetMax = fCommonPlots.getMetBinSettings().max();

  const int nHtBins  = fCommonPlots.getHtBinSettings().bins();
  const float fHtMin = fCommonPlots.getHtBinSettings().min();
  const float fHtMax = fCommonPlots.getHtBinSettings().max();
  
  //const int nDEtaBins     = fCommonPlots.getDeltaEtaBinSettings().bins();
  //const double fDEtaMin   = fCommonPlots.getDeltaEtaBinSettings().min();
  //const double fDEtaMax   = fCommonPlots.getDeltaEtaBinSettings().max();

  const int nDPhiBins     = fCommonPlots.getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots.getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots.getDeltaPhiBinSettings().max();

  const int nDRBins       = fCommonPlots.getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots.getDeltaRBinSettings().min();
  const double fDRMax     = fCommonPlots.getDeltaRBinSettings().max();

  TDirectory* dirTH1 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "SystTopBDT");
  TDirectory* dirTH2 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "SystTopBDT_TH2");
  std::string myInclusiveLabel  = "SystTopBDT_";
  std::string myFakeLabel       = myInclusiveLabel+"Fake";
  std::string myGenuineLabel    = myInclusiveLabel+"Genuine";
  TDirectory* myInclusiveDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myGenuineDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs = {myInclusiveDir, myFakeDir, myGenuineDir};

  hMET_vs_MuonMiniIso = fHistoWrapper.makeTH<TH2F>(HistoLevel::kInformative, dirTH2, "MET_vs_MuonMiniIso", ";E_{T, miss};miniIsolation", 
						   nMetBins, fMetMin, fMetMax, 100000, 0, 1000);


  // Book non-common histograms
  h_AfterStandardSelections_MET_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_MET_SR", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterStandardSelections_HT_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_HT_SR", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterStandardSelections_NJets_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NJets_SR", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_Jets_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Pt_SR", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jets_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Eta_SR", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterStandardSelections_Jets_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Phi_SR", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_NBJets_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NBJets_SR", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_BJets_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Pt_SR", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_BJets_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Eta_SR", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Phi_SR", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_CSV_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_CSV_SR", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Muon_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Pt_SR", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Muon_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Eta_SR", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Phi_SR", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_BJetMinDR_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_BJetMinDR_SR", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_Muon_LeadingTrijetDR_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_LeadingTrijetDR_SR", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_LeadingTrijet_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Pt_SR", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Eta_SR","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Phi_SR","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_Pt_SR", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_CSV_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_CSV_SR", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_WMass_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_WMass_SR", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  
  h_AfterStandardSelections_LeadingTrijet_BDT_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BDT_SR", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_DeltaPhi_MuMET_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_DeltaPhi_MuMET_SR", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);

  h_AfterStandardSelections_Trijets_Pt_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Pt_SR", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Trijets_Eta_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Eta_SR", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterStandardSelections_Trijets_Phi_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Phi_SR", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);

  // After All Selections
  h_AfterAllSelections_MET_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_MET_SR", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterAllSelections_HT_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_HT_SR", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterAllSelections_NJets_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NJets_SR", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_Jets_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Pt_SR", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jets_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Eta_SR", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterAllSelections_Jets_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Phi_SR", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_NBJets_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NBJets_SR", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_BJets_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Pt_SR", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_BJets_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Eta_SR", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Phi_SR", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_CSV_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_CSV_SR", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_Muon_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Pt_SR", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Muon_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Eta_SR", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Phi_SR", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_BJetMinDR_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_BJetMinDR_SR", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_Muon_LeadingTrijetDR_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_LeadingTrijetDR_SR", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_LeadingTrijet_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Pt_SR", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_Eta_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Eta_SR","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterAllSelections_LeadingTrijet_Phi_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Phi_SR","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_LeadingTrijet_BJet_Pt_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative,myDirs,"AfterAllSelections_LeadingTrijet_BJet_Pt_SR", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_BJet_CSV_SR =fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs,"AfterAllSelections_LeadingTrijet_BJet_CSV_SR", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_WMass_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_WMass_SR", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterAllSelections_LeadingTrijet_BDT_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BDT_SR", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_DeltaPhi_MuMET_SR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_DeltaPhi_MuMET_SR", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);

  h_AfterAllSelections_Trijets_Pt_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Pt_SR", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Trijets_Eta_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Eta_SR", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterAllSelections_Trijets_Phi_SR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Phi_SR", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);
    
  hCEvts_TopPassBDT_SR        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "CEvts_TopPassBDT",       ";"                        , 2,       0,      2     );
  hCEvts_PassSelections_SR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "CEvts_PassSelections",   ";"                        , 5,       0,      5     );

  //====================================================================
  //Control Region 1
  //====================================================================
  // Book non-common histograms
  h_AfterStandardSelections_MET_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_MET_CR1", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterStandardSelections_HT_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_HT_CR1", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterStandardSelections_NJets_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NJets_CR1", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_Jets_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Pt_CR1", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jets_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Eta_CR1", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterStandardSelections_Jets_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Phi_CR1", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_NBJets_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NBJets_CR1", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_BJets_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Pt_CR1", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_BJets_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Eta_CR1", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Phi_CR1", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_CSV_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_CSV_CR1", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Muon_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Pt_CR1", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Muon_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Eta_CR1", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Phi_CR1", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_BJetMinDR_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_BJetMinDR_CR1", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_Muon_LeadingTrijetDR_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_LeadingTrijetDR_CR1", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_LeadingTrijet_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Pt_CR1", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Eta_CR1","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Phi_CR1","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_Pt_CR1", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_CSV_CR1", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_WMass_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_WMass_CR1", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  
  h_AfterStandardSelections_LeadingTrijet_BDT_CR1= fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BDT_CR1", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_DeltaPhi_MuMET_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_DeltaPhi_MuMET_CR1", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  
  h_AfterStandardSelections_Trijets_Pt_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Pt_CR1", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Trijets_Eta_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Eta_CR1", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterStandardSelections_Trijets_Phi_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Phi_CR1", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);

  // After All Selections
  h_AfterAllSelections_MET_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_MET_CR1", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterAllSelections_HT_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_HT_CR1", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterAllSelections_NJets_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NJets_CR1", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_Jets_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Pt_CR1", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jets_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Eta_CR1", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterAllSelections_Jets_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Phi_CR1", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_NBJets_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NBJets_CR1", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_BJets_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Pt_CR1", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_BJets_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Eta_CR1", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Phi_CR1", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_CSV_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_CSV_CR1", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_Muon_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Pt_CR1", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Muon_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Eta_CR1", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Phi_CR1", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_BJetMinDR_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_BJetMinDR_CR1", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_Muon_LeadingTrijetDR_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_LeadingTrijetDR_CR1", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_LeadingTrijet_Pt_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Pt_CR1", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_Eta_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Eta_CR1","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterAllSelections_LeadingTrijet_Phi_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Phi_CR1","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR1 =fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs,"AfterAllSelections_LeadingTrijet_BJet_Pt_CR1", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR1 =fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs,"AfterAllSelections_LeadingTrijet_BJet_CSV_CR1", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_WMass_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_WMass_CR1", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterAllSelections_LeadingTrijet_BDT_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BDT_CR1", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_DeltaPhi_MuMET_CR1 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_DeltaPhi_MuMET_CR1", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  h_AfterAllSelections_Trijets_Pt_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Pt_CR1", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Trijets_Eta_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Eta_CR1", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterAllSelections_Trijets_Phi_CR1  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Phi_CR1", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);
   
  //====================================================================
  //Control Region 2
  //====================================================================
  // Book non-common histograms
  h_AfterStandardSelections_MET_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_MET_CR2", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterStandardSelections_HT_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_HT_CR2", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterStandardSelections_NJets_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NJets_CR2", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_Jets_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Pt_CR2", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jets_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Eta_CR2", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterStandardSelections_Jets_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Phi_CR2", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_NBJets_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NBJets_CR2", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_BJets_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Pt_CR2", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_BJets_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Eta_CR2", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Phi_CR2", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_CSV_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_CSV_CR2", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Muon_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Pt_CR2", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Muon_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Eta_CR2", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Phi_CR2", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_BJetMinDR_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_BJetMinDR_CR2", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_Muon_LeadingTrijetDR_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_LeadingTrijetDR_CR2", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_LeadingTrijet_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Pt_CR2", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Eta_CR2","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Phi_CR2","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_Pt_CR2", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_CSV_CR2", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_WMass_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_WMass_CR2", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterStandardSelections_DeltaPhi_MuMET_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_DeltaPhi_MuMET_CR2", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  h_AfterStandardSelections_LeadingTrijet_BDT_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BDT_CR2", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Trijets_Pt_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Pt_CR2", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Trijets_Eta_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Eta_CR2", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterStandardSelections_Trijets_Phi_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Phi_CR2", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);
 
  // After All Selections
  h_AfterAllSelections_MET_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_MET_CR2", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterAllSelections_HT_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_HT_CR2", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterAllSelections_NJets_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NJets_CR2", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_Jets_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Pt_CR2", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jets_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Eta_CR2", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterAllSelections_Jets_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Phi_CR2", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_NBJets_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NBJets_CR2", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_BJets_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Pt_CR2", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_BJets_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Eta_CR2", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Phi_CR2", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_CSV_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_CSV_CR2", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_Muon_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Pt_CR2", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Muon_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Eta_CR2", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Phi_CR2", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_BJetMinDR_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_BJetMinDR_CR2", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_Muon_LeadingTrijetDR_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_LeadingTrijetDR_CR2", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_LeadingTrijet_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Pt_CR2", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_Eta_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Eta_CR2","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterAllSelections_LeadingTrijet_Phi_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Phi_CR2","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs,"AfterAllSelections_LeadingTrijet_BJet_Pt_CR2", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs,"AfterAllSelections_LeadingTrijet_BJet_CSV_CR2", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_WMass_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_WMass_CR2", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterAllSelections_LeadingTrijet_BDT_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BDT_CR2", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_DeltaPhi_MuMET_CR2 = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_DeltaPhi_MuMET_CR2", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  h_AfterAllSelections_Trijets_Pt_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Pt_CR2", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Trijets_Eta_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Eta_CR2", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterAllSelections_Trijets_Phi_CR2  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Phi_CR2", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);
  
  //====================================================================
  //Verification Region
  //====================================================================
  // Book non-common histograms
  h_AfterStandardSelections_MET_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_MET_VR", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterStandardSelections_HT_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_HT_VR", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterStandardSelections_NJets_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NJets_VR", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_Jets_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Pt_VR", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jets_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Eta_VR", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterStandardSelections_Jets_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Jets_Phi_VR", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_NBJets_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_NBJets_VR", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterStandardSelections_BJets_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Pt_VR", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_BJets_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Eta_VR", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_Phi_VR", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_BJets_CSV_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_BJets_CSV_VR", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Muon_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Pt_VR", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Muon_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Eta_VR", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_Phi_VR", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_Muon_BJetMinDR_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_BJetMinDR_VR", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_Muon_LeadingTrijetDR_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Muon_LeadingTrijetDR_VR", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterStandardSelections_LeadingTrijet_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Pt_VR", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Eta_VR","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_Phi_VR","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_Pt_VR", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LeadingTrijet_BJet_CSV_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BJet_CSV_VR", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_WMass_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_WMass_VR", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterStandardSelections_DeltaPhi_MuMET_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_DeltaPhi_MuMET_VR", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  h_AfterStandardSelections_LeadingTrijet_BDT_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_LeadingTrijet_BDT_VR", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterStandardSelections_Trijets_Pt_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Pt_VR", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Trijets_Eta_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Eta_VR", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterStandardSelections_Trijets_Phi_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterStandardSelections_Trijets_Phi_VR", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);

  // After All Selections
  h_AfterAllSelections_MET_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_MET_VR", "MET", nMetBins, fMetMin, fMetMax);
  h_AfterAllSelections_HT_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_HT_VR", "H_{T} (GeV/c)", nHtBins, fHtMin, fHtMax);
  h_AfterAllSelections_NJets_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NJets_VR", "Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_Jets_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Pt_VR", "Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jets_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Eta_VR", "Jets #eta", nEtaBins, fEtaMin, fEtaMax); 
  h_AfterAllSelections_Jets_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Jets_Phi_VR", "Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_NBJets_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_NBJets_VR", "B-Jets Multiplicity", nNBins, fNMin, fNMax);
  h_AfterAllSelections_BJets_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Pt_VR", "B-Jets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_BJets_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Eta_VR", "B-Jets #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_Phi_VR", "B-Jets #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_BJets_CSV_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_BJets_CSV_VR", "B-Jets CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_Muon_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Pt_VR", "#mu p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Muon_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Eta_VR", "#mu #eta", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_Phi_VR", "#mu #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_Muon_BJetMinDR_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_BJetMinDR_VR", "Min #Delta R(#mu, b-jet)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_Muon_LeadingTrijetDR_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Muon_LeadingTrijetDR_VR", "#Delta R(#mu, leading top)", nDRBins, fDRMin, fDRMax);
  h_AfterAllSelections_LeadingTrijet_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Pt_VR", "Leading top p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_Eta_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Eta_VR","Leading top #eta", 4*nEtaBins, 4*fEtaMin,4*fEtaMax);
  h_AfterAllSelections_LeadingTrijet_Phi_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_Phi_VR","Leading top #phi", nEtaBins, fEtaMin,fEtaMax);
  h_AfterAllSelections_LeadingTrijet_BJet_Pt_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BJet_Pt_VR", "Leading top, b-jet p_{T} (GeV/c)",  nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LeadingTrijet_BJet_CSV_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BJet_CSV_VR", "Leading top, b-jet CSV", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_WMass_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_WMass_VR", "W Mass (GeV/c^{2})", nWMassBins, fWMassMin, fWMassMax);
  h_AfterAllSelections_LeadingTrijet_BDT_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_LeadingTrijet_BDT_VR", " Leading top BDT", nBDiscBins, fBDiscMin, fBDiscMax);
  h_AfterAllSelections_DeltaPhi_MuMET_VR = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_DeltaPhi_MuMET_VR", "#Delta #phi(#mu, E_{T, miss})", nDPhiBins, fDPhiMin, fDPhiMax);
  h_AfterAllSelections_Trijets_Pt_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Pt_VR", "Trijets p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Trijets_Eta_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Eta_VR", "Trijets #eta", nEtaBins, fEtaMin, fEtaMax);
  h_AfterAllSelections_Trijets_Phi_VR  = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myDirs, "AfterAllSelections_Trijets_Phi_VR", "Trijets #phi", nPhiBins, fPhiMin, fPhiMax);
  
  //====================================================================

  return;
}


void SystTopBDT::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void SystTopBDT::process(Long64_t entry) {

  // Sanity check
  if (cfg_LdgTopDefinition != "MVA" &&  cfg_LdgTopDefinition != "Pt")
    {
      throw hplus::Exception("config") << "Unsupported method of defining the leading top (=" << cfg_LdgTopDefinition << "). Please select from \"MVA\" and \"Pt\".";
    }

  int Debug = 0;


  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  //================================================================================================   
  // 1) Apply HLT_IsoMu24 trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;
  
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

  //================================================================================================   
  // 2) MET filters (to remove events with spurious sources of fake MET)
  //================================================================================================   
  if (0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  

  //================================================================================================   
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================   
  if (0) std::cout << "=== Vertices" << std::endl;
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  //================================================================================================   
  // 4) Electron veto (Fully hadronic + orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================   
  // 5) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 6) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
 
  //================================================================================================  
  // 7) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
   fCommonPlots.fillControlPlotsAfterBjetSelection(fEvent, bjetData);

  //================================================================================================  
  // 8) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBTaggingSFCounter.increment();

  //================================================================================================
  // - MET selection
  //================================================================================================
  if (0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.silentAnalyze(fEvent, nVertices);
  //if (!METData.passedSelection()) return;
  
  //================================================================================================
  // 10) Quark-Gluon Likelihood Ratio Selection
  //================================================================================================
  if (0) std::cout << "=== QGLR selection" << std::endl;
  const QuarkGluonLikelihoodRatio::Data QGLRData = fQGLRSelection.analyze(fEvent, jetData, bjetData);
  if (!QGLRData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);
  
  bool passPrelimMVACut = false;  
  if (topData.getSelectedTopsBJet().size() > 0) passPrelimMVACut = true;
  
  hCEvts_TopPassBDT_SR -> Fill("All Events", 1);
  hCEvts_PassSelections_SR -> Fill("All Events", 1);
  if (passPrelimMVACut){
    hCEvts_TopPassBDT_SR -> Fill("Pass BDT", 1);
    hCEvts_PassSelections_SR -> Fill("Selected Tops", 1);
  }

  
  // ================================================================================================
  // Muon Selection
  // ================================================================================================
  if (0) std::cout << "\n=== Muon Selection" << std::endl;
  
  std::vector<Muon> selectedMuons;
  // For-loop: All muons
  for(Muon muon: fEvent.muons()) {
    
    // Apply cut on pt
    if (muon.pt() < cfg_MuonPtCut) continue;
    
    // Apply cut on abs(eta)
    if (std::fabs(muon.eta()) > cfg_MuonEtaCut) continue;
    
    // Apply cut on muon ID
    if (!muon.muonIDDiscriminator()) continue;
    
    //double miniIso = muon.effAreaMiniIso();
        
    selectedMuons.push_back(muon);
  }
  
  if (selectedMuons.size() != 1) return;
  
  const Muon mu = selectedMuons.at(0);
    
  if (Debug) std::cout<<" Muon ="<<mu.index()<<"  pT="<<mu.pt()<<"  eta="<<mu.eta()<<"  miniIso="<<mu.muonIDDiscriminator()<<std::endl;
  
  
  //================================================================================================
  // PreSelections
  //================================================================================================
  if (Debug) std::cout << "\n=== PreSelections" << std::endl;
  
  // Increment counters & fill histograms
  cSelected.increment();
  
  if (Debug){
    std::cout<<" "<<std::endl;
    std::cout<<"=== Event = "<<entry<<"  passed all pre-selections"<<std::endl;
  }
  
  double met = METData.getMET().R();
  double dRmin_mu_bjet = 999.999;
  
  bool MuPass_Iso       = cfg_MiniIsoCut.passedCut(mu.effAreaMiniIso());
  bool MuPass_InvIso    = cfg_MiniIsoInvCut.passedCut(mu.effAreaMiniIso()) && !MuPass_Iso;
  bool MetPassCut       = cfg_METCut.passedCut(met);

  if (0)
    {
      //if (MuPass_Iso)       std::cout << "Pass Muon Isolation: "          << mu.effAreaMiniIso() << std::endl;
      if (MuPass_InvIso)    std::cout << "Pass Muon Inverted Isolation: " << mu.effAreaMiniIso() << std::endl;
      //if (!MetPassCut)      std::cout << "Fail MET Selection: "           << met                 << std::endl;
      std::cout<<"==="<<std::endl;      
    }
  
  bool searchForLeptonicTop = false;
  Jet BJet_LeptonicBr;
  if (searchForLeptonicTop)
    {
      for (auto& bjet: bjetData.getSelectedBJets()) 
	{
	  // DeltaR(mu, bjet)
	  double dR = ROOT::Math::VectorUtil::DeltaR(mu.p4(), bjet.p4());
      
	  if (dR < dRmin_mu_bjet){
	    BJet_LeptonicBr = bjet;
	    dRmin_mu_bjet  = dR;
	  }
	}
      // Apply DR cut selection between b-jet and muon
      if (dRmin_mu_bjet > 1.5) return;
    }

  hCEvts_PassSelections_SR -> Fill("B from mu", 1);
  //if (Debug) std::cout<<"Muon pT = "<<mu.pt()<<"  BJet index="<<BJet_LeptonicBr.index()<<"  BJet pT="<<BJet_LeptonicBr.pt()<<"   ΔR( μ, bjet) = "<<dRmin_mu_bjet<<std::endl;

  /*  
  int nTopCandidates = 0;
  int nTopCandidatesFarFromMuon = 0;
  
  nTopCandidates            = TopCandMultiplicity(topData, "all", BJet_LeptonicBr, mu, searchForLeptonicTop, false);
  nTopCandidatesFarFromMuon = TopCandMultiplicity(topData, "all", BJet_LeptonicBr, mu, searchForLeptonicTop, true);
  
  if (0){
    std::cout<<" Found "<<nTopCandidates            <<" candidates"<<std::endl;
    std::cout<<" Found "<<nTopCandidatesFarFromMuon <<" candidates far from muon"<<std::endl;
  }
  */
  vector<int> vAllTops_index      = GetTopsIndex(topData, "all", BJet_LeptonicBr, mu, searchForLeptonicTop, true);

  int nTopCandidatesFarFromMuon = vAllTops_index.size();

  // At least 1 top candidate far from muon
  if (nTopCandidatesFarFromMuon < 1) return;
  hCEvts_PassSelections_SR -> Fill("Top far from Mu", 1);
  hMET_vs_MuonMiniIso      -> Fill(met, mu.effAreaMiniIso());
  //=======================================================================
  // Split int Baseline - Inverted Analysis
  //=======================================================================
  if (MetPassCut)
    {
      if (Debug) std::cout<<"Will do Baseline Analysis"<<std::endl;
      DoBaselineAnalysis(jetData, bjetData, mu, METData, topData, BJet_LeptonicBr, searchForLeptonicTop);
    }
  else
    {
      if (Debug) std::cout<<"Will do Inverted Analysis"<<std::endl;
      DoInvertedAnalysis(jetData, bjetData, mu, METData, topData, BJet_LeptonicBr, searchForLeptonicTop);
    }

  return;
}


void SystTopBDT::DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData,  Muon mu, const METSelection::Data& METData, 
				    const TopSelectionBDT::Data& topData, Jet BJet_LeptonicBr, bool searchForLeptonicTop){

  int Debug = 0;
  double met    = METData.getMET().R();
  // double dRmin_mu_bjet = 999.999;
  // double dRmin_mu_top  = 999.999;
  // size_t nTops = topData.getAllTopsMVA().size();
  
  // Calculate transverse W mass
  double deltaPhi_mu_met = std::abs(ROOT::Math::VectorUtil::DeltaPhi(mu.p4(), METData.getMET()));
  double MT = sqrt(2*met*mu.pt()*(1-cos(deltaPhi_mu_met)));

  vector<int> vAllTops_index      = GetTopsIndex(topData, "all", BJet_LeptonicBr, mu, searchForLeptonicTop, true);
  vector<int> vSelectedTops_index = GetTopsIndex(topData, "selected", BJet_LeptonicBr, mu, searchForLeptonicTop, true);

  int ldgTopIndex = getLeadingTopIndex(topData, "all", mu, BJet_LeptonicBr, searchForLeptonicTop);
  int nTopCandidatesFarFromMuonPassBDT = vSelectedTops_index.size();

  /*
  // Search for Tops passing the BDT cut
  int nTopCandidatesFarFromMuonPassBDT = TopCandMultiplicity(topData, "selected", BJet_LeptonicBr, mu, searchForLeptonicTop, true);
  */

  Jet  ldgTop_Jet1 =  topData.getAllTopsJet1().at(ldgTopIndex);
  Jet  ldgTop_Jet2 =  topData.getAllTopsJet2().at(ldgTopIndex);
  Jet  ldgTop_BJet =  topData.getAllTopsBJet().at(ldgTopIndex);
  float ldgTop_MVA =  topData.getAllTopsMVA().at(ldgTopIndex);

  // Get 4-momentum of top (trijet)
  math::XYZTLorentzVector LdgTop_p4;
  LdgTop_p4 = ldgTop_Jet1.p4() + ldgTop_Jet2.p4() + ldgTop_BJet.p4();
  
  //DeltaR(mu, top)
  double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgTop_p4);
  
  double LdgTrijet_MaxPt    = LdgTop_p4.pt();
  double LdgTrijet_Eta      = LdgTop_p4.eta();
  double LdgTrijet_Phi      = LdgTop_p4.phi();
  double DR_mu_LdgTrijet    = dR_mu_top;
  double LdgTrijet_BJet_Pt  = ldgTop_BJet.pt();
  double LdgTrijet_BJet_CSV = ldgTop_BJet.bjetDiscriminator();
  
  if (Debug)
    {
      std::cout<<"leading top index = "<<ldgTopIndex<<std::endl;
      std::cout<<"leading top BDT = "  <<topData.getAllTopsMVA().at(ldgTopIndex)<<std::endl;
    }
  
  bool MuPass_Iso       = cfg_MiniIsoCut.passedCut(mu.effAreaMiniIso());
  bool MuPass_InvIso    = cfg_MiniIsoInvCut.passedCut(mu.effAreaMiniIso()) && !MuPass_Iso;

  
  //Matching
  const double twoSigma = 0.32;
  const double dRcut    = 0.4;
  bool isGenuineTop_StandardSelections = false;
  bool isGenuineTop_AllSelections = false;

  if (fEvent.isMC()){
    vector<genParticle> GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
    vector<genParticle> GenTops_BQuark, GenTops_LdgQuark, GenTops_SubldgQuark;
    for (auto& top: GenTops){
      vector<genParticle> quarks;
      genParticle bquark;
      bool foundB = false;
      for (size_t i=0; i<top.daughters().size(); i++){
        int dau_index = top.daughters().at(i);
        genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
        // B-Quark                                                                                                                                                                          
        if (std::abs(dau.pdgId()) ==  5){
          bquark = dau;
          foundB = true;
        }
        // W-Boson                                                                                                                                                                                                     
        if (std::abs(dau.pdgId()) == 24){
          // Get the last copy                                                                                                                                                                                         
          genParticle W = GetLastCopy(fEvent.genparticles().getGenParticles(), dau);
          // Find the decay products of W                                                                                                                                                                              
          for (size_t idau=0; idau<W.daughters().size(); idau++){
            int Wdau_index = W.daughters().at(idau);
            genParticle Wdau = fEvent.genparticles().getGenParticles()[Wdau_index];
            // Consider only quarks as decaying products                                                                                                                                                               
            if (std::abs(Wdau.pdgId()) > 5) continue;
	    quarks.push_back(Wdau);
          }
        }
      }
      //Soti: If top does not decay into W+b return
      if (!foundB) return;   
      // Fill vectors for b-quarks, leading and subleading quarks coming from tops 
      GenTops_BQuark.push_back(bquark);
      if (Debug) std::cout<<"W decay products = "<<quarks.size()<<std::endl;
      
      if (quarks.size() == 2){
	if (quarks.at(0).pt() > quarks.at(1).pt()) {
	  GenTops_LdgQuark.push_back(quarks.at(0));
	  GenTops_SubldgQuark.push_back(quarks.at(1));
	}
	else{
	  GenTops_LdgQuark.push_back(quarks.at(1));
	  GenTops_SubldgQuark.push_back(quarks.at(0));
	}
      }
    }
    
    //======= B jet matching (Loop over all Jets)                                                                                                                                                 
    int imatched =0;
    vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, BJetCand;
    vector <double> dRminB;
    for (size_t i=0; i<GenTops.size(); i++){
      genParticle BQuark      = GenTops_BQuark.at(i);
      Jet mcMatched_BJet;
      double dRmin  = 99999.9;
      for (auto& bjet: jetData.getSelectedJets()){
	double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
	double dPtOverPt = std::abs((bjet.pt() - BQuark.pt())/BQuark.pt());
	if (dR > dRcut)   continue;
	if (dR > dRmin)   continue;
	if (dPtOverPt > twoSigma) continue;
	dRmin  = dR;	
	mcMatched_BJet = bjet;
      }
      dRminB.push_back(dRmin);
	BJetCand.push_back(mcMatched_BJet);
    }
      
    //======= Dijet matching (Loop over all Jets)     
    for (size_t i=0; i<GenTops_LdgQuark.size(); i++){
      genParticle LdgQuark    = GenTops_LdgQuark.at(i);
      genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
      Jet mcMatched_LdgJet, mcMatched_SubldgJet;
      double dR1min = 9999.9, dR2min = 9999.9;
      for (auto& jet: jetData.getSelectedJets()){
	bool same = false;
	for (size_t k=0; k<GenTops.size(); k++){
	  if (dRminB.at(k) <= dRcut){
	    if( areSameJets(jet,BJetCand.at(k))) same = true; //Skip the jets that are matched with bquarks   
	  }
	}
	if (same) continue;
	double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
	double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
	double dPtOverPt1 = std::abs((jet.pt() - LdgQuark.pt())/LdgQuark.pt());
	double dPtOverPt2 = std::abs( (jet.pt() - SubldgQuark.pt())/SubldgQuark.pt());
	if (std::min(dR1, dR2) > dRcut) continue;	
	if (dR1 < dR2)
	  {
	    if (dR1 < dR1min)
	      {
		if(dPtOverPt1 < twoSigma)
		  {
		    dR1min = dR1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	    else if (dR2 <= dRcut && dR2 < dR2min)
	      {
		if (dPtOverPt2 < twoSigma)
		  {
		    dR2min  = dR2;
		    mcMatched_SubldgJet = jet;
		  }
	      }
	  }
	else
	  {
	    if (dR2 < dR2min)
	      {
		if(dPtOverPt2 < twoSigma)
		    {
		      dR2min  = dR2;
		      mcMatched_SubldgJet = jet;
		    }
	      }
	    else if (dR1 <= dRcut && dR1 < dR1min)
	      {
		if (dPtOverPt1 < twoSigma)
		  {
		    dR1min  = dR1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	  }
      }
      if (Debug) std::cout<<"MCtrue: size: "<<MCtrue_LdgJet.size()<<" "<<MCtrue_SubldgJet.size()<<" "<<MCtrue_Bjet.size()<<std::endl;
      //Genuine if all the top quarks are matched   
      genParticle top = GenTops.at(i);
      bool genuine = (dR1min<= dRcut && dR2min <= dRcut && dRminB.at(i) <= dRcut);
      if (genuine){
	imatched ++;
	MCtrue_LdgJet.push_back(mcMatched_LdgJet);
	MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
	MCtrue_Bjet.push_back(BJetCand.at(i));
      }
    }
    isGenuineTop_StandardSelections = IsGenuineTop(topData, "all", mu, BJet_LeptonicBr, searchForLeptonicTop, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
    isGenuineTop_AllSelections      = IsGenuineTop(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
    //Skip if no trijets have been mached for datasets with gen top
    bool haveGenTop        = GenTops.size() > 0;
    bool haveMatchedTrijet = MCtrue_Bjet.size() > 0;

    if (0) {
      if (haveGenTop && !haveMatchedTrijet) return;
    }
  }//if (fEvent.isMC())

  if (MuPass_Iso){ 
    if (Debug) std::cout<<"Signal R"<<std::endl;    
    //=======================================================================
    //SIGNAL REGION
    //=======================================================================
    h_AfterStandardSelections_MET_SR         -> Fill(isGenuineTop_StandardSelections, met);
    h_AfterStandardSelections_HT_SR          -> Fill(isGenuineTop_StandardSelections, jetData.HT());
    h_AfterStandardSelections_NJets_SR       -> Fill(isGenuineTop_StandardSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterStandardSelections_Jets_Pt_SR   -> Fill(isGenuineTop_StandardSelections, jet.pt()); 
      h_AfterStandardSelections_Jets_Eta_SR  -> Fill(isGenuineTop_StandardSelections, jet.eta());
      h_AfterStandardSelections_Jets_Phi_SR  -> Fill(isGenuineTop_StandardSelections, jet.phi());
    }
    h_AfterStandardSelections_NBJets_SR      -> Fill(isGenuineTop_StandardSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterStandardSelections_BJets_Pt_SR  -> Fill(isGenuineTop_StandardSelections, bjet.pt());
      h_AfterStandardSelections_BJets_Eta_SR -> Fill(isGenuineTop_StandardSelections, bjet.eta());
      h_AfterStandardSelections_BJets_Phi_SR -> Fill(isGenuineTop_StandardSelections, bjet.phi());
      h_AfterStandardSelections_BJets_CSV_SR -> Fill(isGenuineTop_StandardSelections, bjet.bjetDiscriminator());
    }

    for (size_t i=0; i < vAllTops_index.size(); i++){
      int index = vAllTops_index.at(i);
      Jet bjet = topData.getAllTopsBJet().at(index);
      Jet jet1 = topData.getAllTopsJet1().at(index);
      Jet jet2 = topData.getAllTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterStandardSelections_Trijets_Pt_SR  -> Fill(isGenuineTop_StandardSelections, Top_p4.Pt());
      h_AfterStandardSelections_Trijets_Eta_SR -> Fill(isGenuineTop_StandardSelections, Top_p4.Eta());
      h_AfterStandardSelections_Trijets_Phi_SR -> Fill(isGenuineTop_StandardSelections, Top_p4.Phi());
    }

    h_AfterStandardSelections_Muon_Pt_SR     -> Fill(isGenuineTop_StandardSelections, mu.pt());
    h_AfterStandardSelections_Muon_Eta_SR    -> Fill(isGenuineTop_StandardSelections, mu.eta());
    h_AfterStandardSelections_Muon_Phi_SR    -> Fill(isGenuineTop_StandardSelections, mu.phi());
    h_AfterStandardSelections_WMass_SR      -> Fill(isGenuineTop_StandardSelections, MT);
    h_AfterStandardSelections_LeadingTrijet_BDT_SR -> Fill(isGenuineTop_StandardSelections, ldgTop_MVA);
    h_AfterStandardSelections_DeltaPhi_MuMET_SR    -> Fill(isGenuineTop_StandardSelections, deltaPhi_mu_met);
    //h_AfterStandardSelections_Muon_BJetMinDR         -> Fill(isGenuineTop_StandardSelections, dRmin_mu_bjet);
    h_AfterStandardSelections_Muon_LeadingTrijetDR_SR   -> Fill(isGenuineTop_StandardSelections, DR_mu_LdgTrijet);
    h_AfterStandardSelections_LeadingTrijet_Pt_SR       -> Fill(isGenuineTop_StandardSelections, LdgTrijet_MaxPt);
    h_AfterStandardSelections_LeadingTrijet_Eta_SR      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Eta);
    h_AfterStandardSelections_LeadingTrijet_Phi_SR      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Phi);
    h_AfterStandardSelections_LeadingTrijet_BJet_Pt_SR  -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_Pt);
    h_AfterStandardSelections_LeadingTrijet_BJet_CSV_SR -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_CSV);
    
    if (Debug){
      std::cout<<" "<<std::endl;
      std::cout<<" Top candidates passing BDT:  "<< topData.getSelectedTopsBJet().size()<< std::endl;
      std::cout<<" "<<std::endl;
    }    
       
    //=======================================================================
    // Final Selection
    //=======================================================================
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
    hCEvts_PassSelections_SR -> Fill("Top pass BDT", 1);
    
    int selected_ldgTopIndex = getLeadingTopIndex(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop);

    Jet ldgSelTop_Jet1 =  topData.getAllTopsJet1().at(selected_ldgTopIndex);
    Jet ldgSelTop_Jet2 =  topData.getAllTopsJet2().at(selected_ldgTopIndex);
    Jet ldgSelTop_BJet =  topData.getAllTopsBJet().at(selected_ldgTopIndex);
    
    // Get 4-momentum of top (trijet)
    math::XYZTLorentzVector LdgSelTop_p4;
    LdgSelTop_p4 = ldgSelTop_Jet1.p4() + ldgSelTop_Jet2.p4() + ldgSelTop_BJet.p4();
    
    //DeltaR(mu, top)
    double dR_mu_selTop = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgSelTop_p4);
    
    // Do I need them?
    double LdgBDTTrijet_MaxPt    = LdgSelTop_p4.pt();
    double LdgBDTTrijet_Eta      = LdgSelTop_p4.eta();
    double LdgBDTTrijet_Phi      = LdgSelTop_p4.phi();
    double LdgBDTTrijet_BJet_Pt  = ldgSelTop_BJet.pt();
    double LdgBDTTrijet_BJet_CSV = ldgSelTop_BJet.bjetDiscriminator();
    double LdgBDTTrijet_MuDR     = dR_mu_selTop;
    
    if (0) std::cout<<LdgBDTTrijet_MaxPt<<LdgBDTTrijet_Eta<<LdgBDTTrijet_Phi<<LdgBDTTrijet_BJet_Pt<<LdgBDTTrijet_BJet_CSV<<LdgBDTTrijet_MuDR<<std::endl;  //Avoid warnings

    // Final Selection
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
    hCEvts_PassSelections_SR -> Fill("Top pass BDT", 1);
			 
    if (Debug){
      std::cout<<"Leading BDT Trijet  pT="<<LdgBDTTrijet_MaxPt<<"  Eta="<<LdgBDTTrijet_Eta<<std::endl;
      std::cout<<"Standard Selections Genuine B: "<<isGenuineTop_StandardSelections<<std::endl;
      std::cout<<"All Selections Genuine B: "<<isGenuineTop_AllSelections<<std::endl;
      std::cout<<"==="<<std::endl;
    }
    //=======================================================================
    // Fill Plots: After All Selections
    //=======================================================================
    h_AfterAllSelections_MET_SR         -> Fill(isGenuineTop_AllSelections, met);
    h_AfterAllSelections_HT_SR          -> Fill(isGenuineTop_AllSelections, jetData.HT());
    h_AfterAllSelections_NJets_SR       -> Fill(isGenuineTop_AllSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterAllSelections_Jets_Pt_SR   -> Fill(isGenuineTop_AllSelections, jet.pt()); 
      h_AfterAllSelections_Jets_Eta_SR  -> Fill(isGenuineTop_AllSelections, jet.eta());
      h_AfterAllSelections_Jets_Phi_SR  -> Fill(isGenuineTop_AllSelections, jet.phi());
    }
    h_AfterAllSelections_NBJets_SR      -> Fill(isGenuineTop_AllSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterAllSelections_BJets_Pt_SR  -> Fill(isGenuineTop_AllSelections, bjet.pt());
      h_AfterAllSelections_BJets_Eta_SR -> Fill(isGenuineTop_AllSelections, bjet.eta());
      h_AfterAllSelections_BJets_Phi_SR -> Fill(isGenuineTop_AllSelections, bjet.phi());
      h_AfterAllSelections_BJets_CSV_SR -> Fill(isGenuineTop_AllSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vSelectedTops_index.size(); i++){
      int index = vSelectedTops_index.at(i);
      Jet bjet = topData.getSelectedTopsBJet().at(index);
      Jet jet1 = topData.getSelectedTopsJet1().at(index);
      Jet jet2 = topData.getSelectedTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterAllSelections_Trijets_Pt_SR  -> Fill(isGenuineTop_AllSelections, Top_p4.Pt());
      h_AfterAllSelections_Trijets_Eta_SR -> Fill(isGenuineTop_AllSelections, Top_p4.Eta());
      h_AfterAllSelections_Trijets_Phi_SR -> Fill(isGenuineTop_AllSelections, Top_p4.Phi());
    }
    h_AfterAllSelections_Muon_Pt_SR     -> Fill(isGenuineTop_AllSelections, mu.pt());
    h_AfterAllSelections_Muon_Eta_SR    -> Fill(isGenuineTop_AllSelections, mu.eta());
    h_AfterAllSelections_Muon_Phi_SR    -> Fill(isGenuineTop_AllSelections, mu.phi());
    //h_AfterAllSelections_Muon_BJetMinDR -> Fill(isGenuineTop_AllSelections, dRmin_mu_bjet);
    h_AfterAllSelections_WMass_SR       -> Fill(isGenuineTop_AllSelections, MT);
    
    h_AfterAllSelections_LeadingTrijet_BDT_SR -> Fill(isGenuineTop_AllSelections, ldgTop_MVA);
    h_AfterAllSelections_DeltaPhi_MuMET_SR    -> Fill(isGenuineTop_AllSelections, deltaPhi_mu_met);
    
    if (cfg_PrelimTopMVACut.passedCut(ldgTop_MVA)){
      h_AfterAllSelections_Muon_LeadingTrijetDR_SR   -> Fill(isGenuineTop_AllSelections, DR_mu_LdgTrijet);
      h_AfterAllSelections_LeadingTrijet_Pt_SR       -> Fill(isGenuineTop_AllSelections, LdgTrijet_MaxPt);
      h_AfterAllSelections_LeadingTrijet_Eta_SR      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Eta);
      h_AfterAllSelections_LeadingTrijet_Phi_SR      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Phi);
      h_AfterAllSelections_LeadingTrijet_BJet_Pt_SR  -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_Pt);
      h_AfterAllSelections_LeadingTrijet_BJet_CSV_SR -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_CSV);
    }
    // We need another plot with the LeadingTrijet BDT
    if (Debug) std::cout<<"End of Signal R"<<std::endl;    
  } //Signal Region
  
  else if (MuPass_InvIso){
    //=======================================================================
    //VERIFICATION REGION
    //=======================================================================
    if (Debug) std::cout<<"Verification R"<<std::endl;

    h_AfterStandardSelections_MET_VR         -> Fill(isGenuineTop_StandardSelections, met);
    h_AfterStandardSelections_HT_VR          -> Fill(isGenuineTop_StandardSelections, jetData.HT());
    h_AfterStandardSelections_NJets_VR       -> Fill(isGenuineTop_StandardSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterStandardSelections_Jets_Pt_VR   -> Fill(isGenuineTop_StandardSelections, jet.pt()); 
      h_AfterStandardSelections_Jets_Eta_VR  -> Fill(isGenuineTop_StandardSelections, jet.eta());
      h_AfterStandardSelections_Jets_Phi_VR  -> Fill(isGenuineTop_StandardSelections, jet.phi());
    }
    h_AfterStandardSelections_NBJets_VR      -> Fill(isGenuineTop_StandardSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterStandardSelections_BJets_Pt_VR  -> Fill(isGenuineTop_StandardSelections, bjet.pt());
      h_AfterStandardSelections_BJets_Eta_VR -> Fill(isGenuineTop_StandardSelections, bjet.eta());
      h_AfterStandardSelections_BJets_Phi_VR -> Fill(isGenuineTop_StandardSelections, bjet.phi());
      h_AfterStandardSelections_BJets_CSV_VR -> Fill(isGenuineTop_StandardSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vAllTops_index.size(); i++){
      int index = vAllTops_index.at(i);
      Jet bjet = topData.getAllTopsBJet().at(index);
      Jet jet1 = topData.getAllTopsJet1().at(index);
      Jet jet2 = topData.getAllTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterStandardSelections_Trijets_Pt_VR  -> Fill(isGenuineTop_StandardSelections, Top_p4.Pt());
      h_AfterStandardSelections_Trijets_Eta_VR -> Fill(isGenuineTop_StandardSelections, Top_p4.Eta());
      h_AfterStandardSelections_Trijets_Phi_VR -> Fill(isGenuineTop_StandardSelections, Top_p4.Phi());
    }
    h_AfterStandardSelections_Muon_Pt_VR     -> Fill(isGenuineTop_StandardSelections, mu.pt());
    h_AfterStandardSelections_Muon_Eta_VR    -> Fill(isGenuineTop_StandardSelections, mu.eta());
    h_AfterStandardSelections_Muon_Phi_VR    -> Fill(isGenuineTop_StandardSelections, mu.phi());
    h_AfterStandardSelections_WMass_VR      -> Fill(isGenuineTop_StandardSelections, MT);
    h_AfterStandardSelections_LeadingTrijet_BDT_VR      -> Fill(isGenuineTop_StandardSelections, ldgTop_MVA);
    h_AfterStandardSelections_DeltaPhi_MuMET_VR         -> Fill(isGenuineTop_StandardSelections, deltaPhi_mu_met);
    //h_AfterStandardSelections_Muon_BJetMinDR          -> Fill(isGenuineTop_StandardSelections, dRmin_mu_bjet);
    h_AfterStandardSelections_Muon_LeadingTrijetDR_VR   -> Fill(isGenuineTop_StandardSelections, DR_mu_LdgTrijet);
    h_AfterStandardSelections_LeadingTrijet_Pt_VR       -> Fill(isGenuineTop_StandardSelections, LdgTrijet_MaxPt);
    h_AfterStandardSelections_LeadingTrijet_Eta_VR      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Eta);
    h_AfterStandardSelections_LeadingTrijet_Phi_VR      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Phi);
    h_AfterStandardSelections_LeadingTrijet_BJet_Pt_VR  -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_Pt);
    h_AfterStandardSelections_LeadingTrijet_BJet_CSV_VR -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_CSV);
    
    if (Debug){
      std::cout<<" "<<std::endl;
      std::cout<<" Top candidates passing BDT:  "<< topData.getSelectedTopsBJet().size()<< std::endl;
      std::cout<<" "<<std::endl;
    }    
       
    //=======================================================================
    // Final Selection
    //=======================================================================
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
    
    int selected_ldgTopIndex = getLeadingTopIndex(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop);

    Jet ldgSelTop_Jet1 =  topData.getAllTopsJet1().at(selected_ldgTopIndex);
    Jet ldgSelTop_Jet2 =  topData.getAllTopsJet2().at(selected_ldgTopIndex);
    Jet ldgSelTop_BJet =  topData.getAllTopsBJet().at(selected_ldgTopIndex);
    
    // Get 4-momentum of top (trijet)
    math::XYZTLorentzVector LdgSelTop_p4;
    LdgSelTop_p4 = ldgSelTop_Jet1.p4() + ldgSelTop_Jet2.p4() + ldgSelTop_BJet.p4();
    
    //DeltaR(mu, top)
    double dR_mu_selTop = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgSelTop_p4);
    
    // Do I need them?
    double LdgBDTTrijet_MaxPt    = LdgSelTop_p4.pt();
    double LdgBDTTrijet_Eta      = LdgSelTop_p4.eta();
    double LdgBDTTrijet_Phi      = LdgSelTop_p4.phi();
    double LdgBDTTrijet_BJet_Pt  = ldgSelTop_BJet.pt();
    double LdgBDTTrijet_BJet_CSV = ldgSelTop_BJet.bjetDiscriminator();
    double LdgBDTTrijet_MuDR     = dR_mu_selTop;
    
    if (0) std::cout<<LdgBDTTrijet_MaxPt<<LdgBDTTrijet_Eta<<LdgBDTTrijet_Phi<<LdgBDTTrijet_BJet_Pt<<LdgBDTTrijet_BJet_CSV<<LdgBDTTrijet_MuDR<<std::endl;  //Avoid warnings

    // Final Selection
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
			 
    if (Debug) std::cout<<"Leading BDT Trijet  pT="<<LdgBDTTrijet_MaxPt<<"  Eta="<<LdgBDTTrijet_Eta<<std::endl;
			 
    //=======================================================================
    // Fill Plots: After All Selections
    //=======================================================================
    h_AfterAllSelections_MET_VR         -> Fill(isGenuineTop_AllSelections, met);
    h_AfterAllSelections_HT_VR          -> Fill(isGenuineTop_AllSelections, jetData.HT());
    h_AfterAllSelections_NJets_VR       -> Fill(isGenuineTop_AllSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterAllSelections_Jets_Pt_VR   -> Fill(isGenuineTop_AllSelections, jet.pt()); 
      h_AfterAllSelections_Jets_Eta_VR  -> Fill(isGenuineTop_AllSelections, jet.eta());
      h_AfterAllSelections_Jets_Phi_VR  -> Fill(isGenuineTop_AllSelections, jet.phi());
    }
    h_AfterAllSelections_NBJets_VR      -> Fill(isGenuineTop_AllSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterAllSelections_BJets_Pt_VR  -> Fill(isGenuineTop_AllSelections, bjet.pt());
      h_AfterAllSelections_BJets_Eta_VR -> Fill(isGenuineTop_AllSelections, bjet.eta());
      h_AfterAllSelections_BJets_Phi_VR -> Fill(isGenuineTop_AllSelections, bjet.phi());
      h_AfterAllSelections_BJets_CSV_VR -> Fill(isGenuineTop_AllSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vSelectedTops_index.size(); i++){
      int index = vSelectedTops_index.at(i);
      Jet bjet = topData.getSelectedTopsBJet().at(index);
      Jet jet1 = topData.getSelectedTopsJet1().at(index);
      Jet jet2 = topData.getSelectedTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterAllSelections_Trijets_Pt_VR  -> Fill(isGenuineTop_AllSelections, Top_p4.Pt());
      h_AfterAllSelections_Trijets_Eta_VR -> Fill(isGenuineTop_AllSelections, Top_p4.Eta());
      h_AfterAllSelections_Trijets_Phi_VR -> Fill(isGenuineTop_AllSelections, Top_p4.Phi());
    }
    h_AfterAllSelections_Muon_Pt_VR     -> Fill(isGenuineTop_AllSelections, mu.pt());
    h_AfterAllSelections_Muon_Eta_VR    -> Fill(isGenuineTop_AllSelections, mu.eta());
    h_AfterAllSelections_Muon_Phi_VR    -> Fill(isGenuineTop_AllSelections, mu.phi());
    //h_AfterAllSelections_Muon_BJetMinDR -> Fill(isGenuineTop_AllSelections, dRmin_mu_bjet);
    h_AfterAllSelections_WMass_VR       -> Fill(isGenuineTop_AllSelections, MT);

    h_AfterAllSelections_LeadingTrijet_BDT_VR -> Fill(isGenuineTop_AllSelections, ldgTop_MVA);
    h_AfterAllSelections_DeltaPhi_MuMET_VR    -> Fill(isGenuineTop_AllSelections, deltaPhi_mu_met);
    
    if (cfg_PrelimTopMVACut.passedCut(ldgTop_MVA)){
      h_AfterAllSelections_Muon_LeadingTrijetDR_VR   -> Fill(isGenuineTop_AllSelections, DR_mu_LdgTrijet);
      h_AfterAllSelections_LeadingTrijet_Pt_VR       -> Fill(isGenuineTop_AllSelections, LdgTrijet_MaxPt);
      h_AfterAllSelections_LeadingTrijet_Eta_VR      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Eta);
      h_AfterAllSelections_LeadingTrijet_Phi_VR      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Phi);
      h_AfterAllSelections_LeadingTrijet_BJet_Pt_VR  -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_Pt);
      h_AfterAllSelections_LeadingTrijet_BJet_CSV_VR -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_CSV);
    }
    // We need another plot with the LeadingTrijet BDT
  } //Verification Region

  return;
  } //Baseline Analysis

void SystTopBDT::DoInvertedAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, Muon mu, const METSelection::Data& METData, 
				    const TopSelectionBDT::Data& topData, Jet BJet_LeptonicBr, bool searchForLeptonicTop){
  
  int Debug = 0;
  if (Debug) std::cout<<"===== Inverted Analysis"<<std::endl;
  double met    = METData.getMET().R();
  //double dRmin_mu_bjet = 999.999;
  // double dRmin_mu_top  = 999.999;
  // size_t nTops = topData.getAllTopsMVA().size();
  
  if (Debug) std::cout<<"1"<<std::endl;
  
  // Calculate transverse W mass
  double deltaPhi_mu_met = std::abs(ROOT::Math::VectorUtil::DeltaPhi(mu.p4(), METData.getMET()));
  double MT = sqrt(2*met*mu.pt()*(1-cos(deltaPhi_mu_met)));
    

  vector<int> vAllTops_index      = GetTopsIndex(topData, "all", BJet_LeptonicBr, mu, searchForLeptonicTop, true);
  vector<int> vSelectedTops_index = GetTopsIndex(topData, "selected", BJet_LeptonicBr, mu, searchForLeptonicTop, true);

  int ldgTopIndex = getLeadingTopIndex(topData, "all", mu, BJet_LeptonicBr, searchForLeptonicTop);
  int nTopCandidatesFarFromMuonPassBDT = vSelectedTops_index.size();

  /*
  // Search for Tops passing the BDT cut
  int nTopCandidatesFarFromMuonPassBDT = TopCandMultiplicity(topData, "selected", BJet_LeptonicBr, mu, searchForLeptonicTop, true);
  */

  Jet  ldgTop_Jet1 =  topData.getAllTopsJet1().at(ldgTopIndex);
  Jet  ldgTop_Jet2 =  topData.getAllTopsJet2().at(ldgTopIndex);
  Jet  ldgTop_BJet =  topData.getAllTopsBJet().at(ldgTopIndex);
  float ldgTop_MVA =  topData.getAllTopsMVA().at(ldgTopIndex);

  // Get 4-momentum of top (trijet)
  math::XYZTLorentzVector LdgTop_p4;
  LdgTop_p4 = ldgTop_Jet1.p4() + ldgTop_Jet2.p4() + ldgTop_BJet.p4();
  
  if (Debug) std::cout<<"2"<<std::endl;
  
  //DeltaR(mu, top)
  double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgTop_p4);
  
  double LdgTrijet_MaxPt    = LdgTop_p4.pt();
  double LdgTrijet_Eta      = LdgTop_p4.eta();
  double LdgTrijet_Phi      = LdgTop_p4.phi();
  double DR_mu_LdgTrijet    = dR_mu_top;
  double LdgTrijet_BJet_Pt  = ldgTop_BJet.pt();
  double LdgTrijet_BJet_CSV = ldgTop_BJet.bjetDiscriminator();
  
  if (Debug)
    {
      std::cout<<"leading top index = "<<ldgTopIndex<<std::endl;
      std::cout<<"leading top BDT = "  <<topData.getAllTopsMVA().at(ldgTopIndex)<<std::endl;
    }

  bool MuPass_Iso       = cfg_MiniIsoCut.passedCut(mu.effAreaMiniIso());
  bool MuPass_InvIso    = cfg_MiniIsoInvCut.passedCut(mu.effAreaMiniIso()) && !MuPass_Iso;

  //Matching
  const double twoSigma = 0.32;
  const double dRcut    = 0.4;
  bool isGenuineTop_StandardSelections = false;
  bool isGenuineTop_AllSelections = false;
  
  if (fEvent.isMC()){
    vector<genParticle> GenTops = GetGenParticles(fEvent.genparticles().getGenParticles(), 6);
    vector<genParticle> GenTops_BQuark, GenTops_LdgQuark, GenTops_SubldgQuark;
    for (auto& top: GenTops){
      vector<genParticle> quarks;
      genParticle bquark;
      bool foundB = false;
      for (size_t i=0; i<top.daughters().size(); i++){
        int dau_index = top.daughters().at(i);
        genParticle dau = fEvent.genparticles().getGenParticles()[dau_index];
        // B-Quark                                                                                                                                                                          
        if (std::abs(dau.pdgId()) ==  5){
          bquark = dau;
          foundB = true;
        }
        // W-Boson                                                                                                                                                                                                     
        if (std::abs(dau.pdgId()) == 24){
          // Get the last copy                                                                                                                                                                                         
          genParticle W = GetLastCopy(fEvent.genparticles().getGenParticles(), dau);
          // Find the decay products of W                                                                                                                                                                              
          for (size_t idau=0; idau<W.daughters().size(); idau++){
            int Wdau_index = W.daughters().at(idau);
            genParticle Wdau = fEvent.genparticles().getGenParticles()[Wdau_index];
            // Consider only quarks as decaying products                                                                                                                                                               
            if (std::abs(Wdau.pdgId()) > 5) continue;
	    quarks.push_back(Wdau);
          }
        }
      }
      //Soti: If top does not decay into W+b return
      if (!foundB) return;   
      // Fill vectors for b-quarks, leading and subleading quarks coming from tops 
      GenTops_BQuark.push_back(bquark);
      if (Debug) std::cout<<"W decay products = "<<quarks.size()<<std::endl;
      
      if (quarks.size() == 2){
	if (quarks.at(0).pt() > quarks.at(1).pt()) {
	  GenTops_LdgQuark.push_back(quarks.at(0));
	  GenTops_SubldgQuark.push_back(quarks.at(1));
	}
	else{
	  GenTops_LdgQuark.push_back(quarks.at(1));
	  GenTops_SubldgQuark.push_back(quarks.at(0));
	}
      }
    }
    
    //======= B jet matching (Loop over all Jets)                                                                                                                                                 
    int imatched =0;
    vector <Jet> MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet, BJetCand;
    vector <double> dRminB;
    for (size_t i=0; i<GenTops.size(); i++){
      genParticle BQuark      = GenTops_BQuark.at(i);
      Jet mcMatched_BJet;
      double dRmin  = 99999.9;
      for (auto& bjet: jetData.getSelectedJets()){
	double dR  = ROOT::Math::VectorUtil::DeltaR( bjet.p4(), BQuark.p4());
	double dPtOverPt = std::abs((bjet.pt() - BQuark.pt())/BQuark.pt());
	if (dR > dRcut)   continue;
	if (dR > dRmin)   continue;
	if (dPtOverPt > twoSigma) continue;
	dRmin  = dR;	
	mcMatched_BJet = bjet;
      }
      dRminB.push_back(dRmin);
	BJetCand.push_back(mcMatched_BJet);
    }
      
    //======= Dijet matching (Loop over all Jets)     
    for (size_t i=0; i<GenTops_LdgQuark.size(); i++){
      genParticle LdgQuark    = GenTops_LdgQuark.at(i);
      genParticle SubldgQuark = GenTops_SubldgQuark.at(i);
      Jet mcMatched_LdgJet, mcMatched_SubldgJet;
      double dR1min = 9999.9, dR2min = 9999.9;
      for (auto& jet: jetData.getSelectedJets()){
	bool same = false;
	for (size_t k=0; k<GenTops.size(); k++){
	  if (dRminB.at(k) <= dRcut){
	    if( areSameJets(jet,BJetCand.at(k))) same = true; //Skip the jets that are matched with bquarks   
	  }
	}
	if (same) continue;
	double dR1 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), LdgQuark.p4());
	double dR2 = ROOT::Math::VectorUtil::DeltaR(jet.p4(), SubldgQuark.p4());
	double dPtOverPt1 = std::abs((jet.pt() - LdgQuark.pt())/LdgQuark.pt());
	double dPtOverPt2 = std::abs( (jet.pt() - SubldgQuark.pt())/SubldgQuark.pt());
	if (std::min(dR1, dR2) > dRcut) continue;	
	if (dR1 < dR2)
	  {
	    if (dR1 < dR1min)
	      {
		if(dPtOverPt1 < twoSigma)
		  {
		    dR1min = dR1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	    else if (dR2 <= dRcut && dR2 < dR2min)
	      {
		if (dPtOverPt2 < twoSigma)
		  {
		    dR2min  = dR2;
		    mcMatched_SubldgJet = jet;
		  }
	      }
	  }
	else
	  {
	    if (dR2 < dR2min)
	      {
		if(dPtOverPt2 < twoSigma)
		    {
		      dR2min  = dR2;
		      mcMatched_SubldgJet = jet;
		    }
	      }
	    else if (dR1 <= dRcut && dR1 < dR1min)
	      {
		if (dPtOverPt1 < twoSigma)
		  {
		    dR1min  = dR1;
		    mcMatched_LdgJet = jet;
		  }
	      }
	  }
      }
      if (Debug) std::cout<<"MCtrue: size: "<<MCtrue_LdgJet.size()<<" "<<MCtrue_SubldgJet.size()<<" "<<MCtrue_Bjet.size()<<std::endl;
      //Genuine if all the top quarks are matched   
      genParticle top = GenTops.at(i);
      bool genuine = (dR1min<= dRcut && dR2min <= dRcut && dRminB.at(i) <= dRcut);
      if (genuine){
	imatched ++;
	MCtrue_LdgJet.push_back(mcMatched_LdgJet);
	MCtrue_SubldgJet.push_back(mcMatched_SubldgJet);
	MCtrue_Bjet.push_back(BJetCand.at(i));
      }
    }
    isGenuineTop_StandardSelections = IsGenuineTop(topData, "all", mu, BJet_LeptonicBr, searchForLeptonicTop, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
    isGenuineTop_AllSelections      = IsGenuineTop(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet);
    bool haveGenTop        = GenTops.size() > 0;
    bool haveMatchedTrijet = MCtrue_Bjet.size() > 0;
    
    if (0){
      if (haveGenTop && !haveMatchedTrijet) return;
    }
  }//if (fEvent.isMC())

  if (MuPass_Iso){
    
    if (Debug) std::cout<<"Control Region 1"<<std::endl;    
    
    //=======================================================================
    //SIGNAL REGION
    //=======================================================================
    h_AfterStandardSelections_MET_CR1         -> Fill(isGenuineTop_StandardSelections, met);
    h_AfterStandardSelections_HT_CR1          -> Fill(isGenuineTop_StandardSelections, jetData.HT());
    h_AfterStandardSelections_NJets_CR1       -> Fill(isGenuineTop_StandardSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterStandardSelections_Jets_Pt_CR1   -> Fill(isGenuineTop_StandardSelections, jet.pt()); 
      h_AfterStandardSelections_Jets_Eta_CR1  -> Fill(isGenuineTop_StandardSelections, jet.eta());
      h_AfterStandardSelections_Jets_Phi_CR1  -> Fill(isGenuineTop_StandardSelections, jet.phi());
    }
    h_AfterStandardSelections_NBJets_CR1      -> Fill(isGenuineTop_StandardSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterStandardSelections_BJets_Pt_CR1  -> Fill(isGenuineTop_StandardSelections, bjet.pt());
      h_AfterStandardSelections_BJets_Eta_CR1 -> Fill(isGenuineTop_StandardSelections, bjet.eta());
      h_AfterStandardSelections_BJets_Phi_CR1 -> Fill(isGenuineTop_StandardSelections, bjet.phi());
      h_AfterStandardSelections_BJets_CSV_CR1 -> Fill(isGenuineTop_StandardSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vAllTops_index.size(); i++){
      int index = vAllTops_index.at(i);
      Jet bjet = topData.getAllTopsBJet().at(index);
      Jet jet1 = topData.getAllTopsJet1().at(index);
      Jet jet2 = topData.getAllTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterStandardSelections_Trijets_Pt_CR1  -> Fill(isGenuineTop_StandardSelections, Top_p4.Pt());
      h_AfterStandardSelections_Trijets_Eta_CR1 -> Fill(isGenuineTop_StandardSelections, Top_p4.Eta());
      h_AfterStandardSelections_Trijets_Phi_CR1 -> Fill(isGenuineTop_StandardSelections, Top_p4.Phi());
    }
    h_AfterStandardSelections_Muon_Pt_CR1     -> Fill(isGenuineTop_StandardSelections, mu.pt());
    h_AfterStandardSelections_Muon_Eta_CR1    -> Fill(isGenuineTop_StandardSelections, mu.eta());
    h_AfterStandardSelections_Muon_Phi_CR1    -> Fill(isGenuineTop_StandardSelections, mu.phi());
    h_AfterStandardSelections_WMass_CR1      -> Fill(isGenuineTop_StandardSelections, MT);
    h_AfterStandardSelections_LeadingTrijet_BDT_CR1      -> Fill(isGenuineTop_StandardSelections, ldgTop_MVA);
    h_AfterStandardSelections_DeltaPhi_MuMET_CR1         -> Fill(isGenuineTop_StandardSelections, deltaPhi_mu_met);
    //h_AfterStandardSelections_Muon_BJetMinDR         -> Fill(isGenuineTop_StandardSelections, dRmin_mu_bjet);
    h_AfterStandardSelections_Muon_LeadingTrijetDR_CR1   -> Fill(isGenuineTop_StandardSelections, DR_mu_LdgTrijet);
    h_AfterStandardSelections_LeadingTrijet_Pt_CR1       -> Fill(isGenuineTop_StandardSelections, LdgTrijet_MaxPt);
    h_AfterStandardSelections_LeadingTrijet_Eta_CR1      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Eta);
    h_AfterStandardSelections_LeadingTrijet_Phi_CR1      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Phi);
    h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR1  -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_Pt);
    h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR1 -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_CSV);
    
    if (Debug){
      std::cout<<" "<<std::endl;
      std::cout<<" Top candidates passing BDT:  "<< topData.getSelectedTopsBJet().size()<< std::endl;
      std::cout<<" "<<std::endl;
    }    
       
    //=======================================================================
    // Final Selection
    //=======================================================================
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
    
    int selected_ldgTopIndex = getLeadingTopIndex(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop);

    Jet ldgSelTop_Jet1 =  topData.getAllTopsJet1().at(selected_ldgTopIndex);
    Jet ldgSelTop_Jet2 =  topData.getAllTopsJet2().at(selected_ldgTopIndex);
    Jet ldgSelTop_BJet =  topData.getAllTopsBJet().at(selected_ldgTopIndex);
    
    // Get 4-momentum of top (trijet)
    math::XYZTLorentzVector LdgSelTop_p4;
    LdgSelTop_p4 = ldgSelTop_Jet1.p4() + ldgSelTop_Jet2.p4() + ldgSelTop_BJet.p4();
    
    //DeltaR(mu, top)
    double dR_mu_selTop = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgSelTop_p4);
    
    // Do I need them?
    double LdgBDTTrijet_MaxPt    = LdgSelTop_p4.pt();
    double LdgBDTTrijet_Eta      = LdgSelTop_p4.eta();
    double LdgBDTTrijet_Phi      = LdgSelTop_p4.phi();
    double LdgBDTTrijet_BJet_Pt  = ldgSelTop_BJet.pt();
    double LdgBDTTrijet_BJet_CSV = ldgSelTop_BJet.bjetDiscriminator();
    double LdgBDTTrijet_MuDR     = dR_mu_selTop;
    
    if (0) std::cout<<LdgBDTTrijet_MaxPt<<LdgBDTTrijet_Eta<<LdgBDTTrijet_Phi<<LdgBDTTrijet_BJet_Pt<<LdgBDTTrijet_BJet_CSV<<LdgBDTTrijet_MuDR<<std::endl;  //Avoid warnings

    // Final Selection
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
			 
    if (Debug) std::cout<<"Leading BDT Trijet  pT="<<LdgBDTTrijet_MaxPt<<"  Eta="<<LdgBDTTrijet_Eta<<std::endl;
    //=======================================================================
    // Fill Plots: After All Selections
    //=======================================================================
    h_AfterAllSelections_MET_CR1         -> Fill(isGenuineTop_AllSelections, met);
    h_AfterAllSelections_HT_CR1          -> Fill(isGenuineTop_AllSelections, jetData.HT());
    h_AfterAllSelections_NJets_CR1       -> Fill(isGenuineTop_AllSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterAllSelections_Jets_Pt_CR1   -> Fill(isGenuineTop_AllSelections, jet.pt()); 
      h_AfterAllSelections_Jets_Eta_CR1  -> Fill(isGenuineTop_AllSelections, jet.eta());
      h_AfterAllSelections_Jets_Phi_CR1  -> Fill(isGenuineTop_AllSelections, jet.phi());
    }
    h_AfterAllSelections_NBJets_CR1      -> Fill(isGenuineTop_AllSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterAllSelections_BJets_Pt_CR1  -> Fill(isGenuineTop_AllSelections, bjet.pt());
      h_AfterAllSelections_BJets_Eta_CR1 -> Fill(isGenuineTop_AllSelections, bjet.eta());
      h_AfterAllSelections_BJets_Phi_CR1 -> Fill(isGenuineTop_AllSelections, bjet.phi());
      h_AfterAllSelections_BJets_CSV_CR1 -> Fill(isGenuineTop_AllSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vSelectedTops_index.size(); i++){
      int index = vSelectedTops_index.at(i);
      Jet bjet = topData.getSelectedTopsBJet().at(index);
      Jet jet1 = topData.getSelectedTopsJet1().at(index);
      Jet jet2 = topData.getSelectedTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterAllSelections_Trijets_Pt_CR1  -> Fill(isGenuineTop_AllSelections, Top_p4.Pt());
      h_AfterAllSelections_Trijets_Eta_CR1 -> Fill(isGenuineTop_AllSelections, Top_p4.Eta());
      h_AfterAllSelections_Trijets_Phi_CR1 -> Fill(isGenuineTop_AllSelections, Top_p4.Phi());
    }
    h_AfterAllSelections_Muon_Pt_CR1     -> Fill(isGenuineTop_AllSelections, mu.pt());
    h_AfterAllSelections_Muon_Eta_CR1    -> Fill(isGenuineTop_AllSelections, mu.eta());
    h_AfterAllSelections_Muon_Phi_CR1    -> Fill(isGenuineTop_AllSelections, mu.phi());
    //h_AfterAllSelections_Muon_BJetMinDR -> Fill(isGenuineTop_AllSelections, dRmin_mu_bjet);
    h_AfterAllSelections_WMass_CR1       -> Fill(isGenuineTop_AllSelections, MT);
    
    h_AfterAllSelections_LeadingTrijet_BDT_CR1 -> Fill(isGenuineTop_AllSelections, ldgTop_MVA);
    h_AfterAllSelections_DeltaPhi_MuMET_CR1    -> Fill(isGenuineTop_AllSelections, deltaPhi_mu_met);
    
    if (cfg_PrelimTopMVACut.passedCut(ldgTop_MVA)){
      h_AfterAllSelections_Muon_LeadingTrijetDR_CR1   -> Fill(isGenuineTop_AllSelections, DR_mu_LdgTrijet);
      h_AfterAllSelections_LeadingTrijet_Pt_CR1       -> Fill(isGenuineTop_AllSelections, LdgTrijet_MaxPt);
      h_AfterAllSelections_LeadingTrijet_Eta_CR1      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Eta);
      h_AfterAllSelections_LeadingTrijet_Phi_CR1      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Phi);
      h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR1  -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_Pt);
      h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR1 -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_CSV);
    }
    // We need another plot with the LeadingTrijet BDT
    if (Debug) std::cout<<"End of Control Region 1"<<std::endl;    
  } //cONTROL Region 1
  
  else if (MuPass_InvIso){
    //=======================================================================
    //CONTROL REGION 2
    //=======================================================================
    if (Debug) std::cout<<"Control Region 2"<<std::endl;

    h_AfterStandardSelections_MET_CR2         -> Fill(isGenuineTop_StandardSelections, met);
    h_AfterStandardSelections_HT_CR2          -> Fill(isGenuineTop_StandardSelections, jetData.HT());
    h_AfterStandardSelections_NJets_CR2       -> Fill(isGenuineTop_StandardSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterStandardSelections_Jets_Pt_CR2   -> Fill(isGenuineTop_StandardSelections, jet.pt()); 
      h_AfterStandardSelections_Jets_Eta_CR2  -> Fill(isGenuineTop_StandardSelections, jet.eta());
      h_AfterStandardSelections_Jets_Phi_CR2  -> Fill(isGenuineTop_StandardSelections, jet.phi());
    }
    h_AfterStandardSelections_NBJets_CR2      -> Fill(isGenuineTop_StandardSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterStandardSelections_BJets_Pt_CR2  -> Fill(isGenuineTop_StandardSelections, bjet.pt());
      h_AfterStandardSelections_BJets_Eta_CR2 -> Fill(isGenuineTop_StandardSelections, bjet.eta());
      h_AfterStandardSelections_BJets_Phi_CR2 -> Fill(isGenuineTop_StandardSelections, bjet.phi());
      h_AfterStandardSelections_BJets_CSV_CR2 -> Fill(isGenuineTop_StandardSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vAllTops_index.size(); i++){
      int index = vAllTops_index.at(i);
      Jet bjet = topData.getAllTopsBJet().at(index);
      Jet jet1 = topData.getAllTopsJet1().at(index);
      Jet jet2 = topData.getAllTopsJet2().at(index);
      // Get 4-momentum of top (trijet)     
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterStandardSelections_Trijets_Pt_CR2  -> Fill(isGenuineTop_StandardSelections, Top_p4.Pt());
      h_AfterStandardSelections_Trijets_Eta_CR2 -> Fill(isGenuineTop_StandardSelections, Top_p4.Eta());
      h_AfterStandardSelections_Trijets_Phi_CR2 -> Fill(isGenuineTop_StandardSelections, Top_p4.Phi());
    }
    h_AfterStandardSelections_Muon_Pt_CR2     -> Fill(isGenuineTop_StandardSelections, mu.pt());
    h_AfterStandardSelections_Muon_Eta_CR2    -> Fill(isGenuineTop_StandardSelections, mu.eta());
    h_AfterStandardSelections_Muon_Phi_CR2    -> Fill(isGenuineTop_StandardSelections, mu.phi());
    h_AfterStandardSelections_WMass_CR2      -> Fill(isGenuineTop_StandardSelections, MT);
    h_AfterStandardSelections_LeadingTrijet_BDT_CR2      -> Fill(isGenuineTop_StandardSelections, ldgTop_MVA);
    h_AfterStandardSelections_DeltaPhi_MuMET_CR2         -> Fill(isGenuineTop_StandardSelections, deltaPhi_mu_met);
    //h_AfterStandardSelections_Muon_BJetMinDR         -> Fill(isGenuineTop_StandardSelections, dRmin_mu_bjet);
    h_AfterStandardSelections_Muon_LeadingTrijetDR_CR2   -> Fill(isGenuineTop_StandardSelections, DR_mu_LdgTrijet);
    h_AfterStandardSelections_LeadingTrijet_Pt_CR2       -> Fill(isGenuineTop_StandardSelections, LdgTrijet_MaxPt);
    h_AfterStandardSelections_LeadingTrijet_Eta_CR2      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Eta);
    h_AfterStandardSelections_LeadingTrijet_Phi_CR2      -> Fill(isGenuineTop_StandardSelections, LdgTrijet_Phi);
    h_AfterStandardSelections_LeadingTrijet_BJet_Pt_CR2  -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_Pt);
    h_AfterStandardSelections_LeadingTrijet_BJet_CSV_CR2 -> Fill(isGenuineTop_StandardSelections, LdgTrijet_BJet_CSV);
    
    if (Debug){
      std::cout<<" "<<std::endl;
      std::cout<<" Top candidates passing BDT:  "<< topData.getSelectedTopsBJet().size()<< std::endl;
      std::cout<<" "<<std::endl;
    }    
       
    //=======================================================================
    // Final Selection
    //=======================================================================
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
    
    int selected_ldgTopIndex = getLeadingTopIndex(topData, "selected", mu, BJet_LeptonicBr, searchForLeptonicTop);

    Jet ldgSelTop_Jet1 =  topData.getAllTopsJet1().at(selected_ldgTopIndex);
    Jet ldgSelTop_Jet2 =  topData.getAllTopsJet2().at(selected_ldgTopIndex);
    Jet ldgSelTop_BJet =  topData.getAllTopsBJet().at(selected_ldgTopIndex);
    
    // Get 4-momentum of top (trijet)
    math::XYZTLorentzVector LdgSelTop_p4;
    LdgSelTop_p4 = ldgSelTop_Jet1.p4() + ldgSelTop_Jet2.p4() + ldgSelTop_BJet.p4();
    
    //DeltaR(mu, top)
    double dR_mu_selTop = ROOT::Math::VectorUtil::DeltaR(mu.p4(), LdgSelTop_p4);
    
    // Do I need them?
    double LdgBDTTrijet_MaxPt    = LdgSelTop_p4.pt();
    double LdgBDTTrijet_Eta      = LdgSelTop_p4.eta();
    double LdgBDTTrijet_Phi      = LdgSelTop_p4.phi();
    double LdgBDTTrijet_BJet_Pt  = ldgSelTop_BJet.pt();
    double LdgBDTTrijet_BJet_CSV = ldgSelTop_BJet.bjetDiscriminator();
    double LdgBDTTrijet_MuDR     = dR_mu_selTop;
    
    if (0) std::cout<<LdgBDTTrijet_MaxPt<<LdgBDTTrijet_Eta<<LdgBDTTrijet_Phi<<LdgBDTTrijet_BJet_Pt<<LdgBDTTrijet_BJet_CSV<<LdgBDTTrijet_MuDR<<std::endl;  //Avoid warnings

    // Final Selection
    if (nTopCandidatesFarFromMuonPassBDT < 1) return;
			 
    if (Debug) std::cout<<"Leading BDT Trijet  pT="<<LdgBDTTrijet_MaxPt<<"  Eta="<<LdgBDTTrijet_Eta<<std::endl;
			 
    //=======================================================================
    // Fill Plots: After All Selections
    //=======================================================================
    h_AfterAllSelections_MET_CR2         -> Fill(isGenuineTop_AllSelections, met);
    h_AfterAllSelections_HT_CR2          -> Fill(isGenuineTop_AllSelections, jetData.HT());
    h_AfterAllSelections_NJets_CR2       -> Fill(isGenuineTop_AllSelections, jetData.getSelectedJets().size());
    for (auto& jet: jetData.getSelectedJets()){
      h_AfterAllSelections_Jets_Pt_CR2   -> Fill(isGenuineTop_AllSelections, jet.pt()); 
      h_AfterAllSelections_Jets_Eta_CR2  -> Fill(isGenuineTop_AllSelections, jet.eta());
      h_AfterAllSelections_Jets_Phi_CR2  -> Fill(isGenuineTop_AllSelections, jet.phi());
    }
    h_AfterAllSelections_NBJets_CR2      -> Fill(isGenuineTop_AllSelections, bjetData.getSelectedBJets().size());
    for (auto& bjet: bjetData.getSelectedBJets()){
      h_AfterAllSelections_BJets_Pt_CR2  -> Fill(isGenuineTop_AllSelections, bjet.pt());
      h_AfterAllSelections_BJets_Eta_CR2 -> Fill(isGenuineTop_AllSelections, bjet.eta());
      h_AfterAllSelections_BJets_Phi_CR2 -> Fill(isGenuineTop_AllSelections, bjet.phi());
      h_AfterAllSelections_BJets_CSV_CR2 -> Fill(isGenuineTop_AllSelections, bjet.bjetDiscriminator());
    }
    for (size_t i=0; i < vSelectedTops_index.size(); i++){
      int index = vSelectedTops_index.at(i);
      Jet bjet = topData.getSelectedTopsBJet().at(index);
      Jet jet1 = topData.getSelectedTopsJet1().at(index);
      Jet jet2 = topData.getSelectedTopsJet2().at(index);
      // Get 4-momentum of top (trijet)                                                                                                                                                                                 
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      h_AfterAllSelections_Trijets_Pt_CR2  -> Fill(isGenuineTop_AllSelections, Top_p4.Pt());
      h_AfterAllSelections_Trijets_Eta_CR2 -> Fill(isGenuineTop_AllSelections, Top_p4.Eta());
      h_AfterAllSelections_Trijets_Phi_CR2 -> Fill(isGenuineTop_AllSelections, Top_p4.Phi());
    }
    h_AfterAllSelections_Muon_Pt_CR2     -> Fill(isGenuineTop_AllSelections, mu.pt());
    h_AfterAllSelections_Muon_Eta_CR2    -> Fill(isGenuineTop_AllSelections, mu.eta());
    h_AfterAllSelections_Muon_Phi_CR2    -> Fill(isGenuineTop_AllSelections, mu.phi());
    //h_AfterAllSelections_Muon_BJetMinDR -> Fill(isGenuineTop_AllSelections, dRmin_mu_bjet);
    h_AfterAllSelections_WMass_CR2       -> Fill(isGenuineTop_AllSelections, MT);
    
    h_AfterAllSelections_LeadingTrijet_BDT_CR2 -> Fill(isGenuineTop_AllSelections, ldgTop_MVA);
    h_AfterAllSelections_DeltaPhi_MuMET_CR2    -> Fill(isGenuineTop_AllSelections, deltaPhi_mu_met);
    
    if (cfg_PrelimTopMVACut.passedCut(ldgTop_MVA)){
      h_AfterAllSelections_Muon_LeadingTrijetDR_CR2   -> Fill(isGenuineTop_AllSelections, DR_mu_LdgTrijet);
      h_AfterAllSelections_LeadingTrijet_Pt_CR2       -> Fill(isGenuineTop_AllSelections, LdgTrijet_MaxPt);
      h_AfterAllSelections_LeadingTrijet_Eta_CR2      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Eta);
      h_AfterAllSelections_LeadingTrijet_Phi_CR2      -> Fill(isGenuineTop_AllSelections, LdgTrijet_Phi);
      h_AfterAllSelections_LeadingTrijet_BJet_Pt_CR2  -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_Pt);
      h_AfterAllSelections_LeadingTrijet_BJet_CSV_CR2 -> Fill(isGenuineTop_AllSelections, LdgTrijet_BJet_CSV);
    }
    // We need another plot with the LeadingTrijet BDT
  } //Control Region 2

  return;
} //Inverted Analysis


int SystTopBDT::getLeadingTopIndex(const TopSelectionBDT::Data& topData, string topType, Muon mu, Jet BJet_LeptonicBr, bool searchForLeptonicTop){
  //double dRmin_mu_top = 999.999;
  double LdgTrijet_MaxPt = -999.99;
  int LdgTrijet_Index = -1;
  size_t nTops = 0;

  if (topType == "all") nTops = topData.getAllTopsMVA().size();
  else if (topType == "selected") nTops = topData.getSelectedTopsMVA().size();
  else return -1;
  
  for (size_t i=0; i < nTops; i++)
    {
      Jet bjet, jet1, jet2;
      if (topType == "all")
	{
	  bjet = topData.getAllTopsBJet().at(i);
	  jet1 = topData.getAllTopsJet1().at(i);
	  jet2 = topData.getAllTopsJet2().at(i);
	}
      else
	{
	  bjet = topData.getSelectedTopsBJet().at(i);
	  jet1 = topData.getSelectedTopsJet1().at(i);
	  jet2 = topData.getSelectedTopsJet2().at(i);
	}

      if (searchForLeptonicTop)
	{
	  // Skip jet given to the leptonic branch
	  if (areSameJets(bjet, BJet_LeptonicBr)) continue;
	  if (areSameJets(jet1, BJet_LeptonicBr)) continue;		  
	  if (areSameJets(jet2, BJet_LeptonicBr)) continue;
	}
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      //DeltaR(mu, top)
      double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), Top_p4);
      
      // Find min and max DR(mu, top candidate)
      //if (dR_mu_top < dRmin_mu_top) dRmin_mu_top = dR_mu_top;

      // Consider only top candidates that are far from the muon (back-to-back)
      if (dR_mu_top < 2.0) continue;	      
      if (Top_p4.pt() < LdgTrijet_MaxPt) continue;
       	LdgTrijet_MaxPt = Top_p4.pt();
	LdgTrijet_Index = i;
    }
  return LdgTrijet_Index;
}

/*
int SystTopBDT::TopCandMultiplicity( const TopSelectionBDT::Data& topData, string topType, Jet BJet_LeptonicBr, Muon mu, bool searchForLeptonicTop, bool askTopFarFromMu){

  double dRmin_mu_top = 999.999;

  int nTopCandidates = 0;
  int nTopCandidatesFarFromMuon = 0;
  size_t nTops = -1;

  if (topType == "all") nTops = topData.getAllTopsMVA().size();
  else if (topType == "selected") nTops = topData.getSelectedTopsMVA().size();
  else return -1;
  if (nTops < 1 ) return -1;
  for (size_t i=0; i < nTops; i++)
    {
      Jet bjet, jet1, jet2;
      if (topType == "all")
	{
	  bjet = topData.getAllTopsBJet().at(i);
	  jet1 = topData.getAllTopsJet1().at(i);
	  jet2 = topData.getAllTopsJet2().at(i);
	}
      else
	{
	  bjet = topData.getSelectedTopsBJet().at(i);
	  jet1 = topData.getSelectedTopsJet1().at(i);
	  jet2 = topData.getSelectedTopsJet2().at(i);
	}
      
      if (searchForLeptonicTop)
	{
	  // Skip jet given to the leptonic branch
	  if (areSameJets(bjet, BJet_LeptonicBr)) continue;
	  if (areSameJets(jet1, BJet_LeptonicBr)) continue;		  
	  if (areSameJets(jet2, BJet_LeptonicBr)) continue;
	}
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      //DeltaR(mu, top)
      double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), Top_p4);
      
      // Find min and max DR(mu, top candidate)
      if (dR_mu_top < dRmin_mu_top) dRmin_mu_top = dR_mu_top;
      
      nTopCandidates++;
      
      // Consider only top candidates that are far from the muon (back-to-back)
      if (dR_mu_top < 2.0) continue;	      
      
      nTopCandidatesFarFromMuon++;
	      
      if (0) std::cout<<"Top pT="<<Top_p4.pt()<<"  jet 1="<<jet1.index()<<"  jet2="<<jet2.index()<<"  bjet="<<bjet.index()<<"   ΔR (μ, top candidate ) = "<<dR_mu_top<<std::endl;
    }

  if (!askTopFarFromMu) return nTopCandidates;
  return nTopCandidatesFarFromMuon;
}
*/
bool SystTopBDT::IsGenuineTop(const TopSelectionBDT::Data& topData, string topType, Muon mu, Jet BJet_LeptonicBr, bool searchForLeptonicTop,
			      const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet){
  //double dRmin_mu_top = 999.999;
  size_t nTops = 0;
  
  if (min(MCtrue_Bjet.size(), min(MCtrue_LdgJet.size(), MCtrue_SubldgJet.size())) == 0) return false;
  if (topType == "all") nTops = topData.getAllTopsMVA().size();
  else if (topType == "selected") nTops = topData.getSelectedTopsMVA().size();
  else return false;
  
  for (size_t i=0; i < nTops; i++)
    {
      Jet bjet, jet1, jet2;
      if (topType == "all")
	{
	  bjet = topData.getAllTopsBJet().at(i);
	  jet1 = topData.getAllTopsJet1().at(i);
	  jet2 = topData.getAllTopsJet2().at(i);
	}
      else
	{
	  bjet = topData.getSelectedTopsBJet().at(i);
	  jet1 = topData.getSelectedTopsJet1().at(i);
	  jet2 = topData.getSelectedTopsJet2().at(i);
	}

      if (searchForLeptonicTop)
	{
	  // Skip jet given to the leptonic branch
	  if (areSameJets(bjet, BJet_LeptonicBr)) continue;
	  if (areSameJets(jet1, BJet_LeptonicBr)) continue;		  
	  if (areSameJets(jet2, BJet_LeptonicBr)) continue;
	}
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      //DeltaR(mu, top)
      double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), Top_p4);
      
      // Consider only top candidates that are far from the muon (back-to-back)
      if (dR_mu_top < 2.0) continue;	      
      if (isRealMVATop(jet1, jet2, bjet, MCtrue_LdgJet, MCtrue_SubldgJet, MCtrue_Bjet)) return true;
    }
  return false;
}

bool SystTopBDT::isRealMVATop(const Jet& trijetJet1, const Jet& trijetJet2, const Jet& trijetBJet, 
			      const std::vector<Jet>& MCtrue_LdgJet,  const std::vector<Jet>& MCtrue_SubldgJet, const std::vector<Jet>& MCtrue_Bjet){

  for (size_t k=0; k<MCtrue_Bjet.size(); k++){
    bool same1 = areSameJets(trijetJet1, MCtrue_LdgJet.at(k))       && areSameJets(trijetJet2, MCtrue_SubldgJet.at(k)) && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    bool same2 = areSameJets(trijetJet1, MCtrue_SubldgJet.at(k))    && areSameJets(trijetJet2, MCtrue_LdgJet.at(k))    && areSameJets(trijetBJet,  MCtrue_Bjet.at(k));
    if (same1 || same2) return true;
  }
  return false;
}

double SystTopBDT::DeltaEta(double eta1, double eta2)
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  double deltaEta = fabs ( eta1 - eta2 );
  return deltaEta;
}

double SystTopBDT::DeltaPhi(double phi1, double phi2)
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  double PI = 3.14159265;
  double result = phi1 - phi2;
  while (result > PI) result -= 2*PI;
  while (result <= -PI) result += 2*PI;
  return result;
}

double SystTopBDT::DeltaR(double eta1, double eta2,
			  double phi1, double phi2)
{
  double dEta = DeltaEta(eta1, eta2);
  double dPhi = DeltaPhi(phi1, phi2);
  double dR = TMath::Sqrt(TMath::Power(dEta,2)+TMath::Power(dPhi,2));
  return dR;
}

bool SystTopBDT::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}


vector<genParticle> SystTopBDT::GetGenParticles(const vector<genParticle> genParticles, const int pdgId)
{
  std::vector<genParticle> particles;
  // For-loop: All genParticles
  for (auto& p: genParticles){
    // Find last copy of a given particle
    if (!p.isLastCopy()) continue;
    // Consider only particles 
    if (std::abs(p.pdgId()) != pdgId) continue;
    // Save this particle 
    particles.push_back(p);
  }
  return particles;
}

const genParticle SystTopBDT::GetLastCopy(const vector<genParticle> genParticles, const genParticle &p){
  int gen_pdgId = p.pdgId();
  for (size_t i=0; i<p.daughters().size(); i++){
    const genParticle genDau = genParticles[p.daughters().at(i)];
    int genDau_pdgId   = genDau.pdgId();
    if (gen_pdgId == genDau_pdgId)  return GetLastCopy(genParticles, genDau);
  }
  return p;
}


vector <int> SystTopBDT::GetTopsIndex( const TopSelectionBDT::Data& topData, string topType, Jet BJet_LeptonicBr, Muon mu, bool searchForLeptonicTop, bool askTopFarFromMu){
  double dRmin_mu_top = 999.999;

  size_t nTops = -1;
  vector <int> vTops;
  if (topType == "all") nTops = topData.getAllTopsMVA().size();
  else if (topType == "selected") nTops = topData.getSelectedTopsMVA().size();
  else return vTops;
  if (nTops < 1 ) return vTops;
  for (size_t i=0; i < nTops; i++)
    {
      Jet bjet, jet1, jet2;
      if (topType == "all")
	{
	  bjet = topData.getAllTopsBJet().at(i);
	  jet1 = topData.getAllTopsJet1().at(i);
	  jet2 = topData.getAllTopsJet2().at(i);
	}
      else
	{
	  bjet = topData.getSelectedTopsBJet().at(i);
	  jet1 = topData.getSelectedTopsJet1().at(i);
	  jet2 = topData.getSelectedTopsJet2().at(i);
	}
      
      if (searchForLeptonicTop)
	{
	  // Skip jet given to the leptonic branch
	  if (areSameJets(bjet, BJet_LeptonicBr)) continue;
	  if (areSameJets(jet1, BJet_LeptonicBr)) continue;		  
	  if (areSameJets(jet2, BJet_LeptonicBr)) continue;
	}
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      //DeltaR(mu, top)
      double dR_mu_top = ROOT::Math::VectorUtil::DeltaR(mu.p4(), Top_p4);
      
      // Find min and max DR(mu, top candidate)
      if (dR_mu_top < dRmin_mu_top) dRmin_mu_top = dR_mu_top;
      
      // Consider only top candidates that are far from the muon (back-to-back)
      if (dR_mu_top < 2.0) continue;	      
      vTops.push_back(i);
    }
  return vTops;
}
