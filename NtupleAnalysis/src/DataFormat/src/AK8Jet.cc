#include "DataFormat/interface/AK8Jet.h"

#include "Framework/interface/BranchManager.h"

void AK8JetCollection::initialize() {
  fJetIDDiscriminatorName = "";
  fJetPUIDDiscriminatorName = "";
  fBJetDiscriminatorName = "";
  bValidityOfJetIDDiscr = false;
  bValidityOfJetPUIDDiscr = false;
  bValidityOfBJetDiscr = false;
}

void AK8JetCollection::setJetIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getJetIDDiscriminatorNames());
  fJetIDDiscriminatorName = name;
}

void AK8JetCollection::setJetPUIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetPUIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getPUIDDiscriminatorNames());
  fJetPUIDDiscriminatorName = name;
}

void AK8JetCollection::setBJetDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfBJetDiscr = true;
  checkDiscriminatorNameValidity(name, this->getBJetTagsDiscriminatorNames());
  fBJetDiscriminatorName = name;
}

void AK8JetCollection::setupBranches(BranchManager& mgr) {
  AK8JetGeneratedCollection::setupBranches(mgr);
  
  if (jetIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetIDDiscriminatorName, &fJetIDDiscriminator);
  if (jetPUIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetPUIDDiscriminatorName, &fJetPUIDDiscriminator);
  if (bjetDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fBJetDiscriminatorName, &fBJetDiscriminator);
}
