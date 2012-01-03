#include "QCDMeasurementCalculator.h"
#include "Dataset.h"
#include "NormalisationInfo.h"
#include "TMath.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"

#include <iostream>
#include <sstream>

QCDMeasurementCalculator::QCDMeasurementCalculator(std::string id)
: Extractable(id) {
  bDebug = !false;
  reset();
}

QCDMeasurementCalculator::QCDMeasurementCalculator(std::string mode, std::string id, std::string distribution, std::string description)
: Extractable(id, distribution, description) {
  bDebug = false;
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
  hBasicMtShapeEWKStat = 0;
  hBasicMtShape = 0;
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

void QCDMeasurementCalculator::setTransverseMassInfo(std::string histoPrefix, std::string basicMtHisto) {
  if (basicMtHisto.size())
    sBasicMtHisto = histoPrefix + "/" + basicMtHisto;
}

void QCDMeasurementCalculator::setNormalisationInfo(NormalisationInfo* info, std::string counterHisto) {
  fNormalisationInfo = new NormalisationInfo(info->getConfigInfoHisto(), counterHisto, info->getLuminosity(), info->getLuminosityScaling());

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
  for (int i = 1; i <= nBins; ++i) {
    std::stringstream s;
    s << "CtrlBasicMtShape_bin" << i;
    hBinnedMtShape.push_back(new TH1F(s.str().c_str(), s.str().c_str(), 20, 0, 400));
  }
  hBasicMtShape = new TH1F("CtrlBasicMtShape_Combined", "CtrlBasicMtShape_Combined", 20, 0, 400);
  hBasicMtShape->Sumw2();

  hBasicMtShapeDataStat = new TH2F("CtrlBasicMtShape_Systematics_DataStat", "CtrlBasicMtShape_Systematics_DataStat", 20, 0, 400, nBins-1, 1., nBins);
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(1, "40-50");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(2, "50-60");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(3, "60-70");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(4, "70-80");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(5, "80-100");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(6, "100-120");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(7, "120-150");
  hBasicMtShapeDataStat->GetYaxis()->SetBinLabel(8, ">150");
  hBasicMtShapeDataStat->SetYTitle("tau p_{T} bin, GeV/c");
  hBasicMtShapeDataStat->SetXTitle("m_{T}(tau,MET), GeV/c^{2}");
  
  if (!hBasicMtShapeEWKStat) {
    hBasicMtShapeEWKStat = dynamic_cast<TH2*>(hBasicMtShapeDataStat->Clone("CtrlBasicMtShape_Systematics_EWKStat"));
    hBasicMtShapeEWKSyst = dynamic_cast<TH2*>(hBasicMtShapeDataStat->Clone("CtrlBasicMtShape_Systematics_EWKSyst"));
  }
  
  std::cout << "... QCD Measurement calculation ..." << std::endl;
  if (isRate() && bDebug) { // print only once
    for (size_t i = 0; i < vData.size(); ++i)
      std::cout << "  data dataset=" << vData[i]->getFilename() << std::endl;
    for (size_t i = 0; i < vMCEWK.size(); ++i)
      std::cout << "  MC EWK dataset=" << vMCEWK[i]->getFilename() << " norm.fact.=" << fNormalisationInfo->getNormalisationFactor(vMCEWK[i]->getFile()) << std::endl;
  }

  // Loop over bins to get NQCD
  double myResultNQCD = 0.0;
  double myStatUncertaintySqNQCD = 0.0;
  double mySystUncertaintySqNQCD = 0.0;
  double myTotalDataBB = 0.0;
  double myTotalDataMinusEWKTauLeg = 0.0;
  double myTotalDataTauLeg = 0.0;
  double myTotalDataMETLeg = 0.0;
  for (int i = 1; i <= nBins; ++i) {
    double myBigBoxCounts = getMeasurementCounts(vData, i, sBigboxHisto, true) - getMeasurementCounts(vMCEWK, i, sBigboxHisto);
    myTotalDataBB += getMeasurementCounts(vData, i, sBigboxHisto, true);
    if (myBigBoxCounts < 0.0001) continue;
    double myMETLegCounts = getMeasurementCounts(vData, i, sAfterMETLegHisto, true) - getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto);
    myTotalDataMETLeg += getMeasurementCounts(vData, i, sAfterMETLegHisto, true);
    double myTauLegCounts = getMeasurementCounts(vData, i, sAfterTauLegHisto, true) - getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto);
    myTotalDataTauLeg += getMeasurementCounts(vData, i, sAfterTauLegHisto, true);
    myTotalDataMinusEWKTauLeg += myTauLegCounts;
    //std::cout << "bin=" << i << " bb=" << myBigBoxCounts << " metleg=" << myMETLegCounts << " tauleg=" << myTauLegCounts << " nQCD=" << myTauLegCounts * myMETLegCounts / myBigBoxCounts << std::endl;
    //std::cout << "bin=" << i << " met leg DATA = " << getMeasurementCounts(vData, i, sAfterMETLegHisto, true) << "+-" << getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true) << " tau leg DATA = " << getMeasurementCounts(vData, i, sAfterTauLegHisto, true) << "+-" << getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) << std::endl;
    if (bDebug) {
      std::cout << "  tau pt bin=" << i << ", Big box: Ndata=" << getMeasurementCounts(vData, i, sBigboxHisto, true) << " EWK MC=" << getMeasurementCounts(vMCEWK, i, sBigboxHisto)
                << " MET leg Ndata=" << getMeasurementCounts(vData, i, sAfterMETLegHisto, true) << " EWK MC=" << getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto)
                << " tau leg Ndata=" << getMeasurementCounts(vData, i, sAfterTauLegHisto, true) << " EWK MC=" << getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto) << std::endl;
      std::cout << TMath::Sqrt(getMeasurementAbsUncertaintySquared(vMCEWK, i, sBigboxHisto)) << std::endl;
    }
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
    double myTauLegStatAndSystUncertainty = TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) +
                                                 getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto) +
                                                 TMath::Power(getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.20,2)) / myBigBoxCounts;
    myDataStatUncertaintySq = getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) * TMath::Power(myNQCDForThisBin / myTauLegCounts, 2);
    myEWKStatUncertaintySq = getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto) * TMath::Power(myNQCDForThisBin / myTauLegCounts, 2);
    //std::cout << "bin=" << i << " abs. stat. uncert = (" << myDataStatUncertaintySq << ", " << myEWKStatUncertaintySq  << "), tot=" << (myDataStatUncertaintySq + myEWKStatUncertaintySq) << std::endl;
    //std::cout << "bin=" << i << " abs. stat. uncert = (" << TMath::Sqrt(myDataStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << ", " << TMath::Sqrt(myEWKStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << "), tot=" << TMath::Sqrt(myDataStatUncertaintySq + myEWKStatUncertaintySq) * myTauLegCounts / myNQCDForThisBin << std::endl;
    //std::cout << "bin=" << i << " rel. stat. uncert = (" << TMath::Sqrt(myDataStatUncertaintySq)/myResultNQCD << "), " << TMath::Sqrt(myEWKStatUncertaintySq)/myResultNQCD << ", tot=" << TMath::Sqrt(myDataStatUncertaintySq + myEWKStatUncertaintySq)/myResultNQCD << std::endl;
    myStatUncertaintySqNQCD += (myDataStatUncertaintySq + myEWKStatUncertaintySq);
    mySystUncertaintySqNQCD += TMath::Power(getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.20 * myNQCDForThisBin / myTauLegCounts, 2);
    hCtrlSystematics->SetBinContent(i-1, 1, TMath::Sqrt(myDataStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 2, TMath::Sqrt(myEWKStatUncertaintySq));
    hCtrlSystematics->SetBinContent(i-1, 3, getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.20 * myNQCDForThisBin / myTauLegCounts); // assume 20 % syst.
    // Fill efficiency histograms
    hMETLegEfficiency->SetBinContent(i, myMETLegCounts / myBigBoxCounts);
    hMETLegEfficiency->SetBinError(i, TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true) +
                                                  getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterMETLegHisto)) / myBigBoxCounts);
    hTauLegEfficiency->SetBinContent(i, myTauLegCounts / myBigBoxCounts);
    hTauLegEfficiency->SetBinError(i, TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true) +
                                                  getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto)) / myBigBoxCounts);
    if (bDebug) {
      std::cout << "  tau pt bin=" << i << ", eff(metleg) = " << hMETLegEfficiency->GetBinContent(i) << " +- " << hMETLegEfficiency->GetBinError(i)
                << ", eff(tauleg) = " << hTauLegEfficiency->GetBinContent(i) << " +- " << hTauLegEfficiency->GetBinError(i) << std::endl;
    }
    // Fill purity histograms
    // purity = D-E / D  = 1-E/D
    // delta^2 = (E/D^2*delta_D)^2 + (1/D*delta_E)^2 = 1/D^4*(E^2*delta_D^2 + D^2*delta_E^2)
    hBigboxPurity->SetBinContent(i, myBigBoxCounts / getMeasurementCounts(vData, i, sBigboxHisto, true));
    double a = getMeasurementCounts(vMCEWK, i, sBigboxHisto) / TMath::Power(getMeasurementCounts(vData, i, sBigboxHisto, true), 2);
    double b = 1.0 / getMeasurementCounts(vData, i, sBigboxHisto, true);
    hBigboxPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sBigboxHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sBigboxHisto)));
    hMETLegPurity->SetBinContent(i, myMETLegCounts / getMeasurementCounts(vData, i, sAfterMETLegHisto, true));
    a = getMeasurementCounts(vMCEWK, i, sAfterMETLegHisto) / TMath::Power(getMeasurementCounts(vData, i, sAfterMETLegHisto, true), 2);
    b = 1.0 / getMeasurementCounts(vData, i, sAfterMETLegHisto, true);
    hMETLegPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sAfterMETLegHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterMETLegHisto)));
    hTauLegPurity->SetBinContent(i, myTauLegCounts / getMeasurementCounts(vData, i, sAfterTauLegHisto, true));
    a = getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto) / TMath::Power(getMeasurementCounts(vData, i, sAfterTauLegHisto, true), 2);
    b = 1.0 / getMeasurementCounts(vData, i, sAfterTauLegHisto, true);
    hTauLegPurity->SetBinError(i, TMath::Sqrt(a*a*getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true)
                                            + b*b*getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto)));
    if (bDebug) {
      std::cout << "  tau pt bin=" << i << ", purity(bigbox) = " << hBigboxPurity->GetBinContent(i) << " +- " << hBigboxPurity->GetBinError(i)
                << ", purity(metleg) = " << hMETLegPurity->GetBinContent(i) << " +- " << hMETLegPurity->GetBinError(i)
                << ", purity(tauleg) = " << hTauLegPurity->GetBinContent(i) << " +- " << hTauLegPurity->GetBinError(i) << std::endl;
    }
    // Transverse mass with traditional value
    if (!sBasicMtHisto.size()) continue;
    // Obtain histogram with mT shape for data - EWK in given tau pT bin
    std::stringstream s;
    s << sBasicMtHisto << "_bin" << i-1;
    if (!getMergedMtHistogramForAPtBin(i-1, s.str(), hBinnedMtShape[i-1], hBasicMtShapeDataStat, hBasicMtShapeEWKStat, hBasicMtShapeEWKSyst)) {
      std::cout << "Failed to obtain mT histogram for tau pT bin " << i-1 << std::endl;
      return;
    }
    // Normalise with eff(tauleg)
    for (int j = 0; j <= hBinnedMtShape[i-1]->GetNbinsX()+1; ++j) {
      // uncert: f=a*b -> df = b*da + a*da
      if (myBigBoxCounts > 0) {
        if (bDebug && j == 1) { 
          std::cout << "  d(eff(tauleg)*dN)=" << myTauLegCounts / myBigBoxCounts * hBinnedMtShape[i-1]->GetBinError(j) << " d(N*deff(tauleg))=" << hBinnedMtShape[i-1]->GetBinContent(j) * myTauLegStatAndSystUncertainty << std::endl;
          std::cout << "  tauleg data stat = " << TMath::Sqrt(getMeasurementAbsUncertaintySquared(vData, i, sAfterTauLegHisto, true)) / myBigBoxCounts
                    << " ewk stat = " << TMath::Sqrt(getMeasurementAbsUncertaintySquared(vMCEWK, i, sAfterTauLegHisto)) / myBigBoxCounts
                    << " ewk syst = " << getMeasurementCounts(vMCEWK, i, sAfterTauLegHisto)*0.20 / myBigBoxCounts << std::endl;
        }
        hBinnedMtShape[i-1]->SetBinError(j, TMath::Sqrt(TMath::Power(myTauLegCounts / myBigBoxCounts * hBinnedMtShape[i-1]->GetBinError(j),2) +
                                                        TMath::Power(hBinnedMtShape[i-1]->GetBinContent(j) * myTauLegStatAndSystUncertainty, 2)));
        hBinnedMtShape[i-1]->SetBinContent(j, hBinnedMtShape[i-1]->GetBinContent(j) * myTauLegCounts / myBigBoxCounts);
      }
    }
    if (bDebug) {
      std::cout << "  tau pt bin=" << i << ", basicMt[1] = " << hBinnedMtShape[i-1]->GetBinContent(1) << " +- " << hBinnedMtShape[i-1]->GetBinError(1) << std::endl;
    }
    hBasicMtShape->Add(hBinnedMtShape[i-1]);
    // weight in pt bin corresponding eff(tau leg)
    // multiply by 1/(1-eff(tight isolation))
  }

std::cout << "Data events after bigbox: " << myTotalDataBB << std::endl;
std::cout << "Data events after tauleg: " << myTotalDataTauLeg << std::endl;
std::cout << "Data events after metleg: " << myTotalDataMETLeg << std::endl;
std::cout << "Data-EWK events after tauleg: " << myTotalDataMinusEWKTauLeg << std::endl;

// Store result
  fResultValue = myResultNQCD;
  fResultRelativeStatisticalUncertainty = TMath::Sqrt(myStatUncertaintySqNQCD) / myResultNQCD;
  fResultRelativeSystematicalUncertainty = TMath::Sqrt(mySystUncertaintySqNQCD) / myResultNQCD;
  // Uncertainties have been stored as squares, take now square root
  for (int i = 1; i <= nBins; ++i) {
    for (int j = 0; j <= hBasicMtShapeDataStat->GetNbinsX()+1; ++j) {
      hBasicMtShapeDataStat->SetBinContent(j, i, TMath::Sqrt(hBasicMtShapeDataStat->GetBinContent(j, i)));
      hBasicMtShapeEWKStat->SetBinContent(j, i, TMath::Sqrt(hBasicMtShapeEWKStat->GetBinContent(j, i)));
      hBasicMtShapeEWKSyst->SetBinContent(j, i, TMath::Sqrt(hBasicMtShapeEWKSyst->GetBinContent(j, i)));
    }
  }

  // Normalise mT shape
  hBasicMtShape->Scale(myResultNQCD / (hBasicMtShape->GetBinContent(0) + hBasicMtShape->GetBinContent(hBasicMtShape->GetNbinsX()+1) + hBasicMtShape->Integral()));
  hMtShapeForResult = dynamic_cast<TH1F*>(hBasicMtShape->Clone("QCDMt"));
  std::cout << "  QCD measurement result: NQCD = " << fResultValue
            << " +- " << fResultRelativeStatisticalUncertainty*100.0 << " % stat."
            << " +- " << fResultRelativeSystematicalUncertainty*100.0 << " % syst." << std::endl;
  if (fNormalisationInfo->getLuminosityScaling() > 1)
    std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m QCD measurement rate and data stat. uncertainty scaled for lumi forecast" << std::endl;

  if (isRate()) { // do only once, save control histograms
    hCtrlSystematics->SetDirectory(myFile);
    hMETLegEfficiency->SetDirectory(myFile);
    hTauLegEfficiency->SetDirectory(myFile);
    hBigboxPurity->SetDirectory(myFile);
    hMETLegPurity->SetDirectory(myFile);
    hTauLegPurity->SetDirectory(myFile);
    // Control histograms for mT
    for (size_t i = 0; i < hBinnedMtShape.size(); ++i) {
      hBinnedMtShape[i]->SetDirectory(myFile);
    }
    hBasicMtShape->SetDirectory(myFile);
    hBasicMtShapeDataStat->SetDirectory(myFile);
    hBasicMtShapeEWKStat->SetDirectory(myFile);
    hBasicMtShapeEWKSyst->SetDirectory(myFile);
    myFile->Write();
    //myFile->Close();
  }
  std::cout << "Control histograms written to " << myQCDCtrlName << std::endl;
  std::cout << "... QCD Measurement done ..." << std::endl;
}

bool QCDMeasurementCalculator::getMergedMtHistogramForAPtBin(int bin, std::string histoName, TH1* h, TH2* dataStat, TH2* ewkStat, TH2* ewkSyst) {
  std::vector<double> fDataStatUncertaintySquared;
  std::vector<double> fEWKStatUncertaintySquared;
  std::vector<double> fEWKSystUncertaintySquared;
  
  for (int i = 0; i <= h->GetNbinsX()+1; ++i) {
    h->SetBinContent(i, 0.);
    h->SetBinError(i, 0);
    fDataStatUncertaintySquared.push_back(0.);
    fEWKStatUncertaintySquared.push_back(0.);
    fEWKSystUncertaintySquared.push_back(0.);
  }
  //h->Sumw2();
  // Loop over data
  for (size_t i = 0; i < vData.size(); ++i) {
    TH1* myHisto = getHistogram(vData[i]->getFile(), histoName);
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram '" << histoName << "' in file '" << vData[i]->getFilename() << "'!" << std::endl;
      return false;
    }
    // Luminosity scaling (yes, it's for data, but that's the way to get the correct result and uncertainty for QCD
    double myNormFactor = fNormalisationInfo->getLuminosityScaling();
    // Sum histo
    h->Add(myHisto, myNormFactor);
    // Add stat uncertainty
    for (int j = 0; j <= h->GetNbinsX()+1; ++j) {
      fDataStatUncertaintySquared[j] += TMath::Power(myHisto->GetBinError(j),2) * 1.0/fNormalisationInfo->getLuminosityScaling();
    }
  }
  if (bDebug && bin == 1) std::cout << "  mt[1]: data = " << h->GetBinContent(2) << std::endl;
  // Loop over MC and substract it from data
  for (size_t i = 0; i < vMCEWK.size(); ++i) {
    TH1* myHisto = getHistogram(vMCEWK[i]->getFile(), histoName);
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram '" << histoName << "' in file '" << vMCEWK[i]->getFilename() << "'!" << std::endl;
      return false;
    }
    // Normalise MC
    double myNormFactor = fNormalisationInfo->getNormalisationFactor(vMCEWK[i]->getFile());
    // Add properly (i.e. substract value and sum in square uncertainty)
    for (int j = 0; j <= myHisto->GetNbinsX()+1; ++j) { // loop also over underflow and overflow bins
      if (h->GetBinContent(j) >= myHisto->GetBinContent(j)*myNormFactor) {
        h->SetBinContent(j, h->GetBinContent(j) - myHisto->GetBinContent(j)*myNormFactor);
      } else {
        h->SetBinContent(j, 0.0);
      }
      // take also syst. error into account for MC EWK
      fEWKStatUncertaintySquared[j] += TMath::Power(myHisto->GetBinError(j)*myNormFactor,2);
      fEWKSystUncertaintySquared[j] += TMath::Power(myHisto->GetBinContent(j)*myNormFactor*0.20,2);
      if (bDebug && bin == 1 && j == 1) std::cout << " mt[1]: EWK(" << vMCEWK[i]->getFilename() << ") counts = " << myHisto->GetBinContent(j)*myNormFactor << " +- " << myHisto->GetBinError(j)*myNormFactor << " (stat.) +- " << myHisto->GetBinContent(j)*myNormFactor*0.2 << " (syst.)" << std::endl;
    }
  }
  for (int i = 0; i <= h->GetNbinsX()+1; ++i) {
    h->SetBinError(i,TMath::Sqrt(fDataStatUncertaintySquared[i] + fEWKStatUncertaintySquared[i] + fEWKSystUncertaintySquared[i]));
    dataStat->SetBinContent(i, bin, dataStat->GetBinContent(i,bin) + fDataStatUncertaintySquared[i]);
    ewkStat->SetBinContent(i, bin, ewkStat->GetBinContent(i,bin) + fEWKStatUncertaintySquared[i]);
    ewkSyst->SetBinContent(i, bin, ewkSyst->GetBinContent(i,bin) + fEWKSystUncertaintySquared[i]);
    if (bDebug && bin == 1 && i == 1) std::cout << " mt[1]: data-EWK = " << h->GetBinContent(i) << " data stat = " << TMath::Sqrt(dataStat->GetBinContent(i,bin)) << " ewk stat = " << TMath::Sqrt(ewkStat->GetBinContent(i,bin)) << " ewk syst = " << TMath::Sqrt(ewkSyst->GetBinContent(i,bin)) << std::endl;
  }
  return true;
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
      myValue += myHisto->GetBinContent(bin) * fNormalisationInfo->getLuminosityScaling();
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
    if (isData) {
      //sqrt(a^2 + b^2)* sqrt(2) = sqrt(a^2*2 + b^2*2) = sqrt((a*sqrt(2))^2 + (b*sqrt(2))^2)
      a *= TMath::Sqrt(fNormalisationInfo->getLuminosityScaling());
    } else {
      a *= fNormalisationInfo->getNormalisationFactor(datasets[i]->getFile());
    }
    myValue += a * a;
    //if (datasets[i]->getFilename() == "QCDpath/TTJets_TuneZ2_Summer11/res/histograms-TTJets_TuneZ2_Summer11.root")
    //  std::cout << datasets[i]->getFilename() << " error = " << a << ", unnormalised = " << myHisto->GetBinError(bin) << ", unnormalised counts= " << myHisto->GetBinContent(bin) << "weights=" << TMath::Sqrt(myHisto->GetSumw2()->At(bin)) <<  std::endl;
  }
  return myValue;
}

TH1* QCDMeasurementCalculator::getHistogram(TFile* f, std::string name) {
  TH1F* h = dynamic_cast<TH1F*>(f->Get(name.c_str()));
  if (!h)
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot find histogram: " << name << std::endl;
  return h;
}

double QCDMeasurementCalculator::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation) {
  if (!bIsCalculated) doCalculate();
  if (isRate())
    return fResultValue;
  if (bStatisticsMode)
    return fResultRelativeStatisticalUncertainty;
  else if (bSystematicsMode)
    return fResultRelativeSystematicalUncertainty;
  return 0.;
}

void QCDMeasurementCalculator::addHistogramsToFile(std::string label, std::string id, TFile* f) {
  //if (!bIsCalculated) doCalculate();
  std::stringstream s;
  s << label;
  TH1F* h = new TH1F(s.str().c_str(), s.str().c_str(), 20, 0, 400);
  h->Sumw2();
  h->Add(hMtShapeForResult);
  h->SetDirectory(f);
  std::cout << "  Created histogram " << s.str() << " with normalisation " << h->Integral() <<  std::endl;
}