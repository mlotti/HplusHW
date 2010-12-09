#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEmulationEfficiency.h"
#include <iostream>

using namespace std;

TriggerEmulationEfficiency::TriggerEmulationEfficiency(const edm::ParameterSet& iConfig) {
	l1Emulation = new L1Emulation(iConfig);
	hltTauEmulation = new HLTTauEmulation(iConfig);
	hltMETEmulation = new HLTMETEmulation(iConfig);
	hltPFMHTEmulation = new HLTPFMHTEmulation(iConfig);
	hltNJetsEmulation = new HLTNJetsEmulation(iConfig);

	allEvents = 0;
	l1tau     = 0;
	l1quad    = 0;
	hltTau    = 0;
        hltMet    = 0;
        hltpfmht  = 0;
        hlt3jets  = 0;
        hlt4jets  = 0;
}
TriggerEmulationEfficiency::~TriggerEmulationEfficiency(){
	cout << "All events       " << allEvents << endl;
	cout << "L1 tau passed    " << l1tau << endl;
	cout << "L1 quad passed   " << l1quad << endl;
	cout << "HLT Tau passed   " << hltTau << endl;
	cout << "HLT Met passed   " << hltMet << endl;
	cout << "HLT pfmht passed " << hltpfmht << endl;
	cout << "HLT 3jets passed " << hlt3jets << endl;
	cout << "HLT 4jets passed " << hlt4jets << endl;

	delete l1Emulation;
}

void TriggerEmulationEfficiency::analyse(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	allEvents++;

	l1Emulation->setParameters(1,20,30);
	bool passedL1Tau = l1Emulation->passedEvent(iEvent,iSetup);
	std::vector<LorentzVector> l1jets = l1Emulation->L1Jets();

	if(passedL1Tau) l1tau++;


        l1Emulation->setParameters(4,8,8);
        bool passedL1QuadJet = l1Emulation->passedEvent(iEvent,iSetup);
        std::vector<LorentzVector> l1quadjets = l1Emulation->L1Jets();

	if(passedL1QuadJet) l1quad++;


}
