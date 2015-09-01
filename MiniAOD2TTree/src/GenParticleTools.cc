#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleTools.h"

namespace GenParticleTools {  
  std::vector<const reco::Candidate*> findParticles(edm::Handle<reco::GenParticleCollection>& handle, int pID) {
    std::vector<const reco::Candidate*> matches;
    for(size_t i = 0; i < handle->size(); ++i) {
      const reco::Candidate & gp = handle->at(i);
      if (abs(gp.pdgId()) == pID) {
        // Check for radiation; save only the lepton after the radiation
        bool myStatus = true;
        for (size_t k = 0; k < gp.numberOfDaughters(); ++k) {
          if (abs(gp.daughter(k)->pdgId()) == pID)
            myStatus = false;
        }
        if (myStatus) {
          matches.push_back(&(handle->at(i)));
        }
      }
    }
    return matches;
  }

  std::vector<const reco::Candidate*> findOffspring(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* mother) {
    std::vector<const reco::Candidate*> offspring;
    for (size_t k = 0; k < mother->numberOfDaughters(); ++k) {
      // Save only particles after radiation
      if (mother->daughter(k)->pdgId() != mother->pdgId()) {
        offspring.push_back(mother->daughter(k));
      }
      // Save offspring of the daughter
      std::vector<const reco::Candidate*> newOffspring = findOffspring(handle, mother->daughter(k));
      for (auto p: newOffspring) {
        // Save only particles after radiation
        if (mother->daughter(k)->pdgId() != p->pdgId()) {
          offspring.push_back(p);
        }
      }
    }
    return offspring;
  }

  std::vector<const reco::Candidate*> findAncestry(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* particle) {
    std::vector<const reco::Candidate*> ancestry;
    if (particle->mother() != nullptr) {
      if (particle->pdgId() != particle->mother()->pdgId())
        ancestry.push_back(particle->mother());
      std::vector<const reco::Candidate*> newAncestry = findAncestry(handle, particle->mother());
      for (auto p: newAncestry) {
        ancestry.push_back(p);
      }
    }
    return ancestry;
  }
}