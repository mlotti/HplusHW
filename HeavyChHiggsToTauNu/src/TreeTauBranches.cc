#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTauBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeTauBranches::TreeTauBranches(const edm::ParameterSet& iConfig):
    fTauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
    fTausGenMatch("taus_genmatch")
  {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("tauFunctions");
    std::vector<std::string> names = pset.getParameterNames();
    fTausFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fTausFunctions.push_back(TauFunctionBranch("taus_f_"+names[i], pset.getParameter<std::string>(names[i])));
    }
  }
  TreeTauBranches::~TreeTauBranches() {}


  void TreeTauBranches::book(TTree *tree) {
    tree->Branch("taus_p4", &fTaus);

    tree->Branch("taus_leadPFChargedHadrCand_p4", &fTausLeadingChCand);
    tree->Branch("taus_signalPFChargedHadrCands_n", &fTausSignalChCands);
    tree->Branch("taus_emFraction", &fTausEmFraction);
    tree->Branch("taus_decayMode", &fTausDecayMode);

    for(size_t i=0; i<fTausFunctions.size(); ++i) {
      fTausFunctions[i].book(tree);
    }

    fTausGenMatch.book(tree);
  }

  void TreeTauBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fTauSrc, htaus);
    setValues(*htaus);
  }

  void TreeTauBranches::setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fTauSrc, htaus);
    setValues(*htaus);

    for(size_t i=0; i<htaus->size(); ++i) {
      const pat::Tau& tau = htaus->at(i);
      const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 15, tau, 0.5, true);
      if(!gen) {
        gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 13, tau, 0.5);
      }
      if(!gen) {
        gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 11, tau, 0.5);
      }

      fTausGenMatch.addValue(gen);
    }
  }

  void TreeTauBranches::setValues(const edm::View<pat::Tau>& taus) {
    for(size_t i=0; i<taus.size(); ++i) {
      const pat::Tau& tau = taus[i];
      fTaus.push_back(tau.p4());
      if(tau.leadPFChargedHadrCand().isNonnull())
        fTausLeadingChCand.push_back(tau.leadPFChargedHadrCand()->p4());
      fTausEmFraction.push_back(tau.emFraction());
      fTausSignalChCands.push_back(tau.signalPFChargedHadrCands().size());
      fTausDecayMode.push_back(tau.decayMode());
    }

    for(size_t i=0; i<fTausFunctions.size(); ++i) {
      fTausFunctions[i].setValues(taus);
    }
  }

  void TreeTauBranches::reset() {
    fTaus.clear();

    fTausLeadingChCand.clear();
    fTausEmFraction.clear();
    fTausSignalChCands.clear();
    fTausDecayMode.clear();

    for(size_t i=0; i<fTausFunctions.size(); ++i)
      fTausFunctions[i].reset();

    fTausGenMatch.reset();
  }
}
