#ifndef DATASET_H
#define DATASET_H

#include <TFile.h>
#include <fstream>

class Dataset {

public:
  Dataset(std::string filename);
  virtual ~Dataset();

  TFile* getFile() { return fFile; }
  std::string& getFilename() { return sFilename; }
  bool isRootFile() const { return fFile != 0; }
  
private:
  TFile* fFile;
  std::string sFilename;
};

#endif // DATASET_H
