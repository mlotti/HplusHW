// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HistoWrapper_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HistoWrapper_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

#include <string>
#include <vector>

namespace HPlus {
  // Forward declarations of WrappedTHN
  class WrappedTH1;
  class WrappedTH2;
  class WrappedTH3;

  /// Class for wrapping the making of histogram; calling Sumw2; and setting the event weight by default (can be overridden)
  class HistoWrapper {
  public:
    enum HistoLevel {
      kVital,
      kInformative,
      kDebug
    };

    HistoWrapper(EventWeight& eventWeight, std::string level);
    ~HistoWrapper();

    /// Wraps the making of histogram; histogram is created only if the ambient level is low enough
    template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
    WrappedTH1* makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                       const Arg4& a4, const Arg5& a5);
    /// Wraps the making of histogram; histogram is created only if the ambient level is low enough
    template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8>
    WrappedTH2* makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                       const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8);
    /// Wraps the making of histogram; histogram is created only if the ambient level is low enough
    template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8, typename Arg9,
           typename Arg10, typename Arg11>
    WrappedTH3* makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                       const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8,
                       const Arg9& a9, const Arg10& a10, const Arg11& a11);

    /// Returns the event weight
    double getWeight() const { return fEventWeight.getWeight(); }

  private:
    /// Method for checking if a directory exists
    bool checkIfDirExists(TDirectory* d, std::string name) const;

  private:
    /// EventWeight object
    EventWeight& fEventWeight;
    /// Level of what histograms are saved to the root file
    HistoLevel fAmbientLevel;

    std::vector<WrappedTH1*> fAllTH1Histos;
    std::vector<WrappedTH2*> fAllTH2Histos;
    std::vector<WrappedTH3*> fAllTH3Histos;
  };

  /// Wrapper class for TH1 object
  class WrappedTH1 {
  public:
    WrappedTH1(HistoWrapper& histoWrapper, TH1* histo, bool isActive);
    ~WrappedTH1();

    /// Returns true if the histogram exists
    bool isActive() const { return bIsActive; }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH1* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1> void Fill(const Arg1& a1) { if (bIsActive) h->Fill(a1, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (bIsActive) h->Fill(a1, a2); }

  private:
    HistoWrapper& fHistoWrapper;
    TH1* h;
    bool bIsActive;
  };

  /// Wrapper class for TH2 object
  class WrappedTH2 {
  public:
    WrappedTH2(HistoWrapper& histoWrapper, TH2* histo, bool isActive);
    ~WrappedTH2();

    /// Returns true if the histogram exists
    bool isActive() const { return bIsActive; }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH2* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (bIsActive) h->Fill(a1, a2, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (bIsActive) h->Fill(a1, a2, a3); }

  private:
    HistoWrapper& fHistoWrapper;
    TH2* h;
    bool bIsActive;
  };

  /// Wrapper class for TH3 object
  class WrappedTH3 {
  public:
    WrappedTH3(HistoWrapper& histoWrapper, TH3* histo, bool isActive);
    ~WrappedTH3();

    /// Returns true if the histogram exists
    bool isActive() const { return bIsActive; }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH3* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (bIsActive) h->Fill(a1, a2, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (bIsActive) h->Fill(a1, a2, a3); }

  private:
    HistoWrapper& fHistoWrapper;
    TH3* h;
    bool bIsActive;
  };

  //////////////////////////////////////// Implementations of inline/template functions
  //
  // The implementations of makeTH must be after WrappedTHN constructor declarations

  /// HistoWrapper
  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
  WrappedTH1* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                   const Arg4& a4, const Arg5& a5) {
    if (level <= fAmbientLevel) {
      // making a separate directory for debug histograms is not that easy here;
      // it should be done at the level of code which is calling this command
      T* histo = fd.make<T>(a1, a2, a3, a4, a5);
      histo->Sumw2();
      fAllTH1Histos.push_back(new WrappedTH1(*this, histo, true));
    } else {
      // Histogram is suppressed
      TH1* histo = 0;
      fAllTH1Histos.push_back(new WrappedTH1(*this, histo, false));
    }
    return fAllTH1Histos.at(fAllTH1Histos.size()-1);
  }

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8>
  WrappedTH2* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                     const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8) {
    if (level <= fAmbientLevel) {
      T* histo = fd.make<T>(a1, a2, a3, a4, a5, a6, a7, a8);
      histo->Sumw2();
      fAllTH2Histos.push_back(new WrappedTH2(*this, histo, true));
    } else {
      // Histogram is suppressed
      TH2* histo = 0;
      fAllTH2Histos.push_back(new WrappedTH2(*this, histo, false));
    }
    return fAllTH2Histos.at(fAllTH2Histos.size()-1);
  }

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8, typename Arg9,
           typename Arg10, typename Arg11>
  WrappedTH3* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                     const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8,
                     const Arg9& a9, const Arg10& a10, const Arg11& a11) {
    if (level <= fAmbientLevel) {
      T* histo = fd.make<T>(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11);
      histo->Sumw2();
      fAllTH3Histos.push_back(new WrappedTH3(*this, histo, true));
    } else {
      // Histogram is suppressed
      TH3* histo = 0;
      fAllTH3Histos.push_back(new WrappedTH3(*this, histo, false));
    }
    return fAllTH3Histos.at(fAllTH3Histos.size()-1);
  }


}

#endif
