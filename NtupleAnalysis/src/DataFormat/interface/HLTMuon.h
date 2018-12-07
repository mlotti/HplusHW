
// -*- c++ -*-
#ifndef DataFormat_HLTMuon_h
#define DataFormat_HLTMuon_h

#include "DataFormat/interface/HLTMuonGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTMuon;

class HLTMuonCollection: public HLTMuonGeneratedCollection, public ParticleIteratorAdaptor<HLTMuonCollection> {
public:
  using value_type = HLTMuon;

  HLTMuonCollection() {}
  explicit HLTMuonCollection(const std::string& prefix): HLTMuonGeneratedCollection(prefix) {}
  ~HLTMuonCollection() {}

  void setupBranches(BranchManager& mgr);

  HLTMuon operator[](size_t i) const;
  std::vector<HLTMuon> toVector() const;

  friend class HLTMuon;
  friend class HLTMuonGenerated<HLTMuonCollection>;
  friend class Particle<HLTMuonCollection>;

protected:

private:

};

class HLTMuon: public HLTMuonGenerated<HLTMuonCollection> {
public:
  HLTMuon() {}
  HLTMuon(const HLTMuonCollection* coll, size_t index): HLTMuonGenerated(coll, index) {}
  ~HLTMuon() {}
  
};

inline
HLTMuon HLTMuonCollection::operator[](size_t i) const {
  return HLTMuon(this, i);
}

inline
std::vector<HLTMuon> HLTMuonCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif


