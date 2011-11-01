#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhiJets.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TLorentzVector.h"

namespace HPlus {
  double DeltaPhiJets::reconstruct(const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets) {
    
    // Construct tau vector, mtau = 1.777 GeV/c2
    TLorentzVector myTau;
    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 

    double maxDeltaPhi = -999;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      double myCosPhi = 100;
      if (iJet->pt() > 0 && myTau.Pt() > 0)
	myCosPhi = (myTau.X()* iJet->px() + myTau.Y()* iJet->py()) / (myTau.Pt()*iJet->pt());
      double myDeltaPhi = -999;
      if ( myCosPhi < 1) myDeltaPhi =   acos(myCosPhi);
      if (myDeltaPhi > maxDeltaPhi) maxDeltaPhi = myDeltaPhi;
    }
    return maxDeltaPhi;
  }
}
