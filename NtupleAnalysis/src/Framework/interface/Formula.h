// -*- c++ -*-
#ifndef Framework_Formula_h
#define Framework_Formula_h

#include "Framework/interface/FormulaManager.h"

#include <string>

class Formula {
public:
  Formula() {}

  double value() const {
    return fManager->value(fIndex);
  }

private:
  Formula(const FormulaManager *manager, size_t index):
    fManager(manager), fIndex(index)
  {}

  friend FormulaManager;

  const FormulaManager *fManager;
  size_t fIndex;
};

#endif
