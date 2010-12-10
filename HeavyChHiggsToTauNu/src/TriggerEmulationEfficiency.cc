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
	l1_3j     = 0;
	l1quad    = 0;
	hltTau    = 0;
        hltMet    = 0;
        hltpfmht  = 0;
        hlt3jets  = 0;
        hlt4jets  = 0;

        passedTauMET     = 0;
        passedTauPFMHT   = 0;
        passedTau3j      = 0;
        passedTau3jMET   = 0;
        passedTau3jPFMHT = 0;
        passedTau4j      = 0;
        passedTau4jMET   = 0;
        passedTau4jPFMHT = 0;
}
TriggerEmulationEfficiency::~TriggerEmulationEfficiency(){
	cout << "All events       " << allEvents << endl;
	cout << "L1 tau passed    " << l1tau << endl;
        cout << "L1 3jets passed  " << l1_3j << endl;
	cout << "L1 quad passed   " << l1quad << endl;
	cout << "HLT Tau passed   " << hltTau << endl;
	cout << "HLT Met passed   " << hltMet << endl;
	cout << "HLT pfmht passed " << hltpfmht << endl;
	cout << "HLT 3jets passed " << hlt3jets << endl;
	cout << "HLT 4jets passed " << hlt4jets << endl;
	cout << endl;
	cout << "TauMET           " << passedTauMET << endl;
	cout << "TauPFMHT         " << passedTauPFMHT << endl;
	cout << "Tau3j            " << passedTau3j << endl;
	cout << "Tau3jMET         " << passedTau3jMET << endl;
	cout << "Tau3jPFMHT       " << passedTau3jPFMHT << endl;
	cout << "Tau4j            " << passedTau4j << endl;
	cout << "Tau4jMET         " << passedTau4jMET << endl;
	cout << "Tau4jPFMHT       " << passedTau4jPFMHT << endl;
	cout << endl;

	delete l1Emulation;
	delete hltNJetsEmulation;
	delete hltTauEmulation;
	delete hltMETEmulation;
	delete hltPFMHTEmulation;
}

void TriggerEmulationEfficiency::analyse(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	allEvents++;
// L1
	l1Emulation->setParameters(1,20,30);//n,ptTau,ptCen
	bool passedL1Tau = l1Emulation->passedEvent(iEvent,iSetup);
	std::vector<LorentzVector> l1jets = l1Emulation->L1Jets();

	if(passedL1Tau) l1tau++;

        l1Emulation->setParameters(3,25,25);
        bool passedL1_3Jet = l1Emulation->passedEvent(iEvent,iSetup);
        std::vector<LorentzVector> l1_3jets = l1Emulation->L1Jets();

        if(passedL1_3Jet) l1_3j++;

        l1Emulation->setParameters(4,8,8);
        bool passedL1QuadJet = l1Emulation->passedEvent(iEvent,iSetup);
        std::vector<LorentzVector> l1quadjets = l1Emulation->L1Jets();

	if(passedL1QuadJet) l1quad++;

// HLT
	// Jets
	hltNJetsEmulation->setParameters(3,20);//pt
	bool passedL1_3jHLT3Jets = hltNJetsEmulation->passedEvent(iEvent,iSetup,l1_3jets);
	std::vector<LorentzVector> hlt3jets = hltNJetsEmulation->HLTJets();

	hltNJetsEmulation->setParameters(4,20);
	bool passedL1quadHLT4Jets = hltNJetsEmulation->passedEvent(iEvent,iSetup,l1quadjets);
	std::vector<LorentzVector> hlt4jets = hltNJetsEmulation->HLTJets();

	// Tau
	hltTauEmulation->setParameters(20,15);//pt,ltr_pt
	bool passedL1TauHLTTau = hltTauEmulation->passedEvent(iEvent,iSetup,l1jets);

	bool passedL1_3jHLTTau = hltTauEmulation->passedEvent(iEvent,iSetup,hlt3jets);

	bool passedL1quadHLTTau = hltTauEmulation->passedEvent(iEvent,iSetup,hlt4jets);

	// MET
	hltMETEmulation->setParameters(35);
	bool passedHLTMET = hltMETEmulation->passedEvent(iEvent,iSetup);

	// PFMHT
	hltPFMHTEmulation->setParameters(35);
	bool passedHLTPFMHT = hltPFMHTEmulation->passedEvent(iEvent,iSetup);

// cross triggers
	if(passedL1Tau && passedL1TauHLTTau && passedHLTMET) passedTauMET++;
	if(passedL1Tau && passedL1TauHLTTau && passedHLTPFMHT) passedTauPFMHT++;
	if(passedL1_3Jet && passedL1_3jHLT3Jets && passedL1_3jHLTTau) passedTau3j++;
        if(passedL1_3Jet && passedL1_3jHLT3Jets && passedL1_3jHLTTau && passedHLTMET) passedTau3jMET++;
        if(passedL1_3Jet && passedL1_3jHLT3Jets && passedL1_3jHLTTau && passedHLTPFMHT) passedTau3jPFMHT++;
	if(passedL1QuadJet && passedL1quadHLT4Jets && passedL1quadHLTTau) passedTau4j++;
	if(passedL1QuadJet && passedL1quadHLT4Jets && passedL1quadHLTTau && passedHLTMET) passedTau4jMET++;
	if(passedL1QuadJet && passedL1quadHLT4Jets && passedL1quadHLTTau && passedHLTPFMHT) passedTau4jPFMHT++;

}
