#ifndef test_createTree_h
#define test_createTree_h

#include "TTree.h"
#include "TFile.h"
#include "TDirectory.h"

#include "boost/property_tree/ptree.hpp"

#include <memory>
#include <string>
#include <cmath>
#include <cstdlib>



std::unique_ptr<TTree> createEmptyTree();

std::unique_ptr<TTree> createSimpleTree();

std::unique_ptr<TTree> createRealisticTree(const std::string& tauPrefix="Taus");

boost::property_tree::ptree getMinimalConfig();

TDirectory* getDirectory(std::string name);

void closeDirectory(TDirectory* d);

#endif
