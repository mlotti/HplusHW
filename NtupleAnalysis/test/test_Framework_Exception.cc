#include "catch.hpp"

#include "Framework/interface/Exception.h"

#include <iostream>

TEST_CASE("Exception", "[Framework]") {
  SECTION("Exception throwing") {
  throw hplus::Exception("LogicError") << "Test exception";

}
