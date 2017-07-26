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
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "bjetSelection_"+sPostfix);

  const int  nBinsBDisc = 10;
  const float minBDisc = 0.0;
  const float maxBDisc = 10.0;
  if (fCommonPlots != nullptr) {  
    nBinsBDisc= fCommonPlots->getBJetDiscBinSettings().bins();
    minBDisc = fCommonPlots->getBJetDiscBinSettings().min();
    maxBDisc = fCommonPlots->getBJetDiscBinSettings().max();
  }

  hTriggerMatchDeltaR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatchDeltaR", "Trigger match #DeltaR;#DeltaR", 60, 0, 3.);
  hTriggerMatches     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatches"    , "trigger-matched objects multiplicity; Multiplicity", 20, 0, 20.);
  hTriggerBJets       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerBJets"      , "trigger object multiplicity; Multiplicity", 20, 0, 20.);
  
  hTriggerMatchedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedLdgBJetPt"   , "Ldg trigger matched b-jet pT;p_{T} (GeV/c)"   , 50, 0.0, 500.0) );
  hTriggerMatchedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedSubldgBJetPt", "Subldg trigger matched b-jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hTriggerMatchedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedLdgBJetEta"   , "Ldg trigger matched b-jet eta;#eta"   , 50, -2.5, 2.5) );
  hTriggerMatchedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "triggerMatchedSubldgBJetEta", "Subldg trigger matched b-jet eta;#eta", 50, -2.5, 2.5) );

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
  int trgMatches            = 0;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;
  const int nTrgBJets       = iEvent.triggerBJets().size(); // max number of trigger objects in OR trigger

  // Cache vector of trigger bjet 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerBJetMomenta;
  
  if (bTriggerMatchingApply)
    {
      for (auto p: iEvent.triggerBJets()) 
	{
	  // std::cout << "HLTBJet: pt eta phi = " <<  p.pt() << ", " << p.eta() << ", " << p.phi() << std::endl;      
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
      else passedTrgMatching = (trgMatches == nTrgBJets);
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
  
  // Return data object
  return output;
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
  double myMinDeltaR = 9999.0;
  double myDeltaR    = 9999.0;

  // For-loop: All HLTBJets
  for (auto& p: trgBJets) 
    {
      myDeltaR    = ROOT::Math::VectorUtil::DeltaR(p, bjet.p4());
      myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
      
    }
  // Fill histograms
  hTriggerMatchDeltaR->Fill(myMinDeltaR);

  return (myMinDeltaR < fTriggerMatchingCone);
}

void BJetSelection::SortFailedBJetsCands(Data &output, std::vector<math::LorentzVectorT<double>> myTriggerBJetMomenta)
{
  
  // Copy the failed bjet candidates vector
  output.fFailedBJetCandsDescendingDiscr = output.fFailedBJetCands;
  output.fFailedBJetCandsAscendingDiscr  = output.fFailedBJetCands;
  output.fFailedBJetCandsShuffled        = output.fFailedBJetCands;

  // Sort by descending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsDescendingDiscr.begin(), output.fFailedBJetCandsDescendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() > b.bjetDiscriminator();});

  // Sort jets by ascending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  std::sort(output.fFailedBJetCandsAscendingDiscr.begin(), output.fFailedBJetCandsAscendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() < b.bjetDiscriminator();});

  // Sort randomly (https://stackoverflow.com/questions/6926433/how-to-shuffle-a-stdvector)
  std::random_shuffle(output.fFailedBJetCandsShuffled.begin(), output.fFailedBJetCandsShuffled.end());

  // Default sort: first all trg-matched objects (if any) then randomly
  output.fFailedBJetCands = output.fFailedBJetCandsShuffled;
  
  // Now put the trg-matched objects in the front
  for (auto it = output.fFailedBJetCands.begin(); it != output.fFailedBJetCands.end(); ++it) 
    {
      if (!this->passTrgMatching(*it, myTriggerBJetMomenta)) continue;
      auto jet = *it;
      output.fFailedBJetCands.erase(it);
      output.fFailedBJetCands.insert(output.fFailedBJetCands.begin(), jet);
    }
    
  return;
}
