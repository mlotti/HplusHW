#include "HiggsAnalysis/MiniAOD2TTree/interface/TrackDumper.h"


TrackDumper::TrackDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets) {
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    
    pdgId = new std::vector<short>[inputCollections.size()];    

    token = new edm::EDGetTokenT<edm::View<pat::PackedCandidate>>[inputCollections.size()];

    for(size_t i = 0; i < inputCollections.size(); ++i){
      edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
      token[i] = iConsumesCollector.consumes<edm::View<pat::PackedCandidate>>(inputtag);
    }
    
    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
TrackDumper::~TrackDumper(){}

void TrackDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);
        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);
    }
}

bool TrackDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
        double ptCut = inputCollections[ic].getUntrackedParameter<double>("ptCut");
        double etaCut = inputCollections[ic].getUntrackedParameter<double>("etaCut");
        edm::Handle<edm::View<pat::PackedCandidate> > handle;
 
        iEvent.getByToken(token[ic], handle);
	if(handle.isValid()){
	    for(size_t i=0; i<handle->size(); ++i) {  
                const pat::PackedCandidate& cand = handle->at(i);
                // Place cuts
                if (cand.p4().pt() < ptCut) continue;
                if (std::fabs(cand.p4().eta()) > etaCut) continue;
                // Save candidates which have passed the cuts
                pt[ic].push_back(cand.p4().pt());
                eta[ic].push_back(cand.p4().eta());
                phi[ic].push_back(cand.p4().phi());
                e[ic].push_back(cand.p4().energy());
                pdgId[ic].push_back(cand.pdgId());
	    }
	}
    }
    return filter();
}

bool TrackDumper::filter(){
    if(!useFilter) return true;
    return true;
}

void TrackDumper::reset(){
    if(booked){
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){

	pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();
        pdgId[ic].clear();
      }
    }
}
