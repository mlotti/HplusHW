// -*- c++ -*-
#ifndef DataFormat_METFilter_h
#define DataFormat_METFilter_h

#include "DataFormat/interface/METFilterGenerated.h"

class METFilter: public METFilterGenerated {
public:
  METFilter() {}
  ~METFilter() {}

  void setupBranches(BranchManager& mgr);
  // Discriminators
  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }
  void checkDiscriminatorValidity(const std::string& name) const;
  void checkDiscriminatorValidity(const std::vector<std::string>& names) const;

  std::vector<bool> getConfigurableDiscriminatorValues() const {
    std::vector<bool> v;
    for (auto& disc: fConfigurableDiscriminators)
      v.push_back(disc->value());
    return v;
  }
  std::vector<std::string> getConfigurableDiscriminatorNames() const {
    return fConfigurableDiscriminatorNames;
  }
  
protected:
  std::vector<const Branch<bool> *> fConfigurableDiscriminators;
  
private:
  std::vector<std::string> fConfigurableDiscriminatorNames;
};

#endif
