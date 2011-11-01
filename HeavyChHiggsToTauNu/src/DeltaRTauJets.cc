#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaRTauJets.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"
#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"

namespace HPlus {
  double DeltaRTauJets::reconstruct(const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets) {
    
    // Construct tau vector, mtau = 1.777 GeV/c2
    TLorentzVector myTau;
    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 

    double maxDeltaR = -999;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      double deltaR = ROOT::Math::VectorUtil::DeltaR(myTau, iJet->p4());

      if (deltaR > maxDeltaR) maxDeltaR = deltaR;
    }
    return maxDeltaR;
  }
}
