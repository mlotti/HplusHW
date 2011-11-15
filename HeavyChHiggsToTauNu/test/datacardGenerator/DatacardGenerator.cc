#include "DatacardGenerator.h"
#include "TMath.h"

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
  generateObservationLine(datasetGroups, extractables);
  sResult << mySeparator << std::endl;
  generateProcessLines(datasetGroups);
  sResult << mySeparator << std::endl;
  generateRateLine(datasetGroups, extractables);
  sResult << mySeparator << std::endl;
  generateNuisanceLines(datasetGroups, extractables, useShapes);
  
  // dummy
  std::cout << std::endl << sResult.str() << std::endl;
  
  // Make directory if it doesn't already exist
  std::stringstream s;
  s << "datacards_"+sDirectory+"/datacard_"+description;
  if (useShapes)
    s << "_withShapes";
  s << "_M" << fMassPoint << ".txt";
  
  std::ofstream myFile(s.str().c_str());
  if (myFile.bad() || myFile.fail()) {
    std::string myDirCommand = "mkdir datacards_" + sDirectory;
    int myResult = std::system(myDirCommand.c_str());
    if (myResult) return false; // could not create directory
    myFile.open(s.str().c_str());
    if (myFile.bad() || myFile.fail()) {
      std::cout << "Error: Cannot open file '" << s.str() << "' for output!" << std::endl;
      return false;
    }
  }
  myFile << sResult.str() << std::endl;
  myFile.close();
  std::cout << "Written datacard to file: " << s.str() << std::endl;
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
    if (extractables[i]->isNuisance() && 
        (!extractables[i]->isShapeNuisance() || useShapes)) {
      ++nNuisances;
    }
  }
  // Construct output
  sResult << "imax\t" << nChannel << "\tnumber of channels" << std::endl;
  sResult << "jmax\t*\tnumber of backgrounds" << std::endl;
  sResult << "kmax\t" << nNuisances << "\tnumber of nuisance parameters" << std::endl;
}

void DatacardGenerator::generateShapeHeader(std::string source) {
  sResult << "shapes * * " << source << " $PROCESS $PROCESS_$SYSTEMATIC" << std::endl;
}

void DatacardGenerator::generateObservationLine(std::vector< DatasetGroup* >& datasetGroups,
                                                std::vector< Extractable* >& extractables) {
  sResult << "Observation";
  for (size_t i = 0; i < extractables.size(); ++i) {
    if (extractables[i]->isObservation()) {
      for (size_t j = 0; j < datasetGroups.size(); ++j) {
        if (datasetGroups[j]->hasExtractable(extractables[i])) {
          sResult << "\t" << std::fixed << std::setprecision(0) << datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
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
  std::string myString((nDatagroups + 2) * 8 + myMaxSize, '=');
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
    ++myIndex;
  }
  sResult << std::endl;
}

void DatacardGenerator::generateRateLine(std::vector< DatasetGroup* >& datasetGroups,
                                             std::vector< Extractable* >& extractables) {
  sResult << "rate\t";
  for (size_t j = 0; j < datasetGroups.size(); ++j) {
    double myValue = 0;
    if (datasetGroups[j]->isData() || !datasetGroups[j]->hasMassPoint(fMassPoint)) continue;
    for (size_t i = 0; i < extractables.size(); ++i) {
      if (!extractables[i]->isRate()) continue;
      if (datasetGroups[j]->hasExtractable(extractables[i])) {
        myValue = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
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
    if (extractables[i]->isNuisance() && 
        (!extractables[i]->isShapeNuisance() || useShapes)) {
      sResult << extractables[i]->getId() << "\t"
              << extractables[i]->getDistribution() << "\t";
      for (size_t j = 0; j < datasetGroups.size(); ++j) {
        if (!datasetGroups[j]->isData() && datasetGroups[j]->hasMassPoint(fMassPoint)) {
          double myValue = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
          if (TMath::Abs(myValue - 1.0) < 0.0001) {
            sResult << std::fixed << std::setprecision(0) << myValue << "\t";
          } else {
            sResult << std::fixed << std::setprecision(3) << myValue << "\t";
          }
        }
      }
      sResult << extractables[i]->getDescription() << std::endl;
    }
  }

}
