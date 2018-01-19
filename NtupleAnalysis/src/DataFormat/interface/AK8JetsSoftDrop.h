// -*- c++ -*-
#ifndef DataFormat_AK8JetsSoftDrop_h
#define DataFormat_AK8JetsSoftDrop_h

#include "DataFormat/interface/AK8JetsSoftDropGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class AK8JetsSoftDrop;

class AK8JetsSoftDropCollection: public AK8JetsSoftDropGeneratedCollection, public ParticleIteratorAdaptor<AK8JetsSoftDropCollection> {
public:
  using value_type = AK8JetsSoftDrop;

  AK8JetsSoftDropCollection() { initialize(); }
  AK8JetsSoftDropCollection(const std::string& prefix): AK8JetsSoftDropGeneratedCollection(prefix) { initialize(); }
  ~AK8JetsSoftDropCollection() {}
  
  //Discriminators
  void setJetIDDiscriminator(const std::string& name);
  void setJetPUIDDiscriminator(const std::string& name);
  void setBJetDiscriminator(const std::string& name);
  bool jetIDDiscriminatorIsValid() const { return bValidityOfJetIDDiscr; }
  bool jetPUIDDiscriminatorIsValid() const { return bValidityOfJetPUIDDiscr; }
  bool bjetDiscriminatorIsValid() const { return bValidityOfBJetDiscr; }

  void setupBranches(BranchManager& mgr);

  AK8JetsSoftDrop operator[](size_t i) const;
  std::vector<AK8JetsSoftDrop> toVector() const;
    

  friend class AK8JetsSoftDrop;
  friend class AK8JetsSoftDropGenerated<AK8JetsSoftDropCollection>;
  friend class Particle<AK8JetsSoftDropCollection>;

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

class AK8JetsSoftDrop: public AK8JetsSoftDropGenerated<AK8JetsSoftDropCollection> {
public:
  AK8JetsSoftDrop() {}
  AK8JetsSoftDrop(const AK8JetsSoftDropCollection* coll, size_t index): AK8JetsSoftDropGenerated(coll, index) {}
  ~AK8JetsSoftDrop() {}
  
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
  bool operator<(const AK8JetsSoftDrop& jet) const {
    // Descending order by jet pT
    return (this->pt() > jet.pt());
  }
};

inline
AK8JetsSoftDrop AK8JetsSoftDropCollection::operator[](size_t i) const {
  return AK8JetsSoftDrop(this, i);
}

inline
std::vector<AK8JetsSoftDrop> AK8JetsSoftDropCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
