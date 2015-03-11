#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

BaseDumper::BaseDumper(){}

BaseDumper::BaseDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;
}
BaseDumper::~BaseDumper(){}

void BaseDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();
//        tree->Branch((name+"_p4").c_str(),&p4[i]);  

        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

//        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);

	std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	    tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*i]);
	}
    }
}

bool BaseDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if(booked) return filter();
    return true;
}

bool BaseDumper::filter(){
    return true;
}

void BaseDumper::reset(){
    if(booked){
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){

	pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();

//	p4[ic].clear();
//	pdgId[ic].clear();
      }
      for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
	discriminators[ic].clear();
      }
    }
}
