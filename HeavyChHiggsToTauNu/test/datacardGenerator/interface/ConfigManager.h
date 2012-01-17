#ifndef CONFIGMANAGER_H
#define CONFIGMANAGER_H

#include "Extractable.h"
#include "DatasetGroup.h"
#include "DatacardGenerator.h"
#include "NormalisationInfo.h"

#include <string>
#include <vector>

class ConfigManager {

public:
  ConfigManager(bool verbose);
  virtual ~ConfigManager();

  bool initialize(std::string configFile);
  bool doExtract();
  void generateCards(bool useShapes);

private:
  bool checkValidity();
  double parseNumber(std::string str, size_t& pos);
  std::string parseLabel(std::string str, size_t& pos);
  std::string parseString(std::string str, size_t& pos);
  void parseVectorString(std::string str, size_t& pos, std::vector< std::string >& myStrings);
  void parseVectorValue(std::string str, size_t& pos, std::vector<double>& myValues);
  bool addExtractable(std::string str, Extractable::ExtractableType type);
  bool addDataGroup(std::string str);
  bool addMergingOfExtractable(std::string str);
  bool registerExtractable(DatasetGroup* group, std::string id);
  
private:
  std::vector<Extractable*> vExtractables; // Owner
  std::vector<DatasetGroup*> vDatasetGroups; // Owner
  std::vector<DatacardGenerator*> vDatacardGenerators; // Owner
  NormalisationInfo* fNormalisationInfo; // Owner
  NormalisationInfo* fNormalisationInfoQCD; // Owner

  std::string sDescription;
  std::string sShapeSource;
  double fLuminosity; // in fb-1
  bool bVerbose;
  
};

#endif // CONFIGMANAGER_H

