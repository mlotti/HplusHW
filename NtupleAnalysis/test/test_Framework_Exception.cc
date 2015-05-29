#include "catch.hpp"

#include "Framework/interface/Exception.h"

#include <iostream>

TEST_CASE("Exception works", "[Framework]") {
  try {
    
  }
  
  
  
  std::unique_ptr<TTree> tree = createSimpleTree();

  SECTION("Construction") {
    Branch<int> b_event("event");
    REQUIRE( b_event.isValid() == false );
    REQUIRE( b_event.getName() == "event" );
  }
  SECTION("Simple branch") {
    Branch<int> b_event("event");
    b_event.setupBranch(tree.get());
    REQUIRE( b_event.isValid() );

    b_event.setEntry(0);
    CHECK( b_event.value() == 1 );
    CHECK( b_event.value() == 1 );

    b_event.setEntry(2);
    CHECK( b_event.value() == 3 );

    b_event.setEntry(1);
    CHECK( b_event.value() == 2 );
  }
  SECTION("Boolean branch") {
    Branch<bool> b_trigger("trigger");
    b_trigger.setupBranch(tree.get());
    REQUIRE(b_trigger.isValid());

    b_trigger.setEntry(0);
    CHECK( b_trigger.value() == true );

    b_trigger.setEntry(1);
    CHECK( b_trigger.value() == false );

    b_trigger.setEntry(2);
    CHECK( b_trigger.value() == true );
  }
  SECTION("Complex branches") {
    Branch<std::vector<int> > b_num1("num1");
    Branch<std::vector<float> > b_num2("num2");

    b_num1.setupBranch(tree.get());
    b_num2.setupBranch(tree.get());
    REQUIRE( b_num1.isValid() );
    REQUIRE( b_num2.isValid() );

    SECTION("same entry") {
      b_num1.setEntry(0);
      b_num2.setEntry(0);
      auto num1_0 = b_num1.value();
      auto num2_0 = b_num2.value();
      REQUIRE( num1_0.size() == 3 );
      REQUIRE( num2_0.size() == 3 );
      CHECK( num1_0[0] == 1 );
      CHECK( num1_0[1] == 2 );
      CHECK( num1_0[2] == 3 );
      CHECK( num2_0[0] == 0.1f );
      CHECK( num2_0[1] == 0.2f );
      CHECK( num2_0[2] == 0.3f );
    }

    SECTION("different entry") {
      b_num1.setEntry(1);
      b_num2.setEntry(2);
      auto num1_1 = b_num1.value();
      auto num2_2 = b_num2.value();
      REQUIRE( num1_1.size() == 1 );
      CHECK( num1_1[0] == 4 );
      REQUIRE( num2_2.size() == 3 );
      CHECK( num2_2[0] == -1e10f );
      CHECK( num2_2[1] == -5e5f );
      CHECK( num2_2[2] == 1.f );
    }
  }

  SECTION("Non-existent branch") {
    Branch<int> num3("num3");
    num3.setupBranch(tree.get());
    REQUIRE( !num3.isValid() );

    num3.setEntry(0);
    REQUIRE_THROWS_AS( num3.value(), std::runtime_error );
  }

  // At the moment wrong type just segfaults...
  // Not good but I haven't figured out a way that works
  /*
  SECTION("Incorrect type") {
    Branch<std::vector<int> > num2("num2");
    std::cout << "foo" << std::endl;
    num2.setupBranch(tree.get());
    REQUIRE( num2.isValid() );

    num2.setEntry(0);
    std::cout << num2.value()[0] << std::endl;
  }
  */
}
