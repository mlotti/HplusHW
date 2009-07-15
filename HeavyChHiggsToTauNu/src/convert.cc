#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::convert(const edm::Event& iEvent,const edm::EventSetup& iSetup){
cout << "check1" << endl;
	allEvents++;

//        tauMETTriggerAnalysis->analyse(iEvent);

//	if(!triggerDecision(iEvent)) return;
	triggeredEvents++;

        if(!primaryVertexFound(iEvent)) return;
	eventsWithPrimaryVertex++;

	getCaloHits(iEvent); // needed if calohits are to be stored
        getTracks(iEvent); // needed if tracks inside jet cones are to be stored
////	getTrajectories(iEvent); // needed if tracker hits are to be stored
cout << "check2" << endl;
	MyEvent* saveEvent = new MyEvent;
	saveEvent->eventNumber          = iEvent.id().event();
	saveEvent->runNumber		= iEvent.run();
	saveEvent->lumiNumber		= iEvent.luminosityBlock();

	saveEvent->triggerResults       = getTriggerResults(iEvent);
	saveEvent->primaryVertex        = getPrimaryVertex();
//	saveEvent->L1objects            = getL1objects(iEvent);
//	saveEvent->HLTobjects           = getHLTObjects(iEvent);
cout << "check3" << endl;
	saveEvent->addCollection("electrons",getElectrons(iEvent,iSetup));
//	saveEvent->photons              = getPhotons(iEvent);
cout << "check4" << endl;
	saveEvent->addCollection("muons",getMuons(iEvent));
	saveEvent->addCollection("calotaus",getTaus(iEvent));
	saveEvent->addCollection("pftaus",getPFTaus(iEvent));
	saveEvent->addCollection("icone05jets",getJets(iEvent));
cout << "check5" << endl;
	saveEvent->mets			= getMET(iEvent);
//	saveEvent->addMET("pfMET",getPFMET(iEvent));
//	saveEvent->addMET("tcMET",getTCMET(iEvent));

        saveEvent->mcParticles          = getMCParticles(iEvent);
	saveEvent->mcMET                = getMCMET();
	saveEvent->mcPrimaryVertex      = getMCPrimaryVertex(iEvent);
        saveEvent->simTracks            = getSimTracks(iEvent,saveEvent);

	saveEvent->addCollection("removedMuons",getExtraObjects(iEvent));
////	saveEvent->addExtraObjects("",getExtraObjects(iEvent));
cout << "check6" << endl;
	userRootTree->fillTree(saveEvent);
	savedEvents++;
cout << "check7" << endl;
	delete saveEvent;
cout << "check8" << endl;
//	tauResolutionAnalysis->analyse(iEvent);
}
