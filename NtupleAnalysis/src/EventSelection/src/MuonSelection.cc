// -*- c++ -*-
#include "EventSelection/interface/MuonSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
//#include "Framework/interface/makeTH.h"

MuonSelection::Data::Data() 
: fHighestSelectedMuonPt(0.0),
  fHighestSelectedMuonEta(0.0),
  fHighestSelectedMuonPtBeforePtCut(0.0) { }

MuonSelection::Data::~Data() { }

MuonSelection::MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fMuonPtCut(config.getParameter<float>("muonPtCut")),
  fMuonEtaCut(config.getParameter<float>("muonEtaCut")),
  // Event counter for passing selection
  cPassedMuonSelection(eventCounter.addCounter("passed mu selection ("+postfix+")")),
  // Sub counters
  cSubAll(eventCounter.addSubCounter("mu selection ("+postfix+")", "All events")),
  cSubPassedID(eventCounter.addSubCounter("mu selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(eventCounter.addSubCounter("mu selection ("+postfix+")", "Passed isolation")),
  cSubPassedEta(eventCounter.addSubCounter("mu selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(eventCounter.addSubCounter("mu selection ("+postfix+")", "Passed pt cut"))
{ }

MuonSelection::~MuonSelection() { }

void MuonSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "muSelection_"+sPostfix);
  hMuonPtAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtAll", "Muon pT, all", 40, 0, 400);
  hMuonEtaAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaAll", "Muon eta, all", 50, -2.5, 2.5);
  hMuonPtPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed", "Muon pT, passed", 40, 0, 400);
  hMuonEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed", "Muon pT, passed", 40, 0, 400);
}

MuonSelection::Data MuonSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();
  return myData;
}

MuonSelection::Data MuonSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  MuonSelection::Data data = privateAnalyze(event);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtMuonSelection(event, data);
  // Return data
  return data;
}

MuonSelection::Data MuonSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedID = false;
  bool passedIsol = false;
  bool passedEta = false;
  bool passedPt = false;
  // Loop over muons
  for(Muon muon: event.muons()) {
    hMuonPtAll->Fill(muon.pt());
    hMuonEtaAll->Fill(muon.eta());
    // Apply cut on muon ID FIXME to be added
    
    passedID = true;
    // Apply cut on muon isolation FIXME to be added
    
    passedIsol = true;
    // Apply cut on eta
    if (std::fabs(muon.eta()) > fMuonEtaCut)
      continue;
    passedEta = true;
    if (muon.pt() > output.fHighestSelectedMuonPtBeforePtCut)
      output.fHighestSelectedMuonPtBeforePtCut = muon.pt();
    // Apply cut on pt
    if (muon.pt() < fMuonPtCut)
      continue;
    // Passed all cuts
    passedPt = true;
    hMuonPtPassed->Fill(muon.pt());
    hMuonEtaPassed->Fill(muon.eta());
    if (muon.pt() > output.fHighestSelectedMuonPt) {
      output.fHighestSelectedMuonPt = muon.pt();
      output.fHighestSelectedMuonEta = muon.eta();
    }
    output.fSelectedMuons.push_back(muon);
  }
  // Fill counters
  if (passedID)
    cSubPassedID.increment();
  if (passedIsol)
    cSubPassedIsolation.increment();
  if (passedEta)
    cSubPassedEta.increment();
  if (passedPt)
    cSubPassedPt.increment();
  if (sPostfix == "Veto") {
    if (output.fSelectedMuons.size() == 0)
      cPassedMuonSelection.increment();
  } else {
    if (output.fSelectedMuons.size() > 0)
      cPassedMuonSelection.increment();
  }
  // Return data object
  return output;
}
