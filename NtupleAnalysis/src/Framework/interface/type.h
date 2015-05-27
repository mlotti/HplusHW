// -*- c++ -*-
#ifndef Framework_type_h
#define Framework_type_h

#include <string>
#include <typeinfo>

// http://stackoverflow.com/questions/281818/unmangling-the-result-of-stdtype-infoname
// https://gcc.gnu.org/onlinedocs/libstdc++/manual/ext_demangling.html

std::string demangle(const std::type_info& typeinfo);

template <typename T>
std::string type(const T& t) {
    return demangle(typeid(t));
}

template <typename T>
std::string type() {
  return demangle(typeid(T));
}


#endif
