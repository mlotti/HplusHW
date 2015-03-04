#include "Framework/interface/ParameterSet.h"

#include "boost/property_tree/json_parser.hpp"

#include <sstream>

ParameterSet::ParameterSet(const std::string& config)
{
  std::stringstream ss(config);
  boost::property_tree::read_json(ss, fConfig);
}

ParameterSet::ParameterSet(const boost::property_tree::ptree& config):
  fConfig(config)
{}

