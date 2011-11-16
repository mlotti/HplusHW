#include "NormalisationInfo.h"
#include <iostream>

#include "TH1F.h"

NormalisationInfo::NormalisationInfo(std::string configInfoHisto, std::string counterHisto, double luminosity)
: sConfigInfoHisto(configInfoHisto),
  sCounterHisto(counterHisto),
  fLuminosity(luminosity) {

}

NormalisationInfo::~NormalisationInfo() {

}

double NormalisationInfo::getNormalisationFactor(TFile* f) {
  // Get histograms
  TH1F* myConfigInfoHisto = dynamic_cast<TH1F*>(f->Get(sConfigInfoHisto.c_str()));
  if (!myConfigInfoHisto) {
    std::cout << "Error: cannot find config info histogram at '" 
              << sConfigInfoHisto << "'!" << std::endl;
    return -1.;
  }
  TH1F* myCounterHisto = dynamic_cast<TH1F*>(f->Get(sCounterHisto.c_str()));
  if (!myCounterHisto) {
    std::cout << "Error: cannot find counter histogram at '" 
              << sCounterHisto << "'!" << std::endl;
    return -1.;
  }
  // Calculate normalisation factor
  double myXsection = myConfigInfoHisto->GetBinContent(2) / myConfigInfoHisto->GetBinContent(1);
  //std::cout << myXsection << std::endl;
  double myAllEvents = myCounterHisto->GetBinContent(1);
  
  if (myAllEvents > 0)
    return myXsection * fLuminosity * 1000.0 / myAllEvents;
  return 0;
}
