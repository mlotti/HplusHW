// -*- c++ -*-
#ifndef Framework_HistoWrapper_h
#define Framework_HistoWrapper_h

#include "Framework/interface/makeTH.h"
#include "Framework/interface/EventWeight.h"
#include "Framework/interface/Exception.h"
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
class WrappedUnfoldedFactorisationHisto; // x-axis containts values, y-axis contains unfolded bins of a multi-dimensional factorisation
class WrappedTH1Triplet;
class WrappedTH2Triplet;
class WrappedTH3Triplet;

enum class HistoLevel {
  kNever = 0,
  kSystematics,
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

  /// Wraps the making of a triplet histogram; histogram is created only if the ambient level is low enough
  template <typename T, typename ...Args>
  typename HistoWrapperTripletTraits<T>::type *makeTHTriplet(bool enableTrueHistogram, HistoLevel level, std::vector<TDirectory*>& dirs, Args&&... args) {
    using WrappedTriplet = typename HistoWrapperTripletTraits<T>::type;
    return makeTHTriplet_<WrappedTriplet, T>(enableTrueHistogram, level, dirs, std::forward<Args>(args)...);
  } 
  
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

  template <typename WrappedTriplet, typename T, typename ...Args>
  WrappedTriplet *makeTHTriplet_(bool enableTrueHistogram, HistoLevel level, std::vector<TDirectory*>& dirs, Args&&... args);
  
  WrappedTH1 *pushWrapper(WrappedTH1 *wrapper) {
    //fAllTH1Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedTH2 *pushWrapper(WrappedTH2 *wrapper) {
    //fAllTH2Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedTH3 *pushWrapper(WrappedTH3 *wrapper) {
    //fAllTH3Histos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedUnfoldedFactorisationHisto *pushWrapper(WrappedUnfoldedFactorisationHisto *wrapper) {
    //fAllUnfoldedFactorisationHistos.emplace_back(wrapper);
    return wrapper;
  }
  WrappedTH1Triplet *pushWrapper(WrappedTH1Triplet *wrapper) {
    //fWrappedTH1TripletHistos.emplace_back(wrapper);
    return wrapper;
  }    
  WrappedTH2Triplet *pushWrapper(WrappedTH2Triplet *wrapper) {
    //fWrappedTH2TripletHistos.emplace_back(wrapper);
    return wrapper;
  }    
  WrappedTH3Triplet *pushWrapper(WrappedTH3Triplet *wrapper) {
    //fWrappedTH3TripletHistos.emplace_back(wrapper);
    return wrapper;
  }    

  /// EventWeight object
  const EventWeight& fEventWeight;
  /// Level of what histograms are saved to the root file
  HistoLevel fAmbientLevel;
  int fHistoLevelStats[static_cast<int>(HistoLevel::kNumberOfLevels)];

  /*std::vector<std::unique_ptr<WrappedTH1>> fAllTH1Histos;
  std::vector<std::unique_ptr<WrappedTH2>> fAllTH2Histos;
  std::vector<std::unique_ptr<WrappedTH3>> fAllTH3Histos;
  std::vector<std::unique_ptr<WrappedUnfoldedFactorisationHisto>> fAllUnfoldedFactorisationHistos;
  std::vector<std::unique_ptr<WrappedTH1Triplet>> fWrappedTH1TripletHistos;
  std::vector<std::unique_ptr<WrappedTH2Triplet>> fWrappedTH2TripletHistos;
  std::vector<std::unique_ptr<WrappedTH3Triplet>> fWrappedTH3TripletHistos;
  */
  bool fIsEnabled;
};

template <typename T>
class WrappedBase {
public:
  WrappedBase(const HistoWrapper& histoWrapper, T *histo, HistoLevel level):
    h(histo), fHistoWrapper(histoWrapper), fLevel(level) {}
  ~WrappedBase() {
    if (h != nullptr) {
      h->Delete();
      h = nullptr;
    }
  }

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

template<class T>
class WrappedTHxTripletBase {
public:
  WrappedTHxTripletBase(const HistoWrapper& histoWrapper, std::vector<T*>& h, HistoLevel level, bool enableTrueHistogram)
  : fHistoWrapper(histoWrapper), fLevel(level), bEnableTrueHistogram(enableTrueHistogram) {
   if (h.size() >= 2) {
      hInclusive = h[0];
      hFalse = h[1];
    } else
      throw hplus::Exception("assert") << "Expect at least 2 histograms for WrappedTHxTriplet (" << h.size() << ") given!";
    if (h.size() > 2)
      hTrue = h[2];
    else
      hTrue = nullptr;
  }
  ~WrappedTHxTripletBase() { 
    if (isActive()) {
      hInclusive->Delete();
      hInclusive = nullptr;
      hFalse->Delete();
      hFalse = nullptr;
      if (hTrue != nullptr) {
        hTrue->Delete();
        hTrue = nullptr;
      }
    }
  }
  
  /// Returns true if the histograms exist
  bool isActive() const { return fHistoWrapper.isActive(fLevel); }
  
  /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
  T* getInclusiveHisto() { return hInclusive; }
  /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active)
  T* getFalseHisto() { return hFalse; }
  /// Returns pointer to the histogram (Note: it can be a zero pointer if the histogram is not active or not enabled)
  T* getTrueHisto() { return hTrue; }
  /// Sets the bin label
  void SetBinLabel(int i, std::string label) {
    if (!this->isActive()) return;
    hInclusive->GetXaxis()->SetBinLabel(i, label.c_str());
    hFalse->GetXaxis()->SetBinLabel(i, label.c_str());
    if (hTrue != nullptr) {
      hTrue->GetXaxis()->SetBinLabel(i, label.c_str());
    }
  }

protected: 
  double getWeight() const { return fHistoWrapper.getWeight(); }
  
  /// Fills histogram (if it exists) with value
  template<typename ...Args> void _Fill(bool status, Args&&... args) {
    if (!this->isActive()) return;
    if (status) {
      if (this->bEnableTrueHistogram) this->hTrue->Fill(std::forward<Args>(args)...);
    } else {
      this->hFalse->Fill(std::forward<Args>(args)...);
    }
    this->hInclusive->Fill(std::forward<Args>(args)...);
  }
  
protected:
  T* hInclusive;
  T* hFalse;
  T* hTrue;

private:
  const HistoWrapper& fHistoWrapper;
  HistoLevel fLevel;
  const bool bEnableTrueHistogram;
};

/// Wrapper class for TH1 triplet object
class WrappedTH1Triplet : public WrappedTHxTripletBase<TH1> {
public:
  WrappedTH1Triplet(const HistoWrapper& histoWrapper, std::vector<TH1*>& h, HistoLevel level, bool enableTrueHistogram)
  : WrappedTHxTripletBase(histoWrapper, h, level, enableTrueHistogram) { }
  ~WrappedTH1Triplet() { }
  
  /// Fills histogram (if it exists) with value
  template<typename Arg1> void Fill(bool status, const Arg1& a1) { this->_Fill(status, a1, getWeight()); }
  /// Fills histogram (if it exists) with value and weight
  template<typename Arg1, typename Arg2> void Fill(bool status, const Arg1& a1, const Arg2& a2) { this->_Fill(status, a1, a2); }
};

/// Wrapper class for TH2 triplet object
class WrappedTH2Triplet : public WrappedTHxTripletBase<TH2> {
public:
  WrappedTH2Triplet(const HistoWrapper& histoWrapper, std::vector<TH2*>& h, HistoLevel level, bool enableTrueHistogram)
  : WrappedTHxTripletBase(histoWrapper, h, level, enableTrueHistogram) { }
  ~WrappedTH2Triplet() { }
  
  /// Fills histogram (if it exists) with value
  template<typename Arg1, typename Arg2> void Fill(bool status, const Arg1& a1, const Arg2& a2) { this->_Fill(status, a1, a2, getWeight()); }
  /// Fills histogram (if it exists) with value and weight
  template<typename Arg1, typename Arg2, typename Arg3> void Fill(bool status, const Arg1& a1, const Arg2& a2, const Arg3& a3) { this->_Fill(status, a1, a2, a3); }
};

/// Wrapper class for TH2 triplet object
class WrappedTH3Triplet : public WrappedTHxTripletBase<TH3> {
public:
  WrappedTH3Triplet(const HistoWrapper& histoWrapper, std::vector<TH3*>& h, HistoLevel level, bool enableTrueHistogram)
  : WrappedTHxTripletBase(histoWrapper, h, level, enableTrueHistogram) { }
  ~WrappedTH3Triplet() { }
  
  /// Fills histogram (if it exists) with value
  template<typename Arg1, typename Arg2, typename Arg3> void Fill(bool status, const Arg1& a1, const Arg2& a2, const Arg3& a3) { this->_Fill(status, a1, a2, a3, getWeight()); }
  /// Fills histogram (if it exists) with value and weight
  template<typename Arg1, typename Arg2, typename Arg3, typename Arg4> void Fill(bool status, const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4) { this->_Fill(status, a1, a2, a3, a4); }
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

template <typename WrappedTriplet, typename T, typename ...Args>
WrappedTriplet *HistoWrapper::makeTHTriplet_(bool enableTrueHistogram, HistoLevel level, std::vector<TDirectory*>& dirs, Args&&... args) {
  if (enableTrueHistogram) {
    if (dirs.size() != 3)
      throw hplus::Exception("Logic") << "Expecting three directories when true histogram is enabled!";
  } else {
    if (dirs.size() != 2)
      throw hplus::Exception("Logic") << "Expecting two directories when true histogram is enabled!";
  }
  
  using THType = typename HistoWrapperTHTraits<T>::type;
  std::vector<THType*> histos;
  for (const auto& p: dirs) {
    if(level <= fAmbientLevel) {
      histos.push_back(::makeTH<T>(p, std::forward<Args>(args)...));
    } else {
      T *histo = nullptr;
      histos.push_back(histo);
    }
  }
  fHistoLevelStats[static_cast<int>(level)] += static_cast<int>(dirs.size());
  return pushWrapper(new WrappedTriplet(*this, histos, level, enableTrueHistogram));
}

#endif
