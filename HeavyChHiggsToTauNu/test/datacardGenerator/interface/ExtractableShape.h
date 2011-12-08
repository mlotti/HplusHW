#ifndef EXTRACTABLESHAPE_H
#define EXTRACTABLESHAPE_H

#include "Extractable.h"

class TH1;

class ExtractableShape : public Extractable {
public:
  /// Constructor for nuisance
  ExtractableShape(std::string id, std::string distribution, std::string description, std::string histoName, std::string upPrefix, std::string downPrefix);
  ~ExtractableShape();

  double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  void addHistogramsToFile(std::string label, std::string id, TFile* f);
  void print();

private:
  std::string sHistoName;
  std::string sUpPrefix;
  std::string sDownPrefix;

  TH1* hUp;
  TH1* hDown;

};

#endif