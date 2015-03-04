// -*- c++ -*-
#ifndef Framework_BranchBase_h
#define Framework_BranchBase_h

#include "Rtypes.h"

class TBranch;

class BranchBase {
public:
  explicit BranchBase(const std::string& n): name(n), branch(0), entry(0), cached(false) {}
  virtual ~BranchBase();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  BranchBase(const BranchBase&) = delete;
  BranchBase(BranchBase&&) = delete;
  BranchBase& operator=(const BranchBase&) = delete;
  BranchBase& operator=(BranchBase&&) = delete;

  bool isValid() const { return branch != 0; }

  void setEntry(Long64_t e) { entry = e; cached = false; }

  const std::string& getName() const { return name; }

  virtual std::string getTypeName() const = 0;

  // public only to allow testability
  bool isBranchTypeOk(const std::string& actualType, bool print=true) const;

protected:
  void assertValid() const;

  const std::string name;
  TBranch *branch;
  Long64_t entry;
  bool cached;
};

#endif
