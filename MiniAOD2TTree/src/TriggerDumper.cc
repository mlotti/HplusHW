#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

TriggerDumper::TriggerDumper(edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;

    triggerResults = inputCollection.getParameter<edm::InputTag>("TriggerResults");
    triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
    useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
    iBit = new bool[triggerBits.size()];
}
TriggerDumper::~TriggerDumper(){}

void TriggerDumper::book(TTree* tree){
    booked = true;
    tree->Branch("L1_ETM",&L1MET);

    for(size_t i = 0; i < triggerBits.size(); ++i){
	tree->Branch(triggerBits[i].c_str(),&iBit[i]);
    }
}

bool TriggerDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    edm::Handle<std::vector<l1extra::L1EtMissParticle> > l1etmhandle;
    iEvent.getByLabel(edm::InputTag("l1extraParticles","MET"), l1etmhandle);
    if(l1etmhandle.isValid()){
	L1MET = l1etmhandle.product()->begin()->et();
    }

    iEvent.getByLabel(triggerResults,handle);
    if(handle.isValid()){
        edm::TriggerResults tr = *handle;
	bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
	std::vector<std::string> hlNames;
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);

	for(size_t i = 0; i < triggerBits.size(); ++i){
	    int n = 0;
	    for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if(triggerBits[i] == *j) {
		    iBit[i] = handle->accept(n);
		    continue;
		}
		n++;
	    }  
	}
    }
/*
    edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
    iEvent.getByLabel(edm::InputTag("selectedPatTrigger"),patTriggerObjects);
    if(patTriggerObjects.isValid()){
	for(pat::TriggerObjectStandAloneCollection::const_iterator patTriggerObject = patTriggerObjects->begin();
            patTriggerObject != patTriggerObjects->end(); ++patTriggerObject ) {
	    if(patTriggerObject->id(trigger::TriggerMET)){
		std::cout << "Trigger MET " << patTriggerObject->p4().Pt() << std::endl;
	    }
//	    patTriggerObject->p4(),patTriggerObject->hasPathName
	}
//	const pat::TriggerObjectStandAlone* tos = hobjects.product();
//	std::vector<pat::TriggerObjectStandAlone> objs = hobjects.product();
    }
*/
    return filter();
}

bool TriggerDumper::filter(){
    if(!useFilter) return true;

    bool passed = false;
    for(size_t i = 0; i < triggerBits.size(); ++i){
	if(iBit[i]) passed = true;
    }
    return passed;
}

void TriggerDumper::reset(){
    if(booked){
      for(size_t i = 0; i < triggerBits.size(); ++i) iBit[i] = 0;
      L1MET = 0;
    }
}
