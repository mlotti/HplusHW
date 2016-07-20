// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_TauGenerated_h
#define DataFormat_TauGenerated_h

#include "DataFormat/interface/Particle.h"
#include <string>
#include <vector>
#include <functional>

class TauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit TauGeneratedCollection(const std::string& prefix="Taus")
  : ParticleCollection(prefix),
    fMCVisibleTau(prefix),
    fmatchingJet(prefix)
  {
    fMCVisibleTau.setEnergySystematicsVariation("_MCVisibleTau");
    fmatchingJet.setEnergySystematicsVariation("_matchingJet");
  }
  ~TauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIsolationDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("byCombinedIsolationDeltaBetaCorrRaw3Hits"), std::string("byIsolationMVArun2v1DBdR03oldDMwLTraw"), std::string("byIsolationMVArun2v1DBnewDMwLTraw"), std::string("byIsolationMVArun2v1DBoldDMwLTraw"), std::string("byIsolationMVArun2v1PWdR03oldDMwLTraw"), std::string("byIsolationMVArun2v1PWnewDMwLTraw"), std::string("byIsolationMVArun2v1PWoldDMwLTraw"), std::string("byLooseCombinedIsolationDeltaBetaCorr3Hits"), std::string("byLooseIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byLooseIsolationMVArun2v1DBnewDMwLT"), std::string("byLooseIsolationMVArun2v1DBoldDMwLT"), std::string("byLooseIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byLooseIsolationMVArun2v1PWnewDMwLT"), std::string("byLooseIsolationMVArun2v1PWoldDMwLT"), std::string("byMediumCombinedIsolationDeltaBetaCorr3Hits"), std::string("byMediumIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byMediumIsolationMVArun2v1DBnewDMwLT"), std::string("byMediumIsolationMVArun2v1DBoldDMwLT"), std::string("byMediumIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byMediumIsolationMVArun2v1PWnewDMwLT"), std::string("byMediumIsolationMVArun2v1PWoldDMwLT"), std::string("byTightCombinedIsolationDeltaBetaCorr3Hits"), std::string("byTightIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byTightIsolationMVArun2v1DBnewDMwLT"), std::string("byTightIsolationMVArun2v1DBoldDMwLT"), std::string("byTightIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byTightIsolationMVArun2v1PWnewDMwLT"), std::string("byTightIsolationMVArun2v1PWoldDMwLT"), std::string("byVLooseIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byVLooseIsolationMVArun2v1DBnewDMwLT"), std::string("byVLooseIsolationMVArun2v1DBoldDMwLT"), std::string("byVLooseIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byVLooseIsolationMVArun2v1PWnewDMwLT"), std::string("byVLooseIsolationMVArun2v1PWoldDMwLT"), std::string("byVTightIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byVTightIsolationMVArun2v1DBnewDMwLT"), std::string("byVTightIsolationMVArun2v1DBoldDMwLT"), std::string("byVTightIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byVTightIsolationMVArun2v1PWnewDMwLT"), std::string("byVTightIsolationMVArun2v1PWoldDMwLT"), std::string("byVVTightIsolationMVArun2v1DBdR03oldDMwLT"), std::string("byVVTightIsolationMVArun2v1DBnewDMwLT"), std::string("byVVTightIsolationMVArun2v1DBoldDMwLT"), std::string("byVVTightIsolationMVArun2v1PWdR03oldDMwLT"), std::string("byVVTightIsolationMVArun2v1PWnewDMwLT"), std::string("byVVTightIsolationMVArun2v1PWoldDMwLT")};
    return n;
  }
  std::vector<std::string> getAgainstMuonDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("againstMuonLoose3"), std::string("againstMuonTight3")};
    return n;
  }
  std::vector<std::string> getAgainstElectronDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("againstElectronLooseMVA6"), std::string("againstElectronMVA6Raw"), std::string("againstElectronMVA6category"), std::string("againstElectronMediumMVA6"), std::string("againstElectronTightMVA6"), std::string("againstElectronVLooseMVA6"), std::string("againstElectronVTightMVA6")};
    return n;
  }

  const ParticleCollection<double>* getMCVisibleTauCollection() const { return &fMCVisibleTau; }
  const ParticleCollection<double>* getmatchingJetCollection() const { return &fmatchingJet; }
protected:
  ParticleCollection<double> fMCVisibleTau;
  ParticleCollection<double> fmatchingJet;

protected:
  const Branch<std::vector<bool>> *fAgainstElectronLooseMVA6;
  const Branch<std::vector<bool>> *fAgainstElectronMVA6Raw;
  const Branch<std::vector<bool>> *fAgainstElectronMVA6category;
  const Branch<std::vector<bool>> *fAgainstElectronMediumMVA6;
  const Branch<std::vector<bool>> *fAgainstElectronTightMVA6;
  const Branch<std::vector<bool>> *fAgainstElectronVLooseMVA6;
  const Branch<std::vector<bool>> *fAgainstElectronVTightMVA6;
  const Branch<std::vector<bool>> *fAgainstMuonLoose3;
  const Branch<std::vector<bool>> *fAgainstMuonTight3;
  const Branch<std::vector<bool>> *fByCombinedIsolationDeltaBetaCorrRaw3Hits;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1DBdR03oldDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1DBnewDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1DBoldDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1PWdR03oldDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1PWnewDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVArun2v1PWoldDMwLTraw;
  const Branch<std::vector<bool>> *fByLooseCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fByMediumCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fByPhotonPtSumOutsideSignalCone;
  const Branch<std::vector<bool>> *fByTightCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1DBdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1DBnewDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1DBoldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1PWdR03oldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1PWnewDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVArun2v1PWoldDMwLT;
  const Branch<std::vector<bool>> *fChargedIsoPtSum;
  const Branch<std::vector<bool>> *fChargedIsoPtSumdR03;
  const Branch<std::vector<bool>> *fDecayModeFinding;
  const Branch<std::vector<bool>> *fDecayModeFindingNewDMs;
  const Branch<std::vector<bool>> *fFootprintCorrection;
  const Branch<std::vector<bool>> *fFootprintCorrectiondR03;
  const Branch<std::vector<bool>> *fNeutralIsoPtSum;
  const Branch<std::vector<bool>> *fNeutralIsoPtSumWeight;
  const Branch<std::vector<bool>> *fNeutralIsoPtSumWeightdR03;
  const Branch<std::vector<bool>> *fNeutralIsoPtSumdR03;
  const Branch<std::vector<bool>> *fPhotonPtSumOutsideSignalCone;
  const Branch<std::vector<bool>> *fPhotonPtSumOutsideSignalConedR03;
  const Branch<std::vector<bool>> *fPuCorrPtSum;
  const Branch<std::vector<double>> *fLChTrkEta;
  const Branch<std::vector<double>> *fLChTrkPt;
  const Branch<std::vector<double>> *fLNeutrTrkEta;
  const Branch<std::vector<double>> *fLNeutrTrkPt;
  const Branch<std::vector<float>> *fIPxy;
  const Branch<std::vector<float>> *fIPxySignif;
  const Branch<std::vector<short>> *fCharge;
  const Branch<std::vector<short>> *fDecayMode;
  const Branch<std::vector<short>> *fMcNPizero;
  const Branch<std::vector<short>> *fMcNProngs;
  const Branch<std::vector<short>> *fNProngs;
  const Branch<std::vector<short>> *fPdgOrigin;
};


template <typename Coll>
class TauGenerated: public Particle<Coll> {
public:
  TauGenerated() {}
  TauGenerated(const Coll* coll, size_t index)
  : Particle<Coll>(coll, index),
    fMCVisibleTau(coll->getMCVisibleTauCollection(), index),
    fmatchingJet(coll->getmatchingJetCollection(), index)
  {}
  ~TauGenerated() {}

  std::vector<std::function<bool()>> getIsolationDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->byCombinedIsolationDeltaBetaCorrRaw3Hits(); },
      [&](){ return this->byIsolationMVArun2v1DBdR03oldDMwLTraw(); },
      [&](){ return this->byIsolationMVArun2v1DBnewDMwLTraw(); },
      [&](){ return this->byIsolationMVArun2v1DBoldDMwLTraw(); },
      [&](){ return this->byIsolationMVArun2v1PWdR03oldDMwLTraw(); },
      [&](){ return this->byIsolationMVArun2v1PWnewDMwLTraw(); },
      [&](){ return this->byIsolationMVArun2v1PWoldDMwLTraw(); },
      [&](){ return this->byLooseCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byLooseIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byLooseIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byLooseIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byLooseIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byLooseIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byLooseIsolationMVArun2v1PWoldDMwLT(); },
      [&](){ return this->byMediumCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byMediumIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byMediumIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byMediumIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byMediumIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byMediumIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byMediumIsolationMVArun2v1PWoldDMwLT(); },
      [&](){ return this->byTightCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byTightIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byTightIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byTightIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byTightIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byTightIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byTightIsolationMVArun2v1PWoldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byVLooseIsolationMVArun2v1PWoldDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byVTightIsolationMVArun2v1PWoldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1DBdR03oldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1DBnewDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1DBoldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1PWdR03oldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1PWnewDMwLT(); },
      [&](){ return this->byVVTightIsolationMVArun2v1PWoldDMwLT(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstMuonDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->againstMuonLoose3(); },
      [&](){ return this->againstMuonTight3(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstElectronDiscriminatorValues() const {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->againstElectronLooseMVA6(); },
      [&](){ return this->againstElectronMVA6Raw(); },
      [&](){ return this->againstElectronMVA6category(); },
      [&](){ return this->againstElectronMediumMVA6(); },
      [&](){ return this->againstElectronTightMVA6(); },
      [&](){ return this->againstElectronVLooseMVA6(); },
      [&](){ return this->againstElectronVTightMVA6(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCVisibleTau() const { return &fMCVisibleTau; }
  const Particle<ParticleCollection<double>>* matchingJet() const { return &fmatchingJet; }

  bool againstElectronLooseMVA6() const { return this->fCollection->fAgainstElectronLooseMVA6->value()[this->index()]; }
  bool againstElectronMVA6Raw() const { return this->fCollection->fAgainstElectronMVA6Raw->value()[this->index()]; }
  bool againstElectronMVA6category() const { return this->fCollection->fAgainstElectronMVA6category->value()[this->index()]; }
  bool againstElectronMediumMVA6() const { return this->fCollection->fAgainstElectronMediumMVA6->value()[this->index()]; }
  bool againstElectronTightMVA6() const { return this->fCollection->fAgainstElectronTightMVA6->value()[this->index()]; }
  bool againstElectronVLooseMVA6() const { return this->fCollection->fAgainstElectronVLooseMVA6->value()[this->index()]; }
  bool againstElectronVTightMVA6() const { return this->fCollection->fAgainstElectronVTightMVA6->value()[this->index()]; }
  bool againstMuonLoose3() const { return this->fCollection->fAgainstMuonLoose3->value()[this->index()]; }
  bool againstMuonTight3() const { return this->fCollection->fAgainstMuonTight3->value()[this->index()]; }
  bool byCombinedIsolationDeltaBetaCorrRaw3Hits() const { return this->fCollection->fByCombinedIsolationDeltaBetaCorrRaw3Hits->value()[this->index()]; }
  bool byIsolationMVArun2v1DBdR03oldDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1DBdR03oldDMwLTraw->value()[this->index()]; }
  bool byIsolationMVArun2v1DBnewDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1DBnewDMwLTraw->value()[this->index()]; }
  bool byIsolationMVArun2v1DBoldDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1DBoldDMwLTraw->value()[this->index()]; }
  bool byIsolationMVArun2v1PWdR03oldDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1PWdR03oldDMwLTraw->value()[this->index()]; }
  bool byIsolationMVArun2v1PWnewDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1PWnewDMwLTraw->value()[this->index()]; }
  bool byIsolationMVArun2v1PWoldDMwLTraw() const { return this->fCollection->fByIsolationMVArun2v1PWoldDMwLTraw->value()[this->index()]; }
  bool byLooseCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByLooseCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByLooseIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool byMediumCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByMediumCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByMediumIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool byPhotonPtSumOutsideSignalCone() const { return this->fCollection->fByPhotonPtSumOutsideSignalCone->value()[this->index()]; }
  bool byTightCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByTightCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byTightIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byTightIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byTightIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byTightIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byTightIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byTightIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByTightIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByVLooseIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByVTightIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1DBdR03oldDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1DBdR03oldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1DBnewDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1DBnewDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1DBoldDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1DBoldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1PWdR03oldDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1PWdR03oldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1PWnewDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1PWnewDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVArun2v1PWoldDMwLT() const { return this->fCollection->fByVVTightIsolationMVArun2v1PWoldDMwLT->value()[this->index()]; }
  bool chargedIsoPtSum() const { return this->fCollection->fChargedIsoPtSum->value()[this->index()]; }
  bool chargedIsoPtSumdR03() const { return this->fCollection->fChargedIsoPtSumdR03->value()[this->index()]; }
  bool decayModeFinding() const { return this->fCollection->fDecayModeFinding->value()[this->index()]; }
  bool decayModeFindingNewDMs() const { return this->fCollection->fDecayModeFindingNewDMs->value()[this->index()]; }
  bool footprintCorrection() const { return this->fCollection->fFootprintCorrection->value()[this->index()]; }
  bool footprintCorrectiondR03() const { return this->fCollection->fFootprintCorrectiondR03->value()[this->index()]; }
  bool neutralIsoPtSum() const { return this->fCollection->fNeutralIsoPtSum->value()[this->index()]; }
  bool neutralIsoPtSumWeight() const { return this->fCollection->fNeutralIsoPtSumWeight->value()[this->index()]; }
  bool neutralIsoPtSumWeightdR03() const { return this->fCollection->fNeutralIsoPtSumWeightdR03->value()[this->index()]; }
  bool neutralIsoPtSumdR03() const { return this->fCollection->fNeutralIsoPtSumdR03->value()[this->index()]; }
  bool photonPtSumOutsideSignalCone() const { return this->fCollection->fPhotonPtSumOutsideSignalCone->value()[this->index()]; }
  bool photonPtSumOutsideSignalConedR03() const { return this->fCollection->fPhotonPtSumOutsideSignalConedR03->value()[this->index()]; }
  bool puCorrPtSum() const { return this->fCollection->fPuCorrPtSum->value()[this->index()]; }
  double lChTrkEta() const { return this->fCollection->fLChTrkEta->value()[this->index()]; }
  double lChTrkPt() const { return this->fCollection->fLChTrkPt->value()[this->index()]; }
  double lNeutrTrkEta() const { return this->fCollection->fLNeutrTrkEta->value()[this->index()]; }
  double lNeutrTrkPt() const { return this->fCollection->fLNeutrTrkPt->value()[this->index()]; }
  float IPxy() const { return this->fCollection->fIPxy->value()[this->index()]; }
  float IPxySignif() const { return this->fCollection->fIPxySignif->value()[this->index()]; }
  short charge() const { return this->fCollection->fCharge->value()[this->index()]; }
  short decayMode() const { return this->fCollection->fDecayMode->value()[this->index()]; }
  short mcNPizero() const { return this->fCollection->fMcNPizero->value()[this->index()]; }
  short mcNProngs() const { return this->fCollection->fMcNProngs->value()[this->index()]; }
  short nProngs() const { return this->fCollection->fNProngs->value()[this->index()]; }
  short pdgOrigin() const { return this->fCollection->fPdgOrigin->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCVisibleTau;
  Particle<ParticleCollection<double>> fmatchingJet;

};

#endif
