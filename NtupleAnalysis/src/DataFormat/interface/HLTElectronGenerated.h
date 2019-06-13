// -*- c++ -*-

#ifndef DataFormat_HLTElectronGenerated_h
#define DataFormat_HLTElectronGenerated_h

#include "DataFormat/interface/Particle.h"

class HLTElectronGeneratedCollection: public ParticleCollection<double> {
    public:
    explicit HLTElectronGeneratedCollection(const std::string& prefix="HLTElectron"): ParticleCollection(prefix) {}
    ~HLTElectronGeneratedCollection() {}
    
    void setupBranches(BranchManager& mgr);
    
    
    protected:
    
};


template <typename Coll>
class HLTElectronGenerated: public Particle<Coll> {
    public:
    HLTElectronGenerated() {}
    HLTElectronGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
    ~HLTElectronGenerated() {}
    
    
    
    
};

#endif
