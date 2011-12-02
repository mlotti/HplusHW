#ifndef QCDMEASUREMENTCALCULATOR_H
#define QCDMEASUREMENTCALCULATOR_H

#include <vector>
#include <string>
#include "Extractable.h"

class TH2;
class TH1;
class TFile;
class Dataset;
class NormalisationInfo;
class QCDMeasurementCalculator : public Extractable {

public:
  /// Constructor for rate
  QCDMeasurementCalculator(std::string id);
  /// Constructor foNormalisationInfo* infor systematics
  QCDMeasurementCalculator(std::string mode, std::string id, std::string distribution, std::string description);
  /// Default desctructor
  virtual ~QCDMeasurementCalculator();

  /// No datasets should be supplied here
  double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  void addHistogramsToFile(std::string label, std::string id, TFile* f);
  
  bool addDatasets(std::string path, std::vector< std::string > mcEWKnames, std::vector< std::string > dataNames);
  void setMeasurementInfo(std::string histoPrefix, std::string bigboxHisto, std::string afterTauLegHisto, std::string afterMETLegHisto);
  void setTransverseMassInfo(std::string histoPrefix, std::string basicMtHisto);
  void setNormalisationInfo(NormalisationInfo* info, std::string counterHisto);
  
private:
  void reset();
  void doCalculate();
  TH1* getHistogram(TFile* f, std::string name);
  bool getMergedMtHistogramForAPtBin(int bin, std::string histoName, TH1* h, TH2* dataStat, TH2* ewkStat, TH2* ewkSyst);
  double getMeasurementCounts(std::vector<Dataset*>& datasets, int bin, std::string histoName, bool isData = false);
  double getMeasurementAbsUncertaintySquared(std::vector<Dataset*>& datasets, int bin, std::string histoName, bool isData = false);
  
private:
  NormalisationInfo* fNormalisationInfo;
  
  std::vector<Dataset*> vMCEWK;
  std::vector<Dataset*> vData;
  
  bool bIsCalculated;
  bool bStatisticsMode;
  bool bSystematicsMode;
  double fResultValue;
  double fResultRelativeStatisticalUncertainty;
  double fResultRelativeSystematicalUncertainty;
  
  std::string sCounterHisto;
  
  std::string sHistoPrefix;
  std::string sBigboxHisto;
  std::string sAfterTauLegHisto;
  std::string sAfterMETLegHisto;
  std::string sBasicMtHisto;
  
  // Control histograms for systematics
  TH2* hCtrlSystematics;
  TH1* hMETLegEfficiency;
  TH1* hTauLegEfficiency;
  TH1* hBigboxPurity;
  TH1* hMETLegPurity;
  TH1* hTauLegPurity;
  // Control histograms for mT
  std::vector<TH1*> hBinnedMtShape;
  TH1* hBasicMtShape;
  TH2* hBasicMtShapeDataStat;
  TH2* hBasicMtShapeEWKStat;
  TH2* hBasicMtShapeEWKSyst;

  
  TH1* hMtShapeForResult;
  // FIXME add data-driven control plots
  
  
  
};

#endif // QCDMEASUREMENT_H
