#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CandViewDeltaRSelector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CandViewClosestDeltaRSelector.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

typedef hplus::CandViewDeltaRSelector<pat::Tau> HPlusPATTauCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);

typedef hplus::CandViewDeltaRSelector<reco::PFCandidate> HPlusPFCandCandViewDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPFCandCandViewDeltaRSelector);


typedef hplus::CandViewClosestDeltaRSelector<pat::Tau> HPlusPATTauCandViewClosestDeltaRSelector;
DEFINE_FWK_MODULE(HPlusPATTauCandViewClosestDeltaRSelector);
