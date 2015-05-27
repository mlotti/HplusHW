#include "Framework/interface/type.h"

#include "TClass.h"

#ifdef __GNUG__
#include <cstdlib>
#include <memory>
#include <cxxabi.h>

namespace {
  std::string demangle_(const char* name) {
    int status = -4;

    // enable c++11 by passing the flag -std=c++11 to g++
    std::unique_ptr<char, void(*)(void*)> res {
      abi::__cxa_demangle(name, NULL, NULL, &status),
        std::free
    };

    return (status==0) ? res.get() : name ;
  }
}
#else

// does nothing if not g++
namespace {
  std::string demangle_(const char* name) {
    return name;
  }
}

#endif


std::string demangle(const std::type_info& typeinfo) {
  // Try first with ROOT's TClass in order to avoid the default
  // parameters of templates in the demangled name (e.g. allocator for
  // vector). If that fails (e.g. primitive types), go with the
  // GCC-specific __cxa_demangle.
  TClass *cl = TClass::GetClass(typeinfo);
  if(cl) {
    return std::string(cl->GetName());
  }
  return demangle_(typeinfo.name());
}
