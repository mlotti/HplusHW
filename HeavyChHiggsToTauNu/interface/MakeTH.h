// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MakeTH_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MakeTH_h

#include "CommonTools/Utils/interface/TFileDirectory.h"

namespace HPlus {
  // Wrappers to call automatically TH1::Sumw2() after the histogram creation
  // If the function for some number of arguments is missing, please go a head and add one

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4, 
           typename Arg5>
  T* makeTH(TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4, 
            const Arg5& a5) {
    T* histo = fd.make<T>(a1, a2, a3, a4, a5);
    histo->Sumw2();
    return histo;
  }

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4, 
           typename Arg5, typename Arg6, typename Arg7, typename Arg8>
  T* makeTH(TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4, 
            const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8) {
    T* histo = fd.make<T>(a1, a2, a3, a4, a5, a6, a7, a8);
    histo->Sumw2();
    return histo;
  }

}

#endif
