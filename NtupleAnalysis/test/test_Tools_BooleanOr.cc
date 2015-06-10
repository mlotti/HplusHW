#include "catch.hpp"

#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"
#include "Tools/interface/BooleanOr.h"
#include "Framework/interface/Exception.h"

TEST_CASE("BooleanOr", "[Tools]") {
  std::unique_ptr<TTree> tree = createRealisticTree();

  BranchManager mgr;
  mgr.setTree(tree.get());

  BooleanOr test;

  SECTION("Empty") {
    mgr.setEntry(0);
    REQUIRE_THROWS_AS( test.value(), hplus::Exception);
    //REQUIRE_THROWS_AS( test.value(), std::runtime_error );
  }

  SECTION("One branch") {
    test.setBranchNames(std::vector<std::string>{"HLT_Trig2"});
    test.setupBranches(mgr);

    mgr.setEntry(0);
    CHECK( test.value() == true );

    mgr.setEntry(1);
    CHECK( test.value() == false );

    mgr.setEntry(2);
    CHECK( test.value() == false );
  }

  SECTION("Many branches") {
    test.setBranchNames(std::vector<std::string>{"HLT_Trig1", "HLT_Trig2", "HLT_Trig3"});
    test.setupBranches(mgr);

    mgr.setEntry(0);
    CHECK( test.value() == true );

    mgr.setEntry(1);
    CHECK( test.value() == true );

    mgr.setEntry(2);
    CHECK( test.value() == false );
  }

  SECTION("Non-existent branch") {
    test.setBranchNames(std::vector<std::string>{"HLT_Dummy"});
    test.setupBranches(mgr);

    mgr.setEntry(0);
    REQUIRE_THROWS_AS( test.value(), hplus::Exception );
  }

  SECTION("Non-existent branch among existing branches") {
    test.setBranchNames(std::vector<std::string>{"HLT_Trig1", "HLT_Dummy", "HLT_Trig3"});
    test.setupBranches(mgr);

    mgr.setEntry(0);
    CHECK( test.value() == true );

    mgr.setEntry(1);
    CHECK( test.value() == true );

    mgr.setEntry(2);
    CHECK( test.value() == false );
  }

}
