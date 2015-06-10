// -*- c++ -*-
#ifndef DataFormat_Jet_h
#define DataFormat_Jet_h

#include "DataFormat/interface/JetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Jet;

class JetCollection: public JetGeneratedCollection, public ParticleIteratorAdaptor<JetCollection> {
public:
  using value_type = Jet;

  JetCollection() { initialize(); }
  JetCollection(const std::string& prefix): JetGeneratedCollection(prefix) { initialize(); }
  ~JetCollection() {}

  //Discriminators
  void setJetIDDiscriminator(const std::string& name);
  void setJetPUIDDiscriminator(const std::string& name);
  void setBJetDiscriminator(const std::string& name);
  bool jetIDDiscriminatorIsValid() const { return bValidityOfJetIDDiscr; }
  bool jetPUIDDiscriminatorIsValid() const { return bValidityOfJetPUIDDiscr; }
  bool bjetDiscriminatorIsValid() const { return bValidityOfBJetDiscr; }
  
  void setupBranches(BranchManager& mgr);

  Jet operator[](size_t i) const;
  std::vector<Jet> toVector() const;
    

  friend class Jet;
  friend class JetGenerated<JetCollection>;
  friend class Particle<JetCollection>;

protected:
  const Branch<std::vector<bool>>* fJetIDDiscriminator;
  const Branch<std::vector<bool>>* fJetPUIDDiscriminator;
  const Branch<std::vector<bool>>* fBJetDiscriminator;
  
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

class Jet: public JetGenerated<JetCollection> {
public:
  Jet() {}
  Jet(const JetCollection* coll, size_t index): JetGenerated(coll, index) {}
  ~Jet() {}
  
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
  bool bjetDiscriminator() const {
    if (!fCollection->bjetDiscriminatorIsValid())
      return true;
    return fCollection->fBJetDiscriminator->value()[index()];
  }
  
  /// Operator defined for using std::sort on vector<Jet>
  bool operator<(const Jet& jet) const {
    // Descending order by tau pT
    return (this->pt() > jet.pt());
  }
};

inline
Jet JetCollection::operator[](size_t i) const {
  return Jet(this, i);
}

inline
std::vector<Jet> JetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
