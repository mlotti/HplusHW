#ifndef DATASETGROUP_H
#define DATASETGROUP_H
#include "Dataset.h"
#include "Extractable.h"
#include "NormalisationInfo.h"

#include <vector>
#include <string>

class TH1F;
class DatasetGroup {

public:
  /// Constructor for all masses
  DatasetGroup(int channel, int process, std::string label, bool isData, std::string mTPlot, std::string mTFile);
  /// Constructor for specified masses
  DatasetGroup(int channel, int process, std::string label, std::vector<double> validMasses, std::string mTPlot, std::string mTFile);
  virtual ~DatasetGroup();

  bool addDatasets(std::string path, std::vector< std::string > filenames, NormalisationInfo* info);
  bool isData() const { return bIsData; }
  int getProcess() const { return iProcess; }
  int getChannel() const { return iChannel; }
  std::string getLabel() { return sLabel; }
  void addExtractable(Extractable* e) { vExtractables.push_back(e); }
  double getValueByExtractable(Extractable* e, NormalisationInfo* info) const;
  double getUpperValueByExtractable(Extractable* e, NormalisationInfo* info) const;
  TH1F* getTransverseMassPlot(NormalisationInfo* info, std::string name, int bins, double min, double max);
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
  
  // mT info
  std::string sExternalFileForTransverseMassPlot;
  std::string sTransverseMassPlotNameWithPath;
  
};

#endif // DATASETGROUP_H
