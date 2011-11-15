#include "ExtractableScaleFactor.h"
#include "TMath.h"

#include <iostream>

ExtractableScaleFactor::ExtractableScaleFactor(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string scaleFactorUncertaintyHisto)
: Extractable(id, distribution, description),
  sCounterHisto(counterHisto),
  sScaleFactorUncertaintyHistogram(scaleFactorUncertaintyHisto) {

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
      // Obtain result
      double myNormFactor = info->getNormalisationFactor((*it)->getFile(), sCounterHisto);
      for (int i = 1; i <= hUncertainty->GetNbinsX(); ++i) {
        double myCount = hUncertainty->GetBinContent(i) * myNormFactor;
        myTotal += myCount;
        mySum += myCount * myCount * hUncertainty->GetBinCenter(i) * hUncertainty->GetBinCenter(i);
      }
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


