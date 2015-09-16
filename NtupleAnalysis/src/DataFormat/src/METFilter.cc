#include "DataFormat/interface/METFilter.h"

#include "Framework/interface/Exception.h"

void METFilter::setupBranches(BranchManager& mgr) {
  METFilterGenerated::setupBranches(mgr);
}

void METFilter::checkDiscriminatorValidity(const std::string& name) const {
  std::string outList;
  for (auto p: this->getDiscriminatorNames()) {
    if (name == p) return;
    if (outList.size() > 0)
      outList += ", ";
    outList += "'"+p+"'";
  }
  // If this fragment is reached, the requested discriminator name was not found
  throw hplus::Exception("config") << "METFilter: The requested discriminator '" << name << "' is not valid! Available options are: " << outList;
}

void METFilter::checkDiscriminatorValidity(const std::vector<std::string>& names) const {
  for (auto p: names) {
    this->checkDiscriminatorValidity(p);
  }
}
