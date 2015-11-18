#include "catch.hpp"
#include "test_createTree.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/GenericScaleFactor.h"
#include "boost/property_tree/json_parser.hpp"



TEST_CASE("GenericScaleFactor", "[Framework]") {
  SECTION("Config validity") {
    std::string tmp = "{\n";
    tmp += "  \"settings1\": {\n"; // nominal
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9]\n";
    tmp += "  },\n";
    tmp += "  \"settings1up\": {\n"; // up
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.15,1.23,0.99]\n";
    tmp += "  },\n";
    tmp += "  \"settings1down\": {\n"; // down
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [0.98,0.6,0.82]\n";
    tmp += "  },\n";
    tmp += "  \"settings2\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0,80.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9]\n";
    tmp += "  },\n";
    tmp += "  \"settings3\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2]\n";
    tmp += "  }\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    REQUIRE_NOTHROW( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("settings1")) );
    REQUIRE_NOTHROW( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("settings1up")) );
    REQUIRE_NOTHROW( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("settings1down")) );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("settings2")), hplus::Exception );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("settings3")), hplus::Exception );
  }
   
  std::string tmp = "{\n";
  tmp += "  \"settings1\": {\n"; // nominal
  tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
  tmp += "    \"scaleFactors\": [1.1,1.2,0.9]\n";
  tmp += "  },\n";
  tmp += "  \"settings1up\": {\n"; // up
  tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
  tmp += "    \"scaleFactors\": [1.15,1.23,0.99]\n";
  tmp += "  },\n";
  tmp += "  \"settings1down\": {\n"; // down
  tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
  tmp += "    \"scaleFactors\": [0.98,0.6,0.82]\n";
  tmp += "  }\n";
  tmp += "}\n";
  ParameterSet pset(tmp, true);

  SECTION("Getters for no pset") {
    REQUIRE_NOTHROW( GenericScaleFactor(pset.getParameterOptional<ParameterSet>("dummy")) );
    GenericScaleFactor sf(pset.getParameterOptional<ParameterSet>("dummy"));
    CHECK( sf.getScaleFactorValue(10.0) == 1.0f );
  }
  
  SECTION("Getters for nominal values") {
    GenericScaleFactor sf(pset.getParameterOptional<ParameterSet>("settings1"));
    CHECK( sf.getScaleFactorValue(-10.0) == 1.1f );
    CHECK( sf.getScaleFactorValue(21.0) == 1.1f );
    CHECK( sf.getScaleFactorValue(40.0) == 1.2f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.9f );
    CHECK( sf.getScaleFactorValue(980.0) == 0.9f );
  }
  
  SECTION("Getters for up variation") {
    GenericScaleFactor sf(pset.getParameterOptional<ParameterSet>("settings1up"));
    CHECK( sf.getScaleFactorValue(21.0) == 1.15f );
    CHECK( sf.getScaleFactorValue(40.0) == 1.23f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.99f );
  }
  SECTION("Getters for up variation") {
    GenericScaleFactor sf(pset.getParameterOptional<ParameterSet>("settings1down"));
    CHECK( sf.getScaleFactorValue(21.0) == 0.98f );
    CHECK( sf.getScaleFactorValue(40.0) == 0.6f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.82f );
  }
}
