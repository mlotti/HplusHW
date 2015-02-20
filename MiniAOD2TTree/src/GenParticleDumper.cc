#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleDumper.h"

GenParticleDumper::GenParticleDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    pdgId = new std::vector<short>[inputCollections.size()];
    status = new std::vector<short>[inputCollections.size()];

    handle = new edm::Handle<reco::GenParticleCollection>[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
GenParticleDumper::~GenParticleDumper(){}

void GenParticleDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);
        tree->Branch((name+"_status").c_str(),&status[i]);
    }
}

bool GenParticleDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
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
		pdgId[ic].push_back(gp.pdgId());
		status[ic].push_back(gp.status());
	    }
	}
/*
    edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("prunedGenParticles", genParticles);

        for (size_t iMC=0; iMC < genParticles->size(); ++iMC) { 
      const reco::Candidate & gp = (*genParticles)[iMC];
      std::cout << " GENPartile ID " << gp.pdgId() << std::endl;
      //      if( abs(gp.pdgId()) == 15){
      //	std::cout << " TAU FOUND" << std::endl;
      //      }
      pt[iMC].push_back(gp.pt());
      eta[iMC].push_back(gp.eta());
      phi[iMC].push_back(gp.phi()); 
      e[iMC].push_back(gp.energy());
      pdgId[iMC].push_back(gp.pdgId());
*/
    }
    return filter();
}

bool GenParticleDumper::filter(){
    if(!useFilter) return true;
    return true;
}

void GenParticleDumper::reset(){
    if(booked){
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){

	pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();
	pdgId[ic].clear();
	status[ic].clear();
      }
    }
}
