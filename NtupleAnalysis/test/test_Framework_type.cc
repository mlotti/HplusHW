#include "catch.hpp"

#include "Framework/interface/type.h"

#include <vector>
#include <iostream>

TEST_CASE("demangling works", "[Framework]") {
  CHECK( type<int>() == "int" );
  CHECK( type<unsigned int>() == "unsigned int" );
  CHECK( type<unsigned long long>() == "unsigned long long" );
  CHECK( type<float>() == "float" );
  CHECK( type<double>() == "double" );
  CHECK( type<std::vector<bool>>() == "vector<bool>" );
  CHECK( type<std::vector<int>>() == "vector<int>" );
  CHECK( type<std::vector<unsigned int>>() == "vector<unsigned int>" );
  CHECK( type<std::vector<unsigned long long>>() == "vector<ULong64_t>" );
  CHECK( type<std::vector<float>>() == "vector<float>" );
  CHECK( type<std::vector<double>>() == "vector<double>" );

}
