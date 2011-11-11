#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBasedAlgorithms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  // TauIDPFShrinkingCone ------------------------------------------------
  
  TauIDPFShrinkingCone::TauIDPFShrinkingCone(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, label+"_PFShrink", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDIsolation = fCounterPackager.addSubCounter(label+"_PFShrink", "Isolation", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFShrinkingCone::~TauIDPFShrinkingCone() { }
  

  bool TauIDPFShrinkingCone::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    // No decay mode finding equivalent in TCTau, always pass true
    return true;
  }

  bool TauIDPFShrinkingCone::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byIsolation05") < 0.5) return false; // 05 points to minimum track pt
    fCounterPackager.incrementSubCount(fIDIsolation);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDPFShrinkingCone::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDIsolation);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFHPSBase ---------------------------------------------
  TauIDPFHPSBase::TauIDPFHPSBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel, TFileDirectory& myDir):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, baseLabel, myDir)
  {}
  TauIDPFHPSBase::~TauIDPFHPSBase() {}

  bool TauIDPFHPSBase::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    if(tau->tauID("decayModeFinding") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    return true;
  }

  bool TauIDPFHPSBase::passTauCandidateEAndMuVetoCuts(const edm::Ptr<pat::Tau> tau) {
    // Electron veto
    if(tau->tauID("againstElectronMedium") < 0.5 ) return false;
    fCounterPackager.incrementSubCount(fIDAgainstElectronCut);
    // Muon veto
    if(tau->tauID("againstMuonTight") < 0.5 ) return false;
    fCounterPackager.incrementSubCount(fIDAgainstMuonCut);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeHPS ---------------------------------------------
  TauIDPFHPSTight::TauIDPFHPSTight(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, eventWeight, label+"_HPSTight", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter(label+"_HPSTight", "HPS", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFHPSTight::~TauIDPFHPSTight() { }
  
  bool TauIDPFHPSTight::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byTightIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFHPSTight::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byLooseIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }
  
  // TauIDPFShrinkingConeHPSMedium ---------------------------------------
  TauIDPFHPSMedium::TauIDPFHPSMedium(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, eventWeight, label+"_HPSMedium", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter(label+"_HPSMedium", "HPS", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFHPSMedium::~TauIDPFHPSMedium() { }
  
  bool TauIDPFHPSMedium::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byMediumIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFHPSMedium::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byMediumIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeHPSLoose ---------------------------------------
  TauIDPFHPSLoose::TauIDPFHPSLoose(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, eventWeight, label+"_HPSLoose", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter(label+"_HPSLoose", "HPS", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFHPSLoose::~TauIDPFHPSLoose() { }
  
  bool TauIDPFHPSLoose::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byLooseIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFHPSLoose::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byLooseIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeHPSVeryLoose ---------------------------------------
  TauIDPFHPSVeryLoose::TauIDPFHPSVeryLoose(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, eventWeight, label+"_HPSVeryLoose", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter(label+"_HPSVeryLoose", "HPS", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFHPSVeryLoose::~TauIDPFHPSVeryLoose() { }
  
  bool TauIDPFHPSVeryLoose::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byVLooseIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFHPSVeryLoose::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byVLooseIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeTaNC --------------------------------------------
  TauIDPFShrinkingConeTaNC::TauIDPFShrinkingConeTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, label+"_TaNCTenth", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDTaNC = fCounterPackager.addSubCounter(label+"_TaNCTenth", "TaNCTenth",
      makeTH<TH1F>(myDir, "TauID_TaNC", "TaNC;TaNC output;N_{jets}/0.02", 60, 0., 1.2));
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFShrinkingConeTaNC::~TauIDPFShrinkingConeTaNC() { }
  
  bool TauIDPFShrinkingConeTaNC::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    // No decay mode finding equivalent in TCTau, always pass true
    return true;
  }

  bool TauIDPFShrinkingConeTaNC::passIsolation(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDTaNC, tau->tauID("byTaNC"));
    if (tau->tauID("byTaNCfrTenthPercent") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDTaNC);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFShrinkingConeTaNC::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDTaNC, tau->tauID("byTaNC"));
    if (tau->tauID("byTaNCfrOnePercent") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDTaNC);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeCombinedHPSTaNC --------------------------------------------
  TauIDPFShrinkingConeCombinedHPSTaNC::TauIDPFShrinkingConeCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, eventWeight, label+"_HPSTaNC", myDir)
  {
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter(label+"_HPSTaNC", "HPSTight", 0);
    fIDTaNC = fCounterPackager.addSubCounter(label+"_HPSTaNC", "TaNCTenth",
      makeTH<TH1F>(myDir, "TauID_CombinedHPSTaNC", "CombinedHPSTaNC;TaNC output;N_{jets}/0.02", 60, 0., 1.2));
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation(prongCount);
  }

  TauIDPFShrinkingConeCombinedHPSTaNC::~TauIDPFShrinkingConeCombinedHPSTaNC() { }

  bool TauIDPFShrinkingConeCombinedHPSTaNC::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    // No decay mode finding equivalent in TCTau, always pass true
    return true;
  }
  
  bool TauIDPFShrinkingConeCombinedHPSTaNC::passIsolation(const edm::Ptr<pat::Tau> tau) {
    // Apply HPS
    if (tau->tauID("byHPStight") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // Apply TaNC
    fCounterPackager.fill(fIDTaNC, tau->tauID("byTaNCvloose"));
    if (tau->tauID("byTaNCtight") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDTaNC);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDPFShrinkingConeCombinedHPSTaNC::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    // Apply HPS
    if (tau->tauID("byHPSvloose") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // Apply TaNC
    fCounterPackager.fill(fIDTaNC, tau->tauID("byTaNCvloose"));
    if (tau->tauID("byTaNCvloose") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDTaNC);
    // All cuts passed, return true
    return true;
  }
  
}
