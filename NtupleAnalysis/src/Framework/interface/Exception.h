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
    Exception(std::string& category) noexcept;
    Exception(const char* category) noexcept;
    Exception(const Exception& e) noexcept;
    virtual ~Exception();

    /// Enable streaming of the message (utilizes copy constructor)
    template <typename T> Exception& operator <<(const T& data) noexcept {
      _msg << data;
      return *this;
    }

    virtual const char* what() const noexcept;
    std::string getMsg() const { return _msg.str(); }
    std::string getCategory() const { return _category; }

  private:
    std::string _category;
    std::stringstream _msg;
  };
}
#endif
