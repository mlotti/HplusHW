#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexZSelector.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/ObjectSelector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

typedef ObjectSelector<
  VertexZSelector<
    edm::View<reco::Candidate>,
    edm::PtrVector<reco::Candidate>
    >,
  edm::PtrVector<reco::Candidate>
  > HPlusCandViewPtrVertexZSelector;

typedef ObjectSelector<
  VertexZSelector<
    edm::View<pat::Muon>,
    std::vector<pat::Muon>
    >,
  std::vector<pat::Muon>
  > HPlusPATMuonViewVertexZSelector;

DEFINE_FWK_MODULE( HPlusCandViewPtrVertexZSelector );
DEFINE_FWK_MODULE( HPlusPATMuonViewVertexZSelector );
