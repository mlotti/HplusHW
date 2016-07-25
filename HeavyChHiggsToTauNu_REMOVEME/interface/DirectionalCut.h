// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_DirectionalCut_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_DirectionalCut_h

#include <string>

namespace HPlus {
  class DirectionalCut {
    enum DirectionalCutType {
      kGT,  // greater than
      kGEQ, // greater than or equal to
      kLT,  // less than
      kLEQ, // less than or equal to
      kEQ,  // equal to
      kNEQ  // not equal to
    };
  public:
    DirectionalCut(size_t value, std::string direction);
    DirectionalCut(unsigned int value, std::string direction);
    DirectionalCut(double value, std::string direction);
    ~DirectionalCut();

    bool passedCut(size_t testValue) const;
    bool passedCut(unsigned int testValue) const;
    bool passedCut(double testValue) const;

  private:
    void initialise(std::string direction);
    double fValue;
    DirectionalCutType fCutDirection;
  };
}

#endif
