#include "HiggsAnalysis/MiniAOD2TTree/interface/MuonDumper.h"

MuonDumper::MuonDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    //p4  = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];
    pdgId = new std::vector<short>[inputCollections.size()];
    isGlobalMuon = new std::vector<bool>[inputCollections.size()];

    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];
    handle = new edm::Handle<edm::View<pat::Muon> >[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
MuonDumper::~MuonDumper(){}

void MuonDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
        if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();
    
        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

        tree->Branch((name+"_isGlobalMuon").c_str(),&isGlobalMuon[i]);
                
        std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
        for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
            tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*i]);
        }
    }
}

bool MuonDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
	std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
	iEvent.getByLabel(inputtag, handle[ic]);
	if(handle[ic].isValid()){

	    for(size_t i=0; i<handle[ic]->size(); ++i) {
    		const pat::Muon& obj = handle[ic]->at(i);

		pt[ic].push_back(obj.p4().pt());
                eta[ic].push_back(obj.p4().eta());
                phi[ic].push_back(obj.p4().phi());
                e[ic].push_back(obj.p4().energy());

		isGlobalMuon[ic].push_back(obj.isGlobalMuon());

		//p4[ic].push_back(obj.p4());
		for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
		    discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*ic].push_back(obj.muonID(discriminatorNames[iDiscr]));
		}
            }
        }
    }
    return filter();
}

void MuonDumper::reset(){                                                                                                                                           
    if(booked){                                                                                                                                                     
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){                                                                                                       
                                                                                                                                                                    
        pt[ic].clear();                                                                                                                                             
        eta[ic].clear();                                                                                                                                            
        phi[ic].clear();                                                                                                                                            
        e[ic].clear();                                                                                                                                              
                                                                                                                                                                    
        isGlobalMuon[ic].clear();
      }                                                                                                                                                             
      for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){                                                                                       
        discriminators[ic].clear();                                                                                                                                 
      }                                                                                                                                                             
    }                                                                                                                                                               
}
