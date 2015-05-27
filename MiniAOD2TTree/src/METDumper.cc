#include "HiggsAnalysis/MiniAOD2TTree/interface/METDumper.h"

METDumper::METDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    MET     = new double[inputCollections.size()];
    MET_phi = new double[inputCollections.size()];                                
    //MET_p4 = new reco::Candidate::LorentzVector[inputCollections.size()];

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
        tree->Branch((name+"_et").c_str(),&MET[i]);
        tree->Branch((name+"_phi").c_str(),&MET_phi[i]);  
    }
//    tree->Branch("GenMET_p4",&GenMET_p4);
    tree->Branch("GenMET_et",&GenMET);
    tree->Branch("GenMET_phi",&GenMET_phi);
}

bool METDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t i = 0; i < inputCollections.size(); ++i){
	edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
	iEvent.getByLabel(inputtag, handle[i]);
	if(handle[i].isValid()){

	    MET[i]     = handle[i]->ptrAt(0)->p4().Pt();
	    MET_phi[i] = handle[i]->ptrAt(0)->p4().Phi();
	    if(handle[i]->ptrAt(0)->genMET()){
              GenMET     = handle[i]->ptrAt(0)->genMET()->pt();
              GenMET_phi = handle[i]->ptrAt(0)->genMET()->phi();
	    }
	    //MET_p4[i] = handle[i]->ptrAt(0)->p4();
	    //GenMET_p4 = handle[i]->ptrAt(0)->genMET()->p4();
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
	MET[i]        = 0;
	MET_phi[i]    = 0;
//	MET_p4[i].SetXYZT(0,0,0,0);
      }
      GenMET = 0;
      GenMET_phi = 0;
//    GenMET_p4.SetXYZT(0,0,0,0);
    }
}
