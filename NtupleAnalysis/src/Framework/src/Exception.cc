// -*- c++ -*-
#include "Framework/interface/Exception.h"
#include <boost/concept_check.hpp>

#include <stdio.h>
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <execinfo.h>
#include <cxxabi.h>
#include <cstring>
#include <sys/wait.h>
#include <unistd.h>
#ifndef HOST_LXPLUS
#include "Framework/interface/woTracer.h"
#else
#include "Framework/interface/wTracer.h"
#endif

#include "TSystem.h"

namespace hplus {
  Exception::Exception(const char* category)
  : std::exception()
  { 
    // Construct beginning of message
    std::stringstream s;
    s << "Exception of category '" << category << "' occurred with message:" << std::endl << std::endl;
    s << ">>> ";
    _msgPrefix = s.str();
    s.str("");
    s << std::endl;
    // Do not construct backtrace message if called from unit tests
    bool isCalledFromUnitTest = false;
    unsigned int max_frames = 63;
    void* addrlist[max_frames+1]; // storage array for stack trace address data
    int addrlen = backtrace(addrlist, sizeof(addrlist) / sizeof(void*)); // retrieve current stack addresses
    if (addrlen != 0) {
      char** symbollist = backtrace_symbols(addrlist, addrlen); // resolve addresses into strings containing "filename(function+address)", this array must be free()-ed
      for (int i = 1; i < addrlen; i++) {
        if (std::string(symbollist[i]).find("HiggsAnalysis/NtupleAnalysis/test/main()") != std::string::npos)
          isCalledFromUnitTest = true;
      }
      free(symbollist);
    }
    if (isCalledFromUnitTest)
      return;
    // Use gdb to obtain backtrace
    int pid = getpid();
// #ifndef HOST_LXPLUS
//     // Do not apply on lxplus
//     prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY, 0, 0, 0); // needed to disable temporarily ptracer
// #endif
    int child_pid = fork(); // needed to disable temporarily ptracer
    if (!child_pid) {           
      std::stringstream cmd;
      cmd << "gdb --batch -p " << pid << " -ex bt &> /dev/null";
      FILE* f = popen (cmd.str().c_str(), "r");
      if (f != NULL) {
        char buff[512];
        for (char* p = fgets(buff, sizeof(buff), f); p != NULL; p = fgets(buff, sizeof(buff), f)) {
          if (p[0] == '#')
            s << p;
        }
        pclose(f);
      }
    } else {
      waitpid(child_pid,NULL,0);
    }
    _backtrace = s.str();
  }
 
  Exception::Exception(const Exception& e)
  : std::exception(),
    _fullString(e._msgPrefix+e._msg+e._backtrace),
    _msgPrefix(e._msgPrefix),
    _msg(e._msg),
    _backtrace(e._backtrace)
  { }
  
  Exception::~Exception() { }

}
