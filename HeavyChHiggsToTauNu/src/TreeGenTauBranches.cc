#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenTauBranches.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<cmath>

namespace HPlus {
  TreeGenTauBranches::TreeGenTauBranches(const std::string& prefix):
    fPrefix(prefix),
    fGenParticle(prefix)
  {
    reset();
  }
  TreeGenTauBranches::~TreeGenTauBranches() {}

  void TreeGenTauBranches::book(TTree *tree) {
    fGenParticle.book(tree);
    tree->Branch((fPrefix+"_daughter_pdgid").c_str(), &fDaughterPdgId);
    tree->Branch((fPrefix+"_visible_p4").c_str(), &fVisibleP4);
  }

  void TreeGenTauBranches::addValue(const reco::GenParticle *tau) {
    fGenParticle.addValue(tau);

    int daughterPdgId = 0;
    XYZTLorentzVector visibleP4;
    if(tau && std::abs(tau->pdgId()) == 15) {
      const reco::GenParticle *daughter = GenParticleTools::findTauDaughter(tau);
      if(daughter)
        daughterPdgId = daughter->pdgId();
      
      visibleP4 = GenParticleTools::calculateVisibleTau(tau);
    }

    fDaughterPdgId.push_back(daughterPdgId);
    fVisibleP4.push_back(visibleP4);
  }

  void TreeGenTauBranches::reset() {
    fGenParticle.reset();
    fDaughterPdgId.clear();
    fVisibleP4.clear();
  }
}
