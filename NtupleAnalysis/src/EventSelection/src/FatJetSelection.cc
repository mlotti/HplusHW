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
  fFatJetMatchedToTopType(FatJetSelection::kNone)
{ }

FatJetSelection::Data::~Data() { }

const FatJetSelection::FatjetType FatJetSelection::Data::getFatJetMatchedToTopType() const {

  return fFatJetMatchedToTopType[0];
}

const AK8Jet& FatJetSelection::Data::getFatJetMatchedToTop() const { 
  if (!fatjetMatchedToTopFound())
    throw hplus::Exception("Assert") << "You forgot to check if the fat jet matched to top exists (fatjetMatchedToTopFound()), this message occurs when none exists!";

  return fFatJetMatchedToTop[0];
}

FatJetSelection::FatJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")),
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")),
  fTopMatchDeltaR(config.getParameter<float>("topMatchDeltaR")),
  fTopMatchTypes(config.getParameter<std::vector<int>>("topMatchTypes")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed PU ID")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedTopMatchType(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed top type")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet number cut"))
{ 
  initialize(config);
}

FatJetSelection::FatJetSelection(const ParameterSet& config)
: BaseSelection(),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")), 
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")), 
  fTopMatchDeltaR(config.getParameter<float>("topMatchDeltaR")),
  fTopMatchTypes(config.getParameter<std::vector<int>>("topMatchTypes")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection", "Passed PU ID")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection", "Passed eta cut")),
  cSubPassedTopMatchType(fEventCounter.addSubCounter("fat jet selection", "Passed top type")),
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
  delete hFatJetTopMatchDeltaRJet1;
  delete hFatJetTopMatchDeltaRJet2; 
  delete hFatJetTopMatchDeltaRBjet;
  delete hFatJetTopMatchPtRatio;
  }

void FatJetSelection::initialize(const ParameterSet& config) {
  
  if(fCommonPlots){
    nNBins   = 0.5 * fCommonPlots->getNjetsBinSettings().bins();
    fNMin    = 0.5 * fCommonPlots->getNjetsBinSettings().min();
    fNMax    = 0.5 * fCommonPlots->getNjetsBinSettings().max();

    nPtBins  = 2 * fCommonPlots->getPtBinSettings().bins();
    fPtMin   = 2 * fCommonPlots->getPtBinSettings().min();
    fPtMax   = 2 * fCommonPlots->getPtBinSettings().max();

    nEtaBins = fCommonPlots->getEtaBinSettings().bins();
    fEtaMin  = fCommonPlots->getEtaBinSettings().min();
    fEtaMax  = fCommonPlots->getEtaBinSettings().max();

    nDRBins = fCommonPlots->getDeltaRBinSettings().bins();
    fDRMin  = fCommonPlots->getDeltaRBinSettings().min();
    fDRMax  = fCommonPlots->getDeltaRBinSettings().max();

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

    nDRBins = 100.0;
    fDRMin  =   0.0;
    fDRMax  =  10.0;
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
  hFatJetTopMatchDeltaRJet1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetTopMatchDeltaRJet1", ";#DeltaR(fat jet, jet1);Occur / %.2f", nDRBins, fDRMin, fDRMax);
  hFatJetTopMatchDeltaRJet2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetTopMatchDeltaRJet2", ";#DeltaR(fat jet, jet2);Occur / %.2f", nDRBins, fDRMin, fDRMax);
  hFatJetTopMatchDeltaRBjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetTopMatchDeltaRBjet", ";#DeltaR(fat jet, bjet);Occur / %.2f", nDRBins, fDRMin, fDRMax);
  hFatJetTopMatchType    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetTopMatchType"   , ";top type;Occur / %.2f", 5, -1.0, 4.0);
  hFatJetTopMatchPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetTopMatchPtRatio", ";fat jet p_{T} / top p_{T};Occur / %.2f", 40, 0.0, 2.0);

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
  
  // Sanity check
  std::vector<int> topTypes = {-1, 0, 1, 2, 3}; // C++11 and later
  bool isValidType = false;
  for (auto t: topTypes)
    {
      bool bFoundType = (std::find(fTopMatchTypes.begin(), fTopMatchTypes.end(), t) != fTopMatchTypes.end());
      if (!bFoundType) continue;
      isValidType = true;
      break;
    }
  if (!isValidType) throw hplus::Exception("Assert") << "Invalid top-match types selected! Please select from (-1, 0, 1, 2, 3)";

  // Definitions
  const math::XYZTLorentzVector topP = topData.getLdgTrijet();
  Data output;
  bool disableTopMatch = false;
  bool passedFatJetID = false;
  bool passedFatJetPUID = false;
  bool passedPt  = false;
  bool passedEta = false;
  bool passedTopMatchType = false;

  // Disable the top-match?
  if (topP.pt() == 0.0) disableTopMatch = true;
  if (std::find(fTopMatchTypes.begin(), fTopMatchTypes.end(), -1) != fTopMatchTypes.end()) disableTopMatch  = true;

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
      if (!disableTopMatch)
	{

	  // Find distance to top constituents
	  double dR_jet1 = 999.9;
	  double dR_jet2 = 999.9;
	  double dR_bjet = 999.9;
	  findFatJetMatchedToTopDeltaR(jet, dR_bjet, dR_jet1, dR_jet2, topData);
	  // Fill histos
	  hFatJetTopMatchDeltaRJet1->Fill(dR_jet1);
	  hFatJetTopMatchDeltaRJet2->Fill(dR_jet2);
	  hFatJetTopMatchDeltaRBjet->Fill(dR_bjet);

	  // Determine top-match type
	  const FatJetSelection::FatjetType type = findFatJetMatchedToTopType(jet, dR_bjet, dR_jet1, dR_jet2, topData);
	  output.fFatJetMatchedToTopType.push_back(type);
	  hFatJetTopMatchType->Fill(type);

	  //=== Apply top-matching type cut
	  if (std::find(fTopMatchTypes.begin(), fTopMatchTypes.end(), type) == fTopMatchTypes.end()) continue;
	  passedTopMatchType = true;

	  // Save info & Fill histos (after matching)
	  output.fSelectedFatJets.push_back(jet);
 	  hFatJetTopMatchPtRatio->Fill( topP.pt() / jet.pt() );
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
  if (passedTopMatchType) cSubPassedTopMatchType.increment();

  //=== Apply cut on number of jets
  if (!fNumberOfFatJetsCut.passedCut(output.fSelectedFatJets.size())) return output;
  cSubPassedFatJetCount.increment();  

  // Sort fat jets by pT (descending order)
  std::sort(output.fSelectedFatJets.begin(), output.fSelectedFatJets.end());
    
  // If more than 1 match found keep highest-pT candidate
  if (output.fSelectedFatJets.size() > 0) output.fFatJetMatchedToTop.push_back(output.fSelectedFatJets.at(0));

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
  if (myMinDeltaR < fTopMatchDeltaR) collection.push_back(event.ak8jets()[mySelectedIndex]);

  return;
}

const FatJetSelection::FatjetType FatJetSelection::findFatJetMatchedToTopType(AK8Jet fatJetTopMatch, 
									      const double dR_bjet, 
									      const double dR_jet1, 
									      const double dR_jet2, 
									      const TopSelectionBDT::Data& topData) {

  FatJetSelection::FatjetType type;

  // Construct simple booleans
  bool match_bjet = (dR_bjet <= fTopMatchDeltaR);
  bool match_jet1 = (dR_jet1 <= fTopMatchDeltaR);
  bool match_jet2 = (dR_jet2 <= fTopMatchDeltaR);
  if (0) std::cout << "\n+++ match_bjet = " << match_bjet << ", match_jet1 = " << match_jet1 << ", match_jet2 = " << match_jet2 << std::endl;

  // Construct composite booleans
  bool jjb = (match_bjet*match_jet1*match_jet2);
  bool jj  = (match_jet1*match_jet2 && !match_bjet);
  bool jb  = ( (match_bjet*match_jet1 && !match_jet2) || (match_bjet*match_jet2 && !match_jet1));
  if (0) std::cout << "+++ jjb = " << jjb << ", jj = " << jj << ", jb = " << jb << std::endl;

  // Fill correct type using composite booleans
  if (jjb) type = FatJetSelection::kJJB;
  else if (jj) type = FatJetSelection::kJJ;
  else if (jb) type = FatJetSelection::kJB;
  else type = FatJetSelection::kJB;
  return type;
}

void FatJetSelection::findFatJetMatchedToTopDeltaR(AK8Jet fatJetTopMatch, 
						   double &dR_bjet, 
						   double &dR_jet1, 
						   double &dR_jet2, 
						   const TopSelectionBDT::Data& topData) {

  // Get leading top AK4 jet constituents
  const Jet top_bjet = topData.getLdgTrijetBJet();
  const Jet top_jet1 = topData.getLdgTrijetJet1();
  const Jet top_jet2 = topData.getLdgTrijetJet2();

  // Caclulate distances
  dR_bjet = ROOT::Math::VectorUtil::DeltaR(fatJetTopMatch.p4(), top_bjet.p4());
  dR_jet1 = ROOT::Math::VectorUtil::DeltaR(fatJetTopMatch.p4(), top_jet1.p4());
  dR_jet2 = ROOT::Math::VectorUtil::DeltaR(fatJetTopMatch.p4(), top_jet2.p4());

  return;
}
