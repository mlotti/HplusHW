#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/L1Emulation.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

L1Emulation::L1Emulation(const edm::ParameterSet& iConfig) :
    l1tauSrc(iConfig.getParameter<edm::InputTag>("L1TauSrc")),
    l1cenSrc(iConfig.getParameter<edm::InputTag>("L1CenSrc"))
{}

L1Emulation::~L1Emulation(){}

void L1Emulation::setParameters(int n,double ptTau,double ptCen){
        njets      = n;
        l1tauPtCut = ptTau;
        l1cenPtCut = ptCen;
}

bool L1Emulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup){
        bool passed = false;
	l1jets.clear();

// L1 tau
        edm::Handle<l1extra::L1JetParticleCollection> l1TauHandle;

        iEvent.getByLabel(l1tauSrc, l1TauHandle);
        const l1extra::L1JetParticleCollection & l1Taus = *(l1TauHandle.product());
        l1extra::L1JetParticleCollection::const_iterator iJet;
        for(iJet = l1Taus.begin(); iJet != l1Taus.end(); ++iJet) {
                if(iJet->et() < l1tauPtCut) continue;
		passed = true;
		l1jets.push_back(iJet->p4());
        }

// L1 central jet
        edm::Handle<l1extra::L1JetParticleCollection> l1CentralJetHandle;
        iEvent.getByLabel(l1cenSrc, l1CentralJetHandle);
        const l1extra::L1JetParticleCollection & l1CentralJets = *(l1CentralJetHandle.product());
        for(iJet = l1CentralJets.begin(); iJet != l1CentralJets.end(); ++iJet) {
                if(iJet->et() < l1cenPtCut) continue;
                passed = true;
                l1jets.push_back(iJet->p4());
        }

        return passed;
}

std::vector<LorentzVector> L1Emulation::L1Jets(){
	return l1jets;
}
