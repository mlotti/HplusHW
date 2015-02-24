#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/BaseSelector.h"

#include "boost/property_tree/json_parser.hpp"

#include <sstream>

namespace SelectorFactory {
  std::unique_ptr<BaseSelector> create(const std::string& className, const std::string& config) {
    boost::property_tree::ptree tree;
    std::stringstream ss(config);
    boost::property_tree::read_json(ss, tree);
    std::unique_ptr<BaseSelector> ret(impl::getGlobalRegistry()->get(className)->create(tree));
    return ret;
  }
}
