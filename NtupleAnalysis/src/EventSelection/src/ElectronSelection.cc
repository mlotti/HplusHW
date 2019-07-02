// -*- c++ -*-
#include "EventSelection/interface/ElectronSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "DataFormat/interface/Electron.h"
//#include "Framework/interface/makeTH.h"

ElectronSelection::Data::Data()
: fHighestSelectedElectronPt(0.0),
  fHighestSelectedElectronEta(0.0) { }

ElectronSelection::Data::~Data() { }

ElectronSelection::ElectronSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerElectronMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fElectronPtCut(config.getParameter<float>("electronPtCut")),
  fElectronEtaCut(config.getParameter<float>("electronEtaCut")),
  fRelIsoCut(-1.0),
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
  fElectronMVA(false),
  fElectronMVACut(config.getParameter<string>("electronMVACut")),
  // Event counter for passing selection
  cPassedElectronSelection(fEventCounter.addCounter("passed e selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("e selection ("+postfix+")", "All events")),
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedPt(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
}

ElectronSelection::ElectronSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerElectronMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fElectronPtCut(config.getParameter<float>("electronPtCut")),
  fElectronEtaCut(config.getParameter<float>("electronEtaCut")),
  fRelIsoCut(-1.0),
  fMiniIsoCut(-1.0),
  fVetoMode(false),
  fMiniIsol(false),
  fElectronMVA(false),
  fElectronMVACut(config.getParameter<string>("electronMVACut")),
  // Event counter for passing selection
  cPassedElectronSelection(fEventCounter.addCounter("passed e selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("e selection ("+postfix+")", "All events")),
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedPt(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed eta cut")),
  cSubPassedID(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed ID")),
  cSubPassedIsolation(fEventCounter.addSubCounter("e selection ("+postfix+")", "Passed isolation"))
{
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}

ElectronSelection::~ElectronSelection() {
  delete hTriggerMatchDeltaR;
  delete hElectronNAll;
  delete hElectronPtAll;
  delete hElectronEtaAll;
  delete hElectronRelIsoAll;
  delete hElectronMiniIsoAll;

  delete hElectronNPassed;
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
  
  std::string idTypeString = config.getParameter<std::string>("electronIDType");
  if (idTypeString == "default") fElectronMVA = false;
  else if (idTypeString == "MVA") fElectronMVA = true;
  else
    {
      throw hplus::Exception("config") << "Invalid electronIDType option '" << idTypeString << "'! Options: 'default', 'MVA'";
    }
  
  return;
}

void ElectronSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir  = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "eSelection_"+sPostfix);

  // Electrons before any cuts
  hElectronNAll       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronNAll", ";e multiplicity;Occur / %.0f", 20, 0, 20.0);
  hElectronPtAll      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtAll", ";p_{T} (GeV/c);Occur / %.0f", 100, 0, 1000.0);
  hElectronEtaAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaAll", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hElectronRelIsoAll  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronRelIsoAll" , ";relative isolation;Occur / %.0f", 1000, 0.0, 200.0);
  hElectronMiniIsoAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronMiniIsoAll", ";relative mini-isolation;Occur / %.0f", 1000, 0.0, 200.0);
 
  // Electrons after all cuts
  hElectronNPassed       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronNPassed", ";e multiplicity;Occur / %.0f", 20, 0, 20.0);
  hElectronPtPassed      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronPtPassed", ";p_{T} (GeV/c);Occur / %.0f", 100, 0.0, 1000.0);
  hElectronEtaPassed     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronEtaPassed", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hElectronRelIsoPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronRelIsoPassed", ";relative isolation;Occur / %.2f", 1000, 0.0, 200.0);
  hElectronMiniIsoPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "electronMiniIsoPassed", ";relative mini-isolation;Occur / %.2f", 1000, 0.0, 200.0);

  hTriggerMatchDeltaR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatchDeltaR"  , "Trigger match #DeltaR;#DeltaR", 60, 0, 3.);

  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , ";(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco};Occur / %.2f", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", ";(#eta^{reco} - #eta^{gen})/#eta^{reco};Occur / %.2f"   , 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", ";(#phi^{reco} - #phi^{gen})/#phi^{reco};Occur / %.2f"   , 200, -1.0, 1.0);

  // Isolation efficiency
  hIsolPtBefore      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore", ";p_{T} (GeV/c);Occur / %.0f", 100, 0.0, 1000.0);
  hIsolEtaBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hIsolVtxBefore     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore", ";Number of Vertices;Occur / %.2f", 150, 0, 150.0);
  hIsolRelIsoBefore  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoBefore", ";relative isolation;Occur / %.2f", 1000, 0.0, 200.0);
  hIsolMiniIsoBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoBefore", ";relative mini-isolation;Occur / %.2f", 1000, 0.0, 200.0);

  hIsolPtAfter      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter", ";p_{T} (GeV/c);Occur / %.0f", 50, 0.0, 500.0);
  hIsolEtaAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter", ";#eta;Occur / %.2f", 50, -2.5, 2.5);
  hIsolVtxAfter     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter", ";Number of Vertices;Occur / %.0f", 150, 0, 150);
  hIsolRelIsoAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolRelIsoAfter", ";relative isolation;Occur / %.2f", 1000, 0.0, 200.0);
  hIsolMiniIsoAfter = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolMiniIsoAfter", ";relative mini-isolation;Occur / %.2f", 1000, 0.0, 200.0);
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
  bool passedTriggerMatching = false;
  bool passedPt = false;
  bool passedEta = false;
  bool passedID = false;
  bool passedIsol = false;

  // Cache vector of trigger ele 4-momenta

  std::vector<math::LorentzVectorT<double>> myTriggerElectronMomenta;
  if (bApplyTriggerMatching) {
    for (HLTElectron p: event.triggerElectrons()) {
      myTriggerElectronMomenta.push_back(p.p4());
    }
  }
  // For-loop: All electrons
  for(Electron electron: event.electrons()) {

    // Apply trigger matching
    if (bApplyTriggerMatching) {
      if (!this->passTrgMatching(electron, myTriggerElectronMomenta))
        continue;
    }

    passedTriggerMatching = true;

    // Fill histograms before any cuts
    hElectronPtAll->Fill(electron.pt());
    hElectronEtaAll->Fill(electron.eta());
    hElectronRelIsoAll->Fill(electron.effAreaIsoDeltaBeta()); // electron.relIsoDeltaBeta()
    hElectronMiniIsoAll->Fill(electron.effAreaMiniIso());

    //=== Apply cut on pt
    if (electron.pt() < fElectronPtCut) continue;
    passedPt = true;

    //=== Apply cut on eta
    if (std::fabs(electron.eta()) > fElectronEtaCut) continue;
    passedEta = true;

    //=== Apply cut on electron ID
    bool passedCutBasedID = electron.electronIDDiscriminator();
    bool passedMVA        = false;
    if(fElectronMVA) passedMVA = getMVADecision(electron, fElectronMVACut); 
    bool passedIDCut      = false;
    if (fElectronMVA) passedIDCut = passedMVA;
    else passedIDCut = passedCutBasedID;
    if (!passedIDCut) continue;
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

    //=== Apply cut on electron isolation
    bool passedRelIso  = (electron.effAreaIsoDeltaBeta() < fRelIsoCut);
    bool passedMiniIso = (electron.effAreaMiniIso() < fMiniIsoCut);
    bool passedIsolCut = false;
    if (fMiniIsol) passedIsolCut =  passedMiniIso;
    else passedIsolCut =  passedRelIso;
    if (!passedIsolCut) continue;
    passedIsol = true;

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
    hElectronRelIsoPassed->Fill(electron.effAreaIsoDeltaBeta()); // electron.relIsoDeltaBeta()
    hElectronMiniIsoPassed->Fill(electron.effAreaMiniIso());

    // Save the highest pt electron
    if (electron.pt() > output.fHighestSelectedElectronPt) 
      {
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

  //sort electrons, needed comparisons defined in Electron.h
  std::sort(output.fSelectedElectrons.begin(), output.fSelectedElectrons.end());

  // Fill histos
  hElectronNAll->Fill(event.electrons().size());
  hElectronNPassed->Fill(output.fSelectedElectrons.size());

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

bool ElectronSelection::getMVADecision(const Electron& ele, const std::string mvaCut){

  if (mvaCut == "loose" || mvaCut == "Loose")
    {
      double AbsEta = std::abs(ele.eta());
      
      if (AbsEta<=0.8 && ele.MVA()>=-0.041){
	return true;
      }
      if (AbsEta>0.8 && AbsEta<1.479 && ele.MVA()>=0.383){
	return true;
      }
      if (AbsEta>=1.479 && ele.MVA()>=-0.515){
	return true;
      }
    }
  else
    {
      throw hplus::Exception("config") << "Invalid electronMVACut option '" << mvaCut << "'! Options: 'Loose'";
    }
  return false;
}

bool ElectronSelection::passTrgMatching(const Electron& electron, std::vector<math::LorentzVectorT<double>>& trgElectrons) const {
  if (!bApplyTriggerMatching)
    return true;
  double myMinDeltaR = 9999.0;
  for (auto& p: trgElectrons) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(p, electron.p4());
    myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
  }
  hTriggerMatchDeltaR->Fill(myMinDeltaR);
  return (myMinDeltaR < fTriggerElectronMatchingCone);
}
