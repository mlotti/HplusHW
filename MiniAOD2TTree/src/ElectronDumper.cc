#include "HiggsAnalysis/MiniAOD2TTree/interface/ElectronDumper.h"

ElectronDumper::ElectronDumper(std::vector<edm::ParameterSet> psets) {
    inputCollections = psets;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    //p4   = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];                                                                                                          
    //pdgId = new std::vector<short>[inputCollections.size()];

    relIsoDeltaBetaCorrected = new std::vector<float>[inputCollections.size()];
    
    MCelectron = new FourVectorDumper[inputCollections.size()];
    
    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];
    handle = new edm::Handle<edm::View<pat::Electron> >[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
ElectronDumper::~ElectronDumper(){}

void ElectronDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
        std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
        if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();
    
        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

        tree->Branch((name+"_relIsoDeltaBeta").c_str(),&relIsoDeltaBetaCorrected[i]);

        MCelectron[i].book(tree, name, "MCelectron");
        
        std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
        for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
            tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*i]);
        }
    }
}

bool ElectronDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;  
  
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("prunedGenParticles", genParticles);
    
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
	std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
	iEvent.getByLabel(inputtag, handle[ic]);
        // Setup also handle for GsfElectrons (needed for ID)
        edm::Handle<edm::View<reco::GsfElectron>> gsfHandle;
        iEvent.getByLabel(inputtag, gsfHandle);
        // Setup handles for rho
        edm::InputTag rhoSource = inputCollections[ic].getParameter<edm::InputTag>("rhoSource");
        edm::Handle<double> rhoHandle;
        iEvent.getByLabel(rhoSource, rhoHandle);
        // Setup handles for ID
        std::string IDprefix = inputCollections[ic].getParameter<std::string>("IDprefix");
        std::vector<edm::Handle<edm::ValueMap<bool>>> IDhandles;
        for (auto p: discriminatorNames) {
          edm::InputTag discrTag(IDprefix, p);
          edm::Handle<edm::ValueMap<bool>> IDhandle;
          iEvent.getByLabel(discrTag, IDhandle);
          IDhandles.push_back(IDhandle);
        }
	if(handle[ic].isValid()){
          
	    for(size_t i=0; i<handle[ic]->size(); ++i) {
    		const pat::Electron& obj = handle[ic]->at(i);

		pt[ic].push_back(obj.p4().pt());
                eta[ic].push_back(obj.p4().eta());
                phi[ic].push_back(obj.p4().phi());
                e[ic].push_back(obj.p4().energy());

		//p4[ic].push_back(obj.p4());

                // Calculate relative isolation for the electron (delta beta)
                double isolation = obj.pfIsolationVariables().sumChargedHadronPt 
                  + std::max(obj.pfIsolationVariables().sumNeutralHadronEt 
                             + obj.pfIsolationVariables().sumPhotonEt
                             - 0.5 * obj.pfIsolationVariables().sumPUPt, 0.0);
                double relIso = isolation / obj.pt();
                relIsoDeltaBetaCorrected[ic].push_back(relIso);
                
                // Calculate relative isolation with effective area
                // FIXME: recipy for effective area is missing
                
		for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
                  discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*ic].push_back((*(IDhandles[iDiscr]))[gsfHandle->ptrAt(i)]);
		}

		// MC match info
                fillMCMatchInfo(ic, genParticles, obj);
            }
        }
    }
    return filter();
}

void ElectronDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Electron& ele) {
  double deltaRBestMatch = 9999.0;
  reco::Candidate::LorentzVector p4BestMatch(0,0,0,0);
  if(genParticles.isValid()){
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
      const reco::Candidate & gp = (*genParticles)[iMC];
      if (abs(gp.pdgId()) != 11) continue;
      reco::Candidate::LorentzVector p4 = gp.p4();
      double DR = deltaR(p4,ele.p4());
      if (DR < 0.1 && DR < deltaRBestMatch) {
        deltaRBestMatch = DR;
        p4BestMatch = p4;
      }
    }
  }
  MCelectron[ic].add(p4BestMatch.pt(), p4BestMatch.eta(), p4BestMatch.phi(), p4BestMatch.energy());
}

void ElectronDumper::reset(){                                                                                                                                           
  if(booked){                                                                                                                                                     
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){                                                                                                       
                                                                                                                                                                  
      pt[ic].clear();                                                                                                                                             
      eta[ic].clear();                                                                                                                                            
      phi[ic].clear();                                                                                                                                            
      e[ic].clear();                                                                                                                                              
                                                                                                                                                                  
      relIsoDeltaBetaCorrected[ic].clear();
      
      MCelectron[ic].reset();
    }                                                                                                                                                             
    for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){                                                                                       
      discriminators[ic].clear();                                                                                                                                 
    }                                                                                                                                                             
  }                                                                                                                                                               
}
