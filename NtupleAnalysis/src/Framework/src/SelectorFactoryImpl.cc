#include "Framework/interface/SelectorFactoryImpl.h"

#include <stdexcept>

namespace SelectorFactory {
  namespace impl {
    CreatorBase::CreatorBase() {}
    CreatorBase::~CreatorBase() {}

    Registry::Registry() {}
    Registry::~Registry() {}

    void Registry::add(const std::string& name, std::unique_ptr<CreatorBase> creator) {
      auto found = fRegistry.find(name);
      if(found != fRegistry.end()) {
        throw std::logic_error("Selector "+name+" is already registered");
      }
      fRegistry.emplace(name, std::move(creator));
    }

    const CreatorBase *Registry::get(const std::string& name) {
      auto found = fRegistry.find(name);
      if(found == fRegistry.end()) {
        throw std::logic_error("Selector "+name+" is not registered");
      }
      return found->second.get();
    }

    Registry *getGlobalRegistry() {
      static Registry reg;
      return &reg;
    }
  };
}
