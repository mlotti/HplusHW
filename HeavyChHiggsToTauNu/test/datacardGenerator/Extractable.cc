#include "Extractable.h"
#include <iostream>
#include <sstream>

Extractable::Extractable(int channel)
: fType(kExtractableObservation) {
  std::stringstream s;
  s << "__DataChannel" << channel;
  sId = s.str();
}

Extractable::Extractable(std::string id)
: sId(id),
  fType(kExtractableRate) {
  
}

Extractable::Extractable(std::string id, std::string distribution, std::string description)
: sDistribution(distribution),
  sId(id),
  sDescription(description),
  fType(kExtractableNuisance) {
  
}

Extractable::~Extractable() {

}

double Extractable::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info) {
  return 0.;
}

void Extractable::print() {
  if (isObservation())
    std::cout << "observation:";
  else if (isRate())
    std::cout << "rate: id=" << sId;
  else if (isNuisance())
    std::cout << "nuisance: id=" << sId 
              << " distribution=" << sDistribution
              << " description=" << sDescription; 
}

TH1F* Extractable::getCounterHistogram(TFile* f, std::string counterHisto) {
  // Open histogram and check validity
  TH1F* h = dynamic_cast<TH1F*>(f->Get(counterHisto.c_str()));
  if (!h) {
    std::cout << "Error: Cannot find counter histogram '" << counterHisto << "'!" << std::endl;
    return 0;
  }
  return h;
}

int Extractable::getCounterItemIndex(TH1F* h, std::string counterItem) {
  for (int i = 1; i <= h->GetNbinsX(); ++i) {
    std::string myBinLabel = h->GetXaxis()->GetBinLabel(i);
    if (myBinLabel == counterItem)
      return i;
  }
  std::cout << "Error: Cannot find counter by name " << counterItem << "!" << std::endl;
  return -1;
}
