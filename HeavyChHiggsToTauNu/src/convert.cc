#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerConverter.h"
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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyRootTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauResolutionAnalysis.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/BTauReco/interface/IsolatedTauTagInfo.h"

#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"


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

struct HLTTau {
  bool operator()(const reco::IsolatedTauTagInfo& tau) const {
    return tau.discriminator(0.1, 0.065, 0.4, 20., 1.);
  }
  void operator()(const edm::Handle<edm::View<reco::IsolatedTauTagInfo> >&, size_t i, MyJet *jet) const {
    jet->type = 15; // label for HLT object being tau
  }
};

struct MuonReplacementTagger {
  void operator()(const edm::Handle<edm::View<reco::Muon> >&, size_t i, MyJet *jet) const {
    jet->tagInfo["mu2tau_selectedMuon"] = 1;
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

template <class T, class C>
void addParticleCollections(MyEvent *saveEvent, const std::vector<edm::InputTag>& labels, const edm::Event& iEvent, C& converter) {
        for(std::vector<edm::InputTag>::const_iterator tag = labels.begin(); tag != labels.end(); ++tag) {
                getParticles<T>(saveEvent, *tag, iEvent, converter);
        }
}
template <class T, class C, class M>
void addParticleCollections(MyEvent *saveEvent, const std::vector<edm::InputTag>& labels, const edm::Event& iEvent, C& converter, const M& modify) {
        for(std::vector<edm::InputTag>::const_iterator tag = labels.begin(); tag != labels.end(); ++tag) {
                getParticles<T>(saveEvent, *tag, iEvent, converter, modify);
        }
}
template <class T, class C, class D>
void addParticleCollectionsIf(MyEvent *saveEvent, const std::vector<edm::InputTag>& labels, const edm::Event& iEvent, C& converter, const D& condition) {
        for(std::vector<edm::InputTag>::const_iterator tag = labels.begin(); tag != labels.end(); ++tag) {
                getParticlesIf<T>(saveEvent, *tag, iEvent, converter, condition);
        }
}
template <class T, class C, class D, class M>
void addParticleCollectionsIf(MyEvent *saveEvent, const std::vector<edm::InputTag>& labels, const edm::Event& iEvent, C& converter, const D& condition, const M& modify) {
        for(std::vector<edm::InputTag>::const_iterator tag = labels.begin(); tag != labels.end(); ++tag) {
                getParticlesIf<T>(saveEvent, *tag, iEvent, converter, condition, modify);
        }
}

void MyEventConverter::convert(const edm::Event& iEvent,const edm::EventSetup& iSetup){

	allEvents++;

        edm::ESHandle<TransientTrackBuilder> builder;
        iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",builder);
        transientTrackBuilder = builder.product();

//        tauMETTriggerAnalysis->analyse(iEvent);

//	if(!triggerDecision(iEvent)) return;
	triggeredEvents++;

        if(!VertexConverter::findPrimaryVertex(iEvent, vertexLabel, &primaryVertex)) return;
	eventsWithPrimaryVertex++;

////	getTrajectories(iEvent); // needed if tracker hits are to be stored

        trackEcalHitPoint.setEvent(iEvent, iSetup); // give event and event setup to our track associator wrapper
	MyEvent* saveEvent = new MyEvent;
        Finalizer finalizer(saveEvent, trackEcalHitPoint); // exception safe way of deleting MyEvent and resetting TrackEcalHitPoint

	saveEvent->eventNumber          = iEvent.id().event();
	saveEvent->runNumber		= iEvent.run();
	saveEvent->lumiNumber		= iEvent.luminosityBlock();

        TriggerConverter::getTriggerResults(iEvent, saveEvent->triggerResults, printTrigger);
        TriggerConverter::addTriggerObjects(saveEvent, iEvent);
        printTrigger = false;
	saveEvent->primaryVertex        = VertexConverter::convert(primaryVertex);
//	saveEvent->L1objects            = getL1objects(iEvent);

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
        MCConverter mcConverter(genJetLabel, simHitLabel, genParticleLabel, muonReplacementHepMcLabel);

        //getParticlesIf<reco::IsolatedTauTagInfo>(saveEvent, edm::InputTag("coneIsolationL3SingleTau"), iEvent, tauConverter, HLTTau(), HLTTau());

        addParticleCollections<reco::GsfElectron>(saveEvent, gsfElectronLabels, iEvent, electronConverter);
        addParticleCollections<pat::Electron>    (saveEvent, patElectronLabels, iEvent, electronConverter);

        //addParticleCollections<reco::Photon>    (saveEvent, photonLabels, iEvent, photonConverter);
        //addParticleCollections<reco::Conversion>(saveEvent, photonLabels, iEvent, photonConverter);

        addParticleCollections<reco::Muon>(saveEvent, muonLabels,    iEvent, muonConverter);
        addParticleCollections<pat::Muon> (saveEvent, patMuonLabels, iEvent, muonConverter);

        addParticleCollectionsIf<reco::CaloTau>(saveEvent, caloTauLabels, iEvent, tauConverter, TauHasLeadingTrack());
        addParticleCollectionsIf<reco::PFTau>  (saveEvent, pfTauLabels,   iEvent, tauConverter, TauHasLeadingTrack());
        addParticleCollections<pat::Tau>       (saveEvent, patTauLabels,  iEvent, tauConverter); 
	addParticleCollectionsIf<reco::CaloTau>(saveEvent, tcTauLabels, iEvent, tauConverter, TauHasLeadingTrack());

        addParticleCollections<reco::CaloJet>(saveEvent, caloJetLabels, iEvent, jetConverter);
        addParticleCollections<pat::Jet>     (saveEvent, patJetLabels,  iEvent, jetConverter);

        metConverter.convert(iEvent, saveEvent->mets);

        mcConverter.addMC(saveEvent, iEvent);

        try {
                getParticles<reco::Muon>(saveEvent, muonReplacementMuonLabel, iEvent, muonConverter, MuonReplacementTagger());
        } catch(const cms::Exception& e) {
          if(e.category() != "ProductNotFound")
            throw;
        }

	userRootTree->fillTree(saveEvent);
	savedEvents++;

//	tauResolutionAnalysis->analyse(iEvent);
}
