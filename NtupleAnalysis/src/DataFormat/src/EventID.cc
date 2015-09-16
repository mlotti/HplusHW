#include "DataFormat/interface/EventID.h"
#include "Framework/interface/BranchManager.h"

EventID::EventID():
  fEvent(nullptr),
  fLumi(nullptr),
  fRun(nullptr),
  fNUP(nullptr),
  fPrescale(nullptr)
{}
EventID::~EventID() {}

void EventID::setupBranches(BranchManager& mgr) {
  mgr.book("event", &fEvent);
  mgr.book("lumi", &fLumi);
  mgr.book("run", &fRun);
  mgr.book("NUP", &fNUP);
  mgr.book("prescale", &fPrescale);
}

