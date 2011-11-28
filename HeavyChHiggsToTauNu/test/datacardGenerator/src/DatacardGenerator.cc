#include "DatacardGenerator.h"
#include "TMath.h"
#include "TH1F.h"
#include "TFile.h"

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <iomanip>

DatacardGenerator::DatacardGenerator(int massPoint, time_t timestamp)
: fMassPoint(massPoint),
  fTimestamp(timestamp) {
  struct tm * timeinfo;
  char buffer[80];
  timeinfo = std::localtime(&timestamp);
  std::strftime (buffer,80,"%d%m%y_%H%M%S",timeinfo);
  sDirectory = buffer;
}

DatacardGenerator::~DatacardGenerator() {

}

bool DatacardGenerator::generateDataCard(std::string description, double luminosity, 
                                         std::string shapeSource, bool useShapes, 
                                         std::vector< Extractable* >& extractables, 
                                         std::vector< DatasetGroup* >& datasetGroups,
                                         NormalisationInfo* info) {
  // Initialise
  fNormalisationInfo = info;
  sResult.str("");

  // Ask once the rate values to make control plots into their separate root files
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    if (datasetGroups[j]->isData() || !datasetGroups[j]->hasMassPoint(fMassPoint)) continue;
    for (size_t i = 0; i < extractables.size(); ++i) {
      if (!extractables[i]->isRate()) continue;
      if (datasetGroups[j]->hasExtractable(extractables[i])) {
        datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
      }
    }
  }

  std::cout << "Generating datacard for mass point " << fMassPoint << std::endl;

  // Construct name of directory
  sDirectory = "datacards_" + sDirectory + "_" + description;
  if (useShapes)
    sDirectory += "_withShapes";
  
  // Make directory if it doesn't already exist
  std::stringstream s;
  s << sDirectory+"/datacard" << fMassPoint << ".txt";
  
  std::ofstream myFile(s.str().c_str());
  if (myFile.bad() || myFile.fail()) {
    std::string myDirCommand = "mkdir " + sDirectory;
    int myResult = std::system(myDirCommand.c_str());
    if (myResult) return false; // could not create directory
    myFile.open(s.str().c_str());
    if (myFile.bad() || myFile.fail()) {
      std::cout << "Error: Cannot open file '" << s.str() << "' for output!" << std::endl;
      return false;
    }
  }
  
  // Open root file
  std::stringstream myOutName;
  if (useShapes) {
    myOutName << sDirectory << "/" << shapeSource << fMassPoint << ".root";
    fFile = TFile::Open(myOutName.str().c_str(), "RECREATE");
    if (!fFile) return false;
  }
  
  // Construct result
  std::string mySeparator = generateSeparatorLine(datasetGroups, extractables, useShapes);
  generateHeader(description, luminosity);
  sResult << mySeparator << std::endl;
  generateParameterLines(datasetGroups, extractables, useShapes);
  sResult << mySeparator << std::endl;
  if (useShapes) {
    generateShapeHeader(shapeSource);
    sResult << mySeparator << std::endl;
  }
  generateObservationLine(datasetGroups, extractables, useShapes);
  sResult << mySeparator << std::endl;
  generateProcessLines(datasetGroups);
  sResult << mySeparator << std::endl;
  generateRateLine(datasetGroups, extractables, useShapes);
  sResult << mySeparator << std::endl;
  generateNuisanceLines(datasetGroups, extractables, useShapes);
  
  // dummy
  std::cout << std::endl << sResult.str() << std::endl;
  
  myFile << sResult.str() << std::endl;
  myFile.close();
  std::cout << "Written datacard to file: " << s.str() << std::endl;
  if (useShapes) {
    fFile->Write();
    fFile->Close();
    std::cout << "Written shape root file to: " << myOutName.str() << std::endl;
  }
  return true;
}

void DatacardGenerator::generateHeader(std::string description, double luminosity) {
  // Description line
  sResult << "Description: LandS datacard (auto generated) mass=" << fMassPoint 
          << ", lumi=" << std::fixed << std::setprecision(3) << luminosity
          << " fb-1, " << description << std::endl;
  // Time stamp
  time_t myRawTime = 0;
  std::time (&myRawTime);
  sResult << "Date: " << std::ctime(&myRawTime);
}

void DatacardGenerator::generateParameterLines(std::vector<DatasetGroup*>& datasetGroups,
                                               std::vector< Extractable* >& extractables, 
                                               bool useShapes) {
  int nChannel = 0;
  int nNuisances = 0;
  // Calculate number of channels
  for (size_t i = 0; i < datasetGroups.size(); ++i) {
    if (datasetGroups[i]->isData()) {
      if (datasetGroups[i]->getChannel() > nChannel)
        nChannel = datasetGroups[i]->getChannel();
    }
  }
  // Calculate number of nuisances
  for (size_t i = 0; i < extractables.size(); ++i) {
    if ((extractables[i]->isNuisance() || extractables[i]->isNuisanceAsymmetric()) && 
        (!extractables[i]->isShapeNuisance() || useShapes) && 
        !extractables[i]->isMerged()) {
      ++nNuisances;
    }
  }
  // Construct output
  sResult << "imax\t" << nChannel << "\tnumber of channels" << std::endl;
  sResult << "jmax\t*\tnumber of backgrounds" << std::endl;
  sResult << "kmax\t" << nNuisances << "\tnumber of nuisance parameters" << std::endl;
}

void DatacardGenerator::generateShapeHeader(std::string source) {
  sResult << "shapes * * " << source << fMassPoint << ".root"
          << " $PROCESS $PROCESS_$SYSTEMATIC" << std::endl;
}

void DatacardGenerator::generateObservationLine(std::vector< DatasetGroup* >& datasetGroups,
                                                std::vector< Extractable* >& extractables,
                                                bool useShapes) {
  sResult << "Observation";
  for (size_t i = 0; i < extractables.size(); ++i) {
    if (extractables[i]->isObservation()) {
      for (size_t j = 0; j < datasetGroups.size(); ++j) {
        if (datasetGroups[j]->hasExtractable(extractables[i])) {
          double myRate = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
          sResult << "\t" << std::fixed << std::setprecision(0) << myRate;
          if (useShapes) {
            fFile->cd();
            TH1F* h = datasetGroups[j]->getTransverseMassPlot(fNormalisationInfo, "data_obs",20,0.,400.);
            if (!h) return;
            if (TMath::Abs(myRate - h->Integral()) > 0.0001) {
              std::cout << "WARNING: Signal rate=" << myRate << " is not same as mT shape integral=" << h->Integral() << "; check mT plot source!" << std::endl;
            }
            // do not scale data !!!
          }
        }
      }
    }
  }
  sResult << std::endl;
}

std::string DatacardGenerator::generateSeparatorLine(std::vector< DatasetGroup* >& datasetGroups,
                                                     std::vector< Extractable* >& extractables,
                                                     bool useShapes) {
  // Calculate number of non-data datagroups
  size_t nDatagroups = 0;
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint))
      ++nDatagroups;
  }
  // Calculate maximum width of nuisance description field
  size_t myMaxSize = 0;
  for (size_t i = 0; i < extractables.size(); ++i) {
    if (extractables[i]->isNuisance() && 
        (!extractables[i]->isShapeNuisance() || useShapes)) {
      if (extractables[i]->getDescription().size() > myMaxSize)
        myMaxSize = extractables[i]->getDescription().size();
    }
  }
  // Construct string
  std::string myString((nDatagroups + 2) * 8 + myMaxSize, '-');
  return myString;
}

void DatacardGenerator::generateProcessLines(std::vector< DatasetGroup* >& datasetGroups) {
  // Channels
  sResult << "bin\t";
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint)) {
      sResult << "\t" << datasetGroups[j]->getChannel();
    }
  }
  sResult << std::endl;
  // Process labels
  sResult << "process\t";
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint)) {
      sResult << "\t" << datasetGroups[j]->getLabel();
    }
  }
  sResult << std::endl;
  // Process index
  int myChannel = 0;
  int myIndex = -1; // Start counting for -1 for HPlus data format
  sResult << "process\t";
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint)) {
      if (myChannel != datasetGroups[j]->getChannel()) {
        // Reset index counter
        myChannel = datasetGroups[j]->getChannel();
        myIndex = -1;
      }
      sResult << "\t" << myIndex;
    }
    if (datasetGroups[j]->hasMassPoint(fMassPoint))
      ++myIndex;
  }
  sResult << std::endl;
}

void DatacardGenerator::generateRateLine(std::vector< DatasetGroup* >& datasetGroups,
                                             std::vector< Extractable* >& extractables,
                                             bool useShapes) {
  sResult << "rate\t";
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    double myValue = 0;
    if (datasetGroups[j]->isData() || !datasetGroups[j]->hasMassPoint(fMassPoint)) continue;
    for (size_t i = 0; i < extractables.size(); ++i) {
      if (!extractables[i]->isRate()) continue;
      if (datasetGroups[j]->hasExtractable(extractables[i])) {
        myValue = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
        //std::cout << "datagroup=" << datasetGroups[j]->getLabel() << ", value=" << myValue << std::endl;
        if (useShapes) {
          fFile->cd();
          TH1F* h = datasetGroups[j]->getTransverseMassPlot(fNormalisationInfo, datasetGroups[j]->getLabel(),20,0.,400.);
          if (!h) return;
          if (h->Integral() > 0) // normalise only histograms that have entries
            h->Scale(myValue / h->Integral());
          h->SetDirectory(fFile);
        }
      }
    }
    sResult << "\t" << std::fixed << std::setprecision(2) << myValue;
  }
  sResult << std::endl;
}

void DatacardGenerator::generateNuisanceLines(std::vector< DatasetGroup* >& datasetGroups,
                                              std::vector< Extractable* >& extractables,
                                              bool useShapes) {
  for (size_t i = 0; i < extractables.size(); ++i) {
    if ((extractables[i]->isNuisance() || extractables[i]->isNuisanceAsymmetric()) && 
        (!extractables[i]->isShapeNuisance() || useShapes) && !extractables[i]->isMerged()) {
      sResult << extractables[i]->getId() << "\t"
              << extractables[i]->getDistribution() << "\t";
      for (size_t j = 0; j < datasetGroups.size(); ++j) {
        if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint)) {
          double myValue = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
          double myUpperValue = 0.0;
          if (extractables[i]->isNuisanceAsymmetric()) {
            myUpperValue = datasetGroups[j]->getUpperValueByExtractable(extractables[i], fNormalisationInfo);
          }
          if (extractables[i]->getDistribution() == "shapeQ") {
            if (myValue > 1.0) {
              sResult << "1\t";
              int myDeltaPhi = 130;
              std::cout << "\033[0;41m\033[1;37mDelta phi: " << myDeltaPhi << "\033[0;0m!" << std::endl;
              std::string sourceHisto;
              std::string sourceCounter;
              if (datasetGroups[j]->getProcess() <= 0) {
                if (myDeltaPhi == 180) { sourceHisto = "transverseMass"; sourceCounter = "btagging"; }
                if (myDeltaPhi == 160) { sourceHisto = "transverseMassAfterDeltaPhi160"; sourceCounter = "deltaPhiTauMET<160"; }
                if (myDeltaPhi == 130) { sourceHisto = "transverseMassAfterDeltaPhi130"; sourceCounter = "deltaPhiTauMET<130"; }
                if (myDeltaPhi == 90) { sourceHisto = "transverseMassAfterDeltaPhi90"; sourceCounter = "deltaPhiTauMET<90"; }
              } else if (datasetGroups[j]->getProcess() == 1 || datasetGroups[j]->getProcess() >= 5) {
                if (myDeltaPhi == 180) { sourceHisto = "NonQCDTypeIITransverseMass"; sourceCounter = "nonQCDType2:btagging"; }
                if (myDeltaPhi == 160) { sourceHisto = "NonQCDTypeIITransverseMassAfterDeltaPhi160"; sourceCounter = "nonQCDType2:deltaphi160"; }
                if (myDeltaPhi == 130) { sourceHisto = "NonQCDTypeIITransverseMassAfterDeltaPhi130"; sourceCounter = "nonQCDType2:deltaphi130"; }
                if (myDeltaPhi == 90) { sourceHisto = "NonQCDTypeIITransverseMassAfterDeltaPhi90"; sourceCounter = "nonQCDType2:deltaphi90"; }
              }
              // Get shape uncertainty from file for signal or fakes
              if (sourceHisto.size()) {
                std::stringstream myShape;
                myShape << datasetGroups[j]->getLabel() << "_JESUp";
                std::string myUpPrefix = "signalAnalysisJESPlus03eta02METMinus10";
                TH1* h = datasetGroups[j]->getTransverseMassPlot(myUpPrefix+"Counters/weighted/counter", sourceCounter, fNormalisationInfo, myShape.str(), "", myUpPrefix+"/"+sourceHisto,20,0.,400.);
                h->SetDirectory(fFile);
                myShape.str("");
                myShape << datasetGroups[j]->getLabel() << "_JESDown";
                std::string myDownPrefix = "signalAnalysisJESMinus03eta02METPlus10";
                h = datasetGroups[j]->getTransverseMassPlot(myDownPrefix+"Counters/weighted/counter", sourceCounter, fNormalisationInfo, myShape.str(), "", myDownPrefix+"/"+sourceHisto, 20,0.,400.);
                h->SetDirectory(fFile);
              }
              if (datasetGroups[j]->getProcess() == 4) {
                // EWK taus, obtain from external file
                std::string myEWKFile = "mt_variated_ewk-20111125.root";
                std::stringstream myShape;
                myShape << datasetGroups[j]->getLabel() << "_JESDown";
                std::stringstream myEWKSourceHisto;
                myEWKSourceHisto << "EWKtau_JESDown_Dphi" << myDeltaPhi;
                TH1* h = datasetGroups[j]->getTransverseMassPlot("", "", fNormalisationInfo, myShape.str(), myEWKFile, myEWKSourceHisto.str(),20,0.,400.);
                h->SetDirectory(fFile);
                myShape.str("");
                myShape << datasetGroups[j]->getLabel() << "_JESUp";
                myEWKSourceHisto.str("");
                myEWKSourceHisto << "EWKtau_JESUp_Dphi" << myDeltaPhi;
                h = datasetGroups[j]->getTransverseMassPlot("", "", fNormalisationInfo, myShape.str(), myEWKFile, myEWKSourceHisto.str(),20,0.,400.);
                h->SetDirectory(fFile);
              }
            } else
              sResult << "0\t";
          } else {
            if (TMath::Abs(myValue - 1.0) < 0.0001) {
              sResult << std::fixed << std::setprecision(0) << myValue << "\t";
            } else {
              if (extractables[i]->isNuisanceAsymmetric()) {
                // asymmetric uncertainties
                sResult << std::fixed << std::setprecision(3) << TMath::Abs(myValue-2.0) 
                        << "/" << std::setprecision(3) << myUpperValue << "\t";
              } else {
                // Tweak for trigger SF MET leg (add 10 % in quadrature)
                if ((datasetGroups[j]->getProcess() <= 1 || datasetGroups[j]->getProcess() >= 5) && extractables[i]->getId() == "1") {
                  double myNuisance = myValue - 1.0;
                  myNuisance = TMath::Sqrt(myNuisance*myNuisance + 0.1*0.1);
                  myValue = myNuisance + 1.0;
                  std::cout << "Warning: added 10 % in quadrature for trigger in datagroup " << datasetGroups[j]->getLabel() << std::endl;
                }
                sResult << std::fixed << std::setprecision(3) << myValue << "\t";
              }
            }
          }
        }
      }
      sResult << extractables[i]->getDescription() << std::endl;
    }
  }

}
