#include "ExtractableScaleFactor.h"
#include "TMath.h"

#include <iostream>

ExtractableScaleFactor::ExtractableScaleFactor(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string scaleFactorUncertaintyHisto, std::string normHisto)
: Extractable(id, distribution, description),
  sCounterHisto(counterHisto),
  sScaleFactorUncertaintyHistogram(scaleFactorUncertaintyHisto),
  sNormHisto(normHisto) {

}

ExtractableScaleFactor::~ExtractableScaleFactor() {

}

double ExtractableScaleFactor::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info) {
    // Only defined for nuisance
  if (isObservation() || isRate())
    return -1.0;
  
  // Loop over histograms to obtain result
  double myTotal = 0.; // result in number of events
  double mySum = 0; // result in number of events
  for (std::vector<Dataset*>::iterator it = datasets.begin(); it != datasets.end(); ++it) {
    if ((*it)->isRootFile()) {
      // Open histogram and check validity
      TH1F* h = getCounterHistogram((*it)->getFile(), sCounterHisto);
      if (!h) return -1.;
      TH1F* hUncertainty = getCounterHistogram((*it)->getFile(), sScaleFactorUncertaintyHistogram);
      if (!hUncertainty) return -1.;
      TH1F* hNorm = getCounterHistogram((*it)->getFile(), sNormHisto);
      if (!hNorm) return -1.;
      // Obtain result
      // FIXME
      std::cout << "ScaleFactor: \033[0;44m\033[1;37mwarning check code!\033[0;0m" << std::endl;
      double myNormFactor = info->getNormalisationFactor((*it)->getFile());
      for (int i = 1; i <= hUncertainty->GetNbinsX(); ++i) {
        if (sId == "1" && hUncertainty->GetBinContent(i) / (double)hUncertainty->GetEntries() > 0.1) { // trg scale factor
          double myCount = hUncertainty->GetBinContent(i) * myNormFactor;
          mySum += myCount * myCount * hUncertainty->GetBinCenter(i) * hUncertainty->GetBinCenter(i);
        } else if (sId != "1") {
          double myCount = hUncertainty->GetBinContent(i) * myNormFactor;
          mySum += myCount * myCount * hUncertainty->GetBinCenter(i) * hUncertainty->GetBinCenter(i);
        }
      }
      myTotal += hNorm->GetBinContent(1) * myNormFactor / 2.0;
    // this is the correct code
      /*double myNormFactor = info->getNormalisationFactor((*it)->getFile());
      for (int i = 1; i <= hUncertainty->GetNbinsX(); ++i) {
        double myCount = hUncertainty->GetBinContent(i) * myNormFactor;
        mySum += myCount * myCount * hUncertainty->GetBinCenter(i) * hUncertainty->GetBinCenter(i);
      }
      myTotal += hNorm->GetBinContent(1) * myNormFactor;*/
    }
  }
  // Return result
  return TMath::Sqrt(mySum) / myTotal;
}

void ExtractableScaleFactor::print() {
  std::cout << "Row / ScaleFactor: ";
  Extractable::print();
  std::cout << " CounterHisto=" << sCounterHisto
            << " ScaleFactorUncertaintyHisto=" << sScaleFactorUncertaintyHistogram << std::endl;
}


