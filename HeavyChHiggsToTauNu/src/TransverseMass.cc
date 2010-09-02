#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TLorentzVector.h"

namespace HPlus {
  double TransverseMass::reconstruct(const reco::Candidate& tau, const reco::MET& met) {
    // Construct tau vector, mtau = 1.777 GeV/c2
    TLorentzVector myTau;
    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 
    // Calculate cosine of angle between jet and met direction
    double myEtMiss = sqrt(met.px()*met.px() + met.py()+met.py());
    double myCosPhi = 100;
    if (myEtMiss > 0 && myTau.Pt() > 0)
      myCosPhi = (myTau.X()*met.px() + myTau.Y()*met.py()) / (myTau.Pt()*myEtMiss);
    // Calculate transverse mass
    double myTransverseMass = -999;
    double myTransverseMassSquared = 0;
    if (myCosPhi < 10)
      myTransverseMassSquared = 2 * myTau.Et() * myEtMiss * (1.0-myCosPhi);
    if (myTransverseMassSquared >= 0)
      myTransverseMass = TMath::Sqrt(myTransverseMassSquared);
    return myTransverseMass; 
  }
}
