#ifndef EXTRACTABLE_H
#define EXTRACTABLE_H

#include "Dataset.h"
#include "NormalisationInfo.h"

#include <TFile.h>
#include <TH1F.h>
#include <string>
#include <vector>

class Extractable {
public:
  enum ExtractableType {
    kExtractableObservation,
    kExtractableRate,
    kExtractableNuisance,
    kExtractableNuisanceAsymmetric,
    kExtractableShapeNuisance
  };
  
  /// Constructor for observation
  Extractable(int channel);
  /// Constructor for rate
  Extractable(std::string id);
  /// Constructor for nuisance
  Extractable(std::string id, std::string distribution, std::string description);
  /// Constructor for nuisance with asymmetric errors
  Extractable(std::string id, std::string distribution, std::string description, bool isAsymmetric);
  /// Constructor for shape nuisance
  Extractable(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string upPrefix, std::string downPrefix);

  virtual ~Extractable();
  /// Mines result from datasets and merges dataset results together
  virtual double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  
  virtual double doExtractAsymmetricUpperValue(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);

  virtual void addHistogramsToFile(std::string label, std::string id, TFile* f);
  
  /// For debugging
  virtual void print();

  bool isObservation() const { return fType == kExtractableObservation; }
  bool isRate() const { return fType == kExtractableRate; }
  bool isNuisance() const { return fType == kExtractableNuisance; }
  bool isNuisanceAsymmetric() const { return fType == kExtractableNuisanceAsymmetric; }
  bool isShapeNuisance() const { return (isNuisance() && sDistribution == "shapeQ"); }

  std::string& getDistribution() { return sDistribution; }
  std::string& getId() { return sId; }
  std::string& getDescription() { return sDescription; }
  
  void addExtractableToBeMerged(Extractable* e) { vExtractablesToBeMerged.push_back(e); }
  bool isMerged() const { return bIsMerged; }
  void setIsMerged(std::string masterId ) { bIsMerged = true; sMergedMasterId = masterId; }
  std::string getMergedMasterId() { return sMergedMasterId; }
  Extractable* mergedContainId(std::string id);
  std::vector<Extractable*> getMergedExtractables() { return vExtractablesToBeMerged; }

protected:
  TH1F* getCounterHistogram(TFile* f, std::string counterHisto);
  int getCounterItemIndex(TH1F* h, std::string counterItem);
  double getMergedValue(std::vector< Dataset* > datasets, NormalisationInfo* info, double hostValue); // Returns first non zero value
  
protected:
  std::string sDistribution;
  std::string sId;
  std::string sDescription;
  
  std::vector<Extractable*> vExtractablesToBeMerged; // list of extractables who's results are to be merged to this one (practically an or function)

private:
  const ExtractableType fType;
  bool bIsMerged; // if true, the nuisance will not produce a new line
  std::string sMergedMasterId; // if non-empty, contains the ID of the master
  
};

#endif
