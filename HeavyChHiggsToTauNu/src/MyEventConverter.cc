#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyEventConverter::MyEventConverter(const edm::ParameterSet& iConfig):
  trackAssociator_(iConfig) {
        init(iConfig);
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


void MyEventConverter::init(const edm::ParameterSet& iConfig){

///	electronIdAlgo = new CutBasedElectronID();
	userRootTree = new MyRootTree(iConfig.getParameter<std::string>("fileName").c_str());

	// counters
	allEvents 		= 0;
	triggeredEvents 	= 0;
	eventsWithPrimaryVertex = 0;
	savedEvents 		= 0;

	printTrigger = true;

	tauResolutionAnalysis = new TauResolutionAnalysis();
	tauMETTriggerAnalysis = new TauMETTriggerAnalysis(userRootTree);


	triggerTable = iConfig.getParameter<InputTag>("TriggerTable");
	HLTSelection = iConfig.getParameter< vector<InputTag> >("HLTSelection");

/*
	tauInputType = (iConfig.getParameter<InputTag>("TauInputType")).label();
	vector<InputTag> HLTSelection = iConfig.getParameter< vector<InputTag> >("HLTSelection");
	for(vector<InputTag>::const_iterator i = HLTSelection.begin(); i != HLTSelection.end(); i++){
		string name = i->label();
		triggerdecision[name] = false;
	}
*/
	jetEnergyCorrectionTypes = iConfig.getParameter<vector<InputTag> >("JetEnergyCorrection");
        btaggingAlgos = iConfig.getParameter<vector<InputTag> >("BTaggingAlgorithms");

	metCollections = iConfig.getParameter<vector<InputTag> >("METCollections");

	electronIdLabels = iConfig.getParameter<vector<InputTag> >("ElectronIdLabels");
////	electronIdAlgo->setup(iConfig);
//	barrelClusterShapeAssocProducer = iConfig.getParameter<edm::InputTag>("barrelClusterShapeAssociation");
//	endcapClusterShapeAssocProducer = iConfig.getParameter<edm::InputTag>("endcapClusterShapeAssociation");
	reducedBarrelRecHitCollection = iConfig.getParameter<edm::InputTag>("ReducedBarrelRecHitCollection");
	reducedEndcapRecHitCollection = iConfig.getParameter<edm::InputTag>("ReducedEndcapRecHitCollection");

        trackCollectionSelection = iConfig.getParameter<InputTag>("TrackCollection");
	trajectoryInput = trackCollectionSelection;

	tauJetCorrection = new TauJetCorrector(iConfig);

        // ECAL clusters 
	BarrelBasicClustersInput = iConfig.getParameter<InputTag>("BarrelBasicClustersSource"); 
	EndcapBasicClustersInput = iConfig.getParameter<InputTag>("EndcapBasicClustersSource"); 
	
}
