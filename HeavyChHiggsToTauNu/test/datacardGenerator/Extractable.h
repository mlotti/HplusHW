#ifndef EXTRACTABLE_H
#define EXTRACTABLE_H

#include "Dataset.h"
#include "NormalisationInfo.h"

#include <TFile.h>
#include <TH1F.h>
#include <string>

class Extractable {
public:
  enum ExtractableType {
    kExtractableObservation,
    kExtractableRate,
    kExtractableNuisance
  };
  
  /// Constructor for observation
  Extractable(int channel);
  /// Constructor for rate
  Extractable(std::string id);
  /// Constructor for nuisance
  Extractable(std::string id, std::string distribution, std::string description);

  virtual ~Extractable();
  /// Mines result from datasets and merges dataset results together
  virtual double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info);
  /// For debugging
  virtual void print();

  bool isObservation() const { return fType == kExtractableObservation; }
  bool isRate() const { return fType == kExtractableRate; }
  bool isNuisance() const { return fType == kExtractableNuisance; }
  bool isShapeNuisance() const { return (isNuisance() && sDistribution == "shapeQ"); }

  std::string& getDistribution() { return sDistribution; }
  std::string& getId() { return sId; }
  std::string& getDescription() { return sDescription; }

protected:
  TH1F* getCounterHistogram(TFile* f, std::string counterHisto);
  int getCounterItemIndex(TH1F* h, std::string counterItem);

protected:
  std::string sDistribution;
  std::string sId;
  std::string sDescription;

private:
  ExtractableType fType;
  
};

#endif
