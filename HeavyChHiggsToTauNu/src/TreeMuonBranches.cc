#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeMuonBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeMuonBranches::TreeMuonBranches(const edm::ParameterSet& iConfig, const std::string& prefix):
    fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc")),
    fMuonCorrectedSrc(iConfig.getParameter<edm::InputTag>("muonCorrectedSrc")),
    fPrefix(prefix+"_"),
    fMuonsGenMatch(fPrefix+"genmatch"),
    fMuonCorrectedEnabled(iConfig.getParameter<bool>("muonCorrectedEnabled")),
    fTunePEnabled(iConfig.getParameter<bool>("muonTunePEnabled"))
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
    if(fMuonCorrectedEnabled) {
      tree->Branch((fPrefix+"correctedP4").c_str(), &fMuonsCorrected);
    }
    if(fTunePEnabled) {
      tree->Branch((fPrefix+"tunePP3").c_str(), &fMuonsTuneP);
      tree->Branch((fPrefix+"tunePPtError").c_str(), &fMuonsTunePPtError);
    }
    tree->Branch((fPrefix+"charge").c_str(), &fMuonsCharge);
    tree->Branch((fPrefix+"globalTrack_normalizedChi2").c_str(), &fMuonsNormChi2);
    for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
      fMuonsFunctions[i].book(tree);
    }
    fMuonsGenMatch.book(tree);
  }

  size_t TreeMuonBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fMuonSrc, hmuons);
    setValues(hmuons->ptrVector());

    if(fMuonCorrectedEnabled) {
      edm::Handle<edm::View<pat::Muon> > hmuonscorr;
      iEvent.getByLabel(fMuonCorrectedSrc, hmuonscorr);
      setValuesCorrected(hmuonscorr->ptrVector());
      if(hmuons->size() != hmuonscorr->size())
        throw cms::Exception("Assert") << "Muon (src " << fMuonSrc.encode() << ") size " << hmuons->size()
                                       << " != corrected muon (src " << fMuonCorrectedSrc.encode() << ") size " << hmuonscorr->size()
                                       << std::endl;
    }

    return hmuons->size();
  }

  

  size_t TreeMuonBranches::setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fMuonSrc, hmuons);
    setValues(hmuons->ptrVector());

    for(size_t i=0; i<hmuons->size(); ++i) {
      const pat::Muon& muon = hmuons->at(i);
      const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 13, muon, 0.5);
      fMuonsGenMatch.addValue(gen);
    }

    if(fMuonCorrectedEnabled) {
      edm::Handle<edm::View<pat::Muon> > hmuonscorr;
      iEvent.getByLabel(fMuonCorrectedSrc, hmuonscorr);
      setValuesCorrected(hmuonscorr->ptrVector());
      if(hmuons->size() != hmuonscorr->size()) 
        throw cms::Exception("Assert") << "Muon (src " << fMuonSrc.encode() << ") size " << hmuons->size()
                                       << " != corrected muon (src " << fMuonCorrectedSrc.encode() << ") size " << hmuonscorr->size()
                                       << std::endl;
    }

    return hmuons->size();
  }

  void TreeMuonBranches::setValues(const edm::PtrVector<pat::Muon>& muons) {
    for(size_t i=0; i<muons.size(); ++i) {
      fMuons.push_back(muons[i]->p4());
      fMuonsCharge.push_back(muons[i]->charge());
      fMuonsNormChi2.push_back(muons[i]->globalTrack()->normalizedChi2());

      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#New_Version_recommended
      if(fTunePEnabled) {
        throw cms::Exception("NotYetImplemented") << "TuneP needs update of DataFormats/MuonReco, which is not yet integrated to the common checkoutTags.sh in " << __FILE__ << ":" << __LINE__;
        /*
        reco::TrackRef cktTrack = (muon::tevOptimized(*(muons[i]), 200, 30., 0., 0.25));
        fMuonsTuneP.push_back(cktTrack->momentum());
        fMuonsTunePPtError.push_back(cktTrack->ptError());
        */
      }
    }

    for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
      fMuonsFunctions[i].setValues(muons);
    }
  }

  void TreeMuonBranches::setValuesCorrected(const edm::PtrVector<pat::Muon>& muons) {
    for(size_t i=0; i<muons.size(); ++i) {
      fMuonsCorrected.push_back(muons[i]->p4());
    }
  }

  void TreeMuonBranches::reset() {
    fMuons.clear();
    fMuonsCorrected.clear();
    fMuonsTuneP.clear();
    fMuonsTunePPtError.clear();
    fMuonsCharge.clear();
    fMuonsNormChi2.clear();
    for(size_t i=0; i<fMuonsFunctions.size(); ++i)
      fMuonsFunctions[i].reset();
    fMuonsGenMatch.reset();
  }
}
