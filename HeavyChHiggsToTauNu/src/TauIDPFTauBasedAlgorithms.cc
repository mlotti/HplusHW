#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBasedAlgorithms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  // TauIDPFHPS ---------------------------------------------
  TauIDPFHPS::TauIDPFHPS(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, const std::string& baseLabel, TFileDirectory& myDir):
    TauIDPFTauBase(iConfig, eventCounter, histoWrapper, baseLabel, myDir)
  { }
  TauIDPFHPS::~TauIDPFHPS() { }

  bool TauIDPFHPS::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.fill(fIDDecayModeFinding, tau->decayMode());
    if(tau->tauID("decayModeFinding") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    return true;
  }

  // TauIDPFTaNC --------------------------------------------
  TauIDPFTaNC::TauIDPFTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label, TFileDirectory& myDir):
    TauIDPFTauBase(iConfig, eventCounter, histoWrapper, label, myDir)
  { }

  TauIDPFTaNC::~TauIDPFTaNC() { }
  
  bool TauIDPFTaNC::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    // No decay mode finding equivalent in TaNC, always pass true
    return true;
  }

  // TauIDPFCombinedHPSTaNC --------------------------------------------
  /*
    TauIDPFCombinedHPSTaNC::TauIDPFCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, int prongCount, std::string label, TFileDirectory& myDir):
    TauIDPFHPSBase(iConfig, eventCounter, histoWrapper, label, myDir)
  { }

  TauIDPFCombinedHPSTaNC::~TauIDPFCombinedHPSTaNC() { }

  bool TauIDPFCombinedHPSTaNC::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    if(tau->tauID("decayModeFinding") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    return true;
  }
  */
}
