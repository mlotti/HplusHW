#include "ExtractableCounter.h"
#include <iostream>

#include "TMath.h"



ExtractableCounter::ExtractableCounter(int channel, std::string counterHisto, std::string counterItem)
: Extractable(channel),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem) {
  
}

ExtractableCounter::ExtractableCounter(std::string id, std::string counterHisto, std::string counterItem)
: Extractable(id),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem) {
  
}

ExtractableCounter::ExtractableCounter(std::string id, std::string distribution, std::string description,
                                       std::string counterHisto, std::string counterItem)
: Extractable(id, distribution, description),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem) {
  
}

ExtractableCounter::~ExtractableCounter() {
  
}

double ExtractableCounter::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation) {
  // Loop over histograms to obtain result
  double fCounterValue = 0.; // result in number of events
  double fCounterUncertainty = 0.; // result in number of events
  for (std::vector<Dataset*>::iterator it = datasets.begin(); it != datasets.end(); ++it) {
    if ((*it)->isRootFile()) {
      // Open histogram and check validity
      TH1F* h = getCounterHistogram((*it)->getFile(), sCounterHisto);
      if (!h) return -1.;
      // Obtain bin index of counter
      int myBinIndex = getCounterItemIndex(h, sCounterItem);
      if (!myBinIndex) return -1.;
      // Obtain result
      double myNormFactor = info->getNormalisationFactor((*it)->getFile());
      if (isObservation()) myNormFactor = info->getLuminosityScaling();
      fCounterValue += h->GetBinContent(myBinIndex) * myNormFactor;
      fCounterUncertainty += h->GetBinError(myBinIndex) * h->GetBinError(myBinIndex)
        * myNormFactor * myNormFactor;
    }
    // FIXME add here obtaining of result from txt file
  }
  // Return result
  fCounterUncertainty = TMath::Sqrt(fCounterUncertainty);
  
  if (isObservation() || isRate())
    return fCounterValue * additionalNormalisation;
  else if (isNuisance())
    return fCounterUncertainty / fCounterValue; // Relative uncertainty
  return -1.;
}

void ExtractableCounter::print() {
  std::cout << "Row / Counter: ";
  Extractable::print();
  std::cout << " counter=" << sCounterItem << std::endl;
}
