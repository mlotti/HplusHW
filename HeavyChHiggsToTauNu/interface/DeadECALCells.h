// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_DeadECALCells_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_DeadECALCells_h


#include "DataFormats/Candidate/interface/Candidate.h"
#include <vector>

namespace HPlus {
  class DeadECALCells {
  public:
    DeadECALCells();
    ~DeadECALCells();

    bool ObjectHitsDeadECALCell(const edm::Ptr<reco::Candidate>& candidate, double deltaR = 0.07) const;

  private:
    std::vector<double> fECALDeadCellEtaTable;
    std::vector<double> fECALDeadCellPhiTable;

  };
}

#endif