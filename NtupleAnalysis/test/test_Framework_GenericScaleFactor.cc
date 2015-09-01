#include "catch.hpp"
#include "test_createTree.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/GenericScaleFactor.h"
#include "boost/property_tree/json_parser.hpp"



TEST_CASE("GenericScaleFactor", "[Framework]") {
  SECTION("Config validity") {
    std::string tmp = "{\n";
    tmp += "  \"settings1\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9],\n";
    tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99],\n";
    tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6,0.82]\n";
    tmp += "  },\n";
    tmp += "  \"settings2\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0,80.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9],\n";
    tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99],\n";
    tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6,0.82]\n";
    tmp += "  },\n";
    tmp += "  \"settings3\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2],\n";
    tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99],\n";
    tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6,0.82]\n";
    tmp += "  },\n";
    tmp += "  \"settings4\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9],\n";
    tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99,1.20],\n";
    tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6,0.82]\n";
    tmp += "  },\n";
    tmp += "  \"settings5\": {\n";
    tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
    tmp += "    \"scaleFactors\": [1.1,1.2,0.9],\n";
    tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99],\n";
    tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6]\n";
    tmp += "  }\n";
    tmp += "}\n";
    ParameterSet pset(tmp, true);
    REQUIRE_NOTHROW( GenericScaleFactor(pset.getParameter<ParameterSet>("settings1")) );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameter<ParameterSet>("settings2")), hplus::Exception );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameter<ParameterSet>("settings3")), hplus::Exception );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameter<ParameterSet>("settings4")), hplus::Exception );
    REQUIRE_THROWS_AS( GenericScaleFactor(pset.getParameter<ParameterSet>("settings5")), hplus::Exception );
  }
   
  std::string tmp = "{\n";
  tmp += "  \"settings1\": {\n";
  tmp += "    \"binLeftEdges\": [40.0,60.0],\n";
  tmp += "    \"scaleFactors\": [1.1,1.2,0.9],\n";
  tmp += "    \"scaleFactorsUpVariation\": [1.15,1.23,0.99],\n";
  tmp += "    \"scaleFactorsDownVariation\": [0.98,0.6,0.82]\n";
  tmp += "  }\n";
  tmp += "}\n";
  ParameterSet pset(tmp, true);

  SECTION("Getters for nominal values") {
    GenericScaleFactor sf(pset.getParameter<ParameterSet>("settings1"));
    CHECK( sf.getScaleFactorValue(-10.0) == 1.1f );
    CHECK( sf.getScaleFactorValue(21.0) == 1.1f );
    CHECK( sf.getScaleFactorValue(40.0) == 1.2f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.9f );
    CHECK( sf.getScaleFactorValue(980.0) == 0.9f );
  }
  
  SECTION("Getters for up variation") {
    GenericScaleFactor sf(pset.getParameter<ParameterSet>("settings1"));
    REQUIRE_THROWS_AS( sf.setVariation("Dummy"), hplus::Exception );
    REQUIRE_NOTHROW( sf.setVariation("JESUp") );
    REQUIRE_NOTHROW( sf.setVariation("JESup") );
    sf.setVariation("JESUp");
    CHECK( sf.getScaleFactorValue(21.0) == 1.15f );
    CHECK( sf.getScaleFactorValue(40.0) == 1.23f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.99f );
  }
  SECTION("Getters for up variation") {
    GenericScaleFactor sf(pset.getParameter<ParameterSet>("settings1"));
    REQUIRE_NOTHROW( sf.setVariation("JESDown") );
    REQUIRE_NOTHROW( sf.setVariation("JESdown") );
    sf.setVariation("JESDown");
    CHECK( sf.getScaleFactorValue(21.0) == 0.98f );
    CHECK( sf.getScaleFactorValue(40.0) == 0.6f );
    CHECK( sf.getScaleFactorValue(80.0) == 0.82f );
  }
}
