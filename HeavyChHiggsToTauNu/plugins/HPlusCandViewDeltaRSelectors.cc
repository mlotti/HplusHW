#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CandViewDeltaRSelector.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

typedef hplus::CandViewDeltaRSelector<pat::Tau> HPlusPATTauCandViewDeltaRSelector;
typedef hplus::CandViewDeltaRSelector<reco::PFCandidate> HPlusPFCandCandViewDeltaRSelector;

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);
DEFINE_FWK_MODULE(HPlusPFCandCandViewDeltaRSelector);
