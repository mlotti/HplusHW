#include "ConfigManager.h"
#include "ExtractableCounter.h"
#include "ExtractableMaxCounter.h"
#include "ExtractableConstant.h"
#include "ExtractableRatio.h"
#include "ExtractableScaleFactor.h"

#include <fstream>
#include <iostream>
#include <sstream>
#include <ctime>

ConfigManager::ConfigManager(bool verbose)
: fNormalisationInfo(0),
  sDescription(""),
  fLuminosity(-1.0),
  bVerbose(verbose) {
  
}

ConfigManager::~ConfigManager() {

}

bool ConfigManager::initialize(std::string configFile) {
  std::cout << "Processing config file " << configFile << " ..." << std::endl;
  if (!bVerbose)
    std::cout << "For more output of configuration parsing, run with parameter -v" << std::endl;
  
  // Time stamp
  time_t myTimestamp;
  std::time(&myTimestamp);
  
  // Open file
  std::ifstream myFile(configFile.c_str());
  if (myFile.bad() || myFile.fail()) {
    std::cout << "Error opening config file '" << configFile << "'!" << std::endl;
    return false;
  }
  // Read file contents
  std::string myLine;
  std::string myConfigInfoHisto;
  std::string myCounterHisto;
  myLine.reserve(2048);
  std::string myCommand;
  myCommand.reserve(100);
  while (!myFile.eof()) {
    size_t myDummyPos = 0;
    // Read line
    std::getline(myFile, myLine);
    // Check that line contains data
    if (myLine.size() < 10) continue;
    // Check comment sign
    if (myLine[0] == '#') continue;
    // Read first word and process the line
    myCommand = parseLabel(myLine, myDummyPos);
    //std::cout << "command : " << myCommand << std::endl;
    myLine.substr(0,myLine.find_first_of('='));
    if (myCommand == "description") {
      sDescription = parseString(myLine, myDummyPos);
      if (bVerbose) std::cout << "Description: " << sDescription << std::endl;
    } else if (myCommand == "configInfoHisto") {
      myConfigInfoHisto = parseString(myLine, myDummyPos);
      if (bVerbose) std::cout << "ConfigInfo histogram: " << myConfigInfoHisto << std::endl;
    } else if (myCommand == "counterHisto") {
      myCounterHisto = parseString(myLine, myDummyPos);
      if (bVerbose) std::cout << "Counter histogram: " << myCounterHisto << std::endl;
    } else if (myCommand == "shapeSource") {
      sShapeSource = parseString(myLine, myDummyPos);
      if (bVerbose) std::cout << "Source of shapes: " << sShapeSource << std::endl;
    } else if (myCommand == "masspoint") {
      int myMassPoint = static_cast<int>(parseNumber(myLine, myDummyPos));
      vDatacardGenerators.push_back(new DatacardGenerator(myMassPoint, myTimestamp));
      if (bVerbose) std::cout << "Added masspoint " << myMassPoint << std::endl;
    } else if (myCommand == "luminosity") {
      fLuminosity = parseNumber(myLine, myDummyPos);
      if ( bVerbose) std::cout << "Luminosity set to " << fLuminosity << std::endl;
    } else if (myCommand == "observation") {
      if (!fNormalisationInfo) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m provide configInfoHisto, counterHisto, and luminosity before observation!" << std::endl;
        return false;
      }
      if (!addExtractable(myLine.substr(myDummyPos+1), Extractable::kExtractableObservation)) return false;
    } else if (myCommand == "rate") {
      if (!fNormalisationInfo) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m provide configInfoHisto, counterHisto, and luminosity before rate!" << std::endl;
        return false;
      }
      if (!addExtractable(myLine.substr(myDummyPos+1), Extractable::kExtractableRate)) return false;
    } else if (myCommand == "nuisance") {
      if (!fNormalisationInfo) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m provide configInfoHisto, counterHisto, and luminosity before nuisance!" << std::endl;
        return false;
      }
      if (!addExtractable(myLine.substr(myDummyPos+1), Extractable::kExtractableNuisance)) return false;
    } else if (myCommand == "column") {
      if (!fNormalisationInfo) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m provide configInfoHisto, counterHisto, and luminosity before column!" << std::endl;
        return false;
      }
      if (!addDataGroup(myLine.substr(myDummyPos+1))) return false;
    } else if (myCommand == "mergeNuisances") {
      if (!addMergingOfExtractable(myLine.substr(myDummyPos+1))) return false;
    } else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m unknown command '" << myCommand << "'!" << std::endl;
      return false;
    }

    if (!fNormalisationInfo) {
      if (myConfigInfoHisto.size()>0 && myCounterHisto.size()>0 && fLuminosity > 0) {
        // Create normalisation info object
        fNormalisationInfo = new NormalisationInfo(myConfigInfoHisto, myCounterHisto, fLuminosity);
      }
    }
  }

  if (bVerbose) {
    // Print extractables and dataset groups
    std::cout << std::endl << "Parsed config for observation:" << std::endl;
    for (std::vector<DatasetGroup*>::const_iterator it = vDatasetGroups.begin(); it != vDatasetGroups.end(); ++it)
      if ((*it)->isData())
        (*it)->print();
    std::cout << std::endl << "Parsed config for rate:" << std::endl;
    for (std::vector<Extractable*>::const_iterator it = vExtractables.begin(); it != vExtractables.end(); ++it)
      if ((*it)->isRate()) (*it)->print();
    std::cout << std::endl << "Parsed config for rows:" << std::endl;
    for (std::vector<Extractable*>::const_iterator it = vExtractables.begin(); it != vExtractables.end(); ++it)
      if ((*it)->isNuisance()) (*it)->print();
    std::cout << std::endl << "Parsed config for columns:" << std::endl;
    for (std::vector<DatasetGroup*>::const_iterator it = vDatasetGroups.begin(); it != vDatasetGroups.end(); ++it)
      if (!(*it)->isData())
        (*it)->print();
  }

  // Check that enough parameters have been given for reasonable operation
  if (!myConfigInfoHisto.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m configInfoHisto is not provided in config file!" << std::endl;
    return false;
  } else if (!myCounterHisto.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m counterHisto is not provided in config file!" << std::endl;
    return false;
  }
  if (!checkValidity())
    return false;

  std::cout << std::endl << "Configuration has been read" << std::endl;
  return true;
}

bool ConfigManager::checkValidity() {
  if (!sDescription.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Description is not provided in config file!" << std::endl;
    return false;
  }
  if (!vDatacardGenerators.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m No mass points provided in config file!" << std::endl;
    return false;
  }
  if (fLuminosity <= 0) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m No luminosity provided in config file!" << std::endl;
    return false;
  }
  
  if (!vDatasetGroups.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m No columns provided in config file!" << std::endl;
    return false;
  }
  
  // Check dataset group labels
  for (size_t i = 0; i < vDatasetGroups.size(); ++i) {
    for (size_t j = i+1; j < vDatasetGroups.size(); ++j) {
      bool myStatus = true;
      if (vDatasetGroups[i]->getLabel() == "Data" && vDatasetGroups[j]->getLabel() == "Data") {
        if (vDatasetGroups[i]->getChannel() == vDatasetGroups[j]->getChannel()) {
          std::cout << "\033[0;41m\033[1;37mError:\033[0;0m two identical channels given for observation!" << std::endl;
          myStatus = false;
        }
      } else {
        if (vDatasetGroups[i]->getLabel() == vDatasetGroups[j]->getLabel()) {
          std::cout << "\033[0;41m\033[1;37mError:\033[0;0m two identical labels found for columns!" << std::endl;
          myStatus = false;
        }
      }
      if (!myStatus) {
        std::cout << std::endl;
        vDatasetGroups[i]->print();
        std::cout << std::endl;
        vDatasetGroups[j]->print();
        return false;
      }
    }
  }
  
  // Check rates and nuisance id's
  for (size_t i = 0; i < vExtractables.size(); ++i) {
    for (size_t j = i+1; j < vExtractables.size(); ++j) {
      bool myStatus = true;
      if (vExtractables[i]->isRate() && vExtractables[j]->isRate()) {
        if (vExtractables[i]->getId() == vExtractables[j]->getId()) {
          std::cout << "\033[0;41m\033[1;37mError:\033[0;0m two identical id's given for rate!" << std::endl;
          myStatus = false;
        }
      } else if (vExtractables[i]->isNuisance() && vExtractables[j]->isNuisance()) {
        if (vExtractables[i]->getId() == vExtractables[j]->getId()) {
          std::cout << "\033[0;41m\033[1;37mError:\033[0;0m two identical id's given for nuisance!" << std::endl;
          myStatus = false;
        }
      }
      if (!myStatus) {
        std::cout << std::endl;
        vExtractables[i]->print();
        std::cout << std::endl;
        vExtractables[j]->print();
        return false;
      }
    }
  }
  
  return true;
}

std::string ConfigManager::parseLabel( std::string str, size_t& pos ) {
  // Extract string between last space and the '=' character
  size_t myEqualPos = str.find_first_of('=', pos);
  if (myEqualPos > str.size()) {
    // no sign was found
    //std::cout << "\033[0;41m\033[1;37mError:\033[0;0m tried to read a label, but could not find the = sign!" << std::endl;
    //std::cout << "  Parsed string: " << str.substr(myEqualPos) << std::endl;
    pos = 9999;
    return "";
  }
  // Find space character(s) before the equal sign
  bool myStatus = true;
  while (myStatus) {
    size_t myTestPos = str.find_first_of(",{ ", pos);
    if (myTestPos == pos && pos < myEqualPos) {
      // Space or other non-alphabetical character was found, advance by one
      ++pos;
    } else {
      myStatus = false;
    }
  }
  // Update position and return
  size_t myStart = pos;
  pos = myEqualPos; // new position is equal sign position
  // Remove space at the end of the string
  if (str[myEqualPos-1] == ' ')
    --myEqualPos;
  if (myEqualPos - myStart > 0)
    return str.substr(myStart, myEqualPos - myStart);
  std::cout << "\033[0;41m\033[1;37mError:\033[0;0m tried to read a string, but string length is zero!" << std::endl;
  std::cout << "  Parsed string: " << str.substr(myStart) << std::endl; 
  return "";
}

double ConfigManager::parseNumber( std::string str, size_t& pos) {
  size_t maxPos = str.size();
  size_t myTempPos = str.find_first_of("},", pos);
  if (myTempPos < maxPos)
    maxPos = myTempPos;
  //std::cout <<"parse: " << str.substr(pos, maxPos-pos+1) << std::endl;
  // Extract number after the '= {' characters
  std::stringstream s;
  bool myStatus = true;
  while (myStatus) {
    size_t myTempPos = str.find_first_of("= {", pos);
    if (myTempPos < maxPos)
      if (myTempPos == pos)
        ++pos;
      else
        myStatus = false;
    else
      myStatus = false;
  }
  if (pos > maxPos)
    return -9999;
  //std::cout <<"parse: pos=" << pos << "/" << maxPos <<" str=" << str << " -> " << str.substr(pos) << std::endl;
  s.str(str.substr(pos));
  double myValue;
  s >> myValue;
  pos += s.tellg();
  return myValue;
}

std::string ConfigManager::parseString ( std::string str, size_t& pos) {
  size_t maxPos = str.size();
  size_t myTempPos = str.find_first_of("},", pos);
  if (myTempPos < maxPos)
    maxPos = myTempPos;
  // Extract the string inside parentheses
  size_t myFirstPos = str.find_first_of('"', pos);
  size_t myLastPos = str.find_first_of('"', myFirstPos+1);
  // Check if nothing was found
  if (myLastPos > maxPos) {
    return "";
  }
  /*if (myLastPos == myFirstPos + 1) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m empty string given as input!" << std::endl;
    pos = 9999;
    return "";
  }*/
  // Update position and return
  pos = myLastPos+1; // position after parenthesis
  if (myLastPos > myFirstPos)
    return str.substr(myFirstPos+1, myLastPos-1 - myFirstPos);
  return "";
}

void ConfigManager::parseVectorString ( std::string str, size_t& pos, std::vector< std::string >& myStrings) {
  // Extract the vector of strings inside curly parentheses
  size_t myEqualPos = str.find_first_of('=', pos);
  size_t myOpeningBracket = str.find_first_of('{', myEqualPos+1);
  size_t myClosingBracket = str.find_first_of('}', myOpeningBracket);
  if (myOpeningBracket == myClosingBracket) {
    // No brackets were found
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m tried to read a vector, but could not find curly brackets!" << std::endl;
    std::cout << "  Parsed string: " << str.substr(myEqualPos) << std::endl;
    pos = 9999;
    return;
  }
  size_t myCurrentPos = myOpeningBracket;
  bool myStatus = true;
  while (myCurrentPos < myClosingBracket && myStatus) {
    ++myCurrentPos;
    std::string myStr = parseString(str, myCurrentPos);
    if (myStr.size())
      myStrings.push_back(myStr);
    else 
      myStatus = false;
    if (myCurrentPos < str.size())
      if (str[myCurrentPos] != ',')
        myStatus = false;
  }
  pos = myClosingBracket+1; // position after closing bracket
}

void ConfigManager::parseVectorValue( std::string str, size_t& pos, std::vector<double>& myValues) {
  // Extract the vector of strings inside curly parentheses
  size_t myEqualPos = str.find_first_of('=', pos);
  size_t myOpeningBracket = str.find_first_of('{', myEqualPos+1);
  size_t myClosingBracket = str.find_first_of('}', myOpeningBracket);
  if (myOpeningBracket > str.size() || myClosingBracket > str.size()) {
    // No brackets were found
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m tried to read a vector, but could not find curly brackets!" << std::endl;
    std::cout << "  Parsed string: " << str.substr(myEqualPos) << std::endl;
    pos = 9999;
    return;
  }
  size_t myCurrentPos = myOpeningBracket+1;
  bool myStatus = true;
  while (myCurrentPos < myClosingBracket && myStatus) {
    double myValue = parseNumber(str, myCurrentPos);
    if (myValue > -9000) {
      myValues.push_back(myValue);
    }
    if (myCurrentPos < str.size())
      if (str[myCurrentPos] != ',')
        myStatus = false;
  }
  pos = myClosingBracket+1; // position after closing bracket
}


bool ConfigManager::addExtractable ( std::string str, Extractable::ExtractableType type ) {
  size_t myPos = 0;
  double myChannel = 0;
  std::vector< std::string > myFiles;
  std::string myId;
  std::string myDistribution;
  std::string myDescription;
  std::string myFunction;
  std::string myCounterHisto;
  std::string myInput1;
  std::string myInput2;
  std::string myFilePath;
  std::string myMTPlot;
  double myValue = -1;
  double myValue2 = -1;
  std::string myLabel = "default";
  // Obtain items
  while (myPos < str.size() && myLabel.size()) {
    //std::cout << " Extractable at pos " << myPos << std::endl;
    // Get label
    myLabel = parseLabel(str, myPos);
    if (myPos < str.size() && myLabel != "") {
      // Check label
      if (myLabel == "id") {
        myId = parseString(str, myPos);
      } else if (myLabel == "distribution") {
        myDistribution = parseString(str, myPos);
      } else if (myLabel == "description") {
        myDescription = parseString(str, myPos);
      } else if (myLabel == "function") {
        myFunction = parseString(str, myPos);
      } else if (myLabel == "counterHisto") {
        myCounterHisto = parseString(str, myPos);
      } else if (myLabel == "histogram" || myLabel == "nominatorCounter" || myLabel == "counter") {
        myInput1 = parseString(str, myPos);
      } else if (myLabel == "denominatorCounter" || myLabel == "normHisto") {
        myInput2 = parseString(str, myPos);
      } else if (myLabel == "lowerValue" || myLabel == "value" || myLabel == "scale") {
        myValue = parseNumber(str, myPos);
      } else if (myLabel == "upperValue") {
        myValue2 = parseNumber(str, myPos);
      } else if (myLabel == "channel") {
        myChannel = parseNumber(str, myPos);
      } else if (myLabel == "filePath") {
        myFilePath = parseString(str, myPos);
      } else if (myLabel == "mTPlot") {
        myMTPlot = parseString(str, myPos);
      } else if (myLabel == "files" || myLabel == "counterPaths") {
        parseVectorString(str, myPos, myFiles);
      } else {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m unknown label in config: '" << myLabel << "'!" << std::endl;
        std::cout << "  Parsed string: " << str << std::endl;
        return false;
      }
    }
  }
  /* if (myPos > 9000) {
    std::cout << "Error occurred for label '" << myLabel << "' on line: " << str << std::endl;
    return false;
  }*/
  // Check that all parameters were supplied and create extractable object
  bool myStatus = true;
  // Check required fields
  if (type == Extractable::kExtractableObservation) {
    if (myChannel == 0) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'channel' for observation!" << std::endl;
      myStatus = false;
    } else if (!myFiles.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'file' for observation!" << std::endl;
      myStatus = false;
    } else if (!myMTPlot.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'mTPlot' for observation!" << std::endl;
      myStatus = false;
    }
    if (!myStatus) {
      std::cout << "  line in config: " << str << std::endl << std::endl;
      std::cout << "Example of correct syntax:" << std::endl;
      std::cout << "observation = { channel=1, function=" << '"' 
                <<  "functionName" << '"' << ", functionparameters, [filePath="
                << '"' << "path" << '"' << ",] file={"
                << '"' << "file1.root" << '"' << ", " << '"' << "file2.root"
                << '"' << " ... } }, mTPlot=" << '"' << "plotwithpath" << '"' << std::endl;
    }
  } else if (type == Extractable::kExtractableRate) {
    // Check required fields
    if (!myId.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'id' for rate!" << std::endl;
      myStatus = false;
    }
    if (!myStatus) {
      std::cout << "  line in config: " << str << std::endl << std::endl;
      std::cout << "  rate = { id=" << '"' << "idlabel" << '"' 
          << ", function=" << '"' << "functionName" << '"' 
          << ", functionParameters }" << std::endl;
    }
  } else if (type == Extractable::kExtractableNuisance) {
    if (!myId.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'id' for nuisance!" << std::endl;
      myStatus = false;
    } else if (!myDistribution.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'distribution' for nuisance!" << std::endl;
      myStatus = false;
    } else if (!myDescription.size()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'description' for nuisance!" << std::endl;
      myStatus = false;
    }
    if (!myStatus) {
      std::cout << "  line in config: " << str << std::endl << std::endl;
      std::cout << "Example of correct syntax:" << std::endl;
      std::cout << "  nuisance = { id=" << '"' << "idlabel" << '"' 
                << ", distribution=" << '"' << "lnN" << '"' << ", description="
                << '"' << "description of nuisance parameter" << '"'
                << ", function=" << '"' << "functionName" << '"' 
                << ", functionParameters }" << std::endl;
    }
  }
  if (!myStatus) return false;
  // Check that function is defined properly
  bool myFunctionStatus = true;
  if (!myFunction.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'function'!" << std::endl;
    myFunctionStatus = false;
  } else if (!myCounterHisto.size() || !myInput1.size() || !myInput2.size() || myValue < 0) {
    if (myFunction == "Constant") {
      if (myValue < 0) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'value' for function 'Constant'!" << std::endl;
        myFunctionStatus = false;
      }
    } else if (myFunction == "Counter") {
      if (!myCounterHisto.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counterHisto' for function 'Counter'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput1.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counter' for function 'Counter'!" << std::endl;
        myFunctionStatus = false;
      }
    } else if (myFunction == "maxCounter") {
      if (!myFiles.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counterPaths' for function 'maxCounter'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput1.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counter' for function 'maxCounter'!" << std::endl;
        myFunctionStatus = false;
      }
    } else if (myFunction == "Ratio") {
      if (!myCounterHisto.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counterHisto' for function 'Ratio'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput1.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'nominatorCounter' for function 'Ratio'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput2.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'denominatorCounter' for function 'Ratio'!" << std::endl;
        myFunctionStatus = false;
      }
    } else if (myFunction == "ScaleFactor") {
      if (!myCounterHisto.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'counterHisto' for function 'ScaleFactor'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput1.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'histogram' for function 'ScaleFactor'!" << std::endl;
        myFunctionStatus = false;
      } else if (!myInput2.size()) {
        std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing or empty field 'normHisto' for function 'ScaleFactor'!" << std::endl;
        myFunctionStatus = false;
      }      
    } else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m specified function is unknown! (valid functions are 'Constant', 'Counter', 'Ratio', 'ScaleFactor', you tried '" << myFunction << "')" << std::endl;
      myFunctionStatus = false;
    }
    if (!myFunctionStatus) {
      std::cout << "  line in config: " << str << std::endl << std::endl;
      std::cout << "Example of functions and their parameters:" << std::endl;
      std::cout << "  function=" << '"' << "Constant" << '"' 
                << ", value=" << '"' << "0.07" << '"' << std::endl;
      std::cout << "  function=" << '"' << "Constant" << '"' 
                << ", lowerValue=" << '"' << "0.05" << '"'
                << ", upperValue=" << '"' << "0.07" << '"' << std::endl;
      std::cout << "  function=" << '"' << "Counter" << '"' 
                << ", counterHisto=" << '"' << "counterHisto" << '"'
                << ", counter=" << '"' << "counterName" << '"' << std::endl;
      std::cout << "  function=" << '"' << "maxCounter" << '"' 
                << ", counterPaths={" << '"' << "pathToCounter" << '"'
                << ", ...}, counter=" << '"' << "counterName" << '"' << std::endl;
      std::cout << "  function=" << '"' << "Ratio" << '"' 
                << ", counterHisto=" << '"' << "counterHisto" << '"'
                << ", nominatorCounter=" << '"' << "counterName" << '"'
                << ", denominatorCounter=" << '"' << "counterName" << '"' << std::endl;
      std::cout << "  function=" << '"' << "ScaleFactor" << '"' 
                << ", counterHisto=" << '"' << "counterHisto" << '"'
                << ", histogram=" << '"' << "scaleFactorAbsUncertaintyHistogramNameWithPath" << '"'
                << ", histogram=" << '"' << "scaleFactorAbsUncertaintyCountsHistogramNameWithPath" << '"' << std::endl;
    }
  }
  if (!myFunctionStatus)
    return false;
  
  // All available parameters have been defined; now create the objects
  // Create extractable
  Extractable* myExtractable = 0;
  if (myFunction == "Constant") {
    if (type == Extractable::kExtractableObservation)
      myExtractable = new ExtractableConstant(myChannel, myValue);
    else if (type == Extractable::kExtractableRate)
      myExtractable = new ExtractableConstant(myId, myValue);
    else if (type == Extractable::kExtractableNuisance) {
      if (myValue2 < 0) {
        myExtractable = new ExtractableConstant(myId, myDistribution, myDescription, myValue);
      } else {
        myExtractable = new ExtractableConstant(myId, myDistribution, myDescription, myValue, myValue2);
      }
    }
  } else if (myFunction == "Counter") {
    if (type == Extractable::kExtractableObservation)
      myExtractable = new ExtractableCounter(myChannel, myCounterHisto, myInput1);
    else if (type == Extractable::kExtractableRate)
      myExtractable = new ExtractableCounter(myId, myCounterHisto, myInput1);
    else if (type == Extractable::kExtractableNuisance)
      myExtractable = new ExtractableCounter(myId, myDistribution, myDescription, myCounterHisto, myInput1);
  } else if (myFunction == "maxCounter") {
    if (type == Extractable::kExtractableNuisance)
      myExtractable = new ExtractableMaxCounter(myId, myDistribution, myDescription, myFiles, myInput1);
    else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m function 'maxCounter' is only available for nuisance!" << std::endl;
      return false;
    }
  } else if (myFunction == "Ratio") {
    if (type == Extractable::kExtractableNuisance)
      myExtractable = new ExtractableRatio(myId, myDistribution, myDescription, myCounterHisto, myInput1, myInput2, myValue);
    else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m function 'Ratio' is only available for nuisance!" << std::endl;
      return false;
    }
  } else if (myFunction == "ScaleFactor") {
    if (type == Extractable::kExtractableNuisance)
      myExtractable = new ExtractableScaleFactor(myId, myDistribution, myDescription, myCounterHisto, myInput1, myInput2);
    else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m function 'ScaleFactor' is only available for nuisance!" << std::endl;
      return false;
    }
  }
  if (myExtractable)
    vExtractables.push_back(myExtractable);
  // Create dataset group for observation (for rate and nuisance they are created via addDataGroup)
  if (type == Extractable::kExtractableObservation) {
    DatasetGroup* myDataGroup = new DatasetGroup(myChannel, -1, "Data", true, myMTPlot, "");
    if (!myDataGroup->addDatasets(myFilePath, myFiles, fNormalisationInfo))
      return false;
    vDatasetGroups.push_back(myDataGroup);
    myDataGroup->addExtractable(myExtractable);
  }
  return true;
}

bool ConfigManager::addDataGroup ( std::string str ) {
  size_t myPos = 0;
  std::vector<double> myMasses;
  std::vector<std::string> myFiles;
  std::vector<std::string> myNuisances;
  double myChannel = -1;
  double myProcess = -10;
  std::string myLabel;
  std::string myLabelItem = "default";
  std::string myRate;
  std::string myFilePath;
  std::string myMTPlot = "";
  std::string myMTFile = "";
  // Obtain items
  while (myPos < str.size() && myLabelItem != "") {
    //std::cout << "pos=" << myPos << ", str=" << str.substr(myPos) << std::endl;
    // Get label
    myLabelItem = parseLabel(str, myPos);
    if (myPos > str.size() || myLabelItem == "") continue;
    // Check label
    if (myLabelItem == "process") {
      myProcess = parseNumber(str, myPos);
    } else if (myLabelItem == "channel") {
      myChannel = parseNumber(str, myPos);
    } else if (myLabelItem == "mass") {
      parseVectorValue(str, myPos, myMasses);
    } else if (myLabelItem == "label") {
      myLabel = parseString(str, myPos);
    } else if (myLabelItem == "rate") {
      myRate = parseString(str, myPos);
    } else if (myLabelItem == "nuisances") {
      parseVectorString(str, myPos, myNuisances);
    } else if (myLabelItem == "filePath") {
      myFilePath = parseString(str, myPos);
    } else if (myLabelItem == "files") {
      parseVectorString(str, myPos, myFiles);
    } else if (myLabelItem == "mTPlot") {
      myMTPlot = parseString(str, myPos);
    } else if (myLabelItem == "mTFile") {
      myMTFile = parseString(str, myPos);
    } else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m unknown label in config: '" << myLabelItem << "'!" << std::endl;
      std::cout << "  Parsed string: " << str << std::endl;
      return false;
    }
  }
  // Check that all parameters were supplied and create extractable object

  // Check required fields
  bool myStatus = true;
  if (myProcess <= -10) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'process' for column!" << std::endl;
    myStatus = false;
  } else if (myChannel <= 0) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'channel' for column!" << std::endl;
    myStatus = false;
  } else if (!myMasses.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'mass' for column!" << std::endl;
    myStatus = false;
  } else if (!myLabel.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'label' for column!" << std::endl;
    myStatus = false;
  } else if (!myRate.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'rate' for column!" << std::endl;
    myStatus = false;
  } else if (!myMTPlot.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing field 'mTPlot' for column!" << std::endl;
    myStatus = false;
  }
  // No check on parameters nuisance or files since they are optional
  
  if (!myStatus) {
    std::cout << "  line in config: " << str << std::endl << std::endl;
    std::cout << "Example of correct syntax:" << std::endl;
    std::cout << "column = { channel=1, process=1, mass={100}, label=" << '"' 
              <<  "name" << '"' <<  ", rate=" << '"' << "IdOfRate" << "'"
              << "[, nuisances={" << '"' << "IdOfNuisance1" << '"' << ", " << '"' << "IdOfNuisance2"
              << '"' << " ... }] [filePath=" << '"' << "path" << '"' << ",] [, files={" 
              << '"' << "file1.root" << '"' << ", " << '"' << "file2.root"
              << '"' << " ... }] } mTPlot = " << '"' << "plotwithpath" << '"'
              << ", [ mTFile = " << '"' << "file.root" << '"'            
              << "]" << std::endl;
    return false;
  }
  // Create dataset group
  DatasetGroup* myDataGroup = new DatasetGroup(myChannel, myProcess, myLabel, myMasses, myMTPlot, myMTFile);
  if (!myDataGroup->addDatasets(myFilePath, myFiles, fNormalisationInfo))
    return false;
  // Register extractables
  if (!registerExtractable(myDataGroup, myRate)) return false;
  for (std::vector<std::string>::iterator it = myNuisances.begin(); it != myNuisances.end(); ++it) {
    if (!registerExtractable(myDataGroup, *it)) return false;
  }
  vDatasetGroups.push_back(myDataGroup);

  return true;
}

bool ConfigManager::registerExtractable(DatasetGroup* group, std::string id) {
  for (std::vector<Extractable*>::iterator it = vExtractables.begin(); it != vExtractables.end(); ++it) {
    if ((*it)->getId() == id) {
      group->addExtractable(*it);
      return true;
    }
  }
  // No extractable found
  std::cout << "\033[0;41m\033[1;37mError:\033[0;0m rate or nuisance with id '" << id << "' not found!" << std::endl;
  return false;
}

bool ConfigManager::addMergingOfExtractable(std::string str) {
  std::string toId;
  std::string fromId;
  // Find strings in command string
  size_t myPos = 0;
  std::string myLabelItem = "default";
  bool myStatus = true;
  while (myPos < str.size() && myLabelItem != "") {
    //std::cout << "pos=" << myPos << ", str=" << str.substr(myPos) << std::endl;
    // Get label
    myLabelItem = parseLabel(str, myPos);
    if (myPos > str.size() || myLabelItem == "") continue;
    // Check label
    if (myLabelItem == "id") {
      toId = parseString(str, myPos);
    } else if (myLabelItem == "id2") {
      fromId = parseString(str, myPos);
    } else {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m unknown item for command mergeNuisances!" << std::endl;
      myStatus = false;
    }
  }
  // Check that all necessary parameters were supplied
  if (!toId.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing item id for command mergeNuisances!" << std::endl;
    myStatus = false;
  }
  if (!fromId.size()) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m missing item id2 for command mergeNuisances!" << std::endl;
    myStatus = false;
  }
  if (!myStatus) {
    std::cout << "Usage: mergeNuisances= { id=" << '"' << "1" << '"' << ", id2=" << '"' << "1b" << '"' << " }" << std::endl;
    return false;
  }

  // Loop over extractables to find pointers
  Extractable* myToObject = 0;
  Extractable* myFromObject = 0;
  std::vector<Extractable*>::iterator itFrom;
  for (std::vector<Extractable*>::iterator it = vExtractables.begin(); it != vExtractables.end(); ++it) {
    if ((*it)->getId() == toId)
      myToObject = *it;
    else if ((*it)->getId() == fromId) {
      itFrom = it;
      myFromObject = *it;
    }
  }
  if (!myToObject) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m merging / could not find nuisance id: " << toId << std::endl;
    return false;
  }
  if (!myFromObject) {
    std::cout << "\033[0;41m\033[1;37mError:\033[0;0m merging / could not find nuisance id: " << fromId << std::endl;
    return false;
  }
  myToObject->addExtractableToBeMerged(myFromObject);
  //vExtractables.erase(itFrom);
  myFromObject->setIsMerged(toId);
  return true;
}

bool ConfigManager::doExtract() {
  // FIXME is this method needed?

  return true;
}

void ConfigManager::generateCards() {
  // Loop over mass points
  /*for (size_t i = 0; i < vDatacardGenerators.size(); ++i) {
    vDatacardGenerators[i]->generateDataCard(sDescription, fLuminosity, 
                                             sShapeSource, false,
                                             vExtractables, vDatasetGroups,
                                             fNormalisationInfo);
  }*/
  //  Generate datacards with shapes
  if (sShapeSource.size()) {
    for (size_t i = 0; i < vDatacardGenerators.size(); ++i) {
      vDatacardGenerators[i]->generateDataCard(sDescription, fLuminosity,
                                              sShapeSource, true,
                                              vExtractables, vDatasetGroups,
                                               fNormalisationInfo);
    }
  }
}
