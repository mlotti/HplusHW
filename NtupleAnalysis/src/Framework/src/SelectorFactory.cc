#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/BaseSelector.h"

#include <sstream>
#include "TH1.h"

namespace SelectorFactory {
  std::unique_ptr<BaseSelector> create(const std::string& className, const std::string& config, bool isMC, const TH1* skimCounters) {
    ParameterSet pset(config, isMC);
    std::unique_ptr<BaseSelector> ret(impl::getGlobalRegistry()->get(className)->create(pset, skimCounters));
    return ret;
  }
}
