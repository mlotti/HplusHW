#ifndef EXTRACTABLEMAXCOUNTER_H
#define EXTRACTABLEMAXCOUNTER_H

#include "ExtractableCounter.h"
#include "Extractable.h"

class ExtractableMaxCounter : public Extractable {
public:
  /// Constructor for nuisance
  ExtractableMaxCounter(std::string id, std::string distribution, std::string description, std::vector< std::string > counterHistos, std::string counterItem);
  ~ExtractableMaxCounter();
  
  double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  void print();
  
private:
  std::vector<ExtractableCounter*> vCounters;
};

#endif