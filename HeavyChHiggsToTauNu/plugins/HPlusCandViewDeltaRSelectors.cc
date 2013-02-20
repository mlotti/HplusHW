#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewDeltaRSelector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewClosestDeltaRSelector.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

typedef HPlus::ViewDeltaRSelector<pat::Tau, reco::Candidate> HPlusPATTauCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);

typedef HPlus::ViewDeltaRSelector<reco::PFCandidate, reco::Candidate> HPlusPFCandCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPFCandCandViewDeltaRSelector);


typedef HPlus::ViewClosestDeltaRSelector<pat::Tau, reco::Candidate> HPlusPATTauCandViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewClosestDeltaRSelector);
