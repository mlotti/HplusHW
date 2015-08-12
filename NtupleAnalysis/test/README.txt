Useful information for writing unit tests:

1) Basic philosophy:
- Add one unit test file per class
- Catch bugs, especially algebraic bugs, rather early than late

2) Methods of the catch-framework to be used for testing
- Checking routines (does not abort if statement is false)
    CHECK( statement )          : checks if statement is true
- Checking routines which abort if statement is false
    REQUIRE( statement )         : checks if statement is true
    REQUIRE_NOTHROW( code )      : passes if no exception is thrown
    REQUIRE_THROWS_AS( code, exception ) : passes if exception of type exception is thrown
- For unit tests with float or double values, use Approx(), for example:
    CHECK( 2.0 == Approx(1.999999) )

3) Adding rigged events for testing:
- See one of the test_EventSelection_* files for examples
 
4) Adding configuration for testing:
- If using the Event class, make sure to include the lines
      #include "test_createTree.h"
      boost::property_tree::ptree tmp = getMinimalConfig();
  into your test file (it guarantees that the discriminators get at
  least empty strings as input and therefore do not throw exception).
- A practical way is to use the boost property tree 
  (see one of the test_EventSelection_* files for examples)

5) Allowing the creation of root files for further debugging
- set the environmental variable DEBUGUNITTEST to "yes" to allow the test routines
  to create root files (not all of them will create them). This could be helpful
  in some debugging cases.
