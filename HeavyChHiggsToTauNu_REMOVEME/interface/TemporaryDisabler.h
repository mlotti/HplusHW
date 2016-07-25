// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TemporaryDisabler_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TemporaryDisabler_h

namespace HPlus {
  /** Helper class to temporarily disable histogram filling
   *
   * Makes use of RAII
   *
   * In the constructor, store the current status of 'enabled' flag,
   * and set it to the requested value. In the destructor, reset the
   * 'enabled' flag to the original value.
   *
   * C++ (RAII) guarantees that the destructor is called when the
   * variable goes out of scope (e.g. because of return)
   */
  template <typename T>
  class TemporaryDisabler {
  public:
    TemporaryDisabler(T& manager, bool enabled):
      fManager(manager),
      fOldEnabled(manager.getEnableStatus())
    {
      fManager.enable(enabled);
    }
    ~TemporaryDisabler() {
      fManager.enable(fOldEnabled);
    }
  private:
    T& fManager;
    bool fOldEnabled;
  };
}

#endif
