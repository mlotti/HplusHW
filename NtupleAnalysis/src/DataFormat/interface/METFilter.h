// -*- c++ -*-
#ifndef DataFormat_METFilter_h
#define DataFormat_METFilter_h

#include "DataFormat/interface/METFilterGenerated.h"

class METFilter: public METFilterGenerated {
public:
  METFilter() {}
  ~METFilter() {}

  void setupBranches(BranchManager& mgr);
};

#endif