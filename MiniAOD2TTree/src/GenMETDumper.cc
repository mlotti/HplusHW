#include "HiggsAnalysis/MiniAOD2TTree/interface/GenMETDumper.h"

GenMETDumper::GenMETDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    handle = new edm::Handle<edm::View<reco::GenMET>>[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
    }
}

GenMETDumper::~GenMETDumper(){}

void GenMETDumper::book(TTree* tree){
    booked = true;
    tree->Branch("GenMET_et",&GenMET);
    tree->Branch("GenMET_phi",&GenMET_phi);
}

bool GenMETDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t i = 0; i < inputCollections.size(); ++i){
	edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
	iEvent.getByLabel(inputtag, handle[i]);
	if(handle[i].isValid()){
              GenMET     = handle[i]->ptrAt(0)->et();
              GenMET_phi = handle[i]->ptrAt(0)->phi();
	} else {
	  std::cout << "Collection " << inputtag.label() << " not found, exiting.." << std::endl;
	  exit(8006);
	}
    }
    return filter();
}

bool GenMETDumper::filter(){
    if(!useFilter) return true;

    return true;
}

void GenMETDumper::reset(){
    if(booked){
      GenMET = 0;
      GenMET_phi = 0;
    }
}
