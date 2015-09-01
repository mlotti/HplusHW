#include "HiggsAnalysis/MiniAOD2TTree/interface/GenJetDumper.h"


GenJetDumper::GenJetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    pdgId = new std::vector<short>[inputCollections.size()];

    genJetToken = new edm::EDGetTokenT<reco::GenJetCollection>[inputCollections.size()];

    for(size_t i = 0; i < inputCollections.size(); ++i){
        edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
        genJetToken[i] = iConsumesCollector.consumes<reco::GenJetCollection>(inputtag);
    }
        
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
        
        edm::Handle<reco::GenJetCollection> handle;
        iEvent.getByToken(genJetToken[ic], handle);
        if(handle.isValid()){

            for(size_t i=0; i<handle->size(); ++i) {
                const reco::Candidate & gp = handle->at(i);
    
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
