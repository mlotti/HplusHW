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
  fFatJetMatchedToTop(0)
{ }

FatJetSelection::Data::~Data() { }

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
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTop(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed top matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet number cut"))
{ 
  initialize(config);
}

FatJetSelection::FatJetSelection(const ParameterSet& config)
: BaseSelection(),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")), 
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")), 
  fTopMatchingDeltaR(config.getParameter<float>("topMatchingDeltaR")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTop(fEventCounter.addSubCounter("fat jet selection", "Passed top matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection", "Passed pt cut")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet number cut"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

FatJetSelection::~FatJetSelection() { 
  
  delete hFatJetPtAll;
  delete hFatJetEtaAll;
  delete hFatJetPtPassed;
  delete hFatJetEtaPassed;
  delete hFatJetMatchingToTopDeltaR;
  delete hFatJetMatchingToTopPtRatio;
  }

void FatJetSelection::initialize(const ParameterSet& config) {
  
  if(fCommonPlots){
    nPtBins    = 2 * fCommonPlots->getPtBinSettings().bins();
    fPtMin     = 2 * fCommonPlots->getPtBinSettings().min();
    fPtMax     = 2 * fCommonPlots->getPtBinSettings().max();

    nEtaBins   = fCommonPlots->getEtaBinSettings().bins();
    fEtaMin    = fCommonPlots->getEtaBinSettings().min();
    fEtaMax    = fCommonPlots->getEtaBinSettings().max();

  }else{
    nPtBins  = 50;
    fPtMin   = 0;
    fPtMax   = 500;

    nEtaBins = 50;
    fEtaMin  = -2.5;
    fEtaMax  = 2.5;

  }
}

void FatJetSelection::bookHistograms(TDirectory* dir) {

  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "fatjetSelection_" + sPostfix);

  // Histograms (1D)
  hFatJetPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtAll"    , ";p_{T} (GeV/c);Occur / %.0f", nPtBins , fPtMin , fPtMax);
  hFatJetEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaAll"   , ";#eta;Occur / %.2f"         , nEtaBins, fEtaMin, fEtaMax);
  hFatJetPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtPassed" , ";p_{T} (GeV/c);Occur / %.0f", nPtBins , fPtMin , fPtMax);
  hFatJetEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaPassed", ";#eta;Occur / %.2f"         , nEtaBins, fEtaMin, fEtaMax); 
  hFatJetMatchingToTopDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopDeltaR" , ";#DeltaR(fat jet, top);Occur / %.2f"  , 40, 0.0, 2.0);
  hFatJetMatchingToTopPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopPtRatio", ";fat jet p{T} / top p_{T}Occur / %.2f", 40, 0.0, 2.0);

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
  bool passedDeltaRMatchWithTop = false;
  bool passedEta = false;
  bool passedPt  = false;

  const math::XYZTLorentzVector topP = topData.getLdgTrijet();
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
      output.fAllFatJets.push_back(jet);   
      
      // Fill histos (before pt/eta cuts)
      hFatJetPtAll->Fill(jet.pt());
      hFatJetEtaAll->Fill(jet.eta());
            
      //=== Apply cut on tau radius
      if (topP.pt() > 0.0) {
	double myDeltaR = ROOT::Math::VectorUtil::DeltaR(topP, jet.p4());
	hFatJetMatchingToTopDeltaR->Fill(myDeltaR);
	if (myDeltaR < fTopMatchingDeltaR) continue;
	passedDeltaRMatchWithTop = true;
      }
      
      //=== Apply cut on eta
      const float jetEtaCut = fFatJetEtaCuts.at(etaCut_index);
      if (std::fabs(jet.eta()) > jetEtaCut) continue;
      passedEta = true;
      
      //=== Apply cut on pt   
      const float jetPtCut = fFatJetPtCuts.at(ptCut_index);
      if (jet.pt() < jetPtCut) continue;
      passedPt = true;
      
      // Fat Jet passed all cuts   
      output.fSelectedFatJets.push_back(jet);

      // Fill histos (after pt/eta cuts)
      hFatJetPtPassed->Fill(jet.pt());
      hFatJetEtaPassed->Fill(jet.eta());
      
      // Increment cut index only. Cannot be bigger than the size of the cut list provided
      if (ptCut_index  < fFatJetPtCuts.size()-1  ) ptCut_index++;
      if (etaCut_index < fFatJetEtaCuts.size()-1 ) etaCut_index++;
    }
  
  // Fill counters so far
  if (passedFatJetID) cSubPassedFatJetID.increment();
  if (passedFatJetPUID) cSubPassedFatJetPUID.increment();
  if (passedDeltaRMatchWithTop) cSubPassedDeltaRMatchWithTop.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedPt)  cSubPassedPt.increment();

  //=== Apply cut on number of jets
  if (!fNumberOfFatJetsCut.passedCut(output.fSelectedFatJets.size())) return output;
  cSubPassedFatJetCount.increment();
  
  // Sort fat jets by pT (descending order)
  std::sort(output.fSelectedFatJets.begin(), output.fSelectedFatJets.end());
  
  //=== Passed all fat jet selections
  output.bPassedSelection = true;
  cPassedFatJetSelection.increment();
  

  // Find jet matched to top
  if (topP.pt() > 0.0) 
    {
      // Create collection of all AK8 jets that match the top
      findFatJetMatchingToTop(output.fFatJetMatchedToTop, event, topP);
      
      // Fill histogram
      if (output.fatjetMatchedToTopFound())  
	{
	  hFatJetMatchingToTopPtRatio->Fill( topP.pt() / output.getFatJetMatchedToTop().pt() );
	}
    }
  
  // Return data object
  return output;
}

void FatJetSelection::findFatJetMatchingToTop(std::vector<AK8Jet>& collection, const Event& event, const math::XYZTLorentzVector& topP) {

  double myMinDeltaR = 9999.9;
  size_t mySelectedIndex = 9999.9;
  size_t i = 0;
  
  // For-loop: All AK8 jets
  for(AK8Jet jet: event.ak8jets()) {
    double dR = ROOT::Math::VectorUtil::DeltaR(topP, jet.p4());

    // Found new minimum distance?
    if (dR < myMinDeltaR) 
      {
	myMinDeltaR = dR;
	mySelectedIndex = i;
      }

    // Increment index
    i += 1;
  }
  
  // Save matching AK8 into collection of jets matching the top
  if (myMinDeltaR < 0.1) collection.push_back(event.ak8jets()[mySelectedIndex]);
}
