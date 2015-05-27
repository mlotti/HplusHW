// -*- c++ -*-
#ifndef __CONFIGURATION__
#define __CONFIGURATION__

#include<cstdlib>
#include<cmath>
#include<string>
#include<exception>

namespace EmbeddingMuonIsolation {
  enum Mode {
    kDisabled,
    kStandard,
    kChargedHadrRel10,
    kChargedHadrRel15,
    kTauLike
  };

  inline Mode stringToMode(const std::string& isolationMode) {
    if     (isolationMode == "disabled")         return kDisabled;
    else if(isolationMode == "standard")         return kStandard;
    else if(isolationMode == "chargedHadrRel10") return kChargedHadrRel10;
    else if(isolationMode == "chargedHadrRel15") return kChargedHadrRel15;
    else if(isolationMode == "taulike")          return kTauLike;
    
    throw std::runtime_error("isolationMode is '"+isolationMode+"', allowed values are 'disabled', 'standard', 'chargedHadrRel10', 'chargedHadrRel15', 'taulike'");
  }
}

namespace MuonID {
  template <typename T> bool pt(T& muon) { return muon.p4().Pt() > 41; }
  template <typename T> bool eta(T& muon) { return std::abs(muon.p4().Eta()) < 2.1; }
  template <typename T> bool dB(T& muon) { return std::abs(muon.dB()) < 0.2; }
  template <typename T> bool chi2(T& muon) { return muon.normalizedChi2() < 10; }

  template <typename T> bool tunePPtError(T& muon) { return muon.tunePPtError() / std::sqrt(muon.tunePP3().Perp2()) < 0.3; }

  template <typename T> bool standardRelativeIsolation(T& muon) { return standardRelativeIsolationCut(muon.standardRelativeIsolation()); }
  bool standardRelativeIsolationCut(double isoVar) { return isoVar < 0.12; }

  template <typename T> bool tauLikeIsolation(T& muon) { return tauLikeIsolationCut(muon.tauLikeIsolation()); }
  bool tauLikeIsolationCut(double isoVar) { return isoVar < 2; }

  template <typename T> bool isolation(T& muon, EmbeddingMuonIsolation::Mode mode) {
    if(mode == EmbeddingMuonIsolation::kStandard) return standardRelativeIsolation(muon);
    if(mode == EmbeddingMuonIsolation::kTauLike)  return tauLikeIsolation(muon);
    if(mode == EmbeddingMuonIsolation::kChargedHadrRel10) return muon.chargedHadronIso()/muon.p4().Pt() < 0.1;
    if(mode == EmbeddingMuonIsolation::kChargedHadrRel15) return muon.chargedHadronIso()/muon.p4().Pt() < 0.15;
    return true;
  }
}

namespace MuonVeto {
  template <typename T> bool pt(T& muon) { return muon.p4().Pt() > 10; }
  template <typename T> bool eta(T& muon) { return std::abs(muon.p4().Eta()) < 2.5; }
  template <typename T> bool chi2(T& muon) { return muon.normalizedChi2() < 10; }
  template <typename T> bool dB(T& muon) { return std::abs(muon.dB()) < 0.02; }
  template <typename T> bool subdetectorIsolation(T& muon) { return (muon.trackIso() + muon.caloIso())/muon.p4().Pt() <= 0.15; }
  template <typename T> bool pfIsolation(T& muon) { return muon.standardRelativeIsolation() <= 0.2; }
  template <typename T> bool isolation(T& muon) { return pfIsolation(muon); }
}

namespace TauID {
  template <typename T> bool decayModeFinding(T& tau) { return tau.decayModeFinding() > 0.5; }
  //template <typename T> bool pt(T& tau) { return tau.p4().Pt() > 40; }
  template <typename T> bool pt(T& tau) { return tau.p4().Pt() > 41; }
  template <typename T> bool eta(T& tau) { return std::abs(tau.p4().Eta()) < 2.1; }
  template <typename T> bool leadingChargedHadrCandPt(T& tau) { return tau.leadPFChargedHadrCandP4().Pt() > 20; }
 
  template <typename T> bool ecalCracks(T& tau) {
    double eta = std::abs(tau.p4().Eta());
    return !(eta < 0.018 ||
             (eta > 0.423 && eta < 0.461) ||
             (eta > 0.770 && eta < 0.806) ||
             (eta > 1.127 && eta < 1.163));
  }
  template <typename T> bool ecalGap(T& tau) {
    double eta = std::abs(tau.p4().Eta());
    return !(eta > 1.460 && eta<1.558);
  }

  //template <typename T> bool againstElectron(T& tau) { return tau.againstElectronMVA() > 0.5; }
  template <typename T> bool againstElectron(T& tau) { return tau.againstElectronTightMVA3() > 0.5; }
  //template <typename T> bool againstMuon(T& tau) { return tau.againstMuonTight() > 0.5; }
  template <typename T> bool againstMuon(T& tau) { return tau.againstMuonTight2() > 0.5; }

  //template <typename T> bool isolation(T& tau) { return tau.mediumCombinedIsolationDeltaBetaCorr() > 0.5; }
  template <typename T> bool isolation(T& tau) { return tau.mediumCombinedIsolationDeltaBetaCorr3Hits() > 0.5; }
  template <typename T> bool oneProng(T& tau) { return tau.signalPFChargedHadrCandsCount() == 1; }
  template <typename T> bool rtau(T& tau) { return tau.rtau() > 0.7; }
}

namespace JetSelection {
  template <typename T> bool pt(T& jet) { return jet.p4().Pt() > 30; }
  template <typename T> bool eta(T& jet) { return std::abs(jet.p4().eta()) < 2.4; }
  template <typename T> bool jetID(T& jet) { return looseID(jet); }
  template <typename T> bool looseID(T& jet) { return jet.looseID(); }
}

#endif
