// -*- c++ -*-
#include "EventSelection/interface/ElectronSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
//#include "Framework/interface/makeTH.h"

ElectronSelection::Data::Data() 
: fHighestSelectedElectronPt(0.0),
  fHighestSelectedElectronEta(0.0) { }

ElectronSelection::Data::~Data() { }

ElectronSelection::ElectronSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fElectronPtCut(config.getParameter<float>("electronPtCut")),
  fElectronEtaCut(config.getParameter<float>("electronEtaCut")),
  fRelIsoCut(-1.0),
  // Event counter for passing selection
  cPassedElectronSelection(eventCounter.addCounter("passed e selection ("+postfix+")")),
  // Sub counters
  cSubAll(eventCounter.addSubCounter("e selection ("+postfix+")", "All events")),
  cSubPassedPt(eventCounter.addSubCounter("e selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(eventCounter.addSubCounter("e selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(eventCounter.addSubCounter("e selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(eventCounter.addSubCounter("e selection ("+postfix+")", "Passed isolation"))
{
  std::string isolString = config.getParameter<std::string>("electronIsolation");
  if (isolString == "veto" || isolString == "Veto") {
    fRelIsoCut = 0.15; // Based on 2012 cut based isolation
  } else if (isolString == "tight" || isolString == "Tight") {
    fRelIsoCut = 0.10; // Based on 2012 cut based isolation
  } else {
    throw hplus::Exception("config") << "Invalid electronIsolation option '" << isolString << "'! Options: 'veto', 'tight'";
  }
}

ElectronSelection::~ElectronSelection() { }

void ElectronSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "eSelection_"+sPostfix);
  hElectronPtAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtAll", "Electron pT, all", 40, 0, 400);
  hElectronEtaAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaAll", "Electron eta, all", 50, -2.5, 2.5);
  hElectronPtPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtPassed", "Electron pT, passed", 40, 0, 400);
  hElectronEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaPassed", "Electron eta, passed", 50, -2.5, 2.5);
  // Resolutions
  hPtResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution", "(reco pT - gen pT) / reco pT", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi", 200, -1.0, 1.0);
  // Isolation efficiency
  hIsolPtBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore", "Electron pT before isolation is applied", 40, 0, 400);
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore", "Electron eta before isolation is applied", 50, -2.5, 2.5);
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied", 60, 0, 60);
  hIsolPtAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter", "Electron pT before isolation is applied", 40, 0, 400);
  hIsolEtaAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter", "Electron eta before isolation is applied", 50, -2.5, 2.5);
  hIsolVtxAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter", "Nvertices before isolation is applied", 60, 0, 60);
}

ElectronSelection::Data ElectronSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();
  return myData;
}

ElectronSelection::Data ElectronSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  ElectronSelection::Data data = privateAnalyze(event);
  // Send data to CommonPlots
  if (fCommonPlotsIsEnabled())
    fCommonPlots->fillControlPlotsAtElectronSelection(event, data);
  // Return data
  return data;
}

ElectronSelection::Data ElectronSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedPt = false;
  bool passedEta = false;
  bool passedID = false;
  bool passedIsol = false;
  // Loop over electrons
  for(Electron electron: event.electrons()) {
    hElectronPtAll->Fill(electron.pt());
    hElectronEtaAll->Fill(electron.eta());
    // Apply cut on pt
    if (electron.pt() < fElectronPtCut)
      continue;
    passedPt = true;
    // Apply cut on eta
    if (std::fabs(electron.eta()) > fElectronEtaCut)
      continue;
    passedEta = true;
    // Apply cut on electron ID
    if (!electron.electronIDDiscriminator()) continue;
    passedID = true;
    // Apply cut on electron isolation
    hIsolPtBefore->Fill(electron.pt());
    hIsolEtaBefore->Fill(electron.eta());
    if (fCommonPlotsIsEnabled())
      hIsolVtxBefore->Fill(fCommonPlots->nVertices());
    if (electron.relIsoDeltaBeta() > fRelIsoCut) continue;
    passedIsol = true;
    hIsolPtAfter->Fill(electron.pt());
    hIsolEtaAfter->Fill(electron.eta());
    if (fCommonPlotsIsEnabled())
      hIsolVtxAfter->Fill(fCommonPlots->nVertices());
    // Passed all cuts
    hElectronPtPassed->Fill(electron.pt());
    hElectronEtaPassed->Fill(electron.eta());
    if (electron.pt() > output.fHighestSelectedElectronPt) {
      output.fHighestSelectedElectronPt = electron.pt();
      output.fHighestSelectedElectronEta = electron.eta();
    }
    output.fSelectedElectrons.push_back(electron);
    // Fill resolution histograms
    if (event.isMC()) {
      hPtResolution->Fill((electron.pt() - electron.MCelectron()->pt()) / electron.pt());
      hEtaResolution->Fill((electron.eta() - electron.MCelectron()->eta()) / electron.eta());
      hPhiResolution->Fill((electron.phi() - electron.MCelectron()->phi()) / electron.phi());
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
  if (sPostfix == "Veto") {
    if (output.fSelectedElectrons.size() == 0)
      cPassedElectronSelection.increment();
  } else {
    if (output.fSelectedElectrons.size() > 0)
      cPassedElectronSelection.increment();
  } 
  // Return data object
  return output;
}
