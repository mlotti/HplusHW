#include "HiggsAnalysis/MiniAOD2TTree/interface/METDumper.h"

METDumper::METDumper(std::vector<edm::ParameterSet> psets, bool isMC = true){
    inputCollections = psets;
    booked           = false;
    ismc             = isMC;

    MET     = new double[inputCollections.size()];
    MET_phi = new double[inputCollections.size()];                                

    handle = new edm::Handle<edm::View<pat::MET> >[inputCollections.size()];

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
	edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
	iEvent.getByLabel(inputtag, handle[i]);
	if(handle[i].isValid()){

	    MET_x[i] = handle[i]->ptrAt(0)->p4().px();
	    MET_y[i] = handle[i]->ptrAt(0)->p4().py();
	    if(handle[i]->ptrAt(0)->genMET()){
              GenMET_x = handle[i]->ptrAt(0)->genMET()->px();
              GenMET_y = handle[i]->ptrAt(0)->genMET()->py();
	    }
	    if(handle[i]->ptrAt(0)->caloMETPt()){
              caloMET_x = handle[i]->ptrAt(0)->caloMETPx();
              caloMET_y = handle[i]->ptrAt(0)->caloMETPy();
            }
	}else{
	  std::cout << "Collection " << inputtag.label() << " not found, exiting.." << std::endl;
	  exit(8006);
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
