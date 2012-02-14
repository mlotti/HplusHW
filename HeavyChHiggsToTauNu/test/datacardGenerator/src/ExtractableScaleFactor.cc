#include "ExtractableScaleFactor.h"
#include "TMath.h"

#include <iostream>

ExtractableScaleFactor::ExtractableScaleFactor(std::string id, std::string distribution, std::string description, std::vector< std::string > scaleFactorUncertaintyHisto, std::vector< std::string > scaleFactorNormHisto)
: Extractable(id, distribution, description) {
  for (std::vector<std::string>::iterator it = scaleFactorUncertaintyHisto.begin(); it != scaleFactorUncertaintyHisto.end(); ++it)
    sScaleFactorUncertaintyHistogram.push_back(*it);
  for (std::vector<std::string>::iterator it = scaleFactorNormHisto.begin(); it != scaleFactorNormHisto.end(); ++it)
    sScaleFactorNormHisto.push_back(*it);
}

ExtractableScaleFactor::~ExtractableScaleFactor() {

}

double ExtractableScaleFactor::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation) {
    // Only defined for nuisance
  if (isObservation() || isRate())
    return -1.0;
  
  // Loop over histograms to obtain result
  double myTotal = 0.; // result in number of events
  double mySum = 0; // result in number of events
  for (std::vector<Dataset*>::iterator it = datasets.begin(); it != datasets.end(); ++it) {
    if ((*it)->isRootFile()) {
      // Loop over different scale factor sources provided
      for (size_t iSource = 0; iSource < sScaleFactorNormHisto.size(); ++iSource) {
        // Open histogram and check validity
        TH1F* hUncertainty = getCounterHistogram((*it)->getFile(), sScaleFactorUncertaintyHistogram[iSource]);
        if (!hUncertainty) return -1.;
        TH1F* hNorm = getCounterHistogram((*it)->getFile(), sScaleFactorNormHisto[iSource]);
        if (!hNorm) return -1.;
        // Obtain result
        double myNormFactor = info->getNormalisationFactor((*it)->getFile());
        for (int i = 1; i <= hUncertainty->GetNbinsX(); ++i) {
          double myCount = hUncertainty->GetBinContent(i) * myNormFactor;
          mySum += myCount * myCount * hUncertainty->GetBinCenter(i) * hUncertainty->GetBinCenter(i);
        }
        myTotal += hNorm->GetBinContent(1) * myNormFactor;
      }
    }
  }
  // Return result
  return TMath::Sqrt(mySum) / myTotal;
}

void ExtractableScaleFactor::print() {
  std::cout << "Row / ScaleFactor: ";
  Extractable::print();
  for (size_t iSource = 0; iSource < sScaleFactorNormHisto.size(); ++iSource) {
    std::cout << "   ScaleFactorUncertaintyHisto = " << sScaleFactorUncertaintyHistogram[iSource]
              << " ScaleFactorNormHisto = " << sScaleFactorNormHisto[iSource] << std::endl;
  }
}


