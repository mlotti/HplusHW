// -*- c++ -*-
#ifndef __BASE_SELECTOR__
#define __BASE_SELECTOR__

#include "Rtypes.h"
#include "TBranch.h"
#include "TTree.h"

#include<string>
#include<vector>
#include<algorithm>

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

// Generic branch
template <typename T>
struct BranchTraits {
  typedef T *DataType;
  typedef const T& ReturnType;
  static ReturnType get(const T* data) { return *data; }
};
template <>
struct BranchTraits<bool> {
  typedef bool DataType;
  typedef bool ReturnType;
  static ReturnType get(bool data) { return data; }
};
template <>
struct BranchTraits<int> {
  typedef int DataType;
  typedef int ReturnType;
  static ReturnType get(int data) { return data; }
};
template <>
struct BranchTraits<unsigned int> {
  typedef unsigned int DataType;
  typedef unsigned int ReturnType;
  static ReturnType get(unsigned int data) { return data; }
};
template <>
struct BranchTraits<float> {
  typedef float DataType;
  typedef float ReturnType;
  static ReturnType get(float data) { return data; }
};
template <>
struct BranchTraits<double> {
  typedef double DataType;
  typedef double ReturnType;
  static ReturnType get(double data) { return data; }
};

class BranchBase {
public:
  explicit BranchBase(const std::string& n): name(n), branch(0), entry(0), cached(false) {}
  virtual ~BranchBase();

  bool isValid() const { return branch != 0; }

  void setEntry(Long64_t e) { entry = e; cached = false; }

  const std::string& getName() const { return name; }

protected:
  const std::string name;
  TBranch *branch;
  Long64_t entry;
  bool cached;
};

template <typename T>
class Branch: public BranchBase {
public:
  explicit Branch(const std::string& n): BranchBase(n), data(0) {}
  ~Branch() {}

  void setupBranch(TTree *tree) {
    tree->SetBranchAddress(this->name.c_str(), &data, &this->branch);
  }
  typename BranchTraits<T>::ReturnType value() {
    if(!cached) {
      branch->GetEntry(this->entry);
      cached = true;
    }
    return BranchTraits<T>::get(data);
  }

private:
  typename BranchTraits<T>::DataType data;
};

// Branch manager, to allow multiple analyzer modules
class BranchManager {
public:
  BranchManager();
  ~BranchManager();

  void setTree(TTree *tree) { fTree = tree; }

  template <typename T>
  void book(const std::string& branchName, Branch<T> **returnValue) {
    std::vector<BranchBase *>::iterator found = std::lower_bound(fBranches.begin(), fBranches.end(), branchName, BranchCompare());

    Branch<T> *ptr = 0;
    if(found == fBranches.end() || (*found)->getName() != branchName) {
      ptr = new Branch<T>(branchName);
      fBranches.insert(found, ptr);
    }
    else {
      ptr = dynamic_cast<Branch<T> *>(*found);
    }
    ptr->setupBranch(fTree);
    *returnValue = ptr;
  }

  void setEntry(Long64_t entry) {
    for(size_t i=0; i<fBranches.size(); ++i) {
      fBranches[i]->setEntry(entry);
    }
  }

private:
  struct BranchCompare {
    bool operator()(const BranchBase *a, const std::string& b) const {
      return a->getName() < b;
    }
  };

  TTree *fTree;
  std::vector<BranchBase *> fBranches;
};

/// Event counter
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


/// Selector base class
class BaseSelector {
public:
  BaseSelector();
  virtual ~BaseSelector();

  void setMCStatus(bool isMC_) { fIsMC = isMC_; }

  void setOutputExt(TDirectory *dir) {
    fEventCounter.setOutput(dir);
    setOutput(dir);
  }
  void terminate() {
    fEventCounter.serialize();
  }

  // Implement these
  virtual void setOutput(TDirectory *dir);
  virtual void setupBranches(BranchManager& branchManager);
  virtual bool process(Long64_t entry);

protected:
  bool isMC() const { return fIsMC; }
  bool isData() const { return !isMC(); }

  EventCounter fEventCounter;

private:
  bool fIsMC;
};

#endif
