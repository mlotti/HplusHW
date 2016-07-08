#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewDeltaRSelector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewClosestDeltaRSelector.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

typedef HPlus::ViewDeltaRSelector<pat::Tau, reco::Candidate> HPlusPATTauCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);

typedef HPlus::ViewDeltaRSelector<reco::PFCandidate, reco::Candidate> HPlusPFCandCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPFCandCandViewDeltaRSelector);


typedef HPlus::ViewClosestDeltaRSelector<pat::Tau, reco::Candidate> HPlusPATTauCandViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewClosestDeltaRSelector);

typedef HPlus::ViewClosestDeltaRSelector<pat::Tau, math::XYZTLorentzVector> HPlusPATTauLorentzVectorViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauLorentzVectorViewClosestDeltaRSelector);

typedef HPlus::ViewClosestDeltaRSelector<pat::Jet, math::XYZTLorentzVector> HPlusPATJetLorentzVectorViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATJetLorentzVectorViewClosestDeltaRSelector);

typedef HPlus::ViewClosestDeltaRSelector<pat::Electron, math::XYZTLorentzVector> HPlusPATElectronLorentzVectorViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATElectronLorentzVectorViewClosestDeltaRSelector);

typedef HPlus::ViewClosestDeltaRSelector<pat::Muon, math::XYZTLorentzVector> HPlusPATMuonLorentzVectorViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATMuonLorentzVectorViewClosestDeltaRSelector);
