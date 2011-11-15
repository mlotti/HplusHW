#ifndef QCDMEASUREMENTCALCULATOR_H
#define QCDMEASUREMENTCALCULATOR_H

#include <vector>
#include <string>

class TH1F;
class TFile;
class Dataset;
class QCDMeasurementCalculator {

public:
  QCDMeasurementCalculator();
  virtual ~QCDMeasurementCalculator();
  
  bool addDatasets(std::string path, std::vector< std::string > mcEWKnames, std::vector< std::string > dataNames);
  void setMeasurementInfo(std::string histoPrefix, std::string bigboxHisto, std::string afterTauLegHisto, std::string afterMETLegHisto);
  
  double getResult() { if (!bIsCalculated) doCalculate(); return fResultValue; }
  double getResultRelativeUncertainty() { if (!bIsCalculated) doCalculate(); return fResultRelativeUncertainty; }
  
private:
  void doCalculate();
  TH1F* getHistogram(TFile* f, std::string name);
  bool getMeasurementCounts(std::vector<Dataset*>& datasets, int bin, double& afterBigBox, double& afterMETLeg, double& afterTauLeg, double& afterBigBoxUncertSq, double& afterMETLegUncertSq, double& afterTauLegUncertSq);
  
private:
  
  std::vector<Dataset*> vMCEWK;
  std::vector<Dataset*> vData;
  
  bool bIsCalculated;
  double fResultValue;
  double fResultRelativeUncertainty;
  
  std::string sCounterHisto;
  
  std::string sHistoPrefix;
  std::string sBigboxHisto;
  std::string sAfterTauLegHisto;
  std::string sAfterMETLegHisto;
  
  // FIXME add mT histograms

  
  
  
};

#endif // QCDMEASUREMENT_H
