#include "QCDInverted.h"

#include "TMath.h"
#include "TSystem.h"
#include <iostream>

QCDInverted::QCDInverted(int channel, std::string counterHisto, std::string counterItem, std::string filePath):
  Extractable(channel),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem),
  path(filePath)
{}

QCDInverted::QCDInverted(std::string id, std::string counterHisto, std::string counterItem, std::string filePath):
  Extractable(id),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem),
  path(filePath)
{}

QCDInverted::QCDInverted(std::string id, std::string distribution, std::string description, std::string counterHisto, std::string counterItem, std::string filePath):
  Extractable(id, distribution, description),
  sCounterHisto(counterHisto),
  sCounterItem(counterItem),
  path(filePath)
{}


QCDInverted::~QCDInverted(){}
  
double QCDInverted::doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation){

	if(path[path.length()-1] != '/') path += '/';

  	// Loop over histograms to obtain result
  	double fCounterValue = 0.; // result in number of events
  	double fCounterUncertainty = 0.; // result in number of events
  	for (std::vector<Dataset*>::iterator it = datasets.begin(); it != datasets.end(); ++it) {
  	  if ((*it)->isRootFile()) {
  	    // Open histogram and check validity
  	    TH1F* h = getCounterHistogram((*it)->getFile(), sCounterHisto);
  	    if (!h) return -1.;
  	    // Obtain bin index of counter
  	    int myBinIndex = getCounterItemIndex(h, sCounterItem);
  	    if (!myBinIndex) return -1.;
  	    // Obtain result
  	    double myNormFactor = info->getNormalisationFactor((*it)->getFile());
  	    if (isObservation()) myNormFactor = info->getLuminosityScaling();
  	    fCounterValue += h->GetBinContent(myBinIndex) * myNormFactor;
  	    fCounterUncertainty += h->GetBinError(myBinIndex) * h->GetBinError(myBinIndex)
  	      * myNormFactor * myNormFactor;
  	  }
  	}
  	// Return result
  	fCounterUncertainty = TMath::Sqrt(fCounterUncertainty);
  	if (isObservation() || isRate())
  	  return fCounterValue * additionalNormalisation;
  	else if (isNuisance())
  	  return fCounterUncertainty / fCounterValue; // Relative uncertainty
  	return -1.;
}

void QCDInverted::addHistogramsToFile(std::string label, std::string id, TFile* fOUT){


        std::string filePlusPath = path + "transverseMassQCDInverted.root";

	TFile* fIN = 0;
	fIN = TFile::Open(filePlusPath.c_str());
	if(!fIN){
		std::cout << "\033[0;41m\033[1;37mError:\033[0;0m file " << filePlusPath 
                          << " not found. Did you remember to run plotSignalAnalysisInverted.py in " << path <<  "?" << std::endl;
		exit(0);
	}

        TH1F* hOUT = (TH1F*)fIN->Get("mtSum");
	hOUT->SetName(label.c_str());
	hOUT->Sumw2();
	hOUT->SetDirectory(fOUT);
	std::cout << "  Created histogram " << label << std::endl;

	fIN->Close();
}
