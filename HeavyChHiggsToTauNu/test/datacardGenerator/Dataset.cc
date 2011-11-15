#include "Dataset.h"
#include <iostream>

Dataset::Dataset(std::string filename)
: fFile(0),
  sFilename(filename) {
  // Check if the file is a root file
  if (filename.substr(filename.size()-5) == ".root") {
    //std::cout << filename << std::endl;
    fFile = TFile::Open(filename.c_str());
    if (!fFile) {
      std::cout << "Error: Cannot open root file '" << filename << "'!" << std::endl;
      fFile = 0;
    }
  } else if (filename.substr(filename.size()-4) == ".txt") {
    
  } else {
    // Assume that user has provided a grid file directory
    size_t myBegin = filename.find_last_of('/') + 1;
    if (myBegin > filename.size())
      myBegin = 0;
    std::string myTestFile = filename + "/res/histograms-" + filename.substr(myBegin) + ".root";
    sFilename = myTestFile;
    fFile = TFile::Open(myTestFile.c_str());
    if (!fFile) {
      std::cout << "Error: Cannot open root file '" << myTestFile << "'!" << std::endl;
      std::cout << "Check filename / did you run HPlusMergeHistograms.py?" << std::endl;
      fFile = 0;
    }
  }
}

Dataset::~Dataset() {

}
