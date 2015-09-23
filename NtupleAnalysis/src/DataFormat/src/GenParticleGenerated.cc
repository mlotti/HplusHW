
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/GenParticleGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenParticleGeneratedCollection::setupBranches(BranchManager& mgr) {
  fGenElectron.setupBranches(mgr);
  fGenHplus.setupBranches(mgr);
  fGenHplusNeutrinos.setupBranches(mgr);
  fGenMuon.setupBranches(mgr);
  fGenNeutrinos.setupBranches(mgr);
  fGenTau.setupBranches(mgr);
  fGenTauNeutrinos.setupBranches(mgr);
  fGenTop.setupBranches(mgr);
  fGenTopBNeutrinos.setupBranches(mgr);
  fGenTopBQuark.setupBranches(mgr);
  fGenVisibleTau.setupBranches(mgr);
  fGenW.setupBranches(mgr);
  fGenWNeutrinos.setupBranches(mgr);

  mgr.book("genParticles_GenTauAssociatedWithHpm", &fGenTauAssociatedWithHpm);
  mgr.book("genParticles_GenTauDecaysToElectron", &fGenTauDecaysToElectron);
  mgr.book("genParticles_GenTauDecaysToMuon", &fGenTauDecaysToMuon);
  mgr.book("genParticles_GenTopBJetContainsLeptons", &fGenTopBJetContainsLeptons);
  mgr.book("genParticles_GenTauRtau", &fGenTauRtau);
  mgr.book("genParticles_GenTauSpinEffects", &fGenTauSpinEffects);
  mgr.book("genParticles_GenTauMother", &fGenTauMother);
  mgr.book("genParticles_GenTauNpi0", &fGenTauNpi0);
  mgr.book("genParticles_GenTauProngs", &fGenTauProngs);
  mgr.book("genParticles_GenTopDecayMode", &fGenTopDecayMode);
  mgr.book("genParticles_GenWDecayMode", &fGenWDecayMode);
}

const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenElectronCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenElectron.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenElectron, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenHplusCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenHplus.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenHplus, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenHplusNeutrinosCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenHplusNeutrinos.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenHplusNeutrinos, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenMuonCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenMuon.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenMuon, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenNeutrinosCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenNeutrinos.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenNeutrinos, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenTauCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenTau.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenTau, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenTauNeutrinosCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenTauNeutrinos.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenTauNeutrinos, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenTopCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenTop.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenTop, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenTopBNeutrinosCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenTopBNeutrinos.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenTopBNeutrinos, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenTopBQuarkCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenTopBQuark.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenTopBQuark, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenVisibleTauCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenVisibleTau.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenVisibleTau, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenWCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenW.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenW, i));
  return v;
}
const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenWNeutrinosCollection() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenWNeutrinos.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenWNeutrinos, i));
  return v;
}

