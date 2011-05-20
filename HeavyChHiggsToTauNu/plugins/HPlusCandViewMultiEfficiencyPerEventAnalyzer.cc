#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HPlusMultiHistoAnalyzer.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHisto.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef HPlusMultiHistoAnalyzer<reco::CandidateView, HPlus::ExpressionEfficiencyHistoPerEvent> HPlusCandViewMultiEfficiencyPerEventAnalyzer;

DEFINE_FWK_MODULE( HPlusCandViewMultiEfficiencyPerEventAnalyzer );
