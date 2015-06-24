// -*- c++ -*-
#ifndef DataFormat_EventNPU_h
#define DataFormat_EventNPU_h

#include "Framework/interface/Branch.h"

class BranchManager;

class EventNPU {
public:
  EventNPU();
  ~EventNPU();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  EventNPU(const EventNPU&) = delete;
  EventNPU(EventNPU&&) = delete;
  EventNPU& operator=(const EventNPU&) = delete;
  EventNPU& operator=(EventNPU&&) = delete;

  void setupBranches(BranchManager& mgr);

  /// Return the number of primary vertices in the event
  int value() const { return fNPU->value(); }
  /// Return the simulated number of primary vertices in the event
  int simulatedValue() const { return fSimulatedNPU->value(); }

private:
  const Branch<int> *fNPU;
  const Branch<int> *fSimulatedNPU;
};
#endif
