#include "catch.hpp"

#include "Framework/interface/BranchTraits.h"

#include <vector>

namespace {
  template <typename T1, typename T2>
  struct is_equal {
    static constexpr bool value = false;
  };
  template <typename T>
  struct is_equal<T, T> {
    static constexpr bool value = true;
  };
}

TEST_CASE("BranchTraits gives correct types", "[Framework]") {
  SECTION("bool is a simple type") {
    CHECK( (is_equal<BranchTraits<bool>::DataType, bool>::value) );
    CHECK( (is_equal<BranchTraits<bool>::ReturnType, bool>::value) );
  }
  SECTION("int is a simple type") {
    CHECK( (is_equal<BranchTraits<int>::DataType, int>::value) );
    CHECK( (is_equal<BranchTraits<int>::ReturnType, int>::value) );
  }
  SECTION("unsigned int is a simple type") {
    CHECK( (is_equal<BranchTraits<unsigned int>::DataType, unsigned int>::value) );
    CHECK( (is_equal<BranchTraits<unsigned int>::ReturnType, unsigned int>::value) );
  }
  SECTION("unsigned long long is a simple type") {
    CHECK( (is_equal<BranchTraits<unsigned long long>::DataType, unsigned long long>::value) );
    CHECK( (is_equal<BranchTraits<unsigned long long>::ReturnType, unsigned long long>::value) );
  }
  SECTION("float is a simple type") {
    CHECK( (is_equal<BranchTraits<float>::DataType, float>::value) );
    CHECK( (is_equal<BranchTraits<float>::ReturnType, float>::value) );
  }
  SECTION("double is a simple type") {
    CHECK( (is_equal<BranchTraits<double>::DataType, double>::value) );
    CHECK( (is_equal<BranchTraits<double>::ReturnType, double>::value) );
  }
  SECTION("vector<int> is a complex type") {
    using Vec = std::vector<int>;
    CHECK( (is_equal<BranchTraits<Vec>::DataType, Vec *>::value) );
    CHECK( (is_equal<BranchTraits<Vec>::ReturnType, const Vec&>::value) );
  }
}
