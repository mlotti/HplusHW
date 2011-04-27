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
    hRtau1pHp = makeTH<TH1F>(*fs, "genRtau1ProngHp", "genRtau1ProngHp", 100, 0., 1.2);
    hRtau13pHp = makeTH<TH1F>(*fs, "genRtau13ProngHp", "genRtau13ProngHp", 100, 0., 1.2);
    hRtau3pHp = makeTH<TH1F>(*fs, "genRtau3ProngHp", "genRtau3ProngHp", 100, 0., 1.2);
    hRtau1pW = makeTH<TH1F>(*fs, "genRtau1ProngW", "genRtau1ProngW", 100, 0., 1.2);
    hRtau13pW = makeTH<TH1F>(*fs, "genRtau13ProngW", "genRtau13ProngW", 100, 0., 1.2);
    hRtau3pW = makeTH<TH1F>(*fs, "genRtau3ProngW", "genRtau3ProngW", 100, 0., 1.2);
    hptVisibleTau1pHp = makeTH<TH1F>(*fs, "genptVisibleTau1ProngHp", "ptVisibleTau1ProngHp", 100, 0., 200);
    hptVisibleTau13pHp = makeTH<TH1F>(*fs, "genptVisibleTau13ProngHp", "ptVisibleTau13ProngHp", 100, 0., 200);
    hptVisibleTau3pHp = makeTH<TH1F>(*fs, "genptVisibleTau3ProngHp", "ptVisibleTau3ProngHp", 100, 0., 200);
    hEtaVisibleTau1pHp = makeTH<TH1F>(*fs, "genEtaVisibleTau1ProngHp", "etaVisibleTau1ProngHp", 100, -5., 5);
    hLeadingTrack1pHp = makeTH<TH1F>(*fs, "genLeadingTrack1ProngHp", "LeadingTrack1ProngHp", 100, 0., 200);
    hptVisibleTau1pW = makeTH<TH1F>(*fs, "genPtVisibleTau1ProngW", "ptVisibleTau1ProngW", 100, 0., 200);
    hptVisibleTau13pW = makeTH<TH1F>(*fs, "genPtVisibleTau13ProngW", "ptVisibleTau13ProngW", 100, 0., 200);
    hptVisibleTau3pW = makeTH<TH1F>(*fs, "genPtVisibleTau3ProngW", "ptVisibleTau3ProngW", 100, 0., 200);
    hEtaVisibleTau1pW = makeTH<TH1F>(*fs, "genEtaVisibleTau1ProngW", "etaVisibleTau1ProngW", 100, -5., 5);
    hLeadingTrack1pW = makeTH<TH1F>(*fs, "genLeadingTrack1ProngW", "LeadingTrack1ProngW", 100, 0., 200);
    hTauMass1pHp = makeTH<TH1F>(*fs, "genTauMass1pHp", "genTauMass1pHp", 100, 0., 2.);
    hTauMass1pW = makeTH<TH1F>(*fs, "genTauMass1pW", "genTauMass1pW", 100, 0., 2.);
    hThetaCM1pHp = makeTH<TH1F>(*fs, "genThetaCM1pHp", "genThetaCMs1pHp", 100, 0., 3.);
    hThetaCM1pW = makeTH<TH1F>(*fs, "genThetaCM1pW", "genThetaCMs1pW", 100, 0., 3.);
    hMagCM1pHp = makeTH<TH1F>(*fs, "genMagCM1pHp", "genMagCMs1pHp", 100, 0.95, 1.);
    hMagCM1pW = makeTH<TH1F>(*fs, "genMagCM1pW", "genMagCMs1pW", 100, 0.95, 1.);
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
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR > 0.2) continue;
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
      
      double thetaCM = tau->BoostToCM().Theta();
      double magCM = tau->BoostToCM().mag2();
      
      if (tauFromHiggs ) {
	hptVisibleTau1pHp->Fill(tau->pt(), fEventWeight.getWeight());
	hEtaVisibleTau1pHp->Fill(tau->eta(), fEventWeight.getWeight());
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
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
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
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
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
	  hRtau13pHp->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau13pHp->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
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
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pHp->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau3pHp->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 30 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pW->Fill(Rtau, fEventWeight.getWeight());
	  hptVisibleTau3pW->Fill(tau->pt(), fEventWeight.getWeight());
	}
      }
    }
  }
  
}
