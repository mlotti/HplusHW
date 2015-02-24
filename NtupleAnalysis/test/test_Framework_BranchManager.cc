#include "catch.hpp"
#include "test_createTree.h"

#include "Framework/interface/BranchManager.h"

TEST_CASE("BranchManager works", "[Framework]") {
  std::unique_ptr<TTree> tree = createSimpleTree();

  BranchManager mgr;
  mgr.setTree(tree.get());

  SECTION("Single branches") {
    Branch<int> *b_event = nullptr;
    Branch<unsigned int> *b_lumi = nullptr;
    Branch<unsigned long long> *b_run = nullptr;
    Branch<std::vector<int> > *b_num1 = nullptr;

    mgr.book("event", &b_event);
    REQUIRE( b_event != nullptr );
    mgr.book("lumi", &b_lumi);
    REQUIRE( b_lumi != nullptr );
    mgr.book("run", &b_run);
    REQUIRE( b_run != nullptr );
    mgr.book("num1", &b_num1);
    REQUIRE( b_num1 != nullptr );

    REQUIRE( b_event->isValid() );
    REQUIRE( b_lumi->isValid() );
    REQUIRE( b_run->isValid() );
    REQUIRE( b_num1->isValid() );

    mgr.setEntry(0);
    CHECK( b_event->value() == 1 );
    CHECK( b_lumi->value() == 2 );
    CHECK( b_run->value() == 3u );
    REQUIRE( b_num1->value().size() == 3 );
    CHECK( b_num1->value()[0] == 1 );
    CHECK( b_num1->value()[1] == 2 );
    CHECK( b_num1->value()[2] == 3 );

    mgr.setEntry(2);
    CHECK( b_event->value() == 3 );
    REQUIRE( b_num1->value().size() == 5 );
    CHECK( b_num1->value()[0] == -10 );
    CHECK( b_num1->value()[1] == 0 );
    CHECK( b_num1->value()[2] == 10 );
    CHECK( b_num1->value()[3] == 100 );
    CHECK( b_num1->value()[4] == 1000 );
  }
  SECTION("Multiple branches") {
    Branch<int> *b_event1 = nullptr;
    Branch<int> *b_event2 = nullptr;

    mgr.book("event", &b_event1);
    REQUIRE( b_event1 != nullptr );
    mgr.book("event", &b_event2);
    REQUIRE( b_event2 != nullptr );

    mgr.setEntry(0);
    CHECK( b_event1->value() == 1 );
    CHECK( b_event2->value() == 1 );

    mgr.setEntry(2);
    CHECK( b_event1->value() == 3 );
    CHECK( b_event2->value() == 3 );

    mgr.setEntry(1);
    CHECK( b_event1->value() == 2 );
    CHECK( b_event2->value() == 2 );
  }

  SECTION("Incorrect type throws exception") {
    Branch<int> *event1 = nullptr;
    Branch<unsigned long long> *event2 = nullptr;

    mgr.book("event", &event1);
    REQUIRE( event1 != nullptr );
    REQUIRE_THROWS_AS( mgr.book("event", &event2), std::runtime_error );
  }
}
