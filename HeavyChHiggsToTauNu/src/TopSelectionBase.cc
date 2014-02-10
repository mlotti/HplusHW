#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {
  typedef TopSelectionBase::Data Data;

  //constructor and desturctor
  TopSelectionBase::TopSelectionBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper) {}
  TopSelectionBase::~TopSelectionBase() {}

  //constructor and destructor for TopSelectionBase::Data class
  TopSelectionBase::Data::Data():
    fPassedEvent(false) {}
  TopSelectionBase::Data::~Data() {}
  
  //silentAnalyze
  Data TopSelectionBase::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, bjets);
  }

  //analyze
  Data TopSelectionBase::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, bjets);
  }

  //silentAnalyze (for BSelection)
  Data TopSelectionBase::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  }

  //analyze (for BSelection)
  Data TopSelectionBase::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  }

  //privateAnalyze
  Data TopSelectionBase::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    Data output;
    return output;
  }

  //privateAnalyze (for BSelection)
  Data TopSelectionBase::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) { 
    Data output;
    return output;
  }
  
  // helper functions
   
  std::vector<const reco::GenParticle*>   TopSelectionBase::getImmediateMothers(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> mothers;
    for (size_t im=0; im < p.numberOfMothers(); ++im){
      const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
      if (mparticle) mothers.push_back(mparticle);
    }
    return mothers;
  }
      
  std::vector<const reco::GenParticle*>   TopSelectionBase::getMothers(const reco::Candidate& p){ 
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
      
  bool  TopSelectionBase::hasImmediateMother(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
    for (size_t im=0; im < mothers.size(); ++im){
      if (mothers[im]->pdgId() == id) return true;
    }
    return false;
  }  
      
  bool  TopSelectionBase::hasMother(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    for (size_t im=0; im < mothers.size(); ++im){
      if (mothers[im]->pdgId() == id) return true;
    }
    return false;
  } 
 
  void  TopSelectionBase::printImmediateMothers(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
    std::cout << "Immediate mothers of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < mothers.size(); ++im){
      std::cout << "  " << mothers[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  
      
  void  TopSelectionBase::printMothers(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    std::cout << "Mothers of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < mothers.size(); ++im){
      std::cout << "  " << mothers[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
      }  
      std::vector<const reco::GenParticle*>  TopSelectionBase::getImmediateDaughters(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> daughters;
    for (size_t im=0; im < p.numberOfDaughters(); ++im){
      const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
      if (dparticle) daughters.push_back(dparticle);
    }
    return daughters;
  }
      
  std::vector<const reco::GenParticle*>   TopSelectionBase::getDaughters(const reco::Candidate& p){ 
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
      
  bool  TopSelectionBase::hasImmediateDaughter(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
    for (size_t im=0; im < daughters.size(); ++im){
      if (daughters[im]->pdgId() == id) return true;
    }
    return false;
      }
      bool  TopSelectionBase::hasDaughter(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    for (size_t im=0; im < daughters.size(); ++im){
      if (daughters[im]->pdgId() == id) return true;
    }
    return false;
  }
      
  void  TopSelectionBase::printImmediateDaughters(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
    std::cout << "Immediate daughters of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < daughters.size(); ++im){
      std::cout << "  " << daughters[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  
      
  void  TopSelectionBase::printDaughters(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    std::cout << "Daughters of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < daughters.size(); ++im){
      std::cout << "  " << daughters[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }
      
}  
