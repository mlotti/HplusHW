// -*- c++ -*-
#ifndef DataFormat_Particle_h
#define DataFormat_Particle_h

#include "Framework/interface/Branch.h"
#include "Framework/interface/BranchManager.h"


#include "Math/LorentzVector.h"
#include "Math/PtEtaPhiE4D.h"
#include "Math/DisplacementVector3D.h"

#include <vector>
#include <limits>

class BranchManager;

// Inspired by CMSSW DataFormats/Math/interface/LorentzVector.h
namespace math {
  template <typename T>
  using XYZTLorentzVectorT = ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<T>>;

  using XYZTLorentzVectorF = XYZTLorentzVectorT<float>;
  using XYZTLorentzVectorD = XYZTLorentzVectorT<double>;
  using XYZTLorentzVector = XYZTLorentzVectorF;


  template <typename T>
  using PtEtaPhiELorentzVectorT = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiE4D<T>>;

  using PtEtaPhiELorentzVectorF = PtEtaPhiELorentzVectorT<float>;
  using PtEtaPhiELorentzVectorD = PtEtaPhiELorentzVectorT<double>;
  using PtEtaPhiELorentzVector = PtEtaPhiELorentzVectorF;

  template <typename T>
  using LorentzVectorT = XYZTLorentzVectorT<T>;
  template <typename T>
  using PolarLorentzVectorT = PtEtaPhiELorentzVectorT<T>;

  using LorentzVector = XYZTLorentzVector;
  using PolarLorentzVector = PtEtaPhiELorentzVector;


  template <typename T>
  using XYZVectorT = ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<T>>;

  using XYZVectorF = XYZVectorT<float>;
  using XYZVectorD = XYZVectorT<double>;
  using XYZVector = XYZVectorF;
}

// The intention of ParticleCollection and Particle is not to be
// usable as such, but to abstract certain commonalities of the
// specific particle types
class ParticleBase {
public:
  ParticleBase(): fIndex(std::numeric_limits<size_t>::max()) {}
  explicit ParticleBase(size_t index): fIndex(index) {}
  ~ParticleBase();

  size_t index() const { return fIndex; }

private:
  size_t fIndex;
};

////////////////////////////////////////

template <typename Coll>
class Particle: public ParticleBase {
public:
  using float_type = typename Coll::float_type;
  using PolarLorentzVector = typename math::PolarLorentzVectorT<float_type>;
  using LorentzVector = typename math::LorentzVectorT<float_type>;

  Particle(): ParticleBase(), fCollection(nullptr) {}
  Particle(const Coll *coll, size_t index): ParticleBase(index), fCollection(coll) {}
  ~Particle() {}

  bool isValid() const { return fCollection != nullptr; }

  float_type pt()  const { return fCollection->fPt->value()[index()]; }
  float_type eta() const { return fCollection->fEta->value()[index()]; }
  float_type phi() const { return fCollection->fPhi->value()[index()]; }
  float_type e()   const { return fCollection->fE->value()[index()]; }

  // Note: asking for polarP4 is more expensive than asking any of
  // pt/eta/phi/e, so call this only when necessary
  PolarLorentzVector polarP4() const {
    return PolarLorentzVector(pt(), eta(), phi(), e());
  }
  // Note: asking for cartesian p4 is even more expensive because of
  // the coordinate change
  LorentzVector p4() const {
    return LorentzVector(polarP4());
  }

protected:
  const Coll *fCollection;
};

////////////////////////////////////////

class ParticleCollectionBase {
public:
  explicit ParticleCollectionBase(const std::string& prefix);
  ~ParticleCollectionBase();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  ParticleCollectionBase(const ParticleCollectionBase&) = delete;
  ParticleCollectionBase(ParticleCollectionBase&&) = delete;
  ParticleCollectionBase& operator=(const ParticleCollectionBase&) = delete;
  ParticleCollectionBase& operator=(ParticleCollectionBase&&) = delete;

  void setEnergySystematicsVariation(const std::string& scenario);

protected:
  const std::string& prefix() const { return fPrefix; }
  const std::string& energySystematicsVariation() const { return fEnergySystematicsVariation; }

  template <typename Coll>
  static
  std::vector<typename Coll::value_type> toVector(Coll& coll) {
    using ValueType = typename Coll::value_type;
    std::vector<ValueType> ret;
    ret.reserve(coll.size());
    for(ValueType item: coll) {
      ret.push_back(item);
    }
    return ret;
  }

private:
  std::string fPrefix;
  std::string fEnergySystematicsVariation;
};

template <typename NUMBER>
class ParticleCollection: public ParticleCollectionBase {
public:
  using float_type = NUMBER;

  explicit ParticleCollection(const std::string& prefix):
    ParticleCollectionBase(prefix),
    fPt(nullptr),
    fEta(nullptr),
    fPhi(nullptr),
    fE(nullptr)
  {}
  ~ParticleCollection() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix()+"_pt"  +energySystematicsVariation(), &fPt);
    mgr.book(prefix()+"_eta",                               &fEta);
    mgr.book(prefix()+"_phi",                               &fPhi);
    mgr.book(prefix()+"_e"   +energySystematicsVariation(), &fE);
  }

  size_t size() const { return fPt->value().size(); }

  Particle<ParticleCollection> operator[](size_t i) const {
    return Particle<ParticleCollection>(this, i);
  }

  friend class Particle<ParticleCollection>;

protected:
  Branch<std::vector<float_type>> *fPt;
  Branch<std::vector<float_type>> *fEta;
  Branch<std::vector<float_type>> *fPhi;
  Branch<std::vector<float_type>> *fE;
};

#endif
