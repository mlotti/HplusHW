#ifndef GENPARTICLEMOTHERTOOLS_CC
#define GENPARTICLEMOTHERTOOLS_CC

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include <limits>



   std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> mothers;
	for (size_t im=0; im < p.numberOfMothers(); ++im){
	  const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	  if (mparticle) mothers.push_back(mparticle);
	}
	return mothers;
      }
      
      std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p){ 
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
      
      bool  hasImmediateMother(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
	for (size_t im=0; im < mothers.size(); ++im){
	  if (mothers[im]->pdgId() == id) return true;
	}
	return false;
      }  
     
      bool  hasMother(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> mothers = getMothers(p);
	for (size_t im=0; im < mothers.size(); ++im){
	  if (mothers[im]->pdgId() == id) return true;
	}
	return false;
      } 
 
     void  printImmediateMothers(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
	std::cout << "Immediate mothers of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < mothers.size(); ++im){
	  std::cout << "  " << mothers[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      
      void  printMothers(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> mothers = getMothers(p);
	std::cout << "Mothers of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < mothers.size(); ++im){
	  std::cout << "  " << mothers[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> daughters;
	for (size_t im=0; im < p.numberOfDaughters(); ++im){
	  const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
	  if (dparticle) daughters.push_back(dparticle);
	}
	return daughters;
      }
      
      std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p){ 
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
      
      bool  hasImmediateDaughter(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
	for (size_t im=0; im < daughters.size(); ++im){
	  if (daughters[im]->pdgId() == id) return true;
	}
	return false;
      }
      bool  hasDaughter(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> daughters = getDaughters(p);
	for (size_t im=0; im < daughters.size(); ++im){
	  if (daughters[im]->pdgId() == id) return true;
	}
	return false;
      }
      
      void  printImmediateDaughters(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
	std::cout << "Immediate daughters of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < daughters.size(); ++im){
	  std::cout << "  " << daughters[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      
      void printDaughters(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> daughters = getDaughters(p);
	std::cout << "Daughters of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < daughters.size(); ++im){
	  std::cout << "  " << daughters[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
#endif
