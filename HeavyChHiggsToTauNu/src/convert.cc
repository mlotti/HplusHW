#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::convert(const edm::Event& iEvent){

	allEvents++;

//        tauMETTriggerAnalysis->analyse(iEvent);

//	if(!triggerDecision(iEvent)) return;
	triggeredEvents++;

        if(!primaryVertexFound(iEvent)) return;
	eventsWithPrimaryVertex++;

	getCaloHits(iEvent); // needed if calohits are to be stored
        getTracks(iEvent); // needed if tracks inside jet cones are to be stored
////	getTrajectories(iEvent); // needed if tracker hits are to be stored

	MyEvent* saveEvent = new MyEvent;
	saveEvent->eventNumber          = iEvent.id().event();
	saveEvent->runNumber		= iEvent.run();

	saveEvent->primaryVertex        = getPrimaryVertex();
//	saveEvent->L1objects            = getL1objects(iEvent);
//	saveEvent->HLTobjects           = getHLTObjects(iEvent);

	saveEvent->electrons            = getElectrons(iEvent);
//	saveEvent->photons              = getPhotons(iEvent);

	saveEvent->muons                = getMuons(iEvent);
	saveEvent->taujets              = getTaus(iEvent);
//	saveEvent->pftaus               = getPFTaus(iEvent);
	saveEvent->jets                 = getJets(iEvent);
	saveEvent->MET                  = getMET(iEvent);

        saveEvent->mcParticles          = getMCParticles(iEvent);
	saveEvent->mcMET                = getMCMET();
	saveEvent->mcPrimaryVertex      = getMCPrimaryVertex(iEvent);
        saveEvent->simTracks            = getSimTracks(iEvent,saveEvent);


	userRootTree->fillTree(saveEvent);
	savedEvents++;

	delete saveEvent;

//	tauResolutionAnalysis->analyse(iEvent);
}
