#include "ExtractableMaxCounter.h"
#include <iostream>

#include "TMath.h"




ExtractableMaxCounter::ExtractableMaxCounter(std::string id, std::string distribution, std::string description,
                                       std::vector< std::string > counterHisto, std::string counterItem)
: Extractable(id, distribution, description) {
  for (size_t i = 0; i < counterHisto.size(); ++i) {
    vCounters.push_back(new ExtractableCounter(id, counterHisto[i], counterItem));
  }
}

ExtractableMaxCounter::~ExtractableMaxCounter() {
  for (size_t i = 0; i < vCounters.size(); ++i) {
    delete vCounters[i];
  }
}

double ExtractableMaxCounter::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation) {
  // First item should contain the nominal results
  double myNominalResult = vCounters[0]->doExtract(datasets, info);
  std::cout << "nominal result: " << myNominalResult << std::endl;
  double myMaxRatio = 0.0;
  for (size_t i = 1; i < vCounters.size(); ++i) {
    double myVariation = vCounters[i]->doExtract(datasets, info);
    //std::cout << "ratio: " << myVariation / myNominalResult << std::endl;
    double myVariationRatio = TMath::Abs(myVariation / myNominalResult - 1.0);
    if (myVariationRatio > myMaxRatio)
      myMaxRatio = myVariationRatio;
    std::cout << "variation: " << myVariation << ", ratio=" << myVariationRatio << std::endl;
  }
  return myMaxRatio; // Relative uncertainty
}

void ExtractableMaxCounter::print() {
  std::cout << "Row / Counter: ";
  Extractable::print();
  vCounters[0]->print();
}
