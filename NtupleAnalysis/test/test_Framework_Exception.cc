#include "catch.hpp"

#include "Framework/interface/Exception.h"

#include <iostream>

TEST_CASE("Exception", "[Framework]") {
  SECTION("Exception throwing") {
    REQUIRE_THROWS_AS( throw hplus::Exception("LogicError") << "Test", hplus::Exception );
    try {
      throw hplus::Exception("LogicError") << "Test " << "exception" << 3;
    } catch (const hplus::Exception& ex) {
      CHECK( ex.getMsg() == "Test exception3" );
    }
  }
}
