#include "QCDMeasurementCalculator.h"
#include "Dataset.h"
#include "NormalisationInfo.h"
#include "TMath.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"

#include <iostream>


QCDMeasurementCalculator::QCDMeasurementCalculator(std::string id)
: Extractable(id) {
  reset();
}

QCDMeasurementCalculator::QCDMeasurementCalculator(std::string mode, std::string id, std::string distribution, std::string description)
: Extractable(id, distribution, description) {
  reset();
  if (mode == "statistics")
    bStatisticsMode = true;
  else if (mode == "systematics")
    bSystematicsMode = true;
  else
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Unknown QCD mode '" << mode << "'! Options: statistics or systematics" << std::endl;
}

QCDMeasurementCalculator::~QCDMeasurementCalculator() {
}

void QCDMeasurementCalculator::reset() {
  fNormalisationInfo = 0;
  bIsCalculated = false;
  bStatisticsMode = false;
  bSystematicsMode = false;
  fResultRelativeStatisticalUncertainty = 0.0;
  fResultRelativeSystematicalUncertainty = 0.0;
  fResultValue = 0.0;
  hCtrlSystematics = 0;
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
  sAfterMETLegHisto = histoPrefix + "/" + afterMETLegHisto;
  sAfterTauLegHisto = histoPrefix + "/" + afterTauLegHisto;
}

void QCDMeasurementCalculator::setNormalisationInfo(NormalisationInfo* info, std::string counterHisto) {
  fNormalisationInfo = new NormalisationInfo(info->getConfigInfoHisto(), counterHisto, info->getLuminosity());
}

void QCDMeasurementCalculator::doCalculate() {
  if (bIsCalculated) return;
  if (!fNormalisationInfo) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m You forgot to call setNormalisationInfo for QCDMeasurement!" << std::endl;
    return;
  }
  bIsCalculated = true;
  // Obtain number of bins
  TH1* myHisto = getHistogram(vData[0]->getFile(), sBigboxHisto);
  if (!myHisto) return;
  int nBins = myHisto->GetNbinsX();

  // Create control histogram
  TFile* myFile = 0;
  std::string myQCDCtrlName = "QCDMeasurementControlPlots.root";
  if (isRate()) { // do only once
    myFile = TFile::Open(myQCDCtrlName.c_str(), "RECREATE");
    if (!myFile) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot open root file for output!" << std::endl;
      return;
    }
    myFile->cd();
  }
  hCtrlSystematics = new TH2F("CtrlNQCD_Systematics", "CtrlNQCD_Systematics", nBins-1, 1., nBins, 6, 0, 6);
  hCtrlSystematics->SetXTitle("tau p_{T} bin, GeV/c");
  hCtrlSystematics->SetYTitle("Abs. uncertainty");
  hCtrlSystematics->GetYaxis()->SetBinLabel(1, "data stat., #tau leg}");
  hCtrlSystematics->GetYaxis()->SetBinLabel(2, "MC EWK stat., #tau leg}");
  hCtrlSystematics->GetYaxis()->SetBinLabel(3, "MC EWK syst., #tau leg}");
  hCtrlSystematics->GetYaxis()->SetBinLabel(4, "data stat., MET leg}");
  hCtrlSystematics->GetYaxis()->SetBinLabel(5, "MC EWK stat., MET leg}");
  hCtrlSystematics->GetYaxis()->SetBinLabel(6, "MC EWK syst., MET leg}");
  hCtrlSystematics->GetXaxis()->SetBinLabel(1, "40-50");
  hCtrlSystematics->GetXaxis()->SetBinLabel(2, "50-60");
  hCtrlSystematics->GetXaxis()->SetBinLabel(3, "60-70");
  hCtrlSystematics->GetXaxis()->SetBinLabel(4, "70-80");
  hCtrlSystematics->GetXaxis()->SetBinLabel(5, "80-100");
  hCtrlSystematics->GetXaxis()->SetBinLabel(6, "100-120");
  hCtrlSystematics->GetXaxis()->SetBinLabel(7, "120-150");
  hCtrlSystematics->GetXaxis()->SetBinLabel(8, ">150");
  hMETLegEfficiency = new TH1F("CtrlNQCD_METLeg_Efficiency", "CtrlNQCD_METLeg_Efficiency", nBins, 0, nBins);
  hTauLegEfficiency = new TH1F("CtrlNQCD_TauLeg_Efficiency", "CtrlNQCD_TauLeg_Efficiency", nBins, 0, nBins);
  hBigboxPurity = new TH1F("CtrlNQCD_BigboxLeg_Purity", "CtrlNQCD_BigboxLeg_Purity", nBins, 0, nBins);
  hMETLegPurity = new TH1F("CtrlNQCD_METLeg_Purity", "CtrlNQCD_METLeg_Purity", nBins, 0, nBins);
  hTauLegPurity = new TH1F("CtrlNQCD_TauLeg_Purity", "CtrlNQCD_TauLeg_Purity", nBins, 0, nBins);

  if (isRate()) { // print only once
    std::cout << "... QCD Measurement calculation ..." << std::endl;
    for (size_t i = 0; i < vData.size(); ++i)
      std::cout << "  data dataset=" << vData[i]->getFilename() << std::endl;
    for (size_t i = 0; i < vMCEWK.size(); ++i)
      std::cout << "  MC EWK dataset=" << vMCEWK[i]->getFilename() << " norm.fact.=" << fNormalisationInfo->getNormalisationFactor(vMCEWK[i]->getFile()) << std::endl;
  }
  
  // Loop over bins to get NQCD
  double myResultNQCD = 0.0;
  double myStatUncertaintySqNQCD = 0.0;
  double mySystUncertaintySqNQCD = 0.0;
  for (int i = 1; i <= nBins; ++i) {
    double myBigBoxCounts = getMeasurementCounts(vData, i, sBigboxHisto, true) - getMeasurementCounts(vMCEWK, i, sBigboxHisto);
    if (myBigBoxCounts < 0.0001) continue;
    double myMETLegCounts = getMeasurementCounts(vData, i, sAfterMETLegHisto, true) - getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto);
    double myTauLegCounts = getMeasurementCounts(vData, i, sAfterTauLegHisto, true) - getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto);
    //std::cout << "bin=" << i << " bb=" << myBigBoxCounts << " metleg=" << myMETLegCounts << " tauleg=" << myTauLegCounts << " nQCD=" << myTauLegCounts * myMETLegCounts / myBigBoxCounts << std::endl;
    //std::cout << "bin=" << i << " met leg DATA = " << getMeasurementCounts(vData, i, sAfterMETLegHisto, true) << "+-" << getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true) << " tau leg DATA = " << getMeasurementCounts(vData, i, sAfterTauLegHisto, true) << "+-" << getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) << std::endl;
    // Obtain result for the bin
    double myNQCDForThisBin = myTauLegCounts * myMETLegCounts / myBigBoxCounts;
    myResultNQCD += myNQCDForThisBin;
    // Calculate systematics for MET leg
    double myDataStatUncertaintySq = getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true) * TMath::Power(myNQCDForThisBin / myMETLegCounts, 2);
    double myEWKStatUncertaintySq = getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterMETLegHisto) * TMath::Power(myNQCDForThisBin / myMETLegCounts, 2);
    myStatUncertaintySqNQCD += (myDataStatUncertaintySq + myEWKStatUncertaintySq);
    mySystUncertaintySqNQCD += TMath::Power(getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto)*0.20 * myNQCDForThisBin / myMETLegCounts, 2);
    hCtrlSystematics->SetBinContent(i-1, 4, TMath::Sqrt(myDataStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 5, TMath::Sqrt(myEWKStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 6, getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto)*0.20 * myNQCDForThisBin / myMETLegCounts); // assume 15 % syst.
    // Calculate systematics for tau leg
    myDataStatUncertaintySq = getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) * TMath::Power(myNQCDForThisBin / myTauLegCounts, 2);
    myEWKStatUncertaintySq = getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto) * TMath::Power(myNQCDForThisBin / myTauLegCounts, 2);
    //std::cout << "bin=" << i << " abs. stat. uncert = (" << myDataStatUncertaintySq << ", " << myEWKStatUncertaintySq  << "), tot=" << (myDataStatUncertaintySq + myEWKStatUncertaintySq) << std::endl;
    //std::cout << "bin=" << i << " abs. stat. uncert = (" << TMath::Sqrt(myDataStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << ", " << TMath::Sqrt(myEWKStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << "), tot=" << TMath::Sqrt(myDataStatUncertaintySq + myEWKStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << std::endl;
    //std::cout << "bin=" << i << " rel. stat. uncert = (" << TMath::Sqrt(myDataStatUncertaintySq)/myResultNQCD << "), " << TMath::Sqrt(myEWKStatUncertaintySq)/myResultNQCD << ", tot=" << TMath::Sqrt(myDataStatUncertaintySq + myEWKStatUncertaintySq)/myResultNQCD << std::endl;
    myStatUncertaintySqNQCD += (myDataStatUncertaintySq + myEWKStatUncertaintySq);
    mySystUncertaintySqNQCD += TMath::Power(getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.15 * myNQCDForThisBin / myTauLegCounts, 2);
    hCtrlSystematics->SetBinContent(i-1, 1, TMath::Sqrt(myDataStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 2, TMath::Sqrt(myEWKStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 3, getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.15 * myNQCDForThisBin / myTauLegCounts); // assume 20 % syst.
    // Fill efficiency histograms
    hMETLegEfficiency->SetBinContent(i, myMETLegCounts / myBigBoxCounts);
    hMETLegEfficiency->SetBinError(i, TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true)) / myBigBoxCounts);
    hTauLegEfficiency->SetBinContent(i, myTauLegCounts / myBigBoxCounts);
    hTauLegEfficiency->SetBinError(i, TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true)) / myBigBoxCounts);
    // Fill purity histograms
    // purity = D-E / D  = 1-E/D
    // delta^2 = (E/D^2*delta_D)^2 + (1/D*delta_E)^2 = 1/D^4*(E^2*delta_D^2 + D^2*delta_E^2)
    hBigboxPurity->SetBinContent(i, myBigBoxCounts / getMeasurementCounts(vData, i, sBigboxHisto, true));
    double a = getMeasurementCounts(vMCEWK, i, sBigboxHisto) / getMeasurementCounts(vData, i, sBigboxHisto, true) /
      getMeasurementCounts(vData, i, sBigboxHisto, true);
    double b = 1.0 / getMeasurementCounts(vData, i, sBigboxHisto, true);
    hBigboxPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sBigboxHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sBigboxHisto)));
    hMETLegPurity->SetBinContent(i, myMETLegCounts / getMeasurementCounts(vData, i, sAfterMETLegHisto, true));
    a = getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto) / getMeasurementCounts(vData, i, sAfterMETLegHisto, true) /
      getMeasurementCounts(vData, i, sAfterMETLegHisto, true);
    b = 1.0 / getMeasurementCounts(vData, i, sAfterMETLegHisto, true);
    hMETLegPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterMETLegHisto)));
    hTauLegPurity->SetBinContent(i, myTauLegCounts / getMeasurementCounts(vData, i, sAfterTauLegHisto, true));
    a = getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto) / getMeasurementCounts(vData, i, sAfterTauLegHisto, true) /
      getMeasurementCounts(vData, i, sAfterTauLegHisto, true);
    b = 1.0 / getMeasurementCounts(vData, i, sAfterTauLegHisto, true);
    hTauLegPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto)));
  }

  // Store result
  fResultValue = myResultNQCD;
  fResultRelativeStatisticalUncertainty = TMath::Sqrt(myStatUncertaintySqNQCD) / myResultNQCD;
  fResultRelativeSystematicalUncertainty = TMath::Sqrt(mySystUncertaintySqNQCD) / myResultNQCD;

  if (isRate()) { // do only once
    std::cout << "QCD result: " << fResultValue
              << " +- " << fResultRelativeStatisticalUncertainty << " % stat."
              << " +- " << fResultRelativeSystematicalUncertainty << " % syst." << std::endl;
    myFile->Write();
    myFile->Close();
    std::cout << "Control histograms written to " << myQCDCtrlName << std::endl;
    std::cout << "... QCD Measurement done ..." << std::endl;
  }
}

double QCDMeasurementCalculator::getMeasurementCounts(std::vector< Dataset* >& datasets, int bin, std::string histoName, bool isData) {
  double myValue = 0.0;
  for (size_t i = 0; i < datasets.size(); ++i) {
    TH1* myHisto = getHistogram(datasets[i]->getFile(), histoName);
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram '" << histoName << "' in file '" << datasets[i]->getFilename() << "'!" << std::endl;
      return -1.;
    }
    if (isData)
      myValue += myHisto->GetBinContent(bin);
    else
      myValue += myHisto->GetBinContent(bin) * fNormalisationInfo->getNormalisationFactor(datasets[i]->getFile());
  }
  return myValue;
}

double QCDMeasurementCalculator::getMeasurementAbsUncertaintySquared(std::vector< Dataset* >& datasets, int bin, std::string histoName, bool isData) {
  double myValue = 0.0;
  for (size_t i = 0; i < datasets.size(); ++i) {
    TH1* myHisto = getHistogram(datasets[i]->getFile(), histoName);
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram '" << histoName << "' in file '" << datasets[i]->getFilename() << "'!" << std::endl;
      return -1.;
    }
    double a = myHisto->GetBinError(bin);
    if (!isData)
      a *= fNormalisationInfo->getNormalisationFactor(datasets[i]->getFile());
    myValue += a * a;
  }
  return myValue;
}

TH1* QCDMeasurementCalculator::getHistogram(TFile* f, std::string name) {
  TH1F* h = dynamic_cast<TH1F*>(f->Get(name.c_str()));
  if (!h)
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram: " << name << std::endl;
  return h;
}

double QCDMeasurementCalculator::doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info) {
  if (!bIsCalculated) doCalculate();
  if (isRate())
    return fResultValue;
  if (bStatisticsMode)
    return fResultRelativeStatisticalUncertainty;
  else if (bSystematicsMode)
    return fResultRelativeSystematicalUncertainty;
  return 0.;
}