#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MultiHistoAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"

typedef MultiHistoAnalyzer<reco::CandidateView> CandViewMultiHistoAnalyzer;

DEFINE_FWK_MODULE( CandViewMultiHistoAnalyzer );
