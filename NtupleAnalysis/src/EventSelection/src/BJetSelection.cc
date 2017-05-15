// -*- c++ -*-
#include "EventSelection/interface/BJetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

BJetSelection::Data::Data() 
: bPassedSelection(false),
  fBTaggingScaleFactorEventWeight(1.0),
  fBTaggingPassProbability((1.0))
{ }

BJetSelection::Data::~Data() { }

BJetSelection::BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "All events")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed discriminator")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed Nbjets")),
  fBTagSFCalculator(config)
{
  initialize(config);
}

BJetSelection::BJetSelection(const ParameterSet& config)
: BaseSelection(),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection", "All events")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection", "Passed discriminator")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection", "Passed Nbjets")),
  fBTagSFCalculator(config)
{
  initialize(config);
  bookHistograms(new TDirectory());
}

BJetSelection::~BJetSelection() {
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

  const int  nBinsBDisc= fCommonPlots->getBJetDiscBinSettings().bins();
  const float minBDisc = fCommonPlots->getBJetDiscBinSettings().min();
  const float maxBDisc = fCommonPlots->getBJetDiscBinSettings().max();

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
  bool passedEta = false;
  bool passedPt  = false;
  bool passedDisr = false;
  unsigned int jet_index    = -1;
  unsigned int ptCut_index  = 0;
  unsigned int etaCut_index = 0;

  // Loop over selected jets
  for(const Jet& jet: jetData.getSelectedJets()) {

    // Jet index (for pT and eta cuts)
    // jet pt and eta cuts can differ from the jet selection
    jet_index++;

    //=== Apply cut on eta   
    const float jetEtaCut = fJetEtaCuts.at(etaCut_index);
    if (std::fabs(jet.eta()) > jetEtaCut)
      {
	output.fFailedBJetCands.push_back(jet);
	continue;
      }
    passedEta = true;  

    //=== Apply cut on pt
    const float jetPtCut = fJetPtCuts.at(ptCut_index);
    if (jet.pt() < jetPtCut)
      {
	output.fFailedBJetCands.push_back(jet);
	continue;
      }
    passedPt = true;

    //=== Apply discriminator
    if (!(jet.bjetDiscriminator() > fDisriminatorValue))
      {
	output.fFailedBJetCands.push_back(jet);
	continue;
      }
    passedDisr = true;

    // jet identified as b jet
    output.fSelectedBJets.push_back(jet);
    // Increment cut index only. Cannot be bigger than the size of the cut list provided
    if (ptCut_index  < fJetPtCuts.size()-1  ) ptCut_index++;
    if (etaCut_index < fJetEtaCuts.size()-1 ) etaCut_index++;
  }

  // Fill counters so far
  if (passedEta&&passedPt&&passedDisr)
    cSubPassedDiscriminator.increment();

  // Sort jets by descending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  output.fFailedBJetCandsDescendingDiscr = output.fFailedBJetCands;
  std::sort(output.fFailedBJetCandsDescendingDiscr.begin(), output.fFailedBJetCandsDescendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() > b.bjetDiscriminator();});

  // Sort jets by ascending b-discriminator value (http://en.cppreference.com/w/cpp/algorithm/sort)
  output.fFailedBJetCandsAscendingDiscr = output.fFailedBJetCands;
  std::sort(output.fFailedBJetCandsAscendingDiscr.begin(), output.fFailedBJetCandsAscendingDiscr.end(), [](const Jet& a, const Jet& b){return a.bjetDiscriminator() < b.bjetDiscriminator();});

  //=== Apply cut on number of selected b jets
  if (!fNumberOfJetsCut.passedCut(output.getNumberOfSelectedBJets()))
    return output;

  //=== Passed b-jet selection
  output.bPassedSelection = true;
  cPassedBJetSelection.increment();
  // Sort bjets by pt (Sortign operator defined in Jet.h)
  std::sort(output.fSelectedBJets.begin(), output.fSelectedBJets.end());
  cSubPassedNBjets.increment();

  // Fill pt and eta of jets
  size_t i = 0;
  //std::cout << "\nSelected bjets:" << std::endl;
  for (Jet jet: output.fSelectedBJets) {
    //std::cout << "\tpT = " << jet.pt() << ", eta = " << jet.eta() << std::endl;
    if (i < 4) {
      hSelectedBJetPt[i]->Fill(jet.pt());
      hSelectedBJetEta[i]->Fill(jet.eta());
      hSelectedBJetBDisc[i]->Fill(jet.bjetDiscriminator());
    }
    ++i;
  }
  
  // Calculate and store b-jet scale factor weight and it's uncertainty
  output.fBTaggingScaleFactorEventWeight = fBTagSFCalculator.calculateSF(jetData.getSelectedJets(), output.fSelectedBJets);
  
  // Calculate probability for passing b tag cut without actually applying the cut
  output.fBTaggingPassProbability = calculateBTagPassingProbability(iEvent, jetData);
  
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
