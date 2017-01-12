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
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
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
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
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
}

void BJetSelection::initialize(const ParameterSet& config) {
  // Obtain algorithm and working point
  std::string sAlgorithm = config.getParameter<std::string>("bjetDiscr");
  std::string sWorkingPoint = config.getParameter<std::string>("bjetDiscrWorkingPoint");
  // Decypher the actual discriminator value
  if (sWorkingPoint != "Loose" && sWorkingPoint != "Medium" && sWorkingPoint != "Tight")
    throw hplus::Exception("config") << "b-tagging algorithm working point '" << sWorkingPoint
                                     << "' is not valid!\nValid values are: Loose, Medium, Tight";

  if (sAlgorithm == "pfCombinedInclusiveSecondaryVertexV2BJetTags") {
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco (Moriond17)
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = 0.5426;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.8484;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.9535;
  } else if (sAlgorithm == "pfCombinedMVA2BJetTags") {
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = -0.5884;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.4432;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.9432;
  } else if (sAlgorithm == "pfCombinedCvsLJetTags") {
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = -0.48;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = -0.1;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.69;    
  } else if (sAlgorithm == "pfCombinedCvsBJetTags") {
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = -0.17;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.08;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = -0.45; 
    // Note: Events selected by the Tight WP are not a subsample of the events selected by the Medium WP, but it is because they WP definition have different goals:
    // Loose to reduce b jets
    // Medium to reduce both b and light jets
    // Tight to reduce light jets
  }
  
  if (fDisriminatorValue < 0.0) {
    throw hplus::Exception("config") << "No discriminator value implemented in BJetSelection.cc constructor for algorithm '" << sAlgorithm
                                     << "' and working point '" << sWorkingPoint << "'!";
  }
}

void BJetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "bjetSelection_"+sPostfix);
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetPt" , "First b-jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetPt", "Second b-jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsThirdJetPt" , "Third b-jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFourthJetPt", "Fourth b-jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetEta" , "First b-jet eta;#eta" , 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetEta", "Second b-jet eta;#eta", 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsThirdJetEta" , "Third b-jet eta;#eta" , 50, -2.5, 2.5) );
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFourthJetEta", "Fourth b-jet eta;#eta", 50, -2.5, 2.5) );
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
  bool passedPt = false;
  bool passedDisr = false;
  // Loop over muons
  for(const Jet& jet: jetData.getSelectedJets()) {
    // jet pt and eta cuts can differ from the jet selection
    //=== Apply cut on eta   
    if (std::fabs(jet.eta()) > fJetEtaCut)
      continue;
    passedEta = true;  
    //=== Apply cut on pt
    if (jet.pt() < fJetPtCut)
      continue;
    passedPt = true;
    //=== Apply discriminator
    if (!(jet.bjetDiscriminator() > fDisriminatorValue))
      continue;
    passedDisr = true;
    // jet identified as b jet
    output.fSelectedBJets.push_back(jet);
  }
  // Fill counters so far
  if (passedEta&&passedPt&&passedDisr)
    cSubPassedDiscriminator.increment();
  //=== Apply cut on number of selected b jets
  if (!fNumberOfJetsCut.passedCut(output.getNumberOfSelectedBJets()))
    return output;
  //=== Passed b-jet selection
  output.bPassedSelection = true;
  cPassedBJetSelection.increment();
  std::sort(output.fSelectedBJets.begin(), output.fSelectedBJets.end());
  cSubPassedNBjets.increment();
  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedBJets) {
    if (i < 4) {
      hSelectedBJetPt[i]->Fill(jet.pt());
      hSelectedBJetEta[i]->Fill(jet.eta());
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
