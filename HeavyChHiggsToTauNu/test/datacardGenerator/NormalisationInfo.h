#ifndef NORMALISATIONINFO_H
#define NORMALISATIONINFO_H

#include <string>
#include "TFile.h"

class NormalisationInfo {

public:
  NormalisationInfo(std::string configInfoHisto, double luminosity);
  virtual ~NormalisationInfo();
  
  double getNormalisationFactor(TFile* f, std::string counterHisto);
  
private:
  std::string sConfigInfoHisto;
  double fLuminosity; // luminosity in fb-1
};

#endif // NORMALISATIONINFO_H
