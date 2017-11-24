#include "Framework/interface/ParameterSet.h"

#include "boost/property_tree/json_parser.hpp"

#include <sstream>
#include "Framework/interface/Exception.h"

ParameterSet::ParameterSet(const std::string& config):
  fIsMC(false),
  fIsMCSet(false),
  fIsSilent(true)
{
  std::stringstream ss(config);
  boost::property_tree::read_json(ss, fConfig);
}

ParameterSet::ParameterSet(const std::string& config, bool isMC, bool silent):
  fIsMC(isMC),
  fIsMCSet(true),
  fIsSilent(silent)
{
  std::stringstream ss(config);
  boost::property_tree::read_json(ss, fConfig);
}

ParameterSet::ParameterSet(const boost::property_tree::ptree& config):
  fConfig(config),
  fIsMC(false),
  fIsMCSet(false),
  fIsSilent(true)
{}

ParameterSet::ParameterSet(const boost::property_tree::ptree& config, bool isMC, bool silent):
  fConfig(config),
  fIsMC(isMC),
  fIsMCSet(true),
  fIsSilent(silent)
{}

bool ParameterSet::isMC() const {
  if(!fIsMCSet) {
    throw hplus::Exception("Runtime") << "MC status has not been set for this ParameterSet";
  }
  return fIsMC;
}

bool ParameterSet::exists(const std::string& name) const {
  boost::optional<const boost::property_tree::ptree&> child = fConfig.get_child_optional(name);
  if(!child) return false;
  return true;
}
