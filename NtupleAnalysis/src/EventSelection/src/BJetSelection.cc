// -*- c++ -*-
#include "EventSelection/interface/BJetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
#include "DataFormat/interface/HLTBJet.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"
#include <cmath>

BJetSelection::Data::Data() 
: bPassedSelection(false),
  bIsGenuineB(false),
  fBTaggingScaleFactorEventWeight(1.0),
  fBTaggingPassProbability((1.0))
{ }

BJetSelection::Data::~Data() { }

BJetSelection::BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  bTriggerMatchingApply(config.getParameter<bool>("triggerMatchingApply")),
  fTriggerMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "All events")),
  cSubPassedEta(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed discriminator")),
  cSubPassedTrgMatching(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed Nbjets")),
  fBTagSFCalculator(config)
{
  initialize(config);
}

BJetSelection::BJetSelection(const ParameterSet& config)
: BaseSelection(),
  bTriggerMatchingApply(config.getParameter<bool>("triggerMatchingApply")),
  fTriggerMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection", "All events")),
  cSubPassedEta(fEventCounter.addSubCounter("bjet selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("bjet selection", "Passed pt cut")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection", "Passed discriminator")),
  cSubPassedTrgMatching(fEventCounter.addSubCounter("bjet selection", "Passed trigger matching")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection", "Passed Nbjets")),
  fBTagSFCalculator(config)
{
  initialize(config);
  bookHistograms(new TDirectory());
}

BJetSelection::~BJetSelection() {
  delete hTriggerMatchDeltaR;
  delete hTriggerMatches;
  delete hTriggerBJets;
  for (auto p: hTriggerMatchedBJetPt) delete p;
  for (auto p: hTriggerMatchedBJetEta) delete p;
  delete hTriggerMatchedBJet_dPt;
  delete hTriggerMatchedBJet_dEta;
  delete hTriggerMatchedBJet_dPhi;
  delete hTriggerMatchedBJet_dR;
  for (auto p: hSelectedBJetPt) delete p;
  for (auto p: hSelectedBJetEta) delete p;
  for (auto p: hSelectedBJetBDisc) delete p;
}

void BJetSelection::initialize(const ParameterSet& config) {
  // Obtain algorithm and working point
  std::string sAlgorithm = config.getParameter<std::string>("bjetDiscr");
  std::string sWorkingPoint = config.getParameter<std::string>("bjetDiscrWorkingPoint");

  // Decypher the actual discriminator value
  if (sWorkingPoint != "Loose" && sWorkingPoint != "Medium" && sWorkingPoint != "Tight")
    throw hplus::Exception("config") << "b-tagging algorithm working point '" << sWorkingPoint
                                     << "' is not valid!\nValid values are: Loose, Medium, Tight";

  // Note: Events selected by the Tight WP are not a subsample of the events selected by the Medium WP, but it is because they WP definition have different goals:
  // Loose to reduce b jets
  // Medium to reduce both b and light jets
  // Tight to reduce light jets
  fDisriminatorValue = getDiscriminatorWP(sAlgorithm, sWorkingPoint);
  
  if (fDisriminatorValue < 0.0)
    {
      throw hplus::Exception("config") << "No discriminator value implemented in BJetSelection.cc constructor for algorithm '" 
				       << sAlgorithm << "' and working point '" << sWorkingPoint << "'!";
    }

  return;
}

void BJetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "bjetSelection_" + sPostfix);

  // Histogram binning options
  int  nPtBins      =  50;
  float fPtMin      =   0.0;
  float fPtMax      = 500.0;
  int  nEtaBins     =  50;
  float fEtaMin     =  -5.0;
  float fEtaMax     =  +5.0;
  int  nBinsBDisc   =  10;
  float minBDisc    =   0.0;
  float maxBDisc    =  10.0;
  int nDEtaBins     = 200;   // 100;
  double fDEtaMin   =   0.0;
  double fDEtaMax   =   0.2; //  10;
  int nDPhiBins     = 200;   // 32;
  double fDPhiMin   =   0.0;
  double fDPhiMax   =   0.2; // 3.2;
  int nDRBins       =  50;
  double fDRMin     =   0;
  double fDRMax     =  10;
  // Overwrite binning from cfg file?
  if (fCommonPlots != nullptr) {  
      nPtBins    = 2*fCommonPlots->getPtBinSettings().bins();
      fPtMin     = fCommonPlots->getPtBinSettings().min();
      fPtMax     = 2*fCommonPlots->getPtBinSettings().max();
      
      nEtaBins   = fCommonPlots->getEtaBinSettings().bins();
      fEtaMin    = fCommonPlots->getEtaBinSettings().min();
      fEtaMax    = fCommonPlots->getEtaBinSettings().max();
      
      nBinsBDisc = fCommonPlots->getBJetDiscBinSettings().bins();
      minBDisc   = fCommonPlots->getBJetDiscBinSettings().min();
      maxBDisc   = fCommonPlots->getBJetDiscBinSettings().max();
      
      // nDEtaBins   = fCommonPlots->getDeltaEtaBinSettings().bins();
      // fDEtaMin    = fCommonPlots->getDeltaEtaBinSettings().min();
      // fDEtaMax    = fCommonPlots->getDeltaEtaBinSettings().max();
      
      // nDPhiBins   = fCommonPlots->getDeltaPhiBinSettings().bins();
      // fDPhiMin    = fCommonPlots->getDeltaPhiBinSettings().min();
      // fDPhiMax    = fCommonPlots->getDeltaPhiBinSettings().max();
      
      nDRBins     = fCommonPlots->getDeltaRBinSettings().bins();
      fDRMin      = fCommonPlots->getDeltaRBinSettings().min();
      fDRMax      = fCommonPlots->getDeltaRBinSettings().max();
  }

  hTriggerMatchDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatchDeltaR", "Trigger matched objects #DeltaR;#DeltaR", nDRBins, fDRMin, fDRMax);
  hTriggerMatches     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatches"    , "trigger-matched objects multiplicity; Multiplicity", 20, 0, 20.0);
  hTriggerBJets       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerBJets"      , "trigger object multiplicity; Multiplicity", 20, 0, 20.0);
  
  hTriggerMatchedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir , "triggerMatchedLdgBJetPt"    , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax) );
  hTriggerMatchedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir , "triggerMatchedSubldgBJetPt" , ";p_{T} (GeV/c)", nPtBins, fPtMin, fPtMax) );
  hTriggerMatchedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedLdgBJetEta"   , ";#eta", nEtaBins, fEtaMin, fEtaMax) );
  hTriggerMatchedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedSubldgBJetEta", ";#eta", nEtaBins, fEtaMin, fEtaMax) );

  hTriggerMatchedBJet_dPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedBJets_dPt" , "Trigger-matched objects;#Delta p_{T} (GeV/c)", 200, -100.0, 100.0);
  hTriggerMatchedBJet_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedBJets_dEta", "Trigger-matched objects;#Delta #eta"         , nDEtaBins, fDEtaMin, fDEtaMax);
  hTriggerMatchedBJet_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedBJets_dPhi", "Trigger-matched objects;#Delta #phi (rads)"  , nDPhiBins, fDPhiMin, fDPhiMax);
  hTriggerMatchedBJet_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedBJets_dR"  , "Trigger-matched objects;#Delta R"            , 200, 0.0, 0.2);

  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetPt" , "First b-jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetPt", "Second b-jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsThirdJetPt" , "Third b-jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFourthJetPt", "Fourth b-jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );

  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetEta" , "First b-jet eta;#eta" , 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetEta", "Second b-jet eta;#eta", 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsThirdJetEta" , "Third b-jet eta;#eta" , 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFourthJetEta", "Fourth b-jet eta;#eta", 50, -2.5, 2.5) );

  hSelectedBJetBDisc.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetBDisc" , "First b-jet BDisc;b-tag discriminator" , nBinsBDisc, minBDisc, maxBDisc) );
  hSelectedBJetBDisc.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetBDisc", "Second b-jet BDisc;b-tag discriminator", nBinsBDisc, minBDisc, maxBDisc) );
  hSelectedBJetBDisc.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsThirdJetBDisc" , "Third b-jet BDisc;b-tag discriminator" , nBinsBDisc, minBDisc, maxBDisc) );
  hSelectedBJetBDisc.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFourthJetBDisc", "Fourth b-jet BDisc;b-tag discriminator", nBinsBDisc, minBDisc, maxBDisc) );
  fBTagSFCalculator.bookHistograms(subdir, fHistoWrapper);
}

BJetSelection::Data BJetSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData);
  enableHistogramsAndCounters();
  return myData;
}

BJetSelection::Data BJetSelection::analyze(const Event& event, const JetSelection::Data& jetData) {
  ensureAnalyzeAllowed(event.eventID());
  BJetSelection::Data data = privateAnalyze(event, jetData);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtBtagging(event, data);
  // Return data
  return data;
}

BJetSelection::Data BJetSelection::privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData) {
  Data output;
  cSubAll.increment();
  bool passedNBjets         = false;
  bool passedTrgMatching    = false;
  bool passedEta            = false;
  bool passedPt             = false;
  bool passedDiscr          = false;
  int jet_index             = -1;
  int trgBJets              = 0;
  int trgMatches            = 0;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;
  const int nTrgBJets       = iEvent.triggerBJets().size(); // max number of trigger objects in OR trigger

  // Cache vector of trigger bjet 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerBJetMomenta;
  
  if (bTriggerMatchingApply)
    {

      // std::cout << "" << std::endl;
      for (auto p: iEvent.triggerBJets()) 
	{
	  trgBJets++;
	  // std::cout << "HLTBJet " << trgBJets << "): pt eta phi = " <<  p.pt() << ", " << p.eta() << ", " << p.phi() << std::endl;      
	  myTriggerBJetMomenta.push_back(p.p4());
	}
    }

  // Loop over selected jets
  for(const Jet& jet: jetData.getSelectedJets()) {
    
    // Jet index (for psT and eta cuts)
    // jet pt and eta cuts can differ from the jet selection
    jet_index++;
    

    //=== Apply cut on eta   
    const float jetEtaCut = fJetEtaCuts.at(etaCut_index);
    if (std::fabs(jet.eta()) > jetEtaCut) continue;
    passedEta = true;  

    //=== Apply cut on pt
    const float jetPtCut = fJetPtCuts.at(ptCut_index);
    if (jet.pt() < jetPtCut) continue;
    passedPt = true;

    //=== Apply discriminator. Save failed bjets
    if (!(jet.bjetDiscriminator() > fDisriminatorValue))
      {
	output.fFailedBJetCands.push_back(jet);
	continue;
      }
    else passedDiscr = true;    
      
    //=== Apply trigger matching after saving failed candidates (any trg-matched jets will be given priority in output.fFailedBJetsCands later on)
    if (!this->passTrgMatching(jet, myTriggerBJetMomenta)) continue;
    else
      {
	trgMatches++;

	// Fill histograms for matched objects
	if (trgMatches <= 2)
	  {
	    hTriggerMatchedBJetPt [trgMatches-1]->Fill(jet.pt());
	    hTriggerMatchedBJetEta[trgMatches-1]->Fill(jet.eta());
	  }
      }
    
    // if (trgMatches>trgBJets) std::cout << "\tBAD! trgMatchets = " << trgMatches << ", trgBJets = " << trgBJets << std::endl;
    // else std::cout << "GOOD! trgMatchets = " << trgMatches << ", trgBJets = " << trgBJets << std::endl;

    // jet identified as b jet
    output.fSelectedBJets.push_back(jet);
    
    // Increment cut index only. Cannot be bigger than the size of the cut list provided
    if (ptCut_index  < fJetPtCuts.size()-1  ) ptCut_index++;
    if (etaCut_index < fJetEtaCuts.size()-1 ) etaCut_index++;

  }//eof jet loop

  // BTag SF should be applied before applying fNumberOfJetsCut (so that SF are applied in inverted method)
  if (iEvent.isMC())
    {
      // Calculate and store b-jet scale factor weight and it's uncertainty
      output.fBTaggingScaleFactorEventWeight = fBTagSFCalculator.calculateSF(jetData.getSelectedJets(), output.fSelectedBJets);
  
      // Calculate probability for passing b tag cut without actually applying the cut
      output.fBTaggingPassProbability = calculateBTagPassingProbability(iEvent, jetData);  
    }

  // Fill histograms for matched objects
  hTriggerMatches->Fill(trgMatches);
  hTriggerBJets->Fill(nTrgBJets);

  // Determine if trigger matching requirement is satisfied
  if (passedEta*passedPt*passedDiscr)
    {
      if (!bTriggerMatchingApply) passedTrgMatching = true;
      else passedTrgMatching = (trgMatches >= 1); // fixme: need smarter implementation (according to trigger name)
    }
  
  // Determine if exact number of the selected bjets is found
  if (passedTrgMatching) 
    {
      if (fNumberOfJetsCut.passedCut(output.getNumberOfSelectedBJets())) passedNBjets = true;
    }

  // Fill counters and sub-counters
  if (passedEta) cSubPassedEta.increment();
  if (passedPt) cSubPassedPt.increment();
  if (passedDiscr) cSubPassedDiscriminator.increment();
  if (passedTrgMatching) cSubPassedTrgMatching.increment();
  if (passedNBjets)
    {
      cSubPassedNBjets.increment();
      cPassedBJetSelection.increment();
    }
  
  // Sort failed bjets by descending/ascending b-discriminator value. Then place trg-matched objects first
  SortFailedBJetsCands(output, myTriggerBJetMomenta);

  //=== Apply cut on trigger-matched jets before saving failed jets
  if (!passedTrgMatching) return output;

  //=== Apply cut on number of selected b jets
  if (!passedNBjets) return output;

  //=== Passed b-jet selection
  output.bPassedSelection = true;

  // Sort bjets by pt (Sorting operator defined in Jet.h)
  std::sort(output.fSelectedBJets.begin(), output.fSelectedBJets.end());

  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedBJets) {

    if (i < 4) {
      hSelectedBJetPt[i]->Fill(jet.pt());
      hSelectedBJetEta[i]->Fill(jet.eta());
      hSelectedBJetBDisc[i]->Fill(jet.bjetDiscriminator());
    }
    ++i;
  }
  
  // Store GenuineB boolean (=All selected b-jets are genuine)
  output.bIsGenuineB = _getIsGenuineB(iEvent.isMC(), output.fSelectedBJets);
  
  // Return data object
  return output;
}


bool BJetSelection::_getIsGenuineB(bool bIsMC, const std::vector<Jet>& selectedBjets){
  if (!bIsMC) return false;

  // GenuineB=All selected b-jets in the event are genuine (using jet-flavour from MC)
  unsigned int nFakes=0;
  for(const Jet& bjet: selectedBjets)
    {
      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
      bool isFakeB = (abs(bjet.pdgId()) != 5); // For data pdgId==0
      if (isFakeB) nFakes++;
    }
  return (nFakes==0);
}

double BJetSelection::calculateBTagPassingProbability(const Event& iEvent, const JetSelection::Data& jetData) {
  // FIXME to be implemented
  return 1.0;
}

const double BJetSelection::getDiscriminatorWP(const std::string sAlgorithm, const std::string sWorkingPoint) {

  // Decypher the actual discriminator value
  if (sWorkingPoint != "Loose" && sWorkingPoint != "Medium" && sWorkingPoint != "Tight")
    throw hplus::Exception("logic") << "b-tagging algorithm working point '" << sWorkingPoint
				    << "' is not valid!\nValid values are: Loose, Medium, Tight";

  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco (Moriond17)
  if (sAlgorithm == "pfCombinedInclusiveSecondaryVertexV2BJetTags") 
    {
      if (sWorkingPoint == "Loose") return +0.5426;
      else if (sWorkingPoint == "Medium") return +0.8484;
      else if (sWorkingPoint == "Tight") return +0.9535;
    } 
  else if (sAlgorithm == "pfCombinedMVA2BJetTags") 
    {
      if (sWorkingPoint == "Loose") return -0.5884;
      else if (sWorkingPoint == "Medium") return +0.4432;
      else if (sWorkingPoint == "Tight") return +0.9432;
    }
  else if (sAlgorithm == "pfCombinedCvsLJetTags") 
    {
      if (sWorkingPoint == "Loose") return-0.48;
      else if (sWorkingPoint == "Medium") return -0.1;
      else if (sWorkingPoint == "Tight") return +0.69;    
    } 
  else if (sAlgorithm == "pfCombinedCvsBJetTags") 
    {
      // Note: Events selected by the Tight WP are not a subsample of the events selected by the Medium WP, but it is because they WP definition have different goals:
      // Loose to reduce b jets
      // Medium to reduce both b and light jets
      // Tight to reduce light jets
      if (sWorkingPoint == "Loose") return -0.17;
      else if (sWorkingPoint == "Medium") return +0.08;
      else if (sWorkingPoint == "Tight") return -0.45; 
    }

  throw hplus::Exception("logic") << "Invalid b-tagging algorithm  '" << sAlgorithm << "' with working point (WP) '" << sWorkingPoint << "'."
				  << "\nValid WP values are: Loose, Medium, Tight." 
				  << "\nValid algorithms are: pfCombinedInclusiveSecondaryVertexV2BJetTags, pfCombinedMVA2BJetTags, pfCombinedCvsLJetTags, pfCombinedCvsBJetTags";
  return -1e6;
}

bool BJetSelection::passTrgMatching(const Jet& bjet, std::vector<math::LorentzVectorT<double>>& trgBJets) const {
  if (!bTriggerMatchingApply) return true;

  // http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_8_0_27/doc/html/da/d54/namespacetrigger.html
  double dR_min = 9999.0;
  double dR     = 9999.0;
  double dPt    = 9999.0;
  double dEta   = 9999.0;
  double dPhi   = 9999.0;

  // For-loop: All HLTBJets
  for (auto& p: trgBJets) 
    {
      dR = ROOT::Math::VectorUtil::DeltaR(p, bjet.p4());

      if (dR < dR_min)
	{
	  dR_min = dR;
	  dPt    = bjet.p4().pt() - p.pt();
	  dEta   = std::fabs(bjet.p4().eta() - p.eta());
	  dPhi   = ROOT::Math::VectorUtil::DeltaPhi(p, bjet.p4());
	}      
    }

  // Fill histograms
  hTriggerMatchDeltaR->Fill(dR_min);
  if (0) std::cout << "passed trigger matching = " << (dR_min < fTriggerMatchingCone) << ": dR = " << dR_min << ": dPt = " << dPt << ", dEta = " << dEta << ", dPhi = " << dPhi << std::endl;
  
  bool bIsTrgMatched = (dR_min < fTriggerMatchingCone);
  
  if (bIsTrgMatched)
    {
      hTriggerMatchedBJet_dPt->Fill( dPt );
      hTriggerMatchedBJet_dEta->Fill( dEta );
      hTriggerMatchedBJet_dPhi->Fill( dPhi );
      hTriggerMatchedBJet_dR->Fill( dR_min );
    }

  return bIsTrgMatched;
}

void BJetSelection::SortFailedBJetsCands(Data &output, std::vector<math::LorentzVectorT<double>> myTriggerBJetMomenta)
{
  
  // Copy the failed bjet candidates vector
  output.fFailedBJetCandsDescendingDiscr = output.fFailedBJetCands;
  output.fFailedBJetCandsAscendingDiscr  = output.fFailedBJetCands;
  output.fFailedBJetCandsShuffled        = output.fFailedBJetCands;
  output.fFailedBJetCandsDescendingPt    = output.fFailedBJetCands;
  output.fFailedBJetCandsAscendingPt     = output.fFailedBJetCands;

  // Sort by descending pt value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsDescendingPt.begin(), output.fFailedBJetCandsDescendingPt.end(), [](const Jet& a, const Jet& b){return a.pt() > b.pt();});

  // Sort by ascending pt value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsAscendingPt.begin(), output.fFailedBJetCandsAscendingPt.end(), [](const Jet& a, const Jet& b){return a.pt() < b.pt();});

  // Sort by descending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsDescendingDiscr.begin(), output.fFailedBJetCandsDescendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() > b.bjetDiscriminator();});

  // Sort jets by ascending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsAscendingDiscr.begin(), output.fFailedBJetCandsAscendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() < b.bjetDiscriminator();});

  // Sort randomly (https://stackoverflow.com/questions/6926433/how-to-shuffle-a-stdvector)
  std::random_shuffle(output.fFailedBJetCandsShuffled.begin(), output.fFailedBJetCandsShuffled.end());

  // For Debugging: Test moving the Trigger-Matched jets to the front
  /*
   for (auto it = output.fFailedBJetCands.begin(); it != output.fFailedBJetCands.end(); ++it) 
       {
         auto jet = *it;
         std::cout << "Before) jet.index() = " << jet.index() << ", jet.pt() = " << jet.pt() << std::endl;
       }
     std::cout << "\n" << std::endl;
  */

  
  // Now put the trg-matched objects in the front
  /*
    if (bTriggerMatchingApply)
    {
      for (auto it = output.fFailedBJetCands.begin(); it != output.fFailedBJetCands.end(); ++it) 
	{
	  if (!this->passTrgMatching(*it, myTriggerBJetMomenta)) continue;
	  auto jet = *it;
	  std::cout << "BJetSelection(): WARNING! Degub before using again! Make sure it does what it should!" << std::endl;
	  output.fFailedBJetCands.erase(it);
	  output.fFailedBJetCands.insert(output.fFailedBJetCands.begin(), jet);
	}
    }
  */
  
  // For Debugging: Test moving the Trigger-Matched jets to the front
  /*
    for (auto it = output.fFailedBJetCands.begin(); it != output.fFailedBJetCands.end(); ++it) 
    {
      auto jet = *it;
      std::cout << "After) jet.index() = " << jet.index() << ", jet.pt() = " << jet.pt() << std::endl;
    }
  std::cout << "\n" << std::endl;
  */

  return;
}
