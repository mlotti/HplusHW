// -*- c++ -*-
#include "Framework/interface/Exception.h"
#include <boost/concept_check.hpp>

#include <stdio.h>
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <execinfo.h>
#include <cxxabi.h>

namespace hplus {
  Exception::Exception(const char* category)
  : std::exception()
  { 
    // Construct beginning of message
    std::stringstream s;
    s << "Exception of category '" << category << "' occurred with message:" << std::endl;
    s << ">>> ";
    _msgPrefix = s.str();
    s.str("");
    
    // Construct backtrace
    unsigned int max_frames = 63;
    bool calledInsideUnitTest = false;
    s << std::endl << "Backtrace:" << std::endl;

    // storage array for stack trace address data
    void* addrlist[max_frames+1];

    // retrieve current stack addresses
    int addrlen = backtrace(addrlist, sizeof(addrlist) / sizeof(void*));

    if (addrlen == 0) {
      s << "  <empty, possibly corrupt>" << std::endl;
      _backtrace = s.str();
      return;
    }

    // resolve addresses into strings containing "filename(function+address)",
    // this array must be free()-ed
    char** symbollist = backtrace_symbols(addrlist, addrlen);

    // allocate string which will be filled with the demangled function name
    size_t funcnamesize = 256;
    char* funcname = (char*)malloc(funcnamesize);

    // iterate over the returned symbol lines. skip the first, it is the
    // address of this function.
    for (int i = 1; i < addrlen; i++) {
      char *begin_name = 0, *begin_offset = 0, *end_offset = 0;

      // find parentheses and +address offset surrounding the mangled name:
      // ./module(function+0x15c) [0x8048a6d]
      for (char *p = symbollist[i]; *p; ++p) {
        if (*p == '(')
          begin_name = p;
        else if (*p == '+')
          begin_offset = p;
        else if (*p == ')' && begin_offset) {
          end_offset = p;
          break;
        }
      }

      if (begin_name && begin_offset && end_offset && begin_name < begin_offset) {
        *begin_name++ = '\0';
        *begin_offset++ = '\0';
        *end_offset = '\0';

        // mangled name is now in [begin_name, begin_offset) and caller
        // offset in [begin_offset, end_offset). now apply
        // __cxa_demangle():

        int status;
        char* ret = abi::__cxa_demangle(begin_name, funcname, &funcnamesize, &status);
        
        if (status == 0) {
          funcname = ret; // use possibly realloc()-ed string
          s << "  " << symbollist[i] << ": " << funcname << ": (symbol offset) " << begin_offset << std::endl;
        } else {
          // demangling failed. Output function name as a C function with
          // no arguments.
          s << "  " << symbollist[i] << ": " << begin_name << ": (symbol offset) " << begin_offset << std::endl;
        }
      }
      else {
        // couldn't parse the line? print the whole line.
        s << "  " << symbollist[i] << std::endl;
      }
    }
    free(funcname);
    free(symbollist);
    _backtrace = s.str();
  }
 
  Exception::Exception(const Exception& e) noexcept
  : std::exception(),
    _msgPrefix(e._msgPrefix),
    _msg(e._msg),
    _backtrace(e._backtrace)
  { }
  
  Exception::~Exception() { }
}
