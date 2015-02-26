#include "Framework/interface/BranchBase.h"

#include <stdexcept>
#include <iostream>

BranchBase::~BranchBase() {}

namespace {
  bool exactlyOneVector(const std::string& a, const std::string b) {
    int c = 0;
    c += (a.find("vector<") != std::string::npos);
    c += (b.find("vector<") != std::string::npos);
    return c == 1;
  }
  bool exactlyOneVectorBool(const std::string& a, const std::string b) {
    int c = 0;
    c += (a.find("vector<bool>") != std::string::npos);
    c += (b.find("vector<bool>") != std::string::npos);
    return c == 1;
  }
}
bool BranchBase::isBranchTypeOk(const std::string& actualType, bool print) const {
  // Let's take the approach that by default the actual branch type
  // can be converted to asked type, but in some cases not (we get
  // segfault). We won't have that many different types (hopefully!)
  // in the ntuples anyway.

  const std::string& askedType = getTypeName();

  bool ok = true;
  if(exactlyOneVector(askedType, actualType)) {
    ok = false;
  }
  if(exactlyOneVectorBool(askedType, actualType)) {
    ok = false;
  }

  if(!ok) {
    if(print) std::cout << "WARNING: Asked branch " << getName() << " with type " << askedType << ", while in the TTree the branch has an incompatible type " << actualType << ". The branch will be ignored." << std::endl;
    return false;
  }

  return true;
}


void BranchBase::assertValid() const {
  if(!isValid())
    throw std::runtime_error("Tried to access branch "+name+" but doesn't exist in the TTree");
}
