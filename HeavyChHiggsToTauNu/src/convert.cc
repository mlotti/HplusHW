#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CaloTowerConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EcalClusterConverter.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/getParticles.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PhotonConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetConverter.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

struct Finalizer {
  Finalizer(MyEvent *ev, TrackEcalHitPoint& tehp):
    event(ev), trackEcalHitPoint(tehp) {}
  ~Finalizer() {
    trackEcalHitPoint.reset();
    delete event;
  }
  
  MyEvent *event;
  TrackEcalHitPoint& trackEcalHitPoint;
};

struct MuonReplacementTagger {
  void tag(const edm::Handle<edm::View<reco::Muon> >, size_t i, std::map<std::string, double>& tagInfo) const {
    tagInfo["mu2tau_selectedMuon"] = 1;
  }
};

struct TauHasLeadingTrack {
  bool operator()(const reco::CaloTau& tau) const {
    return tau.leadTrack().isNonnull();
  }
  bool operator()(const reco::PFTau& tau) const {
    return tau.leadPFChargedHadrCand().isNonnull();
  }
};

void MyEventConverter::convert(const edm::Event& iEvent,const edm::EventSetup& iSetup){

	allEvents++;

//        tauMETTriggerAnalysis->analyse(iEvent);

//	if(!triggerDecision(iEvent)) return;
	triggeredEvents++;

        if(!primaryVertexFound(iEvent)) return;
	eventsWithPrimaryVertex++;

////	getTrajectories(iEvent); // needed if tracker hits are to be stored

        trackEcalHitPoint.setEvent(iEvent, iSetup); // give event and event setup to our track associator wrapper
	MyEvent* saveEvent = new MyEvent;
        Finalizer finalizer(saveEvent, trackEcalHitPoint); // exception safe way of deleting MyEvent and resetting TrackEcalHitPoint

	saveEvent->eventNumber          = iEvent.id().event();
	saveEvent->runNumber		= iEvent.run();
	saveEvent->lumiNumber		= iEvent.luminosityBlock();

	getTriggerResults(iEvent, edm::InputTag("TriggerResults::HLT"), saveEvent->triggerResults);
	saveEvent->primaryVertex        = VertexConverter::convert(primaryVertex);
//	saveEvent->L1objects            = getL1objects(iEvent);
//	saveEvent->HLTobjects           = getHLTObjects(iEvent);

        EcalClusterLazyTools ecalTools(iEvent,iSetup,reducedBarrelRecHitCollection,reducedEndcapRecHitCollection);

        TrackConverter trackConverter(iEvent, trackCollectionSelection);
        ImpactParameterConverter ipConverter(primaryVertex);
        CaloTowerConverter ctConverter(iEvent, iSetup);
        EcalClusterConverter ecConverter(iEvent, barrelBasicClustersInput, endcapBasicClustersInput);

        ElectronConverter electronConverter(trackConverter, ipConverter, *transientTrackBuilder, ecalTools, iEvent, electronIdLabels);
        MuonConverter muonConverter(trackConverter, ipConverter, *transientTrackBuilder);
        //PhotonConverter photonConverter(trackConverter, ipConverter, *transientTrackBuilder);
        TauConverter tauConverter(trackConverter, ipConverter, trackEcalHitPoint, ctConverter, ecConverter, *transientTrackBuilder, *tauJetCorrection);
        JetConverter jetConverter(trackConverter, iEvent, iSetup, jetEnergyCorrectionTypes, btaggingAlgos);

        //saveEvent->addCollection("electrons",              getParticles<reco::GsfElectron>(edm::InputTag("pixelMatchGsfElectrons"),        iEvent, electronConverter));
        saveEvent->addCollection("electrons",              getParticles<reco::GsfElectron>(edm::InputTag("gsfElectrons"),                  iEvent, electronConverter));
        //saveEvent->addCollection("patelectrons",           getParticles<pat::Electron>    (edm::InputTag("selectedLayer1Electrons"),       iEvent, electronConverter));

        //saveEvent->addCollection("photons",                getParticles<reco::Photon>     (edm::InputTag("correctedPhotons"),              iEvent, photonConverter));
        //saveEvent->addCollection("conversions",            getParticles<reco::Conversion> (edm::InputTag("correctedPhotons"),              iEvent, photonConverter));

        saveEvent->addCollection("muons",                  getParticles<reco::Muon>       (edm::InputTag("muons"),                         iEvent, muonConverter));
	//saveEvent->addCollection("patmuons",               getParticles<pat::Muon>        (edm::InputTag("selectedLayer1Muons"),           iEvent, muonConverter));

        saveEvent->addCollection("calotaus",               getParticlesIf<reco::CaloTau>  (edm::InputTag("caloRecoTauProducer"),           iEvent, tauConverter, TauHasLeadingTrack()));
        saveEvent->addCollection("fixedConePFTaus",        getParticlesIf<reco::PFTau>    (edm::InputTag("fixedConePFTauProducer"),        iEvent, tauConverter, TauHasLeadingTrack()));
        saveEvent->addCollection("fixedConeHighEffPFTaus", getParticlesIf<reco::PFTau>    (edm::InputTag("fixedConeHighEffPFTauProducer"), iEvent, tauConverter, TauHasLeadingTrack()));
        saveEvent->addCollection("shrinkingConePFTaus",    getParticlesIf<reco::PFTau>    (edm::InputTag("shrinkingConePFTauProducer"),    iEvent, tauConverter, TauHasLeadingTrack()));
        //saveEvent->addCollection("pattaus",                getParticles<pat::Tau>         (edm::InputTag("selectedLayer1Taus"),            iEvent, tauConverter));
                                                                                            
        saveEvent->addCollection("icone05jets",            getParticles<reco::CaloJet>    (edm::InputTag("iterativeCone5CaloJets"),        iEvent, jetConverter));
        //saveEvent->addCollection("patjets",                getParticles<pat::Jet>         (edm::InputTag("selectedLayer1Jets"),            iEvent, jetConverter));

	getMET(iEvent, saveEvent->mets);

        saveEvent->hasMCdata            = true;
        MCConverter::addMCParticles(iEvent, saveEvent->mcParticles, saveEvent->mcMET);
	saveEvent->mcPrimaryVertex      = MCConverter::getMCPrimaryVertex(iEvent);
        MCConverter::setSimTracks(iEvent, *saveEvent);

        try {
          saveEvent->addCollection("removedMuons", getParticles<reco::Muon> (edm::InputTag("selectedMuons"), iEvent,      muonConverter, MuonReplacementTagger()));
        } catch(const cms::Exception& e) {
          if(e.category() != "ProductNotFound")
            throw;
        }

	userRootTree->fillTree(saveEvent);
	savedEvents++;

//	tauResolutionAnalysis->analyse(iEvent);
}
