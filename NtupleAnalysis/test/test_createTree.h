#ifndef test_createTree_h
#define test_createTree_h

#include "TTree.h"

#include <memory>
#include <string>

std::unique_ptr<TTree> createEmptyTree();

std::unique_ptr<TTree> createSimpleTree();

std::unique_ptr<TTree> createRealisticTree(const std::string& tauPrefix="Taus");

#endif
