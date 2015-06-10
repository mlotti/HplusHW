#include "Framework/interface/ParameterSet.h"

#include "boost/property_tree/json_parser.hpp"

#include <sstream>
#include "Framework/interface/Exception.h"

ParameterSet::ParameterSet(const std::string& config):
  fIsMC(false),
  fIsMCSet(false)
{
  std::stringstream ss(config);
  boost::property_tree::read_json(ss, fConfig);
}

ParameterSet::ParameterSet(const std::string& config, bool isMC):
  fIsMC(isMC),
  fIsMCSet(true)
{
  std::stringstream ss(config);
  boost::property_tree::read_json(ss, fConfig);
}

ParameterSet::ParameterSet(const boost::property_tree::ptree& config):
  fConfig(config),
  fIsMC(false),
  fIsMCSet(false)
{}

ParameterSet::ParameterSet(const boost::property_tree::ptree& config, bool isMC):
  fConfig(config),
  fIsMC(isMC),
  fIsMCSet(true)
{}

bool ParameterSet::isMC() const {
  if(!fIsMCSet) {
    throw hplus::Exception("Runtime") << "MC status has not been set for this ParameterSet";
  }
  return fIsMC;
}
