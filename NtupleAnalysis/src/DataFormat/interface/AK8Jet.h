// -*- c++ -*-
#ifndef DataFormat_AK8Jet_h
#define DataFormat_AK8Jet_h

#include "DataFormat/interface/AK8JetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class AK8Jet;

class AK8JetCollection: public AK8JetGeneratedCollection, public ParticleIteratorAdaptor<AK8JetCollection> {
public:
  using value_type = AK8Jet;

  AK8JetCollection() { initialize(); }
  AK8JetCollection(const std::string& prefix): AK8JetGeneratedCollection(prefix) { initialize(); }
  ~AK8JetCollection() {}

  //Discriminators
  void setJetIDDiscriminator(const std::string& name);
  void setJetPUIDDiscriminator(const std::string& name);
  void setBJetDiscriminator(const std::string& name);
  bool jetIDDiscriminatorIsValid() const { return bValidityOfJetIDDiscr; }
  bool jetPUIDDiscriminatorIsValid() const { return bValidityOfJetPUIDDiscr; }
  bool bjetDiscriminatorIsValid() const { return bValidityOfBJetDiscr; }

  void setupBranches(BranchManager& mgr);

  AK8Jet operator[](size_t i) const;
  std::vector<AK8Jet> toVector() const;
    

  friend class AK8Jet;
  friend class AK8JetGenerated<AK8JetCollection>;
  friend class Particle<AK8JetCollection>;

protected:
  const Branch<std::vector<bool>>* fJetIDDiscriminator;
  const Branch<std::vector<bool>>* fJetPUIDDiscriminator;
  const Branch<std::vector<float>>* fBJetDiscriminator;
  
private:
  /// Initialize data members
  void initialize();
  
  std::string fJetIDDiscriminatorName;
  std::string fJetPUIDDiscriminatorName;
  std::string fBJetDiscriminatorName;
  bool bValidityOfJetIDDiscr;
  bool bValidityOfJetPUIDDiscr;
  bool bValidityOfBJetDiscr;
};

class AK8Jet: public AK8JetGenerated<AK8JetCollection> {
public:
  AK8Jet() {}
  AK8Jet(const AK8JetCollection* coll, size_t index): AK8JetGenerated(coll, index) {}
  ~AK8Jet() {}
  
  bool jetIDDiscriminator() const {
    if (!fCollection->jetIDDiscriminatorIsValid())
      return true;
    return fCollection->fJetIDDiscriminator->value()[index()];
  }
  bool jetPUIDDiscriminator() const {
    if (!fCollection->jetPUIDDiscriminatorIsValid())
      return true;
    return fCollection->fJetPUIDDiscriminator->value()[index()];
  }
  float bjetDiscriminator() const {
    if (!fCollection->bjetDiscriminatorIsValid())
      return 1.0;
    return fCollection->fBJetDiscriminator->value()[index()];
  }
  
  /// Operator defined for using std::sort on vector<AK8Jet>
  bool operator<(const AK8Jet& jet) const {
    // Descending order by jet pT
    return (this->pt() > jet.pt());
  }
};

inline
AK8Jet AK8JetCollection::operator[](size_t i) const {
  return AK8Jet(this, i);
}

inline
std::vector<AK8Jet> AK8JetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
