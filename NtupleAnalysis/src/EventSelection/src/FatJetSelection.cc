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
  // Event counter for passing selection
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
  // Event counter for passing selection
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
  delete hFatJetPhiAll;
  delete hFatJetCSVAll;
  delete hFatJettau1All;
  delete hFatJettau2All;
  delete hFatJettau3All;
  delete hFatJettau4All;
  delete hFatJettau21All;
  delete hFatJettau32All;
  
  delete hFatJetPtPassed;
  delete hFatJetEtaPassed;
  delete hFatJetPhiPassed;
  delete hFatJetCSVPassed;
  delete hFatJettau1Passed;
  delete hFatJettau2Passed;
  delete hFatJettau3Passed;
  delete hFatJettau4Passed;
  delete hFatJettau21Passed;
  delete hFatJettau32Passed;

  for (auto p: hSelectedFatJetPt) delete p;
  for (auto p: hSelectedFatJetEta) delete p;  
  for (auto p: hSelectedFatJetPhi) delete p;
  for (auto p: hSelectedFatJetCSV) delete p;
  for (auto p: hSelectedFatJettau1) delete p;
  for (auto p: hSelectedFatJettau2) delete p;
  for (auto p: hSelectedFatJettau3) delete p;
  for (auto p: hSelectedFatJettau4) delete p;
  for (auto p: hSelectedFatJettau21) delete p;
  for (auto p: hSelectedFatJettau32) delete p;
  
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

  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "fatjetSelection_"+sPostfix);

  // Histograms (1D)
  
  hFatJetPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtAll", "Fat Jet pT, all;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hFatJetEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaAll", "Fat Jet #eta, all;#eta", nEtaBins, fEtaMin, fEtaMax);
  /* NEW
  delete hFatJetPhiAll;
  delete hFatJetCSVAll;
  delete hFatJettau1All;
  delete hFatJettau2All;
  delete hFatJettau3All;
  delete hFatJettau4All;
  delete hFatJettau21All;
  delete hFatJettau32All;
  */
  
  hFatJetPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetPtPassed", "Fat Jet pT, passed;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hFatJetEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetEtaPassed", "Fat Jet Eta, passed", nEtaBins, fEtaMin, fEtaMax);
  /* NEW
  delete hFatJetPtPassed;
  delete hFatJetEtaPassed;
  delete hFatJetPhiPassed;
  delete hFatJetCSVPassed;
  delete hFatJettau1Passed;
  delete hFatJettau2Passed;
  delete hFatJettau3Passed;
  delete hFatJettau4Passed;
  delete hFatJettau21Passed;
  delete hFatJettau32Passed;
  */
  
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFirstJetPt"  , "First fat jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSecondJetPt" , "Second fat jet pT;p_{T} (GeV/c)" , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsThirdJetPt"  , "Third fat jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFourthJetPt" , "Fourth fat jet pT;p_{T} (GeV/c)" , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFifthJetPt"  , "Fifth fat jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSixthJetPt"  , "Sixth fat jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSeventhJetPt", "Seventh fat jet pT;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFirstJetEta"  , "First fat jet #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSecondJetEta" , "Second fat jet #eta;#eta" , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsThirdJetEta"  , "Third fat jet #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFourthJetEta" , "Fourth fat jet #eta;#eta" , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsFifthJetEta"  , "Fifth fat jet #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSixthJetEta"  , "Sixth fat jet #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSeventhJetEta", "Seventh fat jet #eta;#eta", nEtaBins, fEtaMin, fEtaMax) );
  /* NEW
  for (auto p: hSelectedFatJetPt) delete p;
  for (auto p: hSelectedFatJetEta) delete p;  
  for (auto p: hSelectedFatJetPhi) delete p;
  for (auto p: hSelectedFatJetCSV) delete p;
  for (auto p: hSelectedFatJettau1) delete p;
  for (auto p: hSelectedFatJettau2) delete p;
  for (auto p: hSelectedFatJettau3) delete p;
  for (auto p: hSelectedFatJettau4) delete p;
  for (auto p: hSelectedFatJettau21) delete p;
  for (auto p: hSelectedFatJettau32) delete p;
  */
  hFatJetMatchingToTopDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopDeltaR" , "#DeltaR(fat jet, top)", 40, 0, 2);
  hFatJetMatchingToTopPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTopPtRatio", "fat jet p{T} / top p_{T}", 40, 0, 2);

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
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  FatJetSelection::Data data = privateAnalyze(event, TopSelectionBDT::Data());
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr)
  // fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSelection::Data FatJetSelection::privateAnalyze(const Event& event, const TopSelectionBDT::Data& topData) {
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() " << std::endl;

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
      // std::cout << jet_index << ") abs(eta)["<< etaCut_index << "] > " << jetEtaCut << " (" << jet.eta() << ")" << std::endl;
      if (std::fabs(jet.eta()) > jetEtaCut) continue;
      passedEta = true;
      
      //=== Apply cut on pt   
      const float jetPtCut = fFatJetPtCuts.at(ptCut_index);
      // std::cout << jet_index << ") pT["<< ptCut_index << "] > " << jetPtCut << " GeV/c (" << jet.pt() << ")" << std::endl;
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
      std::cout << jet_index+1 << ") pT = " << jet.pt() << std::endl;
      std::cout << jet_index+1 << ") |eta| = " << jet.eta() << std::endl;
    }
  
  // Fill counters so far
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() Counters" << std::endl;
  if (passedFatJetID) cSubPassedFatJetID.increment();
  if (passedFatJetPUID) cSubPassedFatJetPUID.increment();
  if (passedDeltaRMatchWithTop) cSubPassedDeltaRMatchWithTop.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedPt)  cSubPassedPt.increment();
  
  //=== Apply cut on number of jets
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() NJets cut" << std::endl;
  if (!fNumberOfFatJetsCut.passedCut(output.fSelectedFatJets.size())) return output;
  cSubPassedFatJetCount.increment();
  
  // Sort fat jets by pT (descending order)
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() Sort by pt" << std::endl;
  std::sort(output.fSelectedFatJets.begin(), output.fSelectedFatJets.end());
  
  //=== Passed all fat jet selections
  output.bPassedSelection = true;
  cPassedFatJetSelection.increment();
  

  // Find jet matched to top
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() Matching Top" << std::endl;
  if (topP.pt() > 0.0) {
    findFatJetMatchingToTop(output.fFatJetMatchedToTop, event, topP);
    if (output.fatjetMatchedToTopFound())  
      {
	hFatJetMatchingToTopPtRatio->Fill(topP.pt() / output.getFatJetMatchedToTop().pt());
      }
  }
  
  if (1) std::cout << "=== FatJetSelection::privateAnalyze() Auxiliary Histos" << std::endl;
  // Fill pt and eta of jets
  size_t i = 0;
  for (AK8Jet jet: output.fSelectedFatJets) {
    if (i < 6) {
      hSelectedFatJetPt[i]->Fill(jet.pt());
      hSelectedFatJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }  
  

  if (1) std::cout << "=== FatJetSelection::privateAnalyze() Return" << std::endl;  

  // Return data object
  return output;
}

void FatJetSelection::findFatJetMatchingToTop(std::vector<AK8Jet>& collection, const Event& event, const math::XYZTLorentzVector& topP) {
//const math::LorentzVectorT<double>& topP) {
  double myMinDeltaR = 9999;
  size_t mySelectedIndex = 9999;
  size_t i = 0;
  
  // For-loop: All AK8 jets
  for(AK8Jet jet: event.ak8jets()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(topP, jet.p4());
    if (myDeltaR < myMinDeltaR) {
      myMinDeltaR = myDeltaR;
      mySelectedIndex = i;
    }
    i += 1;
  }
  if (myMinDeltaR < 0.1)
    collection.push_back(event.ak8jets()[mySelectedIndex]);
}
