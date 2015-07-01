#include "DataFormat/interface/Jet.h"

#include "Framework/interface/BranchManager.h"

void JetCollection::initialize() {
  fJetIDDiscriminatorName = "";
  fJetPUIDDiscriminatorName = "";
  fBJetDiscriminatorName = "";
  bValidityOfJetIDDiscr = false;
  bValidityOfJetPUIDDiscr = false;
  bValidityOfBJetDiscr = false;
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

void JetCollection::setBJetDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfBJetDiscr = true;
  checkDiscriminatorNameValidity(name, this->getBJetTagsDiscriminatorNames());
  fBJetDiscriminatorName = name;
}

void JetCollection::setupBranches(BranchManager& mgr) {
  JetGeneratedCollection::setupBranches(mgr);
  
  if (jetIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetIDDiscriminatorName, &fJetIDDiscriminator);
  if (jetPUIDDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fJetPUIDDiscriminatorName, &fJetPUIDDiscriminator);
  if (bjetDiscriminatorIsValid())
    mgr.book(prefix()+"_"+fBJetDiscriminatorName, &fBJetDiscriminator);

  mgr.book(prefix()+"_pdgId", &fJetPDGId);
}
