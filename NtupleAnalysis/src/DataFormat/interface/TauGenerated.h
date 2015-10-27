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
    static std::vector<std::string> n = { std::string("byCombinedIsolationDeltaBetaCorrRaw3Hits"), std::string("byIsolationMVA3newDMwLTraw"), std::string("byIsolationMVA3oldDMwLTraw"), std::string("byLooseCombinedIsolationDeltaBetaCorr3Hits"), std::string("byLooseIsolationMVA3newDMwLT"), std::string("byLooseIsolationMVA3oldDMwLT"), std::string("byMediumCombinedIsolationDeltaBetaCorr3Hits"), std::string("byMediumIsolationMVA3newDMwLT"), std::string("byMediumIsolationMVA3oldDMwLT"), std::string("byTightCombinedIsolationDeltaBetaCorr3Hits"), std::string("byTightIsolationMVA3newDMwLT"), std::string("byTightIsolationMVA3oldDMwLT"), std::string("byVLooseIsolationMVA3newDMwLT"), std::string("byVLooseIsolationMVA3oldDMwLT"), std::string("byVTightIsolationMVA3newDMwLT"), std::string("byVTightIsolationMVA3oldDMwLT"), std::string("byVVTightIsolationMVA3newDMwLT"), std::string("byVVTightIsolationMVA3oldDMwLT")};
    return n;
  }
  std::vector<std::string> getAgainstMuonDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("againstMuonLoose3"), std::string("againstMuonTight3")};
    return n;
  }
  std::vector<std::string> getAgainstElectronDiscriminatorNames() const {
    static std::vector<std::string> n = { std::string("againstElectronLooseMVA5"), std::string("againstElectronMVA5category"), std::string("againstElectronMediumMVA5"), std::string("againstElectronTightMVA5"), std::string("againstElectronVLooseMVA5"), std::string("againstElectronVTightMVA5")};
    return n;
  }

  const ParticleCollection<double>* getMCVisibleTauCollection() const { return &fMCVisibleTau; }
  const ParticleCollection<double>* getmatchingJetCollection() const { return &fmatchingJet; }
protected:
  ParticleCollection<double> fMCVisibleTau;
  ParticleCollection<double> fmatchingJet;

protected:
  const Branch<std::vector<bool>> *fTrgMatch_LooseIsoPFTau50_Trk30_eta2p1;
  const Branch<std::vector<bool>> *fAgainstElectronLooseMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronMVA5category;
  const Branch<std::vector<bool>> *fAgainstElectronMediumMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronTightMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronVLooseMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronVTightMVA5;
  const Branch<std::vector<bool>> *fAgainstMuonLoose3;
  const Branch<std::vector<bool>> *fAgainstMuonTight3;
  const Branch<std::vector<bool>> *fByCombinedIsolationDeltaBetaCorrRaw3Hits;
  const Branch<std::vector<bool>> *fByIsolationMVA3newDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVA3oldDMwLTraw;
  const Branch<std::vector<bool>> *fByLooseCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByMediumCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByTightCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fChargedIsoPtSum;
  const Branch<std::vector<short>> *fDecayMode;
  const Branch<std::vector<bool>> *fDecayModeFinding;
  const Branch<std::vector<bool>> *fDecayModeFindingNewDMs;
  const Branch<std::vector<bool>> *fNeutralIsoPtSum;
  const Branch<std::vector<bool>> *fPuCorrPtSum;
  const Branch<std::vector<double>> *fLChTrkEta;
  const Branch<std::vector<double>> *fLChTrkPt;
  const Branch<std::vector<double>> *fLNeutrTrkEta;
  const Branch<std::vector<double>> *fLNeutrTrkPt;
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
      [&](){ return this->byIsolationMVA3newDMwLTraw(); },
      [&](){ return this->byIsolationMVA3oldDMwLTraw(); },
      [&](){ return this->byLooseCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byLooseIsolationMVA3newDMwLT(); },
      [&](){ return this->byLooseIsolationMVA3oldDMwLT(); },
      [&](){ return this->byMediumCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byMediumIsolationMVA3newDMwLT(); },
      [&](){ return this->byMediumIsolationMVA3oldDMwLT(); },
      [&](){ return this->byTightCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byTightIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVA3newDMwLT(); },
      [&](){ return this->byVLooseIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byVTightIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byVVTightIsolationMVA3oldDMwLT(); }
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
      [&](){ return this->againstElectronLooseMVA5(); },
      [&](){ return this->againstElectronMVA5category(); },
      [&](){ return this->againstElectronMediumMVA5(); },
      [&](){ return this->againstElectronTightMVA5(); },
      [&](){ return this->againstElectronVLooseMVA5(); },
      [&](){ return this->againstElectronVTightMVA5(); }
    };
    return values;
  }

  const Particle<ParticleCollection<double>>* MCVisibleTau() const { return &fMCVisibleTau; }
  const Particle<ParticleCollection<double>>* matchingJet() const { return &fmatchingJet; }

  bool TrgMatch_LooseIsoPFTau50_Trk30_eta2p1() const { return this->fCollection->fTrgMatch_LooseIsoPFTau50_Trk30_eta2p1->value()[this->index()]; }
  bool againstElectronLooseMVA5() const { return this->fCollection->fAgainstElectronLooseMVA5->value()[this->index()]; }
  bool againstElectronMVA5category() const { return this->fCollection->fAgainstElectronMVA5category->value()[this->index()]; }
  bool againstElectronMediumMVA5() const { return this->fCollection->fAgainstElectronMediumMVA5->value()[this->index()]; }
  bool againstElectronTightMVA5() const { return this->fCollection->fAgainstElectronTightMVA5->value()[this->index()]; }
  bool againstElectronVLooseMVA5() const { return this->fCollection->fAgainstElectronVLooseMVA5->value()[this->index()]; }
  bool againstElectronVTightMVA5() const { return this->fCollection->fAgainstElectronVTightMVA5->value()[this->index()]; }
  bool againstMuonLoose3() const { return this->fCollection->fAgainstMuonLoose3->value()[this->index()]; }
  bool againstMuonTight3() const { return this->fCollection->fAgainstMuonTight3->value()[this->index()]; }
  bool byCombinedIsolationDeltaBetaCorrRaw3Hits() const { return this->fCollection->fByCombinedIsolationDeltaBetaCorrRaw3Hits->value()[this->index()]; }
  bool byIsolationMVA3newDMwLTraw() const { return this->fCollection->fByIsolationMVA3newDMwLTraw->value()[this->index()]; }
  bool byIsolationMVA3oldDMwLTraw() const { return this->fCollection->fByIsolationMVA3oldDMwLTraw->value()[this->index()]; }
  bool byLooseCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByLooseCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byLooseIsolationMVA3newDMwLT() const { return this->fCollection->fByLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVA3oldDMwLT() const { return this->fCollection->fByLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byMediumCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByMediumCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byMediumIsolationMVA3newDMwLT() const { return this->fCollection->fByMediumIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVA3oldDMwLT() const { return this->fCollection->fByMediumIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byTightCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByTightCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byTightIsolationMVA3newDMwLT() const { return this->fCollection->fByTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3newDMwLT() const { return this->fCollection->fByVLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3oldDMwLT() const { return this->fCollection->fByVLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3newDMwLT() const { return this->fCollection->fByVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3newDMwLT() const { return this->fCollection->fByVVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByVVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool chargedIsoPtSum() const { return this->fCollection->fChargedIsoPtSum->value()[this->index()]; }
  short decayMode() const { return this->fCollection->fDecayMode->value()[this->index()]; }
  bool decayModeFinding() const { return this->fCollection->fDecayModeFinding->value()[this->index()]; }
  bool decayModeFindingNewDMs() const { return this->fCollection->fDecayModeFindingNewDMs->value()[this->index()]; }
  bool neutralIsoPtSum() const { return this->fCollection->fNeutralIsoPtSum->value()[this->index()]; }
  bool puCorrPtSum() const { return this->fCollection->fPuCorrPtSum->value()[this->index()]; }
  double lChTrkEta() const { return this->fCollection->fLChTrkEta->value()[this->index()]; }
  double lChTrkPt() const { return this->fCollection->fLChTrkPt->value()[this->index()]; }
  double lNeutrTrkEta() const { return this->fCollection->fLNeutrTrkEta->value()[this->index()]; }
  double lNeutrTrkPt() const { return this->fCollection->fLNeutrTrkPt->value()[this->index()]; }
  short mcNPizero() const { return this->fCollection->fMcNPizero->value()[this->index()]; }
  short mcNProngs() const { return this->fCollection->fMcNProngs->value()[this->index()]; }
  short nProngs() const { return this->fCollection->fNProngs->value()[this->index()]; }
  short pdgOrigin() const { return this->fCollection->fPdgOrigin->value()[this->index()]; }

protected:
  Particle<ParticleCollection<double>> fMCVisibleTau;
  Particle<ParticleCollection<double>> fmatchingJet;

};

#endif
