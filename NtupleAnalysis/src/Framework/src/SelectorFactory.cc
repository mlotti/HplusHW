#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/BaseSelector.h"

#include <sstream>

namespace SelectorFactory {
  std::unique_ptr<BaseSelector> create(const std::string& className, const std::string& config) {
    ParameterSet pset(config);
    std::unique_ptr<BaseSelector> ret(impl::getGlobalRegistry()->get(className)->create(pset));
    return ret;
  }
}
