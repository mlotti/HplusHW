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
    Exception(std::string& category);
    Exception(const char* category);
    Exception(const Exception& e);
    virtual ~Exception();

    /// Enable streaming of the message (utilizes copy constructor)
    template <typename T> Exception& operator <<(const T& data) {
      _msg << data;
      return *this;
    }

    virtual const char* what() const throw();
    std::string getMsg() const { return _msg.str(); }
    std::string getCategory() const { return _category; }

  private:
    std::string _category;
    std::stringstream _msg;
  };
}
#endif
