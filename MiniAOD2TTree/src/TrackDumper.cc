#include "HiggsAnalysis/MiniAOD2TTree/interface/TrackDumper.h"
#include <../external/boost_1_57_0/boost/concept_check.hpp>


TrackDumper::TrackDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets) {
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    
    pdgId = new std::vector<short>[inputCollections.size()];    

    fIPTwrtPV  = new std::vector<float>[inputCollections.size()];
    fIPzwrtPV  = new std::vector<float>[inputCollections.size()];
    fIPTSignif = new std::vector<float>[inputCollections.size()];
    fIPzSignif  = new std::vector<float>[inputCollections.size()];
    
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
        
        tree->Branch((name+"_IPTwrtPV").c_str(),&fIPTwrtPV[i]);
        tree->Branch((name+"_IPzwrtPV").c_str(),&fIPzwrtPV[i]);
        tree->Branch((name+"_IPTSignificance").c_str(),&fIPTSignif[i]);
        tree->Branch((name+"_IPzSignificance").c_str(),&fIPzSignif[i]);
    }
}

bool TrackDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
        double ptCut = inputCollections[ic].getUntrackedParameter<double>("ptCut");
        double etaCut = inputCollections[ic].getUntrackedParameter<double>("etaCut");
        bool saveOnlyChargedParticles = inputCollections[ic].getUntrackedParameter<bool>("saveOnlyChargedParticles");
        double IPvsPVzCut = inputCollections[ic].getUntrackedParameter<double>("IPvsPVz");
        edm::Handle<edm::View<pat::PackedCandidate> > handle;
        iEvent.getByToken(token[ic], handle);
        
	if(handle.isValid()){
	    for(size_t i=0; i<handle->size(); ++i) {  
                const pat::PackedCandidate& cand = handle->at(i);
                // Place cuts
                if (cand.p4().pt() < ptCut) continue;
                if (std::fabs(cand.p4().eta()) > etaCut) continue;
                int absPid = abs(cand.pdgId());
                // Select only charged particles to save disc space
                if (saveOnlyChargedParticles) {
                  if (!(absPid == 11 || absPid == 13 || absPid == 211)) continue;
                }
                // Save only those particles, which are within 5 mm
                if (cand.dz() > IPvsPVzCut) continue;
                // Calculate IP significances
                float IPTSignif = 0.0;
                if (cand.dxyError() > 0.0)
                  IPTSignif = cand.dxy() / cand.dxyError();
                float IPzSignif = 0.0;
                if (cand.dzError() > 0.0)
                  IPzSignif = cand.dz() / cand.dzError();
                // Save candidates which have passed the cuts
                pt[ic].push_back(cand.p4().pt());
                eta[ic].push_back(cand.p4().eta());
                phi[ic].push_back(cand.p4().phi());
                e[ic].push_back(cand.p4().energy());
                pdgId[ic].push_back(cand.pdgId());
                
                fIPTwrtPV[ic].push_back(cand.dxy());
                fIPzwrtPV[ic].push_back(cand.dz());
                fIPTSignif[ic].push_back(cand.dxyError());
                fIPzSignif[ic].push_back(cand.dzError());
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
        
        fIPTwrtPV[ic].clear();
        fIPzwrtPV[ic].clear();
        fIPTSignif[ic].clear();
        fIPzSignif[ic].clear();
      }
    }
}
