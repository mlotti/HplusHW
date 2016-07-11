// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HistoWrapper_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HistoWrapper_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TemporaryDisabler.h"
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
  class WrappedUnfoldedFactorisationHisto; // x-axis containts values, y-axis contains unfolded bins of a multi-dimensional factorisation (used in QCD factorisation)

  /// Class for wrapping the making of histogram; calling Sumw2; and setting the event weight by default (can be overridden)
  class HistoWrapper {
  public:
    enum HistoLevel {
      kSystematics = 0,
      kVital,
      kInformative,
      kDebug,
      kNumberOfLevels
    };

    typedef HPlus::TemporaryDisabler<HistoWrapper> TemporaryDisabler;

    HistoWrapper(const EventWeight& eventWeight, std::string level);
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
    /// Wraps the making of an unfolded histogram; histogram is created only if the ambient level is low enough
    template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
    WrappedUnfoldedFactorisationHisto* makeTH(const int unfoldedBinCount, HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                              const Arg4& a4, const Arg5& a5);

    // Create directory if level is high enough
    TFileDirectory mkdir(HistoLevel level, TFileDirectory& parent, const std::string& name) {
      if(isActive(level))
        return parent.mkdir(name);
      return parent;
    }

    /// Returns the event weight
    double getWeight() const { return fEventWeight.getWeight(); }

    bool isActive(HistoLevel level) const {
      return fIsEnabled && (level <= fAmbientLevel);
    }

    void enable(bool enabled) { fIsEnabled = enabled; }
    bool getEnableStatus() const { return fIsEnabled; }
    TemporaryDisabler disableTemporarily() { return TemporaryDisabler(*this, false); }

    void printHistoStatistics() const;

  private:
    /// Method for checking if a directory exists
    bool checkIfDirExists(TDirectory* d, std::string name) const;

  private:
    /// EventWeight object
    const EventWeight& fEventWeight;
    /// Level of what histograms are saved to the root file
    HistoLevel fAmbientLevel;
    int fHistoLevelStats[kNumberOfLevels];

    std::vector<WrappedTH1*> fAllTH1Histos;
    std::vector<WrappedTH2*> fAllTH2Histos;
    std::vector<WrappedTH3*> fAllTH3Histos;
    std::vector<WrappedUnfoldedFactorisationHisto*> fAllUnfoldedFactorisationHistos;

    bool fIsEnabled;
  };

  /// Wrapper class for TH1 object
  class WrappedTH1 {
  public:
    WrappedTH1(HistoWrapper& histoWrapper, TH1* histo, HistoWrapper::HistoLevel level);
    ~WrappedTH1();

    /// Returns true if the histogram exists
    bool isActive() const { return fHistoWrapper.isActive(fLevel); }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH1* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1> void Fill(const Arg1& a1) { if (isActive()) h->Fill(a1, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (isActive()) h->Fill(a1, a2); }

    template<typename Arg1, typename Arg2> void SetBinContent(const Arg1& a1, const Arg2& a2) { if(isActive()) h->SetBinContent(a1, a2); }
    template<typename Arg1, typename Arg2> void SetBinError(const Arg1& a1, const Arg2& a2) { if(isActive()) h->SetBinError(a1, a2); }

  private:
    HistoWrapper& fHistoWrapper;
    TH1* h;
    HistoWrapper::HistoLevel fLevel;
  };

  /// Wrapper class for TH2 object
  class WrappedTH2 {
  public:
    WrappedTH2(HistoWrapper& histoWrapper, TH2* histo, HistoWrapper::HistoLevel level);
    ~WrappedTH2();

    /// Returns true if the histogram exists
    bool isActive() const { return fHistoWrapper.isActive(fLevel); }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH2* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (isActive()) h->Fill(a1, a2, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (isActive()) h->Fill(a1, a2, a3); }

  private:
    HistoWrapper& fHistoWrapper;
    TH2* h;
    HistoWrapper::HistoLevel fLevel;
  };

  /// Wrapper class for TH3 object
  class WrappedTH3 {
  public:
    WrappedTH3(HistoWrapper& histoWrapper, TH3* histo, HistoWrapper::HistoLevel level);
    ~WrappedTH3();

    /// Returns true if the histogram exists
    bool isActive() const { return fHistoWrapper.isActive(fLevel); }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH3* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (isActive()) h->Fill(a1, a2, a3, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2, typename Arg3, typename Arg4> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4) { if (isActive()) h->Fill(a1, a2, a3, a4); }

  private:
    HistoWrapper& fHistoWrapper;
    TH3* h;
    HistoWrapper::HistoLevel fLevel;
  };

  /// Wrapper class for factorisation histograms (binning unfolded on y-axis and value(s) on x-axis)
  class WrappedUnfoldedFactorisationHisto {
  public:
    WrappedUnfoldedFactorisationHisto(HistoWrapper& histoWrapper, TH2* histo, HistoWrapper::HistoLevel level);
    ~WrappedUnfoldedFactorisationHisto();

    /// Returns true if the histogram exists
    bool isActive() const { return fHistoWrapper.isActive(fLevel); }
    /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
    TH2* getHisto() { return h; }
    /// Returns the x axis of the histogram for bin label modification
    TAxis* GetXaxis() { return h->GetXaxis(); }
    /// Fills histogram (if it exists) with event weight
    template<typename Arg1> void Fill(const Arg1& a1, int factorisationBin) { if (isActive()) h->Fill(a1, factorisationBin, fHistoWrapper.getWeight()); }
    /// Fills histogram (if it exists) with custom event weight
    template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, int factorisationBin, const Arg2& a2) { if (isActive()) h->Fill(a1, factorisationBin, a2); }

  private:
    HistoWrapper& fHistoWrapper;
    TH2* h;
    HistoWrapper::HistoLevel fLevel;
  };

  //////////////////////////////////////// Implementations of inline/template functions
  //
  // The implementations of makeTH must be after WrappedTHN constructor declarations

  /// HistoWrapper
  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
  WrappedTH1* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                   const Arg4& a4, const Arg5& a5) {
    T* histo = 0;
    if (level <= fAmbientLevel) {
      // making a separate directory for debug histograms is not that easy here;
      // it should be done at the level of code which is calling this command
      histo = fd.make<T>(a1, a2, a3, a4, a5);
      histo->Sumw2();
    }
    fHistoLevelStats[level]++;
    fAllTH1Histos.push_back(new WrappedTH1(*this, histo, level));
    return fAllTH1Histos.at(fAllTH1Histos.size()-1);
  }

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8>
  WrappedTH2* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                     const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8) {
    T* histo = 0;
    if (level <= fAmbientLevel) {
      histo = fd.make<T>(a1, a2, a3, a4, a5, a6, a7, a8);
      histo->Sumw2();
    }
    fHistoLevelStats[level]++;
    fAllTH2Histos.push_back(new WrappedTH2(*this, histo, level));
    return fAllTH2Histos.at(fAllTH2Histos.size()-1);
  }

  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5, typename Arg6, typename Arg7, typename Arg8, typename Arg9,
           typename Arg10, typename Arg11>
  WrappedTH3* HistoWrapper::makeTH(HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                     const Arg4& a4, const Arg5& a5, const Arg6& a6, const Arg7& a7, const Arg8& a8,
                     const Arg9& a9, const Arg10& a10, const Arg11& a11) {
    T* histo = 0;
    if (level <= fAmbientLevel) {
      histo = fd.make<T>(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11);
      histo->Sumw2();
    }
    fHistoLevelStats[level]++;
    fAllTH3Histos.push_back(new WrappedTH3(*this, histo, level));
    return fAllTH3Histos.at(fAllTH3Histos.size()-1);
  }

    template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
    WrappedUnfoldedFactorisationHisto* HistoWrapper::makeTH(const int unfoldedBinCount, HistoLevel level, TFileDirectory& fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                                            const Arg4& a4, const Arg5& a5) {
    T* histo = 0;
    if (level <= fAmbientLevel) {
      histo = fd.make<T>(a1, a2, a3, a4, a5, unfoldedBinCount, 0, unfoldedBinCount);
      histo->Sumw2();
    }
    fHistoLevelStats[level]++;
    fAllUnfoldedFactorisationHistos.push_back(new WrappedUnfoldedFactorisationHisto(*this, histo, level));
    return fAllUnfoldedFactorisationHistos.at(fAllUnfoldedFactorisationHistos.size()-1);
  }


}

#endif
