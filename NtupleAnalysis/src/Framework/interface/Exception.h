// -*- c++ -*-
#ifndef Framework_Exception_h
#define Framework_Exception_h

#include <exception>
#include <string>
#include <sstream>

namespace hplus {
  class Exception : public std::exception {
  public:
    /// Print a demangled stack backtrace of the caller function
    Exception(const char* category);
    Exception(const Exception& e);
    virtual ~Exception();

    /// Enable streaming of the message (utilizes copy constructor)
    template <typename T> Exception& operator <<(const T& data) {
      std::stringstream s;
      s << _msg << data;
      _msg = s.str();
      return *this;
    }

    virtual const char* what() const noexcept { return _fullString.c_str(); }
    const std::string& getMsg() const { return _msg; }

  private:
    std::string _fullString;
    std::string _msgPrefix;
    std::string _msg;
    std::string _backtrace;
  };
}
#endif
