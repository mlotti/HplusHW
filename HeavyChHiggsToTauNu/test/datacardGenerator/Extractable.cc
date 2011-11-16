#include "Extractable.h"
#include <iostream>
#include <sstream>

Extractable::Extractable(int channel)
: fType(kExtractableObservation),
  bIsMerged(false),
  sMergedMasterId("") {
  std::stringstream s;
  s << "__DataChannel" << channel;
  sId = s.str();
}

Extractable::Extractable(std::string id)
: sId(id),
  fType(kExtractableRate),
  bIsMerged(false),
  sMergedMasterId("") {
  
}

Extractable::Extractable(std::string id, std::string distribution, std::string description)
: sDistribution(distribution),
  sId(id),
  sDescription(description),
  fType(kExtractableNuisance),
  bIsMerged(false),
  sMergedMasterId("") {
  
}

Extractable::Extractable(std::string id, std::string distribution, std::string description, bool isAsymmetric)
: sDistribution(distribution),
  sId(id),
  sDescription(description),
  fType(kExtractableNuisanceAsymmetric),
  bIsMerged(false),
  sMergedMasterId("") {
  
}


Extractable::~Extractable() {

}

double Extractable::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info) {
  return 0.;
}

double Extractable::doExtractAsymmetricUpperValue(std::vector< Dataset* > datasets, NormalisationInfo* info) {
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

Extractable* Extractable::mergedContainId(std::string id) {
  for (size_t i = 0; i < vExtractablesToBeMerged.size(); ++i) {
    if (vExtractablesToBeMerged[i]->getId() == id)
      return vExtractablesToBeMerged[i];
  }
  return 0;
}

double Extractable::getMergedValue(std::vector< Dataset* > datasets, NormalisationInfo* info, double hostValue) {
  std::cout << "id=" << sId << " hostvalue=" << hostValue << " merged: " << vExtractablesToBeMerged.size() << std::endl;
  if (hostValue > 0)
    return hostValue;
  // Return first non-zero value
  for (size_t i = 0; i < vExtractablesToBeMerged.size(); ++i) {
    double myValue = vExtractablesToBeMerged[i]->doExtract(datasets, info);
    std::cout << "id=" << vExtractablesToBeMerged[i]->getId() << " value=" << myValue << std::endl;
    if (myValue > 0) return myValue;
  }
  // Nothing has been found, return zero
  return hostValue;
}
