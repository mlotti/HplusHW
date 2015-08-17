#include "HiggsAnalysis/MiniAOD2TTree/interface/TauDumper.h"
#include "HiggsAnalysis/NtupleAnalysis/src/DataFormat/interface/Tau.h"

TauDumper::TauDumper(std::vector<edm::ParameterSet> psets) {
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    

//    p4 = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];
    pdgId = new std::vector<short>[inputCollections.size()];
    pdgTauOrigin = new std::vector<short>[inputCollections.size()];
    
    lChTrackPt = new std::vector<double>[inputCollections.size()];
    lChTrackEta = new std::vector<double>[inputCollections.size()];
    
//    ltrack_p4 = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];

    nProngs = new std::vector<short>[inputCollections.size()];
    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];

    // Systematics
    for (auto p: inputCollections) {
      TESvariation.push_back(p.getParameter<double>("TESvariation"));
      TESvariationExtreme.push_back(p.getParameter<double>("TESvariationExtreme"));
    }
    systTESup = new FourVectorDumper[inputCollections.size()];
    systTESdown = new FourVectorDumper[inputCollections.size()];
    systExtremeTESup = new FourVectorDumper[inputCollections.size()];
    systExtremeTESdown = new FourVectorDumper[inputCollections.size()];
    
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
        tree->Branch((name+"_pdgOrigin").c_str(),&pdgTauOrigin[i]);

        tree->Branch((name+"_lChTrkPt").c_str(),&lChTrackPt[i]);
        tree->Branch((name+"_lChTrkEta").c_str(),&lChTrackEta[i]);
        tree->Branch((name+"_lNeutrTrkPt").c_str(),&lNeutrTrackPt[i]);
        tree->Branch((name+"_lNeutrTrkEta").c_str(),&lNeutrTrackEta[i]);
	//tree->Branch((name+"_lTrk_p4").c_str(),&ltrack_p4[i]);
        tree->Branch((name+"_nProngs").c_str(),&nProngs[i]);

	std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(src/DataFormat/src/Event.cc:62:); ++iDiscr) {
	    tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*i]);
	}
	
	systTESup[i].book(tree, name, "TESup");
        systTESdown[i].book(tree, name, "TESdown");
        systExtremeTESup[i].book(tree, name, "TESextremeUp");
        systExtremeTESdown[i].book(tree, name, "TESextremeDown");
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
		    lChTrackPt[ic].push_back(tau.leadChargedHadrCand()->p4().Pt());
                    lChTrackEta[ic].push_back(tau.leadChargedHadrCand()->p4().Eta());
                    lNeutrTrackPt[ic].push_back(tau.leadNeutralCand()->p4().Pt());
                    lNeutrTrackEta[ic].push_back(tau.leadNeutralCand()->p4().Eta());
		    nProngs[ic].push_back(tau.signalCands().size());  
		}
		for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
		    //std::cout << "check tau " << tau.p4().Pt() << " " << tau.p4().Eta() << " " << tau.p4().Phi() << " " << discriminatorNames[iDiscr] << " " << tau.tauID(discriminatorNames[iDiscr]) << std::endl;
		    discriminators[inputCollections.size()*iDiscr+(iDiscr+1)*ic].push_back(tau.tauID(discriminatorNames[iDiscr]));
		}
		// Systematics variations
		systTESup[ic].add(tau.p4().pt()*(1.0+TESvariation[ic]),
                                  tau.p4().eta(),
                                  tau.p4().phi(),
                                  tau.p4().energy()*(1.0+TESvariation[ic]));
                systTESdown[ic].add(tau.p4().pt()*(1.0-TESvariation[ic]),
                                  tau.p4().eta(),
                                  tau.p4().phi(),
                                  tau.p4().energy()*(1.0-TESvariation[ic]));
                systExtremeTESup[ic].add(tau.p4().pt()*(1.0+TESvariationExtreme[ic]),
                                         tau.p4().eta(),
                                         tau.p4().phi(),
                                         tau.p4().energy()*(1.0+TESvariationExtreme[ic]));
                systExtremeTESdown[ic].add(tau.p4().pt()*(1.0-TESvariationExtreme[ic]),
                                         tau.p4().eta(),
                                         tau.p4().phi(),
                                         tau.p4().energy()*(1.0-TESvariationExtreme[ic]));
		
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
                
                // Find MC particle matching to the tau. Logic is done in the following order:
                // - e is true if DeltaR(reco_tau, MC_e) < 0.1
                // - mu is true if DeltaR(reco_tau, MC_mu) < 0.1
                // - tau is true if DeltaR(reco_tau, MC_mu) < 0.1
                // - jet flavour should be taken from the flavour of the jet matching to the tau
                // The assignment is done in the following order:
                // - If e is true and tau is true   -> pdgId = +-1511
                // - If e is true and tau is false  -> pdgId = +-11
                // - If mu is true and tau is true  -> pdgId = +-1513
                // - If mu is true and tau is false -> pdgId = +-13
                // - If tau is true                 -> pdgId = +-15
                // - else                           -> pdgId = 0
		int tauPid = 0;
                int tauOrigin = 0;
                bool matchesToTau = false;
                bool matchesToE = false;
                bool matchesToMu = false;
		if(genParticles.isValid()){
                  for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
                    const reco::Candidate & gp = (*genParticles)[iMC];
                    //std::cout << " GENPartile ID " << gp.pdgId() << std::endl;
                    if( abs(gp.pdgId()) != 11 && abs(gp.pdgId()) != 13 && abs(gp.pdgId()) != 15) continue;
                    reco::Candidate::LorentzVector p4 = gp.p4();
                    if (abs(gp.pdgId()) == 11) {
                      if (deltaR(p4,tau.p4()) < 0.1)
                        matchesToE = true;
                    } else if (abs(gp.pdgId()) == 13) {
                      if (deltaR(p4,tau.p4()) < 0.1)
                        matchesToMu = true;
                    } else if (abs(gp.pdgId()) == 15) {
                      // Calculate visible tau pt
                      p4 = reco::Candidate::LorentzVector(0,0,0,0);
                      //std::cout << " TAU FOUND" << std::endl;
                      //std::cout << " Number of daughters " << gp.numberOfDaughters() << std::endl;
                      for (size_t iDaughter =  0; iDaughter < gp.numberOfDaughters(); ++iDaughter){
                        //std::cout << "     id " << gp.daughter(iDaughter)->pdgId() << std::endl;
                        int id = abs(gp.daughter(iDaughter)->pdgId());
                        if (id != 12 && id != 14 && id != 16){
                          p4 += gp.daughter(iDaughter)->p4();
                        }
                      }
                      if (deltaR(p4,tau.p4()) < 0.1) {
                        matchesToTau = true;
                        // Find out which particle produces the tau
                        const reco::Candidate* mother1 = (*genParticles)[gp.mother()];
                        if (mother1 != nullptr) {
                          if (abs(mother1->pdgId()) == 15) {
                            // Tau radiation (tau->tau+gamma), navigate to its mother
                            mother1 = (*genParticles)[mother1->mother()];
                          }
                        }
                        if (mother1 != nullptr) {
                          int moID = abs(mother1->pdgId());
                          if (moID == kFromW) {
                            tauOrigin == kFromW;
                          } else if (moID == kFromZ) {
                            tauOrigin == kFromZ;
                          } else if (moID == kFromHplus) {
                            tauOrigin == kFromHplus;
                          } else {
                            tauOrigin == kFromOtherSource;
                          }
                        }
                      }
                    }
                  }
		}
		if (matchesToE) {
                  if (matchesToTau)
                    tauPid = kTauDecaysToElectron;
                  else
                    tauPid = 11;
                } else if (matchesToMu) {
                  if (matchesToTau)
                    tauPid = kTauDecaysToMuon;
                  else
                    tauPid = 13;
                } else if (matchesToTau) {
                  tauPid = 15;
                } else {
                  // Look for reference jet
                  if (tau.PFJetRef().isNonnull()) {
                    tauPid = abs(tau.PFJetRef()->partonFlavour());
                  }
                }
		pdgId[ic].push_back(tauPid);
                pdgTauOrigin[ic].push_back(tauOrigin);
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
	lChTrackPt[ic].clear();
        lChTrackEta[ic].clear();  
        lNeutrTrackPt[ic].clear();
        lNeutrTrackEta[ic].clear();  
	//ltrack_p4[ic].clear();
	nProngs[ic].clear();
	pdgId[ic].clear();
        pdgTauOrigin[ic].clear();
        // Systematics
        systTESup[ic].reset();
        systTESdown[ic].reset();
        systExtremeTESup[ic].reset();
        systExtremeTESdown[ic].reset();
      }
      for(size_t ic = 0; ic < inputCollections.size()*nDiscriminators; ++ic){
	discriminators[ic].clear();
      }
    }
}
