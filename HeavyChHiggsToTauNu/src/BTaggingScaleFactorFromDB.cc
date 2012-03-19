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
  algoName(iConfig.getParameter<std::string>("BTagDBAlgo"))
{}

BTaggingScaleFactorFromDB::~BTaggingScaleFactorFromDB(){}

void BTaggingScaleFactorFromDB::setup(const edm::EventSetup& iSetup){
        
        // btag
//        edm::ESHandle<BtagPerformance> bHandle;
        iSetup.get<BTagPerformanceRecord>().get("BTAG" + algoName,bHandle);
//        const BtagPerformance & bperf = *(bHandle.product());
        
        // mistag
//        edm::ESHandle<BtagPerformance> misHandle;
        iSetup.get<BTagPerformanceRecord>().get("MISTAG" + algoName,misHandle);
//        const BtagPerformance & misperf = *(misHandle.product());
	
}
BTaggingScaleFactorFromDB::Data BTaggingScaleFactorFromDB::getScaleFactors(double pt,double eta){

	// btag
//        edm::ESHandle<BtagPerformance> bHandle;
//        iSetup.get<BTagPerformanceRecord>().get("BTAG" + algoName,bHandle); 
        const BtagPerformance & bperf = *(bHandle.product());

	// mistag
//        edm::ESHandle<BtagPerformance> misHandle;
//        iSetup.get<BTagPerformanceRecord>().get("MISTAG" + algoName,misHandle);
        const BtagPerformance & misperf = *(misHandle.product());

        BinningPointByMap measurePoint;
        measurePoint.insert(BinningVariables::JetEt,pt);
        measurePoint.insert(BinningVariables::JetAbsEta,fabs(eta));

	double btagEff              = bperf.getResult(PerformanceResult::BTAGBEFF, measurePoint);
	double btagErr              = bperf.getResult(PerformanceResult::BTAGBERR, measurePoint);
	double mistagEff            = misperf.getResult(PerformanceResult::BTAGLEFF, measurePoint);
	double mistagErr	    = misperf.getResult(PerformanceResult::BTAGLERR, measurePoint);

        double scaleFactorBtag      = bperf.getResult(PerformanceResult::BTAGBEFFCORR, measurePoint);
        double scaleFactorBtagErr   = bperf.getResult(PerformanceResult::BTAGBERRCORR, measurePoint);
        double scaleFactorMistag    = misperf.getResult(PerformanceResult::BTAGLEFFCORR, measurePoint);
	double scaleFactorMistagErr = misperf.getResult(PerformanceResult::BTAGLERRCORR, measurePoint);

	return Data(btagEff,btagErr,mistagEff,mistagErr,
                    scaleFactorBtag,scaleFactorBtagErr,scaleFactorMistag,scaleFactorMistagErr);
}
