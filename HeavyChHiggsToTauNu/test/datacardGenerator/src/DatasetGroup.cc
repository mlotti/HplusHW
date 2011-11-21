#include "DatasetGroup.h"
#include "TMath.h"
#include "TH1F.h"
#include "TFile.h"
#include <iostream>

DatasetGroup::DatasetGroup( int channel, int process, std::string label, bool isData, std::string mTPlot, std::string mTFile)
: bIsData(isData), 
  iChannel(channel),
  iProcess(process),
  sLabel(label),
  sExternalFileForTransverseMassPlot(mTFile),
  sTransverseMassPlotNameWithPath(mTPlot) {
  vValidMasses.push_back(-1);
}

DatasetGroup::DatasetGroup( int channel, int process, std::string label, std::vector< double > validMasses, std::string mTPlot, std::string mTFile)
: bIsData(false),
  iChannel(channel),
  iProcess(process),
  sLabel(label),
  sExternalFileForTransverseMassPlot(mTFile),
  sTransverseMassPlotNameWithPath(mTPlot) {
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
  } else {
    // Search id in merged extractables
    std::vector<Extractable*> myMerged = e->getMergedExtractables();
    for (size_t i = 0; i < myMerged.size(); ++i) {
      if (hasExtractable(myMerged[i])) {
        myValue = myMerged[i]->doExtract(vDatasets, info);
      }
    }
  }
  
  // Return result
  if (e->isNuisance() || e->isNuisanceAsymmetric())
    myValue += 1.0;
  return myValue;
}

double DatasetGroup::getUpperValueByExtractable(Extractable* e, NormalisationInfo* info) const {
  double myValue = 0;
  // Search if Extrable::id is in the list of active ones
  if (hasExtractable(e)) {
    // Extractable is active, read its value for all files
    myValue = e->doExtractAsymmetricUpperValue(vDatasets, info);
  } else {
    // Search id in merged extractables
    std::vector<Extractable*> myMerged = e->getMergedExtractables();
    for (size_t i = 0; i < myMerged.size(); ++i) {
      if (hasExtractable(myMerged[i])) {
        myValue = myMerged[i]->doExtractAsymmetricUpperValue(vDatasets, info);
      }
    }
  }
  
  // Return result
  if (e->isNuisanceAsymmetric())
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

bool DatasetGroup::addDatasets (std::string path, std::vector< std::string > filenames, NormalisationInfo* info) {
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
    // Print output
    std::cout << "  File " << *it << " norm. factor=" << info->getNormalisationFactor(myDataset->getFile()) << std::endl;
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

TH1F* DatasetGroup::getTransverseMassPlot(NormalisationInfo* info, std::string name, int bins, double min, double max) {
  TH1F* myPlot = new TH1F(name.c_str(), name.c_str(), bins, min, max);
  /*for (int i = 1; i <= myPlot->GetNbinsX(); ++i) {
    myPlot->SetBinContent(i,0);
    myPlot->SetBinError(i,0);
  }*/
  myPlot->Sumw2();
  if (sTransverseMassPlotNameWithPath == "empty") return myPlot;
  if (sExternalFileForTransverseMassPlot.size()) {
    // Obtain plot from external file
    std::cout << "Obtaining plot '" << sTransverseMassPlotNameWithPath << "' from file '" << sExternalFileForTransverseMassPlot << "'";
    TFile* f = TFile::Open(sExternalFileForTransverseMassPlot.c_str());
    if (!f) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open file " << sExternalFileForTransverseMassPlot << "!" << std::endl;
      return myPlot;
    }
    TH1* myHisto = dynamic_cast<TH1*>(f->Get(sTransverseMassPlotNameWithPath.c_str()));
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open histogram " << sTransverseMassPlotNameWithPath << " in file " 
                << sExternalFileForTransverseMassPlot << "!" << std::endl;
      //std::cout << f << ", " << myHisto << std::endl;
      return myPlot;
    }
    if (myHisto->GetNbinsX() > myPlot->GetNbinsX()) {
      //std::cout << "bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
      myHisto->Rebin(myHisto->GetNbinsX() / myPlot->GetNbinsX());
      //std::cout << "new bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
    }
    myPlot->Add(myHisto);
    return myPlot;
  }
    
  // Obtain plot from datasets
  for (size_t i = 0; i < vDatasets.size(); ++i) {
    std::cout << "Obtaining plot '" << sTransverseMassPlotNameWithPath << "' from file '" << vDatasets[i]->getFilename() << "'" << std::endl;
    TH1F* myHisto = (dynamic_cast<TH1F*>(vDatasets[i]->getFile()->Get(sTransverseMassPlotNameWithPath.c_str())));
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open histogram " << sTransverseMassPlotNameWithPath << " in file " << vDatasets[i]->getFilename() << "!" << std::endl;
      return myPlot;
    }
    if (!bIsData)
      myHisto->Scale(info->getNormalisationFactor(vDatasets[i]->getFile()));
    if (myHisto->GetNbinsX() > myPlot->GetNbinsX())
      myHisto->Rebin(myHisto->GetNbinsX() / myPlot->GetNbinsX());
    myPlot->Add(myHisto);
  }
  return myPlot; // empty histogram, if no datasets
}
