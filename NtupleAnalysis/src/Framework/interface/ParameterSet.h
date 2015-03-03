// -*- c++ -*-
#ifndef Framework_ParameterSet_h
#define Framework_ParameterSet_h

#include "boost/property_tree/ptree.hpp"
#include "boost/optional.hpp"

#include <type_traits>

class ParameterSet {
public:
  explicit ParameterSet(const boost::property_tree::ptree& config);

  template <typename T>
  T getParameter(const std::string& name) const {
    return fConfig.get<T>(name);
  }

  template <typename T>
  boost::optional<T> getParameterOptional(const std::string& name) const {
    return fConfig.get_optional<T>(name);
  }

private:
  boost::property_tree::ptree fConfig;
};

#endif
