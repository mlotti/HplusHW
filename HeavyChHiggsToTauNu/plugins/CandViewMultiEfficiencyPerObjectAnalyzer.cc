#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHisto.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef MultiHistoAnalyzer<reco::CandidateView, ExpressionEfficiencyHistoPerObject> CandViewMultiEfficiencyPerObjectAnalyzer;

DEFINE_FWK_MODULE( CandViewMultiEfficiencyPerObjectAnalyzer );
