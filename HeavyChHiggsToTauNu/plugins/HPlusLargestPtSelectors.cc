#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/ObjectSelector.h"
#include "CommonTools/UtilAlgos/interface/SortCollectionSelector.h"
#include "CommonTools/Utils/interface/PtComparator.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include<vector>

typedef ObjectSelector<
  SortCollectionSelector<
    std::vector<pat::Muon>,
    GreaterByPt<pat::Muon>
    >
  > HPlusLargestPtPATMuonSelector;

typedef ObjectSelector<
  SortCollectionSelector<
    edm::View<pat::Muon>,
    GreaterByPt<pat::Muon>,
    std::vector<pat::Muon>
    >,
  std::vector<pat::Muon>
  > HPlusLargestPtPATMuonViewSelector;

typedef ObjectSelector<
  SortCollectionSelector<
    edm::View<reco::Candidate>,
    GreaterByPt<reco::Candidate>,
    edm::PtrVector<reco::Candidate>
    >,
  edm::PtrVector<reco::Candidate>
  > HPlusLargestPtCandViewPtrSelector;


DEFINE_FWK_MODULE( HPlusLargestPtPATMuonSelector );
DEFINE_FWK_MODULE( HPlusLargestPtPATMuonViewSelector );
DEFINE_FWK_MODULE( HPlusLargestPtCandViewPtrSelector );
