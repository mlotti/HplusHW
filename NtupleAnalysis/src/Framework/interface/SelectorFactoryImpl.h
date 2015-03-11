// -*- c++ -*-
#ifndef Framework_SelectorFactoryImpl_h
#define Framework_SelectorFactoryImpl_h

#include "Framework/interface/ParameterSet.h"

#include <unordered_map>
#include <string>
#include <memory>

class BaseSelector;

namespace SelectorFactory {
  namespace impl {
    class CreatorBase {
    public:
      CreatorBase();
      virtual ~CreatorBase();

      virtual BaseSelector *create(const ParameterSet& config) const = 0;
    };

    template <typename T>
    class Creator: public CreatorBase {
    public:
      Creator() {};
      virtual ~Creator() {};

      virtual BaseSelector *create(const ParameterSet& config) const override {
        return new T(config);
      };
    };


    class Registry {
    public:
      Registry();
      ~Registry();

      void add(const std::string& name, std::unique_ptr<CreatorBase> creator);
      const CreatorBase *get(const std::string& name);

    private:
      std::unordered_map<std::string, std::unique_ptr<CreatorBase> > fRegistry;
    };

    Registry *getGlobalRegistry();

    template <typename T>
    class Registrar {
    public:
      Registrar(const std::string& name) {
        getGlobalRegistry()->add(name, std::unique_ptr<CreatorBase>(new Creator<T>()));
      }
    };
  }
}

#endif
