// -*- c++ -*-
#ifndef DataFormat_Particle_h
#define DataFormat_Particle_h

#include "Framework/interface/Branch.h"
#include "Framework/interface/BranchManager.h"

#include "Math/LorentzVector.h"
#include "Math/PtEtaPhiE4D.h"
#include "Math/DisplacementVector3D.h"
#include "Math/DisplacementVector2D.h"
#include "Math/Vector2D.h"

#include <vector>
#include <string>
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

  template <typename T>
  using XYVectorT = ROOT::Math::DisplacementVector2D<ROOT::Math::Cartesian2D<T>>;

  using XYVectorF = XYVectorT<float>;
  using XYVectorD = XYVectorT<double>;
  using XYVector  = XYVectorF;

  template <typename T>
  using Polar2DVectorT = ROOT::Math::DisplacementVector2D<ROOT::Math::Polar2D<T>>;

  using Polar2DVectorF = Polar2DVectorT<float>;
  using Polar2DVectorD = Polar2DVectorT<double>;
  using Polar2DVector  = Polar2DVectorF;
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
  void setIndex(size_t i ) { fIndex = i; }

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
  using Scalar = float_type;

  Particle(): ParticleBase(), fCollection(nullptr) {}
  Particle(const Coll *coll, size_t index): ParticleBase(index), fCollection(coll) {}
  ~Particle() {}

  bool isValid() const { return fCollection != nullptr; }

  float_type pt()  const { return fCollection->fPt->value()[index()]; }
  float_type eta() const { return fCollection->fEta->value()[index()]; }
  float_type phi() const { return fCollection->fPhi->value()[index()]; }
  float_type e()   const { return fCollection->fE->value()[index()]; }
  short pdgId()  const { return fCollection->fPdgId->value()[index()]; }
  short mother() const { return fCollection->fMother->value()[index()]; }
  short status() const { return fCollection->fStatus->value()[index()]; }
  short charge() const { return fCollection->fCharge->value()[index()]; }
  double vtxX() const { return fCollection->fVtxX->value()[index()]; }
  double vtxY() const { return fCollection->fVtxY->value()[index()]; }
  double vtxZ() const { return fCollection->fVtxZ->value()[index()]; }
  bool fromHardProcessBeforeFSR() const { return fCollection->fFromHardProcessBeforeFSR->value()[index()]; }
  bool fromHardProcessDecayed() const { return fCollection->fFromHardProcessDecayed->value()[index()]; }
  bool fromHardProcessFinalState() const { return fCollection->fFromHardProcessFinalState->value()[index()]; }
  bool isDirectHardProcessTauDecayProductFinalState() const { return fCollection->fIsDirectHardProcessTauDecayProductFinalState->value()[index()]; }
  bool isDirectPromptTauDecayProductFinalState() const { return fCollection->fIsDirectPromptTauDecayProductFinalState->value()[index()]; }
  bool isHardProcess() const { return fCollection->fIsHardProcess->value()[index()]; }
  bool isLastCopy() const { return fCollection->fIsLastCopy->value()[index()]; }
  bool isLastCopyBeforeFSR() const { return fCollection->fIsLastCopyBeforeFSR->value()[index()]; }
  bool isPromptDecayed() const { return fCollection->fIsPromptDecayed->value()[index()]; }
  bool isPromptFinalState() const { return fCollection->fIsPromptFinalState->value()[index()]; }
  bool fromHardProcess() const { return fCollection->fFromHardProcess->value()[index()]; }
  bool isDecayedLeptonHadron() const { return fCollection->fIsDecayedLeptonHadron->value()[index()]; }
  bool isDirectHadronDecayProduct() const { return fCollection->fIsDirectHadronDecayProduct->value()[index()]; }
  bool isDirectHardProcessTauDecayProduct() const { return fCollection->fIsDirectHardProcessTauDecayProduct->value()[index()]; }
  bool isDirectPromptTauDecayProduct() const { return fCollection->fIsDirectPromptTauDecayProduct->value()[index()]; }
  bool isDirectTauDecayProduct() const { return fCollection->fIsDirectTauDecayProduct->value()[index()]; }
  bool isFirstCopy() const { return fCollection->fIsFirstCopy->value()[index()]; }
  bool isHardProcessTauDecayProduct() const { return fCollection->fIsHardProcessTauDecayProduct->value()[index()]; }
  bool isPrompt() const { return fCollection->fIsPrompt->value()[index()]; }
  bool isPromptTauDecayProduct() const { return fCollection->fIsPromptTauDecayProduct->value()[index()]; }
  bool isTauDecayProduct() const { return fCollection->fIsTauDecayProduct->value()[index()]; }

  float_type Phi() const { return phi(); }

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

  // Note: asking for polarP4 is more expensive than asking any of
  // pt/phi, so call this only when necessary
  math::Polar2DVector polarP2() const {
    return math::Polar2DVector(pt(), phi());
  }

  // Note: asking for cartesian p2 is even more expensive because of
  // the coordinate change
  math::XYVector p2() const {
    return math::XYVector(polarP2());
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
  void checkDiscriminatorNameValidity(const std::string& name, const std::vector<std::string>& list) const;
  
protected:  
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
    fE(nullptr),
    fPdgId(nullptr),
    fMother(nullptr),
    fStatus(nullptr),
    fCharge(nullptr),
    fVtxX(nullptr),
    fVtxY(nullptr),
    fVtxZ(nullptr),
    // FIXME: These must be moved (added becaused autogenerate script not fully operation for GenParticles)
    fFromHardProcessBeforeFSR(nullptr),
    fFromHardProcessDecayed(nullptr),
    fFromHardProcessFinalState(nullptr),
    fIsDirectHardProcessTauDecayProductFinalState(nullptr),
    fIsDirectPromptTauDecayProductFinalState(nullptr),
    fIsHardProcess(nullptr),
    fIsLastCopy(nullptr),
    fIsLastCopyBeforeFSR(nullptr),
    fIsPromptDecayed(nullptr),
    fIsPromptFinalState(nullptr),
    fFromHardProcess(nullptr),
    fIsDecayedLeptonHadron(nullptr),
    fIsDirectHadronDecayProduct(nullptr),
    fIsDirectHardProcessTauDecayProduct(nullptr),
    fIsDirectPromptTauDecayProduct(nullptr),
    fIsDirectTauDecayProduct(nullptr),
    fIsFirstCopy(nullptr),
    fIsHardProcessTauDecayProduct(nullptr),
    fIsPrompt(nullptr),
    fIsPromptTauDecayProduct(nullptr),
    fIsTauDecayProduct(nullptr)

  {}
  ~ParticleCollection() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix()+"_pt"  +energySystematicsVariation(), &fPt);
    mgr.book(prefix()+"_eta" +energySystematicsVariation(), &fEta);
    mgr.book(prefix()+"_phi" +energySystematicsVariation(), &fPhi);
    mgr.book(prefix()+"_e"   +energySystematicsVariation(), &fE);
    mgr.book(prefix()+"_pdgId" , &fPdgId);
    mgr.book(prefix()+"_mother", &fMother);
    mgr.book(prefix()+"_status", &fStatus);
    mgr.book(prefix()+"_charge", &fCharge);
    mgr.book(prefix()+"_vtxX"  , &fVtxX);
    mgr.book(prefix()+"_vtxY"  , &fVtxY);
    mgr.book(prefix()+"_vtxZ"  , &fVtxZ);
    // FIXME: These must be moved (added becaused autogenerate script not fully operation for GenParticles)
    mgr.book(prefix()+"_fromHardProcessBeforeFSR"                    , &fFromHardProcessBeforeFSR);
    mgr.book(prefix()+"_fromHardProcessDecayed"                      , &fFromHardProcessDecayed);
    mgr.book(prefix()+"_fromHardProcessFinalState"                   , &fFromHardProcessFinalState);
    mgr.book(prefix()+"_isDirectHardProcessTauDecayProductFinalState", &fIsDirectHardProcessTauDecayProductFinalState);
    mgr.book(prefix()+"_isDirectPromptTauDecayProductFinalState"     , &fIsDirectPromptTauDecayProductFinalState);
    mgr.book(prefix()+"_isHardProcess"                               , &fIsHardProcess); 
    mgr.book(prefix()+"_isLastCopy"                                  , &fIsLastCopy);
    mgr.book(prefix()+"_isLastCopyBeforeFSR"                         , &fIsLastCopyBeforeFSR);
    mgr.book(prefix()+"_isPromptDecayed"                             , &fIsPromptDecayed);
    mgr.book(prefix()+"_isPromptFinalState"                          , &fIsPromptFinalState);
    mgr.book(prefix()+"_fromHardProcess"                             , &fFromHardProcess);
    mgr.book(prefix()+"_isDecayedLeptonHadron"                       , &fIsDecayedLeptonHadron);
    mgr.book(prefix()+"_isDirectHadronDecayProduct"                  , &fIsDirectHadronDecayProduct);
    mgr.book(prefix()+"_isDirectHardProcessTauDecayProduct"          , &fIsDirectHardProcessTauDecayProduct);
    mgr.book(prefix()+"_isDirectPromptTauDecayProduct"               , &fIsDirectPromptTauDecayProduct);
    mgr.book(prefix()+"_isDirectTauDecayProduct"                     , &fIsDirectTauDecayProduct);
    mgr.book(prefix()+"_isFirstCopy"                                 , &fIsFirstCopy);
    mgr.book(prefix()+"_isHardProcessTauDecayProduct"                , &fIsHardProcessTauDecayProduct);
    mgr.book(prefix()+"_isPrompt"                                    , &fIsPrompt);
    mgr.book(prefix()+"_isPromptTauDecayProduct"                     , &fIsPromptTauDecayProduct);
    mgr.book(prefix()+"_isTauDecayProduct"                           , &fIsTauDecayProduct);
  }

  size_t size() const { return fPt->value().size(); }

  Particle<ParticleCollection> operator[](size_t i) const {
    return Particle<ParticleCollection>(this, i);
  }

  friend class Particle<ParticleCollection>;

protected:
  const Branch<std::vector<float_type>> *fPt;
  const Branch<std::vector<float_type>> *fEta;
  const Branch<std::vector<float_type>> *fPhi;
  const Branch<std::vector<float_type>> *fE;
  const Branch<std::vector<short>> *fPdgId;
  const Branch<std::vector<short>> *fMother;
  const Branch<std::vector<short>> *fStatus;
  const Branch<std::vector<short>> *fCharge;
  const Branch<std::vector<double>> *fVtxX;
  const Branch<std::vector<double>> *fVtxY;
  const Branch<std::vector<double>> *fVtxZ;
  // FIXME: These must be moved (added becaused autogenerate script not fully operation for GenParticles)
  const Branch<std::vector<bool>> *fFromHardProcessBeforeFSR;
  const Branch<std::vector<bool>> *fFromHardProcessDecayed;
  const Branch<std::vector<bool>> *fFromHardProcessFinalState;
  const Branch<std::vector<bool>> *fIsDirectHardProcessTauDecayProductFinalState;
  const Branch<std::vector<bool>> *fIsDirectPromptTauDecayProductFinalState;
  const Branch<std::vector<bool>> *fIsHardProcess;
  const Branch<std::vector<bool>> *fIsLastCopy;
  const Branch<std::vector<bool>> *fIsLastCopyBeforeFSR;
  const Branch<std::vector<bool>> *fIsPromptDecayed;
  const Branch<std::vector<bool>> *fIsPromptFinalState;
  const Branch<std::vector<bool>> *fFromHardProcess;
  const Branch<std::vector<bool>> *fIsDecayedLeptonHadron;
  const Branch<std::vector<bool>> *fIsDirectHadronDecayProduct;
  const Branch<std::vector<bool>> *fIsDirectHardProcessTauDecayProduct;
  const Branch<std::vector<bool>> *fIsDirectPromptTauDecayProduct;
  const Branch<std::vector<bool>> *fIsDirectTauDecayProduct;
  const Branch<std::vector<bool>> *fIsFirstCopy;
  const Branch<std::vector<bool>> *fIsHardProcessTauDecayProduct;
  const Branch<std::vector<bool>> *fIsPrompt;
  const Branch<std::vector<bool>> *fIsPromptTauDecayProduct;
  const Branch<std::vector<bool>> *fIsTauDecayProduct;

};

#endif
