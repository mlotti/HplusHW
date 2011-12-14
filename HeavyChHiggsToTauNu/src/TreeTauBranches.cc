#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTauBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeTauBranches::TreeTauBranches(const edm::ParameterSet& iConfig):
    fTauSrc(iConfig.getParameter<edm::InputTag>("tauSrc"))
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

    tree->Branch("taus_pdgid", &fTausPdgId);
    tree->Branch("taus_mother_pdgid", &fTausMotherPdgId);
    tree->Branch("taus_grandmother_pdgid", &fTausGrandMotherPdgId);
    tree->Branch("taus_daughter_pdgid", &fTausDaughterPdgId);
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
      const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 15, tau, 0.5);
      if(!gen) {
        const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 13, tau, 0.5);
      }
      if(!gen) {
        const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 11, tau, 0.5);
      }

      int pdgId = 0;
      int motherPdgId = 0;
      int grandMotherPdgId = 0;
      int daughterPdgId = 0;
      if(gen) {
        pdgId = gen->pdgId();
        const reco::GenParticle *mother = GenParticleTools::findMother(gen);
        if(mother) {
          motherPdgId = mother->pdgId();
          const reco::GenParticle *grandMother = GenParticleTools::findMother(mother);
          if(grandMother)
            grandMotherPdgId = grandMother->pdgId();
        }

        size_t nDaughters = gen->numberOfDaughters();
        for(size_t j=0; j<nDaughters; ++j) {
          int id = gen->daughter(j)->pdgId();
          int ida = std::abs(id);
          // ignore neutrinos
          if(ida == 12 || ida == 14 || ida == 16)
            continue;

          // if e/mu, take it
          if(ida == 11 || ida == 13) {
            daughterPdgId = id;
            break;
          }

          // if W, look for it's non-neutrino daughter
          if(ida == 24) {
            const reco::GenParticle *daugh = GenParticleTools::findMaxNonNeutrinoDaughter(dynamic_cast<const reco::GenParticle *>(gen->daughter(j)));
            if(daugh != 0) {
              daughterPdgId = daugh->pdgId();
              break;
            }
          }
          
          // else, take the one with largest id number, and continue
          if(ida > std::abs(daughterPdgId))
            daughterPdgId = id;
        }
      }

      fTausPdgId.push_back(pdgId);
      fTausMotherPdgId.push_back(motherPdgId);
      fTausGrandMotherPdgId.push_back(grandMotherPdgId);
      fTausDaughterPdgId.push_back(daughterPdgId);
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

    fTausPdgId.clear();
    fTausMotherPdgId.clear();
    fTausGrandMotherPdgId.clear();
    fTausDaughterPdgId.clear();
  }
}
