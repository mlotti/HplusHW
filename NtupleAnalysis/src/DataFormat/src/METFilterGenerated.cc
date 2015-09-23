
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/METFilterGenerated.h"

void METFilterGenerated::setupBranches(BranchManager& mgr) {
  mgr.book("METFilter_Flag_CSCTightHaloFilter", &fCSCTightHaloFilter);
  mgr.book("METFilter_Flag_eeBadScFilter", &fEeBadScFilter);
  mgr.book("METFilter_Flag_goodVertices", &fGoodVertices);

}
