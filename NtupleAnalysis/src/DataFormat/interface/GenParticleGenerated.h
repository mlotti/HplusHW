// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"
#include <vector>

class GenParticleGeneratedCollection {
public:
  using float_type = double;
  explicit GenParticleGeneratedCollection(const std::string& prefix="genParticles")
  : fGenElectron(prefix),
    fGenHplus(prefix),
    fGenHplusNeutrinos(prefix),
    fGenMuon(prefix),
    fGenNeutrinos(prefix),
    fGenTau(prefix),
    fGenTauNeutrinos(prefix),
    fGenTop(prefix),
    fGenTopBNeutrinos(prefix),
    fGenTopBQuark(prefix),
    fGenVisibleTau(prefix),
    fGenW(prefix),
    fGenWNeutrinos(prefix)
  {
    fGenElectron.setEnergySystematicsVariation("_GenElectron");
    fGenHplus.setEnergySystematicsVariation("_GenHplus");
    fGenHplusNeutrinos.setEnergySystematicsVariation("_GenHplusNeutrinos");
    fGenMuon.setEnergySystematicsVariation("_GenMuon");
    fGenNeutrinos.setEnergySystematicsVariation("_GenNeutrinos");
    fGenTau.setEnergySystematicsVariation("_GenTau");
    fGenTauNeutrinos.setEnergySystematicsVariation("_GenTauNeutrinos");
    fGenTop.setEnergySystematicsVariation("_GenTop");
    fGenTopBNeutrinos.setEnergySystematicsVariation("_GenTopBNeutrinos");
    fGenTopBQuark.setEnergySystematicsVariation("_GenTopBQuark");
    fGenVisibleTau.setEnergySystematicsVariation("_GenVisibleTau");
    fGenW.setEnergySystematicsVariation("_GenW");
    fGenWNeutrinos.setEnergySystematicsVariation("_GenWNeutrinos");
  }
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  const std::vector<Particle<ParticleCollection<float_type>>> getGenElectronCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenHplusCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenHplusNeutrinosCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenMuonCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenNeutrinosCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenTauCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenTauNeutrinosCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenTopCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenTopBNeutrinosCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenTopBQuarkCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenVisibleTauCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenWCollection() const;
  const std::vector<Particle<ParticleCollection<float_type>>> getGenWNeutrinosCollection() const;
protected:
  ParticleCollection<float_type> fGenElectron;
  ParticleCollection<float_type> fGenHplus;
  ParticleCollection<float_type> fGenHplusNeutrinos;
  ParticleCollection<float_type> fGenMuon;
  ParticleCollection<float_type> fGenNeutrinos;
  ParticleCollection<float_type> fGenTau;
  ParticleCollection<float_type> fGenTauNeutrinos;
  ParticleCollection<float_type> fGenTop;
  ParticleCollection<float_type> fGenTopBNeutrinos;
  ParticleCollection<float_type> fGenTopBQuark;
  ParticleCollection<float_type> fGenVisibleTau;
  ParticleCollection<float_type> fGenW;
  ParticleCollection<float_type> fGenWNeutrinos;


public:
  const Short_t getGenTauAssociatedWithHpm() const { return fGenTauAssociatedWithHpm->value(); }
  const std::vector<bool> getGenTauDecaysToElectron() const { return fGenTauDecaysToElectron->value(); }
  const std::vector<bool> getGenTauDecaysToMuon() const { return fGenTauDecaysToMuon->value(); }
  const std::vector<bool> getGenTopBJetContainsLeptons() const { return fGenTopBJetContainsLeptons->value(); }
  const std::vector<double> getGenTauRtau() const { return fGenTauRtau->value(); }
  const std::vector<double> getGenTauSpinEffects() const { return fGenTauSpinEffects->value(); }
  const std::vector<short> getGenTauMother() const { return fGenTauMother->value(); }
  const std::vector<short> getGenTauNpi0() const { return fGenTauNpi0->value(); }
  const std::vector<short> getGenTauProngs() const { return fGenTauProngs->value(); }
  const std::vector<short> getGenTopDecayMode() const { return fGenTopDecayMode->value(); }
  const std::vector<short> getGenWDecayMode() const { return fGenWDecayMode->value(); }

protected:
  const Branch<Short_t> *fGenTauAssociatedWithHpm;
  const Branch<std::vector<bool>> *fGenTauDecaysToElectron;
  const Branch<std::vector<bool>> *fGenTauDecaysToMuon;
  const Branch<std::vector<bool>> *fGenTopBJetContainsLeptons;
  const Branch<std::vector<double>> *fGenTauRtau;
  const Branch<std::vector<double>> *fGenTauSpinEffects;
  const Branch<std::vector<short>> *fGenTauMother;
  const Branch<std::vector<short>> *fGenTauNpi0;
  const Branch<std::vector<short>> *fGenTauProngs;
  const Branch<std::vector<short>> *fGenTopDecayMode;
  const Branch<std::vector<short>> *fGenWDecayMode;
};

#endif
