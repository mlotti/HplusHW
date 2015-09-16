// -*- c++ -*-
#ifndef DataFormat_METFilter_h
#define DataFormat_METFilter_h

#include "DataFormat/interface/METFilterGenerated.h"

class METFilter: public METFilterGenerated {
public:
  METFilter() {}
  ~METFilter() {}

  void setupBranches(BranchManager& mgr);
  
  void checkDiscriminatorValidity(const std::string& name) const;
  void checkDiscriminatorValidity(const std::vector<std::string>& names) const;
};

#endif