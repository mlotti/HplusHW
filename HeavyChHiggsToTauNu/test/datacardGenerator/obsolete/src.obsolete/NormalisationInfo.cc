#include "NormalisationInfo.h"
#include <iostream>

#include "TH1F.h"

NormalisationInfo::NormalisationInfo(std::string configInfoHisto, std::string counterHisto, double luminosity, double luminosityScaling)
: sConfigInfoHisto(configInfoHisto),
  sCounterHisto(counterHisto),
  fLuminosity(luminosity),
  fLuminosityScaling(luminosityScaling) {

}

NormalisationInfo::~NormalisationInfo() {

}

double NormalisationInfo::getNormalisationFactor(TFile* f) {
  // Get histograms
  TH1F* myConfigInfoHisto = dynamic_cast<TH1F*>(f->Get(sConfigInfoHisto.c_str()));
  if (!myConfigInfoHisto) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m cannot find config info histogram at '" 
              << sConfigInfoHisto << "'!" << std::endl;
    return -1.;
  }
  TH1F* myCounterHisto = dynamic_cast<TH1F*>(f->Get(sCounterHisto.c_str()));
  if (!myCounterHisto) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m cannot find counter histogram at '" 
              << sCounterHisto << "'!" << std::endl;
    return -1.;
  }
  // Check if the file is data
  int myDataBin = 0;
  for (int i = 1; i <= myConfigInfoHisto->GetNbinsX()+1; ++i) {
    std::string myBinLabel = myConfigInfoHisto->GetXaxis()->GetBinLabel(i);
    if (myBinLabel == "isData")
      myDataBin = i;
  }
  if (!myDataBin) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m cannot find bin 'isData' in config info histogram "
              << sConfigInfoHisto << "!" << std::endl;
    return -1;
  }
  // Return for data just the luminosity scaling factor (1 if no scaling is used)
  if (myConfigInfoHisto->GetBinContent(myDataBin) > 0.)
    return fLuminosityScaling;
  
  // Calculate normalisation factor for simulated samples
  double myXsection = myConfigInfoHisto->GetBinContent(2) / myConfigInfoHisto->GetBinContent(1);
  //std::cout << myXsection << std::endl;
  double myAllEvents = myCounterHisto->GetBinContent(1);
  
  if (myAllEvents > 0)
    return myXsection * fLuminosity * fLuminosityScaling * 1000.0 / myAllEvents;
  return 0;
}
