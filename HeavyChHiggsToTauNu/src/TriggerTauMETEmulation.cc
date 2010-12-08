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
    l1tauSrc(iConfig.getParameter<edm::InputTag>("L1TauSrc")),
    l1cenSrc(iConfig.getParameter<edm::InputTag>("L1CenSrc")),
    tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
    metSrc(iConfig.getParameter<edm::InputTag>("metSrc")),
    l1tauPtCut(iConfig.getParameter<double>("L1TauPtCut")),
    l1cenPtCut(iConfig.getParameter<double>("L1CenPtCut")),
    tauPtCut(iConfig.getParameter<double>("TauPtCut")),
    tauLTrkCut(iConfig.getParameter<double>("TauLeadTrkPtCut")),
    metCut(iConfig.getParameter<double>("METCut")),
    fEventWeight(eventWeight)
  {
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

  TriggerTauMETEmulation::~TriggerTauMETEmulation() {}

  TriggerTauMETEmulation::Data TriggerTauMETEmulation::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

        bool tau = tauSelection(iEvent);
        bool met = metSelection(iEvent);

        if(tau) {
//                ++counter_tau;
        }
        if(met) {
//                ++counter_met;
        }
        if(tau && met) {
//                ++counter_taumet;
        }
        bool passEvent = tau && met;
    	return Data(this, passEvent);
  }


  bool TriggerTauMETEmulation::tauSelection(const edm::Event& iEvent){
        bool tauFound = false;

// L1 tau
        edm::Handle<l1extra::L1JetParticleCollection> l1TauHandle;
        iEvent.getByLabel(l1tauSrc, l1TauHandle);
        const l1extra::L1JetParticleCollection & l1Taus = *(l1TauHandle.product());
        l1extra::L1JetParticleCollection::const_iterator iJet;
        for(iJet = l1Taus.begin(); iJet != l1Taus.end(); ++iJet) {
                if(iJet->et() < l1tauPtCut) continue;
//                counter_l1tau++;
                tauFound = HLTTauFound(iEvent,iJet->p4());
        }

        edm::Handle<l1extra::L1JetParticleCollection> l1CentralJetHandle;
        iEvent.getByLabel(l1cenSrc, l1CentralJetHandle);
        const l1extra::L1JetParticleCollection & l1CentralJets = *(l1CentralJetHandle.product());
        for(iJet = l1CentralJets.begin(); iJet != l1CentralJets.end(); ++iJet) {
                if(iJet->et() < l1cenPtCut) continue;
//                counter_l1cen++;
                tauFound = HLTTauFound(iEvent,iJet->p4());
        }

        return tauFound;
  }

  bool TriggerTauMETEmulation::HLTTauFound(const edm::Event& iEvent,const LorentzVector& p4){
        bool tauFound = false;
//std::cout << "check TauMETTriggerEmulator::HLTTauFound L1Tau " << p4.Eta() << " " << p4.Phi() << std::endl;
// HLT tau

        edm::Handle<edm::View<reco::CaloTau> > htaus;
        iEvent.getByLabel(tauSrc, htaus);
        edm::PtrVector<reco::CaloTau> taus = htaus->ptrVector();

        for(edm::PtrVector<reco::CaloTau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
                edm::Ptr<reco::CaloTau> iTau = *iter;

                double DR = ROOT::Math::VectorUtil::DeltaR(p4,iTau->p4());

                if(DR > 0.4) continue;
//std::cout << "check HLTTau " << iTau->p4().eta() << " " << iTau->p4().eta() << " " << DR << std::endl;
                if(iTau->isolationECALhitsEtSum() > 5) continue;

                if(!(iTau->pt() > tauPtCut)) continue;
//                counter_l2++;

                reco::TrackRef leadTrk = iTau->leadTrack();
                if(leadTrk.isNull() || !(leadTrk->pt() > tauLTrkCut)) continue;
//                counter_l25++;

                if(iTau->isolationTracks().size()) continue;
//                counter_l3++;

                tauFound = true;
        }

        return tauFound;
  }

  bool TriggerTauMETEmulation::metSelection(const edm::Event& iEvent){

        edm::Handle<edm::View<reco::MET> > hmet;
        iEvent.getByLabel(metSrc, hmet);

        edm::Ptr<reco::MET> met = hmet->ptrAt(0);

        return met->et() > metCut;
  }
}
