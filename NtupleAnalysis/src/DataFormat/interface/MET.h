// -*- c++ -*-
#ifndef DataFormat_MET_h
#define DataFormat_MET_h

#include "Framework/interface/Branch.h"
#include "Framework/interface/BranchManager.h"
#include "DataFormat/interface/Particle.h"

class BranchManager;

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
  using XYVector = math::XYVectorT<float_type>;
  using Scalar = float_type;

  explicit MET_T(const std::string& prefix):
    METBase(prefix),
    fX(nullptr),
    fY(nullptr)
  {}
  ~MET_T() {}

  void setupBranches(BranchManager& mgr) {
    mgr.book(prefix()+"_x"+energySystematicsVariation(), &fX);
    mgr.book(prefix()+"_y"+energySystematicsVariation(), &fY);
  }

  float_type x() const { return fX->value(); }
  float_type y() const { return fY->value(); }
  float_type et() const { return p2().R(); }
  float_type Phi() const { return p2().Phi(); }
  float_type phi() const { return p2().Phi(); }

  XYVector p2() const {
    return XYVector(x(), y());
  }

private:
  const Branch<float_type> *fX;
  const Branch<float_type> *fY;
};

using MET = MET_T<double>;

#endif
