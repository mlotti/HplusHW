// -*- c++ -*-
#include "EventSelection/interface/FatJetSoftDropSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

FatJetSoftDropSelection::Data::Data()
: bPassedSelection(false),
  fFatJetSoftDropMatchedToTau(0),
  fHT(-1.0),
  fMHTvalue(-1.0),
  fMinDeltaPhiFatJetSoftDropMHT(-1.0),
  fMaxDeltaPhiFatJetSoftDropMHT(-1.0),
  fMinDeltaRFatJetSoftDropMHT(-1.0),
  fMinDeltaRReversedFatJetSoftDropMHT(-1.0)
{ }

FatJetSoftDropSelection::Data::~Data() { }

const AK8JetsSoftDrop& FatJetSoftDropSelection::Data::getFatJetSoftDropMatchedToTau() const { 
  if (!fatjetSoftDropMatchedToTauFound())
    throw hplus::Exception("Assert") << "You forgot to check if the fat jet matched to tau exists (fatjetSoftDropMatchedToTauFound()), this message occurs when none exists!";
  return fFatJetSoftDropMatchedToTau[0];
}

FatJetSoftDropSelection::FatJetSoftDropSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fFatJetSoftDropPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")),
  fFatJetSoftDropEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")),
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfFatJetsSoftDropCut(config, "numberOfFatJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedFatJetSoftDropSelection(fEventCounter.addCounter("passed fat jet soft drop selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "All events")),
  cSubPassedFatJetSoftDropID(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed fat jet ID")),
  cSubPassedFatJetSoftDropPUID(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed pt cut")),
  cSubPassedFatJetSoftDropCount(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed fat jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("fat jet soft drop selection ("+postfix+")", "Passed MHT cut"))
{ 
  initialize(config);
}

FatJetSoftDropSelection::FatJetSoftDropSelection(const ParameterSet& config)
: BaseSelection(),
  fFatJetSoftDropPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")), 
  fFatJetSoftDropEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")), 
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfFatJetsSoftDropCut(config, "numberOfFatJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedFatJetSoftDropSelection(fEventCounter.addCounter("passed fat jet soft drop selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet soft drop selection", "All events")),
  cSubPassedFatJetSoftDropID(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed fat jet ID")),
  cSubPassedFatJetSoftDropPUID(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed pt cut")),
  cSubPassedFatJetSoftDropCount(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed fat jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("fat jet soft drop selection", "Passed MHT cut"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

FatJetSoftDropSelection::~FatJetSoftDropSelection() { 
  
  delete hFatJetSoftDropPtAll;
  delete hFatJetSoftDropEtaAll;
  delete hFatJetSoftDropSubjetsAll;
  delete hFatJetSoftDropHasBSubjetAll;
  
  delete hFatJetSoftDropPtPassed;
  delete hFatJetSoftDropEtaPassed;
  delete hFatJetSoftDropSubjetsPassed;
  delete hFatJetSoftDropHasBSubjetPassed;
  
  for (auto p: hSelectedFatJetSoftDropPt) delete p;
  for (auto p: hSelectedFatJetSoftDropEta) delete p;  
  delete hFatJetSoftDropMatchingToTauDeltaR;
  delete hFatJetSoftDropMatchingToTauPtRatio;
  delete hHTAll;
  delete hJTAll;
  delete hMHTAll;
  delete hHTPassed;
  delete hJTPassed;
  delete hMHTPassed;
  
  
  }

void FatJetSoftDropSelection::initialize(const ParameterSet& config) {

  if(fCommonPlots){
    nPtBins    = 2 * fCommonPlots->getPtBinSettings().bins();
    fPtMin     = 2 * fCommonPlots->getPtBinSettings().min();
    fPtMax     = 2 * fCommonPlots->getPtBinSettings().max();

    nEtaBins   = fCommonPlots->getEtaBinSettings().bins();
    fEtaMin    = fCommonPlots->getEtaBinSettings().min();
    fEtaMax    = fCommonPlots->getEtaBinSettings().max();

    nHtBins    = fCommonPlots->getHtBinSettings().bins();
    fHtMin     = fCommonPlots->getHtBinSettings().min();
    fHtMax     = fCommonPlots->getHtBinSettings().max();
  }else{
    nPtBins  = 50;
    fPtMin   = 0;
    fPtMax   = 500;

    nEtaBins = 50;
    fEtaMin  = -2.5;
    fEtaMax  = 2.5;

    nHtBins  = 240;
    fHtMin   = 0;
    fHtMax   = 2400;
  }
}

void FatJetSoftDropSelection::bookHistograms(TDirectory* dir) {

  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "fatjetSoftDropSelection_"+sPostfix);

  // Histograms (1D)
  
  hFatJetSoftDropPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropPtAll", "Fat Jet SoftDrop pT, all;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hFatJetSoftDropEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropEtaAll", "Fat Jet SoftDrop  #eta, all;#eta", nEtaBins, fEtaMin, fEtaMax);
  hFatJetSoftDropSubjetsAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropSubjetsAll", "Fat Jet SoftDrop subjets multiplicity", 10, 0, 10);
  hFatJetSoftDropHasBSubjetAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropHasBSubjetAll", "Fat Jet SoftDrop has B-Subjet", 2, 0, 2); 
  
  hFatJetSoftDropPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropPtPassed", "Fat Jet SoftDrop pT, passed;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax);
  hFatJetSoftDropEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropEtaPassed", "Fat Jet SoftDrop Eta, passed", nEtaBins, fEtaMin, fEtaMax);
  hFatJetSoftDropSubjetsPassed    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropSubjetsPassed", "Fat Jet SoftDrop subjets multiplicity", 10, 0, 10);
  hFatJetSoftDropHasBSubjetPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "fatjetSoftDropHasBSubjetPassed", "Fat Jet SoftDrop has B-Subjet", 2, 0, 2);
  
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFirstJetPt"  , "First fat SoftDrop jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSecondJetPt" , "Second fat SoftDrop jet pT;p_{T} (GeV/c)" , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropThirdJetPt"  , "Third fat SoftDrop jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFourthJetPt" , "Fourth fat SoftDrop jet pT;p_{T} (GeV/c)" , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFifthJetPt"  , "Fifth fat SoftDrop jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSixthJetPt"  , "Sixth fat SoftDrop jet pT;p_{T} (GeV/c)"  , nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSeventhJetPt", "Seventh fat SoftDrop jet pT;p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFirstJetEta"  , "First fat SoftDrop jet #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSecondJetEta" , "Second fat jet SoftDrop #eta;#eta" , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropThirdJetEta"  , "Third fat jet SoftDrop #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFourthJetEta" , "Fourth fat jet SoftDrop #eta;#eta" , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropFifthJetEta"  , "Fifth fat jet SoftDrop #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSixthJetEta"  , "Sixth fat jet SoftDrop #eta;#eta"  , nEtaBins, fEtaMin, fEtaMax) );
  hSelectedFatJetSoftDropEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedFatJetsSoftDropSeventhJetEta", "Seventh fat jet SoftDrop #eta;#eta", nEtaBins, fEtaMin, fEtaMax) );
  hFatJetSoftDropMatchingToTauDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetSoftDropMatchingToTauDeltaR" , "#DeltaR(fat jet SoftDrop, #tau)", 40, 0, 2);
  hFatJetSoftDropMatchingToTauPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetSoftDropMatchingToTauPtRatio", "fat jet SoftDrop pT / #tau pT", 40, 0, 2);

  hHTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "HTAll"    , ";H_{T}",  nHtBins, fHtMin, fHtMax); 
  hJTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JTAll"    , ";J_{T}",  nHtBins, fHtMin, fHtMax); 
  hMHTAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "MHTAll"   , ";MHT"  ,  50, 0.0,  500.0);
  hHTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "HTPassed" , ";H_{T}",  nHtBins, fHtMin, fHtMax); 
  hJTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JTPassed" , ";J_{T}",  nHtBins, fHtMin, fHtMax); 
  hMHTPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "MHTPassed", ";MHT"  ,  50, 0.0,  500.0);
  
  
  return;
}

FatJetSoftDropSelection::Data FatJetSoftDropSelection::silentAnalyze(const Event& event, const Tau& tau) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, tau.p4(), tau.pt());
  enableHistogramsAndCounters();
  return myData;
}

FatJetSoftDropSelection::Data FatJetSoftDropSelection::silentAnalyzeWithoutTau(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  Data myData = privateAnalyze(event, tauP, -1.0);
  enableHistogramsAndCounters();
  return myData;
}

FatJetSoftDropSelection::Data FatJetSoftDropSelection::analyze(const Event& event, const Tau& tau) {
  ensureAnalyzeAllowed(event.eventID());
  FatJetSoftDropSelection::Data data = privateAnalyze(event, tau.p4(), tau.pt());
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr)
  // fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSoftDropSelection::Data FatJetSoftDropSelection::analyzeWithoutTau(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  FatJetSoftDropSelection::Data data = privateAnalyze(event, tauP, -1.);
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr)
  // fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSoftDropSelection::Data FatJetSoftDropSelection::privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  Data output;

  cSubAll.increment();
  
  bool passedFatJetSoftDropID = false;
  bool passedFatJetSoftDropPUID = false;
  bool passedDeltaRMatchWithTau = false;
  bool passedEta = false;
  bool passedPt  = false;
  unsigned int jet_index    = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;
  
  // For-loop: All jets (pT-sorted)
  for(AK8JetsSoftDrop jet: event.ak8jetsSoftDrop())
    {
      // Jet index (for pT and eta cuts)
      jet_index++;
      
      //=== Apply cut on jet ID
      if (!jet.jetIDDiscriminator())
	continue;
      passedFatJetSoftDropID = true;
      
      //=== Apply cut on jet PU ID
      if (!jet.jetPUIDDiscriminator())
	continue;
      passedFatJetSoftDropPUID = true;
      output.fAllFatJetsSoftDrop.push_back(jet);   
      
      hFatJetSoftDropPtAll         -> Fill(jet.pt());
      hFatJetSoftDropEtaAll        -> Fill(jet.eta());
      hFatJetSoftDropSubjetsAll    -> Fill(jet.nSubjets());
      hFatJetSoftDropHasBSubjetAll -> Fill(jet.hasBTagSubjets());

      //=== Apply cut on tau radius
      //if (tauPt > 0.0) {
      //double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
      //// hFatJetMatchingToTauDeltaR->Fill(myDeltaR);
      //	if (myDeltaR < fTauMatchingDeltaR)
      //continue;
      //	passedDeltaRMatchWithTau = true;
      //}
      
      
      //=== Apply cut on eta
      const float jetEtaCut = fFatJetSoftDropEtaCuts.at(etaCut_index);
      //std::cout << jet_index << ") abs(eta)["<< etaCut_index << "] > " << jetEtaCut << " ( " << jet.eta() << ")" << std::endl;
      if (std::fabs(jet.eta()) > jetEtaCut)
	continue;
      passedEta = true;
      
      
      //=== Apply cut on pt   
      const float jetPtCut = fFatJetSoftDropPtCuts.at(ptCut_index);
      //std::cout << jet_index << ") pT["<< ptCut_index << "] > " << jetPtCut << " GeV/c ( " << jet.pt() << ")" << std::endl;
      if (jet.pt() < jetPtCut)
	continue;
      passedPt = true;
      
      // Fat Jet passed all cuts   
      output.fSelectedFatJetsSoftDrop.push_back(jet);
      hFatJetSoftDropPtPassed         -> Fill(jet.pt());
      hFatJetSoftDropEtaPassed        -> Fill(jet.eta());
      hFatJetSoftDropSubjetsPassed    -> Fill(jet.nSubjets());
      hFatJetSoftDropHasBSubjetPassed -> Fill(jet.hasBTagSubjets());
      
      // Increment cut index only. Cannot be bigger than the size of the cut list provided
      if (ptCut_index  < fFatJetSoftDropPtCuts.size()-1  ) ptCut_index++;
      if (etaCut_index < fFatJetSoftDropEtaCuts.size()-1 ) etaCut_index++;
      //std::cout << jet_index+1 << ") pT = " << jet.pt() << std::endl;
      //std::cout << jet_index+1 << ") |eta| = " << jet.eta() << std::endl;
    }
  
  // Fill counters so far
  if (passedFatJetSoftDropID)
    cSubPassedFatJetSoftDropID.increment();
  if (passedFatJetSoftDropPUID)
    cSubPassedFatJetSoftDropPUID.increment();
  if (passedDeltaRMatchWithTau)
    cSubPassedDeltaRMatchWithTau.increment();
  if (passedEta)
    cSubPassedEta.increment();
  if (passedPt)
    cSubPassedPt.increment();
  
  //=== Apply cut on number of jets
  if (!fNumberOfFatJetsSoftDropCut.passedCut(output.fSelectedFatJetsSoftDrop.size()))
    return output;
  cSubPassedFatJetSoftDropCount.increment();
  
  // Sort fat jets by pT (descending order)
  std::sort(output.fSelectedFatJetsSoftDrop.begin(), output.fSelectedFatJetsSoftDrop.end());
  
  // Calculate HT
  output.fHT = 0.0;
  for(AK8JetsSoftDrop jet: output.getSelectedFatJetsSoftDrop()) 
    {
      // std::cout << "pT = " << jet.pt() << ", eta = " << jet.eta() << std::endl;
      output.fHT += jet.pt();
    }
  if (tauPt > 0.0) output.fHT += tauPt;
  hHTAll->Fill(output.fHT);
  /*
  // Calculate JT
  output.fJT = output.fHT - output.fSelectedFatJetsSoftDrop.at(0).pt();
  hJTAll->Fill(output.fJT);
  //=== Apply cut on HT
  if (!fHTCut.passedCut(output.fHT)) return output;
  cSubPassedHT.increment();
  hHTPassed->Fill(output.fHT);
  //=== Apply cut on JT
  if (!fJTCut.passedCut(output.fJT)) return output;
  cSubPassedJT.increment();
  hJTPassed->Fill(output.fJT);

  // Calculate MHT
  calculateMHTInformation(output, tauP, tauPt);
  hMHTAll->Fill(output.fMHTvalue);
  //=== Apply cut on MHT
  if (!fMHTCut.passedCut(output.fMHTvalue)) return output;
  cSubPassedMHT.increment();
  hMHTPassed->Fill(output.fMHTvalue);
  */
  
  
  //=== Passed all fat jet selections
  output.bPassedSelection = true;
  cPassedFatJetSoftDropSelection.increment();
  

  // Find jet matched to tau
  //if (tauPt > 0.0) {
  //  findFatJetSoftDropMatchingToTau(output.fFatJetSoftDropMatchedToTau, event, tauP);
  //  if (output.fatjetSoftDropMatchedToTauFound()) {
  //hFatJetMatchingToTauPtRatio->Fill(tauPt / output.getFatJetMatchedToTau().pt());
  //  }
  // }
  
  // Fill pt and eta of jets
  size_t i = 0;
  for (AK8JetsSoftDrop jet: output.fSelectedFatJetsSoftDrop) {
    if (i < 6) {
      hSelectedFatJetSoftDropPt[i]->Fill(jet.pt());
      hSelectedFatJetSoftDropEta[i]->Fill(jet.eta());
    }
    ++i;
  }  


  // Return data object
  return output;
}

void FatJetSoftDropSelection::findFatJetSoftDropMatchingToTau(std::vector<AK8JetsSoftDrop>& collection, const Event& event, const math::LorentzVectorT<double>& tauP) {
  double myMinDeltaR = 9999;
  size_t mySelectedIndex = 9999;
  size_t i = 0;
  for(AK8JetsSoftDrop jet: event.ak8jetsSoftDrop()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
    if (myDeltaR < myMinDeltaR) {
      myMinDeltaR = myDeltaR;
      mySelectedIndex = i;
    }
    i += 1;
  }
  if (myMinDeltaR < 0.1)
    collection.push_back(event.ak8jetsSoftDrop()[mySelectedIndex]);
}

void FatJetSoftDropSelection::calculateMHTInformation(FatJetSoftDropSelection::Data& output, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  // Construct a list of the jet four momenta for speeding up calculations and for simplifying code
  std::vector<math::LorentzVectorT<double>> fourMomenta;
  for(AK8JetsSoftDrop jet: output.getSelectedFatJetsSoftDrop()) {
    fourMomenta.push_back(jet.p4());
  }
  if (tauPt > 0.0) {
    fourMomenta.push_back(tauP);
  }
  // Calculate MHT (negative vector sum of selected jets and the tau)
  // I.e. not as sensitive as MET to forward calorimetry
  output.fMHT.SetXYZ(0.0, 0.0, 0.0);
  for(auto& p: fourMomenta) {
    output.fMHT.SetXYZ(output.fMHT.x() - p.x(),
                       output.fMHT.y() - p.y(),
                       output.fMHT.z() - p.z());
  }
  output.fMHTvalue = std::sqrt(output.fMHT.Perp2());

  // Calculate the minimum and maximum DeltaPhi and DeltaR of the jet/tau, MHT-jet/tau system
  // I.e. look for events with collinear or back-to-back topologies architypal of QCD multi-jet events
  output.fMinDeltaPhiFatJetSoftDropMHT = 9999.0;
  output.fMaxDeltaPhiFatJetSoftDropMHT = -1.0;
  output.fMinDeltaRFatJetSoftDropMHT = 9999.0;
  output.fMinDeltaRReversedFatJetSoftDropMHT = 9999.0;
  for(auto& p: fourMomenta) {
    math::XYZVectorD modifiedMHT = output.MHT();
    modifiedMHT.SetXYZ(output.fMHT.x() + p.x(),
                       output.fMHT.y() + p.y(),
                       output.fMHT.z() + p.z());
    double deltaPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(p, modifiedMHT));
    if (deltaPhi < output.fMinDeltaPhiFatJetSoftDropMHT) {
      output.fMinDeltaPhiFatJetSoftDropMHT = deltaPhi;
    }
    if (deltaPhi > output.fMaxDeltaPhiFatJetSoftDropMHT) {
      output.fMaxDeltaPhiFatJetSoftDropMHT = deltaPhi;
    }
    double deltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (deltaR < output.fMinDeltaRFatJetSoftDropMHT) {
      output.fMinDeltaRFatJetSoftDropMHT = deltaR;
    }
    // Reverse one of the vectors and calculate DeltaR; small DeltaR means the system is back-to-back
    modifiedMHT.SetXYZ(-output.fMHT.x(),
                       -output.fMHT.y(),
                       -output.fMHT.z());
    double reversedSystemDeltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (reversedSystemDeltaR < output.fMinDeltaRReversedFatJetSoftDropMHT) {
      output.fMinDeltaRReversedFatJetSoftDropMHT = reversedSystemDeltaR;
    }
  }

  return;
}
