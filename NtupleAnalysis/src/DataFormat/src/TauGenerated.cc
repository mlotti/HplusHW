
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/TauGenerated.h"

#include "Framework/interface/BranchManager.h"

void TauGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_againstElectronLooseMVA5", &fAgainstElectronLooseMVA5);
  mgr.book(prefix()+"_againstElectronMVA5category", &fAgainstElectronMVA5category);
  mgr.book(prefix()+"_againstElectronMediumMVA5", &fAgainstElectronMediumMVA5);
  mgr.book(prefix()+"_againstElectronTightMVA5", &fAgainstElectronTightMVA5);
  mgr.book(prefix()+"_againstElectronVLooseMVA5", &fAgainstElectronVLooseMVA5);
  mgr.book(prefix()+"_againstElectronVTightMVA5", &fAgainstElectronVTightMVA5);
  mgr.book(prefix()+"_againstMuonLoose3", &fAgainstMuonLoose3);
  mgr.book(prefix()+"_againstMuonTight3", &fAgainstMuonTight3);
  mgr.book(prefix()+"_byCombinedIsolationDeltaBetaCorrRaw3Hits", &fByCombinedIsolationDeltaBetaCorrRaw3Hits);
  mgr.book(prefix()+"_byIsolationMVA3newDMwLTraw", &fByIsolationMVA3newDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVA3newDMwoLTraw", &fByIsolationMVA3newDMwoLTraw);
  mgr.book(prefix()+"_byIsolationMVA3oldDMwLTraw", &fByIsolationMVA3oldDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVA3oldDMwoLTraw", &fByIsolationMVA3oldDMwoLTraw);
  mgr.book(prefix()+"_byLooseCombinedIsolationDeltaBetaCorr3Hits", &fByLooseCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byLooseIsolationMVA3newDMwLT", &fByLooseIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVA3newDMwoLT", &fByLooseIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byLooseIsolationMVA3oldDMwLT", &fByLooseIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVA3oldDMwoLT", &fByLooseIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_byMediumCombinedIsolationDeltaBetaCorr3Hits", &fByMediumCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byMediumIsolationMVA3newDMwLT", &fByMediumIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVA3newDMwoLT", &fByMediumIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byMediumIsolationMVA3oldDMwLT", &fByMediumIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVA3oldDMwoLT", &fByMediumIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_byTightCombinedIsolationDeltaBetaCorr3Hits", &fByTightCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byTightIsolationMVA3newDMwLT", &fByTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVA3newDMwoLT", &fByTightIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byTightIsolationMVA3oldDMwLT", &fByTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVA3oldDMwoLT", &fByTightIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3newDMwLT", &fByVLooseIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3newDMwoLT", &fByVLooseIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3oldDMwLT", &fByVLooseIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3oldDMwoLT", &fByVLooseIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3newDMwLT", &fByVTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3newDMwoLT", &fByVTightIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3oldDMwLT", &fByVTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3oldDMwoLT", &fByVTightIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3newDMwLT", &fByVVTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3newDMwoLT", &fByVVTightIsolationMVA3newDMwoLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3oldDMwLT", &fByVVTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3oldDMwoLT", &fByVVTightIsolationMVA3oldDMwoLT);
  mgr.book(prefix()+"_chargedIsoPtSum", &fChargedIsoPtSum);
  mgr.book(prefix()+"_decayModeFinding", &fDecayModeFinding);
  mgr.book(prefix()+"_decayModeFindingNewDMs", &fDecayModeFindingNewDMs);
  mgr.book(prefix()+"_neutralIsoPtSum", &fNeutralIsoPtSum);
  mgr.book(prefix()+"_puCorrPtSum", &fPuCorrPtSum);
  mgr.book(prefix()+"_eMCVisibleTau", &fEMCVisibleTau);
  mgr.book(prefix()+"_eTESdown", &fETESdown);
  mgr.book(prefix()+"_eTESextremeDown", &fETESextremeDown);
  mgr.book(prefix()+"_eTESextremeUp", &fETESextremeUp);
  mgr.book(prefix()+"_eTESup", &fETESup);
  mgr.book(prefix()+"_ematchingJet", &fEmatchingJet);
  mgr.book(prefix()+"_etaMCVisibleTau", &fEtaMCVisibleTau);
  mgr.book(prefix()+"_etaTESdown", &fEtaTESdown);
  mgr.book(prefix()+"_etaTESextremeDown", &fEtaTESextremeDown);
  mgr.book(prefix()+"_etaTESextremeUp", &fEtaTESextremeUp);
  mgr.book(prefix()+"_etaTESup", &fEtaTESup);
  mgr.book(prefix()+"_etamatchingJet", &fEtamatchingJet);
  mgr.book(prefix()+"_lChTrkEta", &fLChTrkEta);
  mgr.book(prefix()+"_lChTrkPt", &fLChTrkPt);
  mgr.book(prefix()+"_lNeutrTrkEta", &fLNeutrTrkEta);
  mgr.book(prefix()+"_lNeutrTrkPt", &fLNeutrTrkPt);
  mgr.book(prefix()+"_phiMCVisibleTau", &fPhiMCVisibleTau);
  mgr.book(prefix()+"_phiTESdown", &fPhiTESdown);
  mgr.book(prefix()+"_phiTESextremeDown", &fPhiTESextremeDown);
  mgr.book(prefix()+"_phiTESextremeUp", &fPhiTESextremeUp);
  mgr.book(prefix()+"_phiTESup", &fPhiTESup);
  mgr.book(prefix()+"_phimatchingJet", &fPhimatchingJet);
  mgr.book(prefix()+"_ptMCVisibleTau", &fPtMCVisibleTau);
  mgr.book(prefix()+"_ptTESdown", &fPtTESdown);
  mgr.book(prefix()+"_ptTESextremeDown", &fPtTESextremeDown);
  mgr.book(prefix()+"_ptTESextremeUp", &fPtTESextremeUp);
  mgr.book(prefix()+"_ptTESup", &fPtTESup);
  mgr.book(prefix()+"_ptmatchingJet", &fPtmatchingJet);
  mgr.book(prefix()+"_nProngs", &fNProngs);
  mgr.book(prefix()+"_pdgOrigin", &fPdgOrigin);
}
