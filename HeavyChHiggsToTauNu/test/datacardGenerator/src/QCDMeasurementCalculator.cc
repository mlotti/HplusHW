#include "QCDMeasurementCalculator.h"
#include "Dataset.h"
#include "TMath.h"
#include "TH1F.h"

#include <iostream>


QCDMeasurementCalculator::QCDMeasurementCalculator() {
  bIsCalculated = false;
  fResultRelativeUncertainty = 0.0;
  fResultValue = 0.0;
}

QCDMeasurementCalculator::~QCDMeasurementCalculator() {

}

bool QCDMeasurementCalculator::addDatasets(std::string path, std::vector< std::string > mcEWKnames, std::vector< std::string > dataNames) {
  for (std::vector< std::string >::iterator it = mcEWKnames.begin(); it != mcEWKnames.end(); ++it) {
    std::string myCombinedName = path+"/"+(*it);
    if (!path.size())
      myCombinedName = (*it);
    Dataset* myDataset = new Dataset(myCombinedName);
    // Check that file has been opened successfully
    if (myDataset->getFile() < 0) {
      std::cout << "Tried to open file '" << *it << "'" << std::endl;
      return false;
    }
    vMCEWK.push_back(myDataset);
  }
  for (std::vector< std::string >::iterator it = dataNames.begin(); it != dataNames.end(); ++it) {
    std::string myCombinedName = path+"/"+(*it);
    if (!path.size())
      myCombinedName = (*it);
    Dataset* myDataset = new Dataset(myCombinedName);
    // Check that file has been opened successfully
    if (myDataset->getFile() < 0) {
      std::cout << "Tried to open file '" << *it << "'" << std::endl;
      return false;
    }
    vData.push_back(myDataset);
  }
  return true;
}

void QCDMeasurementCalculator::setMeasurementInfo(std::string histoPrefix, std::string bigboxHisto, std::string afterTauLegHisto, std::string afterMETLegHisto) {
  sHistoPrefix = histoPrefix;
  sBigboxHisto = bigboxHisto;
  sAfterMETLegHisto = afterMETLegHisto;
  sAfterTauLegHisto = afterTauLegHisto;
}

void QCDMeasurementCalculator::doCalculate() {
  bIsCalculated = true;
  double myResult = 0.;
  double myStatUncertaintySq = 0.;
  // Obtain number of bins
  TH1F* myHisto = getHistogram(vData[0]->getFile(), sBigboxHisto);
  if (!myHisto) return;
  int nBins = myHisto->GetNbinsX();
  // Loop over bins
  for (int i = 1; i <= nBins; ++i) {
    // MC EWK counts for the bin
    double myEWKBigBoxCounts = 0.;
    double myEWKTauLegCounts = 0.;
    double myEWKMETLegCounts = 0.;
    double myEWKBigBoxCountsUncertSq = 0.;
    double myEWKTauLegCountsUncertSq = 0.;
    double myEWKMETLegCountsUncertSq = 0.;
    if (!getMeasurementCounts(vMCEWK, i, myEWKBigBoxCounts, myEWKMETLegCounts, myEWKTauLegCounts, myEWKBigBoxCountsUncertSq, myEWKMETLegCountsUncertSq, myEWKTauLegCountsUncertSq))
      return;
    // data counts for the bin
    double myDataBigBoxCounts = 0.;
    double myDataTauLegCounts = 0.;
    double myDataMETLegCounts = 0.;
    double myDataBigBoxCountsUncertSq = 0.;
    double myDataTauLegCountsUncertSq = 0.;
    double myDataMETLegCountsUncertSq = 0.;
    if (!getMeasurementCounts(vData, i, myDataBigBoxCounts, myDataMETLegCounts, myDataTauLegCounts, myDataBigBoxCountsUncertSq, myDataMETLegCountsUncertSq, myDataTauLegCountsUncertSq))
      return;
    // Obtain result for the bin
    myResult += (myDataTauLegCounts-myEWKTauLegCounts) * 
      (myDataMETLegCounts-myEWKMETLegCounts) /
      (myDataBigBoxCounts-myEWKBigBoxCounts);
    // Obtain squared statistical uncertainty
    myStatUncertaintySq += (myDataMETLegCountsUncertSq+myEWKMETLegCountsUncertSq) / (myEWKMETLegCounts-myEWKMETLegCounts)
      + (myDataTauLegCountsUncertSq+myEWKTauLegCountsUncertSq) / (myDataTauLegCounts-myEWKTauLegCounts);
    // FIXME add syst. uncert to MC EWK
  }
  // Store result
  fResultValue = myResult;
  fResultRelativeUncertainty = TMath::Sqrt(myStatUncertaintySq);
}

bool QCDMeasurementCalculator::getMeasurementCounts(std::vector< Dataset* >& datasets, int bin, double& afterBigBox, double& afterMETLeg, double& afterTauLeg, double& afterBigBoxUncertSq, double& afterMETLegUncertSq, double& afterTauLegUncertSq) {
  for (size_t i = 0; i < datasets.size(); ++i) {
    TH1F* myBigboxHisto = getHistogram(datasets[i]->getFile(), sBigboxHisto);
    if (!myBigboxHisto) return false;
    TH1F* myTauLegHisto = getHistogram(datasets[i]->getFile(), sAfterTauLegHisto);
    if (!myTauLegHisto) return false;
    TH1F* myMETLegHisto = getHistogram(datasets[i]->getFile(), sAfterMETLegHisto);
    if (!myMETLegHisto) return false;
    afterBigBox += myBigboxHisto->GetBinContent(i);
    afterBigBoxUncertSq += myBigboxHisto->GetBinError(i)*myBigboxHisto->GetBinError(i);
    afterMETLeg += myMETLegHisto->GetBinContent(i);
    afterMETLegUncertSq += myMETLegHisto->GetBinError(i)*myMETLegHisto->GetBinError(i);
    afterTauLeg += myTauLegHisto->GetBinContent(i);
    afterTauLegUncertSq += myTauLegHisto->GetBinError(i)*myTauLegHisto->GetBinError(i);
  }
  return true;
}


TH1F* QCDMeasurementCalculator::getHistogram(TFile* f, std::string name) {
  std::string myCombinedName = sHistoPrefix + "/" + name;
  TH1F* h = dynamic_cast<TH1F*>(f->Get(myCombinedName.c_str()));
  if (!h)
    std::cout << "Error: Cannot find histogram: " << myCombinedName << std::endl;
  return h;
}
