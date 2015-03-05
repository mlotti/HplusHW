// -*- c++ -*-
#ifndef DataFormat_Muon_h
#define DataFormat_Muon_h

#include "DataFormat/interface/MuonGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Muon;

class MuonCollection: public MuonGeneratedCollection, public ParticleIteratorAdaptor<MuonCollection> {
public:
  using value_type = Muon;

  MuonCollection() {}
  MuonCollection(const std::string& prefix): MuonGeneratedCollection(prefix) {}
  ~MuonCollection() {}

  void setupBranches(BranchManager& mgr);

  Muon operator[](size_t i);
  std::vector<Muon> toVector();

  friend class Muon;
  friend class MuonGenerated<MuonCollection>;
  friend class Particle<MuonCollection>;

protected:
};

class Muon: public MuonGenerated<MuonCollection> {
public:
  Muon() {}
  Muon(MuonCollection* coll, size_t index): MuonGenerated(coll, index) {}
  ~Muon() {}
};

inline
Muon MuonCollection::operator[](size_t i) {
  return Muon(this, i);
}

inline
std::vector<Muon> MuonCollection::toVector() {
  return ParticleCollectionBase::toVector(*this);
}

#endif
