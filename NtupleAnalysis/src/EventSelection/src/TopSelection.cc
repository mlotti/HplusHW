// -*- c++ -*-
#include "EventSelection/interface/TopSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

TopSelection::Data::Data()
: bPassedSelection(false),
  bHasElectronsOrMuons(false),
  bHasOneLeptonicTopDecay(false),
  bHasTwoleptonicTopDecays(false)
{ }

TopSelection::Data::~Data() { }


TopSelection::TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
//   fJetPtCut(config.getParameter<float>("jetPtCut")),
//   fJetEtaCut(config.getParameter<float>("jetEtaCut")),
//   fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
//   fNumberOfJetsCut(config, "numberOfJetsCut"),
  // Event counter for passing selection
//  cPassedTopSelection(fEventCounter.addCounter("passed jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("jet selection ("+postfix+")", "All events"))
//   cSubPassedJetID(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed jet ID")),
//   cSubPassedJetPUID(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed PU ID")),
//   cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed tau matching")),
//   cSubPassedEta(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed eta cut")),
//   cSubPassedPt(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed pt cut")),
//   cSubPassedJetCount(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed jet number cut"))
{
  initialize(config);
}

TopSelection::TopSelection(const ParameterSet& config)
: BaseSelection(),
//   fJetPtCut(config.getParameter<float>("jetPtCut")),
//   fJetEtaCut(config.getParameter<float>("jetEtaCut")),
//   fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
//   fNumberOfJetsCut(config, "numberOfJetsCut"),
  // Event counter for passing selection
//  cPassedTopSelection(fEventCounter.addCounter("passed jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("jet selection", "All events"))
//   cSubPassedJetID(fEventCounter.addSubCounter("jet selection", "Passed jet ID")),
//   cSubPassedJetPUID(fEventCounter.addSubCounter("jet selection", "Passed PU ID")),
//   cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("jet selection", "Passed tau matching")),
//   cSubPassedEta(fEventCounter.addSubCounter("jet selection", "Passed eta cut")),
//   cSubPassedPt(fEventCounter.addSubCounter("jet selection", "Passed pt cut")),
//   cSubPassedJetCount(fEventCounter.addSubCounter("jet selection", "Passed jet number cut"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}

TopSelection::~TopSelection() { }

void TopSelection::initialize(const ParameterSet& config) {
  
}

void TopSelection::bookHistograms(TDirectory* dir) {
  //TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "topSelection_"+sPostfix);
  //hJetPtAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtAll", "Jet pT, all", 40, 0, 400);
}

TopSelection::Data TopSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData, bjetData);
  enableHistogramsAndCounters();
  return myData;
}

TopSelection::Data TopSelection::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  TopSelection::Data data = privateAnalyze(event, jetData, bjetData);
  // Send data to CommonPlots
  //if (fCommonPlots != nullptr)
  //  fCommonPlots->fillControlPlotsAtTopSelection(event, data);
  // Return data
  return data;
}

TopSelection::Data TopSelection::privateAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  Data output;
  cSubAll.increment();
  //bool passedJetID = false;

//   // Find jets compatible with W
//   for (auto jet1: jetData.getSelectedJets()) {
//     if (matchesToBJet(jet1, bjetData)) continue;
//     for (auto jet2: jetData.getSelectedJets()) {
//       
//     }
//   }
  
  
  //double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
  
  
  // Loop over jets
//   for(Jet jet: event.jets()) {
// 
//   }
//   
  //=== Passed top selection
  output.bPassedSelection = true;

  // Return data object
  return output;
}

bool TopSelection::matchesToBJet(const Jet& jet, const BJetSelection::Data& bjetData) const {
  for (auto bjet: bjetData.getSelectedBJets()) {
    if (std::abs(jet.pt()-bjet.pt()) < 0.0001 && std::abs(jet.eta()-bjet.eta()) < 0.0001)
      return true;
  }
  return false;
}
