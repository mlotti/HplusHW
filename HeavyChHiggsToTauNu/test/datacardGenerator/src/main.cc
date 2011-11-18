#include "ConfigManager.h"

#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMath.h"
#include "TLatex.h"
#include "TCanvas.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>


/*
int getCounterBin(string label, TH1* histo) {
  int j = 1;
  while (j <= histo->GetNbinsX()+1) {
    string myBinLabel(histo->GetXaxis()->GetBinLabel(j));
    if (myBinLabel == label) return j;
    ++j;
  }
  cout << "label btagging was not found!" << endl;
  return -1;
}

double getCounterValue(string histoName, string label, TFile* aFile) {
  TH1F* h = (TH1F*)aFile->Get(histoName.c_str());
  if (!h) {
    cout << "Error: Unable to open histogram " << histoName << endl;
    return -1;
  }
  int myBin = getCounterBin(label, h);
  if (myBin < 0) return -1;
  return h->GetBinContent(myBin);
}

double getCounterRelUncertainty(string histoName, string label, TFile* aFile) {
  TH1F* h = (TH1F*)aFile->Get(histoName.c_str());
  if (!h) {
    cout << "Error: Unable to open histogram " << histoName << endl;
    return -1;
  }
  int myBin = getCounterBin(label, h);
  if (myBin < 0) return -1;
  return h->GetBinError(myBin) / h->GetBinContent(myBin);
}

// ----------------------------------------------------------------------
int main(int argc, char** argv) {
  vector<string> names;
  names.push_back("signalAnalysis/Trigger/TriggerScaleFactorUncertainty");
  names.push_back("signalAnalysis/Btagging/BTagUncertainty");

  vector<string> jesNames;
  jesNames.push_back("signalAnalysisCounters/weighted/counter");
  jesNames.push_back("signalAnalysisJESPlus03eta02METPlus10Counters/weighted/counter");
  jesNames.push_back("signalAnalysisJESMinus03eta02METPlus10Counters/weighted/counter");
  jesNames.push_back("signalAnalysisJESPlus03eta02METMinus10Counters/weighted/counter");
  jesNames.push_back("signalAnalysisJESMinus03eta02METMinus10Counters/weighted/counter");

  string leptonVetoName = "signalAnalysisCounters/weighted/counter";

  if (argc < 2) {
    std::cout << "Usage: generateTauIDFactorizationMap sample.root [sample2.root] [...]" << std::endl;
    return -1;
  }

  for (int i = 1; i < argc; ++i) {
    // Obtain stub of filename
    std::string myFilename(argv[i]);
    size_t myPos = myFilename.find_last_of('/');
    if (myPos == myFilename.size()) {
      myPos = 0;
    } else {
      ++myPos;
    }
    myFilename = myFilename.substr(myPos, myFilename.size());
    myFilename = myFilename.substr(0, myFilename.find_last_of('.'));
    // Replace any dash signs in filename stub with underscore (python does not like dashes)
    for (int j = 0; j < static_cast<int>(myFilename.size()); ++j) {
      if (myFilename[j] == '-') myFilename[j] = '_';
    }

    // Open file
    std::cout << "Processing sample: " << myFilename << std::endl;
    TFile* myFile = TFile::Open(argv[i]);
    if (!myFile) {
      std::cout << "Error: File '" << argv[i] << "' does not exist or could not be opened!" << std::endl;
      return -1;
    }

    // Loop over histograms
    for (vector<string>::iterator it = names.begin(); it != names.end(); ++it) {
      TH1F* h = (TH1F*)myFile->Get((*it).c_str());
      if (!h) {
        cout << "Error: Unable to open histogram " << *it << endl;
        return -1;
      }
      // Calculate total
      double myTotal = 0;
      for (int j = 1; j <= h->GetNbinsX(); ++j) {
        myTotal += h->GetBinContent(j);
      }
      // Calculate uncertainty
      double mySum = 0;
      for (int j = 1; j <= h->GetNbinsX(); ++j) {
       // double myValue = h->GetBinContent(j) / myTotal * h->GetBinCenter(j);
       // mySum += myValue*myValue;
        double myValue = h->GetBinContent(j) * h->GetBinCenter(j);
        mySum += myValue*myValue * h->GetBinContent(j);
        //if (myValue > 0) cout << h->GetBinCenter(j) << "," << h->GetBinContent(j) << endl;
      }
      //cout << *it << ", Total weight," << myTotal << ",rel.uncertainty," << TMath::Sqrt(mySum) << endl;
      cout << *it << ", Total weight," << myTotal << ",rel.uncertainty," << TMath::Sqrt(mySum)/myTotal << endl;
    }

    // JES
    double myNominalSignalCount = 0;
    double myNominalTypeIICount = 0;
    double mySignalRatio = 0;
    double myTypeIIRatio = 0;

    //cout << "TAS/JES/MET," << endl;;
    for (vector<string>::iterator it = jesNames.begin(); it != jesNames.end(); ++it) {
      TH1F* h = (TH1F*)myFile->Get((*it).c_str());
      if (!h) {
        cout << "Error: Unable to open histogram " << *it << endl;
        return -1;
      }
      // get counter bins
      int mySignalBin = getCounterBin("btagging",h);
      int myTypeIIBin = getCounterBin("nonQCDType2:btagging",h);
      if (mySignalBin < 0 || myTypeIIBin < 0) return -1;
      if (myNominalSignalCount == 0) {
        myNominalSignalCount = h->GetBinContent(mySignalBin);
      } else {
        double myValue = TMath::Abs(h->GetBinContent(mySignalBin) - myNominalSignalCount);
        myValue /= myNominalSignalCount;
        //cout << "," << myValue;
        if (myValue > mySignalRatio) 
          mySignalRatio = myValue;
      }
      //cout << endl;
      if (myNominalTypeIICount == 0) {
        myNominalTypeIICount = h->GetBinContent(myTypeIIBin);
      } else {
        double myValue = TMath::Abs(h->GetBinContent(myTypeIIBin) - myNominalTypeIICount);
        myValue /= myNominalTypeIICount;
        //cout << "," << myValue;
        if (myValue > myTypeIIRatio) 
          myTypeIIRatio = myValue;
      }
      //cout << endl;
    }
    cout << "Signal TAS/JES/MET," << mySignalRatio << endl;
    cout << "(TypeII TAS/JES/MET," << myTypeIIRatio << ") use Signal TAS/JES/MET instead" << endl;

    // Get counter histogram
    TH1F* h = (TH1F*)myFile->Get(leptonVetoName.c_str());
    if (!h) {
      cout << "Error: Unable to open histogram " << leptonVetoName << endl;
      return -1;
    }

    // Lepton veto for signal
    int myMETBin = getCounterBin("MET",h);
    int myEVetoBin = getCounterBin("electron veto",h);
    int myMuVetoBin = getCounterBin("muon veto",h);
    if (myMETBin < 0 || myEVetoBin < 0 || myMuVetoBin < 0) return -1;
    // not passed / passed * Delta
    double myEUncertainty = (h->GetBinContent(myMETBin) - h->GetBinContent(myEVetoBin)) / h->GetBinContent(myEVetoBin) * 0.02;
    double myMuUncertainty = (h->GetBinContent(myEVetoBin) - h->GetBinContent(myMuVetoBin)) / h->GetBinContent(myMuVetoBin) * 0.01;
    cout << "Signal eveto uncert," << myEUncertainty << ", muveto uncert," <<myMuUncertainty << ",combined uncert.," 
         << TMath::Sqrt(myEUncertainty*myEUncertainty + myMuUncertainty*myMuUncertainty) << endl;

    // Lepton veto for type II
    myMETBin = getCounterBin("nonQCDType2:MET",h);
    myEVetoBin = getCounterBin("nonQCDType2:electron veto",h);
    myMuVetoBin = getCounterBin("nonQCDType2:muon veto",h);
    if (myMETBin < 0 || myEVetoBin < 0 || myMuVetoBin < 0) return -1;
    // not passed / passed * Delta
    myEUncertainty = (h->GetBinContent(myMETBin) - h->GetBinContent(myEVetoBin)) / h->GetBinContent(myEVetoBin) * 0.02;
    myMuUncertainty = (h->GetBinContent(myEVetoBin) - h->GetBinContent(myMuVetoBin)) / h->GetBinContent(myMuVetoBin) * 0.01;
    cout << "TypeII eveto uncert," << myEUncertainty << ", muveto uncert," <<myMuUncertainty << ",combined uncert.," 
         << TMath::Sqrt(myEUncertainty*myEUncertainty + myMuUncertainty*myMuUncertainty) << endl;

    // Statistical uncertainty signal
    int myBTagBin = getCounterBin("btagging",h);
    cout << "Signal statistical uncert.," << h->GetBinError(myBTagBin) / h->GetBinContent(myBTagBin) << endl;

    // Statistical uncertainty type II
    myBTagBin = getCounterBin("nonQCDType2:btagging",h);
    cout << "TypeII statistical uncert.," << h->GetBinError(myBTagBin) / h->GetBinContent(myBTagBin) << endl;

    // Type II fake composition
    double etau = getCounterValue("signalAnalysisCounters/weighted/e->tau", ":btagging", myFile);
    double mutau = getCounterValue("signalAnalysisCounters/weighted/e->tau", ":btagging", myFile);
    double jettau = getCounterValue("signalAnalysisCounters/weighted/jet->tau", ":btagging", myFile);
    double tauOutside = getCounterValue("signalAnalysisCounters/weighted/e->tau with tau outside acceptance", ":btagging", myFile)
      + getCounterValue("signalAnalysisCounters/weighted/mu->tau with tau outside acceptance", ":btagging", myFile)
      + getCounterValue("signalAnalysisCounters/weighted/jet->tau with tau outside acceptance", ":btagging", myFile);
    double all = etau + mutau + jettau + tauOutside;
    cout << "Type II composition: e->tau," << etau/all << ",mu->tau," << mutau/all << ",jet->tau," << jettau/all << ",tau outside acceptance," << tauOutside/all << ",total weight," << all << endl;
    

  }
  return 0;
}
*/

void printUsage() {
  std::cout << "Usage: datacardgenerator myconfigfile.config [params]" << std::endl;
  std::cout << "Parameters include:" << std::endl
            << "  -h  Print this help message" << std::endl
            << "  -v  Print additional info (i.e. verbose)" << std::endl;
  
}

int main(int argc, char** argv) {
  std::string myConfigName;
  bool myVerboseStatus = false;
  // Loop over arguments
  for (int i = 1; i < argc; ++i) {
    std::string myArg(argv[i]);
    if (myArg.size() > 7) {
      if (myArg.substr(myArg.size()-7) == ".config") {
        myConfigName = myArg;
      }
    } else if (myArg[0] == '-') {
    // Parse options
      if (myArg == "-h") {
        printUsage();
        return 0;
      } else if (myArg == "-v") {
        myVerboseStatus = true;
      } else {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Unknown argument: " << myArg << std::endl;
        printUsage();
        return 0;
      }
    }
  }
  if (!myConfigName.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m No config file was given as argument!" << std::endl;
    printUsage();
    return 0;
  }

  ConfigManager myManager(myVerboseStatus);
  if (!myManager.initialize(myConfigName)) return 0;
  myManager.generateCards();
  return 0;
}