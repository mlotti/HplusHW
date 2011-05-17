#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauLikeIsolationEmbedder.h"


typedef HPlus::TauLikeIsolationEmbedder<edm::View<pat::Muon>, pat::Muon> HPlusPATMuonViewTauLikeIsolationEmbedder;

DEFINE_FWK_MODULE( HPlusPATMuonViewTauLikeIsolationEmbedder );

