// -*- c++ -*-
#include "EventSelection/interface/MuonSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "DataFormat/interface/Muon.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

#include <cmath>

MuonSelection::Data::Data() 
: fHighestSelectedMuonPt(0.0),
  fHighestSelectedMuonEta(0.0),
  fHighestSelectedMuonPhi(0.0) { }

MuonSelection::Data::~Data() { }

MuonSelection::MuonSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerMuonMatchingCone(config.getParameter<float>("triggerMatchingCone")),
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
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedPt(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
}

MuonSelection::MuonSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerMuonMatchingCone(config.getParameter<float>("triggerMatchingCone")),
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
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedPt(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("mu selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}

MuonSelection::~MuonSelection() {
  delete hTriggerMatchDeltaR;
  delete hMuonNAll;
  delete hMuonPtAll;
  delete hMuonEtaAll;
  delete hMuonRelIsoAll;
  delete hMuonMiniIsoAll;
  
  delete hMuonNPassed;
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
    fRelIsoCut  = 0.15; // Based on 2012 isolation = 0.12
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

  // Muons before any cuts
  hMuonNAll       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonNAll", ";#mu multiplicity;Occur / %.0f", 20, 0.0, 20.0);
  hMuonPtAll      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtAll", ";p_{T} (GeV/c);Occur / %.0f", 100, 0.0, 1000.0);
  hMuonEtaAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaAll", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hMuonRelIsoAll  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoAll", ";relative isolation;Occur / %.0f", 1000, 0.0, 200.0);
  hMuonMiniIsoAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonMiniIsoAll", ";relative mini-isolation;Occur / %.0f", 1000, 0.0, 200.0);

  // Muons after all cuts  
  hMuonNPassed       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonNPassed", ";#mu multiplicity;Occur / %.0f", 20, 0.0, 20.0);
  hMuonPtPassed      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonPtPassed", ";p_{T} (GeV/c);Occur / %.0f", 100, 0.0, 1000.0);
  hMuonEtaPassed     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonEtaPassed", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hMuonRelIsoPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonRelIsoPassed", ";relative isolation;Occur / %.0f", 1000, 0.0, 200.0);
  hMuonMiniIsoPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "muonMiniIsoPassed", ";mini relative isolation;Occur / %.0f", 1000, 0.0, 200.0);
  
  hTriggerMatchDeltaR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatchDeltaR"  , "Trigger match #DeltaR;#DeltaR", 60, 0, 3.);

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco};Occur / %.2f", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", ";(#eta^{reco} - #eta^{gen})/#eta^{reco};Occur / %.2f"   , 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", ";(#phi^{reco} - #phi^{gen})/#phi^{reco};Occur / %.2f"   , 200, -1.0, 1.0);

  // Isolation efficiency
  hIsolPtBefore      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore", ";p_{T} (GeV/c);Occur / %.0f", 100, 0.0, 1000.0);
  hIsolEtaBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hIsolVtxBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore", ";Number of Vertices;Occur / %.0f", 150, 0, 150);
  hIsolRelIsoBefore  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoBefore", ";relative isolation;Occur / %.2f", 1000, 0.0, 200.0);
  hIsolMiniIsoBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoBefore", ";mini relative isolation;Occur / %.2f", 1000, 0.0, 200.0);

  hIsolPtAfter      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter", ";p_{T} (GeV/c);Occur / %.0f", 100, 0, 1000.0);
  hIsolEtaAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hIsolVtxAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter", ";Number of Vertices;Occur / %.0f", 150, 0, 150);
  hIsolRelIsoAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoAfter" , ";relative Isolation;Occur / %.2f", 1000, 0.0, 200.0);
  hIsolMiniIsoAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoAfter", ";mini relative isolation;Occur / %.2f", 1000, 0.0, 200.0);
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
  bool passedTriggerMatching = false;
  bool passedPt = false;
  bool passedEta = false;
  bool passedID = false;
  bool passedIsol = false;

  // Cache vector of trigger mu 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerMuonMomenta;
  for (HLTMuon p: event.triggerMuons()) {
    myTriggerMuonMomenta.push_back(p.p4());
  }
  // For-loop: All muons
  for(Muon muon: event.muons()) {

    // Apply trigger matching
    if (!this->passTrgMatching(muon, myTriggerMuonMomenta))
      continue;
    passedTriggerMatching = true;

    // Fill histograms before any cuts
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
    hIsolMiniIsoBefore->Fill(muon.effAreaMiniIso());
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
  
  //sort muons
  std::sort(output.fSelectedMuons.begin(), output.fSelectedMuons.end());

  // Fill histos
  hMuonNAll->Fill(event.muons().size());
  hMuonNPassed->Fill(output.fSelectedMuons.size());

  // Fill sub-counters
  if (passedTriggerMatching) 
    cSubPassedTriggerMatching.increment();

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

bool MuonSelection::passTrgMatching(const Muon& muon, std::vector<math::LorentzVectorT<double>>& trgMuons) const {
  if (!bApplyTriggerMatching)
    return true;
  double myMinDeltaR = 9999.0;
  for (auto& p: trgMuons) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(p, muon.p4());
    myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
  }
  hTriggerMatchDeltaR->Fill(myMinDeltaR);
  return (myMinDeltaR < fTriggerMuonMatchingCone);
}
