#include "HiggsAnalysis/MiniAOD2TTree/interface/GenMETDumper.h"

#include "DataFormats/METReco/interface/GenMET.h"

GenMETDumper::GenMETDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
    inputCollections = psets;
    booked           = false;

    token = new edm::EDGetTokenT<edm::View<reco::GenMET>>[inputCollections.size()];

    for(size_t i = 0; i < inputCollections.size(); ++i){
      edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
      token[i] = iConsumesCollector.consumes<edm::View<reco::GenMET>>(inputtag);
    }
    
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
	edm::Handle<edm::View<reco::GenMET>> handle;
        iEvent.getByToken(token[i], handle);
	if(handle.isValid()){
              GenMET     = handle->ptrAt(0)->et();
              GenMET_phi = handle->ptrAt(0)->phi();
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
