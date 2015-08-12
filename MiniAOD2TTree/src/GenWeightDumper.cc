#include "HiggsAnalysis/MiniAOD2TTree/interface/GenWeightDumper.h"

GenWeightDumper::GenWeightDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    handle = new edm::Handle<GenEventInfoProduct>[inputCollections.size()];

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
	edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
	iEvent.getByLabel(inputtag, handle[i]);
	if(handle[i].isValid()){
              GenWeight = handle[i]->weight();
	} else {
	  std::cout << "Collection " << inputtag.label() << " not found, exiting.." << std::endl;
	  exit(8006);
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
