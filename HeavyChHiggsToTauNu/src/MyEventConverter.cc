#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyRootTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauResolutionAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauMETTriggerAnalysis.h"

#include "JetMETCorrections/TauJet/interface/TauJetCorrector.h"

#include<iostream>

using std::vector;
using edm::InputTag;
using std::cout;
using std::endl;

MyEventConverter::MyEventConverter(const edm::ParameterSet& iConfig):
//        HLTSelection(iConfig.getParameter< vector<InputTag> >("HLTSelection")),
        trackCollectionSelection(iConfig.getParameter<InputTag>("TrackCollection")),
        gsfElectronLabels(iConfig.getParameter<std::vector<InputTag> >("GsfElectrons")),
        patElectronLabels(iConfig.getParameter<std::vector<InputTag> >("PATElectrons")),
        //photonLabels(iConfig.getParameter<std::vector<InputTag> >("Photons")),
        muonLabels(iConfig.getParameter<std::vector<InputTag> >("Muons")),
        patMuonLabels(iConfig.getParameter<std::vector<InputTag> >("PATMuons")),
        caloTauLabels(iConfig.getParameter<std::vector<InputTag> >("CaloTaus")),
        pfTauLabels(iConfig.getParameter<std::vector<InputTag> >("PFTaus")),
        patTauLabels(iConfig.getParameter<std::vector<InputTag> >("PATTaus")),
        caloJetLabels(iConfig.getParameter<std::vector<InputTag> >("CaloJets")),
        patJetLabels(iConfig.getParameter<std::vector<InputTag> >("PATJets")),
        genParticleLabel(iConfig.getParameter<InputTag>("GenParticles")),
        muonReplacementHepMcLabel(iConfig.getParameter<InputTag>("MuonReplacementHepMc")),
        genJetLabel(iConfig.getParameter<InputTag>("GenJets")),
        simHitLabel(iConfig.getParameter<InputTag>("SimHits")),
//	barrelClusterShapeAssocProducer(iConfig.getParameter<edm::InputTag>("barrelClusterShapeAssociation")),
//	endcapClusterShapeAssocProducer(iConfig.getParameter<edm::InputTag>("endcapClusterShapeAssociation")),
	reducedBarrelRecHitCollection(iConfig.getParameter<edm::InputTag>("ReducedBarrelRecHitCollection")),
	reducedEndcapRecHitCollection(iConfig.getParameter<edm::InputTag>("ReducedEndcapRecHitCollection")),
        transientTrackBuilder(0),
        tauJetCorrection(new TauJetCorrector(iConfig)),
	jetEnergyCorrectionTypes(iConfig.getParameter<std::vector<std::string> >("JetEnergyCorrection")),
        btaggingAlgos(iConfig.getParameter<std::vector<std::string> >("BTaggingAlgorithms")),
	electronIdLabels(iConfig.getParameter<std::vector<edm::InputTag> >("ElectronIdLabels")),
	barrelBasicClustersInput(iConfig.getParameter<InputTag>("BarrelBasicClustersSource")),
        endcapBasicClustersInput(iConfig.getParameter<InputTag>("EndcapBasicClustersSource")),
        trajectoryInput(trackCollectionSelection),
        allEvents(0),
	triggeredEvents(0),
        eventsWithPrimaryVertex(0),
	savedEvents(0),
	userRootTree(new MyRootTree(iConfig.getParameter<std::string>("fileName").c_str())),
        tauResolutionAnalysis(new TauResolutionAnalysis()),
	tauMETTriggerAnalysis(new TauMETTriggerAnalysis(userRootTree)),
        trackEcalHitPoint(iConfig),
        metConverter(iConfig.getParameter<std::vector<edm::InputTag> >("METCollections"), edm::InputTag("pfMet"), edm::InputTag("tcMet")),
        printTrigger(true)
{}

MyEventConverter::~MyEventConverter(){

        cout << endl << endl;
        cout << "    SUMMARY " << endl << endl;
        cout << "    All events   : " << allEvents << endl;
//        cout << "    HLT          : " << triggeredEvents << endl;
//        cout << "    PV reconstr. : " << eventsWithPrimaryVertex << endl;
        cout << "    saved events : " << savedEvents << endl;
        cout << endl << endl;


        delete tauMETTriggerAnalysis;

	userRootTree->setAcceptance("allEvents",allEvents);
//	userRootTree->setAcceptance("HLTselection",triggeredEvents);
//        userRootTree->setAcceptance("eventsWithPrimaryVertex",eventsWithPrimaryVertex);
        userRootTree->setAcceptance("savedEvents",savedEvents);
        delete userRootTree;

	delete tauResolutionAnalysis;
}
