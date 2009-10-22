#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/getParticles.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonConverter.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

void MyEventConverter::convert(const edm::Event& iEvent,const edm::EventSetup& iSetup){

	allEvents++;

//        tauMETTriggerAnalysis->analyse(iEvent);

//	if(!triggerDecision(iEvent)) return;
	triggeredEvents++;

        if(!primaryVertexFound(iEvent)) return;
	eventsWithPrimaryVertex++;

	getCaloHits(iEvent); // needed if calohits are to be stored
        getTracks(iEvent); // needed if tracks inside jet cones are to be stored
////	getTrajectories(iEvent); // needed if tracker hits are to be stored
        getEcalClusters(iEvent); // needed if ecal clusters for taus are to be stored

        trackEcalHitPoint.setEvent(iEvent, iSetup); // give event and event setup to our track associator wrapper
        ImpactParameterConverter ipConverter(primaryVertex);

	MyEvent* saveEvent = new MyEvent;
	saveEvent->eventNumber          = iEvent.id().event();
	saveEvent->runNumber		= iEvent.run();
	saveEvent->lumiNumber		= iEvent.luminosityBlock();

	getTriggerResults(iEvent, edm::InputTag("TriggerResults::HLT"), saveEvent->triggerResults);
	saveEvent->primaryVertex        = VertexConverter::convert(primaryVertex);
//	saveEvent->L1objects            = getL1objects(iEvent);
//	saveEvent->HLTobjects           = getHLTObjects(iEvent);

	saveEvent->addCollection("electrons",getElectrons(iEvent,iSetup, edm::InputTag("pixelMatchGsfElectrons")));
//	saveEvent->photons              = getPhotons(iEvent);

	saveEvent->addCollection("muons",    getParticles<reco::Muon>(edm::InputTag("muons"),               iEvent, MuonConverter(*transientTrackBuilder, ipConverter)));
	//saveEvent->addCollection("patmuons", getParticles<pat::Muon> (edm::InputTag("selectedLayer1Muons"), iEvent, MuonConverter(*transientTrackBuilder, ipConverter)));
	saveEvent->addCollection("calotaus",getTaus(iEvent, edm::InputTag("caloRecoTauProducer")));
	saveEvent->addCollection("fixedConePFTaus",getPFTaus(iEvent, edm::InputTag("fixedConePFTauProducer")));
	saveEvent->addCollection("fixedConeHighEffPFTaus",getPFTaus(iEvent, edm::InputTag("fixedConeHighEffPFTauProducer")));
        saveEvent->addCollection("shrinkingConePFTaus",getPFTaus(iEvent, edm::InputTag("shrinkingConePFTauProducer")));
	saveEvent->addCollection("icone05jets",getJets(iEvent, edm::InputTag("iterativeCone5CaloJets")));

	getMET(iEvent, saveEvent->mets);
        saveEvent->hasMCdata            = true;
        MCConverter::addMCParticles(iEvent, saveEvent->mcParticles, saveEvent->mcMET);
	saveEvent->mcPrimaryVertex      = MCConverter::getMCPrimaryVertex(iEvent);
        MCConverter::setSimTracks(iEvent, *saveEvent);

	saveEvent->addCollection("removedMuons",getExtraObjects(iEvent));
////	saveEvent->addExtraObjects("",getExtraObjects(iEvent));

	userRootTree->fillTree(saveEvent);
	savedEvents++;

        trackEcalHitPoint.reset();

	delete saveEvent;

//	tauResolutionAnalysis->analyse(iEvent);
}
