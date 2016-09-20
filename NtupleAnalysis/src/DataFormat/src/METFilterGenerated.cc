
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/METFilterGenerated.h"

void METFilterGenerated::setupBranches(BranchManager& mgr) {
  mgr.book("METFilter_Flag_CSCTightHalo2015Filter", &fFlag_CSCTightHalo2015Filter);
  mgr.book("METFilter_Flag_CSCTightHaloFilter", &fFlag_CSCTightHaloFilter);
  mgr.book("METFilter_Flag_EcalDeadCellTriggerPrimitiveFilter", &fFlag_EcalDeadCellTriggerPrimitiveFilter);
  mgr.book("METFilter_Flag_HBHENoiseFilter", &fFlag_HBHENoiseFilter);
  mgr.book("METFilter_Flag_HBHENoiseIsoFilter", &fFlag_HBHENoiseIsoFilter);
  mgr.book("METFilter_Flag_eeBadScFilter", &fFlag_eeBadScFilter);
  mgr.book("METFilter_Flag_globalTightHalo2016Filter", &fFlag_globalTightHalo2016Filter);
  mgr.book("METFilter_Flag_goodVertices", &fFlag_goodVertices);
  mgr.book("METFilter_badChargedCandidateFilter", &fBadChargedCandidateFilter);
  mgr.book("METFilter_badPFMuonFilter", &fBadPFMuonFilter);
  mgr.book("METFilter_hbheIsoNoiseToken", &fHbheIsoNoiseToken);
  mgr.book("METFilter_hbheNoiseTokenRun2Loose", &fHbheNoiseTokenRun2Loose);
  mgr.book("METFilter_hbheNoiseTokenRun2Tight", &fHbheNoiseTokenRun2Tight);

}
