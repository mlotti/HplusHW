// -*- c++ -*-
#ifndef Framework_BranchBase_h
#define Framework_BranchBase_h

#include "Rtypes.h"

class TBranch;

class BranchBase {
public:
  explicit BranchBase(const std::string& n): name(n), branch(0), entry(0), cached(false) {}
  virtual ~BranchBase();

  bool isValid() const { return branch != 0; }

  void setEntry(Long64_t e) { entry = e; cached = false; }

  const std::string& getName() const { return name; }

  virtual const char *getTypeidName() const = 0;

protected:
  void assertValid() const;

  const std::string name;
  TBranch *branch;
  Long64_t entry;
  bool cached;
};

#endif
