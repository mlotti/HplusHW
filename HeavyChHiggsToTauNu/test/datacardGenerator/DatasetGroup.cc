#include "DatasetGroup.h"
#include "TMath.h"
#include <iostream>

DatasetGroup::DatasetGroup( int channel, int process, std::string label, bool isData)
: bIsData(isData), 
  iChannel(channel),
  iProcess(process),
  sLabel(label) {
  vValidMasses.push_back(-1);
}

DatasetGroup::DatasetGroup( int channel, int process, std::string label, std::vector< double > validMasses)
: bIsData(false),
  iChannel(channel),
  iProcess(process),
  sLabel(label) {
  for (std::vector<double>::iterator it = validMasses.begin(); it != validMasses.end(); ++it) {
    vValidMasses.push_back(static_cast<int>(*it));
  }
}

DatasetGroup::~DatasetGroup() {
  vValidMasses.clear();
  vExtractables.clear();
  vDatasets.clear();
}

double DatasetGroup::getValueByExtractable(Extractable* e, NormalisationInfo* info) const {
  double myValue = 0;
  // Search if Extrable::id is in the list of active ones
  if (hasExtractable(e)) {
    // Extractable is active, read its value for all files
    myValue = e->doExtract(vDatasets, info);
  }
  if (e->isNuisance())
    myValue += 1.0;
  return myValue;
}

bool DatasetGroup::hasExtractable(Extractable* e) const {
  for (std::vector<Extractable*>::const_iterator it = vExtractables.begin();
       it != vExtractables.end(); ++it) {
    if (e->getId() == (*it)->getId())
      return true;
  }
  return false;
}

bool DatasetGroup::addDatasets (std::string path, std::vector< std::string > filenames) {
  for (std::vector< std::string >::iterator it = filenames.begin(); it != filenames.end(); ++it) {
    std::string myCombinedName = path+"/"+(*it);
    if (!path.size())
      myCombinedName = (*it);
    Dataset* myDataset = new Dataset(myCombinedName);
    // Check that file has been opened successfully
    if (myDataset->getFile() < 0) {
      std::cout << "Tried to open file '" << *it << "'" << std::endl;
      return false;
    }
    vDatasets.push_back(myDataset);
  }
  return true;
}

bool DatasetGroup::hasMassPoint(double mass) const {
  for (size_t i = 0; i < vValidMasses.size(); ++i) {
    if (vValidMasses[i] == static_cast<int>(mass) || vValidMasses[i] < 0)
      return true;
  }
  return false;
}

void DatasetGroup::print() {
  std::cout << "Column: channel=" << iChannel << " process=" << iProcess << " label=" << sLabel << " masses=";
  if (vValidMasses.size() == 1) {
    if (vValidMasses[0] < 0)
      std::cout << "all";
    else
      std::cout << vValidMasses[0];
  } else {
    for (size_t i = 0; i < vValidMasses.size(); ++i) {
      if (i != 0)
        std::cout << ", ";
      std::cout << vValidMasses[i];
    }
  }
  std::cout << std::endl << "- has " << vExtractables.size() << " extractables:" << std::endl;
  for (size_t i = 0; i < vExtractables.size(); ++i) {
    if (vExtractables[i]->isRate())
      std::cout << "  - rate: id=" << vExtractables[i]->getId() << std::endl;
    else
      std::cout << "  - nuisance: id=" << vExtractables[i]->getId() << " / " 
                << vExtractables[i]->getDescription() << std::endl;
  }
  std::cout << "- has " << vDatasets.size() << " input files:" << std::endl;
  for (size_t i = 0; i < vDatasets.size(); ++i)
    std::cout << "  - " << vDatasets[i]->getFilename() << std::endl;
}
