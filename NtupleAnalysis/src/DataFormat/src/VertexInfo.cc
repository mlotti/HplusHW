#include "DataFormat/interface/VertexInfo.h"
#include "Framework/interface/BranchManager.h"

VertexInfo::VertexInfo():
  fNPU(nullptr),
  fSimulatedNPU(nullptr),
  fPVDistanceToClosestVertex(nullptr),
  fPVDistanceToNextVertex(nullptr),
  fPVx(nullptr),
  fPVy(nullptr),
  fPVz(nullptr)
{}
VertexInfo::~VertexInfo() {}

void VertexInfo::setupBranches(BranchManager& mgr) {
  //mgr.book("nPU", &fNPU); // The MC number of PU vertices is not available for data
  mgr.book("nGoodOfflineVertices", &fNPU);
  mgr.book("nPUvertices", &fSimulatedNPU);
  mgr.book("pvDistanceToClosestVertex", &fPVDistanceToClosestVertex);
  mgr.book("pvDistanceToNextVertex", &fPVDistanceToNextVertex);
  mgr.book("pvX", &fPVx);
  mgr.book("pvY", &fPVy);
  mgr.book("pvZ", &fPVz);
}

