#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenBranches.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/View.h"

#include "TTree.h"

#include<cstdlib>
#include<cmath>

namespace HPlus {
  TreeGenBranches::TreeGenBranches(const edm::ParameterSet& iConfig):
    fGenSrc(iConfig.getParameter<edm::InputTag>("genParticleSrc"))
  {
    reset();
  }
  TreeGenBranches::~TreeGenBranches() {}

  void TreeGenBranches::book(TTree *tree) {
    tree->Branch("gen_number_BQuarks", &fNumberBquarks);
    tree->Branch("gen_number_WToTau", &fNumberWTaus);
    tree->Branch("gen_number_ZToTau", &fNumberZTaus);
    tree->Branch("gen_number_HToTau", &fNumberHTaus);
    tree->Branch("gen_number_XToTau", &fNumberXTaus);
  }

  void TreeGenBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
    iEvent.getByLabel(fGenSrc, hgenparticles);

    for(edm::View<reco::GenParticle>::const_iterator iGen = hgenparticles->begin(); iGen != hgenparticles->end(); ++iGen) {
      int pdgid = std::abs(iGen->pdgId());

      // We're not really interested in radiation, where the pdgId stays
      if(iGen->mother() && iGen->mother()->pdgId() == iGen->pdgId())
        continue;

      // Count number of b quarks
      if(pdgid == 5) {
        fNumberBquarks++;
      }

      if(pdgid == 15) {
        int motherid = std::abs(iGen->mother()->pdgId());
        if(motherid == 24) // W
          fNumberWTaus++;
        else if(motherid == 23) // Z
          fNumberZTaus++;
        else if(motherid == 37) // H+
          fNumberHTaus++;
        else // anything else
          fNumberXTaus++; 
      }
    }
  }

  void TreeGenBranches::reset() {
    fNumberBquarks = 0;
    fNumberWTaus = 0;
    fNumberZTaus = 0;
    fNumberHTaus = 0;
    fNumberXTaus = 0;
  }
}
