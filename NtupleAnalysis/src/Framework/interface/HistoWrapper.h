// -*- c++ -*-
#ifndef Framework_HistoWrapper_h
#define Framework_HistoWrapper_h

#include "Framework/interface/makeTH.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/HistoWrapperTraits.h"

#include "TDirectory.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

#include <vector>
#include <string>
#include <memory>

// Forward declarations of WrappedTHN
class WrappedTH1;
class WrappedTH2;
class WrappedTH3;
class WrappedUnfoldedFactorisationHisto; // x-axis containts values, y-axis contains unfolded bins of a multi-dimensional factorisation (used in QCD factorisation)

enum class HistoLevel {
  kSystematics = 0,
  kVital,
  kInformative,
  kDebug,
  kNumberOfLevels
};

/// Class for wrapping the making of histogram; calling Sumw2; and setting the event weight by default (can be overridden)
class HistoWrapper {
public:

  HistoWrapper(const EventWeight& eventWeight, const std::string& level);
  ~HistoWrapper();

  template <typename T, typename ...Args>
  typename HistoWrapperTraits<T>::type *makeTH(HistoLevel level, TDirectory *dir, Args&&... args) {
    using Wrapped = typename HistoWrapperTraits<T>::type;
    return makeTH_<Wrapped, T>(level, dir, std::forward<Args>(args)...);
  }

  /// Wraps the making of an unfolded histogram; histogram is created only if the ambient level is low enough
  template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
           typename Arg5>
  WrappedUnfoldedFactorisationHisto* makeTH(const int unfoldedBinCount, HistoLevel level, TDirectory *fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                            const Arg4& a4, const Arg5& a5);

  // Create directory if level is high enough
  TDirectory *mkdir(HistoLevel level, TDirectory *parent, const std::string& name) {
    if(isActive(level))
      return parent->mkdir(name.c_str());
    return parent;
  }

  /// Returns the event weight
  double getWeight() const { return fEventWeight.getWeight(); }

  bool isActive(HistoLevel level) const {
    return fIsEnabled && (level <= fAmbientLevel);
  }

  void enable(bool enabled) { fIsEnabled = enabled; }
  bool isEnabled() const { return fIsEnabled; }

  void printHistoStatistics() const;

private:
  template <typename Wrapped, typename T, typename ...Args>
  Wrapped *makeTH_(HistoLevel level, TDirectory *dir, Args&&... args);

  WrappedTH1 *pushWrapper(WrappedTH1 *wrapper) {
    fAllTH1Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedTH2 *pushWrapper(WrappedTH2 *wrapper) {
    fAllTH2Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedTH3 *pushWrapper(WrappedTH3 *wrapper) {
    fAllTH3Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedUnfoldedFactorisationHisto *pushWrapper(WrappedUnfoldedFactorisationHisto *wrapper) {
    fAllUnfoldedFactorisationHistos.emplace_back(wrapper);
    return wrapper;
  }

  /// EventWeight object
  const EventWeight& fEventWeight;
  /// Level of what histograms are saved to the root file
  HistoLevel fAmbientLevel;
  int fHistoLevelStats[static_cast<int>(HistoLevel::kNumberOfLevels)];

  std::vector<std::unique_ptr<WrappedTH1>> fAllTH1Histos;
  std::vector<std::unique_ptr<WrappedTH2>> fAllTH2Histos;
  std::vector<std::unique_ptr<WrappedTH3>> fAllTH3Histos;
  std::vector<std::unique_ptr<WrappedUnfoldedFactorisationHisto>> fAllUnfoldedFactorisationHistos;

  bool fIsEnabled;
};

template <typename T>
class WrappedBase {
public:
  WrappedBase(const HistoWrapper& histoWrapper, T *histo, HistoLevel level):
    h(histo), fHistoWrapper(histoWrapper), fLevel(level) {}

  /// Returns true if the histogram exists
  bool isActive() const { return fHistoWrapper.isActive(fLevel); }
  /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
  T* getHisto() { return h; }
  /// Returns the x axis of the histogram for bin label modification
  TAxis* GetXaxis() { return h->GetXaxis(); }

protected:
  T* h;

  double getWeight() const { return fHistoWrapper.getWeight(); }

private:
  const HistoWrapper& fHistoWrapper;
  HistoLevel fLevel;
};

/// Wrapper class for TH1 object
class WrappedTH1: public WrappedBase<TH1> {
public:
  WrappedTH1(const HistoWrapper& histoWrapper, TH1* histo, HistoLevel level):
    WrappedBase<TH1>(histoWrapper, histo, level) {}
  ~WrappedTH1();

  /// Fills histogram (if it exists) with event weight
  template<typename Arg1> void Fill(const Arg1& a1) { if (isActive()) h->Fill(a1, getWeight()); }
  /// Fills histogram (if it exists) with custom event weight
  template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (isActive()) h->Fill(a1, a2); }

  template<typename Arg1, typename Arg2> void SetBinContent(const Arg1& a1, const Arg2& a2) { if(isActive()) h->SetBinContent(a1, a2); }
  template<typename Arg1, typename Arg2> void SetBinError(const Arg1& a1, const Arg2& a2) { if(isActive()) h->SetBinError(a1, a2); }
};

/// Wrapper class for TH2 object
class WrappedTH2: public WrappedBase<TH2> {
public:
  WrappedTH2(const HistoWrapper& histoWrapper, TH2* histo, HistoLevel level):
    WrappedBase<TH2>(histoWrapper, histo, level) {}
  ~WrappedTH2();

  /// Fills histogram (if it exists) with event weight
  template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, const Arg2& a2) { if (isActive()) h->Fill(a1, a2, getWeight()); }
  /// Fills histogram (if it exists) with custom event weight
  template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (isActive()) h->Fill(a1, a2, a3); }
};

/// Wrapper class for TH3 object
class WrappedTH3: public WrappedBase<TH3> {
public:
  WrappedTH3(const HistoWrapper& histoWrapper, TH3* histo, HistoLevel level):
    WrappedBase<TH3>(histoWrapper, histo, level) {}
  ~WrappedTH3();

  /// Fills histogram (if it exists) with event weight
  template<typename Arg1, typename Arg2, typename Arg3> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3) { if (isActive()) h->Fill(a1, a2, a3, getWeight()); }
  /// Fills histogram (if it exists) with custom event weight
  template<typename Arg1, typename Arg2, typename Arg3, typename Arg4> void Fill(const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4) { if (isActive()) h->Fill(a1, a2, a3, a4); }
};

/// Wrapper class for factorisation histograms (binning unfolded on y-axis and value(s) on x-axis)
class WrappedUnfoldedFactorisationHisto: public WrappedBase<TH2> {
public:
  WrappedUnfoldedFactorisationHisto(const HistoWrapper& histoWrapper, TH2* histo, HistoLevel level):
    WrappedBase<TH2>(histoWrapper, histo, level) {}
  ~WrappedUnfoldedFactorisationHisto();

  /// Fills histogram (if it exists) with event weight
  template<typename Arg1> void Fill(const Arg1& a1, int factorisationBin) { if (isActive()) h->Fill(a1, factorisationBin, getWeight()); }
  /// Fills histogram (if it exists) with custom event weight
  template<typename Arg1, typename Arg2> void Fill(const Arg1& a1, int factorisationBin, const Arg2& a2) { if (isActive()) h->Fill(a1, factorisationBin, a2); }
};

//////////////////////////////////////// Implementations of inline/template functions
//
// The implementations of makeTH must be after WrappedTHN constructor declarations

template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4,
         typename Arg5>
WrappedUnfoldedFactorisationHisto* HistoWrapper::makeTH(const int unfoldedBinCount, HistoLevel level, TDirectory *fd, const Arg1& a1, const Arg2& a2, const Arg3& a3,
                                                        const Arg4& a4, const Arg5& a5) {
  return makeTH_<WrappedUnfoldedFactorisationHisto, T>(level, fd, a1, a2, a3, a4, a5, unfoldedBinCount, 0, unfoldedBinCount);
}

template <typename Wrapped, typename T, typename ...Args>
Wrapped *HistoWrapper::makeTH_(HistoLevel level, TDirectory *dir, Args&&... args) {
  T *histo = nullptr;
  if(level <= fAmbientLevel) {
    // making a separate directory for debug histograms is not that easy here;
    // it should be done at the level of code which is calling this command
    histo = ::makeTH<T>(dir, std::forward<Args>(args)...);
  }
  fHistoLevelStats[static_cast<int>(level)]++;
  return pushWrapper(new Wrapped(*this, histo, level));
}


#endif
