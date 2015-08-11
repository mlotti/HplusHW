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
#include <sys/prctl.h> 

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
    
    // Use gdb to obtain backtrace
    int pid = getpid();
    prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY, 0, 0, 0); // needed to disable temporarily ptracer
    int child_pid = fork(); // needed to disable temporarily ptracer
    if (!child_pid) {           
      std::stringstream cmd;
      cmd << "gdb --batch -p " << pid << " -ex bt";
      FILE* f = popen (cmd.str().c_str(), "r");
      if (f != NULL) {
        std::cout << cmd.str() << std::endl;
        char buff[512];
        for (char* p = fgets(buff, sizeof(buff), f); p != NULL; p = fgets(buff, sizeof(buff), f)) {
          s << p;
        }
        pclose(f);
      }
    } else {
      waitpid(child_pid,NULL,0);
    }
    _backtrace = s.str();
  }
 
  Exception::Exception(const Exception& e) noexcept
  : std::exception(),
    _fullString(e._msgPrefix+e._msg+e._backtrace),
    _msgPrefix(e._msgPrefix),
    _msg(e._msg),
    _backtrace(e._backtrace)
  { }
  
  Exception::~Exception() { }

}
