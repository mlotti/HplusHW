#include "Framework/interface/BranchManager.h"

#include <stdexcept>

BranchManager::BranchManager(): fTree(0) {}
BranchManager::~BranchManager() {}

void BranchManager::throwTypeMismatch(const std::string& name, const std::string& oldType, const std::string& newType) const {
  throw std::runtime_error("Trying to book branch "+name+" with a type '"+newType+"', but it is already booked with a different type '"+oldType+"'");
}
