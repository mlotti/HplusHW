#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeMuonBranches::TreeMuonBranches(const edm::ParameterSet& iConfig, const std::string& prefix):
    fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc")),
    fPrefix(prefix+"_")
  {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("muonFunctions");
    std::vector<std::string> names = pset.getParameterNames();
    fMuonsFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fMuonsFunctions.push_back(MuonFunctionBranch(fPrefix+"f_"+names[i], pset.getParameter<std::string>(names[i])));
    }
  }
  TreeMuonBranches::~TreeMuonBranches() {}


  void TreeMuonBranches::book(TTree *tree) {
    tree->Branch((fPrefix+"p4").c_str(), &fMuons);
    for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
      fMuonsFunctions[i].book(tree);
    }
    tree->Branch((fPrefix+"pdgid").c_str(), &fMuonsPdgId);
    tree->Branch((fPrefix+"mother_pdgid").c_str(), &fMuonsMotherPdgId);
    tree->Branch((fPrefix+"grandmother_pdgid").c_str(), &fMuonsGrandMotherPdgId);
  }

  size_t TreeMuonBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fMuonSrc, hmuons);
    setValues(*hmuons);

    return hmuons->size();
  }

  size_t TreeMuonBranches::setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fMuonSrc, hmuons);
    setValues(*hmuons);

    for(size_t i=0; i<hmuons->size(); ++i) {
      const pat::Muon& muon = hmuons->at(i);
      const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 13, muon, 0.5);

      int pdgId = 0;
      int motherPdgId = 0;
      int grandMotherPdgId = 0;
      if(gen) {
        pdgId = gen->pdgId();
        const reco::GenParticle *mother = GenParticleTools::findMother(gen);
        if(mother) {
          motherPdgId = mother->pdgId();
          const reco::GenParticle *grandMother = GenParticleTools::findMother(mother);
          if(grandMother)
            grandMotherPdgId = grandMother->pdgId();
        }
      }

      fMuonsPdgId.push_back(pdgId);
      fMuonsMotherPdgId.push_back(motherPdgId);
      fMuonsGrandMotherPdgId.push_back(grandMotherPdgId);
    }

    return hmuons->size();
  }

  void TreeMuonBranches::setValues(const edm::View<pat::Muon>& muons) {
    for(size_t i=0; i<muons.size(); ++i) {
      fMuons.push_back(muons[i].p4());
    }

    for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
      fMuonsFunctions[i].setValues(muons);
    }
  }

  void TreeMuonBranches::reset() {
    fMuons.clear();
    for(size_t i=0; i<fMuonsFunctions.size(); ++i)
      fMuonsFunctions[i].reset();
    fMuonsPdgId.clear();
    fMuonsMotherPdgId.clear();
    fMuonsGrandMotherPdgId.clear();
  }
}
