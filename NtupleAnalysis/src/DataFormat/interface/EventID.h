// -*- c++ -*-
#ifndef DataFormat_EventID_h
#define DataFormat_EventID_h

#include "Framework/interface/Branch.h"

class BranchManager;

class EventID {
public:
  EventID();
  ~EventID();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  EventID(const EventID&) = delete;
  EventID(EventID&&) = delete;
  EventID& operator=(const EventID&) = delete;
  EventID& operator=(EventID&&) = delete;

  void setupBranches(BranchManager& mgr);

  unsigned long long event() { return fEvent->value(); }
  unsigned int       lumi()  { return fLumi->value(); }
  unsigned int       run()   { return fRun->value(); }

private:
  Branch<unsigned long long> *fEvent;
  Branch<unsigned int> *fLumi;
  Branch<unsigned int> *fRun;
};

#endif
