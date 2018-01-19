#include "DataFormat/interface/AK8JetsSoftDrop.h"

#include "Framework/interface/BranchManager.h"

void AK8JetsSoftDropCollection::initialize() {
  fJetIDDiscriminatorName = "";
  fJetPUIDDiscriminatorName = "";
  fBJetDiscriminatorName = "";
  bValidityOfJetIDDiscr = false;
  bValidityOfJetPUIDDiscr = false;
  bValidityOfBJetDiscr = false;
}

void AK8JetsSoftDropCollection::setJetIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getJetIDDiscriminatorNames());
  fJetIDDiscriminatorName = name;
}

void AK8JetsSoftDropCollection::setJetPUIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfJetPUIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getPUIDDiscriminatorNames());
  fJetPUIDDiscriminatorName = name;
}

void AK8JetsSoftDropCollection::setBJetDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfBJetDiscr = true;
  checkDiscriminatorNameValidity(name, this->getBJetTagsDiscriminatorNames());
  fBJetDiscriminatorName = name;
}

void AK8JetsSoftDropCollection::setupBranches(BranchManager& mgr) {
  AK8JetsSoftDropGeneratedCollection::setupBranches(mgr);
  
  if (jetIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetIDDiscriminatorName, &fJetIDDiscriminator);
  if (jetPUIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetPUIDDiscriminatorName, &fJetPUIDDiscriminator);
  if (bjetDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fBJetDiscriminatorName, &fBJetDiscriminator);
}
