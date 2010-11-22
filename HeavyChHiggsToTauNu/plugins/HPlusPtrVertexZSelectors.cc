#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ViewPtrVertexZSelector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

typedef ViewPtrVertexZSelector<reco::Candidate> HPlusCandViewPtrVertexZSelector;
typedef ViewPtrVertexZSelector<pat::Muon> HPlusPATMuonViewPtrVertexZSelector;

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewPtrVertexZSelector);
DEFINE_FWK_MODULE(HPlusPATMuonViewPtrVertexZSelector);
