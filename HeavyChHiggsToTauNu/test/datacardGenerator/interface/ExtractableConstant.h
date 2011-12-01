#ifndef EXTRACTABLECONSTANT_H
#define EXTRACTABLECONSTANT_H

#include "Extractable.h"

class ExtractableConstant : public Extractable {
 public:
  /// Constructor for observation
  ExtractableConstant(int channel, float value);
  /// Constructor for rate
  ExtractableConstant(std::string id, float value);
  /// Constructor for nuisance
  ExtractableConstant(std::string id, std::string distribution, std::string description, float value);
  /// Constructor for nuisance with asymmetric errors
  ExtractableConstant(std::string id, std::string distribution, std::string description, float value, float upperValue);
virtual ~ExtractableConstant();
  
  virtual double doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  virtual double doExtractAsymmetricUpperValue(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  virtual void print();

 private:
  double fValue;
  double fUpperValue; // For asymmetric nuisances
  
};

#endif // EXTRACTABLECONSTANT_H
