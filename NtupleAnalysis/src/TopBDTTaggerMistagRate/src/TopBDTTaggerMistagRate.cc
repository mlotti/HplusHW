// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"
//TopBDTTaggerMistagRate
class TopBDTTaggerMistagRate: public BaseSelector {
public:
  explicit TopBDTTaggerMistagRate(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TopBDTTaggerMistagRate() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
  //Check if jets are same
  bool areSameJets(const Jet& jet1, const Jet& jet2);
  //Get leading in pt jet
  Jet GetLdgJet(const std::vector<Jet>& Jets);
  //Get leading in pt trijet
  int GetLdgTopIndex(const TopSelectionBDT::Data& topData, vector<int> TopCandIndex);
  // Check if Top candidate passes Top selection
  bool PassBDT(const TopSelectionBDT::Data& topData, int ldgTop_index);

private:
  // Input parameters
  // const DirectionalCut<double> cfg_PrelimTopMVACut;
  // const std::string            cfg_LdgTopDefinition;
  const DirectionalCut<double> cfg_MVACut;
  const unsigned int cfg_NBjets;
  const std::vector<float> cfg_JetPtCuts; 

  // Common plots
  CommonPlots fCommonPlots;

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count              cVertexSelection;
  ElectronSelection  fElectronSelection;
  MuonSelection      fMuonSelection;
  TauSelection       fTauSelection;
  JetSelection       fJetSelection;
  BJetSelection      fBJetSelection;
  Count              cBTaggingSFCounter;
  METSelection       fMETSelection;
  TopSelectionBDT    fTopSelection;
  Count cSelected;
    
  // Non-common histograms
  //After Standard Selections
  WrappedTH1 *h_AfterStandardSelections_LdgTop_Pt;
  WrappedTH1 *h_AfterStandardSelections_LdgTop_Mass;
  WrappedTH1 *h_AfterStandardSelections_Tops_Pt;
  WrappedTH1 *h_AfterStandardSelections_Jet1_Pt;
  WrappedTH1 *h_AfterStandardSelections_Jet2_Pt;
  WrappedTH1 *h_AfterStandardSelections_Jet3_Pt;
  WrappedTH1 *h_AfterStandardSelections_Bjet1_Pt;
  WrappedTH1 *h_AfterStandardSelections_Bjet2_Pt;
  WrappedTH1 *h_AfterStandardSelections_MET;
  WrappedTH1 *h_AfterStandardSelections_HT;
  WrappedTH1 *h_AfterStandardSelections_JetMult;
  WrappedTH1 *h_AfterStandardSelections_BjetMult;

  WrappedTH1 *h_AfterStandardSelection_DeltaR_ldgJet_Top;
  WrappedTH1 *h_AfterStandardSelection_DeltaR_fatJets_Top;

  //After All Selections
  WrappedTH1 *h_AfterAllSelections_LdgTop_Pt;
  WrappedTH1 *h_AfterAllSelections_LdgTop_Mass;
  WrappedTH1 *h_AfterAllSelections_Tops_Pt;
  WrappedTH1 *h_AfterAllSelections_Jet1_Pt;
  WrappedTH1 *h_AfterAllSelections_Jet2_Pt;
  WrappedTH1 *h_AfterAllSelections_Jet3_Pt;
  WrappedTH1 *h_AfterAllSelections_Bjet1_Pt;
  WrappedTH1 *h_AfterAllSelections_Bjet2_Pt;
  WrappedTH1 *h_AfterAllSelections_MET;
  WrappedTH1 *h_AfterAllSelections_HT;
  WrappedTH1 *h_AfterAllSelections_JetMult;
  WrappedTH1 *h_AfterAllSelections_BjetMult;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TopBDTTaggerMistagRate);

TopBDTTaggerMistagRate::TopBDTTaggerMistagRate(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    // cfg_PrelimTopMVACut(config, "FakeBTopSelectionBDT.MVACut"),
    // cfg_LdgTopDefinition(config.getParameter<std::string>("FakeBTopSelectionBDT.LdgTopDefinition")),
    cfg_MVACut(config, "TopSelectionBDT.MVACut"),
    cfg_NBjets(config.getParameter<unsigned int>("BJetSelection.numberOfBJetsCutValue")),
    cfg_JetPtCuts(config.getParameter<std::vector<float>>("JetSelection.jetPtCuts")),
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
    // fQGLRSelection(config.getParameter<ParameterSet>("QGLRSelection")),// fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    // fFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void TopBDTTaggerMistagRate::book(TDirectory *dir) {

  if (0) std::cout << "=== TopBDTTaggerMistagRate::book()" << std::endl;
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
  // fQGLRSelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  // fFatJetSelection.bookHistograms(dir);

  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = 2*fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = 2*fCommonPlots.getPtBinSettings().max();

  const int nTopMassBins    = fCommonPlots.getTopMassBinSettings().bins();
  const float fTopMassMin   = fCommonPlots.getTopMassBinSettings().min();
  const float fTopMassMax   = fCommonPlots.getTopMassBinSettings().max();

  const int nMetBins  = fCommonPlots.getMetBinSettings().bins();
  const float fMetMin = fCommonPlots.getMetBinSettings().min();
  const float fMetMax = 2*fCommonPlots.getMetBinSettings().max();

  const int nHtBins  = fCommonPlots.getHtBinSettings().bins();
  const float fHtMin = fCommonPlots.getHtBinSettings().min();
  const float fHtMax = fCommonPlots.getHtBinSettings().max();

  TDirectory* dirTH1 = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "TopBDTTagger_QCDMistagRate");
  // Book non-common histograms
  //After Standard Selections
  h_AfterStandardSelections_LdgTop_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_LdgTop_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Tops_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Tops_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_LdgTop_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_LdgTop_Mass", ";m_{jjb} (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  h_AfterStandardSelections_Jet1_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Jet1_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jet2_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Jet2_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Jet3_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Jet3_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Bjet1_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Bjet1_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterStandardSelections_Bjet2_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_Bjet2_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  h_AfterStandardSelections_MET         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_MET", ";E_{T,missing} GeV", nMetBins, fMetMin, fMetMax);         
  h_AfterStandardSelections_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_HT", ";H_{T} GeV", nHtBins, fHtMin, fHtMax);
  h_AfterStandardSelections_JetMult     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_JetMult", ";", 20, 0, 20);
  h_AfterStandardSelections_BjetMult    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelections_BjetMult", ";", 20, 0, 20);

  h_AfterStandardSelection_DeltaR_ldgJet_Top  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelection_DeltaR_ldgJet_Top", ";#Delta R", 60, 0, 6.0);
  h_AfterStandardSelection_DeltaR_fatJets_Top = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterStandardSelection_DeltaR_fatJets_Top", ";#Delta R", 60, 0, 6.0);



  //After All Selection
  h_AfterAllSelections_LdgTop_Pt      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_LdgTop_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Tops_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Tops_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_LdgTop_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_LdgTop_Mass", ";m_{jjb} (GeV/c^{2})", nTopMassBins, fTopMassMin, fTopMassMax);
  h_AfterAllSelections_Jet1_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Jet1_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jet2_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Jet2_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Jet3_Pt     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Jet3_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Bjet1_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Bjet1_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  h_AfterAllSelections_Bjet2_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_Bjet2_Pt", ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);

  h_AfterAllSelections_MET         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_MET", ";E_{T,missing} GeV", nMetBins, fMetMin, fMetMax);         
  h_AfterAllSelections_HT          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_HT", ";H_{T} GeV", nHtBins, fHtMin, fHtMax);
  h_AfterAllSelections_JetMult     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_JetMult", ";", 20, 0, 20);
  h_AfterAllSelections_BjetMult    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dirTH1, "AfterAllSelections_BjetMult", ";", 20, 0, 20);

  return;
}


void TopBDTTaggerMistagRate::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}

bool TopBDTTaggerMistagRate::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}

Jet TopBDTTaggerMistagRate::GetLdgJet(const std::vector<Jet>& Jets){

  double maxPt = -999.99;
  Jet LdgJet;
  for (auto& jet: Jets){
    if (jet.pt() < maxPt) continue;
    maxPt = jet.pt();
    LdgJet = jet;
  }

  return LdgJet;
}

int TopBDTTaggerMistagRate::GetLdgTopIndex(const TopSelectionBDT::Data& topData, vector<int> TopCandIndex){
  size_t nTops = TopCandIndex.size();
  double maxPt =  -999.99;
  int ldgTopIndex = -1;
  for (size_t i=0; i < nTops; i++){
    int index = TopCandIndex.at(i);
    Jet bjet = topData.getAllTopsBJet().at(index);
    Jet jet1 = topData.getAllTopsJet1().at(index);
    Jet jet2 = topData.getAllTopsJet2().at(index);

    // Get 4-momentum of top (trijet)
    math::XYZTLorentzVector Top_p4;
    Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
    if (Top_p4.Pt() < maxPt) continue;
    maxPt = Top_p4.Pt();
    ldgTopIndex = index;
  }

  return ldgTopIndex;
}


bool TopBDTTaggerMistagRate::PassBDT(const TopSelectionBDT::Data& topData, int ldgTop_index){

  Jet ldgTop_Jet1 = topData.getAllTopsJet1().at(ldgTop_index);
  Jet ldgTop_Jet2 = topData.getAllTopsJet2().at(ldgTop_index);
  Jet ldgTop_BJet = topData.getAllTopsBJet().at(ldgTop_index);

  bool passBDT = false;

  for (size_t i = 0; i < topData.getSelectedTopsBJet().size(); i++){
    Jet bjet = topData.getSelectedTopsBJet().at(i);
    Jet jet1 = topData.getSelectedTopsJet1().at(i);
    Jet jet2 = topData.getSelectedTopsJet2().at(i);

    if (areSameJets(ldgTop_Jet1, jet1) && areSameJets(ldgTop_Jet2, jet2) && areSameJets(ldgTop_BJet, bjet)) passBDT = true;
  }
  return passBDT;
}
void TopBDTTaggerMistagRate::process(Long64_t entry) {

  // Sanity check
  // if (cfg_LdgTopDefinition != "MVA" &&  cfg_LdgTopDefinition != "Pt")
  //   {
  //     throw hplus::Exception("config") << "Unsupported method of defining the leading top (=" << cfg_LdgTopDefinition << "). Please select from \"MVA\" and \"Pt\".";
  //   }

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  //================================================================================================   
  // 1) Apply trigger 
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
  // 5) Muon veto (Fully hadronic + orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 7) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
 
  //================================================================================================  
  // 8) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
  // fCommonPlots.fillControlPlotsAfterBJetSelection(fEvent, bjetData);

  //================================================================================================  
  // 9) BJet SF  
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
  if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);

  //Standard selections

  double met = METData.getMET().R();
  vector<int> TopCandIndex;

  //Debug
  if (0) std::cout<<"At least "<<cfg_NBjets<<" bjets per event"<<std::endl;
  
  //If 2 jet are required: form the top candidates excluding the leadin in pt jet.
  if (cfg_JetPtCuts.at(0) == 100){
    
    if (0) std::cout<<"ldg top analysis"<<std::endl;
    Jet Ldgjet = GetLdgJet(jetData.getSelectedJets());
    
    for (size_t i=0; i < topData.getAllTopsBJet().size(); i++){
      Jet bjet = topData.getAllTopsBJet().at(i);
      Jet jet1 = topData.getAllTopsJet1().at(i);
      Jet jet2 = topData.getAllTopsJet2().at(i);
      
      //Exclude leading in pt jet
      if (areSameJets(Ldgjet, bjet) || areSameJets(Ldgjet, jet1) || areSameJets(Ldgjet, jet2)) continue;
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      //DeltaR(ldgJet, top)
      double dR_ldgJet_Top = ROOT::Math::VectorUtil::DeltaR(Ldgjet.p4(), Top_p4);
      
      h_AfterStandardSelection_DeltaR_ldgJet_Top -> Fill(dR_ldgJet_Top);
      //Skip if DeltaR(ldgJet, top) < 2.0
      if (dR_ldgJet_Top < 2.0) continue;
      TopCandIndex.push_back(i);
      
      //Pt of all top candidates
      h_AfterStandardSelections_Tops_Pt  -> Fill(Top_p4.Pt());
      
      float mva = topData.getAllTopsMVA().at(i);
      //Pt of all top candidates passing the BDT cut
      if (cfg_MVACut.passedCut(mva)) h_AfterAllSelections_Tops_Pt  -> Fill(Top_p4.Pt());
    }
  }
  
  else if (cfg_JetPtCuts.at(0) == 40){
    if (0) std::cout<<"fat jets analysis"<<std::endl;
    for (size_t i=0; i < topData.getAllTopsBJet().size(); i++){
      Jet bjet = topData.getAllTopsBJet().at(i);
      Jet jet1 = topData.getAllTopsJet1().at(i);
      Jet jet2 = topData.getAllTopsJet2().at(i);
      
      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      bool keepTopCandidate = false;
      for(AK8Jet fatJet: fEvent.ak8jets()){
	//Fatjets: definitions
	double tau_21 = fatJet.NjettinessAK8tau2()/fatJet.NjettinessAK8tau1();
	double tau_32 = fatJet.NjettinessAK8tau3()/fatJet.NjettinessAK8tau2();
	//Skip if fat jet does not pass the selection criteria
	
	//=== Apply cut on jet ID
	if (!fatJet.jetIDDiscriminator()) continue;
	//=== Apply cut on jet PU ID
	if (!fatJet.jetPUIDDiscriminator())  continue;
	//=== Apply cut on jet eta
	if (std::abs(fatJet.eta()) >= 2.4) continue;
	//=== Apply cut on jet pt
	if (fatJet.pt() < 150) continue;
	//=== Apply cut on jet tau_21
	if (tau_21 < 0.6)      continue;  
	//=== Apply cut on jet tau_32
	if (tau_32 < 0.67)     continue;  

	//DeltaR(ldgJet, top)
	double dR_fatjet_Top = ROOT::Math::VectorUtil::DeltaR(fatJet.p4(), Top_p4);
	
	h_AfterStandardSelection_DeltaR_fatJets_Top -> Fill(dR_fatjet_Top);
	//Skip if DeltaR(ldgJet, top) < 2.0
	if (dR_fatjet_Top > 2.0) keepTopCandidate = true;	
      }
      
      if (!keepTopCandidate) continue;
      TopCandIndex.push_back(i);
      
      //Pt of all top candidates
      h_AfterStandardSelections_Tops_Pt  -> Fill(Top_p4.Pt());
      
      float mva = topData.getAllTopsMVA().at(i);
      //Pt of all top candidates passing the BDT cut
      if (cfg_MVACut.passedCut(mva)) h_AfterAllSelections_Tops_Pt  -> Fill(Top_p4.Pt());
    }    
  }
  //If 2 bjet are required (BBbar event): form the top candidates excluding the most distant bjet
  else if (0){
    
    for (size_t i=0; i < topData.getAllTopsBJet().size(); i++){
      Jet bjet = topData.getAllTopsBJet().at(i);
      Jet jet1 = topData.getAllTopsJet1().at(i);
      Jet jet2 = topData.getAllTopsJet2().at(i);

      // Get 4-momentum of top (trijet)
      math::XYZTLorentzVector Top_p4;
      Top_p4 = bjet.p4() + jet1.p4() + jet2.p4();
      
      bool keepTopCandidate = false;
      for (auto& bjet_free: bjetData.getSelectedBJets())
	{	  
	  //Skip if bjet forms a top candidate
	  if (areSameJets(bjet_free, bjet) || areSameJets(bjet_free, jet1) || areSameJets(bjet_free, jet2)) continue;
      
	  //DeltaR(ldgJet, top)
	  double dR_bjetFree_Top = ROOT::Math::VectorUtil::DeltaR(bjet_free.p4(), Top_p4);
      
	  //Skip if DeltaR(ldgJet, top) < 2.0
	  if (dR_bjetFree_Top > 2.0) keepTopCandidate = true;
	}

      if (!keepTopCandidate) continue;
      TopCandIndex.push_back(i);
      
      //Pt of all top candidates
      h_AfterStandardSelections_Tops_Pt  -> Fill(Top_p4.Pt());
      
      float mva = topData.getAllTopsMVA().at(i);
      //Pt of all top candidates passing the BDT cut
      if (cfg_MVACut.passedCut(mva)) h_AfterAllSelections_Tops_Pt  -> Fill(Top_p4.Pt());
    }    
  }
 
  int nTopCand = TopCandIndex.size();
  //Return if left with no top candidates
  if (nTopCand < 1) return;

  int ldgTop_index = GetLdgTopIndex(topData, TopCandIndex);
    
  //Get jets of top candidate
  Jet ldgTop_Jet1 = topData.getAllTopsJet1().at(ldgTop_index);
  Jet ldgTop_Jet2 = topData.getAllTopsJet2().at(ldgTop_index);
  Jet ldgTop_BJet = topData.getAllTopsBJet().at(ldgTop_index);
    
  //Get 4-momentum of top (trijet)                                                                                                                                                                     
  math::XYZTLorentzVector Top_p4;
  Top_p4 = ldgTop_Jet1.p4() + ldgTop_Jet2.p4() + ldgTop_BJet.p4();
    
  //Fill plots after standard Selections
  h_AfterStandardSelections_LdgTop_Pt   -> Fill(Top_p4.Pt());
  h_AfterStandardSelections_LdgTop_Mass -> Fill(Top_p4.M());
  h_AfterStandardSelections_MET         -> Fill(met);
  h_AfterStandardSelections_HT          -> Fill(jetData.HT());
  h_AfterStandardSelections_JetMult     -> Fill(jetData.getSelectedJets().size());
  h_AfterStandardSelections_BjetMult    -> Fill(bjetData.getSelectedBJets().size());

  h_AfterStandardSelections_Jet1_Pt     -> Fill(jetData.getSelectedJets().at(0).pt());
  h_AfterStandardSelections_Jet2_Pt     -> Fill(jetData.getSelectedJets().at(1).pt());
  h_AfterStandardSelections_Jet3_Pt     -> Fill(jetData.getSelectedJets().at(2).pt());
  h_AfterStandardSelections_Bjet1_Pt    -> Fill(bjetData.getSelectedBJets().at(0).pt());

  if (bjetData.getSelectedBJets().size() > 1) h_AfterStandardSelections_Bjet2_Pt     -> Fill(bjetData.getSelectedBJets().at(1).pt());

  bool passBDT = PassBDT(topData, ldgTop_index);  
  if (!passBDT) return;

  //Fill plots after all Selections
  h_AfterAllSelections_LdgTop_Pt       -> Fill(Top_p4.Pt());  
  h_AfterAllSelections_LdgTop_Mass -> Fill(Top_p4.M());
  h_AfterAllSelections_MET         -> Fill(met);
  h_AfterAllSelections_HT          -> Fill(jetData.HT());
  h_AfterAllSelections_JetMult     -> Fill(jetData.getSelectedJets().size());
  h_AfterAllSelections_BjetMult    -> Fill(bjetData.getSelectedBJets().size());

  h_AfterAllSelections_Jet1_Pt     -> Fill(jetData.getSelectedJets().at(0).pt());
  h_AfterAllSelections_Jet2_Pt     -> Fill(jetData.getSelectedJets().at(1).pt());
  h_AfterAllSelections_Jet3_Pt     -> Fill(jetData.getSelectedJets().at(2).pt());
  h_AfterAllSelections_Bjet1_Pt    -> Fill(bjetData.getSelectedBJets().at(0).pt());
  if (bjetData.getSelectedBJets().size() > 1) h_AfterAllSelections_Bjet2_Pt     -> Fill(bjetData.getSelectedBJets().at(1).pt());

  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
