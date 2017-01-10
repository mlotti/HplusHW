// -*- c++ -*-
#include "EventSelection/interface/TauSelection.h"

#include "Framework/interface/Exception.h"
#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "DataFormat/interface/HLTTau.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

#include <cmath>

TauSelection::Data::Data() 
: fRtau(-1.0),
  fIsGenuineTau(false),
  fTauIDSF(1.0),
  fTauMisIDSF(1.0),
  fTauTriggerSF(1.0),
  fRtauAntiIsolatedTau(-1.0),
  fIsGenuineTauAntiIsolatedTau(false),
  fAntiIsolatedTauMisIDSF(1.0),
  fAntiIsolatedTauTriggerSF(1.0)
{ }

TauSelection::Data::~Data() { }

const Tau& TauSelection::Data::getSelectedTau() const { 
  if (!hasIdentifiedTaus())
    throw hplus::Exception("Assert") << "You forgot to check if taus exist (hasIdentifiedTaus()), this message occurs when none exist!";
  return fSelectedTaus[0];
}

const Tau& TauSelection::Data::getAntiIsolatedTau() const {
  if (!hasAntiIsolatedTaus())
    throw hplus::Exception("Assert") << "You forgot to check if taus exist (hasAntiIsolatedTaus()), this message occurs when none exist!";
  return fAntiIsolatedTaus[0];
}

TauSelection::TauSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerTauMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  fTauEtaCut(config.getParameter<float>("tauEtaCut")),
  fTauLdgTrkPtCut(config.getParameter<float>("tauLdgTrkPtCut")),
  fTauNprongs(config.getParameter<int>("prongs")),
  fTauRtauCut(config.getParameter<float>("rtau")),
  fVetoMode(false),
  // tau identification SF
  fTauIDSF(config.getParameter<float>("tauIdentificationSF")), 
  // tau misidentification SF
  fEToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "E")),
  fEToTauMisIDSFValue(assignTauMisIDSFValue(config, "E")),
  fMuToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "Mu")),
  fMuToTauMisIDSFValue(assignTauMisIDSFValue(config, "Mu")),
  fJetToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "Jet")),
  fJetToTauMisIDSFValue(assignTauMisIDSFValue(config, "Jet")),
  // tau trigger SF
  fTauTriggerSFReader(config.getParameterOptional<ParameterSet>("tauTriggerSF")),
  // Event counter for passing selection
  cPassedTauSelection(fEventCounter.addCounter("Passed tau selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("tau selection ("+postfix+")", "All events")),
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedDecayMode(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed decay mode")),
  cSubPassedGenericDiscriminators(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed generic discriminators")),
  cSubPassedElectronDiscr(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed e discr")),
  cSubPassedMuonDiscr(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed mu discr")),
  cSubPassedPt(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed eta cut")),
  cSubPassedLdgTrk(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed ldg.trk pt cut")),
  cSubPassedNprongs(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed nprongs")),
  cSubPassedIsolation(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed isolation")),
  cSubPassedRtau(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed Rtau")),
  cSubPassedAntiIsolation(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed anti-isolation")),
  cSubPassedAntiIsolationRtau(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed anti-isolated Rtau")),
  cSubPassedTauSelectionGenuine(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed tau selection and genuine")),
  cSubPassedTauSelectionMultipleTaus(fEventCounter.addSubCounter("tau selection ("+postfix+")", "multiple selected taus")),
  cSubPassedAntiIsolatedTauSelection(fEventCounter.addSubCounter("tau selection ("+postfix+")", "Passed anti-isolated tau selection")),
  cSubPassedAntiIsolatedTauSelectionMultipleTaus(fEventCounter.addSubCounter("tau selection ("+postfix+")", "multiple anti-isolated taus"))
{ 
  initialize(config, postfix);
} 

TauSelection::TauSelection(const ParameterSet& config, const std::string& postfix)
: BaseSelection(),
  bApplyTriggerMatching(config.getParameter<bool>("applyTriggerMatching")),
  fTriggerTauMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  fTauEtaCut(config.getParameter<float>("tauEtaCut")),
  fTauLdgTrkPtCut(config.getParameter<float>("tauLdgTrkPtCut")),
  fTauNprongs(config.getParameter<int>("prongs")),
  fTauRtauCut(config.getParameter<float>("rtau")),
  fVetoMode(false),
  // tau misidentification SF
  fEToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "E")),
  fEToTauMisIDSFValue(assignTauMisIDSFValue(config, "E")),
  fMuToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "Mu")),
  fMuToTauMisIDSFValue(assignTauMisIDSFValue(config, "Mu")),
  fJetToTauMisIDSFRegion(assignTauMisIDSFRegion(config, "Jet")),
  fJetToTauMisIDSFValue(assignTauMisIDSFValue(config, "Jet")),
  // tau trigger SF
  fTauTriggerSFReader(config.getParameterOptional<ParameterSet>("tauTriggerSF")),
  // Event counter for passing selection
  cPassedTauSelection(fEventCounter.addCounter("Passed tau selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("tau selection", "All events")),
  cSubPassedTriggerMatching(fEventCounter.addSubCounter("tau selection", "Passed trigger matching")),
  cSubPassedDecayMode(fEventCounter.addSubCounter("tau selection", "Passed decay mode")),
  cSubPassedGenericDiscriminators(fEventCounter.addSubCounter("tau selection", "Passed generic discriminators")),
  cSubPassedElectronDiscr(fEventCounter.addSubCounter("tau selection", "Passed e discr")),
  cSubPassedMuonDiscr(fEventCounter.addSubCounter("tau selection", "Passed mu discr")),
  cSubPassedPt(fEventCounter.addSubCounter("tau selection", "Passed pt cut")),
  cSubPassedEta(fEventCounter.addSubCounter("tau selection", "Passed eta cut")),
  cSubPassedLdgTrk(fEventCounter.addSubCounter("tau selection", "Passed ldg.trk pt cut")),
  cSubPassedNprongs(fEventCounter.addSubCounter("tau selection", "Passed nprongs")),
  cSubPassedIsolation(fEventCounter.addSubCounter("tau selection", "Passed isolation")),
  cSubPassedRtau(fEventCounter.addSubCounter("tau selection", "Passed Rtau")),
  cSubPassedAntiIsolation(fEventCounter.addSubCounter("tau selection", "Passed anti-isolation")),
  cSubPassedAntiIsolationRtau(fEventCounter.addSubCounter("tau selection", "Passed anti-isolated Rtau")),
  cSubPassedTauSelectionGenuine(fEventCounter.addSubCounter("tau selection", "Passed tau selection and genuine")),
  cSubPassedTauSelectionMultipleTaus(fEventCounter.addSubCounter("tau selection", "multiple selected taus")),
  cSubPassedAntiIsolatedTauSelection(fEventCounter.addSubCounter("tau selection", "Passed anti-isolated tau selection")),
  cSubPassedAntiIsolatedTauSelectionMultipleTaus(fEventCounter.addSubCounter("tau selection", "multiple anti-isolated taus"))
{ 
  initialize(config, postfix);
  bookHistograms(new TDirectory());
}

TauSelection::~TauSelection() {
  delete hTriggerMatchDeltaR;
  delete hTauPtTriggerMatched;
  delete hTauEtaTriggerMatched;
  delete hNPassed;
  delete hPtResolution;
  delete hEtaResolution;
  delete hPhiResolution;
  delete hIsolPtBefore;
  delete hIsolEtaBefore;
  delete hIsolVtxBefore;
  delete hIsolPtAfter;
  delete hIsolEtaAfter;
  delete hIsolVtxAfter;
  delete hNprongsMatrixForAllAfterIsolation;
  delete hNprongsMatrixForBmesonsAfterIsolation;
  delete hNprongsMatrixForAllAfterAntiIsolation;
  delete hNprongsMatrixForBmesonsAfterAntiIsolation;
}

void TauSelection::initialize(const ParameterSet& config, const std::string& postfix) {
  if (postfix.find("veto") != std::string::npos || postfix.find("Veto") != std::string::npos)
    {
      fVetoMode = true;
    }
}

void TauSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "tauSelection_"+sPostfix);
  hTriggerMatchDeltaR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "triggerMatchDeltaR"  , "Trigger match #DeltaR;#DeltaR", 60, 0, 3.);
  hTauPtTriggerMatched  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauPtTriggerMatched" , "Tau pT, trigger matched;p_{T} (GeV/c)", 50, 0, 500.0);
  hTauEtaTriggerMatched = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauEtaTriggerMatched", "Tau eta, trigger matched;#eta", 50, -2.5, 2.5);
  hNPassed              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauNpassed"          , "Number of passed taus;Number of taus", 10, 0, 10);
  // Resolutions
  hPtResolution  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ptResolution" , "(reco pT - gen pT) / reco pT;(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{reco}", 200, -1.0, 1.0);
  hEtaResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "etaResolution", "(reco eta - gen eta) / reco eta;(#eta^{reco} - #eta^{gen})/#eta^{reco}", 200, -1.0, 1.0);
  hPhiResolution = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "phiResolution", "(reco phi - gen phi) / reco phi;(#phi^{reco} - #phi^{gen})/#phi^{reco}", 200, -1.0, 1.0);
  // Isolation efficiency
  hIsolPtBefore  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtBefore" , "Tau pT before isolation is applied;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hIsolEtaBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaBefore", "Tau eta before isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxBefore = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxBefore", "Nvertices before isolation is applied;Number of Vertices", 60, 0, 60);
  hIsolPtAfter   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolPtAfter"  , "Tau pT before isolation is applied;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hIsolEtaAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolEtaAfter" , "Tau eta before isolation is applied;#eta", 50, -2.5, 2.5);
  hIsolVtxAfter  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "IsolVtxAfter" , "Nvertices before isolation is applied;Number of Vertices", 60, 0, 60);
  hNprongsMatrixForAllAfterIsolation         = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "NprongsMatrixForAllAfterIsolation"        , ";Simulated prongs;Reconstructed prongs", 4, 0, 4, 4, 0, 4);
  hNprongsMatrixForBmesonsAfterIsolation     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "NprongsMatrixForBmesonsAfterIsolation"    , ";Simulated prongs;Reconstructed prongs", 4, 0, 4, 4, 0, 4);
  hNprongsMatrixForAllAfterAntiIsolation     = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "NprongsMatrixForAllAfterAntiIsolation"    , ";Simulated prongs;Reconstructed prongs", 4, 0, 4, 4, 0, 4);
  hNprongsMatrixForBmesonsAfterAntiIsolation = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "NprongsMatrixForBmesonsAfterAntiIsolation", ";Simulated prongs;Reconstructed prongs", 4, 0, 4, 4, 0, 4);
}

TauSelection::Data TauSelection::silentAnalyze(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event);
  enableHistogramsAndCounters();
  return myData;
}

TauSelection::Data TauSelection::analyze(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  TauSelection::Data data = privateAnalyze(event);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtTauSelection(event, data);
//    fCommonPlots->fillControlPlotsAfterTauSelection(event, data); // filled in privateAnalyze
  // Return data
  return data;
}

TauSelection::Data TauSelection::privateAnalyze(const Event& event) {
  Data output;
 
  cSubAll.increment();
  bool passedTriggerMatching = false;
  bool passedDecayMode = false;
  bool passedGenericDiscr = false;
  bool passedEdiscr = false;
  bool passedMuDiscr = false;
  bool passedPt = false;
  bool passedEta = false;
  bool passedLdgTrkPt = false;
  bool passedNprongs = false;
  bool passedIsol = false;
  bool passedRtau = false;
  bool passedAntiIsol = false;
  bool passedAntiIsolRtau = false;
  
  // Cache vector of trigger tau 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerTauMomenta;
  for (HLTTau p: event.triggerTaus()) {
    myTriggerTauMomenta.push_back(p.p4());
  }
  // Loop over taus
  for (Tau tau: event.taus()) {
    // Apply trigger matching
    if (!this->passTrgMatching(tau, myTriggerTauMomenta))
      continue;
    passedTriggerMatching = true;
    // Apply cut on decay mode
    if (!this->passDecayModeFinding(tau)) {
      continue;
    }
    passedDecayMode = true;
    hTauPtTriggerMatched->Fill(tau.pt());
    hTauEtaTriggerMatched->Fill(tau.eta());
    // Generic discriminators
    if (!this->passGenericDiscriminators(tau))
      continue;
    passedGenericDiscr = true;
    // Electron discrimator
    if (!this->passElectronDiscriminator(tau))
      continue;
    passedEdiscr = true;
    // Muon discriminator
    if (!this->passMuonDiscriminator(tau))
      continue;
    passedMuDiscr = true;
    // Pt cut on tau
    if (!this->passPtCut(tau))
      continue;
    passedPt = true;
    // Eta cut on tau
    if (!this->passEtaCut(tau))
      continue;
    passedEta = true;
    // Ldg. track pt cut
    if (!this->passLdgTrkPtCut(tau))
      continue;
    passedLdgTrkPt = true;
    // Number of prongs
    if (!this->passNprongsCut(tau))
      continue;
    passedNprongs = true;
    // Apply tau isolation
    hIsolPtBefore->Fill(tau.pt());
    hIsolEtaBefore->Fill(tau.eta());
    if (fCommonPlotsIsEnabled())
      hIsolVtxBefore->Fill(fCommonPlots->nVertices());
    if (this->passIsolationDiscriminator(tau)) {
      // tau is isolated
      passedIsol = true;
      hIsolPtAfter->Fill(tau.pt());
      hIsolEtaAfter->Fill(tau.eta());
      if (fCommonPlotsIsEnabled())
        hIsolVtxAfter->Fill(fCommonPlots->nVertices());
      // Apply cut on Rtau
      if (!this->passRtauCut(tau))
        continue;
      passedRtau = true;
      // Passed tau selection
      output.fSelectedTaus.push_back(tau);
      // Fill resolution histograms only for isolated taus
      if (event.isMC()) {
        hPtResolution->Fill((tau.pt() - tau.MCVisibleTau()->pt()) / tau.pt());
        hEtaResolution->Fill((tau.eta() - tau.MCVisibleTau()->eta()) / tau.eta());
        hPhiResolution->Fill((tau.phi() - tau.MCVisibleTau()->phi()) / tau.phi());
      }
    } else {
      // tau is not isolated
      passedAntiIsol = true;
      // Apply cut on Rtau
      if (!this->passRtauCut(tau))
        continue;
      passedAntiIsolRtau = true;
      // Passed anti-isolated tau selection
      output.fAntiIsolatedTaus.push_back(tau);
    }
  }
  hNPassed->Fill(output.fSelectedTaus.size());
  // If there are multiple taus, choose the one with highest pT
  std::sort(output.fSelectedTaus.begin(), output.fSelectedTaus.end());
  std::sort(output.fAntiIsolatedTaus.begin(), output.fAntiIsolatedTaus.end());
  
  // Fill data object
  if (output.fSelectedTaus.size()) {
    output.fRtau = output.getSelectedTau().rtau();
    if (event.isMC()) {
      output.fIsGenuineTau = output.getSelectedTau().isGenuineTau();
    }
  }
  if (output.fAntiIsolatedTaus.size()) {
    output.fRtauAntiIsolatedTau = output.getAntiIsolatedTau().rtau();
    if (event.isMC()) {
      output.fIsGenuineTauAntiIsolatedTau = output.getAntiIsolatedTau().isGenuineTau();
    }
  }
  if (fCommonPlots != nullptr) {
    if (output.fSelectedTaus.size()) {
      fCommonPlots->fillControlPlotsAfterTauSelection(event, output);
    } else if (output.fAntiIsolatedTaus.size()) {
      fCommonPlots->fillControlPlotsAfterAntiIsolatedTauSelection(event, output);
    }
  }
  // Fill Nprongs matrix plots
  if (event.isMC()) {
    if (output.fSelectedTaus.size()) {
      // Isolated genuine tau exists
      if (output.isGenuineTau()) {
        hNprongsMatrixForAllAfterIsolation->Fill(output.getSelectedTau().mcNProngs(), output.getSelectedTau().nProngs());
        if (output.getSelectedTau().isFromOtherSource()) {
          hNprongsMatrixForBmesonsAfterIsolation->Fill(output.getSelectedTau().mcNProngs(), output.getSelectedTau().nProngs());
        }
      }
    } else if (output.fAntiIsolatedTaus.size()) {
      // No isolated tau, but isolated genuine tau(s) exist
      if (output.getAntiIsolatedTauIsGenuineTau()) {
        hNprongsMatrixForAllAfterAntiIsolation->Fill(output.getAntiIsolatedTau().mcNProngs(), output.getAntiIsolatedTau().nProngs());
        if (output.getAntiIsolatedTau().isFromOtherSource()) {
          hNprongsMatrixForBmesonsAfterAntiIsolation->Fill(output.getAntiIsolatedTau().mcNProngs(), output.getAntiIsolatedTau().nProngs());
        }
      }
    }
  }
  // Set tau identification SF value to data object
  if (event.isMC()) {
    setTauIDSFValue(output);
  }

  // Set tau misidentification SF value to data object
  if (event.isMC()) {
    setTauMisIDSFValue(output);
  }
  // Set tau trigger SF value to data object
  if (event.isMC()) {
    if (output.hasIdentifiedTaus()) {
      output.fTauTriggerSF = fTauTriggerSFReader.getScaleFactorValue(output.getSelectedTau().pt());
    }
    if (output.hasAntiIsolatedTaus()) {
      output.fAntiIsolatedTauTriggerSF = fTauTriggerSFReader.getScaleFactorValue(output.getAntiIsolatedTau().pt());
    }
  }

  // Fill sub-counters
  if (passedTriggerMatching)
    cSubPassedTriggerMatching.increment();
  if (passedDecayMode)
    cSubPassedDecayMode.increment();
  if (passedGenericDiscr)
    cSubPassedGenericDiscriminators.increment();
  if (passedEdiscr)
    cSubPassedElectronDiscr.increment();
  if (passedMuDiscr)
    cSubPassedMuonDiscr.increment();
  if (passedPt)
    cSubPassedPt.increment();
  if (passedEta)
    cSubPassedEta.increment();
  if (passedLdgTrkPt)
    cSubPassedLdgTrk.increment();
  if (passedNprongs)
    cSubPassedNprongs.increment();
  if (passedIsol)
    cSubPassedIsolation.increment();
  if (passedRtau)
    cSubPassedRtau.increment();
  if (passedAntiIsol)
    cSubPassedAntiIsolation.increment();
  if (passedAntiIsolRtau)
    cSubPassedAntiIsolationRtau.increment();
  if (output.fSelectedTaus.size() > 0 && output.isGenuineTau() )
  cSubPassedTauSelectionGenuine.increment();
  if (output.fSelectedTaus.size() > 1)
    cSubPassedTauSelectionMultipleTaus.increment();
  if (output.fAntiIsolatedTaus.size() > 0)
    cSubPassedAntiIsolatedTauSelection.increment();
  if (output.fAntiIsolatedTaus.size() > 1)
    cSubPassedAntiIsolatedTauSelectionMultipleTaus.increment();

  // Fill counters
  if (fVetoMode) {
    if (output.fSelectedTaus.size() == 0)
      cPassedTauSelection.increment();
  } else {
    if (output.fSelectedTaus.size() > 0)
      cPassedTauSelection.increment();
  }

  // Return data object
  return output;
}

bool TauSelection::passTrgMatching(const Tau& tau, std::vector<math::LorentzVectorT<double>>& trgTaus) const {
  if (!bApplyTriggerMatching)
    return true;
  double myMinDeltaR = 9999.0;
  for (auto& p: trgTaus) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(p, tau.p4());
    myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
  }
  hTriggerMatchDeltaR->Fill(myMinDeltaR);
  return (myMinDeltaR < fTriggerTauMatchingCone);
}

bool TauSelection::passNprongsCut(const Tau& tau) const {
  if (fTauNprongs > 0) {
    if (fTauNprongs == 12) {
      return (tau.decayMode() >= 0 && tau.decayMode() <= 9);
    } else if (fTauNprongs == 13) {
      return ((tau.decayMode() >= 0 && tau.decayMode() <= 4) || (tau.decayMode() >= 10 && tau.decayMode() <= 14));
    } else if (fTauNprongs == 23) {
      return (tau.decayMode() >= 5 && tau.decayMode() <= 14);
    } else if (fTauNprongs == 123) {
      return (tau.decayMode() >= 0 && tau.decayMode() <= 14);
    } else {
      return (tau.decayMode() >= (fTauNprongs-1)*5 && tau.decayMode() <= fTauNprongs*5-1);
    }
  }
  return true;
}

std::vector<TauSelection::TauMisIDRegionType> TauSelection::assignTauMisIDSFRegion(const ParameterSet& config, const std::string& label) const{
  std::vector<TauMisIDRegionType> result;
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauBarrelSF"))
    result.push_back(kBarrel);
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauEndcapSF"))
    result.push_back(kEndcap);
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauSF"))
    result.push_back(kFullCoverage);
//   if (!result.size())
//     throw hplus::Exception("config") << "Could not found " << label << "->tau misID SF in config!";
  return result;
}

std::vector<float> TauSelection::assignTauMisIDSFValue(const ParameterSet& config, const std::string& label) const {
  std::vector<float> result;
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauBarrelSF"))
    result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauBarrelSF"));
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauEndcapSF"))
    result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauEndcapSF"));
  if (config.getParameterOptional<float>("tauMisidetification"+label+"ToTauSF"))
    result.push_back(config.getParameter<float>("tauMisidetification"+label+"ToTauSF"));
//   if (!result.size())
//     throw hplus::Exception("config") << "Could not found " << label << "->tau misID SF in config!";
  return result;
}

void TauSelection::setTauIDSFValue(Data& data) {
  if (data.hasIdentifiedTaus()) {
    if (data.isGenuineTau()) {
      data.fTauIDSF = fTauIDSF;
    }
  }
}

void TauSelection::setTauMisIDSFValue(Data& data) {
  if (data.hasIdentifiedTaus()) {
    if (!data.isGenuineTau()) {
      data.fTauMisIDSF = setTauMisIDSFValueHelper(data.getSelectedTau());
    }
  }
  if (data.hasAntiIsolatedTaus()) {
    if (!data.getAntiIsolatedTauIsGenuineTau()) {
      data.fAntiIsolatedTauMisIDSF = setTauMisIDSFValueHelper(data.getAntiIsolatedTau());
    }
  }
}

float TauSelection::setTauMisIDSFValueHelper(const Tau& tau) {
  double eta = tau.eta();
  if (tau.isElectronToTau()) {
    for (size_t i = 0; i < fEToTauMisIDSFRegion.size(); ++i) {
      if (tauMisIDSFBelongsToRegion(fEToTauMisIDSFRegion[i], eta))
        return fEToTauMisIDSFValue[i];
    }
  } else if (tau.isMuonToTau()) {
    for (size_t i = 0; i < fMuToTauMisIDSFRegion.size(); ++i) {
      if (tauMisIDSFBelongsToRegion(fMuToTauMisIDSFRegion[i], eta))
        return fMuToTauMisIDSFValue[i];
    }
  } else if (tau.isJetToTau()) {
    for (size_t i = 0; i < fJetToTauMisIDSFRegion.size(); ++i) {
      if (tauMisIDSFBelongsToRegion(fJetToTauMisIDSFRegion[i], eta))
        return fJetToTauMisIDSFValue[i];
    }
  }
  return 1.0;
}

bool TauSelection::tauMisIDSFBelongsToRegion(TauMisIDRegionType region, double eta) {
  if (region == kFullCoverage)
    return true;
  else if (region == kBarrel)
    return std::abs(eta) < 1.5;
  else if (region == kEndcap)
    return std::abs(eta) > 1.5;
  // never reached
  return false;
}
