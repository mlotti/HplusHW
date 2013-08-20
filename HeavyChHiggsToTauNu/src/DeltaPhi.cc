#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TLorentzVector.h"

namespace HPlus {
  double DeltaPhi::reconstruct(const reco::Candidate& tau, const reco::MET& met) {
    // Construct tau vector, mtau = 1.777 GeV/c2
    TLorentzVector myTau;
    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 
    // Calculate cosine of angle between jet and met direction
	  //    double myEtMiss = TMath::Sqrt(met.px()*met.px() + met.py()*met.py());
    double myEtMiss = met.et();
    double myCosPhi = 100;
    if (myEtMiss > 0 && myTau.Pt() > 0)
      myCosPhi = (myTau.X()*met.px() + myTau.Y()*met.py()) / (myTau.Pt()*myEtMiss);
    double myDeltaPhi = -999;
    if ( myCosPhi < 1) myDeltaPhi =   acos(myCosPhi);
    return myDeltaPhi; 
  }
}
