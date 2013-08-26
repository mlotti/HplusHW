#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "TTree.h"

#include<cmath>

namespace HPlus {
  TreeGenParticleBranches::TreeGenParticleBranches(const std::string& prefix):
    fPrefix(prefix)
  {
    reset();
  }
  TreeGenParticleBranches::~TreeGenParticleBranches() {}

  void TreeGenParticleBranches::book(TTree *tree) {
    tree->Branch((fPrefix+"_p4").c_str(), &fP4);
    tree->Branch((fPrefix+"_pdgid").c_str(), &fPdgId);
    tree->Branch((fPrefix+"_mother_pdgid").c_str(), &fMotherPdgId);
    tree->Branch((fPrefix+"_grandmother_pdgid").c_str(), &fGrandMotherPdgId);
  }

  void TreeGenParticleBranches::addValue(const reco::GenParticle *particle) {
    XYZTLorentzVector p4;
    int pdgId = 0;
    int motherPdgId = 0;
    int grandMotherPdgId = 0;

    if(particle) {
      p4 = particle->p4();
      pdgId = particle->pdgId();
      const reco::GenParticle *mother = GenParticleTools::findMother(particle);
      if(mother) {
        motherPdgId = mother->pdgId();
        const reco::GenParticle *grandMother = GenParticleTools::findMother(mother);
        if(grandMother) {
          grandMotherPdgId = grandMother->pdgId();
        }
      }
    }

    fP4.push_back(p4);
    fPdgId.push_back(pdgId);
    fMotherPdgId.push_back(motherPdgId);
    fGrandMotherPdgId.push_back(grandMotherPdgId);
  }

  void TreeGenParticleBranches::reset() {
    fP4.clear();
    fPdgId.clear();
    fMotherPdgId.clear();
    fGrandMotherPdgId.clear();
  }
}
