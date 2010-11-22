#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewPtrVertexZSelector.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef ViewPtrVertexZSelector<reco::Candidate> HPlusCandViewPtrVertexZSelector;

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewPtrVertexZSelector);
