// -*- c++ -*-

#ifndef DataFormat_HLTMuonGenerated_h
#define DataFormat_HLTMuonGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTMuonGeneratedCollection: public ParticleCollection<double> {
public:
  explicit HLTMuonGeneratedCollection(const std::string& prefix="HLTMuon"): ParticleCollection(prefix) {}
  ~HLTMuonGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);


protected:

};


template <typename Coll>
class HLTMuonGenerated: public Particle<Coll> {
public:
  HLTMuonGenerated() {}
  HLTMuonGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~HLTMuonGenerated() {}




};

#endif
