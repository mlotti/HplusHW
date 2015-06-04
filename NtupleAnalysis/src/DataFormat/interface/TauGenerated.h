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
  explicit TauGeneratedCollection(const std::string& prefix="Taus"): ParticleCollection(prefix) {}
  ~TauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  std::vector<std::string> getIsolationDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("byCombinedIsolationDeltaBetaCorrRaw3Hits"), std::string("byIsolationMVA3newDMwLTraw"), std::string("byIsolationMVA3newDMwoLTraw"), std::string("byIsolationMVA3oldDMwLTraw"), std::string("byIsolationMVA3oldDMwoLTraw"), std::string("byLooseCombinedIsolationDeltaBetaCorr3Hits"), std::string("byLooseIsolationMVA3newDMwLT"), std::string("byLooseIsolationMVA3newDMwoLT"), std::string("byLooseIsolationMVA3oldDMwLT"), std::string("byLooseIsolationMVA3oldDMwoLT"), std::string("byMediumCombinedIsolationDeltaBetaCorr3Hits"), std::string("byMediumIsolationMVA3newDMwLT"), std::string("byMediumIsolationMVA3newDMwoLT"), std::string("byMediumIsolationMVA3oldDMwLT"), std::string("byMediumIsolationMVA3oldDMwoLT"), std::string("byTightCombinedIsolationDeltaBetaCorr3Hits"), std::string("byTightIsolationMVA3newDMwLT"), std::string("byTightIsolationMVA3newDMwoLT"), std::string("byTightIsolationMVA3oldDMwLT"), std::string("byTightIsolationMVA3oldDMwoLT"), std::string("byVLooseIsolationMVA3newDMwLT"), std::string("byVLooseIsolationMVA3newDMwoLT"), std::string("byVLooseIsolationMVA3oldDMwLT"), std::string("byVLooseIsolationMVA3oldDMwoLT"), std::string("byVTightIsolationMVA3newDMwLT"), std::string("byVTightIsolationMVA3newDMwoLT"), std::string("byVTightIsolationMVA3oldDMwLT"), std::string("byVTightIsolationMVA3oldDMwoLT"), std::string("byVVTightIsolationMVA3newDMwLT"), std::string("byVVTightIsolationMVA3newDMwoLT"), std::string("byVVTightIsolationMVA3oldDMwLT"), std::string("byVVTightIsolationMVA3oldDMwoLT")};
    return n;
  }
  std::vector<std::string> getAgainstMuonDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("againstMuonLoose"), std::string("againstMuonLoose2"), std::string("againstMuonLoose3"), std::string("againstMuonLooseMVA"), std::string("againstMuonMVAraw"), std::string("againstMuonMedium"), std::string("againstMuonMedium2"), std::string("againstMuonMediumMVA"), std::string("againstMuonTight"), std::string("againstMuonTight2"), std::string("againstMuonTight3"), std::string("againstMuonTightMVA")};
    return n;
  }
  std::vector<std::string> getAgainstElectronDiscriminatorNames() {
    static std::vector<std::string> n = { std::string("againstElectronLoose"), std::string("againstElectronLooseMVA5"), std::string("againstElectronMVA5category"), std::string("againstElectronMVA5raw"), std::string("againstElectronMedium"), std::string("againstElectronMediumMVA5"), std::string("againstElectronTight"), std::string("againstElectronTightMVA5"), std::string("againstElectronVLooseMVA5"), std::string("againstElectronVTightMVA5")};
    return n;
  }

protected:
  const Branch<std::vector<bool>> *fAgainstElectronLoose;
  const Branch<std::vector<bool>> *fAgainstElectronLooseMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronMVA5category;
  const Branch<std::vector<bool>> *fAgainstElectronMVA5raw;
  const Branch<std::vector<bool>> *fAgainstElectronMedium;
  const Branch<std::vector<bool>> *fAgainstElectronMediumMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronTight;
  const Branch<std::vector<bool>> *fAgainstElectronTightMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronVLooseMVA5;
  const Branch<std::vector<bool>> *fAgainstElectronVTightMVA5;
  const Branch<std::vector<bool>> *fAgainstMuonLoose;
  const Branch<std::vector<bool>> *fAgainstMuonLoose2;
  const Branch<std::vector<bool>> *fAgainstMuonLoose3;
  const Branch<std::vector<bool>> *fAgainstMuonLooseMVA;
  const Branch<std::vector<bool>> *fAgainstMuonMVAraw;
  const Branch<std::vector<bool>> *fAgainstMuonMedium;
  const Branch<std::vector<bool>> *fAgainstMuonMedium2;
  const Branch<std::vector<bool>> *fAgainstMuonMediumMVA;
  const Branch<std::vector<bool>> *fAgainstMuonTight;
  const Branch<std::vector<bool>> *fAgainstMuonTight2;
  const Branch<std::vector<bool>> *fAgainstMuonTight3;
  const Branch<std::vector<bool>> *fAgainstMuonTightMVA;
  const Branch<std::vector<bool>> *fByCombinedIsolationDeltaBetaCorrRaw3Hits;
  const Branch<std::vector<bool>> *fByIsolationMVA3newDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVA3newDMwoLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVA3oldDMwLTraw;
  const Branch<std::vector<bool>> *fByIsolationMVA3oldDMwoLTraw;
  const Branch<std::vector<bool>> *fByLooseCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByLooseIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fByMediumCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByMediumIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fByTightCombinedIsolationDeltaBetaCorr3Hits;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByTightIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVLooseIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVTightIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3newDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3newDMwoLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3oldDMwLT;
  const Branch<std::vector<bool>> *fByVVTightIsolationMVA3oldDMwoLT;
  const Branch<std::vector<bool>> *fChargedIsoPtSum;
  const Branch<std::vector<bool>> *fDecayModeFinding;
  const Branch<std::vector<bool>> *fDecayModeFindingNewDMs;
  const Branch<std::vector<bool>> *fNeutralIsoPtSum;
  const Branch<std::vector<bool>> *fPuCorrPtSum;
  const Branch<std::vector<double>> *fLTrkEta;
  const Branch<std::vector<double>> *fLTrkPt;
  const Branch<std::vector<int>> *fNProngs;
};


template <typename Coll>
class TauGenerated: public Particle<Coll> {
public:
  TauGenerated() {}
  TauGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~TauGenerated() {}

  std::vector<std::function<bool()>> getIsolationDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->byCombinedIsolationDeltaBetaCorrRaw3Hits(); },
      [&](){ return this->byIsolationMVA3newDMwLTraw(); },
      [&](){ return this->byIsolationMVA3newDMwoLTraw(); },
      [&](){ return this->byIsolationMVA3oldDMwLTraw(); },
      [&](){ return this->byIsolationMVA3oldDMwoLTraw(); },
      [&](){ return this->byLooseCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byLooseIsolationMVA3newDMwLT(); },
      [&](){ return this->byLooseIsolationMVA3newDMwoLT(); },
      [&](){ return this->byLooseIsolationMVA3oldDMwLT(); },
      [&](){ return this->byLooseIsolationMVA3oldDMwoLT(); },
      [&](){ return this->byMediumCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byMediumIsolationMVA3newDMwLT(); },
      [&](){ return this->byMediumIsolationMVA3newDMwoLT(); },
      [&](){ return this->byMediumIsolationMVA3oldDMwLT(); },
      [&](){ return this->byMediumIsolationMVA3oldDMwoLT(); },
      [&](){ return this->byTightCombinedIsolationDeltaBetaCorr3Hits(); },
      [&](){ return this->byTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byTightIsolationMVA3newDMwoLT(); },
      [&](){ return this->byTightIsolationMVA3oldDMwLT(); },
      [&](){ return this->byTightIsolationMVA3oldDMwoLT(); },
      [&](){ return this->byVLooseIsolationMVA3newDMwLT(); },
      [&](){ return this->byVLooseIsolationMVA3newDMwoLT(); },
      [&](){ return this->byVLooseIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVLooseIsolationMVA3oldDMwoLT(); },
      [&](){ return this->byVTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byVTightIsolationMVA3newDMwoLT(); },
      [&](){ return this->byVTightIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVTightIsolationMVA3oldDMwoLT(); },
      [&](){ return this->byVVTightIsolationMVA3newDMwLT(); },
      [&](){ return this->byVVTightIsolationMVA3newDMwoLT(); },
      [&](){ return this->byVVTightIsolationMVA3oldDMwLT(); },
      [&](){ return this->byVVTightIsolationMVA3oldDMwoLT(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstMuonDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->againstMuonLoose(); },
      [&](){ return this->againstMuonLoose2(); },
      [&](){ return this->againstMuonLoose3(); },
      [&](){ return this->againstMuonLooseMVA(); },
      [&](){ return this->againstMuonMVAraw(); },
      [&](){ return this->againstMuonMedium(); },
      [&](){ return this->againstMuonMedium2(); },
      [&](){ return this->againstMuonMediumMVA(); },
      [&](){ return this->againstMuonTight(); },
      [&](){ return this->againstMuonTight2(); },
      [&](){ return this->againstMuonTight3(); },
      [&](){ return this->againstMuonTightMVA(); }
    };
    return values;
  }
  std::vector<std::function<bool()>> getAgainstElectronDiscriminatorValues() {
    static std::vector<std::function<bool()>> values = {
      [&](){ return this->againstElectronLoose(); },
      [&](){ return this->againstElectronLooseMVA5(); },
      [&](){ return this->againstElectronMVA5category(); },
      [&](){ return this->againstElectronMVA5raw(); },
      [&](){ return this->againstElectronMedium(); },
      [&](){ return this->againstElectronMediumMVA5(); },
      [&](){ return this->againstElectronTight(); },
      [&](){ return this->againstElectronTightMVA5(); },
      [&](){ return this->againstElectronVLooseMVA5(); },
      [&](){ return this->againstElectronVTightMVA5(); }
    };
    return values;
  }

  bool againstElectronLoose() const { return this->fCollection->fAgainstElectronLoose->value()[this->index()]; }
  bool againstElectronLooseMVA5() const { return this->fCollection->fAgainstElectronLooseMVA5->value()[this->index()]; }
  bool againstElectronMVA5category() const { return this->fCollection->fAgainstElectronMVA5category->value()[this->index()]; }
  bool againstElectronMVA5raw() const { return this->fCollection->fAgainstElectronMVA5raw->value()[this->index()]; }
  bool againstElectronMedium() const { return this->fCollection->fAgainstElectronMedium->value()[this->index()]; }
  bool againstElectronMediumMVA5() const { return this->fCollection->fAgainstElectronMediumMVA5->value()[this->index()]; }
  bool againstElectronTight() const { return this->fCollection->fAgainstElectronTight->value()[this->index()]; }
  bool againstElectronTightMVA5() const { return this->fCollection->fAgainstElectronTightMVA5->value()[this->index()]; }
  bool againstElectronVLooseMVA5() const { return this->fCollection->fAgainstElectronVLooseMVA5->value()[this->index()]; }
  bool againstElectronVTightMVA5() const { return this->fCollection->fAgainstElectronVTightMVA5->value()[this->index()]; }
  bool againstMuonLoose() const { return this->fCollection->fAgainstMuonLoose->value()[this->index()]; }
  bool againstMuonLoose2() const { return this->fCollection->fAgainstMuonLoose2->value()[this->index()]; }
  bool againstMuonLoose3() const { return this->fCollection->fAgainstMuonLoose3->value()[this->index()]; }
  bool againstMuonLooseMVA() const { return this->fCollection->fAgainstMuonLooseMVA->value()[this->index()]; }
  bool againstMuonMVAraw() const { return this->fCollection->fAgainstMuonMVAraw->value()[this->index()]; }
  bool againstMuonMedium() const { return this->fCollection->fAgainstMuonMedium->value()[this->index()]; }
  bool againstMuonMedium2() const { return this->fCollection->fAgainstMuonMedium2->value()[this->index()]; }
  bool againstMuonMediumMVA() const { return this->fCollection->fAgainstMuonMediumMVA->value()[this->index()]; }
  bool againstMuonTight() const { return this->fCollection->fAgainstMuonTight->value()[this->index()]; }
  bool againstMuonTight2() const { return this->fCollection->fAgainstMuonTight2->value()[this->index()]; }
  bool againstMuonTight3() const { return this->fCollection->fAgainstMuonTight3->value()[this->index()]; }
  bool againstMuonTightMVA() const { return this->fCollection->fAgainstMuonTightMVA->value()[this->index()]; }
  bool byCombinedIsolationDeltaBetaCorrRaw3Hits() const { return this->fCollection->fByCombinedIsolationDeltaBetaCorrRaw3Hits->value()[this->index()]; }
  bool byIsolationMVA3newDMwLTraw() const { return this->fCollection->fByIsolationMVA3newDMwLTraw->value()[this->index()]; }
  bool byIsolationMVA3newDMwoLTraw() const { return this->fCollection->fByIsolationMVA3newDMwoLTraw->value()[this->index()]; }
  bool byIsolationMVA3oldDMwLTraw() const { return this->fCollection->fByIsolationMVA3oldDMwLTraw->value()[this->index()]; }
  bool byIsolationMVA3oldDMwoLTraw() const { return this->fCollection->fByIsolationMVA3oldDMwoLTraw->value()[this->index()]; }
  bool byLooseCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByLooseCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byLooseIsolationMVA3newDMwLT() const { return this->fCollection->fByLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVA3newDMwoLT() const { return this->fCollection->fByLooseIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byLooseIsolationMVA3oldDMwLT() const { return this->fCollection->fByLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVA3oldDMwoLT() const { return this->fCollection->fByLooseIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byMediumCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByMediumCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byMediumIsolationMVA3newDMwLT() const { return this->fCollection->fByMediumIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVA3newDMwoLT() const { return this->fCollection->fByMediumIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byMediumIsolationMVA3oldDMwLT() const { return this->fCollection->fByMediumIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVA3oldDMwoLT() const { return this->fCollection->fByMediumIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byTightCombinedIsolationDeltaBetaCorr3Hits() const { return this->fCollection->fByTightCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byTightIsolationMVA3newDMwLT() const { return this->fCollection->fByTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byTightIsolationMVA3newDMwoLT() const { return this->fCollection->fByTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byTightIsolationMVA3oldDMwoLT() const { return this->fCollection->fByTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3newDMwLT() const { return this->fCollection->fByVLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3newDMwoLT() const { return this->fCollection->fByVLooseIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3oldDMwLT() const { return this->fCollection->fByVLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3oldDMwoLT() const { return this->fCollection->fByVLooseIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVTightIsolationMVA3newDMwLT() const { return this->fCollection->fByVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3newDMwoLT() const { return this->fCollection->fByVTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3oldDMwoLT() const { return this->fCollection->fByVTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3newDMwLT() const { return this->fCollection->fByVVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3newDMwoLT() const { return this->fCollection->fByVVTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3oldDMwLT() const { return this->fCollection->fByVVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3oldDMwoLT() const { return this->fCollection->fByVVTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool chargedIsoPtSum() const { return this->fCollection->fChargedIsoPtSum->value()[this->index()]; }
  bool decayModeFinding() const { return this->fCollection->fDecayModeFinding->value()[this->index()]; }
  bool decayModeFindingNewDMs() const { return this->fCollection->fDecayModeFindingNewDMs->value()[this->index()]; }
  bool neutralIsoPtSum() const { return this->fCollection->fNeutralIsoPtSum->value()[this->index()]; }
  bool puCorrPtSum() const { return this->fCollection->fPuCorrPtSum->value()[this->index()]; }
  double lTrkEta() const { return this->fCollection->fLTrkEta->value()[this->index()]; }
  double lTrkPt() const { return this->fCollection->fLTrkPt->value()[this->index()]; }
  int nProngs() const { return this->fCollection->fNProngs->value()[this->index()]; }

};

#endif
