#include "DatasetGroup.h"
#include "TMath.h"
#include "TH1F.h"
#include "TFile.h"
#include <iostream>

DatasetGroup::DatasetGroup( int channel, int process, std::string label, bool isData, std::string mTPlot, std::string mTFile, double additionalNormalisationFactor)
: bIsData(isData), 
  iChannel(channel),
  iProcess(process),
  fAdditionaNormalisationFactor(additionalNormalisationFactor),
  sLabel(label),
  sExternalFileForTransverseMassPlot(mTFile),
  sTransverseMassPlotNameWithPath(mTPlot) {
  vValidMasses.push_back(-1);
}

DatasetGroup::DatasetGroup( int channel, int process, std::string label, std::vector< double > validMasses, std::string mTPlot, std::string mTFile, double additionalNormalisationFactor)
: bIsData(false),
  iChannel(channel),
  iProcess(process),
  fAdditionaNormalisationFactor(additionalNormalisationFactor),
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

double DatasetGroup::getRate(NormalisationInfo* info) const {
  for (size_t i = 0; i < vExtractables.size(); ++i) {
    if (vExtractables[i]->isRate())
      return getValueByExtractable(vExtractables[i], info);
  }
  return -1.;
}

double DatasetGroup::getValueByExtractable(Extractable* e, NormalisationInfo* info) const {
  double myValue = 0;
  // Search if Extrable::id is in the list of active ones
  if (hasExtractable(e)) {
    // Extractable is active, read its value for all files
    myValue = e->doExtract(vDatasets, info, fAdditionaNormalisationFactor);
    if (e->isShapeNuisance())
      return 1.0;
  } else {
    // Search id in merged extractables
    std::vector<Extractable*> myMerged = e->getMergedExtractables();
    for (size_t i = 0; i < myMerged.size(); ++i) {
      if (hasExtractable(myMerged[i])) {
        myValue = myMerged[i]->doExtract(vDatasets, info, fAdditionaNormalisationFactor);
        if (myMerged[i]->isShapeNuisance())
          return 1.0;
      }
    }
  }
  
  // Return result
  if (e->isShapeNuisance())
    return 0.0;
  
  if (e->isNuisance() || e->isNuisanceAsymmetric())
    myValue += 1.0;
  return myValue;
}

double DatasetGroup::getUpperValueByExtractable(Extractable* e, NormalisationInfo* info) const {
  double myValue = 0;
  // Search if Extrable::id is in the list of active ones
  if (hasExtractable(e)) {
    // Extractable is active, read its value for all files
    myValue = e->doExtractAsymmetricUpperValue(vDatasets, info, fAdditionaNormalisationFactor);
  } else {
    // Search id in merged extractables
    std::vector<Extractable*> myMerged = e->getMergedExtractables();
    for (size_t i = 0; i < myMerged.size(); ++i) {
      if (hasExtractable(myMerged[i])) {
        myValue = myMerged[i]->doExtractAsymmetricUpperValue(vDatasets, info, fAdditionaNormalisationFactor);
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
    std::cout << "  File " << *it << " norm. factor=" << info->getNormalisationFactor(myDataset->getFile());
    if (TMath::Abs(fAdditionaNormalisationFactor - 1.0) > 0.00001)
      std::cout << " additional norm. factor=" << fAdditionaNormalisationFactor;
    if (TMath::Abs(info->getLuminosityScaling() - 1.0) > 0.00001)
      std::cout << " scaling of luminosity for forecast=" << info->getLuminosityScaling();
    std::cout << std::endl;
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
    std::cout << "Obtaining plot '" << sTransverseMassPlotNameWithPath << "' from file '" << sExternalFileForTransverseMassPlot << "'" << std::endl;
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
    } else if (myHisto->GetNbinsX() < myPlot->GetNbinsX()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m You asked for " << myPlot->GetNbinsX() << ", but the provided histogram for " << sLabel << " has only " << myHisto->GetNbinsX() << " bins!" << std::endl;
    }
    myPlot->Add(myHisto);
    myPlot->Scale(fAdditionaNormalisationFactor);
    f->Close();
    return myPlot;
  }
    
  // Obtain plot from datasets
  for (size_t i = 0; i < vDatasets.size(); ++i) {
    //std::cout << "Obtaining plot '" << sTransverseMassPlotNameWithPath << "' from file '" << vDatasets[i]->getFilename() << "'" << std::endl;
    TH1F* myHisto = (dynamic_cast<TH1F*>(vDatasets[i]->getFile()->Get(sTransverseMassPlotNameWithPath.c_str())));
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open histogram " << sTransverseMassPlotNameWithPath << " in file " << vDatasets[i]->getFilename() << "!" << std::endl;
      return myPlot;
    }
    double myNormFactor = 1.0;
    if (bIsData) {
      myNormFactor = info->getLuminosityScaling();
    } else {
      myNormFactor = info->getNormalisationFactor(vDatasets[i]->getFile());
    }
    if (myHisto->GetNbinsX() > myPlot->GetNbinsX())
      myHisto->Rebin(myHisto->GetNbinsX() / myPlot->GetNbinsX());
    myPlot->Add(myHisto, myNormFactor);
  }
  myPlot->Scale(fAdditionaNormalisationFactor);
  return myPlot; // empty histogram, if no datasets
}

TH1F* DatasetGroup::getTransverseMassPlot(std::string counterHisto, std::string counterName, NormalisationInfo* info, std::string name, std::string file, std::string source, int bins, double min, double max) {
  TH1F* myPlot = new TH1F(name.c_str(), name.c_str(), bins, min, max);
  /*for (int i = 1; i <= myPlot->GetNbinsX(); ++i) {
    myPlot->SetBinContent(i,0);
    myPlot->SetBinError(i,0);
  }*/
  myPlot->Sumw2();
  
  if (file.size()) {
    // Obtain plot from external file
    std::cout << "Obtaining plot '" << source << "' from file '" << file << "'" << std::endl;
    TFile* f = TFile::Open(file.c_str());
    if (!f) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open file " << file << "!" << std::endl;
      return myPlot;
    }
    TH1* myHisto = dynamic_cast<TH1*>(f->Get(source.c_str()));
    if (!myHisto) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not open histogram " << source << " in file " 
                << file << "!" << std::endl;
      //std::cout << f << ", " << myHisto << std::endl;
      return myPlot;
    }
    if (myHisto->GetNbinsX() > myPlot->GetNbinsX()) {
      //std::cout << "bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
      myHisto->Rebin(myHisto->GetNbinsX() / myPlot->GetNbinsX());
      //std::cout << "new bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
    } else if (myHisto->GetNbinsX() < myPlot->GetNbinsX()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m You asked for " << myPlot->GetNbinsX() << ", but the provided histogram for " << sLabel << " has only " << myHisto->GetNbinsX() << " bins!" << std::endl;
    }
    myPlot->Add(myHisto); // FIXME for 2011B
    f->Close();
    myPlot->Scale(fAdditionaNormalisationFactor);
    return myPlot;
  } else {
    // Obtain plot from datasets
    for (size_t i = 0; i < vDatasets.size(); ++i) {
      //std::cout << "Obtaining plot '" << source << "' from file '" << vDatasets[i]->getFilename() << "'" << std::endl;
      // Obtain normalisation from counter
      TH1* myCounterHisto = dynamic_cast<TH1*>(vDatasets[i]->getFile()->Get(counterHisto.c_str()));
      if (!myCounterHisto) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not find histogram " << counterHisto << " in file " << vDatasets[i]->getFilename() << "!" << std::endl;
        return myPlot;
      }
      // Find counter item
      bool myFoundStatus = false;
      double myCount = 0.;
      for (int k = 1; k <= myCounterHisto->GetNbinsX(); ++k) {
        std::string myBinLabel = myCounterHisto->GetXaxis()->GetBinLabel(k);
        if (myBinLabel == counterName) {
          myFoundStatus = true;
          double myNormFactor = 1.0;
          if (bIsData) {
            myNormFactor = info->getLuminosityScaling();
          } else {
            myNormFactor = info->getNormalisationFactor(vDatasets[i]->getFile());
          }
          myCount = myCounterHisto->GetBinContent(k) * myNormFactor;
        }
      }
      if (!myFoundStatus) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not find counter name " << counterName << " in histogram " << counterHisto << " in file " << vDatasets[i]->getFilename() << "!" << std::endl;
        return myPlot;
      }
      // Find histogram by name
      TH1* h = dynamic_cast<TH1*>(vDatasets[i]->getFile()->Get(source.c_str()));
      if (!h) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not find histogram " << source << " in file " << vDatasets[i]->getFilename() << "!" << std::endl;
        return myPlot;
      }
      // Normalise to counts
      if (h->Integral() > 0)
        h->Scale(myCount / h->Integral());
      // Rebin if necessary
      if (h->GetNbinsX() > myPlot->GetNbinsX()) {
        h->Rebin(h->GetNbinsX() / myPlot->GetNbinsX());
      }
      // Add to result histogram
      std::cout << "... plot found with rate of " << myCount << std::endl;
      myPlot->Add(h); // FIXME for 2011B
    }
  }
  myPlot->Scale(fAdditionaNormalisationFactor);
  return myPlot; // empty histogram, if no datasets
}
