#ifndef DATACARDGENERATOR_H
#define DATACARDGENERATOR_H

#include "Extractable.h"
#include "DatasetGroup.h"
#include "NormalisationInfo.h"

#include <string>
#include <sstream>
#include <vector>
#include <ctime>

class TFile;
class TH1F;

class DatacardGenerator {
public:
  DatacardGenerator(int massPoint, time_t timestamp);
  ~DatacardGenerator();

  bool generateDataCard(std::string description, double luminosity,
                        std::string shapeSource, bool useShapes,
                        std::vector<Extractable*>& extractables,
                        std::vector<DatasetGroup*>& datasetGroups,
                        NormalisationInfo* info);
  int getMassPoint() const { return fMassPoint; }
  
private:
  /// Generates first lines of config
  void generateHeader(std::string description, NormalisationInfo* info);
  /// Generates parameter lines
  void generateParameterLines(std::vector<DatasetGroup*>& datasetGroups,
                              std::vector< Extractable* >& extractables,
                              bool useShapes);
  /// Generates shape line
  void generateShapeHeader(std::string source);
  /// Generates observation line
  void generateObservationLine(std::vector<DatasetGroup*>& datasetGroups,
                               std::vector< Extractable* >& extractables,
                               NormalisationInfo* info,
                               bool useShapes);
  /// Generates process lines
  void generateProcessLines(std::vector<DatasetGroup*>& datasetGroups);
  /// Generates rate line
  void generateRateLine(std::vector<DatasetGroup*>& datasetGroups,
                        std::vector< Extractable* >& extractables,
                        NormalisationInfo* info,
                        bool useShapes);
  /// Generates nuisance lines (incl. shapes)
  void generateNuisanceLines(std::vector<DatasetGroup*>& datasetGroups,
                             std::vector<Extractable*>& extractables,
                             NormalisationInfo* info,
                             bool useShapes);
  /// Generate separator line
  std::string generateSeparatorLine(std::vector<DatasetGroup*>& datasetGroups,
                                    std::vector<Extractable*>& extractables,
                                    bool useShapes);
  
private:
  int fMassPoint;
  time_t fTimestamp;
  std::string sDirectory;
  std::stringstream sResult;
  NormalisationInfo* fNormalisationInfo;
  TFile* fFile;
};

#endif // DATACARDGENERATOR_H
