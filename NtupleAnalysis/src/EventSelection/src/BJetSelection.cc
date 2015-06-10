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
  fBTaggingEventWeight(1.0)
{ }

BJetSelection::Data::~Data() { }

BJetSelection::BJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedBJetSelection(eventCounter.addCounter("passed mu selection ("+postfix+")")),
  // Sub counters
  cSubAll(eventCounter.addSubCounter("bjet selection ("+postfix+")", "All events")),
  cSubPassedDiscriminator(eventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed discriminator")),
  cSubPassedNBjets(eventCounter.addSubCounter("bjet selection ("+postfix+")", "Passed Nbjets"))
{
  // Obtain algorithm and working point
  std::string sAlgorithm = config.getParameter<std::string>("bjetDiscr");
  std::string sWorkingPoint = config.getParameter<std::string>("bjetDiscrWorkingPoint");
  // Decypher the actual discriminator value
  if (sWorkingPoint != "Loose" && sWorkingPoint != "Medium" && sWorkingPoint != "Tight")
    throw hplus::Exception("config") << "b-tagging algorithm working point '" << sWorkingPoint
                                     << "' is not valid!\nValid values are: Loose, Medium, Tight";
  if (sAlgorithm == "combinedInclusiveSecondaryVertexV2BJetTags") {
    // Preliminary values 10.6.2015 from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging
    if (sWorkingPoint == "Loose")
      fDisriminatorValue = 0.423;
    else if (sWorkingPoint == "Medium")
      fDisriminatorValue = 0.814;
    else if (sWorkingPoint == "Tight")
      fDisriminatorValue = 0.941;
  }
  if (fDisriminatorValue < 0.0)
    throw hplus::Exception("config") << "No discriminator value implemented in BJetSelection.cc constructor for algorithm '"
                                     << "' and working point '" << sWorkingPoint << "'!";
}

BJetSelection::~BJetSelection() { }

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
  return privateAnalyze(event, jetData);
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
  // Calculate and store b-jet weight and it's uncertainty
  // FIXME to be implemented
  
  // Return data object
  return output;
}
