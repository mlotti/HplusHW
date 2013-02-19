#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "Math/VectorUtil.h"

namespace HPlus {
  TriggerTauMETEmulation::Data::Data():
    fPassedEvent(false) {}
  TriggerTauMETEmulation::Data::~Data() {}

  TriggerTauMETEmulation::TriggerTauMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper) {
        l1Emulation     = new L1Emulation(iConfig);
        hltTauEmulation = new HLTTauEmulation(iConfig);
        hltMETEmulation = new HLTMETEmulation(iConfig);
/*
        edm::Service<TFileService> fs;
        h_alltau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_alltau", "h_alltau", 25, 0, 100);
        h_allmet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_allmet", "h_allmet", 25, 0, 100);
        h_tau    = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_tau", "h_tau", 25, 0, 100);
        h_met    = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_met", "h_met", 25, 0, 100);
        h_taumet_tau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_taumet_tau", "h_taumet_tau", 25, 0, 100);
        h_taumet_met = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "h_taumet_met", "h_taumet_met", 25, 0, 100);
*/
  }

  TriggerTauMETEmulation::~TriggerTauMETEmulation() {
	delete l1Emulation;
	delete hltTauEmulation;
	delete hltMETEmulation;
  }


  TriggerTauMETEmulation::Data TriggerTauMETEmulation::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  TriggerTauMETEmulation::Data TriggerTauMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  TriggerTauMETEmulation::Data TriggerTauMETEmulation::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;
    // L1
    l1Emulation->setParameters(1,20,30);//n,ptTau,ptCen
    bool passedL1Tau = l1Emulation->passedEvent(iEvent,iSetup);
    std::vector<LorentzVector> l1jets = l1Emulation->L1Jets();

    // Tau
    hltTauEmulation->setParameters(20,15);//pt,ltr_pt
    bool passedL1TauHLTTau = hltTauEmulation->passedEvent(iEvent,iSetup,l1jets);

    // MET
    hltMETEmulation->setParameters(35);
    bool passedHLTMET = hltMETEmulation->passedEvent(iEvent,iSetup);

    output.fPassedEvent = passedL1Tau && passedL1TauHLTTau && passedHLTMET;
    return output;
  }

}
