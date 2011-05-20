#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/UtilAlgos/interface/ExpressionHisto.h"

typedef HPlus::MultiHistoAnalyzer<reco::CandidateView, ExpressionHisto> HPlusCandViewMultiHistoAnalyzer;

DEFINE_FWK_MODULE( HPlusCandViewMultiHistoAnalyzer );
