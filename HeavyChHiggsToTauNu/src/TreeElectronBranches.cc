#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeElectronBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeElectronBranches::TreeElectronBranches(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, const std::string& prefix):
    fElectronSrc(iConfig.getParameter<edm::InputTag>("electronSrc")),
    fConversionSrc(iConfig.getParameter<edm::InputTag>("electronConversionSrc")),
    fVertexSrc(vertexSrc),
    fBeamspotSrc(iConfig.getParameter<edm::InputTag>("beamspotSrc")),
    fRhoSrc(iConfig.getParameter<edm::InputTag>("electronRhoSrc")),
    fPrefix(prefix+"_"),
    fElectronsGenMatch(fPrefix+"genmatch")
  {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("electronFunctions");
    std::vector<std::string> names = pset.getParameterNames();
    fElectronsFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fElectronsFunctions.push_back(ElectronFunctionBranch(fPrefix+"f_"+names[i], pset.getParameter<std::string>(names[i])));
    }
  }
  TreeElectronBranches::~TreeElectronBranches() {}


  void TreeElectronBranches::book(TTree *tree) {
    tree->Branch((fPrefix+"p4").c_str(), &fElectrons);
    for(size_t i=0; i<fElectronsFunctions.size(); ++i) {
      fElectronsFunctions[i].book(tree);
    }
    fElectronsGenMatch.book(tree);
    tree->Branch((fPrefix+"hasGsfTrack").c_str(), &fElectronsHasGsfTrack);
    tree->Branch((fPrefix+"hasSuperCluster").c_str(), &fElectronsHasSuperCluster);
    tree->Branch((fPrefix+"cutBasedIdVeto").c_str(), &fElectronsCutBasedIdVeto);
    tree->Branch((fPrefix+"cutBasedIdLoose").c_str(), &fElectronsCutBasedIdLoose);
    tree->Branch((fPrefix+"cutBasedIdMedium").c_str(), &fElectronsCutBasedIdMedium);
    tree->Branch((fPrefix+"cutBasedIdTight").c_str(), &fElectronsCutBasedIdTight);
  }

  size_t TreeElectronBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<pat::Electron> > helectrons;
    iEvent.getByLabel(fElectronSrc, helectrons);
    edm::Handle<reco::ConversionCollection> hConversion;
    iEvent.getByLabel(fConversionSrc, hConversion);
    edm::Handle<reco::BeamSpot> hBeamspot;
    iEvent.getByLabel(fBeamspotSrc, hBeamspot);
    edm::Handle<reco::VertexCollection> hVertex;
    iEvent.getByLabel(fVertexSrc, hVertex);
    edm::Handle<double> hRho;
    iEvent.getByLabel(fRhoSrc, hRho);

    setValues(*helectrons, hConversion, hBeamspot, hVertex, hRho);



    return helectrons->size();
  }

  size_t TreeElectronBranches::setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles) {
    edm::Handle<edm::View<pat::Electron> > helectrons;
    iEvent.getByLabel(fElectronSrc, helectrons);
    edm::Handle<reco::ConversionCollection> hConversion;
    iEvent.getByLabel(fConversionSrc, hConversion);
    edm::Handle<reco::BeamSpot> hBeamspot;
    iEvent.getByLabel(fBeamspotSrc, hBeamspot);
    edm::Handle<reco::VertexCollection> hVertex;
    iEvent.getByLabel(fVertexSrc, hVertex);
    edm::Handle<double> hRho;
    iEvent.getByLabel(fRhoSrc, hRho);

    setValues(*helectrons, hConversion, hBeamspot, hVertex, hRho);

    for(size_t i=0; i<helectrons->size(); ++i) {
      const pat::Electron& electron = helectrons->at(i);
      const reco::GenParticle *gen = GenParticleTools::findMatching(genParticles.begin(), genParticles.end(), 11, electron, 0.5);
      fElectronsGenMatch.addValue(gen);
    }

    return helectrons->size();
  }

  void TreeElectronBranches::setValues(const edm::View<pat::Electron>& electrons,
                                       edm::Handle<reco::ConversionCollection>& hConversion,
                                       edm::Handle<reco::BeamSpot>& hBeamspot,
                                       edm::Handle<reco::VertexCollection>& hVertex,
                                       edm::Handle<double>& hRho) {
    for(size_t i=0; i<electrons.size(); ++i) {
      fElectrons.push_back(electrons[i].p4());
      fElectronsHasGsfTrack.push_back(electrons[i].gsfTrack().isNonnull());
      fElectronsHasSuperCluster.push_back(electrons[i].superCluster().isNonnull());
      fElectronsCutBasedIdVeto.push_back(EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::VETO, electrons[i], hConversion, *hBeamspot, hVertex,
                                                                     electrons[i].chargedHadronIso(), electrons[i].photonIso(), electrons[i].neutralHadronIso(),
                                                                     *hRho));
      fElectronsCutBasedIdLoose.push_back(EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::LOOSE, electrons[i], hConversion, *hBeamspot, hVertex,
                                                                      electrons[i].chargedHadronIso(), electrons[i].photonIso(), electrons[i].neutralHadronIso(),
                                                                      *hRho));
      fElectronsCutBasedIdMedium.push_back(EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::MEDIUM, electrons[i], hConversion, *hBeamspot, hVertex,
                                                                       electrons[i].chargedHadronIso(), electrons[i].photonIso(), electrons[i].neutralHadronIso(),
                                                                       *hRho));
      fElectronsCutBasedIdTight.push_back(EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::TIGHT, electrons[i], hConversion, *hBeamspot, hVertex,
                                                                      electrons[i].chargedHadronIso(), electrons[i].photonIso(), electrons[i].neutralHadronIso(),
                                                                      *hRho));
    }

    for(size_t i=0; i<fElectronsFunctions.size(); ++i) {
      fElectronsFunctions[i].setValues(electrons);
    }
  }

  void TreeElectronBranches::reset() {
    fElectrons.clear();
    for(size_t i=0; i<fElectronsFunctions.size(); ++i)
      fElectronsFunctions[i].reset();
    fElectronsGenMatch.reset();
    fElectronsHasGsfTrack.clear();
    fElectronsHasSuperCluster.clear();
    fElectronsCutBasedIdVeto.clear();
    fElectronsCutBasedIdLoose.clear();
    fElectronsCutBasedIdMedium.clear();
    fElectronsCutBasedIdTight.clear();
  }
}
