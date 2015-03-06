// -*- c++ -*-
#ifndef Framework_FormulaManager_h
#define Framework_FormulaManager_h

//#include "Framework/interface/Formula.h"

#include "TTreeFormula.h"

#include <vector>
#include <string>
#include <unordered_map>
#include <memory>

class Formula;

class TTree;

class FormulaManager {
public:
  FormulaManager();
  ~FormulaManager();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  FormulaManager(const FormulaManager&) = delete;
  FormulaManager(FormulaManager&&) = delete;
  FormulaManager& operator=(const FormulaManager&) = delete;
  FormulaManager& operator=(FormulaManager&&) = delete;

  void setupBranch(TTree *tree);
  void updateLeaves();

  Formula book(const std::string& expression);

private:
  struct FormulaImpl {
    explicit FormulaImpl(const std::string& expression):
      fExpression(expression) {}
    std::string fExpression;
    std::unique_ptr<TTreeFormula> fFormula;
  };

  double value(size_t index) const {
    return fFormulas[index].fFormula->EvalInstance();
  };

  friend Formula;

  std::vector<FormulaImpl> fFormulas;
  std::unordered_map<std::string, size_t> fExpressionIndexMap;
};

#endif

