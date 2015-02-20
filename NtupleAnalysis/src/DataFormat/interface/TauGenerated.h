// -*- c++ -*-
#ifndef DataFormat_TauGenerated_h
#define DataFormat_TauGenerated_h

#include "DataFormat/interface/Particle.h"

class TauGenerated;

class TauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit TauGeneratedCollection(const std::string& prefix="Taus"): ParticleCollection(prefix) {}
  ~TauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  TauGenerated operator[](size_t i);

  friend class TauGenerated;
  friend class Particle<TauGeneratedCollection>;

protected:
  Branch<std::vector<bool>> *fAgainstElectronLoose;
  Branch<std::vector<bool>> *fAgainstElectronLooseMVA5;
  Branch<std::vector<bool>> *fAgainstElectronMVA5category;
  Branch<std::vector<bool>> *fAgainstElectronMVA5raw;
  Branch<std::vector<bool>> *fAgainstElectronMedium;
  Branch<std::vector<bool>> *fAgainstElectronMediumMVA5;
  Branch<std::vector<bool>> *fAgainstElectronTight;
  Branch<std::vector<bool>> *fAgainstElectronTightMVA5;
  Branch<std::vector<bool>> *fAgainstElectronVLooseMVA5;
  Branch<std::vector<bool>> *fAgainstElectronVTightMVA5;
  Branch<std::vector<bool>> *fAgainstMuonLoose;
  Branch<std::vector<bool>> *fAgainstMuonLoose2;
  Branch<std::vector<bool>> *fAgainstMuonLoose3;
  Branch<std::vector<bool>> *fAgainstMuonLooseMVA;
  Branch<std::vector<bool>> *fAgainstMuonMVAraw;
  Branch<std::vector<bool>> *fAgainstMuonMedium;
  Branch<std::vector<bool>> *fAgainstMuonMedium2;
  Branch<std::vector<bool>> *fAgainstMuonMediumMVA;
  Branch<std::vector<bool>> *fAgainstMuonTight;
  Branch<std::vector<bool>> *fAgainstMuonTight2;
  Branch<std::vector<bool>> *fAgainstMuonTight3;
  Branch<std::vector<bool>> *fAgainstMuonTightMVA;
  Branch<std::vector<bool>> *fByCombinedIsolationDeltaBetaCorrRaw3Hits;
  Branch<std::vector<bool>> *fByIsolationMVA3newDMwLTraw;
  Branch<std::vector<bool>> *fByIsolationMVA3newDMwoLTraw;
  Branch<std::vector<bool>> *fByIsolationMVA3oldDMwLTraw;
  Branch<std::vector<bool>> *fByIsolationMVA3oldDMwoLTraw;
  Branch<std::vector<bool>> *fByLooseCombinedIsolationDeltaBetaCorr3Hits;
  Branch<std::vector<bool>> *fByLooseIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByLooseIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByLooseIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByLooseIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fByMediumCombinedIsolationDeltaBetaCorr3Hits;
  Branch<std::vector<bool>> *fByMediumIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByMediumIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByMediumIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByMediumIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fByTightCombinedIsolationDeltaBetaCorr3Hits;
  Branch<std::vector<bool>> *fByTightIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByTightIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByTightIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByTightIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fByVLooseIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByVLooseIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByVLooseIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByVLooseIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fByVTightIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByVTightIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByVTightIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByVTightIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fByVVTightIsolationMVA3newDMwLT;
  Branch<std::vector<bool>> *fByVVTightIsolationMVA3newDMwoLT;
  Branch<std::vector<bool>> *fByVVTightIsolationMVA3oldDMwLT;
  Branch<std::vector<bool>> *fByVVTightIsolationMVA3oldDMwoLT;
  Branch<std::vector<bool>> *fChargedIsoPtSum;
  Branch<std::vector<bool>> *fDecayModeFinding;
  Branch<std::vector<bool>> *fDecayModeFindingNewDMs;
  Branch<std::vector<bool>> *fNeutralIsoPtSum;
  Branch<std::vector<bool>> *fPuCorrPtSum;
  Branch<std::vector<double>> *fLTrkPt;
  Branch<std::vector<int>> *fNProngs;
  Branch<std::vector<short>> *fPdgId;
};


class TauGenerated: public Particle<TauGeneratedCollection> {
public:
  TauGenerated() {}
  TauGenerated(TauGeneratedCollection* coll, size_t index): Particle<TauGeneratedCollection>(coll, index) {}
  ~TauGenerated() {}

  bool againstElectronLoose() { return fCollection->fAgainstElectronLoose->value()[index()]; }
  bool againstElectronLooseMVA5() { return fCollection->fAgainstElectronLooseMVA5->value()[index()]; }
  bool againstElectronMVA5category() { return fCollection->fAgainstElectronMVA5category->value()[index()]; }
  bool againstElectronMVA5raw() { return fCollection->fAgainstElectronMVA5raw->value()[index()]; }
  bool againstElectronMedium() { return fCollection->fAgainstElectronMedium->value()[index()]; }
  bool againstElectronMediumMVA5() { return fCollection->fAgainstElectronMediumMVA5->value()[index()]; }
  bool againstElectronTight() { return fCollection->fAgainstElectronTight->value()[index()]; }
  bool againstElectronTightMVA5() { return fCollection->fAgainstElectronTightMVA5->value()[index()]; }
  bool againstElectronVLooseMVA5() { return fCollection->fAgainstElectronVLooseMVA5->value()[index()]; }
  bool againstElectronVTightMVA5() { return fCollection->fAgainstElectronVTightMVA5->value()[index()]; }
  bool againstMuonLoose() { return fCollection->fAgainstMuonLoose->value()[index()]; }
  bool againstMuonLoose2() { return fCollection->fAgainstMuonLoose2->value()[index()]; }
  bool againstMuonLoose3() { return fCollection->fAgainstMuonLoose3->value()[index()]; }
  bool againstMuonLooseMVA() { return fCollection->fAgainstMuonLooseMVA->value()[index()]; }
  bool againstMuonMVAraw() { return fCollection->fAgainstMuonMVAraw->value()[index()]; }
  bool againstMuonMedium() { return fCollection->fAgainstMuonMedium->value()[index()]; }
  bool againstMuonMedium2() { return fCollection->fAgainstMuonMedium2->value()[index()]; }
  bool againstMuonMediumMVA() { return fCollection->fAgainstMuonMediumMVA->value()[index()]; }
  bool againstMuonTight() { return fCollection->fAgainstMuonTight->value()[index()]; }
  bool againstMuonTight2() { return fCollection->fAgainstMuonTight2->value()[index()]; }
  bool againstMuonTight3() { return fCollection->fAgainstMuonTight3->value()[index()]; }
  bool againstMuonTightMVA() { return fCollection->fAgainstMuonTightMVA->value()[index()]; }
  bool byCombinedIsolationDeltaBetaCorrRaw3Hits() { return fCollection->fByCombinedIsolationDeltaBetaCorrRaw3Hits->value()[index()]; }
  bool byIsolationMVA3newDMwLTraw() { return fCollection->fByIsolationMVA3newDMwLTraw->value()[index()]; }
  bool byIsolationMVA3newDMwoLTraw() { return fCollection->fByIsolationMVA3newDMwoLTraw->value()[index()]; }
  bool byIsolationMVA3oldDMwLTraw() { return fCollection->fByIsolationMVA3oldDMwLTraw->value()[index()]; }
  bool byIsolationMVA3oldDMwoLTraw() { return fCollection->fByIsolationMVA3oldDMwoLTraw->value()[index()]; }
  bool byLooseCombinedIsolationDeltaBetaCorr3Hits() { return fCollection->fByLooseCombinedIsolationDeltaBetaCorr3Hits->value()[index()]; }
  bool byLooseIsolationMVA3newDMwLT() { return fCollection->fByLooseIsolationMVA3newDMwLT->value()[index()]; }
  bool byLooseIsolationMVA3newDMwoLT() { return fCollection->fByLooseIsolationMVA3newDMwoLT->value()[index()]; }
  bool byLooseIsolationMVA3oldDMwLT() { return fCollection->fByLooseIsolationMVA3oldDMwLT->value()[index()]; }
  bool byLooseIsolationMVA3oldDMwoLT() { return fCollection->fByLooseIsolationMVA3oldDMwoLT->value()[index()]; }
  bool byMediumCombinedIsolationDeltaBetaCorr3Hits() { return fCollection->fByMediumCombinedIsolationDeltaBetaCorr3Hits->value()[index()]; }
  bool byMediumIsolationMVA3newDMwLT() { return fCollection->fByMediumIsolationMVA3newDMwLT->value()[index()]; }
  bool byMediumIsolationMVA3newDMwoLT() { return fCollection->fByMediumIsolationMVA3newDMwoLT->value()[index()]; }
  bool byMediumIsolationMVA3oldDMwLT() { return fCollection->fByMediumIsolationMVA3oldDMwLT->value()[index()]; }
  bool byMediumIsolationMVA3oldDMwoLT() { return fCollection->fByMediumIsolationMVA3oldDMwoLT->value()[index()]; }
  bool byTightCombinedIsolationDeltaBetaCorr3Hits() { return fCollection->fByTightCombinedIsolationDeltaBetaCorr3Hits->value()[index()]; }
  bool byTightIsolationMVA3newDMwLT() { return fCollection->fByTightIsolationMVA3newDMwLT->value()[index()]; }
  bool byTightIsolationMVA3newDMwoLT() { return fCollection->fByTightIsolationMVA3newDMwoLT->value()[index()]; }
  bool byTightIsolationMVA3oldDMwLT() { return fCollection->fByTightIsolationMVA3oldDMwLT->value()[index()]; }
  bool byTightIsolationMVA3oldDMwoLT() { return fCollection->fByTightIsolationMVA3oldDMwoLT->value()[index()]; }
  bool byVLooseIsolationMVA3newDMwLT() { return fCollection->fByVLooseIsolationMVA3newDMwLT->value()[index()]; }
  bool byVLooseIsolationMVA3newDMwoLT() { return fCollection->fByVLooseIsolationMVA3newDMwoLT->value()[index()]; }
  bool byVLooseIsolationMVA3oldDMwLT() { return fCollection->fByVLooseIsolationMVA3oldDMwLT->value()[index()]; }
  bool byVLooseIsolationMVA3oldDMwoLT() { return fCollection->fByVLooseIsolationMVA3oldDMwoLT->value()[index()]; }
  bool byVTightIsolationMVA3newDMwLT() { return fCollection->fByVTightIsolationMVA3newDMwLT->value()[index()]; }
  bool byVTightIsolationMVA3newDMwoLT() { return fCollection->fByVTightIsolationMVA3newDMwoLT->value()[index()]; }
  bool byVTightIsolationMVA3oldDMwLT() { return fCollection->fByVTightIsolationMVA3oldDMwLT->value()[index()]; }
  bool byVTightIsolationMVA3oldDMwoLT() { return fCollection->fByVTightIsolationMVA3oldDMwoLT->value()[index()]; }
  bool byVVTightIsolationMVA3newDMwLT() { return fCollection->fByVVTightIsolationMVA3newDMwLT->value()[index()]; }
  bool byVVTightIsolationMVA3newDMwoLT() { return fCollection->fByVVTightIsolationMVA3newDMwoLT->value()[index()]; }
  bool byVVTightIsolationMVA3oldDMwLT() { return fCollection->fByVVTightIsolationMVA3oldDMwLT->value()[index()]; }
  bool byVVTightIsolationMVA3oldDMwoLT() { return fCollection->fByVVTightIsolationMVA3oldDMwoLT->value()[index()]; }
  bool chargedIsoPtSum() { return fCollection->fChargedIsoPtSum->value()[index()]; }
  bool decayModeFinding() { return fCollection->fDecayModeFinding->value()[index()]; }
  bool decayModeFindingNewDMs() { return fCollection->fDecayModeFindingNewDMs->value()[index()]; }
  bool neutralIsoPtSum() { return fCollection->fNeutralIsoPtSum->value()[index()]; }
  bool puCorrPtSum() { return fCollection->fPuCorrPtSum->value()[index()]; }
  double lTrkPt() { return fCollection->fLTrkPt->value()[index()]; }
  int nProngs() { return fCollection->fNProngs->value()[index()]; }
  short pdgId() { return fCollection->fPdgId->value()[index()]; }
};

inline
TauGenerated TauGeneratedCollection::operator[](size_t i) {
  return TauGenerated(this, i);
}

#endif
