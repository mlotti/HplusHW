#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingScaleFactorFromDB.h"

BTaggingScaleFactorFromDB::Data::Data(double btagEff,
                                      double btagErr,
                                      double mistagEff,
                                      double mistagErr,
                                      double btagSF,
                                      double bSFerr,
                                      double mistagSF,
                                      double mistagSFerr){
	btagEff_     = btagEff;
	btagErr_     = btagErr;
	mistagEff_   = mistagEff;
	mistagErr_   = mistagErr;
	btagSF_      = btagSF;
	bSFerr_      = bSFerr;
	mistagSF_    = mistagSF;
	mistagSFerr_ = mistagSFerr;
}
double BTaggingScaleFactorFromDB::Data::btagEfficiency(){ return btagEff_;}
double BTaggingScaleFactorFromDB::Data::btagEfficiencyError(){ return btagErr_;}
double BTaggingScaleFactorFromDB::Data::mistagEfficiency(){ return mistagEff_;}
double BTaggingScaleFactorFromDB::Data::mistagEfficiencyError(){ return mistagErr_;}
double BTaggingScaleFactorFromDB::Data::btagScaleFactor(){ return btagSF_;}
double BTaggingScaleFactorFromDB::Data::btagScaleFactorError(){return bSFerr_;}
double BTaggingScaleFactorFromDB::Data::mistagScaleFactor(){return mistagSF_;}
double BTaggingScaleFactorFromDB::Data::mistagScaleFactorError(){return mistagSFerr_;}


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

	// btag
        const BtagPerformance & bperf    = *(bHandle.product());
	const BtagPerformance & userperf = *(userHandle.product());

	// mistag
        const BtagPerformance & misperf  = *(misHandle.product());

        BinningPointByMap measurePoint;
        measurePoint.insert(BinningVariables::JetEt,pt);
        measurePoint.insert(BinningVariables::JetAbsEta,fabs(eta));

	double btagEff              = userperf.getResult(PerformanceResult::BTAGBEFF, measurePoint);
	double btagErr              = userperf.getResult(PerformanceResult::BTAGBERR, measurePoint);
	double mistagEff            = misperf.getResult(PerformanceResult::BTAGLEFF, measurePoint);
	double mistagErr	    = misperf.getResult(PerformanceResult::BTAGLERR, measurePoint);

        double scaleFactorBtag      = bperf.getResult(PerformanceResult::BTAGBEFFCORR, measurePoint);
        double scaleFactorBtagErr   = bperf.getResult(PerformanceResult::BTAGBERRCORR, measurePoint);
        double scaleFactorMistag    = misperf.getResult(PerformanceResult::BTAGLEFFCORR, measurePoint);
	double scaleFactorMistagErr = misperf.getResult(PerformanceResult::BTAGLERRCORR, measurePoint);

	return Data(btagEff,btagErr,mistagEff,mistagErr,
                    scaleFactorBtag,scaleFactorBtagErr,scaleFactorMistag,scaleFactorMistagErr);
}
