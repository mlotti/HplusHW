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

    template <typename T> Exception& operator <<(const T& data) {
      _msg << data;
      return *this;
    }
    //template <typename T> std::ostream operator <<(std::ostream& s, const T& data);
    //template <typename E, typename T> E& operator <<(E& e, const T& data);

//     template <typename E, typename T> Exception& operator<<(const E& e, const T& data) {
//       E& ref = const_cast<E&>(e);
//       ref._msg << data;
//       return e;
//     }

    /*Exception& operator << (const char* msg);
    Exception& operator << (std::string& msg);
    Exception& operator << (Exception& e);*/
    virtual const char* what() const throw();
    std::string getMsg() const { return _msg.str(); }

  private:
    std::string _category;
    std::stringstream _msg;
  };
  

//   template <typename E, typename T> E& operator <<(E& e, const T& data) {
//     e._msg << data;
//     return e;
//   }

  
  
}
#endif
