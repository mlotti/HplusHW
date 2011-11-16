#include "ExtractableRatio.h"
#include <iostream>


ExtractableRatio::ExtractableRatio(std::string id, std::string distribution, std::string description,
                                   std::string counterHisto, std::string nominatorCounter, std::string denominatorCounter, double scale)
: Extractable(id, distribution, description),
  sCounterHisto(counterHisto),
  sNominatorItem(nominatorCounter),
  sDenominatorItem(denominatorCounter),
  fScale(scale) {

}

ExtractableRatio::~ExtractableRatio() {

}

double ExtractableRatio::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info) {
  // Only defined for nuisance
  if (isObservation() || isRate())
    return -1.0;
  
  // Loop over histograms to obtain result
  double myNominatorValue = 0.; // result in number of events
  double myDenominatorValue = 0.; // result in number of events
  for (std::vector<Dataset*>::iterator it = datasets.begin(); it != datasets.end(); ++it) {
    if ((*it)->isRootFile()) {
      // Open histogram and check validity
      TH1F* h = getCounterHistogram((*it)->getFile(), sCounterHisto);
      if (!h) return -1.;
      // Obtain bin indices of counter
      int myNominatorIndex = getCounterItemIndex(h, sNominatorItem);
      if (!myNominatorIndex) return -1.;
      int myDenominatorIndex = getCounterItemIndex(h, sDenominatorItem);
      if (!myDenominatorIndex) return -1.;
      // Obtain result
      double myNormFactor = info->getNormalisationFactor((*it)->getFile());
      myNominatorValue += h->GetBinContent(myNominatorIndex) * myNormFactor;
      myDenominatorValue += h->GetBinContent(myDenominatorIndex) * myNormFactor;
    }
    // FIXME add here obtaining of result from txt file
  }
  // Return result
  return (myDenominatorValue - myNominatorValue) / myNominatorValue * fScale;
}
//(h->GetBinContent(myMETBin) - h->GetBinContent(myEVetoBin)) / h->GetBinContent(myEVetoBin) * 0.02;

void ExtractableRatio::print() {
  std::cout << "Row / Ratio: ";
  Extractable::print();
  std::cout << " CounterHisto=" << sCounterHisto
            << " NominatorCounter=" << sNominatorItem
            << " DenominatorCounter=" << sDenominatorItem
            << " Scale=" << fScale << std::endl;
}


