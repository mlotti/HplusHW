//#######################################################################
// -*- C++ -*-
//       File Name:  EvtTopology.h
// Original Author:  Alexandros Attikis
//         Created:  Mon 4 Oct 2010
//     Description:  Designed to calculate Evt Topology related variables                   
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h

/// ROOT libraries
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>
#include <vector>
#include <Math/Vector3D.h>
#include <Math/Point3D.h>
#include <Riostream.h>
#include <TVector3.h>
#include <TLorentzVector.h>
#include <TRotation.h>
#include <TLorentzRotation.h>
/// C++ libraries
#include <functional>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <assert.h>
/// CMSSW libraries
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MathFunctions.h"

namespace reco {
  class Candidate;
  //  class PtrVector; // delete me
}


struct  AlphaStruc{
  float fAlphaT;
  float fJt; // Jt = Ht - TauJetEt - LdgJetEt
  float fHt;
  float fDeltaHt;
  float fMHt;
  vector<float> vDiJetMassesNoTau;
};

namespace HPlus {
  class EvtTopology {
  public:

    static AlphaStruc alphaT( const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);

  private:
    
  };
}

#endif
