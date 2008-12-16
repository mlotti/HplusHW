#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::cfgInput(const edm::ParameterSet& iConfig){

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

////	electronIdAlgo->setup(iConfig);
	barrelClusterShapeAssocProducer = iConfig.getParameter<edm::InputTag>("barrelClusterShapeAssociation");
	endcapClusterShapeAssocProducer = iConfig.getParameter<edm::InputTag>("endcapClusterShapeAssociation");

        trackCollectionSelection = iConfig.getParameter<InputTag>("TrackCollection");
	trajectoryInput = trackCollectionSelection;

	tauJetCorrection = new TauJetCorrector(iConfig);
}
