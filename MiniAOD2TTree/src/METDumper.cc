#include "HiggsAnalysis/MiniAOD2TTree/interface/METDumper.h"

#include "TMath.h"

METDumper::METDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, bool isMC = true){
    inputCollections = psets;
    booked           = false;
    ismc             = isMC;

    MET_x = new double[inputCollections.size()];
    MET_y = new double[inputCollections.size()];                                

    token = new edm::EDGetTokenT<edm::View<pat::MET>>[inputCollections.size()];

    for(size_t i = 0; i < inputCollections.size(); ++i){
        edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
        token[i] = iConsumesCollector.consumes<edm::View<pat::MET>>(inputtag);
    }
    
    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        if(inputCollections[i].getUntrackedParameter<bool>("filter",false)) useFilter = true;
    }
}
METDumper::~METDumper(){}

void METDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();
	  //tree->Branch((name+"_p4").c_str(),&MET_p4[i]);
        tree->Branch((name+"_x").c_str(),&MET_x[i]);
        tree->Branch((name+"_y").c_str(),&MET_y[i]);  
    }
    tree->Branch("CaloMET_x",&caloMET_x);
    tree->Branch("CaloMET_y",&caloMET_y);
    if(ismc){
        tree->Branch("GenMET_x",&GenMET_x);
        tree->Branch("GenMET_y",&GenMET_y);
    }
}

bool METDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t i = 0; i < inputCollections.size(); ++i){
	
	edm::Handle<edm::View<pat::MET>> handle;
        iEvent.getByToken(token[i], handle);
	if(handle.isValid()){

	    MET_x[i] = handle->ptrAt(0)->p4().px();
	    MET_y[i] = handle->ptrAt(0)->p4().py();
	    if(handle->ptrAt(0)->genMET()){
              GenMET_x = handle->ptrAt(0)->genMET()->px();
              GenMET_y = handle->ptrAt(0)->genMET()->py();
	    }
	    if(handle->ptrAt(0)->caloMETPt()){
              caloMET_x = handle->ptrAt(0)->caloMETPt() * TMath::Cos(handle->ptrAt(0)->caloMETPhi());
              caloMET_y = handle->ptrAt(0)->caloMETPt() * TMath::Sin(handle->ptrAt(0)->caloMETPhi());
            }
	}else{
	  throw cms::Exception("config") << "Cannot find MET collection!";
	}
    }
    return filter();
}

bool METDumper::filter(){
    if(!useFilter) return true;

    return true;
}

void METDumper::reset(){
    if(booked){
      for(size_t i = 0; i < inputCollections.size(); ++i){
	MET_x[i] = 0;
	MET_y[i] = 0;
      }
      caloMET_x = 0;
      caloMET_y = 0;
      GenMET_x = 0;
      GenMET_y = 0;
    }
}
