#include "catch.hpp"

#include "Framework/interface/SelectorFactory.h"
#include "Framework/interface/BaseSelector.h"

namespace {
  class SelectorTestSelectorFactory: public BaseSelector {
  public:
    SelectorTestSelectorFactory(const ParameterSet& config):
      BaseSelector(config),
      name(config.getParameter<std::string>("name")),
      intvalue(config.getParameter<int>("intvalue")),
      floatvalue(config.getParameter<float>("floatvalue")),
      nested_intvalue(config.getParameter<int>("nested.intvalue"))
    {}
    virtual ~SelectorTestSelectorFactory() {}

    virtual void book(TDirectory *dir) override {}
    virtual void setupBranches(BranchManager& branchManager) override {}
    virtual void process(Long64_t entry) override {}

    std::string name;
    int intvalue;
    float floatvalue;
    int nested_intvalue;
  };
}

REGISTER_SELECTOR(SelectorTestSelectorFactory);

TEST_CASE("Selector factory and semi-automatic registration", "[Framework]") {
  auto selector = SelectorFactory::create("SelectorTestSelectorFactory", "{\"name\":\"foo\", \"intvalue\":42, \"floatvalue\":2.71, \"nested\":{\"intvalue\":-100}}");
  REQUIRE( selector.get() != nullptr );
  const SelectorTestSelectorFactory *s = dynamic_cast<SelectorTestSelectorFactory *>(selector.get());
  REQUIRE( s != nullptr );
  CHECK( s->name == "foo" );
  CHECK( s->intvalue == 42 );
  CHECK( s->floatvalue == 2.71f );
  CHECK( s->nested_intvalue == -100 );
}
