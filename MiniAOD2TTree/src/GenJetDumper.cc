#include "HiggsAnalysis/MiniAOD2TTree/interface/GenJetDumper.h"

GenJetDumper::GenJetDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    pdgId = new std::vector<short>[inputCollections.size()];

    handle = new edm::Handle<reco::GenJetCollection>[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
GenJetDumper::~GenJetDumper(){}

void GenJetDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

//        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);
    }
}

bool GenJetDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
        edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
        iEvent.getByLabel(inputtag, handle[ic]);
        if(handle[ic].isValid()){

            for(size_t i=0; i<handle[ic]->size(); ++i) {
                const reco::Candidate & gp = handle[ic]->at(i);
    
                pt[ic].push_back(gp.pt());
                eta[ic].push_back(gp.eta());
                phi[ic].push_back(gp.phi());
                e[ic].push_back(gp.energy());	
//		pdgId[ic].push_back(gp.pdgId());
	    }
	}
    }
    return filter();
}

bool GenJetDumper::filter(){
    if(!useFilter) return true;
    return true;
}

void GenJetDumper::reset(){
    if(booked){
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();
//	pdgId[ic].clear();
      }
    }
}
