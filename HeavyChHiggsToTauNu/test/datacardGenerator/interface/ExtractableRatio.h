#ifndef EXTRACTABLERATIO_H
#define EXTRACTABLERATIO_H

#include <Extractable.h>


class ExtractableRatio : public Extractable {
 public:
  ExtractableRatio(std::string id, std::string distribution, std::string description,
                   std::string counterHisto, std::string nominatorCounter, std::string denominatorCounter, double scale);
  ~ExtractableRatio();
  
  double doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info);
  void print();

 private:
  std::string sCounterHisto;
  std::string sNominatorItem;
  std::string sDenominatorItem;
  double fScale;
};

#endif // EXTRACTABLERATIO_H
