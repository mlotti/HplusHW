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

template <typename Coll>
class TauGenerated: public Particle<Coll> {
public:
  TauGenerated() {}
  TauGenerated(Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~TauGenerated() {}

  bool againstElectronLoose() { return this->fCollection->fAgainstElectronLoose->value()[this->index()]; }
  bool againstElectronLooseMVA5() { return this->fCollection->fAgainstElectronLooseMVA5->value()[this->index()]; }
  bool againstElectronMVA5category() { return this->fCollection->fAgainstElectronMVA5category->value()[this->index()]; }
  bool againstElectronMVA5raw() { return this->fCollection->fAgainstElectronMVA5raw->value()[this->index()]; }
  bool againstElectronMedium() { return this->fCollection->fAgainstElectronMedium->value()[this->index()]; }
  bool againstElectronMediumMVA5() { return this->fCollection->fAgainstElectronMediumMVA5->value()[this->index()]; }
  bool againstElectronTight() { return this->fCollection->fAgainstElectronTight->value()[this->index()]; }
  bool againstElectronTightMVA5() { return this->fCollection->fAgainstElectronTightMVA5->value()[this->index()]; }
  bool againstElectronVLooseMVA5() { return this->fCollection->fAgainstElectronVLooseMVA5->value()[this->index()]; }
  bool againstElectronVTightMVA5() { return this->fCollection->fAgainstElectronVTightMVA5->value()[this->index()]; }
  bool againstMuonLoose() { return this->fCollection->fAgainstMuonLoose->value()[this->index()]; }
  bool againstMuonLoose2() { return this->fCollection->fAgainstMuonLoose2->value()[this->index()]; }
  bool againstMuonLoose3() { return this->fCollection->fAgainstMuonLoose3->value()[this->index()]; }
  bool againstMuonLooseMVA() { return this->fCollection->fAgainstMuonLooseMVA->value()[this->index()]; }
  bool againstMuonMVAraw() { return this->fCollection->fAgainstMuonMVAraw->value()[this->index()]; }
  bool againstMuonMedium() { return this->fCollection->fAgainstMuonMedium->value()[this->index()]; }
  bool againstMuonMedium2() { return this->fCollection->fAgainstMuonMedium2->value()[this->index()]; }
  bool againstMuonMediumMVA() { return this->fCollection->fAgainstMuonMediumMVA->value()[this->index()]; }
  bool againstMuonTight() { return this->fCollection->fAgainstMuonTight->value()[this->index()]; }
  bool againstMuonTight2() { return this->fCollection->fAgainstMuonTight2->value()[this->index()]; }
  bool againstMuonTight3() { return this->fCollection->fAgainstMuonTight3->value()[this->index()]; }
  bool againstMuonTightMVA() { return this->fCollection->fAgainstMuonTightMVA->value()[this->index()]; }
  bool byCombinedIsolationDeltaBetaCorrRaw3Hits() { return this->fCollection->fByCombinedIsolationDeltaBetaCorrRaw3Hits->value()[this->index()]; }
  bool byIsolationMVA3newDMwLTraw() { return this->fCollection->fByIsolationMVA3newDMwLTraw->value()[this->index()]; }
  bool byIsolationMVA3newDMwoLTraw() { return this->fCollection->fByIsolationMVA3newDMwoLTraw->value()[this->index()]; }
  bool byIsolationMVA3oldDMwLTraw() { return this->fCollection->fByIsolationMVA3oldDMwLTraw->value()[this->index()]; }
  bool byIsolationMVA3oldDMwoLTraw() { return this->fCollection->fByIsolationMVA3oldDMwoLTraw->value()[this->index()]; }
  bool byLooseCombinedIsolationDeltaBetaCorr3Hits() { return this->fCollection->fByLooseCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byLooseIsolationMVA3newDMwLT() { return this->fCollection->fByLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVA3newDMwoLT() { return this->fCollection->fByLooseIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byLooseIsolationMVA3oldDMwLT() { return this->fCollection->fByLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byLooseIsolationMVA3oldDMwoLT() { return this->fCollection->fByLooseIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byMediumCombinedIsolationDeltaBetaCorr3Hits() { return this->fCollection->fByMediumCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byMediumIsolationMVA3newDMwLT() { return this->fCollection->fByMediumIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVA3newDMwoLT() { return this->fCollection->fByMediumIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byMediumIsolationMVA3oldDMwLT() { return this->fCollection->fByMediumIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byMediumIsolationMVA3oldDMwoLT() { return this->fCollection->fByMediumIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byTightCombinedIsolationDeltaBetaCorr3Hits() { return this->fCollection->fByTightCombinedIsolationDeltaBetaCorr3Hits->value()[this->index()]; }
  bool byTightIsolationMVA3newDMwLT() { return this->fCollection->fByTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byTightIsolationMVA3newDMwoLT() { return this->fCollection->fByTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byTightIsolationMVA3oldDMwLT() { return this->fCollection->fByTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byTightIsolationMVA3oldDMwoLT() { return this->fCollection->fByTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3newDMwLT() { return this->fCollection->fByVLooseIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3newDMwoLT() { return this->fCollection->fByVLooseIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3oldDMwLT() { return this->fCollection->fByVLooseIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVLooseIsolationMVA3oldDMwoLT() { return this->fCollection->fByVLooseIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVTightIsolationMVA3newDMwLT() { return this->fCollection->fByVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3newDMwoLT() { return this->fCollection->fByVTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVTightIsolationMVA3oldDMwLT() { return this->fCollection->fByVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVTightIsolationMVA3oldDMwoLT() { return this->fCollection->fByVTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3newDMwLT() { return this->fCollection->fByVVTightIsolationMVA3newDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3newDMwoLT() { return this->fCollection->fByVVTightIsolationMVA3newDMwoLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3oldDMwLT() { return this->fCollection->fByVVTightIsolationMVA3oldDMwLT->value()[this->index()]; }
  bool byVVTightIsolationMVA3oldDMwoLT() { return this->fCollection->fByVVTightIsolationMVA3oldDMwoLT->value()[this->index()]; }
  bool chargedIsoPtSum() { return this->fCollection->fChargedIsoPtSum->value()[this->index()]; }
  bool decayModeFinding() { return this->fCollection->fDecayModeFinding->value()[this->index()]; }
  bool decayModeFindingNewDMs() { return this->fCollection->fDecayModeFindingNewDMs->value()[this->index()]; }
  bool neutralIsoPtSum() { return this->fCollection->fNeutralIsoPtSum->value()[this->index()]; }
  bool puCorrPtSum() { return this->fCollection->fPuCorrPtSum->value()[this->index()]; }
  double lTrkPt() { return this->fCollection->fLTrkPt->value()[this->index()]; }
  int nProngs() { return this->fCollection->fNProngs->value()[this->index()]; }
  short pdgId() { return this->fCollection->fPdgId->value()[this->index()]; }
};

#endif
