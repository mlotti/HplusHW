
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/TauGenerated.h"

#include "Framework/interface/BranchManager.h"

void TauGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCVisibleTau.setupBranches(mgr);
  fmatchingJet.setupBranches(mgr);

  mgr.book(prefix()+"_againstElectronLooseMVA6", &fAgainstElectronLooseMVA6);
  mgr.book(prefix()+"_againstElectronMediumMVA6", &fAgainstElectronMediumMVA6);
  mgr.book(prefix()+"_againstElectronTightMVA6", &fAgainstElectronTightMVA6);
  mgr.book(prefix()+"_againstElectronVLooseMVA6", &fAgainstElectronVLooseMVA6);
  mgr.book(prefix()+"_againstElectronVTightMVA6", &fAgainstElectronVTightMVA6);
  mgr.book(prefix()+"_againstMuonLoose3", &fAgainstMuonLoose3);
  mgr.book(prefix()+"_againstMuonTight3", &fAgainstMuonTight3);
  mgr.book(prefix()+"_byLooseCombinedIsolationDeltaBetaCorr3Hits", &fByLooseCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byMediumCombinedIsolationDeltaBetaCorr3Hits", &fByMediumCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byTightCombinedIsolationDeltaBetaCorr3Hits", &fByTightCombinedIsolationDeltaBetaCorr3Hits);
  mgr.book(prefix()+"_byVLooseIsolationMVArun2v1DBoldDMwLT", &fByVLooseIsolationMVArun2v1DBoldDMwLT);
  mgr.book(prefix()+"_decayModeFinding", &fDecayModeFinding);
  mgr.book(prefix()+"_decayModeFindingNewDMs", &fDecayModeFindingNewDMs);
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
