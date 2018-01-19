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
  fHighestSelectedMuonPhi(0.0) { }

MuonSelection::Data::~Data() { }

MuonSelection::MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fMuonPtCut(config.getParameter<float>("muonPtCut")),
  fMuonEtaCut(config.getParameter<float>("muonEtaCut")),
  fRelIsoCut(-1.0),
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
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
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
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
  delete hMuonMiniIsoAll;
  
  delete hMuonPtPassed;
  delete hMuonEtaPassed;
  delete hMuonRelIsoPassed;
  delete hMuonMiniIsoPassed;
  
  delete hPtResolution;
  delete hEtaResolution;
  delete hPhiResolution;
  
  delete hIsolPtBefore;
  delete hIsolEtaBefore;
  delete hIsolVtxBefore;
  delete hIsolRelIsoBefore;
  delete hIsolMiniIsoBefore;
  
  delete hIsolPtAfter;
  delete hIsolEtaAfter;
  delete hIsolVtxAfter;
  delete hIsolRelIsoAfter;
  delete hIsolMiniIsoAfter;
}

void MuonSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos)
    {
      fVetoMode = true;
    }
  
  std::string isolString = config.getParameter<std::string>("muonIsolation");
  if (isolString == "veto" || isolString == "Veto") {
    fRelIsoCut  = 0.15; // Loose iso sync'ed with MIT
    fMiniIsoCut = 0.4;  // from Brown/MIT sync
  } 
  else if (isolString == "tight" || isolString == "Tight") {
    fRelIsoCut  = 0.12; // Based on 2012 isolation
    fMiniIsoCut = 0.10; // arbitrary value selected
  } 
  else {
    throw hplus::Exception("config") << "Invalid muonIsolation option '" << isolString << "'! Options: 'veto', 'tight'";
  } 
  
  std::string isolTypeString = config.getParameter<std::string>("muonIsolType");
  if (isolTypeString == "default")  fMiniIsol = false;
  else if (isolTypeString == "mini") fMiniIsol = true;
  else
    {
      throw hplus::Exception("config") << "Invalid muonIsolType option '" << isolTypeString << "'! Options: 'default', 'mini'";
    }
  
  return;
}

void MuonSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "muSelection_"+sPostfix);
  hMuonPtAll         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtAll"        , "Muon pT, all;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hMuonEtaAll        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaAll"       , "Muon eta, all;#eta", 50, -2.5, 2.5);
  hMuonRelIsoAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoAll"    , "Muon relative isolation, all;Relative Isolation", 30, 0.0, 300.0);
  hMuonMiniIsoAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonMiniIsoAll"   , ";relative isolation;Events / %.2f", 300, 0.0, 300.0);
  
  hMuonPtPassed      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed"     , "Muon pT, passed;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hMuonEtaPassed     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaPassed"    , "Muon eta, passed;#eta", 50, -2.5, 2.5);
  hMuonRelIsoPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoPassed" , "Muon relative isolation, passed;Relative Isolation", 100, 0.0, 1.0);
  hMuonMiniIsoPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonMiniIsoPassed", ";relative isolation (mini);Events / %.2f", 100, 0.0, 1.0);
  
  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT;(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco}", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta;(#eta^{reco} - #eta^{gen})/#eta^{reco}", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi;(#phi^{reco} - #phi^{gen})/#phi^{reco}", 200, -1.0, 1.0);

  // Isolation efficiency
  hIsolPtBefore      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore"     , "Muon pT before isolation is applied;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hIsolEtaBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore"    , "Muon eta before isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore"    , "Nvertices before isolation is applied;Number of Vertices", 60, 0, 60);
  hIsolRelIsoBefore  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoBefore" , "Muon relative isolation before isolation is applied;Relative Isolation", 30, 0.0, 300.0);
  hIsolMiniIsoBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoBefore", ";relative isolation (mini);Events / %.2f", 300, 0.0, 300.0);

  hIsolPtAfter      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter"     , "Muon pT after isolation is applied;p_{T} (GeV/c)", 50, 0, 500.0);
  hIsolEtaAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter"    , "Muon eta after isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter"    , "Nvertices after isolation is applied;Number of Vertices", 60, 0, 60);
  hIsolRelIsoAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoAfter" , "Muon relative isolation after isolation is applied;Relative Isolation", 100, 0.0, 1.0);
  hIsolMiniIsoAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoAfter", ";relative isolation (mini);Events / %.2f", 100, 0.0, 1.0);
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
    hMuonMiniIsoAll->Fill(muon.effAreaMiniIso());
    
    // Apply cut on pt
    if (muon.pt() < fMuonPtCut) continue;
    passedPt = true;

    // Apply cut on eta
    if (std::fabs(muon.eta()) > fMuonEtaCut) continue;
    passedEta = true;
    
    // Apply cut on muon ID
    if (!muon.muonIDDiscriminator()) continue;
    passedID = true;
    
    // Fill histograms before isolation cut
    hIsolPtBefore->Fill(muon.pt());
    hIsolEtaBefore->Fill(muon.eta());
    hIsolRelIsoBefore->Fill(muon.relIsoDeltaBeta04());
    hIsolMiniIsoAfter->Fill(muon.effAreaMiniIso());
    if (fCommonPlotsIsEnabled())
      {
	hIsolVtxBefore->Fill(fCommonPlots->nVertices());
      }
    
    // Apply cut on muon isolation
    bool passedRelIso  = (muon.relIsoDeltaBeta04() < fRelIsoCut);
    bool passedMiniIso = (muon.effAreaMiniIso() < fMiniIsoCut);
    bool passedIsolCut = false;
    if (fMiniIsol) passedIsolCut = passedMiniIso;
    else passedIsolCut = passedRelIso;
    if (!passedIsolCut) continue;
    passedIsol = true;
    
    // Fill histograms after isolation cut
    hIsolPtAfter->Fill(muon.pt());
    hIsolEtaAfter->Fill(muon.eta());
    hIsolRelIsoAfter->Fill(muon.relIsoDeltaBeta04());
    hIsolMiniIsoAfter->Fill(muon.effAreaMiniIso());
    if (fCommonPlotsIsEnabled())
      {
	hIsolVtxAfter->Fill(fCommonPlots->nVertices());
      }
    
    // Fill histograms after all cuts
    hMuonPtPassed->Fill(muon.pt());
    hMuonEtaPassed->Fill(muon.eta());
    hMuonRelIsoPassed->Fill(muon.relIsoDeltaBeta04());
    hMuonMiniIsoPassed->Fill(muon.effAreaMiniIso());
    
    // Save the highest pt muon
    if (muon.pt() > output.fHighestSelectedMuonPt) {
      output.fHighestSelectedMuonPt = muon.pt();
      output.fHighestSelectedMuonEta = muon.eta();
      output.fHighestSelectedMuonPhi = muon.phi();
    }
    
    // Save all electrons surviving the cuts
    output.fSelectedMuons.push_back(muon);

    // Fill resolution histograms
    if (event.isMC()) 
      {
	hPtResolution->Fill((muon.pt() - muon.MCmuon()->pt()) / muon.pt());
	hEtaResolution->Fill((muon.eta() - muon.MCmuon()->eta()) / muon.eta());
	hPhiResolution->Fill((muon.phi() - muon.MCmuon()->phi()) / muon.phi());
      }
  } //for-loop: muons
  
  // Fill counters
  if (passedPt) cSubPassedPt.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedID) cSubPassedID.increment();
  if (passedIsol) cSubPassedIsolation.increment();
  if (fVetoMode) 
    {
      if (output.fSelectedMuons.size() == 0) cPassedMuonSelection.increment();
    } 
  else
    {
      if (output.fSelectedMuons.size() > 0) cPassedMuonSelection.increment();
    }
  
  // Return data object
  return output;
}
