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

  std::cout << std::endl << "\033[0;44m\033[1;37mGenerating datacard for mass point" << fMassPoint << "\033[0;0m" << std::endl;

  // Construct name of directory
  sDirectory = "datacards_" + sDirectory + "_" + description;
  if (useShapes)
    sDirectory += "_withShapes";

  if (info->getLuminosityScaling() > 1)
    sDirectory += "_forecastByLumiScaling";

  // Make directory if it doesn't already exist
  std::stringstream s;
  s << sDirectory+"/datacard_fullyhadronic_m" << fMassPoint << ".txt";

  std::ofstream myFile(s.str().c_str());
  if (myFile.bad() || myFile.fail()) {
    std::string myDirCommand = "mkdir " + sDirectory;
    int myResult = std::system(myDirCommand.c_str());
    if (myResult) return false; // could not create directory
    myFile.open(s.str().c_str());
    if (myFile.bad() || myFile.fail()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Cannot open file '" << s.str() << "' for output!" << std::endl;
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
  generateHeader(description, info);
  sResult << mySeparator << std::endl;
  generateParameterLines(datasetGroups, extractables, useShapes);
  sResult << mySeparator << std::endl;
  if (useShapes) {
    generateShapeHeader(shapeSource);
    sResult << mySeparator << std::endl;
  }
  generateObservationLine(datasetGroups, extractables, info, useShapes);
  sResult << mySeparator << std::endl;
  generateProcessLines(datasetGroups);
  sResult << mySeparator << std::endl;
  generateRateLine(datasetGroups, extractables, info, useShapes);
  sResult << mySeparator << std::endl;
  generateNuisanceLines(datasetGroups, extractables, info, useShapes);
  
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

std::cout << "Datacard was generated for luminosity \033[0;44m\033[1;37m" << info->getLuminosity() << " 1/fb\033[0;0m" << std::endl;
  if (info->getLuminosityScaling() > 1)
    std::cout << "\033[0;43m\033[1;37mWarning: Luminosity is artificially scaled to " << info->getLuminosity()*info->getLuminosityScaling()  << " 1/fb\033[0;0m" << std::endl;

  return true;
}

void DatacardGenerator::generateHeader(std::string description, NormalisationInfo* info) {
  // Description line
  sResult << "Description: LandS datacard (auto generated) mass=" << fMassPoint;
  if (info->getLuminosityScaling() > 1)
    sResult << ", luminosity artificially scaled from " 
            << std::fixed << std::setprecision(3) << info->getLuminosity()
            << " to " 
            << std::fixed << std::setprecision(3) << info->getLuminosity() * info->getLuminosityScaling() << " 1/fb";
  else
    sResult << ", luminosity=" << std::fixed << std::setprecision(3) << info->getLuminosity()
          << " 1/fb";
  sResult << ", " << description << std::endl;
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
                                                NormalisationInfo* info,
                                                bool useShapes) {
  sResult << "Observation";
  for (size_t i = 0; i < extractables.size(); ++i) {
    if (extractables[i]->isObservation()) {
      for (size_t j = 0; j < datasetGroups.size(); ++j) {
        if (datasetGroups[j]->hasExtractable(extractables[i])) {
          double myRate = datasetGroups[j]->getValueByExtractable(extractables[i], fNormalisationInfo);
          sResult << "\t" << std::fixed << std::setprecision(0) << myRate;
          if (useShapes) {
            TH1F* h = datasetGroups[j]->getTransverseMassPlot(fNormalisationInfo, "data_obs",20,0.,400.);
            if (!h) return;
            if (TMath::Abs(myRate - h->Integral()) > 0.0001) {
              std::cout << "WARNING: Signal rate=" << myRate << " is not same as mT shape integral=" << h->Integral() << "; check mT plot source!" << std::endl;
            }
            // do not scale data except for lumi forecast
            if (info->getLuminosityScaling() > 1) {
              for (int k = 1; k <= h->GetNbinsX(); ++k)
                h->SetBinError(k, h->GetBinError(k)*TMath::Sqrt(1.0/info->getLuminosityScaling()));
            }
            h->SetDirectory(fFile);
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
                                             NormalisationInfo* info,
                                             bool useShapes) {
  if (useShapes) std::cout << "Generating rates and rate histograms" << std::endl;
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
          if (datasetGroups[j]->getLabel() == "QCD" || datasetGroups[j]->getLabel() == "QCDInv") {
            extractables[i]->addHistogramsToFile(datasetGroups[j]->getLabel(),"",fFile);
          } else {
            TH1F* h = datasetGroups[j]->getTransverseMassPlot(fNormalisationInfo, datasetGroups[j]->getLabel(),20,0.,400.);
            if (!h) return;
            double mySum = h->Integral();// + h->GetBinContent(0) + h->GetBinContent(h->GetNbinsX()+1);
            if (mySum > 0) // normalise only histograms that have entries
              h->Scale(myValue / mySum);
            // Scale down uncertainties for EWK since they come from data (scaling does not change the relative uncertainty)
            if (datasetGroups[j]->getLabel() == "EWKTau" && info->getLuminosityScaling() > 1) {
              for (int k = 1; k <= h->GetNbinsX(); ++k)
                h->SetBinError(k, h->GetBinError(k)*TMath::Sqrt(1.0/info->getLuminosityScaling()));
              std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m EWKTau rate uncertainty scaled for lumi forecast" << std::endl;
            }
            h->SetDirectory(fFile);
            std::cout << "  Created histogram " << h->GetTitle() << " with normalisation " << myValue << " source=" << datasetGroups[j]->getMtPlotName() << std::endl;
          }
        }
      }
    }
    sResult << "\t" << std::fixed << std::setprecision(2) << myValue;
  }
  sResult << std::endl;
}

void DatacardGenerator::generateNuisanceLines(std::vector< DatasetGroup* >& datasetGroups,
                                              std::vector< Extractable* >& extractables,
                                              NormalisationInfo* info,
                                              bool useShapes) {
  if (useShapes) std::cout << "Generating nuisances and shape histograms" << std::endl;
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
          if (extractables[i]->isShapeNuisance()) {
            if (myValue > 0) {
              sResult << "1\t";
              // doextractable has been called, store histograms
              std::vector<Extractable*> myMerged = extractables[i]->getMergedExtractables();
              for (size_t k = 0; k < myMerged.size(); ++k) {
                if (datasetGroups[j]->hasExtractable(myMerged[k])) {
                  myMerged[k]->addHistogramsToFile(datasetGroups[j]->getLabel(), extractables[i]->getId(), fFile);
                }
              }
              if (datasetGroups[j]->hasExtractable(extractables[i]))
                extractables[i]->addHistogramsToFile(datasetGroups[j]->getLabel(), extractables[i]->getId(), fFile);
              // begin code for normalising shape uncertainty to rate
              /*std::string myNameUp = datasetGroups[j]->getLabel() + "_" + extractables[i]->getId() + "Up";
              std::string myNameDown = datasetGroups[j]->getLabel() + "_" + extractables[i]->getId() + "Down";
              TH1* hup = dynamic_cast<TH1*>(fFile->Get(myNameUp.c_str()));
              TH1* hdown = dynamic_cast<TH1*>(fFile->Get(myNameDown.c_str()));
              if (hup && hdown) {
                double myRate = 0.;
                for (size_t x = 0; x < extractables.size(); ++x) {
                  if (extractables[x]->isRate() && datasetGroups[j]->hasExtractable(extractables[x]))
                    myRate = datasetGroups[j]->getValueByExtractable(extractables[x], fNormalisationInfo);
                }
                if (myRate > 0.0) {
                  hup->Scale(myRate / hup->Integral());
                  hdown->Scale(myRate / hdown->Integral());
                  std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m shape nuisance " << myNameUp << " and " << myNameDown << " normalised to measured rate " << myRate << std::endl;
                }
              }*/
              // end code for normalising shape uncertainty to rate
            } else {
              sResult << "0\t";
            }
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
                  double myNuisance = (myValue - 1.0);
                  if (info->getLuminosityScaling() > 1) {
                    myNuisance /= TMath::Sqrt(info->getLuminosityScaling());
                    std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m trg uncertainty scaled for lumi forecast for sample " << datasetGroups[j]->getLabel() << std::endl;
                  }
                  myNuisance = TMath::Sqrt(myNuisance*myNuisance + 0.1*0.1);
                  myValue = myNuisance + 1.0;
                  std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m added 10 % in quadrature for trigger in datagroup " << datasetGroups[j]->getLabel() << std::endl;
                } else if (datasetGroups[j]->getProcess() == 4 && (extractables[i]->getId() == "1" || extractables[i]->getId() == "19")) {
                  // Tweak for EWK tau trg eff and stat downscaling for lumi forecast
                  if (info->getLuminosityScaling() > 1) {
                    myValue -= 1.0;
                    myValue /= TMath::Sqrt(info->getLuminosityScaling());
                    std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m EWKTau trg / stat. uncertainty scaled for lumi forecast" << std::endl;
                    myValue += 1.0;
                  }
                }
// FIXME remove
/*
                if ((datasetGroups[j]->getProcess() <= 1 || datasetGroups[j]->getProcess() >= 5)) {
                  if (extractables[i]->getId() == "1") myValue = 1.25;
                  if (extractables[i]->getId() == "10") myValue = 1.15;
                  if (extractables[i]->getId() == "11") myValue = 1.11;
                }
                if ((datasetGroups[j]->getProcess() == 4)) {
                  if (extractables[i]->getId() == "1") myValue = 1.096;
                  if (extractables[i]->getId() == "7") myValue = 1.176;
                }
*/
// FIXME end remove
                sResult << std::fixed << std::setprecision(3) << myValue << "\t";
              }
            }
          }
        }
      }
      sResult << extractables[i]->getDescription() << std::endl;
    }
  }
  // Tweak for EWKTau JES error bars in case of lumi scaling
  if (useShapes && info->getLuminosityScaling() > 1) {
    TH1* h = dynamic_cast<TH1*>(fFile->Get("EWKTau_7Up"));
    if (h)
      for (int k = 1; k < h->GetNbinsX(); ++k)
        h->SetBinError(k, h->GetBinError(k) / TMath::Sqrt(info->getLuminosityScaling()));
    h = dynamic_cast<TH1*>(fFile->Get("EWKTau_7Down"));
    if (h)
      for (int k = 1; k < h->GetNbinsX(); ++k)
        h->SetBinError(k, h->GetBinError(k) / TMath::Sqrt(info->getLuminosityScaling()));
    std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m EWKTau JES uncertainty shape errors scaled for lumi forecast" << std::endl;
  }
}
