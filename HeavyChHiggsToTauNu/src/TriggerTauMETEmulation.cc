#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"

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
#include "TH1F.h"

namespace HPlus {
  TriggerTauMETEmulation::Data::Data(const TriggerTauMETEmulation *TriggerTauMETEmulation, bool passedEvent):
    fTriggerTauMETEmulation(TriggerTauMETEmulation), fPassedEvent(passedEvent) {}
  TriggerTauMETEmulation::Data::~Data() {}

  TriggerTauMETEmulation::TriggerTauMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight)
  {
        l1Emulation     = new L1Emulation(iConfig);
        hltTauEmulation = new HLTTauEmulation(iConfig);
        hltMETEmulation = new HLTMETEmulation(iConfig);
/*
        edm::Service<TFileService> fs;
        h_alltau = fs->make<TH1F>("h_alltau", "h_alltau", 25, 0, 100);
        h_allmet = fs->make<TH1F>("h_allmet", "h_allmet", 25, 0, 100);
        h_tau    = fs->make<TH1F>("h_tau", "h_tau", 25, 0, 100);
        h_met    = fs->make<TH1F>("h_met", "h_met", 25, 0, 100);
        h_taumet_tau = fs->make<TH1F>("h_taumet_tau", "h_taumet_tau", 25, 0, 100);
        h_taumet_met = fs->make<TH1F>("h_taumet_met", "h_taumet_met", 25, 0, 100);
*/
  }

  TriggerTauMETEmulation::~TriggerTauMETEmulation() {
	delete l1Emulation;
	delete hltTauEmulation;
	delete hltMETEmulation;
  }

  TriggerTauMETEmulation::Data TriggerTauMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

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

        bool passEvent = passedL1Tau && passedL1TauHLTTau && passedHLTMET;
    	return Data(this, passEvent);
  }

}
