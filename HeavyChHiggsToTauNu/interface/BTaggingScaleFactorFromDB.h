#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTaggingScaleFactorFromDB_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTaggingScaleFactorFromDB_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "RecoBTag/Records/interface/BTagPerformanceRecord.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"

#include <string>
#include <cmath>

class BTaggingScaleFactorFromDB {

    public:
	class Data {
	    public:
		Data(double,double,double,double,double,double,double,double);

                double btagEfficiency();
                double btagEfficiencyError();
                double mistagEfficiency();
                double mistagEfficiencyError();
	
		double btagScaleFactor();
		double btagScaleFactorError();
		double mistagScaleFactor();	
		double mistagScaleFactorError();
	
	    private:
		double btagEff_,btagErr_,mistagEff_,mistagErr_;
		double btagSF_,bSFerr_,mistagSF_,mistagSFerr_;
	};

    public:
	BTaggingScaleFactorFromDB(const edm::ParameterSet&);
	~BTaggingScaleFactorFromDB();

	void setup(const edm::EventSetup&);
	Data getScaleFactors(double,double);

    private:
	std::string algoName, userAlgoName;

	edm::ESHandle<BtagPerformance> bHandle;
	edm::ESHandle<BtagPerformance> misHandle;
	edm::ESHandle<BtagPerformance> userHandle;
};

#endif
