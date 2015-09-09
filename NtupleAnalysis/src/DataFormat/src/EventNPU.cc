#include "DataFormat/interface/EventNPU.h"
#include "Framework/interface/BranchManager.h"

EventNPU::EventNPU():
  fNPU(nullptr),
  fSimulatedNPU(nullptr),
  fPVz(nullptr)
{}
EventNPU::~EventNPU() {}

void EventNPU::setupBranches(BranchManager& mgr) {
  //mgr.book("nPU", &fNPU); // The MC number of PU vertices is not available for data
  mgr.book("nGoodOfflineVertices", &fNPU);
  mgr.book("nPUvertices", &fSimulatedNPU);
  mgr.book("pvZ", &fPVz);
}

