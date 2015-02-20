#include "Framework/interface/BranchBase.h"

#include <stdexcept>

BranchBase::~BranchBase() {}

void BranchBase::assertValid() const {
  if(!isValid())
    throw std::runtime_error("Tried to access branch "+name+" but doesn't exist in the TTree");
}
