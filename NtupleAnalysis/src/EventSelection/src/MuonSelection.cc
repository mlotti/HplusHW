// -*- c++ -*-
#include "EventSelection/interface/MuonSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
//#include "Framework/interface/makeTH.h"

MuonSelection::Data::Data() 
: fHighestSelectedMuonPt(0.0),
  fHighestSelectedMuonEta(0.0) { }

MuonSelection::Data::~Data() { }

MuonSelection::MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fMuonPtCut(config.getParameter<float>("muonPtCut")),
  fMuonEtaCut(config.getParameter<float>("muonEtaCut")),
  fRelIsoCut(-1.0),
  fVetoMode(false),
  // Event counter for passing selection
  cPassedMuonSelection(fEventCounter.addCounter("passed mu selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("mu selection ("+postfix+")", "All events")),
  cSubPassedPt(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
}

MuonSelection::MuonSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  fMuonPtCut(config.getParameter<float>("muonPtCut")),
  fMuonEtaCut(config.getParameter<float>("muonEtaCut")),
  fRelIsoCut(-1.0),
  fVetoMode(false),
  // Event counter for passing selection
  cPassedMuonSelection(fEventCounter.addCounter("passed mu selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("mu selection ("+postfix+")", "All events")),
  cSubPassedPt(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}

MuonSelection::~MuonSelection() {
  delete hMuonPtAll;
  delete hMuonEtaAll;
  delete hMuonPtPassed;
  delete hMuonEtaPassed;
  delete hPtResolution;
  delete hEtaResolution;
  delete hPhiResolution;
  delete hIsolPtBefore;
  delete hIsolEtaBefore;
  delete hIsolVtxBefore;
  delete hIsolPtAfter;
  delete hIsolEtaAfter;
  delete hIsolVtxAfter;
}

void MuonSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos)
    fVetoMode = true;
  std::string isolString = config.getParameter<std::string>("muonIsolation");
  if (isolString == "veto" || isolString == "Veto") {
    fRelIsoCut = 0.20; // Based on 2012 isolation
  } else if (isolString == "tight" || isolString == "Tight") {
    fRelIsoCut = 0.12; // Based on 2012 isolation
  } else {
    throw hplus::Exception("config") << "Invalid muonIsolation option '" << isolString << "'! Options: 'veto', 'tight'";
  }  
}

void MuonSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "muSelection_"+sPostfix);
  hMuonPtAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtAll", "Muon pT, all", 40, 0, 400);
  hMuonEtaAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaAll", "Muon eta, all", 50, -2.5, 2.5);
  hMuonPtPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed", "Muon pT, passed", 40, 0, 400);
  hMuonEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaPassed", "Muon eta, passed", 50, -2.5, 2.5);
  // Resolution
  hPtResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution", "(reco pT - gen pT) / reco pT", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi", 200, -1.0, 1.0);
    // Isolation efficiency
  hIsolPtBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore", "Muon pT before isolation is applied", 40, 0, 400);
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore", "Muon eta before isolation is applied", 50, -2.5, 2.5);
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied", 60, 0, 60);
  hIsolPtAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter", "Muon pT before isolation is applied", 40, 0, 400);
  hIsolEtaAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter", "Muon eta before isolation is applied", 50, -2.5, 2.5);
  hIsolVtxAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter", "Nvertices before isolation is applied", 60, 0, 60);
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
  if (fCommonPlotsIsEnabled())
    fCommonPlots->fillControlPlotsAtMuonSelection(event, data);
  // Return data
  return data;
}

MuonSelection::Data MuonSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedPt = false;
  bool passedEta = false;
  bool passedID = false;
  bool passedIsol = false;
  // Loop over muons
  for(Muon muon: event.muons()) {
    hMuonPtAll->Fill(muon.pt());
    hMuonEtaAll->Fill(muon.eta());
    // Apply cut on pt
    if (muon.pt() < fMuonPtCut)
      continue;
    passedPt = true;
    // Apply cut on eta
    if (std::fabs(muon.eta()) > fMuonEtaCut)
      continue;
    passedEta = true;
    // Apply cut on muon ID
    if (!muon.muonIDDiscriminator()) continue;
    passedID = true;
    // Apply cut on muon isolation
    hIsolPtBefore->Fill(muon.pt());
    hIsolEtaBefore->Fill(muon.eta());
    if (fCommonPlotsIsEnabled())
      hIsolVtxBefore->Fill(fCommonPlots->nVertices());
    if (muon.relIsoDeltaBeta() > fRelIsoCut) continue;
    passedIsol = true;
    hIsolPtAfter->Fill(muon.pt());
    hIsolEtaAfter->Fill(muon.eta());
    if (fCommonPlotsIsEnabled())
      hIsolVtxAfter->Fill(fCommonPlots->nVertices());
    // Passed all cuts
    hMuonPtPassed->Fill(muon.pt());
    hMuonEtaPassed->Fill(muon.eta());
    if (muon.pt() > output.fHighestSelectedMuonPt) {
      output.fHighestSelectedMuonPt = muon.pt();
      output.fHighestSelectedMuonEta = muon.eta();
    }
    output.fSelectedMuons.push_back(muon);
    // Fill resolution histograms
    if (event.isMC()) {
      hPtResolution->Fill((muon.pt() - muon.MCmuon()->pt()) / muon.pt());
      hEtaResolution->Fill((muon.eta() - muon.MCmuon()->eta()) / muon.eta());
      hPhiResolution->Fill((muon.phi() - muon.MCmuon()->phi()) / muon.phi());
    }
  }
  // Fill counters
  if (passedPt)
    cSubPassedPt.increment();
  if (passedEta)
    cSubPassedEta.increment();
  if (passedID)
    cSubPassedID.increment();
  if (passedIsol)
    cSubPassedIsolation.increment();
  if (fVetoMode) {
    if (output.fSelectedMuons.size() == 0)
      cPassedMuonSelection.increment();
  } else {
    if (output.fSelectedMuons.size() > 0)
      cPassedMuonSelection.increment();
  }
  // Return data object
  return output;
}
