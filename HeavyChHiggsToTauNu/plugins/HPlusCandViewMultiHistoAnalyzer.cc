#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HPlusMultiHistoAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/UtilAlgos/interface/ExpressionHisto.h"

typedef HPlusMultiHistoAnalyzer<reco::CandidateView, ExpressionHisto> HPlusCandViewMultiHistoAnalyzer;

DEFINE_FWK_MODULE( HPlusCandViewMultiHistoAnalyzer );
