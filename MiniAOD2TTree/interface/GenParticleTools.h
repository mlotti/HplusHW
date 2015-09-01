#ifndef GenParticleTools_h
#define GenParticleTools_h

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Handle.h"

#include <vector>

namespace GenParticleTools {
  /// Finds particles by ID; returns a vector of pointers to the particles
  std::vector<const reco::Candidate*> findParticles(edm::Handle<reco::GenParticleCollection>& handle, int pID);
  /// Returns offspring particles for a mother particle
  std::vector<const reco::Candidate*> findOffspring(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* mother);
  /// Returns ancestry particles for a particle
  std::vector<const reco::Candidate*> findAncestry(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* particle);
}
#endif
