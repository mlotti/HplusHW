#ifndef HigssAnalysis_HeavyChHiggsToTauNu_genParticleMotherTools
#define HigssAnalysis_HeavyChHiggsToTauNu_genParticleMotherTools

#include <vector>

namespace reco {
  class Candidate;
  class GenParticle;
}

namespace HPlus {
  std::vector<const reco::GenParticle*> getImmediateMothers(const reco::Candidate& p);
  std::vector<const reco::GenParticle*> getMothers(const reco::Candidate& p);
  bool hasImmediateMother(const reco::Candidate& p, int id);
  bool hasMother(const reco::Candidate& p, int id);
  void printImmediateMothers(const reco::Candidate& p);
  void printMothers(const reco::Candidate& p);
  std::vector<const reco::GenParticle*> getImmediateDaughters(const reco::Candidate& p);
  std::vector<const reco::GenParticle*> getDaughters(const reco::Candidate& p);
  bool hasImmediateDaughter(const reco::Candidate& p, int id);
  bool hasDaughter(const reco::Candidate& p, int id);
  void printImmediateDaughters(const reco::Candidate& p);
  void printDaughters(const reco::Candidate& p);
}
#endif

