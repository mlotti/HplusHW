#include "HiggsAnalysis/MiniAOD2TTree/interface/GenWeightDumper.h"


GenWeightDumper::GenWeightDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    token = new edm::EDGetTokenT<GenEventInfoProduct>[inputCollections.size()];

    for(size_t i = 0; i < inputCollections.size(); ++i){
        edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
        token[i] = iConsumesCollector.consumes<GenEventInfoProduct>(inputtag);
    }
    
    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
    }
}

GenWeightDumper::~GenWeightDumper(){}

void GenWeightDumper::book(TTree* tree){
    booked = true;
    tree->Branch("GenWeight",&GenWeight);
}

bool GenWeightDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t i = 0; i < inputCollections.size(); ++i){
	
	edm::Handle<GenEventInfoProduct> handle;
        iEvent.getByToken(token[i], handle);
	if(handle.isValid()){
              GenWeight = handle->weight();
	}
    }
    return filter();
}

bool GenWeightDumper::filter(){
    if(!useFilter) return true;

    return true;
}

void GenWeightDumper::reset(){
    if(booked){
      GenWeight = 0;
    }
}
