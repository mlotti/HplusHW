// -*- c++ -*-
#ifndef DataFormat_GenWeight_h
#define DataFormat_GenWeight_h

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

class GenWeightBase {
public:
  explicit GenWeightBase(const std::string& prefix);
  ~GenWeightBase();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  GenWeightBase(const GenWeightBase&) = delete;
  GenWeightBase(GenWeightBase&&) = delete;
  GenWeightBase& operator=(const GenWeightBase&) = delete;
  GenWeightBase& operator=(GenWeightBase&&) = delete;

protected:
  const std::string& prefix() const { return fPrefix; }

private:
  std::string fPrefix;
};

template <typename NUMBER>
class GenWeight_T: public GenWeightBase {
public:
  using float_type = NUMBER;
  using Polar2DVector = math::Polar2DVectorT<float_type>;
  using XYVector = math::XYVectorT<float_type>;
  using Scalar = float_type;

  explicit GenWeight_T(const std::string& prefix):
    GenWeightBase(prefix),
    fGenWeight(nullptr)
  {}
  ~GenWeight_T() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix(), &fGenWeight);
  }

  float_type weight() const { return fGenWeight->value(); }

private:
  const Branch<float_type> *fGenWeight;
};

using GenWeight = GenWeight_T<double>;

#endif
