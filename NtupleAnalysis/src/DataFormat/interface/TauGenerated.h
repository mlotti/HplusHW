// -*- c++ -*-
#ifndef DataFormat_TauGenerated_h
#define DataFormat_TauGenerated_h

#include "DataFormat/interface/Particle.h"

class TauGeneratedCollection: public ParticleCollection<double> {
public:
  explicit TauGeneratedCollection(const std::string& prefix="Taus"): ParticleCollection(prefix) {}
  ~TauGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

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
  const Branch<std::vector<double>> *fLTrkPt;
  const Branch<std::vector<int>> *fNProngs;
  const Branch<std::vector<short>> *fPdgId;
};

template <typename Coll>
class TauGenerated: public Particle<Coll> {
public:
  TauGenerated() {}
  TauGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~TauGenerated() {}

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
  double lTrkPt() const { return this->fCollection->fLTrkPt->value()[this->index()]; }
  int nProngs() const { return this->fCollection->fNProngs->value()[this->index()]; }
  short pdgId() const { return this->fCollection->fPdgId->value()[this->index()]; }
};

#endif
