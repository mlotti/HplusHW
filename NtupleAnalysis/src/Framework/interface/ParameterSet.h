// -*- c++ -*-
#ifndef Framework_ParameterSet_h
#define Framework_ParameterSet_h

#include "boost/property_tree/ptree.hpp"
#include "boost/optional.hpp"

#include <type_traits>

namespace ParameterSetImpl {
  template <typename T>
  struct ParameterGetter {
    static
    T get(const boost::property_tree::ptree& config, const std::string& name) {
      return config.get<T>(name);
    };

    static
    boost::optional<T> getOptional(const boost::property_tree::ptree& config, const std::string& name) {
      return config.get_optional<T>(name);
    }
  };
}

class ParameterSet {
public:
  explicit ParameterSet(const std::string& config);
  explicit ParameterSet(const boost::property_tree::ptree& config);

  template <typename T>
  T getParameter(const std::string& name) const {
    return ParameterSetImpl::ParameterGetter<T>::get(fConfig, name);
  }

  template <typename T>
  boost::optional<T> getParameterOptional(const std::string& name) const {
    return ParameterSetImpl::ParameterGetter<T>::getOptional(fConfig, name);
  }

private:
  boost::property_tree::ptree fConfig;
};

#endif
