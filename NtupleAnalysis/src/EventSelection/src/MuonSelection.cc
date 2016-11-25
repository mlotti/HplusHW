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
  delete hMuonRelIsoAll;
  delete hMuonPtPassed;
  delete hMuonEtaPassed;
  delete hMuonRelIsoPassed;
  delete hPtResolution;
  delete hEtaResolution;
  delete hPhiResolution;
  delete hIsolPtBefore;
  delete hIsolEtaBefore;
  delete hIsolVtxBefore;
  delete hIsolRelIsoBefore;
  delete hIsolPtAfter;
  delete hIsolEtaAfter;
  delete hIsolVtxAfter;
  delete hIsolRelIsoAfter;
}

void MuonSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos)
    fVetoMode = true;
  std::string isolString = config.getParameter<std::string>("muonIsolation");
  if (isolString == "veto" || isolString == "Veto") {
    fRelIsoCut = 0.15; // Loose iso sync'ed with MIT
  } else if (isolString == "tight" || isolString == "Tight") {
    fRelIsoCut = 0.12; // Based on 2012 isolation
  } else {
    throw hplus::Exception("config") << "Invalid muonIsolation option '" << isolString << "'! Options: 'veto', 'tight'";
  }  
}

void MuonSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "muSelection_"+sPostfix);
  hMuonPtAll         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtAll"       , "Muon pT, all;p_{T} (GeV/c)", 40, 0, 400);
  hMuonEtaAll        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaAll"      , "Muon eta, all;#eta", 50, -2.5, 2.5);
  hMuonRelIsoAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoAll"   , "Muon relative isolation, all;Relative Isolation", 1000, 0.0, 100.0);
  hMuonPtPassed      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed"    , "Muon pT, passed;p_{T} (GeV/c)", 40, 0, 400);
  hMuonEtaPassed     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaPassed"   , "Muon eta, passed;#eta", 50, -2.5, 2.5);
  hMuonRelIsoPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoPassed", "Muon relative isolation, passed;Relative Isolation", 1000, 0.0, 100.0);

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT;(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco}", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta;(#eta^{reco} - #eta^{gen})/#eta^{reco}", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi;(#phi^{reco} - #phi^{gen})/#phi^{reco}", 200, -1.0, 1.0);

  // Isolation efficiency
  hIsolPtBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore"    , "Muon pT before isolation is applied;p_{T} (GeV/c)", 40, 0, 400);
  hIsolEtaBefore    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore"   , "Muon eta before isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxBefore    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore"   , "Nvertices before isolation is applied;Number of Vertices", 60, 0, 60);
  hIsolRelIsoBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoBefore", "Muon relative isolation before isolation is applied;Relative Isolation", 1000, 0.0, 100.0);
  hIsolPtAfter      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter"     , "Muon pT after isolation is applied;p_{T} (GeV/c)", 40, 0, 400);
  hIsolEtaAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter"    , "Muon eta after isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter"    , "Nvertices after isolation is applied;Number of Vertices", 60, 0, 60);
  hIsolRelIsoAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoAfter" , "Muon relative isolation after isolation is applied;Relative Isolation", 1000, 0.0, 100.0);
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
    hMuonRelIsoAll->Fill(muon.relIsoDeltaBeta04());

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
    hIsolRelIsoBefore->Fill(muon.relIsoDeltaBeta04());
    if (fCommonPlotsIsEnabled())
      hIsolVtxBefore->Fill(fCommonPlots->nVertices());

    if (muon.relIsoDeltaBeta04() > fRelIsoCut) continue;
    passedIsol = true;

    hIsolPtAfter->Fill(muon.pt());
    hIsolEtaAfter->Fill(muon.eta());
    hIsolRelIsoAfter->Fill(muon.relIsoDeltaBeta04());

    if (fCommonPlotsIsEnabled())
      hIsolVtxAfter->Fill(fCommonPlots->nVertices());

    // Passed all cuts
    hMuonPtPassed->Fill(muon.pt());
    hMuonEtaPassed->Fill(muon.eta());
    hMuonRelIsoPassed->Fill(muon.relIsoDeltaBeta04());

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
