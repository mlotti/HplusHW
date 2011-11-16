#ifndef EXTRACTABLESCALEFACTOR_H
#define EXTRACTABLESCALEFACTOR_H

#include <Extractable.h>

class ExtractableScaleFactor : public Extractable {

 public:
  ExtractableScaleFactor(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string scaleFactorUncertaintyHisto, std::string normHisto);
  ~ExtractableScaleFactor();
  
  double doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info);
  void print();

 private:
  std::string sCounterHisto;
  std::string sScaleFactorUncertaintyHistogram;
  std::string sNormHisto;
};

#endif // EXTRACTABLESCALEFACTOR_H
