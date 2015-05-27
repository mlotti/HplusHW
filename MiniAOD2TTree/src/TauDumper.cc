#include "HiggsAnalysis/MiniAOD2TTree/interface/TauDumper.h"

TauDumper::TauDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

//    p4 = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];
    pdgId = new std::vector<short>[inputCollections.size()];

    ltrackPt = new std::vector<double>[inputCollections.size()];
    ltrackEta = new std::vector<double>[inputCollections.size()];
//    ltrack_p4 = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];

    nProngs = new std::vector<int>[inputCollections.size()];
    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];

    handle = new edm::Handle<edm::View<pat::Tau> >[inputCollections.size()];

    useFilter = false;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
        if(param) useFilter = true;
    }
}
TauDumper::~TauDumper(){}

void TauDumper::book(TTree* tree){
    booked = true;
    for(size_t i = 0; i < inputCollections.size(); ++i){
	std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
	if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

        tree->Branch((name+"_pt").c_str(),&pt[i]);
        tree->Branch((name+"_eta").c_str(),&eta[i]);
        tree->Branch((name+"_phi").c_str(),&phi[i]);
        tree->Branch((name+"_e").c_str(),&e[i]);

	//tree->Branch((name+"_p4").c_str(),&p4[i]);
        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);

        tree->Branch((name+"_lTrkPt").c_str(),&ltrackPt[i]);
        tree->Branch((name+"_lTrkEta").c_str(),&ltrackEta[i]);
	//tree->Branch((name+"_lTrk_p4").c_str(),&ltrack_p4[i]);
        tree->Branch((name+"_nProngs").c_str(),&nProngs[i]);

	std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	    tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*i]);
	}
    }
}

bool TauDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("prunedGenParticles", genParticles);
    /*
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) { 
      const reco::Candidate & gp = (*genParticles)[iMC];
      std::cout << " GENPartile ID " << gp.pdgId() << std::endl;
      //      if( abs(gp.pdgId()) == 15){
      //	std::cout << " TAU FOUND" << std::endl;
      //      }
    }
    */
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
	std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
	iEvent.getByLabel(inputtag, handle[ic]);
	if(handle[ic].isValid()){

	    for(size_t i=0; i<handle[ic]->size(); ++i) {
    		const pat::Tau& tau = handle[ic]->at(i);

		pt[ic].push_back(tau.p4().pt());
                eta[ic].push_back(tau.p4().eta());
                phi[ic].push_back(tau.p4().phi());
                e[ic].push_back(tau.p4().energy());

		//p4[ic].push_back(tau.p4());
		
		if(tau.leadChargedHadrCand().isNonnull()){
		    //ltrack_p4[ic].push_back(tau.leadChargedHadrCand()->p4());
		    ltrackPt[ic].push_back(tau.leadChargedHadrCand()->p4().Pt());
                    ltrackEta[ic].push_back(tau.leadChargedHadrCand()->p4().Eta());
		    nProngs[ic].push_back(tau.signalCands().size());  
		}
		for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
		    //std::cout << "check tau " << tau.p4().Pt() << " " << tau.p4().Eta() << " " << tau.p4().Phi() << " " << discriminatorNames[iDiscr] << " " << tau.tauID(discriminatorNames[iDiscr]) << std::endl;
		    discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*ic].push_back(tau.tauID(discriminatorNames[iDiscr]));
		}
		/*
		std::cout << "check tau " << tau.pdgId() << std::endl;
		std::vector<reco::GenParticleRef> associatedGenParticles = tau.genParticleRefs();
		for ( std::vector<reco::GenParticleRef>::const_iterator it = associatedGenParticles.begin();
		      it != associatedGenParticles.end(); ++it ) {
		  if ( it->isAvailable() ) {
		    const reco::GenParticleRef& genParticle = (*it);
		    std::cout << "    GenParticleRef " << genParticle->pdgId() << std::endl;
		  }
		}
		*/
		int tauPid = 1;
		if(genParticles.isValid()){
		for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
		  const reco::Candidate & gp = (*genParticles)[iMC];
		  //std::cout << " GENPartile ID " << gp.pdgId() << std::endl;
		  if( abs(gp.pdgId()) != 11 && abs(gp.pdgId()) != 13 && abs(gp.pdgId()) != 15) continue;
		  reco::Candidate::LorentzVector p4 = gp.p4();
		  if( abs(gp.pdgId()) == 15){
		    p4 = reco::Candidate::LorentzVector(0,0,0,0);
		    //std::cout << " TAU FOUND" << std::endl;
		    //std::cout << " Number of daughters " << gp.numberOfDaughters() << std::endl;
		      for (size_t iDaughter =  0; iDaughter < gp.numberOfDaughters(); ++iDaughter){
			//std::cout << "     id " << gp.daughter(iDaughter)->pdgId() << std::endl;
			int id = gp.daughter(iDaughter)->pdgId(); 
			if (abs(id) != 12 && abs(id) != 14 && abs(id) != 16){
			  p4 += gp.daughter(iDaughter)->p4();
			}
		      }
		  
		  }
		  //std::cout << " deltaR " << deltaR(p4,tau.p4()) << std::endl;
		  if( deltaR(p4,tau.p4()) < 0.2){
		    tauPid = gp.pdgId();
		    //std::cout << " Matching " << gp.pdgId() << std::endl;
		  }
		}
		}
		pdgId[ic].push_back(tauPid);
            }
        }
    }
    return filter();
}

bool TauDumper::filter(){
    if(!useFilter) return true;

    int n = 0;
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
      //	for(std::vector<math::XYZTLorentzVector>::const_iterator i = p4[ic].begin(); i!= p4[ic].end(); ++i){
      //	    if(i->Pt() > 20) n++;
      //	}
      for(std::vector<double>::const_iterator i = pt[ic].begin(); i!= pt[ic].end(); ++i){
	if(*i > 20) n++;
      }
      /*
      for(std::vector<reco::Candidate::LorentzVector>::const_iterator i = p4[ic].begin(); i!= p4[ic].end(); ++i){
        if(i->pt() > 20) n++;
      }
      */
    }
    return n > 0;
}

void TauDumper::reset(){
    if(booked){
      for(size_t ic = 0; ic < inputCollections.size(); ++ic){

	pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();

	//p4[ic].clear();
	ltrackPt[ic].clear();
        ltrackEta[ic].clear();  
	//ltrack_p4[ic].clear();
	nProngs[ic].clear();
	pdgId[ic].clear();
      }
      for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
	discriminators[ic].clear();
      }
    }
}
