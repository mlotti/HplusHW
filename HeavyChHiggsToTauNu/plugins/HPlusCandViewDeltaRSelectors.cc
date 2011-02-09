#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CandViewDeltaRSelector.h"

#include "DataFormats/PatCandidates/interface/Tau.h"


typedef hplus::CandViewDeltaRSelector<pat::Tau> HPlusPATTauCandViewDeltaRSelector;

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPATTauCandViewDeltaRSelector);
