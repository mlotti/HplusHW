#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBasedAlgorithms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  // TauIDPFShrinkingCone ------------------------------------------------
  
  TauIDPFShrinkingCone::TauIDPFShrinkingCone(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, "PFShrink")
  {
    edm::Service<TFileService> fs;
    // Initialize counter objects for tau isolation
    fIDIsolation = fCounterPackager.addSubCounter("PFShrink", "Isolation", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation();
  }

  TauIDPFShrinkingCone::~TauIDPFShrinkingCone() { }
  
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

  // TauIDPFShrinkingConeHPS ---------------------------------------------
  TauIDPFShrinkingConeHPS::TauIDPFShrinkingConeHPS(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, "HPSTight")
  {
    edm::Service<TFileService> fs;
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter("HPSTight", "HPS", 0);
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation();
  }

  TauIDPFShrinkingConeHPS::~TauIDPFShrinkingConeHPS() { }
  
  bool TauIDPFShrinkingConeHPS::passIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byTightIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFShrinkingConeHPS::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (tau->tauID("byLooseIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // All cuts passed, return true
    return true;
  }

  // TauIDPFShrinkingConeTaNC --------------------------------------------
  TauIDPFShrinkingConeTaNC::TauIDPFShrinkingConeTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, "TaNCTenth")
  {
    edm::Service<TFileService> fs;
    // Initialize counter objects for tau isolation
    fIDTaNC = fCounterPackager.addSubCounter("TaNCTenth", "TaNCTenth",
      makeTH<TH1F>(*fs, "TauTaNC", "TaNC;TaNC output;N_{jets}/0.02", 50, 0., 1.));
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation();
  }

  TauIDPFShrinkingConeTaNC::~TauIDPFShrinkingConeTaNC() { }
  
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
  TauIDPFShrinkingConeCombinedHPSTaNC::TauIDPFShrinkingConeCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    TauIDPFTauBase(iConfig, eventCounter, eventWeight, "HPSTaNC")
  {
    edm::Service<TFileService> fs;
    // Initialize counter objects for tau isolation
    fIDHPS = fCounterPackager.addSubCounter("HPSTaNC", "HPSTight", 0);
    fIDTaNC = fCounterPackager.addSubCounter("HPSTaNC", "TaNCTenth",
      makeTH<TH1F>(*fs, "TauCombinedHPSTaNC", "CombinedHPSTaNC;TaNC output;N_{jets}/0.02", 50, 0., 1.));
    // Histograms
    
    // Initialize rest counter objects
    createSelectionCounterPackagesBeyondIsolation();
  }

  TauIDPFShrinkingConeCombinedHPSTaNC::~TauIDPFShrinkingConeCombinedHPSTaNC() { }
  
  bool TauIDPFShrinkingConeCombinedHPSTaNC::passIsolation(const edm::Ptr<pat::Tau> tau) {
    // Apply HPS
    if (tau->tauID("byHPStight") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDHPS);
    // Apply TaNC
    // FIXME: doesn't work for HPS+TaNC
    /*
    fCounterPackager.fill(fIDTaNC, tau->tauID("byCombinedHPSTaNC"));
    */
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
    // FIXME: doesn't work for HPS+TaNC
    /*
    fCounterPackager.fill(fIDTaNC, tau->tauID("byCombinedHPSTaNC"));
    */
    if (tau->tauID("byTaNCvloose") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDTaNC);
    // All cuts passed, return true
    return true;
  }

  
}
