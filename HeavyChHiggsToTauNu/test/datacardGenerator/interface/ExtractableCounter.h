#ifndef EXTRACTABLECOUNTER_H
#define EXTRACTABLECOUNTER_H

#include "Extractable.h"

class ExtractableCounter : public Extractable {
public:
  /// Constructor for observation
  ExtractableCounter(int channel, std::string counterHisto, std::string counterItem);
  /// Constructor for rate
  ExtractableCounter(std::string id, std::string counterHisto, std::string counterItem);
  /// Constructor for nuisance
  ExtractableCounter(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string counterItem);
  ~ExtractableCounter();
  
  double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info);
  void print();
  
private:
  std::string sCounterHisto;
  std::string sCounterItem;
};

#endif