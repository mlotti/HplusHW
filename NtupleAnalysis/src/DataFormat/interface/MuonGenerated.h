// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_MuonGenerated_h
#define DataFormat_MuonGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class MuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit MuonGeneratedCollection(const std::string& prefix="Muons")
  : ParticleCollection(prefix),
    fMCmuon(prefix)
  {
    fMCmuon.setEnergySystematicsVariation("_MCmuon");
  }
  ~MuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIDDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("muIDLoose"), std::string("muIDMedium"), std::string("muIDTight")};
    return n;
  }

  const ParticleCollection<double>* getMCmuonCollection() const { return &fMCmuon; }
protected:
  ParticleCollection<double> fMCmuon;

protected:
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu16_eta2p1;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu17_eta2p1;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu18;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu19_eta2p1;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu20;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu21_eta2p1;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu22;
  const Branch<std::vector<bool>> *fTrgMatch_IsoMu24;
  const Branch<std::vector<bool>> *fIsGlobalMuon;
  const Branch<std::vector<bool>> *fMuIDLoose;
  const Branch<std::vector<bool>> *fMuIDMedium;
  const Branch<std::vector<bool>> *fMuIDTight;
  const Branch<std::vector<float>> *fRelIsoDeltaBeta;
  const Branch<std::vector<short>> *fCharge;
};


template <typename Coll>
class MuonGenerated: public Particle<Coll> {
public:
  MuonGenerated() {}
  MuonGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCmuon(coll->getMCmuonCollection(), index)
  {}
  ~MuonGenerated() {}

  std::vector<std::function<bool()>> getIDDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->muIDLoose(); },
      [&](){ return this->muIDMedium(); },
      [&](){ return this->muIDTight(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCmuon() const { return &fMCmuon; }

  bool TrgMatch_IsoMu16_eta2p1() const { return this->fCollection->fTrgMatch_IsoMu16_eta2p1->value()[this->index()]; }
  bool TrgMatch_IsoMu17_eta2p1() const { return this->fCollection->fTrgMatch_IsoMu17_eta2p1->value()[this->index()]; }
  bool TrgMatch_IsoMu18() const { return this->fCollection->fTrgMatch_IsoMu18->value()[this->index()]; }
  bool TrgMatch_IsoMu19_eta2p1() const { return this->fCollection->fTrgMatch_IsoMu19_eta2p1->value()[this->index()]; }
  bool TrgMatch_IsoMu20() const { return this->fCollection->fTrgMatch_IsoMu20->value()[this->index()]; }
  bool TrgMatch_IsoMu21_eta2p1() const { return this->fCollection->fTrgMatch_IsoMu21_eta2p1->value()[this->index()]; }
  bool TrgMatch_IsoMu22() const { return this->fCollection->fTrgMatch_IsoMu22->value()[this->index()]; }
  bool TrgMatch_IsoMu24() const { return this->fCollection->fTrgMatch_IsoMu24->value()[this->index()]; }
  bool isGlobalMuon() const { return this->fCollection->fIsGlobalMuon->value()[this->index()]; }
  bool muIDLoose() const { return this->fCollection->fMuIDLoose->value()[this->index()]; }
  bool muIDMedium() const { return this->fCollection->fMuIDMedium->value()[this->index()]; }
  bool muIDTight() const { return this->fCollection->fMuIDTight->value()[this->index()]; }
  float relIsoDeltaBeta() const { return this->fCollection->fRelIsoDeltaBeta->value()[this->index()]; }
  short charge() const { return this->fCollection->fCharge->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCmuon;

};

#endif
