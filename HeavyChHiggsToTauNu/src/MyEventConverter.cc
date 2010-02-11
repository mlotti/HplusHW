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
        vertexLabel(iConfig.getParameter<InputTag>("Vertices")),
        trackCollectionSelection(iConfig.getParameter<InputTag>("TrackCollection")),
        gsfElectronLabels(iConfig.getParameter<std::vector<InputTag> >("GsfElectrons")),
        patElectronLabels(iConfig.getParameter<std::vector<InputTag> >("PATElectrons")),
        //photonLabels(iConfig.getParameter<std::vector<InputTag> >("Photons")),
        muonLabels(iConfig.getParameter<std::vector<InputTag> >("Muons")),
        patMuonLabels(iConfig.getParameter<std::vector<InputTag> >("PATMuons")),
        pfTauLabels(iConfig.getParameter<std::vector<InputTag> >("PFTaus")),
        patTauLabels(iConfig.getParameter<std::vector<InputTag> >("PATTaus")),
	tcTauLabels(iConfig.getParameter<std::vector<InputTag> >("TCTaus")),
        caloJetLabels(iConfig.getParameter<std::vector<InputTag> >("CaloJets")),
        patJetLabels(iConfig.getParameter<std::vector<InputTag> >("PATJets")),
        muonReplacementMuonLabel(iConfig.getParameter<edm::InputTag>("MuonReplacementMuons")),
        genParticleLabel(iConfig.getParameter<InputTag>("GenParticles")),
	genVisibleTauLabel(iConfig.getParameter<InputTag>("VisibleTaus")),
        muonReplacementGenLabel(iConfig.getParameter<InputTag>("MuonReplacementGen")),
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
        printTrigger(true)
{
        const std::vector<edm::ParameterSet>& calotaus(iConfig.getParameter<std::vector<edm::ParameterSet> >("CaloTaus"));
        caloTauLabels.reserve(calotaus.size());
        caloTauCorrections.reserve(calotaus.size());
        for(size_t i=0; i<calotaus.size(); ++i) {
                caloTauLabels.push_back(calotaus[i].getParameter<edm::InputTag>("src"));
                caloTauCorrections.push_back(std::make_pair(calotaus[i].getParameter<edm::InputTag>("src"),
                                                            calotaus[i].getParameter<std::vector<std::string> >("corrections")));
        }
}

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
