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
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "All events")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed discriminator")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed Nbjets"))
{
  initialize(config);
}

BJetSelection::BJetSelection(const ParameterSet& config)
: BaseSelection(),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(fEventCounter.addCounter("passed b-jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection", "All events")),
  cSubPassedDiscriminator(fEventCounter.addSubCounter("bjet selection", "Passed discriminator")),
  cSubPassedNBjets(fEventCounter.addSubCounter("bjet selection", "Passed Nbjets"))
{
  initialize(config);
}

BJetSelection::~BJetSelection() { }

void BJetSelection::initialize(const ParameterSet& config) {
  // Obtain algorithm and working point
  std::string sAlgorithm = config.getParameter<std::string>("bjetDiscr");
  std::string sWorkingPoint = config.getParameter<std::string>("bjetDiscrWorkingPoint");
  // Decypher the actual discriminator value
  if (sWorkingPoint != "Loose" && sWorkingPoint != "Medium" && sWorkingPoint != "Tight")
    throw hplus::Exception("config") << "b-tagging algorithm working point '" << sWorkingPoint
                                     << "' is not valid!\nValid values are: Loose, Medium, Tight";
  if (sAlgorithm == "pfCombinedInclusiveSecondaryVertexV2BJetTags") {
    // Oct 2015 https://indico.cern.ch/event/455330/session/1/contribution/173/attachments/1175466/1699105/DMajumder_CMSWeek22Oct_BTVReport_v1.pdf
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = 0.605;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.890;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.970;
  } else if (sAlgorithm == "pfCombinedSecondaryVertexBJetTags") {
    // Run 1 legacy values
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = 0.244;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.679;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.898;
  } else if (sAlgorithm == "pfJetProbabilityBJetTags") {
    // Oct 2015 https://indico.cern.ch/event/455330/session/1/contribution/173/attachments/1175466/1699105/DMajumder_CMSWeek22Oct_BTVReport_v1.pdf
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = 0.275;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.545;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.790;    
  }
  
  if (fDisriminatorValue < 0.0) {
    throw hplus::Exception("config") << "No discriminator value implemented in BJetSelection.cc constructor for algorithm '" << sAlgorithm
                                     << "' and working point '" << sWorkingPoint << "'!";
  }
}

void BJetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "bjetSelection_"+sPostfix);
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetPt", "First b-jet pT", 40, 0, 400));
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetPt", "Second b-jet pT", 40, 0, 400));
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetEta", "First b-jet #eta", 50, -2.5, 2.5));
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetEta", "Second b-jet #eta", 50, -2.5, 2.5));
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
  bool passedDisr = false;
  // Loop over muons
  for(Jet jet: jetData.getSelectedJets()) {
    // jet pt and eta cuts expected to be the same like for the selected jets for simplicity
    //=== Apply discriminator
    if (!(jet.bjetDiscriminator() > fDisriminatorValue))
      continue;
    passedDisr = true;
    // jet identified as b jet
    output.fSelectedBJets.push_back(jet);
  }
  // Fill counters so far
  if (passedDisr)
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
    if (i < 2) {
      hSelectedBJetPt[i]->Fill(jet.pt());
      hSelectedBJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }
  
  // Calculate and store b-jet scale factor weight and it's uncertainty
  // FIXME to be implemented
  
  // Calculate probability for passing b tag cut without actually applying the cut
  output.fBTaggingPassProbability = calculateBTagPassingProbability(iEvent, jetData);
  
  // Return data object
  return output;
}

double BJetSelection::calculateBTagPassingProbability(const Event& iEvent, const JetSelection::Data& jetData) {
  // FIXME to be implemented
  return 1.0;
}