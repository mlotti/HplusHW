#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHisto.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef HPlus::MultiHistoAnalyzer<reco::CandidateView, HPlus::ExpressionEfficiencyHistoPerEvent> HPlusCandViewMultiEfficiencyPerEventAnalyzer;

DEFINE_FWK_MODULE( HPlusCandViewMultiEfficiencyPerEventAnalyzer );
