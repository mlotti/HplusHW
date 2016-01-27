// -*- c++ -*-
#ifndef Framework_SelectorFactory_h
#define Framework_SelectorFactory_h

#include "Framework/interface/SelectorFactoryImpl.h"

#include <string>
#include <memory>

class BaseSelector;
class TH1;

namespace SelectorFactory {
  std::unique_ptr<BaseSelector> create(const std::string& className, const std::string& config, bool isMC, const TH1* skimCounters=nullptr);
}

#define REGISTER_SELECTOR(name) static SelectorFactory::impl::Registrar<name> reg_##name(#name);

#endif
