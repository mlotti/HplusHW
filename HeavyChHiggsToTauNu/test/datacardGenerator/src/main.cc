#include "ConfigManager.h"

#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMath.h"
#include "TLatex.h"
#include "TCanvas.h"
#include "TStyle.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

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
  // Initiate config manager and generate datacards
  ConfigManager myManager(myVerboseStatus);
  if (!myManager.initialize(myConfigName)) return 0;
  myManager.generateCards();
  return 0;
}