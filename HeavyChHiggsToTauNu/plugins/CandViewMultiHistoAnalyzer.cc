#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "CommonTools/UtilAlgos/interface/ExpressionHisto.h"

typedef MultiHistoAnalyzer<reco::CandidateView, ExpressionHisto> CandViewMultiHistoAnalyzer;

DEFINE_FWK_MODULE( CandViewMultiHistoAnalyzer );
