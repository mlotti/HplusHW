// -*- c++ -*-
#ifndef Framework_ParameterSet_h
#define Framework_ParameterSet_h

#include "boost/property_tree/ptree.hpp"
#include "boost/optional.hpp"

#include <type_traits>

// Partial specializations at the end
namespace ParameterSetImpl {
  template <typename T>
  struct ParameterGetter {
    // For simple types, just perfect-forward the possible default parameter
    template <typename ...Args>
    static
    T get(const boost::property_tree::ptree& config, const std::string& name, Args&&... args) {
      return config.get<T>(name, std::forward<Args>(args)...);
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
  ParameterSet(const std::string& config, bool isMC);

  explicit ParameterSet(const boost::property_tree::ptree& config);
  ParameterSet(const boost::property_tree::ptree& config, bool isMC);

  template <typename T, typename ...Args>
  T getParameter(const std::string& name, Args&&... args) const {
    return ParameterSetImpl::ParameterGetter<T>::get(fConfig, name, std::forward<Args>(args)...);
  }

  template <typename T>
  boost::optional<T> getParameterOptional(const std::string& name) const {
    return ParameterSetImpl::ParameterGetter<T>::getOptional(fConfig, name);
  }

  bool isMC() const;

private:
  template <typename T, typename PChild>
  std::vector<T> toVector(const PChild& child) {
    std::vector<T> res;
    for(const auto& item: child) {
      res.push_back(item.second.data());
    }
    return res;
  }

  boost::property_tree::ptree fConfig;
  bool fIsMC;
  bool fIsMCSet;
};


// Partial specializations
namespace ParameterSetImpl {
  // Partial specialization for vector<T>
  template <typename T>
  struct ParameterGetter<std::vector<T> > {
  private:
    template <typename Child>
    static
    std::vector<T> to_vector(const Child& child) {
      std::vector<T> res;
      for(const auto& item: child) {
        res.push_back(ParameterGetter<T>::get(item.second, ""));
      }
    return res;
    }
  public:

    static
    std::vector<T> get(const boost::property_tree::ptree& config, const std::string& name) {
      return to_vector(config.get_child(name));
    }

    // For vector, provide an overload for the default
    static
    std::vector<T> get(const boost::property_tree::ptree& config, const std::string& name, const std::vector<T>& defaultValue) {
      boost::optional<const boost::property_tree::ptree&> child = config.get_child_optional(name);
      if(child)
        return to_vector(*child);

      return defaultValue;
    }

    static
    boost::optional<std::vector<T> > getOptional(const boost::property_tree::ptree& config, const std::string& name) {
      boost::optional<std::vector<T>> res;
      boost::optional<const boost::property_tree::ptree&> child = config.get_child_optional(name);
      if(child) {
        res = to_vector(*child);
      }
      return res;
    }
  };

  //Partial specialization for ParameterSet
  template <>
  struct ParameterGetter<ParameterSet> {
    static
    ParameterSet get(const boost::property_tree::ptree& config, const std::string& name) {
      return ParameterSet(config.get_child(name));
    };

    // For ParameterSet, provide an overload for the default
    static
    ParameterSet get(const boost::property_tree::ptree& config, const std::string& name, const ParameterSet& defaultValue) {
      boost::optional<const boost::property_tree::ptree&> child = config.get_child_optional(name);
      if(child)
        return ParameterSet(*child);
      return defaultValue;
    };

    static
    boost::optional<ParameterSet> getOptional(const boost::property_tree::ptree& config, const std::string& name) {
      boost::optional<ParameterSet> res;

      boost::optional<const boost::property_tree::ptree&> child = config.get_child_optional(name);
      if(child) {
        res = ParameterSet(*child);
      }

      return res;
    }
  };
}

#endif
