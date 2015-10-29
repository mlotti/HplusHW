#include "HiggsAnalysis/MiniAOD2TTree/interface/TauDumper.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/NtupleAnalysis_fwd.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleTools.h"

#include "DataFormats/JetReco/interface/Jet.h"

TauDumper::TauDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets)
: genParticleToken(iConsumesCollector.consumes<reco::GenParticleCollection>(edm::InputTag("prunedGenParticles"))) {
    inputCollections = psets;
    booked           = false;

    pt  = new std::vector<double>[inputCollections.size()];
    eta = new std::vector<double>[inputCollections.size()];    
    phi = new std::vector<double>[inputCollections.size()];    
    e   = new std::vector<double>[inputCollections.size()];    
    pdgId = new std::vector<short>[inputCollections.size()];

    nDiscriminators = inputCollections[0].getParameter<std::vector<std::string> >("discriminators").size();
    discriminators = new std::vector<bool>[inputCollections.size()*nDiscriminators];

//    p4 = new std::vector<reco::Candidate::LorentzVector>[inputCollections.size()];
    lChTrackPt = new std::vector<double>[inputCollections.size()];
    lChTrackEta = new std::vector<double>[inputCollections.size()];
    lNeutrTrackPt = new std::vector<double>[inputCollections.size()];
    lNeutrTrackEta = new std::vector<double>[inputCollections.size()];

    decayMode = new std::vector<short>[inputCollections.size()];
    nProngs = new std::vector<short>[inputCollections.size()];
    pdgTauOrigin = new std::vector<short>[inputCollections.size()];
    MCNProngs = new std::vector<short>[inputCollections.size()];
    MCNPiZeros = new std::vector<short>[inputCollections.size()];
    MCtau = new FourVectorDumper[inputCollections.size()];
    matchingJet = new FourVectorDumper[inputCollections.size()];
    
    systTESup = new FourVectorDumper[inputCollections.size()];
    systTESdown = new FourVectorDumper[inputCollections.size()];
    systExtremeTESup = new FourVectorDumper[inputCollections.size()];
    systExtremeTESdown = new FourVectorDumper[inputCollections.size()];
    
    tauToken = new edm::EDGetTokenT<edm::View<pat::Tau> >[inputCollections.size()];
    jetToken = new edm::EDGetTokenT<edm::View<pat::Jet> >[inputCollections.size()];
    for(size_t i = 0; i < inputCollections.size(); ++i){
        edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
        tauToken[i] = iConsumesCollector.consumes<edm::View<pat::Tau>>(inputtag);
        edm::InputTag jettag = inputCollections[i].getParameter<edm::InputTag>("jetSrc");
        jetToken[i] = iConsumesCollector.consumes<edm::View<pat::Jet>>(jettag);
    }

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
        tree->Branch((name+"_mcNProngs").c_str(),&MCNProngs[i]);
        tree->Branch((name+"_mcNPizero").c_str(),&MCNPiZeros[i]);

        tree->Branch((name+"_lChTrkPt").c_str(),&lChTrackPt[i]);
        tree->Branch((name+"_lChTrkEta").c_str(),&lChTrackEta[i]);
        tree->Branch((name+"_lNeutrTrkPt").c_str(),&lNeutrTrackPt[i]);
        tree->Branch((name+"_lNeutrTrkEta").c_str(),&lNeutrTrackEta[i]);
	//tree->Branch((name+"_lTrk_p4").c_str(),&ltrack_p4[i]);
        tree->Branch((name+"_decayMode").c_str(),&decayMode[i]);
        tree->Branch((name+"_nProngs").c_str(),&nProngs[i]);
        MCtau[i].book(tree, name, "MCVisibleTau");
        matchingJet[i].book(tree, name, "matchingJet");

	std::vector<std::string> discriminatorNames = inputCollections[i].getParameter<std::vector<std::string> >("discriminators");
	for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
	    tree->Branch((name+"_"+discriminatorNames[iDiscr]).c_str(),&discriminators[inputCollections.size()*iDiscr+i]);
	}
	
	systTESup[i].book(tree, name, "TESup");
        systTESdown[i].book(tree, name, "TESdown");
        systExtremeTESup[i].book(tree, name, "TESextremeUp");
        systExtremeTESdown[i].book(tree, name, "TESextremeDown");
    }
}

bool TauDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;
  
  edm::Handle <reco::GenParticleCollection> genParticlesHandle;
  if (!iEvent.isRealData())
    iEvent.getByToken(genParticleToken, genParticlesHandle);

  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    edm::Handle<edm::View<pat::Tau>> tauHandle;
    iEvent.getByToken(tauToken[ic], tauHandle);
    edm::Handle<edm::View<pat::Jet>> jetHandle;
    iEvent.getByToken(jetToken[ic], jetHandle);
    if(tauHandle.isValid()){
      std::vector<std::string> discriminatorNames = inputCollections[ic].getParameter<std::vector<std::string> >("discriminators");
      double TESvariation = inputCollections[ic].getUntrackedParameter<double>("TESvariation");
      double TESvariationExtreme = inputCollections[ic].getUntrackedParameter<double>("TESvariationExtreme");
      
      for(size_t i=0; i<tauHandle->size(); ++i) {
        const pat::Tau& tau = tauHandle->at(i);

        pt[ic].push_back(tau.p4().pt());
        eta[ic].push_back(tau.p4().eta());
        phi[ic].push_back(tau.p4().phi());
        e[ic].push_back(tau.p4().energy());

        //p4[ic].push_back(tau.p4());
        
        // Leading charged particle
        if(tau.leadChargedHadrCand().isNonnull()){
          //ltrack_p4[ic].push_back(tau.leadChargedHadrCand()->p4());
          lChTrackPt[ic].push_back(tau.leadChargedHadrCand()->p4().Pt());
          lChTrackEta[ic].push_back(tau.leadChargedHadrCand()->p4().Eta());
        } else {
          lChTrackPt[ic].push_back(-1.0);
          lChTrackEta[ic].push_back(-10.0);
        }
        // Leading neutral particle
        if (tau.leadNeutralCand().isNonnull()) {
          lNeutrTrackPt[ic].push_back(tau.leadNeutralCand()->p4().Pt());
          lNeutrTrackEta[ic].push_back(tau.leadNeutralCand()->p4().Eta());
        } else {
          lNeutrTrackPt[ic].push_back(-1.0);
          lNeutrTrackEta[ic].push_back(-10.0);
        }
        decayMode[ic].push_back(tau.decayMode());
        nProngs[ic].push_back(tau.signalCands().size());  
        for(size_t iDiscr = 0; iDiscr < discriminatorNames.size(); ++iDiscr) {
          //std::cout << "check tau " << tau.p4().Pt() << " " << tau.p4().Eta() << " " << tau.p4().Phi() << " " << discriminatorNames[iDiscr] << " " << tau.tauID(discriminatorNames[iDiscr]) << std::endl;
          discriminators[inputCollections.size()*iDiscr+ic].push_back(tau.tauID(discriminatorNames[iDiscr]));
        }
        // Systematics variations
        systTESup[ic].add(tau.p4().pt()*(1.0+TESvariation),
                          tau.p4().eta(),
                          tau.p4().phi(),
                          tau.p4().energy()*(1.0+TESvariation));
        systTESdown[ic].add(tau.p4().pt()*(1.0-TESvariation),
                          tau.p4().eta(),
                          tau.p4().phi(),
                          tau.p4().energy()*(1.0-TESvariation));
        systExtremeTESup[ic].add(tau.p4().pt()*(1.0+TESvariationExtreme),
                                  tau.p4().eta(),
                                  tau.p4().phi(),
                                  tau.p4().energy()*(1.0+TESvariationExtreme));
        systExtremeTESdown[ic].add(tau.p4().pt()*(1.0-TESvariationExtreme),
                                  tau.p4().eta(),
                                  tau.p4().phi(),
                                  tau.p4().energy()*(1.0-TESvariationExtreme));
        
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

        // MC match info
        if (!iEvent.isRealData())
          fillMCMatchInfo(ic, genParticlesHandle, tau);
        // Find matching jet
        reco::Candidate::LorentzVector p4BestJet(0,0,0,0);
        double myMinDeltaR = 999.0;
        int jetPdgId = 0;
        for(size_t iJet = 0; iJet < jetHandle->size(); ++iJet) {
          const pat::Jet& jet = jetHandle->at(iJet);
          double DR = deltaR(tau.p4(), jet.p4());
          if (DR < 0.2 && DR < myMinDeltaR) {
            p4BestJet = jet.p4();
            myMinDeltaR = DR;
            jetPdgId = abs(jet.partonFlavour());
          }
        }
        matchingJet[ic].add(p4BestJet.pt(), p4BestJet.eta(), p4BestJet.phi(), p4BestJet.energy());
        // If tau does not match to e/mu/tau; then store as tau pdgId the partonFlavour of the matching jet
        if (!iEvent.isRealData()) {
          if (pdgId[ic][pdgId[ic].size()-1] == -1) {
            pdgId[ic][pdgId[ic].size()-1] = jetPdgId;
          }
        }
      } // tau loop
    } 
  } // input collections
  return filter();
}

void TauDumper::fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Tau& tau) {
  int tauPid = 0;
  int tauOrigin = 0;
  bool matchesToTau = false;
  bool matchesToE = false;
  bool matchesToMu = false;
  double deltaRBestTau = 9999.0;
  short simulatedNProngs = 0;
  short simulatedNPizeros = 0;
  reco::Candidate::LorentzVector p4BestTau(0,0,0,0);
  
  if(genParticles.isValid()){
    for (size_t iMC=0; iMC < genParticles->size(); ++iMC) {
      const reco::Candidate & gp = (*genParticles)[iMC];
      //std::cout << " GENPartile ID " << gp.pdgId() << std::endl;
      if( abs(gp.pdgId()) != 11 && abs(gp.pdgId()) != 13 && abs(gp.pdgId()) != 15) continue;
      reco::Candidate::LorentzVector p4 = gp.p4();
      if (abs(gp.pdgId()) == 11) {
        if (deltaR(p4,tau.p4()) < 0.1) {
          matchesToE = true;
          p4BestTau = p4;
          ++simulatedNProngs;
        }
      } else if (abs(gp.pdgId()) == 13) {
        if (deltaR(p4,tau.p4()) < 0.1) {
          matchesToMu = true;
          p4BestTau = p4;
          ++simulatedNProngs;
        }
      } else if (abs(gp.pdgId()) == 15) {
        std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(genParticles, &(genParticles->at(iMC)));
        // Calculate visible tau pt
        reco::Candidate::LorentzVector neutrinoMomentum(0., 0., 0., 0.);
        for (auto& po: offspring) {
          int absPid = std::abs(po->pdgId());
          if (absPid == 12 || absPid == 14 || absPid == 16) { // neutrino
            neutrinoMomentum += po->p4();
          }
        }
        p4 -= neutrinoMomentum;
        // Do matching
        double DR = deltaR(p4,tau.p4());
        if (DR < 0.1 && DR < deltaRBestTau) {
          // Matches to visible tau
          deltaRBestTau = DR;
          p4BestTau = p4;
          matchesToTau = true;
          // Calculate prongs and pizeros
          for (auto& po: offspring) {
            int absPid = std::abs(po->pdgId());
            if (absPid == 111)
              ++simulatedNPizeros;
            if (absPid == 211 || absPid == 321)
              ++simulatedNProngs;
          }
          // Find out which particle produces the tau
          std::vector<const reco::Candidate*> ancestry = GenParticleTools::findAncestry(genParticles, &(genParticles->at(iMC)));
          for (auto& pa: ancestry) {
            int absPid = std::abs(pa->pdgId());
            if (absPid == kFromZ || absPid == kFromW || absPid == kFromHplus) {
              tauOrigin = absPid;
            }
          }
          if (tauOrigin == 0 && ancestry.size() > 0) {
            tauOrigin = kFromOtherSource;
          }
        }
      }
    }
  }
  if (matchesToE) {
    if (matchesToTau)
      tauPid = kTauDecaysToElectron;
    else
      tauPid = kElectronToTau;
  } else if (matchesToMu) {
    if (matchesToTau)
      tauPid = kTauDecaysToMuon;
    else
      tauPid = kMuonToTau;
  } else if (matchesToTau) {
    tauPid = kTauDecaysToHadrons;
  } else {
    // Reference jet is a reco::PFJet and therefore not included into miniAOD
    // Need to do actual matching in ntuple reader
    tauPid = -1;
  }
  pdgId[ic].push_back(tauPid);
  pdgTauOrigin[ic].push_back(tauOrigin);
  MCNProngs[ic].push_back(simulatedNProngs);
  MCNPiZeros[ic].push_back(simulatedNPizeros);
  MCtau[ic].add(p4BestTau.pt(), p4BestTau.eta(), p4BestTau.phi(), p4BestTau.energy());
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
	decayMode[ic].clear();
        nProngs[ic].clear();
	pdgId[ic].clear();
        pdgTauOrigin[ic].clear();
        MCNProngs[ic].clear();
        MCNPiZeros[ic].clear();
        MCtau[ic].reset();
        matchingJet[ic].reset();
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
