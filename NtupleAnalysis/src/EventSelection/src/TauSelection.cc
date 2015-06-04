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

TauSelection::Data::Data() 
: fRtau(-1.0) { }

TauSelection::Data::~Data() { }

const Tau& TauSelection::Data::getSelectedTau() const { 
  if (!hasIdentifiedTaus())
    throw hplus::Exception("Assert") << "You forgot to check if taus exist (hasIdentifiedTaus())!";
  return fSelectedTaus[0];
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
  bInvertTauIsolation(config.getParameter<bool>("invertTauIsolation")),
  // Event counter for passing selection
  cPassedTauSelection(eventCounter.addCounter("passed tau selection ("+postfix+")")),
  cPassedTauSelectionMultipleTaus(eventCounter.addCounter("multiple taus ("+postfix+")")),
  // Sub counters
  cSubAll(eventCounter.addSubCounter("tau selection ("+postfix+")", "All events")),
  cSubPassedTriggerMatching(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed trigger matching")),
  cSubPassedDecayMode(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed decay mode")),
  cSubPassedElectronDiscr(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed e discr")),
  cSubPassedMuonDiscr(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed mu discr")),
  cSubPassedPt(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed pt cut")),
  cSubPassedEta(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed eta cut")),
  cSubPassedLdgTrk(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed ldg.trk pt cut")),
  cSubPassedNprongs(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed nprongs")),
  cSubPassedIsolation(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed isolation")),
  cSubPassedRtau(eventCounter.addSubCounter("tau selection ("+postfix+")", "Passed Rtau"))
{ }

TauSelection::~TauSelection() { }

void TauSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "eSelection_"+sPostfix);
  hTauPtTriggerMatched = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauPtAll", "Tau pT, all", 40, 0, 400);
  hTauEtaTriggerMatched = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauEtaAll", "Tau eta, all", 50, -2.5, 2.5);
  hNPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "tauNpassed", "Tau eta, all", 20, 0, 20);
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
  return privateAnalyze(event);
}

TauSelection::Data TauSelection::privateAnalyze(const Event& event) {
  Data output;
  cSubAll.increment();
  bool passedTriggerMatching = false;
  bool passedDecayMode = false;
  bool passedEdiscr = false;
  bool passedMuDiscr = false;
  bool passedPt = false;
  bool passedEta = false;
  bool passedLdgTrkPt = false;
  bool passedNprongs = false;
  bool passedIsol = false;
  bool passedRtau = false;
  
  // Cache vector of trigger tau 4-momenta
  std::vector<math::LorentzVectorT<double>> myTriggerTauMomenta;
  for (HLTTau p: event.triggerTaus()) {
    myTriggerTauMomenta.push_back(p.p4());
  }
  // Loop over taus
  for (Tau tau: event.taus()) {
    // Apply trigger matching
    double myMinDeltaR = 9999.0;
    for (auto& p: myTriggerTauMomenta) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(p, tau.p4());
      myMinDeltaR = std::min(myMinDeltaR, myDeltaR);
    }
    if (myMinDeltaR > fTriggerTauMatchingCone)
      continue;
    passedTriggerMatching = true;
    // Apply cut on decay mode
    if (!tau.decayModeFinding())
      continue;
    passedDecayMode = true;
    hTauPtTriggerMatched->Fill(tau.pt());
    hTauEtaTriggerMatched->Fill(tau.eta());
    // Electron discrimator
    if (!tau.againstElectronDiscriminator())
      continue;
    passedEdiscr = true;
    // Muon discriminator
    if (!tau.againstMuonDiscriminator())
      continue;
    passedMuDiscr = true;
    // Pt cut on tau
    if (tau.pt() < fTauPtCut)
      continue;
    passedPt = true;
    // Eta cut on tau
    if (tau.eta() < fTauEtaCut)
      continue;
    passedEta = true;
    // Ldg. track pt cut
    if (tau.lTrkPt() < fTauLdgTrkPtCut)
      continue;
    passedLdgTrkPt = true;
    // Number of prongs
    if (fTauNprongs == 13) {
      if (tau.nProngs() != 1 && tau.nProngs() != 3)
        continue;
    } else {
      if (tau.nProngs() != fTauNprongs)
        continue;
    }
    passedNprongs = true;
    // Apply tau isolation
    if (bInvertTauIsolation) {
      if (tau.isolationDiscriminator()) {
        passedIsol = true;
        continue;
      }
    } else {
      if (!tau.isolationDiscriminator())  
        continue;
      passedIsol = true;
    }
    // Apply cut on Rtau
    if (getRtau(tau) < fTauRtauCut)
      continue;
    passedRtau = true;
    output.fSelectedTaus.push_back(tau);
  }
  // If there are multiple taus, choose the one with highest pT
  std::sort(output.fSelectedTaus.begin(), output.fSelectedTaus.end());
  
  // Fill data object
  output.fRtau = getRtau(output.getSelectedTau());

  // Fill counters
  if (passedTriggerMatching)
    cSubPassedTriggerMatching.increment();
  if (passedDecayMode)
    cSubPassedDecayMode.increment();
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
  if (bInvertTauIsolation) {
    if (!passedIsol)
      cSubPassedIsolation.increment();
  } else {
    if (passedIsol)
      cSubPassedIsolation.increment();
  }  
  if (passedRtau)
    cSubPassedRtau.increment();
  if (output.fSelectedTaus.size() > 0)
    cPassedTauSelection.increment();

  // Return data object
  return output;
}

double TauSelection::getRtau(const Tau& tau) const {
  double myRtau = -1.0;
  //FIXME rtau calculation
  //double myTauMomentum = tau.p4().P();
  //if (myTauMomentum > 0.0)
    //  myRtau = static_cast<double>(tau.l) / myTauMomentum;
  return myRtau;
}