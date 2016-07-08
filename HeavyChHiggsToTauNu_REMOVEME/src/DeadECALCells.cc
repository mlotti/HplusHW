#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeadECALCells.h"

namespace HPlus {

  DeadECALCells::DeadECALCells() {
    // Setup coordinates of center of dead ECAL cells
    // To obtain from root file, use
    //   TH1* h = (TH1*)_file0->Get("ecalveto")     
    //   for (int i = 1; i <= h->GetNbinsX()+1; ++i) { for (int j = 1; j <= h->GetNbinsY()+1; ++j) { if (h->GetBinContent(i,j)>0) { cout << "fECALDeadCellEtaTable.push_back(" << h->GetXaxis()->GetBinCenter(i) << "); fECALDeadCellPhiTable.push_back(" << h->GetYaxis()->GetBinCenter(j) << ");" << endl; }}}
    fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-1.45); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(-1.25); fECALDeadCellPhiTable.push_back(-1.1775);
    fECALDeadCellEtaTable.push_back(-1.15); fECALDeadCellPhiTable.push_back(-1.1775);
    fECALDeadCellEtaTable.push_back(-0.95); fECALDeadCellPhiTable.push_back(2.04972);
    fECALDeadCellEtaTable.push_back(-0.85); fECALDeadCellPhiTable.push_back(2.04972);
    fECALDeadCellEtaTable.push_back(-0.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(-0.45); fECALDeadCellPhiTable.push_back(-1.9625);
    fECALDeadCellEtaTable.push_back(-0.35); fECALDeadCellPhiTable.push_back(0.218056);
    fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.130833);
    fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.218056);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(-2.57306);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.130833);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(-2.57306);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.915833);
    fECALDeadCellEtaTable.push_back(0.15); fECALDeadCellPhiTable.push_back(1.78806);
    fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(1.70083);
    fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(2.83472);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(0.654167);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(1.70083);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(2.83472);
    fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(0.654167);
    fECALDeadCellEtaTable.push_back(1.15); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(1.25); fECALDeadCellPhiTable.push_back(-0.479722);
    fECALDeadCellEtaTable.push_back(1.35); fECALDeadCellPhiTable.push_back(-0.479722);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(-0.218056);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(2.48583);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(2.7475);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(0.828611);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.828611);
    fECALDeadCellEtaTable.push_back(1.85); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(2.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.915833);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.828611);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.741389);
  }

  DeadECALCells::~DeadECALCells() {
    fECALDeadCellEtaTable.clear();
    fECALDeadCellPhiTable.clear();
  }

  bool DeadECALCells::ObjectHitsDeadECALCell(const edm::Ptr<reco::Candidate>& candidate, double deltaR) const {
    double myEta = candidate->eta();
    double myPhi = candidate->phi();
    double myHalfCellSize = 3.14159265 / 180.0;
    size_t myTableSize = fECALDeadCellEtaTable.size();
    for (size_t i = 0; i < myTableSize; ++i) {
      double myDeltaEta = myEta - fECALDeadCellEtaTable[i];
      double myDeltaPhi = myPhi - fECALDeadCellPhiTable[i];
      //if (myDeltaEta <= myHalfCellSize || myDeltaPhi <= myHalfCellSize) return false;
      double myDeltaR = std::sqrt(myDeltaEta*myDeltaEta + myDeltaPhi*myDeltaPhi);
      if (myDeltaR < deltaR) return false;
    }
    return true;
  }

}

