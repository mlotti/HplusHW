#include "Framework/interface/BranchManager.h"

#include <stdexcept>

BranchManager::BranchManager(): fTree(0) {}
BranchManager::~BranchManager() {}

void BranchManager::throwTypeMismatch(const std::string& name, const char *oldType, const char *newType) const {
  throw std::runtime_error("Trying to book branch "+name+" with a type '"+newType+"', but it is already booked with a different type '"+oldType+"'");
}
