#ifndef NtupleAnalysis_fwd_h
#define NtupleAnalysis_fwd_h

enum TauDecayMatchType {
  kTauDecayUnknown = 0,
  kUToTau = 1,
  kDToTau = 2,
  kSToTau = 3,
  kCToTau = 4,
  kBToTau = 5,
  kElectronToTau = 11,
  kMuonToTau = 13,
  kTauDecaysToHadrons = 15,
  kGluonToTau = 21,
  kTauDecaysToElectron = 1511,
  kTauDecaysToMuon = 1513
};

enum TauOriginType {
  kTauOriginUnknown = 0,
  kFromZ = 23,
  kFromW = 24,
  kFromHplus = 37,
  kFromOtherSource = 99
};

enum TopDecayMode {
  kTopDecayUnknown = 0,
  kTopToHadrons = 1,
  kTopToElectron = 11,
  kTopToMuon = 13,
  kTopToTau = 15
};

enum WDecayMode {
  kWDecayUnknown = 0,
  kWToHadrons = 1,
  kWToElectron = 11,
  kWToMuon = 13,
  kWToTau = 15
};

enum JetIDType {
  kJetIDLoose = 0,
  kJetIDTight,
  kJetIDTightLepVeto
};

#endif
