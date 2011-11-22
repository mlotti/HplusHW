#ifndef NORMALISATIONINFO_H
#define NORMALISATIONINFO_H

#include <string>
#include "TFile.h"

class NormalisationInfo {

public:
  NormalisationInfo(std::string configInfoHisto, std::string counterHisto, double luminosity);
  virtual ~NormalisationInfo();
  
  double getNormalisationFactor(TFile* f);
  std::string getConfigInfoHisto() { return sConfigInfoHisto; }
  std::string getCounterHisto() { return sCounterHisto; }
  double getLuminosity() const { return fLuminosity; }
  
private:
  std::string sConfigInfoHisto;
  std::string sCounterHisto;
  double fLuminosity; // luminosity in fb-1
};

#endif // NORMALISATIONINFO_H
