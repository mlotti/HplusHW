#include "DataFormat/interface/Tau.h"

#include "Framework/interface/BranchManager.h"

void TauCollection::initialize() {
  fAgainstElectronDiscriminatorName = "";
  fAgainstMuonDiscriminatorName = "";
  fIsolationDiscriminatorName = "";
  bValidityOfAgainstElectronDiscr = false;
  bValidityOfAgainstMuonDiscr = false;
  bValidityOfIsolationDiscr = false;
}

void TauCollection::setAgainstElectronDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfAgainstElectronDiscr = true;
  checkDiscriminatorNameValidity(name, this->getAgainstElectronDiscriminatorNames());
  fAgainstElectronDiscriminatorName = name;
}

void TauCollection::setAgainstMuonDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfAgainstMuonDiscr = true;
  checkDiscriminatorNameValidity(name, this->getAgainstMuonDiscriminatorNames());
  fAgainstMuonDiscriminatorName = name;
}

void TauCollection::setIsolationDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfIsolationDiscr = true;
  //Debug
//  std::cout << name << "\n";
  //
  checkDiscriminatorNameValidity(name, this->getIsolationDiscriminatorNames());
  fIsolationDiscriminatorName = name;
}

bool TauCollection::againstElectronDiscriminatorIsValid() const {
  return bValidityOfAgainstElectronDiscr;
}
bool TauCollection::againstMuonDiscriminatorIsValid() const {
  return bValidityOfAgainstMuonDiscr;
}
bool TauCollection::isolationDiscriminatorIsValid() const {
  return bValidityOfIsolationDiscr;
}

void TauCollection::setupBranches(BranchManager& mgr) {
  TauGeneratedCollection::setupBranches(mgr);

  fConfigurableDiscriminators.resize(fConfigurableDiscriminatorNames.size());
  std::vector<std::string> allDiscrs;
  for (const auto& name: this->getAgainstElectronDiscriminatorNames())
    allDiscrs.push_back(name);
  for (const auto& name: this->getAgainstMuonDiscriminatorNames())
    allDiscrs.push_back(name);
  for (const auto& name: this->getIsolationDiscriminatorNames())
    allDiscrs.push_back(name);
  size_t i=0;
  for (const auto& name: fConfigurableDiscriminatorNames) {
    checkDiscriminatorNameValidity(name, allDiscrs);
    mgr.book(prefix()+"_"+name, &(fConfigurableDiscriminators[i]));
    ++i;
  }
  if (againstElectronDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fAgainstElectronDiscriminatorName, &fAgainstElectronDiscriminator);
  if (againstMuonDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fAgainstMuonDiscriminatorName, &fAgainstMuonDiscriminator);
  if (isolationDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fIsolationDiscriminatorName, &fIsolationDiscriminator);
}
