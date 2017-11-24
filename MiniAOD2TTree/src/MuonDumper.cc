#include "HiggsAnalysis/MiniAOD2TTree/interface/MuonDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/MiniIsolation.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

MuonDumper::MuonDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, const edm::InputTag& recoVertexTag)
: genParticleToken(iConsumesCollector.consumes<reco::GenParticleCollection>(edm::InputTag("prunedGenParticles"))),
  vertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(recoVertexTag)) {
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

    q   = new std::vector<short>[inputCollections.size()];

    //p4  = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];
    //pdgId = new std::vector<short>[inputCollections.size()];
    isGlobalMuon = new std::vector<bool>[inputCollections.size()];
    isLooseMuon = new std::vector<bool>[inputCollections.size()];
    isMediumMuon = new std::vector<bool>[inputCollections.size()];
    isTightMuon = new std::vector<bool>[inputCollections.size()];
    relIsoDeltaBetaCorrected03 = new std::vector<float>[inputCollections.size()];
    relIsoDeltaBetaCorrected04 = new std::vector<float>[inputCollections.size()];

    MCmuon = new FourVectorDumper[inputCollections.size()];
    
    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];
    
    muonToken = new edm::EDGetTokenT<edm::View<pat::Muon>>[inputCollections.size()];
    // Marina - start
    rhoToken = new edm::EDGetTokenT<double>[inputCollections.size()];
    pfcandsToken      = new edm::EDGetTokenT<edm::View<pat::PackedCandidate> >[inputCollections.size()];
    relMiniIso        = new std::vector<float>[inputCollections.size()];
    effAreaMiniIso    = new std::vector<float>[inputCollections.size()];
    // Marina - end
    
    for(size_t i = 0; i < inputCollections.size(); ++i){
      edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
      muonToken[i] = iConsumesCollector.consumes<edm::View<pat::Muon>>(inputtag);
    
      // Marina - Start                                                  
      edm::InputTag rhoSource = inputCollections[i].getParameter<edm::InputTag>("rhoSource");
      rhoToken[i] = iConsumesCollector.consumes<double>(rhoSource);
      
      edm::InputTag pfcandinputtag = inputCollections[i].getParameter<edm::InputTag>("pfcands");
      pfcandsToken[i] = iConsumesCollector.consumes<edm::View<pat::PackedCandidate>>(pfcandinputtag);
      // Marina - end
    }
    
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

        tree->Branch((name+"_charge").c_str(),&q[i]);

        tree->Branch((name+"_isGlobalMuon").c_str(),&isGlobalMuon[i]);
        tree->Branch((name+"_muIDLoose").c_str(),&isLooseMuon[i]);
        tree->Branch((name+"_muIDMedium").c_str(),&isMediumMuon[i]);
        tree->Branch((name+"_muIDTight").c_str(),&isTightMuon[i]);
        tree->Branch((name+"_relIsoDeltaBeta03").c_str(),&relIsoDeltaBetaCorrected03[i]); // cone 0.3
        tree->Branch((name+"_relIsoDeltaBeta04").c_str(),&relIsoDeltaBetaCorrected04[i]); // cone 0.4
	
	// Marina - start
        tree->Branch((name+"_relMiniIso").c_str(), &relMiniIso[i]);
        tree->Branch((name+"_effAreaMiniIso").c_str(), &effAreaMiniIso[i]);
        // Marina - end
	
        MCmuon[i].book(tree, name, "MCmuon");
        
        std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
        for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
            tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+i]);
        }
    }
}

bool MuonDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;
    
    // Get genParticles
    edm::Handle <reco::GenParticleCollection> genParticlesHandle;
    if (!iEvent.isRealData())
      iEvent.getByToken(genParticleToken, genParticlesHandle);
    // Get vertex
    edm::Handle<edm::View<reco::Vertex> > vertexHandle;
    iEvent.getByToken(vertexToken, vertexHandle);
    
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
	std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
	edm::Handle<edm::View<pat::Muon>> muonHandle;
        iEvent.getByToken(muonToken[ic], muonHandle);

	// Marina - start
	edm::Handle<edm::View<pat::PackedCandidate> > pfcandHandle;
        iEvent.getByToken(pfcandsToken[ic], pfcandHandle);
	// Marina - end
	
	if(muonHandle.isValid()){
	  
	    // Marina - start
	    // Setup handles for rho
	    edm::Handle<double> rhoHandle;
	    iEvent.getByToken(rhoToken[ic], rhoHandle);
	    // Marina - end
	  
            for(size_t i=0; i<muonHandle->size(); ++i) {
    		const pat::Muon& obj = muonHandle->at(i);

		pt[ic].push_back(obj.p4().pt());
                eta[ic].push_back(obj.p4().eta());
                phi[ic].push_back(obj.p4().phi());
                e[ic].push_back(obj.p4().energy());

                q[ic].push_back(obj.charge());
                
		isGlobalMuon[ic].push_back(obj.isGlobalMuon());

                // For the discriminators see: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2

                isLooseMuon[ic].push_back(obj.isLooseMuon());
                isMediumMuon[ic].push_back(obj.isMediumMuon());
                if (vertexHandle->size() == 0) {
                  isTightMuon[ic].push_back(false);
                } else {
                  isTightMuon[ic].push_back(obj.isTightMuon(vertexHandle->at(0)));
                }
                // Calculate relative isolation in cone of DeltaR=0.3
                double isolation03 = (obj.pfIsolationR03().sumChargedHadronPt
                  + std::max(obj.pfIsolationR03().sumNeutralHadronEt
                        + obj.pfIsolationR03().sumPhotonEt
                        - 0.5 * obj.pfIsolationR03().sumPUPt, 0.0));
                double relIso03 = isolation03 / obj.pt();
                relIsoDeltaBetaCorrected03[ic].push_back(relIso03);

                // Calculate relative isolation in cone of DeltaR=0.3
                double isolation04 = (obj.pfIsolationR04().sumChargedHadronPt
		  + std::max(obj.pfIsolationR04().sumNeutralHadronEt
		  + obj.pfIsolationR04().sumPhotonEt
		  - 0.5 * obj.pfIsolationR04().sumPUPt, 0.0));
                double relIso04 = isolation04 / obj.pt();
                relIsoDeltaBetaCorrected04[ic].push_back(relIso04);


		// Marina - start
                double relIsoMini = getMiniIsolation_DeltaBeta(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false);
		double relIsoMiniEffArea = getMiniIsolation_EffectiveArea(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false, false, *rhoHandle);
		
		//std::cout<<"Relative Isolation (Delta Bet) = "<<relIsoMini<<std::endl;
		//std::cout<<"Relative Isolation (Effective Area) = "<<relIsoMiniEffArea<<std::endl;
		  
		relMiniIso[ic].push_back(getMiniIsolation_DeltaBeta(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false));
		effAreaMiniIso[ic].push_back(getMiniIsolation_EffectiveArea(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false, false, *rhoHandle));
		// Marina - end
		
		//p4[ic].push_back(obj.p4());
		for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
		    discriminators[inputCollections.size()*iDiscr+ic].push_back(obj.muonID(discriminatorNames[iDiscr]));
		}
		
                // MC match info
                if (!iEvent.isRealData())
                  fillMCMatchInfo(ic, genParticlesHandle, obj);
            }
        }
    }
    return filter();
}

void MuonDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Muon& ele) {
  double deltaRBestMatch = 9999.0;
  reco::Candidate::LorentzVector p4BestMatch(0,0,0,0);
  if(genParticles.isValid()){
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
      const reco::Candidate & gp = (*genParticles)[iMC];
      if (abs(gp.pdgId()) != 13) continue;
      reco::Candidate::LorentzVector p4 = gp.p4();
      double DR = deltaR(p4,ele.p4());
      if (DR < 0.1 && DR < deltaRBestMatch) {
        deltaRBestMatch = DR;
        p4BestMatch = p4;
      }
    }
  }
  MCmuon[ic].add(p4BestMatch.pt(), p4BestMatch.eta(), p4BestMatch.phi(), p4BestMatch.energy());
}


void MuonDumper::reset(){
    if(booked){         
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){
                        
        pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();  

        q[ic].clear();

        isGlobalMuon[ic].clear();
        isLooseMuon[ic].clear();
        isMediumMuon[ic].clear();
        isTightMuon[ic].clear();
        relIsoDeltaBetaCorrected03[ic].clear();
	relIsoDeltaBetaCorrected04[ic].clear();
	
	// Marina - start
	relMiniIso[ic].clear();
	effAreaMiniIso[ic].clear();
	// Marina - end 
	
        MCmuon[ic].reset();
      }
      for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
        discriminators[ic].clear();
      }
    }  
}
