// -*- c++ -*-
#ifndef DataFormat_MET_h
#define DataFormat_MET_h

#include "Framework/interface/Branch.h"
#include "Framework/interface/BranchManager.h"

#include "Math/Vector2D.h"

class BranchManager;

namespace math {
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

class METBase {
public:
  explicit METBase(const std::string& prefix);
  ~METBase();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  METBase(const METBase&) = delete;
  METBase(METBase&&) = delete;
  METBase& operator=(const METBase&) = delete;
  METBase& operator=(METBase&&) = delete;

  void setEnergySystematicsVariation(const std::string& scenario);

protected:
  const std::string& prefix() const { return fPrefix; }
  const std::string& energySystematicsVariation() const { return fEnergySystematicsVariation; }

private:
  std::string fPrefix;
  std::string fEnergySystematicsVariation;
};

template <typename NUMBER>
class MET_T: public METBase {
public:
  using float_type = NUMBER;
  using Polar2DVector = math::Polar2DVectorT<float_type>;
  using XYVector = math::XYVectorT<float_type>;

  explicit MET_T(const std::string& prefix):
    METBase(prefix),
    fEt(nullptr),
    fPhi(nullptr)
  {}
  ~MET_T() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix()+"_et" +energySystematicsVariation(), &fEt);
    mgr.book(prefix()+"_phi"+energySystematicsVariation(), &fPhi);
  }

  float_type et() const { return fEt->value(); }
  float_type phi() const { return fPhi->value(); }

  // Note: asking for polarP2 is more expensive than asking et/phi
  // separately, so call only when necessary
  Polar2DVector polarP2() const {
    return Polar2DVector(et(), phi());
  }

  // Note: asking for cartesian p2 is even more expensive because of
  // the coordinate change
  XYVector p2() const {
    return XYVector(polarP2());
  }

private:
  Branch<float_type> *fEt;
  Branch<float_type> *fPhi;
};

using MET = MET_T<double>;

#endif
