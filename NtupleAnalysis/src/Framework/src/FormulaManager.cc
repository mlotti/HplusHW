#include "Framework/interface/FormulaManager.h"
#include "Framework/interface/Formula.h"

#include "TTree.h"

#include <algorithm>
#include <stdexcept>

FormulaManager::FormulaManager() {}
FormulaManager::~FormulaManager() {}

void FormulaManager::setupBranch(TTree *tree) {
  for(FormulaImpl& impl: fFormulas) {
    impl.fFormula.reset(new TTreeFormula(impl.fExpression.c_str(), impl.fExpression.c_str(), tree));
    // we don't modify the formula after the construction, so we can benefit from quick load
    //impl.fFormula->SetQuickLoad(kTRUE);
  }
}

void FormulaManager::updateLeaves() {
  for(FormulaImpl& impl: fFormulas) {
    impl.fFormula->UpdateFormulaLeaves();
  }
}

Formula FormulaManager::book(const std::string& expression) {
  auto found = std::find_if(fFormulas.begin(), fFormulas.end(), [&](const FormulaImpl& a) {
      return a.fExpression == expression;
    });
  if(found != fFormulas.end()) {
    return Formula(this, found-fFormulas.begin());
  }
  fFormulas.emplace_back(expression);
  return Formula(this, fFormulas.size()-1);
}

void FormulaManager::assertValid(size_t index) const {
  if(fFormulas[index].fFormula->GetNcodes() == 0)
    throw std::runtime_error("The formula "+fFormulas[index].fExpression+" does not depend on any branch in the TTree");
}
