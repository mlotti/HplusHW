#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleDumper.h"

GenParticleDumper::GenParticleDumper(std::vector<edm::ParameterSet> psets){
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    
    et  = new std::vector<short>[inputCollections.size()];

    pdgId = new std::vector<short>[inputCollections.size()];
    //status = new std::vector<short>[inputCollections.size()];

    mother = new std::vector<short>[inputCollections.size()];
    tauProng = new std::vector<short>[inputCollections.size()];

    massHpm = new std::vector<double>[inputCollections.size()];
    
    tauVisiblePt = new std::vector<double>[inputCollections.size()];
    tauVisiblePhi = new std::vector<double>[inputCollections.size()];
    tauVisibleEta = new std::vector<double>[inputCollections.size()];

    tauPi0RtauW = new std::vector<double>[inputCollections.size()];
    tauPi0RtauHpm = new std::vector<double>[inputCollections.size()];
    tauPi1pi0RtauW = new std::vector<double>[inputCollections.size()];
    tauPi1pi0RtauHpm = new std::vector<double>[inputCollections.size()];
    tauPinpi0RtauW = new std::vector<double>[inputCollections.size()];
    tauPinpi0RtauHpm = new std::vector<double>[inputCollections.size()];

    tauSpinEffectsW = new std::vector<double>[inputCollections.size()];
    tauSpinEffectsHpm = new std::vector<double>[inputCollections.size()];

    associatedWithHpm = new std::vector<short>[inputCollections.size()];

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
	tree->Branch((name+"_et").c_str(),&et[i]);

        tree->Branch((name+"_pdgId").c_str(),&pdgId[i]);
        //tree->Branch((name+"_status").c_str(),&status[i]);
	
	tree->Branch((name+"_mother").c_str(),&mother[i]);
	tree->Branch((name+"_tauProng").c_str(),&tauProng[i]);
	
	tree->Branch((name+"_massHpm").c_str(),&massHpm[i]);

	tree->Branch((name+"_tauVisiblePt").c_str(),&tauVisiblePt[i]);
	tree->Branch((name+"_tauVisiblePhi").c_str(),&tauVisiblePhi[i]);
	tree->Branch((name+"_tauVisibleEta").c_str(),&tauVisibleEta[i]);

	tree->Branch((name+"_tauPi0RtauW").c_str(),&tauPi0RtauW[i]);
	tree->Branch((name+"_tauPi0RtauHpm").c_str(),&tauPi0RtauHpm[i]);
	tree->Branch((name+"_tauPi1pi0RtauW").c_str(),&tauPi1pi0RtauW[i]);
	tree->Branch((name+"_tauPi1pi0RtauHpm").c_str(),&tauPi1pi0RtauHpm[i]);
	tree->Branch((name+"_tauPinpi0RtauW").c_str(),&tauPinpi0RtauW[i]);
	tree->Branch((name+"_tauPinpi0RtauHpm").c_str(),&tauPinpi0RtauHpm[i]);

	tree->Branch((name+"_tauSpinEffectsW").c_str(),&tauSpinEffectsW[i]);
	tree->Branch((name+"_tauSpinEffectsHpm").c_str(),&tauSpinEffectsHpm[i]);

	tree->Branch((name+"_associatedWithHpm").c_str(),&associatedWithHpm[i]);
    }
}

bool GenParticleDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
        edm::InputTag inputtag = inputCollections[ic].getParameter<edm::InputTag>("src");
        iEvent.getByLabel(inputtag, handle[ic]);
        if(handle[ic].isValid()){
	  // dummy values for particles not concerned (FIXME somehow?)
	    int mom = -1;
	    int tauPr = -1;
	    double tauVisPt = -100.0;
	    double tauVisPhi = -100.0;
	    double tauVisEta = -100.0;
            for(size_t i=0; i<handle[ic]->size(); ++i) {
                const reco::Candidate & gp = handle[ic]->at(i);
                pt[ic].push_back(gp.pt());
                eta[ic].push_back(gp.eta());
                phi[ic].push_back(gp.phi());
                e[ic].push_back(gp.energy());	
		et[ic].push_back(gp.et());	
		pdgId[ic].push_back(gp.pdgId());
		//status[ic].push_back(gp.status());
		
		if(abs(gp.pdgId()) == 37) {
		  massHpm[ic].push_back(gp.mass());
		}

		if(abs(gp.pdgId()) == 5 || abs(gp.pdgId()) == 6) {
		  size_t associated = associatedWithHpmProduction(&gp);
		  if(associated) {
		    associatedWithHpm[ic].push_back(1); // 1 (0) denotes being associated (not-associated)
		  } else if (abs(gp.pdgId()) == 5 && bFromAssociatedT(&gp)) {
		    // b-jets from associated t marked as secondary associated particles (denoted with 2)
	            associatedWithHpm[ic].push_back(2);
		  } else if (abs(gp.pdgId()) == 6 && abs(gp.mother()->pdgId()) == 21) {
		    // t-quarks that are produced with associated t in ttbar marked as secondary associated particles (denoted with 2)
		    bool t_ttbar = false;
		    for(reco::Candidate::const_iterator des = gp.mother()->begin(); des != gp.mother()->end(); ++des) {
		      if (&(*des) == &gp) {continue;}
		      if (abs(des->pdgId()) == 6 && topToHp(&(*des))) { 
		      //last condition: dirty hack to skip particles decaying to themselves in MadGraph, if this was not the case associatedWithHpmProduction(&(*des)) could be used
		          t_ttbar = true;
		      }
		    }
		    if (t_ttbar) {associatedWithHpm[ic].push_back(2);} 
		    else {associatedWithHpm[ic].push_back(0);} 
		  } else {
	            associatedWithHpm[ic].push_back(0);
	          }
                } else {
                  associatedWithHpm[ic].push_back(0);
	        }

		if(abs(gp.pdgId()) == 15) {
		    int decaychannel = tauDecayChannel(&gp);
		    double rTau = rtau(&gp);
		    tauPr = tauProngs(&gp);
		    if(abs(gp.mother()->pdgId()) == 37 && tauPr == 1) { 
		      //calculating visible quantities is expensive - do it only for H+ 1-prong taus
		      tauVisPt = visibleTauP4(&gp).Pt();
		      tauVisPhi = visibleTauP4(&gp).Phi();
		      tauVisEta = visibleTauP4(&gp).Eta();
		    }
		    
		    if(decaychannel == pi1pi0) { // polarization only for 1-prong hadronic taus with one neutral pion to make a clean case 
		      if(abs(gp.mother()->pdgId()) == 24) tauPi1pi0RtauW[ic].push_back(rTau);
		      if(abs(gp.mother()->pdgId()) == 37) tauPi1pi0RtauHpm[ic].push_back(rTau);
		    }
		    if(decaychannel == pinpi0) { 
		      if(abs(gp.mother()->pdgId()) == 24) tauPinpi0RtauW[ic].push_back(rTau);
		      if(abs(gp.mother()->pdgId()) == 37) tauPinpi0RtauHpm[ic].push_back(rTau);
		    }
		    if(decaychannel == pi) { // polarization only for 1-prong hadronic taus with no neutral pions
		      double efraction = spinEffects(&gp);
		      if(abs(gp.mother()->pdgId()) == 24) {
			tauPi0RtauW[ic].push_back(rTau);
			tauSpinEffectsW[ic].push_back(efraction);
		      }
		      if(abs(gp.mother()->pdgId()) == 37) {
			tauPi0RtauHpm[ic].push_back(rTau);
			tauSpinEffectsHpm[ic].push_back(efraction);
		      }
		    }
		}
		
		if(abs(gp.pdgId()) != 2212) mom = gp.mother()->pdgId(); // proton (2212) has no mother
		
		mother[ic].push_back(mom);
		tauProng[ic].push_back(tauPr);
		tauVisiblePt[ic].push_back(tauVisPt);
		tauVisiblePhi[ic].push_back(tauVisPhi);
		tauVisibleEta[ic].push_back(tauVisEta);
	    }
	}
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
	et[ic].clear();
	pdgId[ic].clear();
	//status[ic].clear();
	mother[ic].clear();
	tauProng[ic].clear();
	tauVisiblePt[ic].clear();
	tauVisiblePhi[ic].clear();
	tauVisibleEta[ic].clear();
	tauPi0RtauW[ic].clear();
	tauPi0RtauHpm[ic].clear();
	tauPi1pi0RtauW[ic].clear();
	tauPi1pi0RtauHpm[ic].clear();
	tauPinpi0RtauW[ic].clear();
	tauPinpi0RtauHpm[ic].clear();
	tauSpinEffectsW[ic].clear();
	tauSpinEffectsHpm[ic].clear();
	associatedWithHpm[ic].clear();
      }
    }
}

int GenParticleDumper::tauDecayChannel(const reco::Candidate* tau) {
    int channel = undetermined;

    int eCount   = 0,
	muCount  = 0,
	pi0Count = 0,
	piCount  = 0;

    for(reco::Candidate::const_iterator des = tau->begin(); des != tau->end(); ++des) {
	int pid = (*des).pdgId();

	if(abs(pid) == 15) return tauDecayChannel(&(*des));	
	if(abs(pid) == 11)  eCount++;
	if(abs(pid) == 13)  muCount++;
	if(abs(pid) == 111) pi0Count++;
	if(abs(pid) == 211) piCount++;
    }

    if(piCount == 1 && pi0Count == 0) channel = pi;
    if(piCount == 1 && pi0Count == 1)  channel = pi1pi0;
    if(piCount == 1 && pi0Count > 1)  channel = pinpi0;

    if(piCount == 3 && pi0Count == 0) channel = tripi;
    if(piCount == 3 && pi0Count > 0)  channel = tripinpi0;

    if(eCount == 1)                   channel = electron;
    if(muCount == 1)                  channel = muon;

    return channel;
}


int GenParticleDumper::tauProngs(const reco::Candidate* tau){ 
    int nProngs = 0;
    for(reco::Candidate::const_iterator des = tau->begin(); des != tau->end(); ++des) {
    	if(abs((*des).pdgId()) == 15) return tauProngs(&(*des)); 
    	if(abs((*des).pdgId()) == 213 || abs((*des).pdgId()) == 20213) {nProngs += tauProngs(&(*des));}
	else if((*des).status() != 1) {continue;} // unstable particle
	else {
	  if((*des).charge() == 0) continue; //neutral particle
	  nProngs++;
	}
    }
    return nProngs;
}

double GenParticleDumper::spinEffects(const reco::Candidate* tau){
    // polarization only for 1-prong hadronic taus with no neutral pions              
    TLorentzVector pionP4 = leadingPionP4(tau);
    TLorentzVector momP4 = motherP4(tau);
    pionP4.Boost(-1*momP4.BoostVector());
    double energy = pionP4.E()/(tau->mother()->p4().M()/2);
    return energy;
}

double GenParticleDumper::rtau(const reco::Candidate* tau){                
  // polarization only for 1-prong hadronic taus with one neutral pion to make a clean case 
  // if(tau->momentum().perp() < tauEtCut) return; // rtau visible only for boosted taus                               
  double rTau = 0;
  double ltrack = leadingPionP4(tau).P();
  double visibleTauE = visibleTauP4(tau).E();
  if(visibleTauE != 0) rTau = ltrack/visibleTauE;
  return rTau;
}

TLorentzVector GenParticleDumper::motherP4(const reco::Candidate* tau){
    TLorentzVector p4(tau->mother()->px(),
		      tau->mother()->py(),
		      tau->mother()->pz(),
		      tau->mother()->energy());
    return p4;
}

TLorentzVector GenParticleDumper::leadingPionP4(const reco::Candidate* tau){
    TLorentzVector p4(0,0,0,0);
    for(reco::Candidate::const_iterator des = tau->begin(); des != tau->end(); ++des) {
	if(abs((*des).pdgId()) == 15) return leadingPionP4(&(*des));
	if(abs((*des).pdgId()) != 211) continue;
	if((*des).momentum().rho() > p4.P()) {
	    p4 = TLorentzVector((*des).px(),
				(*des).py(),
				(*des).pz(),
				(*des).energy());
	}
    }
    return p4;
}

TLorentzVector GenParticleDumper::visibleTauP4(const reco::Candidate* tau){
  TLorentzVector p4(tau->px(),tau->py(),tau->pz(),tau->energy());
  for(reco::Candidate::const_iterator des = tau->begin(); des != tau->end(); ++des) {
      int pid = (*des).pdgId();
      if(abs(pid) == 15) return visibleTauP4(&(*des));
      if(abs(pid) == 12 || abs(pid) == 14 || abs(pid) == 16) {
          p4 -= TLorentzVector((*des).px(),
			     (*des).py(),
			     (*des).pz(),
			     (*des).energy());
      }
    }
  return p4;
}

bool GenParticleDumper::associatedWithHpmProduction(const reco::Candidate* particle) {
  for(reco::Candidate::const_iterator des = particle->begin(); des != particle->end(); ++des) {
    if (abs((*des).pdgId()) == 37) return true; // associated top (bottom) quarks decaying to Hpm in light case (5FS heavy case)
  }

  size_t nGenMothers = particle->numberOfMothers(); //associated bottom (top and bottom) quarks in light (heavy 4FS) case and associated top quarks in heavy 5FS case
  for (size_t iGenMother = 0; iGenMother < nGenMothers; ++iGenMother) { 
    const reco::Candidate* mom = particle->mother(iGenMother);
    for(reco::Candidate::const_iterator des = mom->begin(); des != mom->end(); ++des) {
      if (abs((*des).pdgId()) == 37) return true;
    }
  } 
  return false;
}

bool GenParticleDumper::topToHp(const reco::Candidate* particle) {
  int pid = particle->pdgId();
  const reco::Candidate* newp;
  bool notitself = true;
  bool haschildren = false;
  for(reco::Candidate::const_iterator des = particle->begin(); des != particle->end(); ++des) {
    if (des->pdgId() == pid) {
      notitself = false;
      newp = &(*des);
    }
    haschildren = true;
  }
  if (haschildren == false) {
    return false;
  }
  if (notitself == false) { // MadGraph produces particles decaying to themselves, skip them
    return topToHp(newp);
  }
  for(reco::Candidate::const_iterator des = particle->begin(); des != particle->end(); ++des) {
    if (abs(des->pdgId()) == 37) {
      return true;
    }
  }
  return false;
}


bool GenParticleDumper::bFromAssociatedT(const reco::Candidate* particle) {
  if (particle->mother()->pdgId() == particle->pdgId()) { // MadGraph produces particles decaying to themselves, skip them
    return bFromAssociatedT(particle->mother());
  } else if (abs(particle->mother()->pdgId()) == 6 && associatedWithHpmProduction(particle->mother())) {
    return true;
  } else {
    return false;
  }
}
  
void GenParticleDumper::printDescendants(const reco::Candidate* particle){
  for(reco::Candidate::const_iterator des = particle->begin(); des != particle->end(); ++des) {
      int pid = (*des).pdgId();
      std::cout << pid << " ";
  }
  std::cout << std::endl;
  return;
}
