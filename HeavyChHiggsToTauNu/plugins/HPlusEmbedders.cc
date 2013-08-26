#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauLikeIsolationEmbedder.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenEmbedder.h"


typedef HPlus::TauLikeIsolationEmbedder<edm::View<pat::Muon>, pat::Muon> HPlusPATMuonViewTauLikeIsolationEmbedder;
typedef HPlus::GenEmbedder<edm::View<pat::Muon>, pat::Muon> HPlusPATMuonViewGenEmbedder;

typedef HPlus::TauLikeIsolationEmbedder<edm::View<pat::Tau>, pat::Tau> HPlusPATTauViewIsolationEmbedder;

DEFINE_FWK_MODULE( HPlusPATMuonViewTauLikeIsolationEmbedder );
DEFINE_FWK_MODULE( HPlusPATMuonViewGenEmbedder );

DEFINE_FWK_MODULE( HPlusPATTauViewIsolationEmbedder );
