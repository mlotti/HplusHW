// -*- c++ -*-
#ifndef DataFormat_VertexInfo_h
#define DataFormat_VertexInfo_h

#include "Framework/interface/Branch.h"

class BranchManager;

class VertexInfo {
public:
  VertexInfo();
  ~VertexInfo();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  VertexInfo(const VertexInfo&) = delete;
  VertexInfo(VertexInfo&&) = delete;
  VertexInfo& operator=(const VertexInfo&) = delete;
  VertexInfo& operator=(VertexInfo&&) = delete;

  void setupBranches(BranchManager& mgr);

  /// Return the number of primary vertices in the event
  short value() const { return fNPU->value(); }
  /// Return the simulated number of primary vertices in the event
  short simulatedValue() const { return fSimulatedNPU->value(); }
  /// Return the distance (in mm) to the vertex closest in z to the PV
  float PVDistanceToClosestVertex() const { return fPVDistanceToClosestVertex->value(); }
  /// Return the distance (in mm) to the next vertex (by sum pt) compared to the selected PV
  float PVDistanceToNextVertex() const { return fPVDistanceToNextVertex->value(); }
  /// Return the x position of the PV in mm
  float pvX() const { return fPVx->value(); }
  /// Return the y position of the PV in mm
  float pvY() const { return fPVy->value(); }
  /// Return the z position of the PV in mm
  float pvZ() const { return fPVz->value(); }

private:
  const Branch<short>   *fNPU;
  const Branch<short> *fSimulatedNPU;
  const Branch<float> *fPVDistanceToClosestVertex;
  const Branch<float> *fPVDistanceToNextVertex;
  const Branch<float> *fPVx;
  const Branch<float> *fPVy;
  const Branch<float> *fPVz;
  
};
#endif
