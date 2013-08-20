#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionHisto.h"

typedef HPlus::MultiHistoAnalyzer<reco::CandidateView, HPlus::ExpressionHisto> HPlusCandViewMultiHistoAnalyzer;

DEFINE_FWK_MODULE( HPlusCandViewMultiHistoAnalyzer );
