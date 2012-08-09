#ifndef EXTRACTABLESCALEFACTOR_H
#define EXTRACTABLESCALEFACTOR_H

#include <Extractable.h>

class ExtractableScaleFactor : public Extractable {

 public:
  ExtractableScaleFactor(std::string id, std::string distribution, std::string description, std::vector<std::string> scaleFactorUncertaintyHisto, std::vector<std::string> scaleFactorNormHisto);
  ~ExtractableScaleFactor();
  
  double doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  void print();

 private:
  std::vector<std::string> sScaleFactorUncertaintyHistogram;
  std::vector<std::string> sScaleFactorNormHisto;
};

#endif // EXTRACTABLESCALEFACTOR_H
