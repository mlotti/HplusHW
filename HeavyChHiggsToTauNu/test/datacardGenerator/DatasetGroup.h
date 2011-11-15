#ifndef DATASETGROUP_H
#define DATASETGROUP_H
#include "Dataset.h"
#include "Extractable.h"
#include "NormalisationInfo.h"

#include <vector>
#include <string>

class DatasetGroup {

public:
  /// Constructor for all masses
  DatasetGroup(int channel, int process, std::string label, bool isData);
  /// Constructor for specified masses
  DatasetGroup(int channel, int process, std::string label, std::vector<double> validMasses);
  virtual ~DatasetGroup();

  bool addDatasets(std::string path, std::vector< std::string > filenames);
  bool isData() const { return bIsData; }
  int getProcess() const { return iProcess; }
  int getChannel() const { return iChannel; }
  std::string getLabel() { return sLabel; }
  void addExtractable(Extractable* e) { vExtractables.push_back(e); }
  double getValueByExtractable(Extractable* e, NormalisationInfo* info) const;
  bool hasExtractable(Extractable* e) const;
  bool hasMassPoint(double mass) const;
  void print();
  
private:
  bool bIsData;
  int iChannel;
  int iProcess;
  std::string sLabel;
  std::vector<int> vValidMasses; // Mass points for which group is active
  std::vector<Extractable*> vExtractables; // Extractables which are active for the group
  std::vector<Dataset*> vDatasets;
  
};

#endif // DATASETGROUP_H
