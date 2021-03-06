// -*- c++ -*-
#ifndef DataFormat_Muon_h
#define DataFormat_Muon_h

#include "DataFormat/interface/MuonGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Muon;

class MuonCollection: public MuonGeneratedCollection, public ParticleIteratorAdaptor<MuonCollection> {
public:
  using value_type = Muon;

  MuonCollection() { initialize(); }
  explicit MuonCollection(const std::string& prefix): MuonGeneratedCollection(prefix) { initialize(); }
  ~MuonCollection() {}

  void setupBranches(BranchManager& mgr);

  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }
  void setMuonIDDiscriminator(const std::string& name);
  bool muonIDDiscriminatorIsValid() const;

  Muon operator[](size_t i) const;
  std::vector<Muon> toVector() const;

  friend class Muon;
  friend class MuonGenerated<MuonCollection>;
  friend class Particle<MuonCollection>;

protected:
  std::vector<const Branch<std::vector<bool>> *> fConfigurableDiscriminators;
  const Branch<std::vector<bool>>* fMuonIDDiscriminator;

private:
  void initialize();

  std::vector<std::string> fConfigurableDiscriminatorNames;
  
  std::string fMuonIDDiscriminatorName;
  bool bValidityOfMuonIDDiscr;
};

class Muon: public MuonGenerated<MuonCollection> {
public:
  Muon() {}
  Muon(const MuonCollection* coll, size_t index): MuonGenerated(coll, index) {}
  ~Muon() {}

  // Methods for discriminators 
  bool configurableDiscriminators() const {
    for(auto& disc: fCollection->fConfigurableDiscriminators) {
      if(!disc->value()[index()])
        return false;
    }
    return true;
  }  
  bool muonIDDiscriminator() const {
    if (!fCollection->muonIDDiscriminatorIsValid())
      return true;
    return fCollection->fMuonIDDiscriminator->value()[index()];
  }
  /// Operator defined for using std::sort on vector<Tau>
  bool operator<(const Muon& muon) const {
    // Descending order by tau pT
    return (this->pt() > muon.pt());
  }
};

inline
Muon MuonCollection::operator[](size_t i) const {
  return Muon(this, i);
}

inline
std::vector<Muon> MuonCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
