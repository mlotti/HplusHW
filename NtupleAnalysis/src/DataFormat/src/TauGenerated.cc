
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/TauGenerated.h"

#include "Framework/interface/BranchManager.h"

void TauGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCVisibleTau.setupBranches(mgr);
  fmatchingJet.setupBranches(mgr);

  mgr.book(prefix()+"_againstElectronLooseMVA6", &fAgainstElectronLooseMVA6);
  mgr.book(prefix()+"_againstElectronMVA6Raw", &fAgainstElectronMVA6Raw);
  mgr.book(prefix()+"_againstElectronMVA6category", &fAgainstElectronMVA6category);
  mgr.book(prefix()+"_againstElectronMediumMVA6", &fAgainstElectronMediumMVA6);
  mgr.book(prefix()+"_againstElectronTightMVA6", &fAgainstElectronTightMVA6);
  mgr.book(prefix()+"_againstElectronVLooseMVA6", &fAgainstElectronVLooseMVA6);
  mgr.book(prefix()+"_againstElectronVTightMVA6", &fAgainstElectronVTightMVA6);
  mgr.book(prefix()+"_againstMuonLoose3", &fAgainstMuonLoose3);
  mgr.book(prefix()+"_againstMuonTight3", &fAgainstMuonTight3);
  mgr.book(prefix()+"_byCombinedIsolationDeltaBetaCorrRaw3Hits", &fByCombinedIsolationDeltaBetaCorrRaw3Hits);
  mgr.book(prefix()+"_byIsolationMVArun2v1DBdR03oldDMwLTraw", &fByIsolationMVArun2v1DBdR03oldDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVArun2v1DBnewDMwLTraw", &fByIsolationMVArun2v1DBnewDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVArun2v1DBoldDMwLTraw", &fByIsolationMVArun2v1DBoldDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVArun2v1PWdR03oldDMwLTraw", &fByIsolationMVArun2v1PWdR03oldDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVArun2v1PWnewDMwLTraw", &fByIsolationMVArun2v1PWnewDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVArun2v1PWoldDMwLTraw", &fByIsolationMVArun2v1PWoldDMwLTraw);
  mgr.book(prefix()+"_byLooseCombinedIsolationDeltaBetaCorr3Hits", &fByLooseCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1DBdR03oldDMwLT", &fByLooseIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1DBnewDMwLT", &fByLooseIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1DBoldDMwLT", &fByLooseIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1PWdR03oldDMwLT", &fByLooseIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1PWnewDMwLT", &fByLooseIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVArun2v1PWoldDMwLT", &fByLooseIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_byMediumCombinedIsolationDeltaBetaCorr3Hits", &fByMediumCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1DBdR03oldDMwLT", &fByMediumIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1DBnewDMwLT", &fByMediumIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1DBoldDMwLT", &fByMediumIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1PWdR03oldDMwLT", &fByMediumIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1PWnewDMwLT", &fByMediumIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVArun2v1PWoldDMwLT", &fByMediumIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_byPhotonPtSumOutsideSignalCone", &fByPhotonPtSumOutsideSignalCone);
  mgr.book(prefix()+"_byTightCombinedIsolationDeltaBetaCorr3Hits", &fByTightCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1DBdR03oldDMwLT", &fByTightIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1DBnewDMwLT", &fByTightIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1DBoldDMwLT", &fByTightIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1PWdR03oldDMwLT", &fByTightIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1PWnewDMwLT", &fByTightIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVArun2v1PWoldDMwLT", &fByTightIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1DBdR03oldDMwLT", &fByVLooseIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1DBnewDMwLT", &fByVLooseIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1DBoldDMwLT", &fByVLooseIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1PWdR03oldDMwLT", &fByVLooseIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1PWnewDMwLT", &fByVLooseIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1PWoldDMwLT", &fByVLooseIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1DBdR03oldDMwLT", &fByVTightIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1DBnewDMwLT", &fByVTightIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1DBoldDMwLT", &fByVTightIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1PWdR03oldDMwLT", &fByVTightIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1PWnewDMwLT", &fByVTightIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVArun2v1PWoldDMwLT", &fByVTightIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1DBdR03oldDMwLT", &fByVVTightIsolationMVArun2v1DBdR03oldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1DBnewDMwLT", &fByVVTightIsolationMVArun2v1DBnewDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1DBoldDMwLT", &fByVVTightIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1PWdR03oldDMwLT", &fByVVTightIsolationMVArun2v1PWdR03oldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1PWnewDMwLT", &fByVVTightIsolationMVArun2v1PWnewDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVArun2v1PWoldDMwLT", &fByVVTightIsolationMVArun2v1PWoldDMwLT);
  mgr.book(prefix()+"_chargedIsoPtSum", &fChargedIsoPtSum);
  mgr.book(prefix()+"_chargedIsoPtSumdR03", &fChargedIsoPtSumdR03);
  mgr.book(prefix()+"_decayModeFinding", &fDecayModeFinding);
  mgr.book(prefix()+"_decayModeFindingNewDMs", &fDecayModeFindingNewDMs);
  mgr.book(prefix()+"_footprintCorrection", &fFootprintCorrection);
  mgr.book(prefix()+"_footprintCorrectiondR03", &fFootprintCorrectiondR03);
  mgr.book(prefix()+"_neutralIsoPtSum", &fNeutralIsoPtSum);
  mgr.book(prefix()+"_neutralIsoPtSumWeight", &fNeutralIsoPtSumWeight);
  mgr.book(prefix()+"_neutralIsoPtSumWeightdR03", &fNeutralIsoPtSumWeightdR03);
  mgr.book(prefix()+"_neutralIsoPtSumdR03", &fNeutralIsoPtSumdR03);
  mgr.book(prefix()+"_photonPtSumOutsideSignalCone", &fPhotonPtSumOutsideSignalCone);
  mgr.book(prefix()+"_photonPtSumOutsideSignalConedR03", &fPhotonPtSumOutsideSignalConedR03);
  mgr.book(prefix()+"_puCorrPtSum", &fPuCorrPtSum);
  mgr.book(prefix()+"_lChTrkEta", &fLChTrkEta);
  mgr.book(prefix()+"_lChTrkPt", &fLChTrkPt);
  mgr.book(prefix()+"_lNeutrTrkEta", &fLNeutrTrkEta);
  mgr.book(prefix()+"_lNeutrTrkPt", &fLNeutrTrkPt);
  mgr.book(prefix()+"_IPxy", &fIPxy);
  mgr.book(prefix()+"_IPxySignif", &fIPxySignif);
  mgr.book(prefix()+"_charge", &fCharge);
  mgr.book(prefix()+"_decayMode", &fDecayMode);
  mgr.book(prefix()+"_mcNPizero", &fMcNPizero);
  mgr.book(prefix()+"_mcNProngs", &fMcNProngs);
  mgr.book(prefix()+"_nProngs", &fNProngs);
  mgr.book(prefix()+"_pdgOrigin", &fPdgOrigin);
}
