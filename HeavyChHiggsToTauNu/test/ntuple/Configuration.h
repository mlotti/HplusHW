// -*- c++ -*-
#ifndef __CONFIGURATION__
#define __CONFIGURATION__

#include<cstdlib>
#include<cmath>

namespace MuonID {
  template <typename T> bool pt(T& muon) { return muon.p4().Pt() > 40; }
  template <typename T> bool eta(T& muon) { return std::abs(muon.p4().Eta()) < 2.1; }
  template <typename T> bool dB(T& muon) { return std::abs(muon.dB()) < 0.02; }

  template <typename T> bool standardRelativeIsolation(T& muon) { return standardRelativeIsolation(muon.standardRelativeIsolation()); }
  bool standardRelativeIsolation(double isoVar) { return isoVar < 0.12; }

  template <typename T> bool embeddingIsolation(T& muon) { return embeddingIsolation(muon.embeddingIsolation()); }
  bool embeddingIsolation(double isoVar) { return isoVar < 2; }
}

namespace MuonVeto {
  template <typename T> bool pt(T& muon) { return muon.p4().Pt() > 15; }
  template <typename T> bool eta(T& muon) { return std::abs(muon.p4().Eta()) < 2.5; }
  template <typename T> bool dB(T& muon) { return std::abs(muon.dB()) < 0.02; }
  template <typename T> bool subdetectorIsolation(T& muon) { return (muon.trackIso() + muon.caloIso())/muon.p4().Pt() <= 0.15; }
}

namespace TauID {
  template <typename T> bool decayModeFinding(T& tau) { return tau.decayModeFinding() > 0.5; }
  template <typename T> bool pt(T& tau) { return tau.p4().Pt() > 40; }
  template <typename T> bool eta(T& tau) { return std::abs(tau.p4().Eta()) < 2.1; }
  template <typename T> bool leadingChargedHadrCandPt(T& tau) { return tau.leadPFChargedHadrCandP4().Pt() > 20; }
 
  template <typename T> bool againstElectron(T& tau) { return tau.againstElectronMVA() > 0.5; }
  template <typename T> bool againstMuon(T& tau) { return tau.againstMuonTight() > 0.5; }

  template <typename T> bool isolation(T& tau) { return tau.mediumCombinedIsolationDeltaBetaCorr() > 0.5; }
  template <typename T> bool oneProng(T& tau) { return tau.signalPFChargedHadrCandsCount() == 1; }
  template <typename T> bool rtau(T& tau) { return tau.rtau() > 0.7; }
}

#endif
