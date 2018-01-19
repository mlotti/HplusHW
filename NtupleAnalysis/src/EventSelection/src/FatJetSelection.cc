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
  fFatJetMatchedToTau(0),
  fHT(-1.0),
  fMHTvalue(-1.0),
  fMinDeltaPhiFatJetMHT(-1.0),
  fMaxDeltaPhiFatJetMHT(-1.0),
  fMinDeltaRFatJetMHT(-1.0),
  fMinDeltaRReversedFatJetMHT(-1.0)
{ }

FatJetSelection::Data::~Data() { }

const AK8Jet& FatJetSelection::Data::getFatJetMatchedToTau() const { 
  if (!fatjetMatchedToTauFound())
    throw hplus::Exception("Assert") << "You forgot to check if the fat jet matched to tau exists (fatjetMatchedToTauFound()), this message occurs when none exists!";
  return fFatJetMatchedToTau[0];
}

FatJetSelection::FatJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")),
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")),
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed fat jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("fat jet selection ("+postfix+")", "Passed MHT cut"))
{ 
  initialize(config);
}

FatJetSelection::FatJetSelection(const ParameterSet& config)
: BaseSelection(),
  fFatJetPtCuts(config.getParameter<std::vector<float>>("fatjetPtCuts")), 
  fFatJetEtaCuts(config.getParameter<std::vector<float>>("fatjetEtaCuts")), 
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfFatJetsCut(config, "numberOfFatJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedFatJetSelection(fEventCounter.addCounter("passed fat jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("fat jet selection", "All events")),
  cSubPassedFatJetID(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet ID")),
  cSubPassedFatJetPUID(fEventCounter.addSubCounter("fat jet selection", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("fat jet selection", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("fat jet selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("fat jet selection", "Passed pt cut")),
  cSubPassedFatJetCount(fEventCounter.addSubCounter("fat jet selection", "Passed fat jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("fat jet selection", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("fat jet selection", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("fat jet selection", "Passed MHT cut"))
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
  
  delete hFatJetMatchingToTauDeltaR;
  delete hFatJetMatchingToTauPtRatio;
  delete hHTAll;
  delete hJTAll;
  delete hMHTAll;
  delete hHTPassed;
  delete hJTPassed;
  delete hMHTPassed;
  
  
  }

void FatJetSelection::initialize(const ParameterSet& config) {
  
  // These should be taken from fCommonPlots
  //int nCSVBins;
  //floatfCSVMin, fCSVMax;

  //int ntauBins;
  //floatftauMin, ftauMax;
  
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
  hFatJetMatchingToTauDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTauDeltaR" , "#DeltaR(fat jet, #tau)", 40, 0, 2);
  hFatJetMatchingToTauPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FatJetMatchingToTauPtRatio", "fat jet pT / #tau pT", 40, 0, 2);

  hHTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "HTAll"    , ";H_{T}",  nHtBins, fHtMin, fHtMax); 
  hJTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JTAll"    , ";J_{T}",  nHtBins, fHtMin, fHtMax); 
  hMHTAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "MHTAll"   , ";MHT"  ,  50, 0.0,  500.0);
  hHTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "HTPassed" , ";H_{T}",  nHtBins, fHtMin, fHtMax); 
  hJTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JTPassed" , ";J_{T}",  nHtBins, fHtMin, fHtMax); 
  hMHTPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "MHTPassed", ";MHT"  ,  50, 0.0,  500.0);
  
  
  return;
}

FatJetSelection::Data FatJetSelection::silentAnalyze(const Event& event, const Tau& tau) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, tau.p4(), tau.pt());
  enableHistogramsAndCounters();
  return myData;
}

FatJetSelection::Data FatJetSelection::silentAnalyzeWithoutTau(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  Data myData = privateAnalyze(event, tauP, -1.0);
  enableHistogramsAndCounters();
  return myData;
}

FatJetSelection::Data FatJetSelection::analyze(const Event& event, const Tau& tau) {
  ensureAnalyzeAllowed(event.eventID());
  FatJetSelection::Data data = privateAnalyze(event, tau.p4(), tau.pt());
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    //fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSelection::Data FatJetSelection::analyzeWithoutTau(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  FatJetSelection::Data data = privateAnalyze(event, tauP, -1.);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    //fCommonPlots->fillControlPlotsAtFatJetSelection(event, data);
  // Return data
  return data;
}

FatJetSelection::Data FatJetSelection::privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  Data output;
  
  cSubAll.increment();
  
  bool passedFatJetID = false;
  bool passedFatJetPUID = false;
  bool passedDeltaRMatchWithTau = false;
  bool passedEta = false;
  bool passedPt  = false;
  unsigned int jet_index    = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;
  
  // For-loop: All jets (pT-sorted)
  for(AK8Jet jet: event.ak8jets())
    {
      // Jet index (for pT and eta cuts)
      jet_index++;
      
      //=== Apply cut on jet ID
      if (!jet.jetIDDiscriminator())
	continue;
      passedFatJetID = true;
      
      //=== Apply cut on jet PU ID
      if (!jet.jetPUIDDiscriminator())
	continue;
      passedFatJetPUID = true;
      output.fAllFatJets.push_back(jet);   
      
      hFatJetPtAll->Fill(jet.pt());
      hFatJetEtaAll->Fill(jet.eta());
            
      //=== Apply cut on tau radius
      //if (tauPt > 0.0) {
      //double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
      //// hFatJetMatchingToTauDeltaR->Fill(myDeltaR);
      //	if (myDeltaR < fTauMatchingDeltaR)
      //continue;
      //	passedDeltaRMatchWithTau = true;
      //}
      
      
      //=== Apply cut on eta
      const float jetEtaCut = fFatJetEtaCuts.at(etaCut_index);
      //std::cout << jet_index << ") abs(eta)["<< etaCut_index << "] > " << jetEtaCut << " ( " << jet.eta() << ")" << std::endl;
      if (std::fabs(jet.eta()) > jetEtaCut)
	continue;
      passedEta = true;
      
      
      //=== Apply cut on pt   
      const float jetPtCut = fFatJetPtCuts.at(ptCut_index);
      //std::cout << jet_index << ") pT["<< ptCut_index << "] > " << jetPtCut << " GeV/c ( " << jet.pt() << ")" << std::endl;
      if (jet.pt() < jetPtCut)
	continue;
      passedPt = true;
      
      // Fat Jet passed all cuts   
      output.fSelectedFatJets.push_back(jet);
      hFatJetPtPassed->Fill(jet.pt());
      hFatJetEtaPassed->Fill(jet.eta());
      
      // Increment cut index only. Cannot be bigger than the size of the cut list provided
      if (ptCut_index  < fFatJetPtCuts.size()-1  ) ptCut_index++;
      if (etaCut_index < fFatJetEtaCuts.size()-1 ) etaCut_index++;
      //std::cout << jet_index+1 << ") pT = " << jet.pt() << std::endl;
      //std::cout << jet_index+1 << ") |eta| = " << jet.eta() << std::endl;
    }
  
  // Fill counters so far
  if (passedFatJetID)    cSubPassedFatJetID.increment();
  if (passedFatJetPUID)  cSubPassedFatJetPUID.increment();
  if (passedDeltaRMatchWithTau) cSubPassedDeltaRMatchWithTau.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedPt)  cSubPassedPt.increment();
  
  //=== Apply cut on number of jets
  if (!fNumberOfFatJetsCut.passedCut(output.fSelectedFatJets.size()))
    return output;
  cSubPassedFatJetCount.increment();
  
  // Sort fat jets by pT (descending order)
  std::sort(output.fSelectedFatJets.begin(), output.fSelectedFatJets.end());
  
  
  // Calculate HT
  output.fHT = 0.0;
  for(AK8Jet jet: output.getSelectedFatJets()) 
    {
      // std::cout << "pT = " << jet.pt() << ", eta = " << jet.eta() << std::endl;
      output.fHT += jet.pt();
    }
  if (tauPt > 0.0) output.fHT += tauPt;
  hHTAll->Fill(output.fHT);
  
  /*
  // Calculate JT
  output.fJT = output.fHT - output.fSelectedFatJets.at(0).pt();
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
  cPassedFatJetSelection.increment();
  

  // Find jet matched to tau
  //if (tauPt > 0.0) {
  // findFatJetMatchingToTau(output.fFatJetMatchedToTau, event, tauP);
  //  if (output.fatjetMatchedToTauFound()) {
  //hFatJetMatchingToTauPtRatio->Fill(tauPt / output.getFatJetMatchedToTau().pt());
  //}
  //}
  
  // Fill pt and eta of jets
  size_t i = 0;
  for (AK8Jet jet: output.fSelectedFatJets) {
    if (i < 6) {
      hSelectedFatJetPt[i]->Fill(jet.pt());
      hSelectedFatJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }  


  // Return data object
  return output;
}

void FatJetSelection::findFatJetMatchingToTau(std::vector<AK8Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP) {
  double myMinDeltaR = 9999;
  size_t mySelectedIndex = 9999;
  size_t i = 0;
  for(AK8Jet jet: event.ak8jets()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
    if (myDeltaR < myMinDeltaR) {
      myMinDeltaR = myDeltaR;
      mySelectedIndex = i;
    }
    i += 1;
  }
  if (myMinDeltaR < 0.1)
    collection.push_back(event.ak8jets()[mySelectedIndex]);
}

void FatJetSelection::calculateMHTInformation(FatJetSelection::Data& output, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  // Construct a list of the jet four momenta for speeding up calculations and for simplifying code
  std::vector<math::LorentzVectorT<double>> fourMomenta;
  for(AK8Jet jet: output.getSelectedFatJets()) {
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
  output.fMinDeltaPhiFatJetMHT = 9999.0;
  output.fMaxDeltaPhiFatJetMHT = -1.0;
  output.fMinDeltaRFatJetMHT = 9999.0;
  output.fMinDeltaRReversedFatJetMHT = 9999.0;
  for(auto& p: fourMomenta) {
    math::XYZVectorD modifiedMHT = output.MHT();
    modifiedMHT.SetXYZ(output.fMHT.x() + p.x(),
                       output.fMHT.y() + p.y(),
                       output.fMHT.z() + p.z());
    double deltaPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(p, modifiedMHT));
    if (deltaPhi < output.fMinDeltaPhiFatJetMHT) {
      output.fMinDeltaPhiFatJetMHT = deltaPhi;
    }
    if (deltaPhi > output.fMaxDeltaPhiFatJetMHT) {
      output.fMaxDeltaPhiFatJetMHT = deltaPhi;
    }
    double deltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (deltaR < output.fMinDeltaRFatJetMHT) {
      output.fMinDeltaRFatJetMHT = deltaR;
    }
    // Reverse one of the vectors and calculate DeltaR; small DeltaR means the system is back-to-back
    modifiedMHT.SetXYZ(-output.fMHT.x(),
                       -output.fMHT.y(),
                       -output.fMHT.z());
    double reversedSystemDeltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (reversedSystemDeltaR < output.fMinDeltaRReversedFatJetMHT) {
      output.fMinDeltaRReversedFatJetMHT = reversedSystemDeltaR;
    }
  }

  return;
}
