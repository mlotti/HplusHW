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
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
  // Event counter for passing selection
  cPassedElectronSelection(fEventCounter.addCounter("passed e selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("e selection ("+postfix+")", "All events")),
  cSubPassedPt(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
}

ElectronSelection::ElectronSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  fElectronPtCut(config.getParameter<float>("electronPtCut")),
  fElectronEtaCut(config.getParameter<float>("electronEtaCut")),
  fRelIsoCut(-1.0),
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
  // Event counter for passing selection
  cPassedElectronSelection(fEventCounter.addCounter("passed e selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("e selection ("+postfix+")", "All events")),
  cSubPassedPt(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}

ElectronSelection::~ElectronSelection() {
  delete hElectronPtAll;
  delete hElectronEtaAll;
  delete hElectronRelIsoAll;
  delete hElectronMiniIsoAll;

  delete hElectronPtPassed;
  delete hElectronEtaPassed;
  delete hElectronRelIsoPassed;
  delete hElectronMiniIsoPassed;

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

void ElectronSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos)
    {
    fVetoMode = true;
    }
 
 std::string isolString = config.getParameter<std::string>("electronIsolation");
  if (isolString == "veto" || isolString == "Veto") {
    fRelIsoCut  = 0.15; // Loose iso sync'ed with MIT
    fMiniIsoCut = 0.4;  // from Brown/MIT sync
  } 
  else if (isolString == "tight" || isolString == "Tight") {
    fRelIsoCut  = 0.10; // Based on 2012 cut based isolation
    fMiniIsoCut = 0.10; // arbitrary value selected
  } 
  else
    {
      throw hplus::Exception("config") << "Invalid electronIsolation option '" << isolString << "'! Options: 'veto', 'tight'";
    } 

  std::string isolTypeString = config.getParameter<std::string>("electronIsolType");
  if (isolTypeString == "default")  fMiniIsol = false;
  else if (isolTypeString == "mini") fMiniIsol = true;
  else
   {
     throw hplus::Exception("config") << "Invalid electronIsolType option '" << isolTypeString << "'! Options: 'default', 'mini'";
   }
  
  return;
}

void ElectronSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir  = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "eSelection_"+sPostfix);
  hElectronPtAll         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtAll"        , ";p_{T} (GeV/c);Events / %.0f", 50, 0, 500.0);
  hElectronEtaAll        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaAll"       , ";#eta;Events / %.2f", 50, -2.5, 2.5);
  hElectronRelIsoAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronRelIsoAll"    , ";relative isolation;Events / %.2f", 300, 0.0, 300.0);
  hElectronMiniIsoAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronMiniIsoAll"   , ";relative isolation;Events / %.2f", 300, 0.0, 300.0);

  hElectronPtPassed      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtPassed"     , ";p_{T} (GeV/c);Events / %.0f", 50, 0.0, 500.0);
  hElectronEtaPassed     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaPassed"    , ";#eta;Events / %.2f", 50, -2.5, 2.5);
  hElectronRelIsoPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronRelIsoPassed" , ";relative isolation;Events / %.2f", 100, 0.0, 1.0);
  hElectronMiniIsoPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronMiniIsoPassed", ";relative isolation (mini);Events / %.2f", 100, 0.0, 1.0);

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco};Events / %.0f", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", ";(#eta^{reco} - #eta^{gen})/#eta^{reco};Events / %.2f", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", ";(#phi^{reco} - #phi^{gen})/#phi^{reco};Events / %.2f", 200, -1.0, 1.0);

  // Isolation efficiency
  hIsolPtBefore      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore"     , ";p_{T} (GeV/c);Events / %.0f", 50, 0.0, 500.0);
  hIsolEtaBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore"    , ";#eta;Events / %.2f", 50, -2.5, 2.5);
  hIsolVtxBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore"    , ";Number of Vertices;Events / %.2f", 60, 0, 60.0);
  hIsolRelIsoBefore  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoBefore" , ";relative isolation;Events / %.2f", 300, 0.0, 300.0);
  hIsolMiniIsoBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoBefore", ";relative isolation (mini);Events / %.2f", 300, 0.0, 300.0);

  hIsolPtAfter      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter"     , ";p_{T} (GeV/c);Events / %.0f", 50, 0.0, 500.0);
  hIsolEtaAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter"    , ";#eta;Events / %.2f", 50, -2.5, 2.5);
  hIsolVtxAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter"    , ";Number of Vertices;Events / %.0f", 60, 0, 60);
  hIsolRelIsoAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoAfter" , ";relative isolation;Events / %.2f", 100, 0.0, 1.0);
  hIsolMiniIsoAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoAfter", ";relative isolation (mini);Events / %.2f", 100, 0.0, 1.0);
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
    // hElectronRelIsoAll->Fill(electron.relIsoDeltaBeta());
    hElectronRelIsoAll->Fill(electron.effAreaIsoDeltaBeta());
    hElectronMiniIsoAll->Fill(electron.effAreaMiniIso());

    // Apply cut on pt
    if (electron.pt() < fElectronPtCut) continue;
    passedPt = true;

    // Apply cut on eta
    if (std::fabs(electron.eta()) > fElectronEtaCut) continue;
    passedEta = true;

    // Apply cut on electron ID
    if (!electron.electronIDDiscriminator()) continue; //fixme: MVA
    passedID = true;
    
    // Fill histograms before isolation cut
    hIsolPtBefore->Fill(electron.pt());
    hIsolEtaBefore->Fill(electron.eta());
    hIsolRelIsoBefore->Fill(electron.effAreaIsoDeltaBeta());
    hIsolMiniIsoBefore->Fill(electron.effAreaMiniIso());
    if (fCommonPlotsIsEnabled())
      {
	hIsolVtxBefore->Fill(fCommonPlots->nVertices());
      }

    // Apply cut on electron isolation
    bool passedRelIso  = (electron.effAreaIsoDeltaBeta() > fRelIsoCut);
    bool passedMiniIso = (electron.effAreaMiniIso() > fRelIsoCut);
    bool passedIsolCut = false;
    if (fMiniIsol) passedIsolCut =  passedMiniIso;
    else passedIsolCut =  passedRelIso;
    if (passedIsolCut) continue;

    // Fill histograms after isolation cut
    hIsolPtAfter->Fill(electron.pt());
    hIsolEtaAfter->Fill(electron.eta());
    hIsolRelIsoAfter->Fill(electron.effAreaIsoDeltaBeta());
    hIsolMiniIsoAfter->Fill(electron.effAreaMiniIso());
    if (fCommonPlotsIsEnabled()) 
      {
	hIsolVtxAfter->Fill(fCommonPlots->nVertices());
      }

    // Fill histograms after all cuts
    hElectronPtPassed->Fill(electron.pt());
    hElectronEtaPassed->Fill(electron.eta());
    // hElectronRelIsoPassed->Fill(electron.relIsoDeltaBeta());
    hElectronRelIsoPassed->Fill(electron.effAreaIsoDeltaBeta());
    hElectronMiniIsoPassed->Fill(electron.effAreaMiniIso());

    // Save the highest pt electron
    if (electron.pt() > output.fHighestSelectedElectronPt) {
      output.fHighestSelectedElectronPt = electron.pt();
      output.fHighestSelectedElectronEta = electron.eta();
    }

    // Save all electrons surviving the cuts
    output.fSelectedElectrons.push_back(electron);

    // Fill resolution histograms
    if (event.isMC()) 
      {
      hPtResolution->Fill((electron.pt() - electron.MCelectron()->pt()) / electron.pt());
      hEtaResolution->Fill((electron.eta() - electron.MCelectron()->eta()) / electron.eta());
      hPhiResolution->Fill((electron.phi() - electron.MCelectron()->phi()) / electron.phi());
      }

  }//for-loop: electrons

  // Fill counters
  if (passedPt) cSubPassedPt.increment();
  if (passedEta) cSubPassedEta.increment();
  if (passedID) cSubPassedID.increment();
  if (passedIsol) cSubPassedIsolation.increment();
  if (fVetoMode) 
    {
      if (output.fSelectedElectrons.size() == 0)
	cPassedElectronSelection.increment();
    } 
  else
    {
      if (output.fSelectedElectrons.size() > 0) cPassedElectronSelection.increment();
    } 

  // Return data object
  return output;
}
