// -*- c++ -*-
#ifndef Framework_makeTH_h
#define Framework_makeTH_h

#include <utility>

class TDirectory;

// Wrapper to call automatically TH1::Sumw2() after the histogram creation
// User C++11 perfect forwarding ti avoid repetition of overloads
template<typename T, typename ...Args>
T* makeTH(TDirectory *dir, Args&&... args) {
  T *histo = new T(std::forward<Args>(args)...);
  histo->SetDirectory(dir);
  histo->Sumw2();
  return histo;
}

#endif
