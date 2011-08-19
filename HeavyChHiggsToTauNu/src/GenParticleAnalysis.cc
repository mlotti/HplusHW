#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"

#include "TH1F.h"
#include "TLorentzVector.h"
#include "TVector3.h"

namespace HPlus {

  GenParticleAnalysis::GenParticleAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight)
    : fEventWeight(eventWeight)
      //    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
      //    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut"))
  {
    init();
  }
  GenParticleAnalysis::GenParticleAnalysis(EventCounter& eventCounter, EventWeight& eventWeight)
    : fEventWeight(eventWeight) {
      init();
    }
/*  GenParticleAnalysis::GenParticleAnalysis(){
    init();
  }*/

  GenParticleAnalysis::~GenParticleAnalysis() {}

  void GenParticleAnalysis::init(){
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("GenParticleAnalysis");
    
    hRtau1pHp = makeTH<TH1F>(myDir, "genRtau1ProngHp", "genRtau1ProngHp", 100, 0., 1.2);
    hRtau13pHp = makeTH<TH1F>(myDir, "genRtau13ProngHp", "genRtau13ProngHp", 100, 0., 1.2);
    hRtau3pHp = makeTH<TH1F>(myDir, "genRtau3ProngHp", "genRtau3ProngHp", 100, 0., 1.2);
    hRtau1pW = makeTH<TH1F>(myDir, "genRtau1ProngW", "genRtau1ProngW", 100, 0., 1.2);
    hRtau13pW = makeTH<TH1F>(myDir, "genRtau13ProngW", "genRtau13ProngW", 100, 0., 1.2);
    hRtau3pW = makeTH<TH1F>(myDir, "genRtau3ProngW", "genRtau3ProngW", 100, 0., 1.2);
    hptVisibleTau1pHp = makeTH<TH1F>(myDir, "genptVisibleTau1ProngHp", "ptVisibleTau1ProngHp", 100, 0., 200);
    hptVisibleTau13pHp = makeTH<TH1F>(myDir, "genptVisibleTau13ProngHp", "ptVisibleTau13ProngHp", 100, 0., 200);
    hptVisibleTau3pHp = makeTH<TH1F>(myDir, "genptVisibleTau3ProngHp", "ptVisibleTau3ProngHp", 100, 0., 200);
    hEtaVisibleTau1pHp = makeTH<TH1F>(myDir, "genEtaVisibleTau1ProngHp", "etaVisibleTau1ProngHp", 100, -5., 5);
    hLeadingTrack1pHp = makeTH<TH1F>(myDir, "genLeadingTrack1ProngHp", "LeadingTrack1ProngHp", 100, 0., 200);
    hptVisibleTau1pW = makeTH<TH1F>(myDir, "genPtVisibleTau1ProngW", "ptVisibleTau1ProngW", 100, 0., 200);
    hptVisibleTau13pW = makeTH<TH1F>(myDir, "genPtVisibleTau13ProngW", "ptVisibleTau13ProngW", 100, 0., 200);
    hptVisibleTau3pW = makeTH<TH1F>(myDir, "genPtVisibleTau3ProngW", "ptVisibleTau3ProngW", 100, 0., 200);
    hEtaVisibleTau1pW = makeTH<TH1F>(myDir, "genEtaVisibleTau1ProngW", "etaVisibleTau1ProngW", 100, -5., 5);
    hLeadingTrack1pW = makeTH<TH1F>(myDir, "genLeadingTrack1ProngW", "LeadingTrack1ProngW", 100, 0., 200);
    hTauMass1pHp = makeTH<TH1F>(myDir, "genTauMass1pHp", "genTauMass1pHp", 100, 0., 2.);
    hTauMass1pW = makeTH<TH1F>(myDir, "genTauMass1pW", "genTauMass1pW", 100, 0., 2.);
    hThetaCM1pHp = makeTH<TH1F>(myDir, "genThetaCM1pHp", "genThetaCMs1pHp", 100, 0., 3.);
    hThetaCM1pW = makeTH<TH1F>(myDir, "genThetaCM1pW", "genThetaCMs1pW", 100, 0., 3.);
    hMagCM1pHp = makeTH<TH1F>(myDir, "genMagCM1pHp", "genMagCMs1pHp", 100, 0.95, 1.);
    hMagCM1pW = makeTH<TH1F>(myDir, "genMagCM1pW", "genMagCMs1pW", 100, 0.95, 1.);
    hHpMass = makeTH<TH1F>(myDir, "HpMass", "HpMass", 100, 100, 200.);
    hBquarkMultiplicity = makeTH<TH1F>(myDir, "genBquark_Multiplicity", "genBquark_Multiplicity", 20, -0.5, 19.5);
    hBquarkStatus2Multiplicity = makeTH<TH1F>(myDir, "genBquark_Status2_Multiplicity", "genBquark_Status2_Multiplicity", 20, -0.5, 19.5);
    hBquarkStatus3Multiplicity = makeTH<TH1F>(myDir, "genBquark_Status3_Multiplicity", "genBquark_Status3_Multiplicity", 20, -0.5, 19.5);
    hBquarkFromTopEta = makeTH<TH1F>(myDir, "genBquark_FromTop_Eta", "genBquark_FromTop_Eta", 300, -6.0, 6.0);
    hBquarkNotFromTopEta = makeTH<TH1F>(myDir, "genBquark_NotFromTop_Eta", "genBquark_NotFromTop_Eta", 300, -6.0, 6.0);
    hBquarkFromTopPt = makeTH<TH1F>(myDir, "genBquark_FromTop_Pt", "genBquark_FromTop_Pt", 400, 0., 800.);
    hBquarkNotFromTopPt = makeTH<TH1F>(myDir, "genBquark_NotFromTop_Pt", "genBquark_NotFromTop_Pt", 400, 0., 800.);
    hBquarkFromTopDeltaRTau = makeTH<TH1F>(myDir, "genBquark_FromTop_DeltaRTau", "genBquark_FromTop_DeltaRTau", 300, 0., 8.);
    hBquarkNotFromTopDeltaRTau = makeTH<TH1F>(myDir, "genBquark_NotFromTop_DeltaRTau", "genBquark_NotFromTop_DeltaRTau", 300, 0., 8.);
    hTopPt = makeTH<TH1F>(myDir, "genTopPt", "genTopPt", 300, 0., 600);
    hTopPt_wrongB = makeTH<TH1F>(myDir, "genTopPt_wrongB", "genTopPt_wrongB", 300, 0., 600);
  }

  void GenParticleAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup ){
  
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;


    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(edm::InputTag("VisibleTaus","HadronicTauOneProng"),oneProngTaus);

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(edm::InputTag("VisibleTaus","HadronicTauOneAndThreeProng"),oneAndThreeProngTaus);	  


    edm::Handle <std::vector<LorentzVector> > threeProngTaus;
    iEvent.getByLabel(edm::InputTag("VisibleTaus","HadronicTauThreeProng"),threeProngTaus);	  


    // One-prong tau jets
    double Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = oneProngTaus->begin();tau!=oneProngTaus->end();++tau) {
  
      double ptmax = 0;
      bool tauFromHiggs = false;
      bool tauFromW = false;

      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	double mass = p.mass();
	int id = p.pdgId();
	if ( abs(id) == 37) {
	  hHpMass->Fill(mass);
	}
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR > 0.2) continue;
	if ( abs(id) == 15 ) {
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    int status = dparticle->status();
	    if ( abs(idmother) == 37 ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }


      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	
	if ( abs(id) != 211 ) continue;      
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	  }
	}
	
      }
      
      double thetaCM = tau->BoostToCM().Theta();
      double magCM = tau->BoostToCM().mag2();
      
      if (tauFromHiggs ) {
	hptVisibleTau1pHp->Fill(tau->pt(), fEventWeight.getWeight());
	hEtaVisibleTau1pHp->Fill(tau->eta(), fEventWeight.getWeight());
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau1pHp->Fill(Rtau, fEventWeight.getWeight());
	  hLeadingTrack1pHp->Fill(ptmax, fEventWeight.getWeight());
	  hThetaCM1pHp->Fill(thetaCM, fEventWeight.getWeight()); 
	  hTauMass1pHp->Fill(tau->mass(), fEventWeight.getWeight());
	  hMagCM1pHp->Fill(magCM, fEventWeight.getWeight());
	}
      }
      if (tauFromW) {
	hptVisibleTau1pW->Fill(tau->pt(), fEventWeight.getWeight());
	hEtaVisibleTau1pW->Fill(tau->eta(), fEventWeight.getWeight());
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau1pW->Fill(Rtau, fEventWeight.getWeight());
	  hLeadingTrack1pW->Fill(ptmax, fEventWeight.getWeight());
	  hThetaCM1pW->Fill(thetaCM, fEventWeight.getWeight()); 
	  hTauMass1pW->Fill(tau->mass(), fEventWeight.getWeight());
	  hMagCM1pW->Fill(magCM, fEventWeight.getWeight());
	}
      }
    }
    


   // One-and-three prong tau jets
    Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
  
      double ptmax = 0;   
      bool tauFromHiggs = false;
      bool tauFromW = false;

      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) == 15 ) {
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    int status = dparticle->status();
	    if ( abs(idmother) == 37 ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }



      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	
	if ( abs(id) != 211 ) continue;
	
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	  }
	}
      }

      if (tauFromHiggs ) {
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau13pHp->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau13pHp->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau13pW->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau13pW->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
    }
    
   // Three-prong tau jets
    Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = threeProngTaus->begin();tau!=threeProngTaus->end();++tau) {  
      //const reco::GenParticle* matchingPion;
      double ptmax = 0;
      bool tauFromHiggs = false;
      bool tauFromW = false;
      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) == 15 ) {
	  //	  bool tauFromHiggs = false;
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    int status = dparticle->status();
	    if ( abs(idmother) == 37  ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }


      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) != 211 ) continue;
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	    //matchingPion  =  dynamic_cast<const reco::GenParticle*>(&p);
	  }
	}
      }
      
      //     std::cout << " pion 1/3 prong " <<  ptmax << " Rtau  " <<  Rtau << std::endl;
      
      if (tauFromHiggs ) {
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pHp->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau3pHp->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 40 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pW->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau3pW->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
    }


    
    // b-quark analysis
    int nBquarks = 0;
    // loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){  
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 5 ) continue;    
      bool bHasBquarkDaughter = false;
      // Check whether the genParticle decays to itself. If yes do not consider in counting
      if ( p.numberOfDaughters() != 0 ){
      	// Loop over all 1st daughters of genParticle    
      	for(size_t j = 0; j < p.numberOfDaughters() ; ++ j) {
      	  const reco::Candidate *d = p.daughter( j );
      	  if( p.pdgId() == d->pdgId() ) bHasBquarkDaughter = true; 
      	}
      }
      if(bHasBquarkDaughter) continue;
      nBquarks++;      
    }
    hBquarkMultiplicity->Fill(nBquarks, fEventWeight.getWeight());
    
    
    double bPt, bEta;
    // Generate a vector of all taus from H+
    std::vector<LorentzVector> tausFromHp;
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if(abs(id) == 15 && (hasMother(p,37) || hasMother(p,-37))) tausFromHp.push_back(p.p4());
    }
    // loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      // Only choose beauties
      if ( abs(id) != 5 ) continue;
      bEta = p.eta();
      bPt = p.pt();
      
      bool bHasBquarkMother = false;
      bool bHasTopMother = false;
      int motherId = 99999;
      // loop over mother particles
      for (size_t im=0; im < p.numberOfMothers(); ++im){
      	const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
      	if ( !mparticle) continue;
      	motherId = mparticle->pdgId();
      	if( id == motherId ) bHasBquarkMother = true; 
      	if (abs(motherId) == 6 ) bHasTopMother = true;
      }      
      // Make sure the b doesn't have b as mother
      if(bHasBquarkMother) continue;
      // Plot eta, pt and deltaR in different histos based on whether there was a t mother or not
      if(bHasTopMother) {
        hBquarkFromTopEta->Fill(bEta, fEventWeight.getWeight());
      	hBquarkFromTopPt->Fill(bPt, fEventWeight.getWeight());
        for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
          // Check that the tau comes from H+
          bool tauFromHp = false;
          for(size_t itau=0; itau<tausFromHp.size(); ++itau) {
            if(ROOT::Math::VectorUtil::DeltaR(*tau, tausFromHp[itau]) < 0.4){
              tauFromHp=true;
              break;
            }
          }
          if(tauFromHp) {
            double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
            hBquarkFromTopDeltaRTau->Fill(deltaR, fEventWeight.getWeight());
          }
        }
      }
      else {
    	hBquarkNotFromTopEta->Fill(bEta, fEventWeight.getWeight());
    	hBquarkNotFromTopPt->Fill(bPt, fEventWeight.getWeight());
        for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
          // Check that the tau comes from H+
          bool tauFromHp = false;
          for(size_t itau=0; itau<tausFromHp.size(); ++itau) {
            if(ROOT::Math::VectorUtil::DeltaR(*tau, tausFromHp[itau]) < 0.4){
              tauFromHp=true;
              break;
            }
          }
          if(tauFromHp) {
            double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
            hBquarkNotFromTopDeltaRTau->Fill(deltaR, fEventWeight.getWeight());
          }
        }
      }
    }
    
        
        
    // loop over all genParticles, search tops that decay to u and d and calculate pt
    // also calculate the "wrong" pt, by picking the b quark that does not come from the t
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 6 || hasDaughter(p,id)) continue;
      std::vector<const reco::GenParticle*> daughters = getDaughters(p);
      int daughterId=9999;
      double px = 0, py = 0;
      double px_wrong = 0, py_wrong = 0;
      bool decaysHadronically = false;
      for(size_t d=0; d<daughters.size(); ++d) {
        const reco::GenParticle dparticle = *daughters[d];
        daughterId = dparticle.pdgId();
        if(abs(daughterId) < 5) {
      	  decaysHadronically = true;
        }
        if( abs(daughterId) == 24 && !hasMother(dparticle, daughterId)) {
          px += dparticle.px();
          py += dparticle.py();
          px_wrong += dparticle.px();
          py_wrong += dparticle.py();
        }
        if( abs(daughterId) == 5  && !hasMother(dparticle, daughterId)) {
          px += dparticle.px();
          py += dparticle.py();
        }
        // Look for other b quarks
        for (size_t j=0; j < genParticles->size(); ++j){
          const reco::Candidate & b = (*genParticles)[i];
          int bId = b.pdgId();
          if ( abs(bId) != 5 || hasMother(p,bId) || hasMother(p,6) || hasMother(p,-6)) continue;
          px_wrong += b.px();
          py_wrong += b.py();
          // Stop at the first found b quark that does not come from top
          break;
        }
      }
      if(decaysHadronically) {
        hTopPt->Fill(sqrt(px*px+py*py), fEventWeight.getWeight());
        hTopPt_wrongB->Fill(sqrt(px_wrong*px_wrong+py_wrong*py_wrong), fEventWeight.getWeight());
      }
    }    
  }
   //eof: void GenParticleAnalysis::analyze()


  std::vector<const reco::GenParticle*> GenParticleAnalysis::getMothers(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> mothers;
    for (size_t im=0; im < p.numberOfMothers(); ++im){
      const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
      if (mparticle) { 
        mothers.push_back(mparticle);
        std::vector<const reco::GenParticle*> mmothers = getMothers( * (dynamic_cast<const reco::Candidate*> (mparticle)) );
        mothers.insert(mothers.end(), mmothers.begin(), mmothers.end()); 
      }
    }
    return mothers;
  }
  
  bool GenParticleAnalysis::hasMother(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    for (size_t im=0; im < mothers.size(); ++im){
      if (mothers[im]->pdgId() == id) return true;
    }
    return false;
  }  

  void GenParticleAnalysis::printMothers(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    std::cout << "Mothers of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < mothers.size(); ++im){
      std::cout << "  " << mothers[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  

  std::vector<const reco::GenParticle*> GenParticleAnalysis::getDaughters(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> daughters;
    for (size_t im=0; im < p.numberOfDaughters(); ++im){
      const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
      if (dparticle) {
        daughters.push_back(dparticle);
        std::vector<const reco::GenParticle*> ddaughters = getDaughters( * (dynamic_cast<const reco::Candidate*> (dparticle)) );
        daughters.insert(daughters.end(), ddaughters.begin(), ddaughters.end()); 
      }
    }
    return daughters;
  }
  
  bool GenParticleAnalysis::hasDaughter(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    for (size_t im=0; im < daughters.size(); ++im){
      if (daughters[im]->pdgId() == id) return true;
    }
    return false;
  }
  
  void GenParticleAnalysis::printDaughters(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    std::cout << "Daughters of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < daughters.size(); ++im){
      std::cout << "  " << daughters[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  


  std::vector<const reco::Candidate*> GenParticleAnalysis::doQCDmAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup ){

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    std::vector<const reco::Candidate*> genBquarks;
  
    // b-quark analysis
    int nBquarks = 0;
    int nStatus2Bquarks = 0;
    int nStatus3Bquarks = 0;

    /// Loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){  
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      
      if ( abs(id) != 5 ) continue;
      nBquarks++;
      if (p.status() == 2) nStatus2Bquarks++;
      if (p.status() == 3) nStatus3Bquarks++;
      
      genBquarks.push_back(&p);
      
    } //eof:  for 
    hBquarkMultiplicity->Fill(nBquarks, fEventWeight.getWeight());
    hBquarkStatus2Multiplicity ->Fill(nStatus2Bquarks, fEventWeight.getWeight());
    hBquarkStatus3Multiplicity ->Fill(nStatus3Bquarks, fEventWeight.getWeight());
    
    return genBquarks;
  }

  
}
