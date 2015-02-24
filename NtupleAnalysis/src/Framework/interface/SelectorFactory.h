// -*- c++ -*-
#ifndef Framework_SelectorFactory_h
#define Framework_SelectorFactory_h

#include "Framework/interface/SelectorFactoryImpl.h"

#include <string>
#include <memory>

class BaseSelector;

namespace SelectorFactory {
  std::unique_ptr<BaseSelector> create(const std::string& className, const std::string& config);
}

#define REGISTER_SELECTOR(name) static SelectorFactory::impl::Registrar<name> reg_##name(#name);

#endif
