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
    Data();
    ~Data();

    const double btagEfficiency() const { return btagEff_; }
    const double btagEfficiencyError() const { return btagErr_; }
    const double mistagEfficiency() const { return mistagEff_; }
    const double mistagEfficiencyError() const { return mistagErr_; }

    const double btagScaleFactor() const { return btagSF_; }
    const double btagScaleFactorError() const { return bSFerr_; }
    const double mistagScaleFactor() const { return mistagSF_; }
    const double mistagScaleFactorError() const { return mistagSFerr_; }

    friend class BTaggingScaleFactorFromDB;

  private:
    double btagEff_,btagErr_,mistagEff_,mistagErr_;
    double btagSF_,bSFerr_,mistagSF_,mistagSFerr_;
  };

  BTaggingScaleFactorFromDB(const edm::ParameterSet&);
  ~BTaggingScaleFactorFromDB();

  void setup(const edm::EventSetup&);
  Data getScaleFactors(double,double);

private:
  std::string algoName, userAlgoName, payloadName;

  edm::ESHandle<BtagPerformance> bHandle;
  edm::ESHandle<BtagPerformance> misHandle;
  edm::ESHandle<BtagPerformance> userHandle;
};

#endif
