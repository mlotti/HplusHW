
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/TauGenerated.h"

#include "Framework/interface/BranchManager.h"

void TauGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCVisibleTau.setupBranches(mgr);
  fmatchingJet.setupBranches(mgr);

  mgr.book(prefix()+"_TrgMatch_LooseIsoPFTau50_Trk30_eta2p1", &fTrgMatch_LooseIsoPFTau50_Trk30_eta2p1);
  mgr.book(prefix()+"_againstElectronLooseMVA6", &fAgainstElectronLooseMVA6);
  mgr.book(prefix()+"_againstElectronLooseMVA6Raw", &fAgainstElectronLooseMVA6Raw);
  mgr.book(prefix()+"_againstElectronMVA6category", &fAgainstElectronMVA6category);
  mgr.book(prefix()+"_againstElectronMediumMVA6", &fAgainstElectronMediumMVA6);
  mgr.book(prefix()+"_againstElectronTightMVA6", &fAgainstElectronTightMVA6);
  mgr.book(prefix()+"_againstElectronVLooseMVA6", &fAgainstElectronVLooseMVA6);
  mgr.book(prefix()+"_againstElectronVTightMVA6", &fAgainstElectronVTightMVA6);
  mgr.book(prefix()+"_againstMuonLoose3", &fAgainstMuonLoose3);
  mgr.book(prefix()+"_againstMuonTight3", &fAgainstMuonTight3);
  mgr.book(prefix()+"_byCombinedIsolationDeltaBetaCorrRaw3Hits", &fByCombinedIsolationDeltaBetaCorrRaw3Hits);
  mgr.book(prefix()+"_byIsolationMVA3newDMwLTraw", &fByIsolationMVA3newDMwLTraw);
  mgr.book(prefix()+"_byIsolationMVA3oldDMwLTraw", &fByIsolationMVA3oldDMwLTraw);
  mgr.book(prefix()+"_byLooseCombinedIsolationDeltaBetaCorr3Hits", &fByLooseCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byLooseIsolationMVA3newDMwLT", &fByLooseIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byLooseIsolationMVA3oldDMwLT", &fByLooseIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byMediumCombinedIsolationDeltaBetaCorr3Hits", &fByMediumCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byMediumIsolationMVA3newDMwLT", &fByMediumIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byMediumIsolationMVA3oldDMwLT", &fByMediumIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byTightCombinedIsolationDeltaBetaCorr3Hits", &fByTightCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byTightIsolationMVA3newDMwLT", &fByTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byTightIsolationMVA3oldDMwLT", &fByTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3newDMwLT", &fByVLooseIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVLooseIsolationMVA3oldDMwLT", &fByVLooseIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3newDMwLT", &fByVTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVTightIsolationMVA3oldDMwLT", &fByVTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3newDMwLT", &fByVVTightIsolationMVA3newDMwLT);
  mgr.book(prefix()+"_byVVTightIsolationMVA3oldDMwLT", &fByVVTightIsolationMVA3oldDMwLT);
  mgr.book(prefix()+"_chargedIsoPtSum", &fChargedIsoPtSum);
  mgr.book(prefix()+"_decayModeFinding", &fDecayModeFinding);
  mgr.book(prefix()+"_decayModeFindingNewDMs", &fDecayModeFindingNewDMs);
  mgr.book(prefix()+"_neutralIsoPtSum", &fNeutralIsoPtSum);
  mgr.book(prefix()+"_puCorrPtSum", &fPuCorrPtSum);
  mgr.book(prefix()+"_lChTrkEta", &fLChTrkEta);
  mgr.book(prefix()+"_lChTrkPt", &fLChTrkPt);
  mgr.book(prefix()+"_lNeutrTrkEta", &fLNeutrTrkEta);
  mgr.book(prefix()+"_lNeutrTrkPt", &fLNeutrTrkPt);
  mgr.book(prefix()+"_IPxy", &fIPxy);
  mgr.book(prefix()+"_IPxySignif", &fIPxySignif);
  mgr.book(prefix()+"_decayMode", &fDecayMode);
  mgr.book(prefix()+"_mcNPizero", &fMcNPizero);
  mgr.book(prefix()+"_mcNProngs", &fMcNProngs);
  mgr.book(prefix()+"_nProngs", &fNProngs);
  mgr.book(prefix()+"_pdgOrigin", &fPdgOrigin);
}
