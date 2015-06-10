#include "DataFormat/interface/Jet.h"

#include "Framework/interface/BranchManager.h"

void JetCollection::initialize() {
  fJetIDDiscriminatorName = "";
  fJetPUIDDiscriminatorName = "";
  bValidityOfJetIDDiscr = false;
  bValidityOfJetPUIDDiscr = false;
}

void JetCollection::setJetIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getJetIDDiscriminatorNames());
  fJetIDDiscriminatorName = name;
}

void JetCollection::setJetPUIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetPUIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getPUIDDiscriminatorNames());
  fJetPUIDDiscriminatorName = name;
}

void JetCollection::setupBranches(BranchManager& mgr) {
  JetGeneratedCollection::setupBranches(mgr);
  
  mgr.book(prefix()+"_"+fJetIDDiscriminatorName, &fJetIDDiscriminator);
  mgr.book(prefix()+"_"+fJetPUIDDiscriminatorName, &fJetPUIDDiscriminator);
}
