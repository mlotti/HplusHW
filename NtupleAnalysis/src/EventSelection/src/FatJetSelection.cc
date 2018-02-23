// -*- c++ -*-
#include "EventSelection/interface/FatJetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

FatJetSelection::Data::Data()
: bPassedSelection(false),
  fFatJetMatchedToTop(0),
  fFatJetMatchedToTopType(FatJetSelection::kUNKNOWN)
{ }

FatJetSelection::Data::~Data() { }

const FatJetSelection::FatjetType FatJetSelection::Data::getFatJetMatchedToTopType() const {
  return fFatJetMatchedToTopType[0];
}

const AK8Jet& FatJetSelection::Data::getFatJetMatchedToTop() const { 
  if (!fatjetMatchedToTopFound())
    throw hplus::Exception("Assert") << "You forgot to check if the fat jet matched to leading trijet exists (fatjetMatchedToTopFound()), this message occurs when none exists!";

  return fFatJetMatchedToTop[0];
}

FatJetSelection::FatJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")),
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")),
  fTopMatchingDeltaR(config.getParameter<float>("topMatchingDeltaR")),
  fTopMatchingType(config.getParameter<int>("topMatchingType")),
  fTopConstituentMatchingDeltaR(config.getParameter<float>("topConstituentMatchingDeltaR")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed PU ID")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedDeltaRMatchWithTop(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed top matching")),
  cSubPassedTopMatchingType(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed top type")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet number cut"))
{ 
  initialize(config);
}

FatJetSelection::FatJetSelection(const ParameterSet& config)
: BaseSelection(),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")), 
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")), 
  fTopMatchingDeltaR(config.getParameter<float>("topMatchingDeltaR")),
  fTopMatchingType(config.getParameter<int>("topMatchingType")),
  fTopConstituentMatchingDeltaR(config.getParameter<float>("topConstituentMatchingDeltaR")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection", "Passed PU ID")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection", "Passed eta cut")),
  cSubPassedDeltaRMatchWithTop(fEventCounter.addSubCounter("fat jet selection", "Passed top matching")),
  cSubPassedTopMatchingType(fEventCounter.addSubCounter("fat jet selection", "Passed top type")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet number cut"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

FatJetSelection::~FatJetSelection() { 
  
  delete hFatJetNAll;
  delete hFatJetPtAll;
  delete hFatJetEtaAll;
  delete hFatJetNPassed;
  delete hFatJetPtPassed;
  delete hFatJetEtaPassed;
  delete hFatJetMatchingToTopDeltaR;
  delete hFatJetMatchingToTopPtRatio;
  }

void FatJetSelection::initialize(const ParameterSet& config) {
  
  if(fCommonPlots){
    nNBins   = fCommonPlots->getNjetsBinSettings().bins();
    fNMin    = fCommonPlots->getNjetsBinSettings().min();
    fNMax    = fCommonPlots->getNjetsBinSettings().max();

    nPtBins  = 2 * fCommonPlots->getPtBinSettings().bins();
    fPtMin   = 2 * fCommonPlots->getPtBinSettings().min();
    fPtMax   = 2 * fCommonPlots->getPtBinSettings().max();

    nEtaBins = fCommonPlots->getEtaBinSettings().bins();
    fEtaMin  = fCommonPlots->getEtaBinSettings().min();
    fEtaMax  = fCommonPlots->getEtaBinSettings().max();

  }else{
    nNBins  = 20;
    fNMin   =  0.0;
    fNMax   = 20.0;

    nPtBins  =  50;
    fPtMin   =   0;
    fPtMax   = 500.0;

    nEtaBins = 50;
    fEtaMin  = -2.5;
    fEtaMax  = +2.5;

  }
}

void FatJetSelection::bookHistograms(TDirectory* dir) {

  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "fatjetSelection_" + sPostfix);

  // Histograms (1D)
  hFatJetNAll      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetNAll"     , ";fat-jet multiplicity;Occur / %.0f", nNBins , fNMin , fNMax);
  hFatJetPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtAll"    , ";p_{T} (GeV/c);Occur / %.0f", nPtBins , fPtMin , fPtMax);
  hFatJetEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaAll"   , ";#eta;Occur / %.2f"         , nEtaBins, fEtaMin, fEtaMax);
  hFatJetNPassed   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetNPassed"  , ";fat-jet multiplicity;Occur / %.0f", nNBins , fNMin , fNMax);
  hFatJetPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtPassed" , ";p_{T} (GeV/c);Occur / %.0f", nPtBins , fPtMin , fPtMax);
  hFatJetEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaPassed", ";#eta;Occur / %.2f"         , nEtaBins, fEtaMin, fEtaMax); 
  hFatJetMatchingToTopDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopDeltaR" , ";#DeltaR(fat jet, top);Occur / %.2f"    , 200, 0.0, 2.0);
  hFatJetMatchingToTopPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopPtRatio", ";fat jet p_{T} / top p_{T};Occur / %.2f", 200, 0.0, 2.0);

  return;
}

FatJetSelection::Data FatJetSelection::silentAnalyze(const Event& event, const TopSelectionBDT::Data& topData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, topData);
  enableHistogramsAndCounters();
  return myData;
}

FatJetSelection::Data FatJetSelection::silentAnalyzeWithoutTop(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, TopSelectionBDT::Data());
  enableHistogramsAndCounters();
  return myData;
}

FatJetSelection::Data FatJetSelection::analyze(const Event& event, const TopSelectionBDT::Data& topData) {
  ensureAnalyzeAllowed(event.eventID());
  FatJetSelection::Data data = privateAnalyze(event, topData);
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr)
  // fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSelection::Data FatJetSelection::analyzeWithoutTop(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  FatJetSelection::Data data = privateAnalyze(event, TopSelectionBDT::Data());
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr)
  // fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSelection::Data FatJetSelection::privateAnalyze(const Event& event, const TopSelectionBDT::Data& topData) {

  // Increment inclusive counter
  cSubAll.increment();
  
  // Definitions
  Data output;
  bool passedFatJetID = false;
  bool passedFatJetPUID = false;
  bool passedPt  = false;
  bool passedEta = false;
  bool passedDeltaRMatchWithTop = false;
  bool passedTopMatchingType = false;

  bool disableMatching = false;
  if (fTopMatchingDeltaR < 0) 
    {
      disableMatching          = true;
      passedDeltaRMatchWithTop = true;
      passedTopMatchingType    = true;
    }
  
  const math::XYZTLorentzVector topP = topData.getLdgTrijet();
  // math::LorentzVectorT<double> topP(0.,0.,9999.,0.);

  unsigned int jet_index    = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;
  
  // For-loop: All jets (pT-sorted)
  for(AK8Jet jet: event.ak8jets())
    {
      // Jet index (for pT and eta cuts)
      jet_index++;

      //=== Apply cut on jet ID
      if (!jet.jetIDDiscriminator()) continue;
      passedFatJetID = true;
      
      //=== Apply cut on jet PU ID
      if (!jet.jetPUIDDiscriminator())	continue;
      passedFatJetPUID = true;
            
      //=== Apply cut on pt   
      const float jetPtCut = fFatJetPtCuts.at(ptCut_index);
      if (jet.pt() < jetPtCut) continue;
      passedPt = true;

      //=== Apply cut on eta
      const float jetEtaCut = fFatJetEtaCuts.at(etaCut_index);
      if (std::fabs(jet.eta()) > jetEtaCut) continue;
      passedEta = true;
      
      // Save info & Fill histos (before matching)
      output.fAllFatJets.push_back(jet);
      hFatJetPtAll->Fill(jet.pt());
      hFatJetEtaAll->Fill(jet.eta());

      //=== Apply cut on top dR-matching
      if (!disableMatching)  //if (topP.pt() > 0.0)
	{
	  // Fill histo
	  double myDeltaR = ROOT::Math::VectorUtil::DeltaR(topP, jet.p4());
	  hFatJetMatchingToTopDeltaR->Fill(myDeltaR);
	  
	  // Check if cut satisfied
	  if (myDeltaR > fTopMatchingDeltaR) continue;
	  passedDeltaRMatchWithTop = true;

	  // Save matched jet to a vector
	  output.fFatJetMatchedToTop.push_back(jet);

	  // Determine matching type [resolved top (jjb), W(jj), jb]
	  const FatJetSelection::FatjetType type = findFatJetMatchedToTopType(output.getFatJetMatchedToTop(), topData);
	  output.fFatJetMatchedToTopType.push_back(type);

	  //=== Apply top-matching cut - fat jet type (resolved top, Wb, jb)
	  if (fTopMatchingType < 0) passedTopMatchingType = true;
	  else if (type <= fTopMatchingType) continue;
	  passedTopMatchingType = true;

	  // Save info & Fill histos (after matching)
	  output.fSelectedFatJets.push_back(jet);
 	  hFatJetMatchingToTopPtRatio->Fill( topP.pt() / output.getFatJetMatchedToTop().pt() );
	  hFatJetPtPassed->Fill(jet.pt());
	  hFatJetEtaPassed->Fill(jet.eta());	  
	}
      else
	{
	  // Save info & Fill histos (after matching)
	  output.fSelectedFatJets.push_back(jet);
	  hFatJetPtPassed->Fill(jet.pt());
	  hFatJetEtaPassed->Fill(jet.eta());
	}

      // Increment cut index only. Cannot be bigger than the size of the cut list
      if (ptCut_index  < fFatJetPtCuts.size()-1  ) ptCut_index++;
      if (etaCut_index < fFatJetEtaCuts.size()-1 ) etaCut_index++;
    }

  // Fill histos
  hFatJetNAll->Fill(output.fAllFatJets.size());
  hFatJetNPassed->Fill(output.fSelectedFatJets.size());

  // Fill counters so far
  if (passedFatJetID) cSubPassedFatJetID.increment();
  if (passedFatJetPUID) cSubPassedFatJetPUID.increment();
  if (passedPt)  cSubPassedPt.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedDeltaRMatchWithTop) cSubPassedDeltaRMatchWithTop.increment();
  if (passedTopMatchingType) cSubPassedTopMatchingType.increment();
  if (passedTopMatchingType) cSubPassedTopMatchingType.increment();

  //=== Apply cut on number of jets
  if (!fNumberOfFatJetsCut.passedCut(output.fSelectedFatJets.size())) return output;
  cSubPassedFatJetCount.increment();  

  // Sort fat jets by pT (descending order)
  std::sort(output.fSelectedFatJets.begin(), output.fSelectedFatJets.end());
    
  //=== Passed all fat jet selections
  output.bPassedSelection = true;
  cPassedFatJetSelection.increment();

  // Return data object
  return output;
}

void FatJetSelection::findFatJetMatchedToTop(std::vector<AK8Jet>& collection, const Event& event, const math::XYZTLorentzVector& topP) {

  double myMinDeltaR = 9999.9;
  size_t mySelectedIndex = 9999.9;
  size_t i = 0;
  
  // For-loop: All AK8 jets
  for(AK8Jet jet: event.ak8jets()) {
    double dR = ROOT::Math::VectorUtil::DeltaR(topP, jet.p4());

    // Update the index of the best match (based on minimum distance)
    if (dR < myMinDeltaR) 
      {
	myMinDeltaR = dR;
	mySelectedIndex = i;
      }

    // Increment index
    i += 1;
  }
  
  // Save matching AK8 into collection of jets matching the top (unique matching)
  if (myMinDeltaR < fTopMatchingDeltaR) collection.push_back(event.ak8jets()[mySelectedIndex]);

  return;
}

const FatJetSelection::FatjetType FatJetSelection::findFatJetMatchedToTopType(AK8Jet fatJetMatchingToTop, const TopSelectionBDT::Data& topData) {

  FatJetSelection::FatjetType type;

  // Get leading top AK4 jet constituents
  const Jet top_bjet = topData.getLdgTrijetBJet();
  const Jet top_jet1 = topData.getLdgTrijetJet1();
  const Jet top_jet2 = topData.getLdgTrijetJet2();

  // Caclulate distances
  double dR_bjet = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_bjet.p4());
  double dR_jet1 = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_jet1.p4());
  double dR_jet2 = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_jet2.p4());
  // std::cout << "dR_bjet = " << dR_bjet << ", dR_jet1 = " << dR_jet1 << ", dR_jet2 = " << dR_jet2 << std::endl;

  // Construct simple booleans
  bool match_bjet = (dR_bjet <= fTopConstituentMatchingDeltaR);
  bool match_jet1 = (dR_jet1 <= fTopConstituentMatchingDeltaR);
  bool match_jet2 = (dR_jet2 <= fTopConstituentMatchingDeltaR);
  // std::cout << "match_bjet = " << match_bjet << ", match_jet1 = " << match_jet1 << ", match_jet2 = " << match_jet2 << std::endl;

  // Construct composite booleans
  bool jjb = (match_bjet*match_jet1*match_jet2);
  bool jj  = (match_jet1*match_jet2 && !match_bjet);
  bool jb  = (match_bjet*match_jet1 || match_bjet*match_jet2);
  // std::cout << "jjb = " << jjb << ", jj = " << jj << ", jb = " << jb << std::endl;

  // Fill correct type using composite booleans
  if (jjb) type = FatJetSelection::kJJB;
  else if (jj) type = FatJetSelection::kJJ;
  else if (jb) type = FatJetSelection::kJB;
  else type = FatJetSelection::kUNKNOWN;

  return type;
}

/*
void FatJetSelection::findFatJetMatchedToTopType(FatJetSelection::FatjetType& type, AK8Jet fatJetMatchingToTop, const TopSelectionBDT::Data& topData) {

  // Get leading top AK4 jet constituents
  const Jet top_bjet = topData.getLdgTrijetBJet();
  const Jet top_jet1 = topData.getLdgTrijetJet1();
  const Jet top_jet2 = topData.getLdgTrijetJet2();

  // Caclulate distances
  double dR_bjet = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_bjet.p4());
  double dR_jet1 = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_jet1.p4());
  double dR_jet2 = ROOT::Math::VectorUtil::DeltaR(fatJetMatchingToTop.p4(), top_jet2.p4());
  // std::cout << "dR_bjet = " << dR_bjet << ", dR_jet1 = " << dR_jet1 << ", dR_jet2 = " << dR_jet2 << std::endl;

  // Construct simple booleans
  bool match_bjet = (dR_bjet <= fTopConstituentMatchingDeltaR);
  bool match_jet1 = (dR_jet1 <= fTopConstituentMatchingDeltaR);
  bool match_jet2 = (dR_jet2 <= fTopConstituentMatchingDeltaR);
  // std::cout << "match_bjet = " << match_bjet << ", match_jet1 = " << match_jet1 << ", match_jet2 = " << match_jet2 << std::endl;

  // Construct composite booleans
  bool jjb = (match_bjet*match_jet1*match_jet2);
  bool jj  = (match_jet1*match_jet2);
  bool jb  = (match_bjet*match_jet1 || match_bjet*match_jet2);
  // std::cout << "jjb = " << jjb << ", jj = " << jj << ", jb = " << jb << std::endl;

  // Fill correct type using composite booleans
  if (jjb) type = FatJetSelection::kJJB;
  else if (jj) type = FatJetSelection::kJJ;
  else if (jb) type = FatJetSelection::kJB;
  else type = FatJetSelection::kUNKNOWN;
  return;
}
*/
