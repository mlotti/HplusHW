#include "catch.hpp"

#include "Framework/interface/EventWeight.h"

TEST_CASE("EventWeight works", "[Framework]") {
  EventWeight weight;

  SECTION("Initialization") {
    REQUIRE( weight.getWeight() == 1.0 );
  }

  SECTION("Set weight") {
    weight.multiplyWeight(0.5);
    REQUIRE( weight.getWeight() == 0.5 );
    weight.multiplyWeight(4.0);
    REQUIRE( weight.getWeight() == 2.0 );
    weight.beginEvent();
    REQUIRE( weight.getWeight() == 1.0 );
  }
}
