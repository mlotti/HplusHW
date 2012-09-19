// -*- c++ -*-
#ifndef __BASE_SELECTOR__
#define __BASE_SELECTOR__

#include "Rtypes.h"

#include<string>
#include<vector>

class TTree;
class TDirectory;
class TH1;

// Wrappers to call automatically TH1::Sumw2() after the histogram creation
// If the function for some number of arguments is missing, please go a head and add one
template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4, 
         typename Arg5>
T* makeTH(const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4, const Arg5& a5) {
  T *histo = new T(a1, a2, a3, a4, a5);
  histo->Sumw2();
  return histo;
}

template<typename T, typename Arg1, typename Arg2, typename Arg3, typename Arg4, 
         typename Arg5, typename Arg6, typename Arg7, typename Arg8>
T* makeTH(const Arg1& a1, const Arg2& a2, const Arg3& a3, const Arg4& a4, const Arg5& a5,
                 const Arg6& a6, const Arg7& a7, const Arg8& a8) {
  T *histo = new T(a1, a2, a3, a4, a5, a6, a7, a8);
  histo->Sumw2();
  return histo;
}

class EventCounter {
public:
  class Count {
  public:
    ~Count();

    void increment();

  private:
    Count(); // NOT IMPLEMENTED
    Count(EventCounter& ec, size_t index);

    EventCounter& fEventCounter;
    size_t fIndex;
  };

  EventCounter();
  ~EventCounter();

  Count addCounter(const std::string& name);
  void incrementCount(size_t countIndex);
  void setWeight(double weight) { fWeight = weight; }

  void setOutput(TDirectory *dir);
  void serialize();

private:
  std::vector<std::string> labels;
  std::vector<long int> values;
  std::vector<double> weights;
  std::vector<double> weightsSquared;

  double fWeight;

  TH1 *counter;
  TH1 *weightedCounter;
};

inline
void EventCounter::Count::increment() {
  fEventCounter.incrementCount(fIndex);
}

class BaseSelector {
public:
  BaseSelector();
  virtual ~BaseSelector();

  void setOutputExt(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    setOutput(dir);
  }
  void terminate() {
    fEventCounter.serialize();
  }

  // Implement these
  virtual void setOutput(TDirectory *dir);
  virtual void setupBranches(TTree *tree);
  virtual bool process(Long64_t entry);

protected:
  EventCounter fEventCounter;
};

#endif
