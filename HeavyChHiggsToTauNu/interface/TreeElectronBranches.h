// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeElectronBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeElectronBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"

#include<vector>
#include<string>

namespace edm {
  class ParameterSet;
  class Event;
}
namespace reco {
  class GenParticle;
  class BreamSpot;
}

class TTree;

namespace HPlus {
  class TreeElectronBranches {
  public:
    TreeElectronBranches(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, const std::string& prefix="electrons");
    ~TreeElectronBranches();

    void book(TTree *tree);
    size_t setValues(const edm::Event& iEvent);
    size_t setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles);
    void reset();

    const edm::InputTag& getInputTag() const { return fElectronSrc; }

  private:
    void setValues(const edm::View<pat::Electron>& electrons,
                   edm::Handle<reco::ConversionCollection>& hConversion,
                   edm::Handle<reco::BeamSpot>& hBeamspot,
                   edm::Handle<reco::VertexCollection>& hVertex,
                   edm::Handle<double>& hRho);

    edm::InputTag fElectronSrc;
    edm::InputTag fConversionSrc;
    edm::InputTag fVertexSrc;
    edm::InputTag fBeamspotSrc;
    edm::InputTag fRhoSrc;
    std::string fPrefix;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Electron> ElectronFunctionBranch;

    std::vector<XYZTLorentzVector> fElectrons;
    std::vector<ElectronFunctionBranch> fElectronsFunctions;
    TreeGenParticleBranches fElectronsGenMatch;
    std::vector<bool> fElectronsHasGsfTrack;
    std::vector<bool> fElectronsHasSuperCluster;
    std::vector<bool> fElectronsCutBasedIdVeto;
    std::vector<bool> fElectronsCutBasedIdLoose;
    std::vector<bool> fElectronsCutBasedIdMedium;
    std::vector<bool> fElectronsCutBasedIdTight;
  };
}

#endif
