#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/SingleObjectSelector.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef SingleObjectSelector<
  edm::View<reco::Candidate>,
  StringCutObjectSelector<reco::Candidate, true>,
  edm::PtrVector<reco::Candidate>
> HPlusCandViewLazyPtrSelector;

DEFINE_FWK_MODULE(HPlusCandViewLazyPtrSelector);
