#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/Merger.h"
//#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include<vector>

typedef Merger< pat::TauCollection > HPlusPATTauMerger;

DEFINE_FWK_MODULE( HPlusPATTauMerger );
