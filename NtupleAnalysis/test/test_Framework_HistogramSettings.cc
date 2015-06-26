#include "catch.hpp"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include "Framework/interface/HistogramSettings.h"


TEST_CASE("HistogramSettings", "[Framework]") {
  SECTION("Missing input") {
    boost::property_tree::ptree tmp;
    tmp.put("missingInput1.axisMin", 0.0);
    tmp.put("missingInput1.axisMax", 1.0);
    tmp.put("missingInput2.nBins", 2);
    tmp.put("missingInput2.axisMax", 1.0);
    tmp.put("missingInput3.nBins", 2);
    tmp.put("missingInput3.axisMin", 0.0);
    ParameterSet pset(tmp, true);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("missingInput1")), hplus::Exception);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("missingInput2")), hplus::Exception);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("missingInput3")), hplus::Exception);
  }
  
  SECTION("Invalid values") {
    boost::property_tree::ptree tmp;
    tmp.put("invalidInput1.nBins", 10);
    tmp.put("invalidInput1.axisMin", 0.0);
    tmp.put("invalidInput1.axisMax", -1.0);
    tmp.put("invalidInput2.nBins", 0);
    tmp.put("invalidInput2.axisMin", 0.0);
    tmp.put("invalidInput2.axisMax", 1.0);
    tmp.put("invalidInput3.nBins", -10);
    tmp.put("invalidInput3.axisMin", 0.0);
    tmp.put("invalidInput3.axisMax", 1.0);
    ParameterSet pset(tmp, true);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("invalidInput1")), hplus::Exception);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("invalidInput2")), hplus::Exception);
    REQUIRE_THROWS_AS( HistogramSettings(pset.getParameter<ParameterSet>("invalidInput3")), hplus::Exception);
  }

  SECTION("Value getters") {
    boost::property_tree::ptree tmp;
    tmp.put("input1.nBins", 12);
    tmp.put("input1.axisMin", 20.4);
    tmp.put("input1.axisMax", 54.2);
    ParameterSet pset(tmp, true);
    REQUIRE_NOTHROW( HistogramSettings(pset.getParameter<ParameterSet>("input1")) );
    HistogramSettings s(pset.getParameter<ParameterSet>("input1"));
    CHECK( s.bins() == 12 );
    CHECK( s.min() == Approx(20.4) );
    CHECK( s.max() == Approx(54.2) );
  }
}
