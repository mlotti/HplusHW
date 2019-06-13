// -*- c++ -*-
#ifndef DataFormat_HLTElectron_h
#define DataFormat_HLTElectron_h

#include "DataFormat/interface/HLTElectronGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTElectron;

class HLTElectronCollection: public HLTElectronGeneratedCollection, public ParticleIteratorAdaptor<HLTElectronCollection> {
    public:
    using value_type = HLTElectron;
    
    HLTElectronCollection() {}
    explicit HLTElectronCollection(const std::string& prefix): HLTElectronGeneratedCollection(prefix) {}
    ~HLTElectronCollection() {}
    
    void setupBranches(BranchManager& mgr);
    
    HLTElectron operator[](size_t i) const;
    std::vector<HLTElectron> toVector() const;
    
    friend class HLTElectron;
    friend class HLTElectronGenerated<HLTElectronCollection>;
    friend class Particle<HLTElectronCollection>;
    
    protected:
    
    private:
    
};

class HLTElectron: public HLTElectronGenerated<HLTElectronCollection> {
    public:
    HLTElectron() {}
    HLTElectron(const HLTElectronCollection* coll, size_t index): HLTElectronGenerated(coll, index) {}
    ~HLTElectron() {}
    
};

inline
HLTElectron HLTElectronCollection::operator[](size_t i) const {
    return HLTElectron(this, i);
}

inline
std::vector<HLTElectron> HLTElectronCollection::toVector() const {
    return ParticleCollectionBase::toVector(*this);
}

#endif
