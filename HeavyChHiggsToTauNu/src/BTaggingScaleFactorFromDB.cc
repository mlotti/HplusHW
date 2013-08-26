#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingScaleFactorFromDB.h"

BTaggingScaleFactorFromDB::Data::Data() :
btagEff_(0),
btagErr_(0),
mistagEff_(0),
mistagErr_(0),
btagSF_(0),
bSFerr_(0),
mistagSF_(0),
mistagSFerr_(0) { }

BTaggingScaleFactorFromDB::Data::~Data() { }

BTaggingScaleFactorFromDB::BTaggingScaleFactorFromDB(const edm::ParameterSet& iConfig):
  algoName(iConfig.getUntrackedParameter<std::string>("BTagDBAlgo")),
  userAlgoName(iConfig.getUntrackedParameter<std::string>("BTagUserDBAlgo"))
{}

BTaggingScaleFactorFromDB::~BTaggingScaleFactorFromDB(){}

void BTaggingScaleFactorFromDB::setup(const edm::EventSetup& iSetup){
  // btag
  iSetup.get<BTagPerformanceRecord>().get("BTAG" + algoName,bHandle);
  iSetup.get<BTagPerformanceRecord>().get(userAlgoName,userHandle);
  
  // mistag
  iSetup.get<BTagPerformanceRecord>().get("MISTAG" + algoName,misHandle);
}
BTaggingScaleFactorFromDB::Data BTaggingScaleFactorFromDB::getScaleFactors(double pt,double eta){
  Data output;
  // btag
  const BtagPerformance & bperf    = *(bHandle.product());
  const BtagPerformance & userperf = *(userHandle.product());

  // mistag
  const BtagPerformance & misperf  = *(misHandle.product());

  BinningPointByMap measurePoint;
  measurePoint.insert(BinningVariables::JetEt,pt);
  measurePoint.insert(BinningVariables::JetAbsEta,fabs(eta));

  output.btagEff_     = userperf.getResult(PerformanceResult::BTAGBEFF, measurePoint);
  output.btagErr_     = userperf.getResult(PerformanceResult::BTAGBERR, measurePoint);
  output.mistagEff_   = misperf.getResult(PerformanceResult::BTAGLEFF, measurePoint);
  output.mistagErr_   = misperf.getResult(PerformanceResult::BTAGLERR, measurePoint);
  output.btagSF_      = bperf.getResult(PerformanceResult::BTAGBEFFCORR, measurePoint);
  output.bSFerr_      = bperf.getResult(PerformanceResult::BTAGBERRCORR, measurePoint);
  output.mistagSF_    = misperf.getResult(PerformanceResult::BTAGLEFFCORR, measurePoint);
  output.mistagSFerr_ = misperf.getResult(PerformanceResult::BTAGLERRCORR, measurePoint);

  return output;
}
